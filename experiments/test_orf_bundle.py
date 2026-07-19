#!/usr/bin/env python3
"""Synthetic temporary-directory tests for the ORF bundle transaction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


HELPER_PATH = Path(__file__).resolve().with_name("orf_bundle.py")
SPEC = importlib.util.spec_from_file_location("orf_bundle_under_test", HELPER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load orf_bundle.py")
BUNDLE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BUNDLE
SPEC.loader.exec_module(BUNDLE)


COMMAND = "python -I fake_runner.py --attempt-dir runs/fake"
ARTIFACTS = ("run.log", "alpha.txt", "beta.txt")
STRUCTURAL_HOOK_POINTS = (
    "before:staging_create",
    "after:staging_create",
    "before:artifact:run.log",
    "after:artifact:run.log",
    "before:artifact:alpha.txt",
    "after:artifact:alpha.txt",
    "before:artifact:beta.txt",
    "after:artifact:beta.txt",
    "before:log_close",
    "after:log_close",
    "before:binding_hash",
    "after:binding_hash",
    "before:artifact_hash",
    "after:artifact_hash",
    "before:complete_write",
    "after:complete_write",
    "before:stage_fsync",
    "after:stage_fsync",
    "before:publish",
    "after:publish",
    "before:parent_fsync",
    "after:parent_fsync",
    "before:self_verify",
    "after:self_verify",
)


class InjectedFailure(RuntimeError):
    pass


class BundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="orf-bundle-test-")
        self.root = Path(self.temporary.name) / "repo"
        self.runs = self.root / "runs"
        self.runs.mkdir(parents=True)
        (self.root / "fake_runner.py").write_text("# runner\n", encoding="utf-8")
        (self.root / "support.py").write_text("# support\n", encoding="utf-8")
        self.binding_paths = (Path("fake_runner.py"), Path("support.py"))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def expected_bindings(self) -> dict[str, str]:
        return BUNDLE.binding_hashes(self.root, self.binding_paths)

    def publish(
        self, name: str, failure_hook=None
    ) -> tuple[Path, dict[str, object]]:
        attempt = self.runs / name
        with BUNDLE.AttemptBundle(
            attempt,
            repo_root=self.root,
            allowed_parent=self.runs,
            canonical_command=COMMAND,
            binding_paths=self.binding_paths,
            expected_artifacts=ARTIFACTS,
            failure_hook=failure_hook,
        ) as writer:
            writer.write_text("alpha.txt", "alpha\n")
            writer.write_text("beta.txt", "beta\n")
            writer.log_metrics({"fake_metric": "one"})
            manifest = writer.complete()
        return attempt, manifest

    def verify(self, attempt: Path, *, bindings=None) -> dict[str, object]:
        return BUNDLE.verify_complete_bundle(
            attempt,
            repo_root=self.root,
            allowed_parent=self.runs,
            expected_attempt_dir=attempt,
            expected_command=COMMAND,
            expected_bindings=self.expected_bindings() if bindings is None else bindings,
            expected_artifacts=ARTIFACTS,
        )

    def assert_rejected(self, attempt: Path, *, bindings=None) -> None:
        with self.assertRaises((BUNDLE.BundleError, FileNotFoundError)):
            self.verify(attempt, bindings=bindings)

    def test_failure_injection_at_every_structural_boundary_never_verifies(self) -> None:
        for index, failure_point in enumerate(STRUCTURAL_HOOK_POINTS):
            with self.subTest(failure_point=failure_point):
                attempt = self.runs / f"failure-{index}"

                def fail_at(point: str, expected: str = failure_point) -> None:
                    if point == expected:
                        raise InjectedFailure(point)

                with self.assertRaises(InjectedFailure):
                    self.publish(attempt.name, fail_at)
                self.assertFalse(attempt.exists())
                failed = sorted(self.runs.glob(f".{attempt.name}.failed-*"))
                if failure_point != "before:staging_create":
                    self.assertEqual(len(failed), 1)
                for failed_attempt in failed:
                    self.assertFalse((failed_attempt / BUNDLE.COMPLETE_NAME).exists())
                    self.assert_rejected(failed_attempt)

    def test_successful_fake_bundle_verifies(self) -> None:
        attempt, manifest = self.publish("success")
        self.assertEqual(manifest, self.verify(attempt))
        self.assertEqual(
            (attempt / "run.log").read_text(encoding="utf-8").splitlines()[0],
            COMMAND,
        )

    def test_second_attempt_cannot_change_a_completed_bundle(self) -> None:
        attempt, _ = self.publish("immutable")
        before = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in attempt.iterdir()
        }
        with self.assertRaises(FileExistsError):
            self.publish("immutable")
        after = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in attempt.iterdir()
        }
        self.assertEqual(before, after)
        self.verify(attempt)

    def test_corrupting_each_artifact_is_rejected(self) -> None:
        for index, artifact in enumerate(ARTIFACTS):
            with self.subTest(artifact=artifact):
                attempt, _ = self.publish(f"corrupt-{index}")
                with (attempt / artifact).open("ab") as handle:
                    handle.write(b"corruption")
                self.assert_rejected(attempt)

    def test_missing_and_extra_files_are_rejected(self) -> None:
        missing, _ = self.publish("missing")
        (missing / "alpha.txt").unlink()
        self.assert_rejected(missing)

        extra, _ = self.publish("extra")
        (extra / "unexpected.txt").write_text("unexpected\n", encoding="utf-8")
        self.assert_rejected(extra)

    def test_missing_and_malformed_complete_are_rejected(self) -> None:
        missing, _ = self.publish("missing-complete")
        (missing / BUNDLE.COMPLETE_NAME).unlink()
        self.assert_rejected(missing)

        malformed, _ = self.publish("malformed-complete")
        (malformed / BUNDLE.COMPLETE_NAME).write_text("{not-json\n", encoding="utf-8")
        self.assert_rejected(malformed)

        wrong_status, _ = self.publish("wrong-status")
        complete = wrong_status / BUNDLE.COMPLETE_NAME
        value = json.loads(complete.read_text(encoding="utf-8"))
        value["status"] = "PARTIAL"
        complete.write_text(BUNDLE.canonical_json(value), encoding="utf-8")
        self.assert_rejected(wrong_status)

        noncanonical, _ = self.publish("noncanonical-complete")
        complete = noncanonical / BUNDLE.COMPLETE_NAME
        value = json.loads(complete.read_text(encoding="utf-8"))
        complete.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        self.assert_rejected(noncanonical)

    def test_binding_mismatch_and_stale_binding_are_rejected(self) -> None:
        mismatch, _ = self.publish("binding-mismatch")
        wrong = self.expected_bindings()
        wrong["support.py"] = "0" * 64
        self.assert_rejected(mismatch, bindings=wrong)

        stale, _ = self.publish("stale-binding")
        old = self.expected_bindings()
        (self.root / "support.py").write_text("# changed\n", encoding="utf-8")
        self.assert_rejected(stale, bindings=old)

    def test_binding_change_during_attempt_prevents_publication(self) -> None:
        attempt = self.runs / "binding-race"

        def change_binding(point: str) -> None:
            if point == "after:artifact:alpha.txt":
                (self.root / "support.py").write_text("# raced\n", encoding="utf-8")

        with self.assertRaises(BUNDLE.BundleError):
            self.publish(attempt.name, change_binding)
        self.assertFalse(attempt.exists())
        failed = sorted(self.runs.glob(f".{attempt.name}.failed-*"))
        self.assertEqual(len(failed), 1)
        self.assertFalse((failed[0] / BUNDLE.COMPLETE_NAME).exists())

    def test_attempt_identity_mismatch_is_rejected(self) -> None:
        attempt, _ = self.publish("identity")
        other = self.runs / "other"
        other.mkdir()
        with self.assertRaises(BUNDLE.BundleError):
            BUNDLE.verify_complete_bundle(
                attempt,
                repo_root=self.root,
                allowed_parent=self.runs,
                expected_attempt_dir=other,
                expected_command=COMMAND,
                expected_bindings=self.expected_bindings(),
                expected_artifacts=ARTIFACTS,
            )

    def test_rename_noreplace_never_overwrites_destination(self) -> None:
        source = self.runs / "rename-source"
        destination = self.runs / "rename-destination"
        source.mkdir()
        destination.mkdir()
        (source / "value.txt").write_text("source\n", encoding="utf-8")
        (destination / "value.txt").write_text("destination\n", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            BUNDLE.rename_noreplace(source, destination)
        self.assertEqual((source / "value.txt").read_text(encoding="utf-8"), "source\n")
        self.assertEqual(
            (destination / "value.txt").read_text(encoding="utf-8"),
            "destination\n",
        )


if __name__ == "__main__":
    unittest.main()
