"""Closed OMST c2-v9 correspondence fixture; gated and presently unexecuted."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import site
import sys
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any, NotRequired, TypedDict


WORKSPACE = Path("/home/soh/agent-security")
CONFIG_PATH = WORKSPACE / "experiments/configs/omst-c2-v9-manifest-run-pairs.json"
FIXTURE_PATH = WORKSPACE / "experiments/omst_c2_v9_fixture.py"
LAUNCHER_PATH = WORKSPACE / "experiments/run_omst_c2_v9_fixture.sh"

EXPECTED_CHILD_ENVIRONMENT = {
    "HOME": "/nonexistent",
    "LANG": "C",
    "LC_ALL": "C",
    "TZ": "UTC",
}

EXPECTED_LANGGRAPH_SOURCE = {
    "tag": "1.2.9",
    "commit": "95af6a00718588e7b7ce17310e8006d267896a77",
}

REQUIRED_LOAD_BEARING_FILES = {
    "langgraph": (
        "langgraph/graph/state.py",
        "langgraph/pregel/_loop.py",
        "langgraph/pregel/_checkpoint.py",
        "langgraph/pregel/_io.py",
        "langgraph/pregel/_algo.py",
        "langgraph/pregel/_retry.py",
        "langgraph/pregel/_read.py",
        "langgraph/_internal/_runnable.py",
    ),
    "langchain_core": (
        "langchain_core/runnables/base.py",
        "langchain_core/runnables/config.py",
        "langchain_core/callbacks/manager.py",
    ),
}

REQUIRED_SOURCE_ASSERTIONS = (
    "L_compile",
    "L_start",
    "L_fresh",
    "L_prepare",
    "L_deliver",
    "P5_callback_config_no_precapture_mutation",
)


class ProvenanceRecord(TypedDict):
    entity_id: str
    activity_id: str
    agent_id: str


class TaskStateOnly(TypedDict):
    subject_id: str
    task_value: str
    effect_id: str
    effect_log: list[dict[str, object]]
    completion: str


class TaskStatePlusProvenance(TaskStateOnly):
    provenance_record: ProvenanceRecord


class GraphState(TaskStatePlusProvenance):
    received_input: NotRequired[str]


S0: GraphState = {
    "subject_id": "subject-0",
    "task_value": "ready",
    "effect_id": "effect-0",
    "effect_log": [],
    "completion": "pending",
    "provenance_record": {
        "entity_id": "entity-0",
        "activity_id": "activity-0",
        "agent_id": "agent-0",
    },
}

S1: GraphState = {
    "subject_id": "subject-0",
    "task_value": "ready",
    "effect_id": "effect-0",
    "effect_log": [],
    "completion": "pending",
    "provenance_record": {
        "entity_id": "entity-0",
        "activity_id": "activity-0",
        "agent_id": "agent-1",
    },
}

TASK_CHANNELS = [
    "subject_id",
    "task_value",
    "effect_id",
    "effect_log",
    "completion",
]
FULL_CHANNELS = [*TASK_CHANNELS, "provenance_record"]

CELLS = {
    "task_s0": (TaskStateOnly, S0, TASK_CHANNELS, "R_task_s0"),
    "task_s1": (TaskStateOnly, S1, TASK_CHANNELS, "R_task_s1"),
    "full_s0": (TaskStatePlusProvenance, S0, FULL_CHANNELS, "R_full_s0"),
    "full_s1": (TaskStatePlusProvenance, S1, FULL_CHANNELS, "R_full_s1"),
}

RUN_CONFIG = {
    "callbacks": [],
    "tags": [],
    "metadata": {},
    "configurable": {},
}


def canonical_text(value: object) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(f"OMST_RUNTIME_GUARD_FAILED:{label}")


def qualified_identity(value: object) -> str:
    value_type = type(value)
    module = getattr(value, "__module__", value_type.__module__)
    qualname = getattr(value, "__qualname__", value_type.__qualname__)
    return f"{module}.{qualname}"


def manifest_payload_sha256(manifest: dict[str, object]) -> str:
    payload = dict(manifest)
    payload.pop("manifest_payload_sha256", None)
    return hashlib.sha256(canonical_text(payload).encode("utf-8")).hexdigest()


def distribution_tree_sha256(distribution: importlib.metadata.Distribution) -> str:
    entries: list[str] = []
    files = distribution.files
    require(files is not None, "distribution_files_present")
    for relative in sorted(files, key=lambda item: item.as_posix()):
        path = Path(distribution.locate_file(relative))
        if path.is_file():
            entries.append(f"{relative.as_posix()}\0{sha256(path)}")
    require(bool(entries), "distribution_files_nonempty")
    return hashlib.sha256("\n".join(entries).encode("utf-8")).hexdigest()


def pth_inventory(site_packages: list[str]) -> list[dict[str, object]]:
    inventory: list[dict[str, object]] = []
    for root_text in site_packages:
        root = Path(root_text)
        for path in sorted(root.glob("*.pth")) if root.is_dir() else ():
            lines = path.read_text(encoding="utf-8").splitlines()
            executable = any(
                line.strip().startswith(("import ", "import\t"))
                for line in lines
                if line.strip() and not line.lstrip().startswith("#")
            )
            inventory.append(
                {
                    "path": str(path.resolve()),
                    "sha256": sha256(path),
                    "executable": executable,
                }
            )
    return inventory


def current_import_context() -> dict[str, object]:
    site_packages = [str(Path(path).resolve()) for path in site.getsitepackages()]
    return {
        "sys_path": list(sys.path),
        "meta_path_identities": [qualified_identity(finder) for finder in sys.meta_path],
        "path_hook_identities": [qualified_identity(hook) for hook in sys.path_hooks],
        "site_packages": site_packages,
        "pth_files": pth_inventory(site_packages),
    }


def load_manifest(manifest_path: Path) -> dict[str, object]:
    require(manifest_path.is_absolute(), "manifest_path_absolute")
    require(manifest_path.is_file(), "manifest_path_file")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(isinstance(manifest, dict), "manifest_object")
    require(
        manifest.get("schema_version") == "omst-c2-v9-environment-manifest",
        "manifest_schema",
    )
    require(
        manifest.get("manifest_path") == str(manifest_path.resolve()),
        "manifest_bound_path",
    )
    require(
        manifest.get("manifest_payload_sha256") == manifest_payload_sha256(manifest),
        "manifest_payload_hash",
    )
    return manifest


def verify_artifact_identity(manifest: dict[str, object]) -> None:
    artifacts = manifest["artifacts"]
    expected = {
        "fixture": FIXTURE_PATH,
        "launcher": LAUNCHER_PATH,
        "config": CONFIG_PATH,
    }
    require(FIXTURE_PATH.resolve() == Path(__file__).resolve(), "fixture_path")
    for name, expected_path in expected.items():
        record = artifacts[name]
        path = Path(record["path"])
        require(path.resolve() == expected_path.resolve(), f"{name}_path")
        require(sha256(path) == record["sha256"], f"{name}_hash")


def verify_interpreter_and_stdlib(manifest: dict[str, object]) -> None:
    interpreter = manifest["interpreter"]
    executable_link = Path(interpreter["link_path"])
    executable_resolved = Path(interpreter["resolved_path"])
    require(executable_link.resolve() == Path(sys.executable).resolve(), "interpreter_link")
    require(Path(sys.executable).resolve() == executable_resolved, "interpreter_path")
    require(sha256(executable_resolved) == interpreter["sha256"], "interpreter_hash")
    require(sys.version == interpreter["version"], "interpreter_version")

    import json as stdlib_json

    stdlib_record = manifest["stdlib_json"]
    stdlib_path = Path(stdlib_json.__file__).resolve()
    require(stdlib_path == Path(stdlib_record["path"]), "stdlib_json_path")
    require(sha256(stdlib_path) == stdlib_record["sha256"], "stdlib_json_hash")


def verify_dependency_lock(manifest: dict[str, object]) -> None:
    lock = manifest["dependency_lock"]
    require(lock["status"] == "present", "dependency_lock_status")
    lock_path = Path(lock["path"])
    require(lock_path.is_absolute() and lock_path.is_file(), "dependency_lock_path")
    require(sha256(lock_path) == lock["sha256"], "dependency_lock_hash")


def verify_packages(manifest: dict[str, object]) -> None:
    packages = manifest["packages"]
    require(set(packages) == set(REQUIRED_LOAD_BEARING_FILES), "package_key_set")
    for key in sorted(REQUIRED_LOAD_BEARING_FILES):
        record = packages[key]
        require(record["status"] == "present", f"{key}_status")
        distribution = importlib.metadata.distribution(record["distribution"])
        require(distribution.version == record["version"], f"{key}_version")
        require(
            Path(distribution.locate_file("")).resolve()
            == Path(record["distribution_root"]),
            f"{key}_distribution_root",
        )
        require(
            distribution_tree_sha256(distribution)
            == record["distribution_tree_sha256"],
            f"{key}_distribution_tree_hash",
        )

        specification = importlib.util.find_spec(record["module"])
        require(specification is not None, f"{key}_module_spec")
        require(specification.origin is not None, f"{key}_module_origin_present")
        require(
            Path(specification.origin).resolve() == Path(record["module_origin"]),
            f"{key}_module_origin",
        )
        locations = specification.submodule_search_locations
        require(locations is not None and len(locations) == 1, f"{key}_module_location")
        require(
            Path(next(iter(locations))).resolve() == Path(record["package_root"]),
            f"{key}_package_root",
        )


def verify_load_bearing_files(manifest: dict[str, object]) -> None:
    records = manifest["load_bearing_files"]
    observed_keys = {
        (record["package"], record["relative_path"])
        for record in records
    }
    expected_keys = {
        (package, relative_path)
        for package, relative_paths in REQUIRED_LOAD_BEARING_FILES.items()
        for relative_path in relative_paths
    }
    require(observed_keys == expected_keys, "load_bearing_file_set")
    require(len(records) == len(expected_keys), "load_bearing_file_unique")

    packages = manifest["packages"]
    for record in records:
        package = record["package"]
        expected_path = (
            Path(packages[package]["distribution_root"]) / record["relative_path"]
        ).resolve()
        path = Path(record["path"])
        require(path.resolve() == expected_path, "load_bearing_file_path")
        require(path.is_file(), "load_bearing_file_present")
        require(sha256(path) == record["sha256"], "load_bearing_file_hash")


def verify_source_audit(manifest: dict[str, object]) -> None:
    source_basis = manifest["source_basis"]
    require(
        source_basis["langgraph"] == EXPECTED_LANGGRAPH_SOURCE,
        "langgraph_source_basis",
    )
    audit = manifest["source_audit"]
    require(audit["status"] == "passed", "source_audit_status")
    report_path = Path(audit["report_path"])
    require(report_path.is_absolute() and report_path.is_file(), "source_audit_path")
    require(sha256(report_path) == audit["report_sha256"], "source_audit_hash")
    require(
        tuple(audit["verified_assertions"]) == REQUIRED_SOURCE_ASSERTIONS,
        "source_audit_assertions",
    )


def verify_import_context(manifest: dict[str, object]) -> None:
    require(sys.gettrace() is None, "python_trace_absent")
    require(sys.getprofile() is None, "python_profile_absent")
    require("sitecustomize" not in sys.modules, "sitecustomize_absent")
    require("usercustomize" not in sys.modules, "usercustomize_absent")
    observed = current_import_context()
    require(observed == manifest["import_context"], "import_context_identity")
    require(
        all(not record["executable"] for record in observed["pth_files"]),
        "executable_pth_absent",
    )


def verify_common_manifest(manifest: dict[str, object]) -> None:
    require(manifest["status"] == "acquired", "manifest_status")
    require(dict(os.environ) == EXPECTED_CHILD_ENVIRONMENT, "child_environment")
    verify_artifact_identity(manifest)
    verify_interpreter_and_stdlib(manifest)
    verify_dependency_lock(manifest)
    verify_packages(manifest)
    verify_load_bearing_files(manifest)
    verify_source_audit(manifest)
    verify_import_context(manifest)


def capture(state: dict[str, object]) -> dict[str, str]:
    received = canonical_text(state)
    return {"received_input": received}


def build_graph(schema: type) -> Any:
    from langgraph.graph import END, START, StateGraph

    builder = StateGraph(GraphState)
    builder.add_node(
        "capture",
        capture,
        input_schema=schema,
        defer=False,
        retry_policy=None,
        cache_policy=None,
    )
    builder.add_edge(START, "capture")
    builder.add_edge("capture", END)
    return builder.compile(checkpointer=None, cache=None, store=None)


def verify_all_guards(
    manifest: dict[str, object], graph: Any, expected_channels: list[str]
) -> None:
    verify_common_manifest(manifest)
    require(RUN_CONFIG == manifest["run_config"], "run_config_identity")
    proc = graph.nodes["capture"]
    actual_channels = (
        list(proc.channels)
        if isinstance(proc.channels, list)
        else list(proc.channels.keys())
    )
    require(actual_channels == expected_channels, "compiled_channels")
    require(proc.mapper is None, "compiled_mapper")
    require(getattr(proc, "cache_policy", None) is None, "node_cache_policy")
    require(getattr(proc, "retry_policy", None) is None, "node_retry_policy")
    require(graph.checkpointer is None, "compiled_checkpointer")
    require(graph.cache is None, "compiled_cache")
    require(graph.store is None, "compiled_store")


def run_cell(manifest_path: Path, cell: str, run_id: str) -> tuple[bytes, str]:
    manifest = load_manifest(manifest_path)
    require(run_id == CELLS[cell][3], "run_id_cell_binding")

    # Authenticate before framework import, then reauthenticate in the single
    # final guard bundle immediately after compile and before invoke.
    verify_common_manifest(manifest)
    schema, state, channels, _ = CELLS[cell]
    graph = build_graph(schema)
    verify_all_guards(manifest, graph, channels)
    result = graph.invoke(deepcopy(state), config=deepcopy(RUN_CONFIG))
    return result["received_input"].encode("utf-8"), manifest["manifest_payload_sha256"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--cell", choices=tuple(CELLS), required=True)
    parser.add_argument(
        "--run-id",
        choices=tuple(record[3] for record in CELLS.values()),
        required=True,
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix=f"omst-c2-v9-{args.cell}-") as run_dir:
        os.chdir(run_dir)
        observed, manifest_id = run_cell(args.manifest, args.cell, args.run_id)

    record = {
        "cell": args.cell,
        "manifest_id": manifest_id,
        "observed_hex": observed.hex(),
        "run_id": args.run_id,
        "status": "complete",
    }
    print(canonical_text(record))


if __name__ == "__main__":
    main()
