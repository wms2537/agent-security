"""Closed OMST c2-v8 correspondence fixture; gated and presently unexecuted."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph


WORKSPACE = Path("/home/soh/agent-security")
CONFIG_PATH = WORKSPACE / "experiments/configs/omst-c2-v8-environment-conditional.json"
FIXTURE_PATH = WORKSPACE / "experiments/omst_c2_v8_fixture.py"
LAUNCHER_PATH = WORKSPACE / "experiments/run_omst_c2_v8_fixture.sh"


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
    "task_s0": (TaskStateOnly, S0, TASK_CHANNELS),
    "task_s1": (TaskStateOnly, S1, TASK_CHANNELS),
    "full_s0": (TaskStatePlusProvenance, S0, FULL_CHANNELS),
    "full_s1": (TaskStatePlusProvenance, S1, FULL_CHANNELS),
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


def verify_environment_identity() -> None:
    specification = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    environment = specification["environment_E0"]
    artifacts = specification["closed_fixture"]

    require(FIXTURE_PATH.resolve() == Path(__file__).resolve(), "fixture_path")
    require(sha256(FIXTURE_PATH) == artifacts["module_sha256"], "fixture_hash")
    require(sha256(LAUNCHER_PATH) == artifacts["launcher_sha256"], "launcher_hash")
    require(Path(sys.executable).resolve() == Path(environment["interpreter_resolved_path"]), "interpreter_path")
    require(sha256(Path(sys.executable).resolve()) == environment["interpreter_sha256"], "interpreter_hash")

    import json as stdlib_json

    json_path = Path(stdlib_json.__file__).resolve()
    require(json_path == Path(environment["stdlib_json_path"]), "stdlib_json_path")
    require(sha256(json_path) == environment["stdlib_json_sha256"], "stdlib_json_hash")


def capture(state: dict[str, object]) -> dict[str, str]:
    received = canonical_text(state)
    return {"received_input": received}


def build_checked(schema: type, expected_channels: list[str]):
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
    graph = builder.compile(checkpointer=None, cache=None, store=None)

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
    return graph


def run_cell(cell: str) -> bytes:
    verify_environment_identity()
    schema, state, channels = CELLS[cell]
    graph = build_checked(schema, channels)
    result = graph.invoke(deepcopy(state), config=deepcopy(RUN_CONFIG))
    return result["received_input"].encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cell", choices=tuple(CELLS), required=True)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="omst-c2-v8-") as run_dir:
        os.chdir(run_dir)
        observed = run_cell(args.cell)

    record = {
        "cell": args.cell,
        "observed_hex": observed.hex(),
        "status": "complete",
    }
    print(canonical_text(record))


if __name__ == "__main__":
    main()
