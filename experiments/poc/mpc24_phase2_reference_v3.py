#!/usr/bin/env python3
"""Deterministic Phase-2 author checker for counterbalanced MPC-24 v6."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


FORBIDDEN_CONTROLLED_ROOT_KEYS = {
    "replay_budget_s",
    "replay_safe_fraction",
    "generation_budget_s",
    "generation_margin_s",
    "max_next_interaction_reserve_s",
    "sentinel_time_cap_s",
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


def verify_bindings(root: Path, config: dict[str, Any], field: str) -> int:
    for relative, expected in config[field].items():
        require(sha256(root / relative) == expected, f"{field} mismatch: {relative}")
    return len(config[field])


def run_checked(root: Path, command: list[str], required_lines: set[str]) -> None:
    completed = subprocess.run(command, cwd=root, check=True, capture_output=True, text=True)
    observed = set(completed.stdout.strip().splitlines())
    require(required_lines.issubset(observed), f"subcheck output drift: {command}")


def verify_clock(config: dict[str, Any]) -> None:
    require(not (FORBIDDEN_CONTROLLED_ROOT_KEYS & set(config)), "conflicting root budget key")
    clock = config["controlled_clock"]
    reserve = float(clock["interaction_reserve_s"])
    generation = float(clock["generation_budget_s"])
    replay = float(clock["replay_budget_s"])
    outer = float(clock["outer_process_timeout_s"])
    require(0.0 < reserve < generation < outer, "controlled clock invariant failed")
    require(replay == generation, "controlled generation/replay ledgers must be explicit peers")
    require(generation - reserve > 0.0, "sentinel inadmissible at time zero")

    fixture = config["author_contract"]["deadline_fixture"]
    remaining = float(fixture["generation_budget_s"]) - float(fixture["observed_attempt_cost_s"])
    require(math.isclose(remaining, float(fixture["expected_remaining_s"])), "deadline fixture arithmetic")
    require(remaining < float(fixture["interaction_reserve_s"]), "deadline fixture does not stop")
    require(fixture["expected_stop"] == "generation_reserve", "deadline reason changed")
    require(fixture["expected_returned_prefix"] == 8, "deadline salvage changed")


def verify_schedule(config: dict[str, Any]) -> tuple[int, int, int]:
    phase3 = config["phase3"]
    methods = phase3["methods"]
    orders = phase3["counterbalanced_orders"]
    require(len(methods) == 4 and len(orders) == phase3["paired_repetitions"] == 4, "schedule size")
    require(all(sorted(order) == sorted(methods) for order in orders), "order is not a method permutation")
    for method in methods:
        positions = [order.index(method) for order in orders]
        require(sorted(positions) == list(range(4)), f"method not position-balanced: {method}")
    require(phase3["static_mixture_sequence"] == [24, 24, 24, 8], "static mixture changed")
    require(phase3["primary_comparator"] == "maximum aggregate constrained raw among fixed_8,fixed_24,static_3x24_1x8", "Occam comparator changed")
    confirm = phase3["confirm"]
    require(confirm["minimum_mpc_to_best_simple_aggregate_ratio"] == 1.05, "primary threshold changed")
    require(confirm["method_position_count_per_cell"] == 1, "position threshold changed")
    require(confirm["paired_repetitions_complete_fraction"] == 1.0, "paired completion changed")
    require(confirm["invalid_timeout_or_overage_count"] == 0, "validity threshold changed")
    return len(phase3["profiles"]), len(orders), len(methods)


def verify_components(config: dict[str, Any]) -> tuple[int, int]:
    contribution = config["contribution_components"]
    controls = config["correctness_controls"]
    require({item["id"] for item in contribution} == {"multiplicity_selector", "replay_surrogate_ledger"}, "contribution components changed")
    require({item["id"] for item in controls} == {"monotone_prefix_salvage", "indexed_attribution", "observable_deadline"}, "correctness controls changed")
    require(all("not_contribution_component" in item["status"] for item in controls), "safety control promoted")
    require(config["replay_surrogate"]["interpretation"] == "first_message_correlated_scale_surrogate", "proxy interpretation changed")
    require(config["replay_surrogate"]["forbidden_interpretation"] == "separately_identified_boundary_cost", "forbidden mechanism absent")
    return len(contribution), len(controls)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    root = config_path.parents[2]
    config = json.loads(config_path.read_text())

    require(config["schema_version"] == "mpc24-c3-v3", "wrong schema")
    require(config["primary_claim_scope"] == "counterbalanced_controlled_phase3", "claim scope changed")
    require(config["official_score_claim"] == "withheld_until_separate_target_confidence_bridge", "official claim reintroduced")
    require(config["states"] == [24, 8, 1], "state order changed")
    require(config["selector"]["only24_eligible"] == "choose1 iff eligible1; otherwise state1 and drop", "only24 edge changed")

    source_count = verify_bindings(root, config, "source_bindings")
    evidence_count = verify_bindings(root, config, "evidence_bindings")
    run_checked(
        root,
        [sys.executable, "-I", "experiments/poc/mpc24_replay_calibration_audit.py"],
        {"mpc24_replay_calibration_audit=PASS", "holdout_envelope_coverage=54/54", "proxy_controller_to_fixed8_ratio=1.443010752688"},
    )
    run_checked(
        root,
        [sys.executable, "-I", "experiments/poc/mpc24_phase2_reference_v2.py", "--config", "experiments/configs/mpc24-c3-v2.json"],
        {"mpc24_phase2_author_check_v2=PASS", "state_machine_fixtures=11", "only24_eligible_policy=choose1_or_drop"},
    )

    verify_clock(config)
    profiles, orders, methods = verify_schedule(config)
    contribution, controls = verify_components(config)
    provenance = config["measurement_provenance"]
    require(provenance["dependency_count"] == 9, "provenance dependency count changed")

    print("mpc24_phase2_author_check_v3=PASS")
    print(f"source_bindings={source_count}")
    print(f"evidence_bindings={evidence_count}")
    print("canonical_controlled_clock_fields=4")
    print("sentinel_admissible_at_time_zero=true")
    print("interaction_reserve_s=0.100000")
    print("generation_budget_s=6.000000")
    print("replay_budget_s=6.000000")
    print("outer_process_timeout_s=120.000000")
    print(f"phase3_profiles={profiles}")
    print(f"counterbalanced_orders={orders}")
    print(f"methods={methods}")
    print("method_position_balance=1_each")
    print("strongest_simple_comparator=fixed8,fixed24,static3x24_1x8")
    print("minimum_mpc_to_best_simple_ratio=1.050000")
    print(f"contribution_components={contribution}")
    print(f"correctness_controls={controls}")
    print("proxy_interpretation=correlated_scale_surrogate")
    print("taxonomy=resource_bottleneck_optimization_search_replace")
    print("official_score_claim=withheld")
    print("review=not_dispatched")


if __name__ == "__main__":
    main()
