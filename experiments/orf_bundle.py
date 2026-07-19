#!/usr/bin/env python3
"""Crash-safe, hash-bound publication for ORF experiment attempts.

The helper deliberately contains no scientific logic.  A caller computes results in
memory, writes the declared artifacts through :class:`AttemptBundle`, and calls
``complete``.  Until ``complete`` returns, no final attempt directory is visible.
"""

from __future__ import annotations

import ctypes
import errno
import hashlib
import json
import os
import re
import stat
import uuid
from pathlib import Path
from typing import Callable, Iterable, Mapping, TextIO


SCHEMA_VERSION = "orf-complete-bundle-v1"
COMPLETE_NAME = "COMPLETE.json"
RENAME_NOREPLACE = 1
AT_FDCWD = -100
FailureHook = Callable[[str], None]


class BundleError(RuntimeError):
    """The attempt bundle is unsafe, incomplete, or inconsistent."""


def canonical_json(value: object) -> str:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _fsync_directory(path: Path) -> None:
    required_flags = ("O_DIRECTORY", "O_NOFOLLOW")
    if any(not hasattr(os, name) for name in required_flags):
        raise BundleError("directory no-follow primitives are unavailable")
    descriptor = os.open(
        path,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0),
    )
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def rename_noreplace(source: Path, destination: Path) -> None:
    """Atomically rename ``source`` while refusing to replace ``destination``.

    Linux/glibc ``renameat2`` is a hard dependency.  Falling back to ``os.rename``
    would permit platform-dependent replacement and is therefore intentionally
    forbidden.
    """

    libc = ctypes.CDLL(None, use_errno=True)
    try:
        renameat2 = libc.renameat2
    except AttributeError as exc:
        raise BundleError("glibc renameat2 is unavailable; refusing unsafe publish") from exc
    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    result = renameat2(
        AT_FDCWD,
        os.fsencode(source),
        AT_FDCWD,
        os.fsencode(destination),
        RENAME_NOREPLACE,
    )
    if result != 0:
        error_number = ctypes.get_errno()
        if error_number == errno.EEXIST:
            raise FileExistsError(error_number, os.strerror(error_number), destination)
        raise OSError(error_number, os.strerror(error_number), destination)


def _lexical_direct_child(path: Path, resolved_parent: Path) -> Path:
    """Return an absolute normalized child path without resolving the child.

    ``resolved_parent`` is trusted only after the caller resolves it independently.
    The child is deliberately normalized with string/path operations, never
    ``Path.resolve()``, so a symlink at the child name cannot rewrite its identity.
    """

    parent = Path(resolved_parent)
    if not parent.is_absolute():
        raise BundleError("allowed parent must already be resolved and absolute")
    lexical = Path(os.path.abspath(os.path.normpath(os.fspath(path))))
    if lexical.parent != parent:
        raise BundleError("attempt directory must be a direct child of the allowed parent")
    return lexical


def _require_absent_child(path: Path, resolved_parent: Path) -> Path:
    lexical = _lexical_direct_child(path, resolved_parent)
    if os.path.lexists(lexical):
        # lstat inspects the named child itself; it never follows a live symlink.
        os.lstat(lexical)
        raise FileExistsError(f"attempt directory already exists: {lexical}")
    return lexical


def _require_existing_directory_child(
    path: Path, resolved_parent: Path
) -> tuple[Path, os.stat_result]:
    lexical = _lexical_direct_child(path, resolved_parent)
    if not os.path.lexists(lexical):
        raise FileNotFoundError(f"attempt directory does not exist: {lexical}")
    metadata = os.lstat(lexical)
    if stat.S_ISLNK(metadata.st_mode):
        raise BundleError(f"attempt path is a symlink: {lexical}")
    if not stat.S_ISDIR(metadata.st_mode):
        raise BundleError(f"attempt path is not a directory: {lexical}")
    return lexical, metadata


def _read_attempt_files(
    attempt: Path, initial_metadata: os.stat_result
) -> dict[str, bytes]:
    """Read one nonsymlink directory through a stable, no-follow descriptor."""

    required_flags = ("O_DIRECTORY", "O_NOFOLLOW")
    if any(not hasattr(os, name) for name in required_flags):
        raise BundleError("directory no-follow primitives are unavailable")
    flags = (
        os.O_RDONLY
        | os.O_DIRECTORY
        | os.O_NOFOLLOW
        | getattr(os, "O_CLOEXEC", 0)
    )
    try:
        directory_fd = os.open(attempt, flags)
    except OSError as exc:
        raise BundleError("attempt directory could not be opened without following") from exc
    try:
        opened_metadata = os.fstat(directory_fd)
        initial_identity = (initial_metadata.st_dev, initial_metadata.st_ino)
        opened_identity = (opened_metadata.st_dev, opened_metadata.st_ino)
        if initial_identity != opened_identity or not stat.S_ISDIR(opened_metadata.st_mode):
            raise BundleError("attempt directory changed during verification")
        names = os.listdir(directory_fd)
        if len(names) != len(set(names)):
            raise BundleError("attempt directory returned duplicate entries")
        values: dict[str, bytes] = {}
        for name in names:
            try:
                file_fd = os.open(
                    name,
                    os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0),
                    dir_fd=directory_fd,
                )
            except OSError as exc:
                raise BundleError(f"bundle entry could not be opened safely: {name}") from exc
            try:
                file_metadata = os.fstat(file_fd)
                if not stat.S_ISREG(file_metadata.st_mode):
                    raise BundleError(f"bundle contains a non-regular entry: {name}")
                chunks: list[bytes] = []
                while True:
                    chunk = os.read(file_fd, 1024 * 1024)
                    if not chunk:
                        break
                    chunks.append(chunk)
                final_file_metadata = os.fstat(file_fd)
                identity_fields = (
                    "st_dev",
                    "st_ino",
                    "st_size",
                    "st_mtime_ns",
                    "st_ctime_ns",
                )
                if any(
                    getattr(file_metadata, field) != getattr(final_file_metadata, field)
                    for field in identity_fields
                ):
                    raise BundleError(f"bundle entry changed while being read: {name}")
                named_metadata = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                if stat.S_ISLNK(named_metadata.st_mode) or (
                    named_metadata.st_dev,
                    named_metadata.st_ino,
                ) != (file_metadata.st_dev, file_metadata.st_ino):
                    raise BundleError(f"bundle entry was replaced while being read: {name}")
                values[name] = b"".join(chunks)
            finally:
                os.close(file_fd)
        if set(os.listdir(directory_fd)) != set(names):
            raise BundleError("attempt contents changed during verification")
        final_metadata = os.lstat(attempt)
        if stat.S_ISLNK(final_metadata.st_mode) or (
            final_metadata.st_dev,
            final_metadata.st_ino,
        ) != opened_identity:
            raise BundleError("attempt path changed during verification")
        return values
    finally:
        os.close(directory_fd)


def _relative_binding_path(repo_root: Path, raw_path: Path) -> tuple[str, Path]:
    root = repo_root.resolve(strict=True)
    candidate = raw_path if raw_path.is_absolute() else root / raw_path
    if candidate.is_symlink():
        raise BundleError(f"binding path is a symlink: {raw_path}")
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise BundleError(f"binding path leaves repository: {raw_path}")
    if not resolved.is_file() or resolved.is_symlink():
        raise BundleError(f"binding path is not a regular nonsymlink file: {raw_path}")
    return resolved.relative_to(root).as_posix(), resolved


def binding_hashes(repo_root: Path, binding_paths: Iterable[Path]) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for raw_path in binding_paths:
        relative, resolved = _relative_binding_path(repo_root, Path(raw_path))
        if relative in bindings:
            raise BundleError(f"duplicate binding path: {relative}")
        bindings[relative] = file_sha256(resolved)
    if not bindings:
        raise BundleError("at least one binding input is required")
    return dict(sorted(bindings.items()))


def _validate_artifact_names(names: Iterable[str]) -> tuple[str, ...]:
    values = tuple(names)
    if not values or len(set(values)) != len(values):
        raise BundleError("artifact names must be a nonempty unique set")
    for name in values:
        path = Path(name)
        if (
            name == COMPLETE_NAME
            or not name
            or path.name != name
            or name in {".", ".."}
            or name.startswith(".")
        ):
            raise BundleError(f"artifact must be a plain visible filename: {name!r}")
    if "run.log" not in values:
        raise BundleError("run.log must be one of the declared artifacts")
    return tuple(sorted(values))


def _manifest_records(values: Mapping[str, str]) -> list[dict[str, str]]:
    return [
        {"path": path, "sha256": digest}
        for path, digest in sorted(values.items())
    ]


def _parse_records(value: object, field: str) -> dict[str, str]:
    if not isinstance(value, list) or not value:
        raise BundleError(f"manifest {field} must be a nonempty list")
    parsed: dict[str, str] = {}
    for record in value:
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            raise BundleError(f"manifest {field} record has the wrong schema")
        path = record.get("path")
        digest = record.get("sha256")
        if (
            not isinstance(path, str)
            or not isinstance(digest, str)
            or not re.fullmatch(r"[0-9a-f]{64}", digest)
            or path in parsed
        ):
            raise BundleError(f"manifest {field} record is malformed or duplicated")
        parsed[path] = digest
    return parsed


def verify_complete_bundle(
    attempt_dir: Path,
    *,
    repo_root: Path,
    allowed_parent: Path,
    expected_attempt_dir: Path,
    expected_command: str,
    expected_bindings: Mapping[str, str],
    expected_artifacts: Iterable[str],
) -> dict[str, object]:
    """Verify one final bundle against exact identity, inputs, files, and hashes."""

    root = repo_root.resolve(strict=True)
    parent = Path(allowed_parent).resolve(strict=True)
    if not parent.is_relative_to(root):
        raise BundleError("allowed parent must be inside the repository root")
    attempt, attempt_metadata = _require_existing_directory_child(
        Path(attempt_dir), parent
    )
    expected_attempt, _ = _require_existing_directory_child(
        Path(expected_attempt_dir), parent
    )
    if attempt != expected_attempt:
        raise BundleError("bundle path is not the expected final attempt identity")
    artifact_names = _validate_artifact_names(expected_artifacts)
    expected_binding_map = dict(sorted(expected_bindings.items()))
    if not expected_binding_map:
        raise BundleError("expected bindings cannot be empty")
    for relative, digest in expected_binding_map.items():
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise BundleError(f"invalid expected binding hash: {relative}")
        actual_relative, resolved = _relative_binding_path(root, Path(relative))
        if actual_relative != relative or file_sha256(resolved) != digest:
            raise BundleError(f"binding is stale or mismatched: {relative}")

    bundle_files = _read_attempt_files(attempt, attempt_metadata)
    discovered = set(bundle_files)
    expected_file_set = set(artifact_names) | {COMPLETE_NAME}
    if discovered != expected_file_set:
        raise BundleError("bundle file set has missing or extra entries")

    try:
        complete_text = bundle_files[COMPLETE_NAME].decode("utf-8")
        manifest = json.loads(complete_text)
    except (KeyError, UnicodeError, json.JSONDecodeError) as exc:
        raise BundleError("COMPLETE.json is unreadable or malformed") from exc
    if complete_text != canonical_json(manifest):
        raise BundleError("COMPLETE.json is not in canonical form")
    if not isinstance(manifest, dict) or set(manifest) != {
        "artifacts",
        "attempt",
        "bindings",
        "canonical_command",
        "schema_version",
        "status",
    }:
        raise BundleError("COMPLETE.json root schema differs from protocol")
    expected_relative = attempt.relative_to(root).as_posix()
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise BundleError("COMPLETE.json schema version mismatch")
    if manifest.get("status") != "COMPLETE":
        raise BundleError("COMPLETE.json status is not COMPLETE")
    if manifest.get("canonical_command") != expected_command:
        raise BundleError("COMPLETE.json command mismatch")
    if manifest.get("attempt") != {
        "id": attempt.name,
        "path": expected_relative,
    }:
        raise BundleError("COMPLETE.json attempt identity mismatch")

    manifest_bindings = _parse_records(manifest.get("bindings"), "bindings")
    if manifest_bindings != expected_binding_map:
        raise BundleError("COMPLETE.json binding set or hashes mismatch")
    manifest_artifacts = _parse_records(manifest.get("artifacts"), "artifacts")
    if set(manifest_artifacts) != set(artifact_names):
        raise BundleError("COMPLETE.json artifact set mismatch")
    for name, digest in manifest_artifacts.items():
        if hashlib.sha256(bundle_files[name]).hexdigest() != digest:
            raise BundleError(f"artifact hash mismatch: {name}")
    try:
        first_line = bundle_files["run.log"].decode("utf-8").split("\n", 1)[0]
    except UnicodeError as exc:
        raise BundleError("run.log is not valid UTF-8") from exc
    if first_line != expected_command:
        raise BundleError("run.log first line is not the canonical command")
    return manifest


class AttemptBundle:
    """One-use staged attempt that publishes atomically only when complete."""

    def __init__(
        self,
        attempt_dir: Path,
        *,
        repo_root: Path,
        allowed_parent: Path,
        canonical_command: str,
        binding_paths: Iterable[Path],
        expected_artifacts: Iterable[str],
        failure_hook: FailureHook | None = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve(strict=True)
        self.allowed_parent = Path(allowed_parent).resolve(strict=True)
        if not self.allowed_parent.is_relative_to(self.repo_root):
            raise BundleError("allowed parent must be inside the repository root")
        self.attempt_dir = _require_absent_child(
            Path(attempt_dir), self.allowed_parent
        )
        if "\n" in canonical_command or "\r" in canonical_command or not canonical_command:
            raise BundleError("canonical command must be one nonempty line")
        self.canonical_command = canonical_command
        self.binding_paths = tuple(Path(path) for path in binding_paths)
        self._initial_bindings = binding_hashes(self.repo_root, self.binding_paths)
        self.expected_artifacts = _validate_artifact_names(expected_artifacts)
        self.failure_hook = failure_hook
        self.staging_dir: Path | None = None
        self._log: TextIO | None = None
        self._written: set[str] = set()
        self._published = False
        self._completed = False

    def _hook(self, point: str) -> None:
        if self.failure_hook is not None:
            self.failure_hook(point)

    def __enter__(self) -> AttemptBundle:
        try:
            _require_absent_child(self.attempt_dir, self.allowed_parent)
            self._hook("before:staging_create")
            staging_name = f".{self.attempt_dir.name}.staging-{uuid.uuid4().hex}"
            self.staging_dir = self.attempt_dir.parent / staging_name
            self.staging_dir.mkdir(mode=0o700, exist_ok=False)
            self._hook("after:staging_create")
            self._hook("before:artifact:run.log")
            self._log = (self.staging_dir / "run.log").open(
                "x", encoding="utf-8", newline="\n"
            )
            self._log.write(self.canonical_command + "\n")
            self._log.flush()
            self._written.add("run.log")
            self._hook("after:artifact:run.log")
            return self
        except BaseException:
            self._abort()
            raise

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> bool:
        if exc_type is not None or not self._completed:
            self._abort()
        return False

    def _require_active(self) -> Path:
        if self.staging_dir is None or self._completed:
            raise BundleError("attempt bundle is not active")
        return self.staging_dir

    def log_line(self, line: str) -> None:
        if self._log is None or self._log.closed:
            raise BundleError("run.log is not open")
        if "\n" in line or "\r" in line:
            raise BundleError("run.log entries must be single lines")
        self._log.write(line + "\n")

    def log_metrics(self, metrics: Mapping[str, str]) -> None:
        for name, value in metrics.items():
            if re.fullmatch(r"[a-z_]+", name) is None:
                raise BundleError(f"metric name must contain lowercase words only: {name}")
            self.log_line(f"{name}: {value}")

    def write_bytes(self, name: str, data: bytes) -> None:
        staging = self._require_active()
        _validate_artifact_names(("run.log", name))
        if name not in self.expected_artifacts:
            raise BundleError(f"undeclared artifact: {name}")
        if name in self._written:
            raise BundleError(f"artifact already written: {name}")
        self._hook(f"before:artifact:{name}")
        with (staging / name).open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        self._written.add(name)
        self._hook(f"after:artifact:{name}")

    def write_text(self, name: str, text: str) -> None:
        self.write_bytes(name, text.encode("utf-8"))

    def complete(self) -> dict[str, object]:
        staging = self._require_active()
        if self._written != set(self.expected_artifacts):
            missing = sorted(set(self.expected_artifacts) - self._written)
            extra = sorted(self._written - set(self.expected_artifacts))
            raise BundleError(f"artifact set incomplete; missing={missing}, extra={extra}")
        if self._log is None or self._log.closed:
            raise BundleError("run.log was not owned by the active bundle")
        try:
            self._hook("before:log_close")
            self._log.flush()
            os.fsync(self._log.fileno())
            self._log.close()
            self._hook("after:log_close")

            self._hook("before:binding_hash")
            bindings = binding_hashes(self.repo_root, self.binding_paths)
            if bindings != self._initial_bindings:
                raise BundleError("a binding input changed during the attempt")
            self._hook("after:binding_hash")

            self._hook("before:artifact_hash")
            artifacts = {
                name: file_sha256(staging / name) for name in self.expected_artifacts
            }
            self._hook("after:artifact_hash")
            manifest: dict[str, object] = {
                "artifacts": _manifest_records(artifacts),
                "attempt": {
                    "id": self.attempt_dir.name,
                    "path": self.attempt_dir.relative_to(self.repo_root).as_posix(),
                },
                "bindings": _manifest_records(bindings),
                "canonical_command": self.canonical_command,
                "schema_version": SCHEMA_VERSION,
                "status": "COMPLETE",
            }

            self._hook("before:complete_write")
            temporary = staging / f".{COMPLETE_NAME}.tmp-{uuid.uuid4().hex}"
            with temporary.open("xb") as handle:
                handle.write(canonical_json(manifest).encode("utf-8"))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, staging / COMPLETE_NAME)
            self._hook("after:complete_write")

            self._hook("before:stage_fsync")
            _fsync_directory(staging)
            self._hook("after:stage_fsync")

            self._hook("before:publish")
            rename_noreplace(staging, self.attempt_dir)
            self._published = True
            self._hook("after:publish")

            self._hook("before:parent_fsync")
            _fsync_directory(self.attempt_dir.parent)
            self._hook("after:parent_fsync")

            self._hook("before:self_verify")
            verified = verify_complete_bundle(
                self.attempt_dir,
                repo_root=self.repo_root,
                allowed_parent=self.allowed_parent,
                expected_attempt_dir=self.attempt_dir,
                expected_command=self.canonical_command,
                expected_bindings=bindings,
                expected_artifacts=self.expected_artifacts,
            )
            self._hook("after:self_verify")
            self._completed = True
            return verified
        except BaseException:
            self._abort()
            raise

    def _abort(self) -> None:
        if self._completed:
            return
        if self._log is not None and not self._log.closed:
            try:
                self._log.flush()
                os.fsync(self._log.fileno())
            finally:
                self._log.close()
        source: Path | None = None
        if self._published and os.path.lexists(self.attempt_dir):
            published_metadata = os.lstat(self.attempt_dir)
            if stat.S_ISLNK(published_metadata.st_mode) or not stat.S_ISDIR(
                published_metadata.st_mode
            ):
                raise BundleError("published attempt identity changed during abort")
            source = self.attempt_dir
        elif self.staging_dir is not None and os.path.lexists(self.staging_dir):
            staging_metadata = os.lstat(self.staging_dir)
            if stat.S_ISLNK(staging_metadata.st_mode) or not stat.S_ISDIR(
                staging_metadata.st_mode
            ):
                raise BundleError("staging identity changed during abort")
            source = self.staging_dir
        if source is None:
            return
        failed = self.attempt_dir.parent / (
            f".{self.attempt_dir.name}.failed-{uuid.uuid4().hex}"
        )
        try:
            complete = source / COMPLETE_NAME
            if os.path.lexists(complete):
                complete_metadata = os.lstat(complete)
                if stat.S_ISLNK(complete_metadata.st_mode) or not stat.S_ISREG(
                    complete_metadata.st_mode
                ):
                    raise BundleError("completion marker identity changed during abort")
                complete.unlink()
                _fsync_directory(source)
            rename_noreplace(source, failed)
            _fsync_directory(self.attempt_dir.parent)
        finally:
            self._published = False
            self.staging_dir = None
