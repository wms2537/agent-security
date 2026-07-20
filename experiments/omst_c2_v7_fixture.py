"""Closed OMST c2-v7 correspondence fixture; do not run before its gate."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from copy import deepcopy
from typing import NotRequired, TypedDict

from langgraph.graph import END, START, StateGraph


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


def capture(state: dict[str, object]) -> dict[str, str]:
    received = canonical_text(state)
    return {"received_input": received}


def build(schema: type, expected_channels: list[str]):
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
    assert actual_channels == expected_channels
    assert proc.mapper is None
    assert getattr(proc, "cache_policy", None) is None
    assert getattr(proc, "retry_policy", None) is None
    assert graph.checkpointer is None
    assert graph.cache is None
    assert graph.store is None
    return graph


def run_cell(cell: str) -> bytes:
    schema, state, channels = CELLS[cell]
    graph = build(schema, channels)
    result = graph.invoke(deepcopy(state), config=deepcopy(RUN_CONFIG))
    return result["received_input"].encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cell", choices=tuple(CELLS), required=True)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="omst-c2-v7-") as run_dir:
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
