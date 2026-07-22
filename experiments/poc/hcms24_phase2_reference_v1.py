#!/usr/bin/env python3
"""Deterministic author checker for the HCMS-24 Phase-2 specification."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


FORBIDDEN_ROOT_BUDGET_KEYS = {
    "generation_budget_s",
    "replay_budget_s",
    "replay_safe_fraction",
    "max_next_interaction_reserve_s",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_bindings(root: Path, config: dict[str, Any], key: str) -> int:
    count = 0
    for relative, expected in config[key].items():
        if expected == "TO_BE_BOUND_AFTER_RESULT_COMMIT":
            continue
        require(sha256(root / relative) == expected, f"{key} mismatch: {relative}")
        count += 1
    return count


def run_checked(root: Path, command: list[str], required: set[str]) -> None:
    completed = subprocess.run(command, cwd=root, check=True, capture_output=True, text=True)
    observed = set(completed.stdout.strip().splitlines())
    require(required.issubset(observed), f"subcheck drift: {command}")


def verify_williams(phase3: dict[str, Any]) -> tuple[int, int]:
    methods = phase3["methods"]
    orders = phase3["counterbalanced_orders"]
    require(len(methods) == len(orders) == phase3["paired_repetitions"] == 4, "Williams size")
    require(all(sorted(order) == sorted(methods) for order in orders), "non-permutation order")
    for method in methods:
        require(sorted(order.index(method) for order in orders) == [0, 1, 2, 3], f"position imbalance: {method}")
    predecessors = Counter(
        (order[index - 1], order[index])
        for order in orders
        for index in range(1, len(order))
    )
    expected = {(left, right) for left in methods for right in methods if left != right}
    require(set(predecessors) == expected, "directed predecessor coverage")
    require(set(predecessors.values()) == {1}, "directed predecessor imbalance")
    return len(orders), len(predecessors)


def verify_methods(config: dict[str, Any]) -> None:
    methods = config["methods"]
    require(set(methods) == {
        "hcms_calibrated",
        "fixed8_calibrated",
        "fixed24_no_salvage_calibrated",
        "hcms_scalar",
    }, "method set changed")
    hcms = methods["hcms_calibrated"]
    scalar = methods["hcms_scalar"]
    require({key: hcms[key] for key in ("proposal", "permitted_prefixes", "salvage", "transition")} ==
            {key: scalar[key] for key in ("proposal", "permitted_prefixes", "salvage", "transition")},
            "scalar removal changes more than ledger")
    require(hcms["ledger"] == "calibrated" and scalar["ledger"] == "scalar_removal", "ledger removal missing")
    require(methods["fixed8_calibrated"]["ledger"] == "calibrated", "fixed8 ledger asymmetry")
    require(methods["fixed24_no_salvage_calibrated"]["ledger"] == "calibrated", "no-salvage ledger asymmetry")
    require(config["eligibility"]["coverage_required"] == 1.0, "exact prefix threshold changed")
    require(config["eligibility"]["aggregate_event_counts_forbidden"] is True, "aggregate attribution reintroduced")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    root = config_path.parents[2]
    config = json.loads(config_path.read_text())

    require(config["schema_version"] == "hcms24-c3-v1", "wrong schema")
    require(config["official_score_claim"] == "withheld_until_separate_target_confidence_bridge", "official claim reintroduced")
    require(not (FORBIDDEN_ROOT_BUDGET_KEYS & set(config)), "conflicting root budget")
    clock = config["controlled_clock"]
    reserve = float(clock["interaction_reserve_s"])
    generation = float(clock["generation_budget_s"])
    replay = float(clock["replay_budget_s"])
    outer = float(clock["outer_process_timeout_s"])
    require(0.0 < reserve < generation < outer, "clock invariant")
    require(math.isclose(generation, replay), "peer controlled ledgers differ")
    require(generation - reserve > 0.0, "first interaction inadmissible")

    source_count = verify_bindings(root, config, "source_bindings")
    evidence_count = verify_bindings(root, config, "evidence_bindings")
    require(sha256(root / "experiments/attack.py") == config["base_attack_sha256"], "competition attack changed")
    run_checked(
        root,
        [sys.executable, "-I", "experiments/poc/mpc24_replay_calibration_audit.py"],
        {
            "mpc24_replay_calibration_audit=PASS",
            "holdout_envelope_coverage=54/54",
            "scalar_1_10_violations_8_24=84/90",
        },
    )
    run_checked(
        root,
        [sys.executable, "-I", "experiments/poc/mpc24_symmetry_occam_audit.py"],
        {
            "mpc24_symmetry_occam_audit=PASS",
            "mpc_first_state_matches_fixed24_ceiling=9/9",
            "mpc_to_fixed24_ceiling_ratio=1.000000000000",
            "scalar_mpc_actual_replay_overage_cells=7/9",
            "decision=retire_selector_pivot_to_high_ceiling_salvage",
        },
    )

    verify_methods(config)
    components = config["contribution_components"]
    require({item["id"] for item in components} == {
        "high_ceiling_monotone_salvage",
        "calibrated_replay_accounting",
    }, "contribution components changed")
    controls = config["correctness_controls"]
    require(all("not_contribution_component" in item["status"] for item in controls), "control promoted to contribution")
    require(config["antecedent_evidence"]["status"] == "FAIL", "antecedent failure hidden")
    require(config["antecedent_evidence"]["selector_result"] == "retired_zero_incremental_value", "selector revived")

    phase3 = config["phase3"]
    orders, predecessor_pairs = verify_williams(phase3)
    require(len(phase3["profiles"]) == 3, "primary profile count")
    require(len(phase3["safety_suite_excluded_from_efficacy"]) == 1, "safety suite contamination")
    primary_ids = {item["id"] for item in phase3["profiles"]}
    safety_ids = {item["id"] for item in phase3["safety_suite_excluded_from_efficacy"]}
    require(primary_ids.isdisjoint(safety_ids), "safety fixture in efficacy")
    confirm = phase3["confirm"]
    require(confirm["minimum_hcms_to_best_simple_ratio"] == 1.10, "materiality threshold changed")
    require(confirm["minimum_hcms_actual_replay_coverage"] == 1.0, "coverage threshold changed")
    require(confirm["maximum_hcms_actual_replay_overage_cells"] == 0, "HCMS overage threshold changed")
    require(confirm["minimum_scalar_actual_replay_overage_cells"] == 1, "scalar ablation threshold changed")
    require(confirm["directed_predecessor_count_per_pair"] == 1, "carryover threshold changed")
    require(confirm["invalid_timeout_duplicate_or_generation_overage_count"] == 0, "validity threshold changed")

    print("hcms24_phase2_author_check_v1=PASS")
    print(f"source_bindings={source_count}")
    print(f"evidence_bindings={evidence_count}")
    print("antecedent_status=FAIL_disclosed")
    print("selector_status=retired_zero_value")
    print("shared_kernel_methods=4")
    print("exact_prefix_coverage=1.000000")
    print("contribution_components=2")
    print(f"correctness_controls={len(controls)}")
    print("primary_profiles=3")
    print("safety_profiles_excluded=1")
    print(f"williams_orders={orders}")
    print(f"directed_predecessor_pairs={predecessor_pairs}")
    print("position_balance=1_each")
    print("predecessor_balance=1_each")
    print("minimum_primary_ratio=1.100000")
    print("replay_removal=end_to_end_hcms_scalar")
    print("official_score_claim=withheld")
    print("attack_unchanged=true")
    print("review=not_dispatched")


if __name__ == "__main__":
    main()
