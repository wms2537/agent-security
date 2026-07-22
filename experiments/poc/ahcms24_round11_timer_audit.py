#!/usr/bin/env python3
"""Read-only source/timing audit for the AHCMS-24 v5 repair.

This script never executes the scientific runner.  It pins the historical
runner, proves the relative ordering of its timer landmarks, recomputes the
sealed retry-tail profile, and evaluates two explicitly bounded scheduler-noise
stress cases over that old profile.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from collections import defaultdict
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "experiments/poc/hcms24_phase3_v1.py"
ATTEMPT = ROOT / "experiments/runs/hcms24-c3-poc-v1"
ATTACK = ROOT / "experiments/attack.py"
EXPECTED_RUNNER_SHA256 = "7b030c67a7f18c4bce77db67f7db757b817aede7cbaf75aa1195a09d42f6b1f6"
EXPECTED_COMPLETE_SHA256 = "34e9dc0274e0828f325cb280b2f392a6e867fabf4315c0c962cf3746dc200b07"
EXPECTED_ATTACK_SHA256 = "8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d"
CELL_KEY = (
    "namespace",
    "profile",
    "master",
    "order_index",
    "position",
    "method",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    path = ATTEMPT / name
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular {name}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
    require(reader.fieldnames is not None, f"missing header: {name}")
    require(all(None not in row for row in rows), f"row-width drift: {name}")
    return rows


def function_source(module_text: str, name: str) -> str:
    tree = ast.parse(module_text)
    matches = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    ]
    require(len(matches) == 1, f"function identity drift: {name}")
    result = ast.get_source_segment(module_text, matches[0])
    require(result is not None, f"source segment unavailable: {name}")
    return result


def ordered(source: str, markers: Iterable[str], name: str) -> None:
    cursor = -1
    for marker in markers:
        position = source.find(marker, cursor + 1)
        require(position >= 0, f"missing {name} timer marker: {marker}")
        require(position > cursor, f"out-of-order {name} timer marker: {marker}")
        cursor = position


def verify_source_boundaries() -> None:
    require(sha256(RUNNER) == EXPECTED_RUNNER_SHA256, "historical runner identity drift")
    module_text = RUNNER.read_text(encoding="utf-8")
    generation = function_source(module_text, "run_method_cell")
    replay = function_source(module_text, "replay_candidate")
    checkpoint = function_source(module_text, "checkpoint_in_flight")

    ordered(
        generation,
        (
            "path_started = time.monotonic()",
            '"generation_environment_construction"',
            "env = env_builder(generation_factory, master)",
            '"generation_reset_complete"',
            '"generation_interaction"',
            "env.interact(message, max_tool_hops=MAX_TOOL_HOPS)",
            '"generation_interaction_complete"',
            "path_cost = max(1e-9, time.monotonic() - path_started)",
            "exact_flags = indexed_exact_flags",
            "selected = choose_return_prefix",
        ),
        "generation",
    )
    ordered(
        replay,
        (
            "started = time.monotonic()",
            '"replay_environment_construction"',
            "env = env_builder(factory, seed)",
            '"replay_reset_complete"',
            '"replay_interaction"',
            "env.interact(message, max_tool_hops=MAX_TOOL_HOPS)",
            '"replay_interaction_complete"',
            "elapsed = max(1e-9, time.monotonic() - started)",
            "trace = env.export_trace_dict()",
            '"replay_evaluation"',
            "predicates = eval_predicates(trace)",
            "actual_raw = float(score_attack_raw([finding]))",
        ),
        "replay",
    )
    require(
        'phase_state["in_flight"] = json.loads(canonical_json(snapshot))' in checkpoint,
        "checkpoint serialization boundary drift",
    )


def verify_seal() -> None:
    complete_path = ATTEMPT / "COMPLETE.json"
    require(sha256(complete_path) == EXPECTED_COMPLETE_SHA256, "COMPLETE identity drift")
    require(sha256(ATTACK) == EXPECTED_ATTACK_SHA256, "attack identity drift")
    complete = json.loads(complete_path.read_text(encoding="utf-8"))
    require(complete["status"] == "invalid", "sealed historical status was rewritten")
    expected_names = set(complete["artifacts"])
    observed_names = {path.name for path in ATTEMPT.iterdir()} - {"COMPLETE.json"}
    require(observed_names == expected_names, "sealed artifact-set drift")
    for name, expected in complete["artifacts"].items():
        require(sha256(ATTEMPT / name) == expected, f"sealed artifact drift: {name}")


def main() -> None:
    getcontext().prec = 50
    verify_source_boundaries()
    verify_seal()
    paths = read_tsv("paths.tsv")
    cells = read_tsv("method_cells.tsv")
    candidates = read_tsv("candidates.tsv")

    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in paths:
        grouped[tuple(row[field] for field in CELL_KEY)].append(row)

    retry_tail: list[dict[str, str]] = []
    for key, rows in grouped.items():
        if key[0] != "primary" or key[-1] != "hcms_calibrated":
            continue
        rows.sort(key=lambda row: int(row["path_index"]))
        first_no_fit = next(
            (index for index, row in enumerate(rows) if row["outcome"] == "drop_ledger_no_fit"),
            None,
        )
        if first_no_fit is not None:
            retry_tail.extend(rows[first_no_fit + 1 :])

    retry_elapsed = sum(
        (
            Decimal(row["generation_elapsed_s"])
            for row in cells
            if row["namespace"] == "primary" and row["method"] == "hcms_calibrated"
        ),
        Decimal(0),
    )
    retry_tail_elapsed = sum(
        (Decimal(row["path_cost_s"]) for row in retry_tail), Decimal(0)
    )
    absorbing_elapsed = retry_elapsed - retry_tail_elapsed
    largest_tail_elapsed = max(Decimal(row["path_cost_s"]) for row in retry_tail)
    retry_raw = sum(
        (
            Decimal(row["actual_raw"])
            for row in candidates
            if row["namespace"] == "primary" and row["method"] == "hcms_calibrated"
        ),
        Decimal(0),
    )
    absorbing_raw = Decimal(39240)

    nominal_ratio = (absorbing_raw / absorbing_elapsed) / (retry_raw / retry_elapsed)
    one_interval_retry_elapsed = retry_elapsed - largest_tail_elapsed
    one_interval_ratio = (absorbing_raw / absorbing_elapsed) / (
        retry_raw / one_interval_retry_elapsed
    )
    half_tail = retry_tail_elapsed / Decimal(2)
    half_tail_retry_elapsed = absorbing_elapsed + half_tail
    half_tail_ratio = (absorbing_raw / absorbing_elapsed) / (
        retry_raw / half_tail_retry_elapsed
    )
    half_tail_fraction = half_tail / half_tail_retry_elapsed

    require(len(retry_tail) == 146, "retry-tail count drift")
    require(retry_tail_elapsed == Decimal("18.36650123470462862"), "tail elapsed drift")
    require(retry_raw == Decimal(39258), "retry raw drift")
    require(nominal_ratio >= Decimal("1.10"), "historical nominal margin absent")
    require(one_interval_ratio >= Decimal("1.10"), "one-interval sensitivity failed")
    require(half_tail_ratio >= Decimal("1.10"), "half-tail sensitivity failed")
    require(half_tail_fraction >= Decimal("0.10"), "half-tail support failed")

    print("ahcms24_round11_timer_audit=PASS")
    print(f"historical_runner_sha256={sha256(RUNNER)}")
    print("scientific_runner_executed=false")
    print("generation_start=before_generation_environment_checkpoint")
    print("generation_end=after_last_interaction_complete_checkpoint_before_exact_prefix_selection")
    print("generation_includes=checkpoint_serialization,environment_construction,reset,interactions,in_interval_scheduling")
    print("generation_excludes=exact_prefix_extraction,candidate_selection,publication,artifact_fsync")
    print("replay_start=before_replay_environment_checkpoint")
    print("replay_end=after_last_interaction_complete_checkpoint_before_final_trace_and_scorer")
    print("replay_includes=checkpoint_serialization,environment_construction,reset,interactions,in_interval_scheduling")
    print("replay_excludes=final_trace_export,predicates,signature,scorer,publication,artifact_fsync")
    print("clock_interpretation=captured_elapsed_not_cpu_time_or_remote_deadline_proof")
    print(f"historical_retry_tail_paths={len(retry_tail)}")
    print(f"historical_retry_elapsed_s={retry_elapsed}")
    print(f"historical_retry_tail_elapsed_s={retry_tail_elapsed}")
    print(f"historical_absorbing_elapsed_s={absorbing_elapsed}")
    print(f"historical_largest_retry_tail_interval_s={largest_tail_elapsed}")
    print(f"historical_nominal_efficiency_ratio={nominal_ratio:.12f}")
    print(f"historical_delete_largest_tail_efficiency_ratio={one_interval_ratio:.12f}")
    print(f"historical_half_tail_efficiency_ratio={half_tail_ratio:.12f}")
    print(f"historical_half_tail_fraction={half_tail_fraction:.12f}")
    print("prospective_sensitivity=charge_only_half_retry_tail_elapsed_keep_all_retry_raw")
    print("scheduler_bound_scope=bounded_sensitivity_not_arbitrary_or_systematic_noise_guarantee")


if __name__ == "__main__":
    main()
