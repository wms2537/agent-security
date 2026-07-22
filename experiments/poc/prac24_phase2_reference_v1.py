#!/usr/bin/env python3
"""Deterministic author checker for the PRAC-24 Phase-2 specification."""

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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_bindings(root: Path, values: dict[str, str], name: str) -> int:
    for relative, expected in values.items():
        path = root / relative
        require(path.is_file() and not path.is_symlink(), f"missing/nonregular {name}: {relative}")
        require(sha256(path) == expected, f"{name} hash drift: {relative}")
    return len(values)


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


def run_diagnostic(root: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "-I", "experiments/poc/rahcms_resource_diagnostic.py"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    observed = set(completed.stdout.splitlines())
    required = {
        "rahcms_resource_diagnostic=PASS",
        "hcms_candidate_coverage=187/189",
        "hcms_aggregate_replay_overage_cells=0/36",
        "scalar_aggregate_replay_overage_cells=19/36",
        "primary_generation_overage_cells=4/144",
        "post_first_no_fit_paths=420",
        "later_recovery_candidates=3",
        "absorbing_hcms_to_best_simple_ratio=1.392971246006",
        "inference=retrospective_diagnosis_only",
    }
    require(required <= observed, "resource diagnostic output drift")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    root = config_path.parents[2]
    config = json.loads(config_path.read_text(encoding="utf-8"))

    require(config["schema_version"] == "prac24-c3-v1", "wrong schema")
    require(config["short_name"] == "PRAC-24", "concept name drift")
    require(config["official_score_claim"] == "withheld_until_separate_target_confidence_bridge", "official claim reintroduced")
    require(config["target_void_proof_claim"] == "forbidden_remote_env_operations_are_not_cancellable", "target hard-safety overclaim")
    require(sha256(root / "experiments/attack.py") == config["base_attack_sha256"], "competition attack changed")
    source_count = verify_bindings(root, config["source_bindings"], "source")
    evidence_count = verify_bindings(root, config["evidence_bindings"], "evidence")
    run_diagnostic(root)

    clock = config["controlled_clock"]
    require(float(clock["generation_budget_s"]) == float(clock["replay_budget_s"]) == 2.0, "controlled budgets drift")
    require(float(clock["outer_process_timeout_s"]) > 2.0, "outer timeout invalid")
    require("publication" in clock["atomic_path_definition"], "atomic path excludes publication")
    require(config["calibration_path_cap"] == config["evaluation_path_cap"] == 16, "calibration/evaluation path support mismatch")

    calibration = config["risk_calibration"]
    n = int(calibration["calibration_cells_per_profile_position_stratum"])
    alpha = float(calibration["cell_risk_alpha"])
    rank = math.ceil((n + 1) * (1.0 - alpha))
    require((n, alpha, rank) == (19, 0.05, 19), "calibration rank drift")
    require(rank == calibration["order_statistic_rank"], "stored rank mismatch")
    require(len(calibration["calibration_masters"]) == len(set(calibration["calibration_masters"])) == n, "calibration master drift")
    require(calibration["calibration_method"] == "unbudgeted_hcms_trace_capture", "circular calibration controller")
    require("no q-dependent replay admission" in calibration["calibration_policy"], "calibration depends on unknown q")
    require("fixed ordinal slots 0,1,2,3" in calibration["calibration_block"], "calibration position strata undefined")
    require(calibration["missing_timeout_censoring"].startswith("set the affected stratum score to positive_infinity"), "censoring erased")
    require(calibration["separate_multipliers"] == ["q_replay", "q_generation"], "risk split drift")

    base_generation = config["base_models"]["atomic_generation_s"]
    require(set(base_generation) >= {"1", "8", "24"}, "generation bases incomplete")
    require(all(float(base_generation[key]) > 0.0 for key in ("1", "8", "24")), "nonpositive generation base")

    methods = config["methods"]
    require(set(methods) == {
        "prac_hcms",
        "prac_fixed8",
        "prac_fixed24_no_salvage",
        "point_hcms_retry",
    }, "method set drift")
    for name in ("prac_hcms", "point_hcms_retry"):
        require(methods[name]["proposal"] == "always propose current monotone state, initialized to 24", f"HCMS proposal drift: {name}")
        require(methods[name]["permitted_prefixes"] == [24, 8, 1], f"HCMS prefix drift: {name}")
        require(methods[name]["salvage"] == "longest_exact_prefix", f"HCMS salvage drift: {name}")
    require(methods["prac_hcms"]["risk_controller"] == "prac", "PRAC controller missing")
    require(methods["point_hcms_retry"]["risk_controller"] == "point_retry_removal", "point removal missing")
    require("absorbing" in config["controller"]["absorbing_no_fit"], "absorbing transition missing")
    require("path 17" in config["controller"]["path_cap"], "hard evaluation path cap missing")

    components = config["component_contract"]
    require({item["id"] for item in components} == {
        "high_ceiling_monotone_salvage",
        "complete_cell_prefix_envelope",
        "absorbing_no_fit",
        "atomic_generation_gate",
    }, "component contract drift")
    require(all(item["removals"] for item in components), "component without removal")

    phase3 = config["phase3"]
    orders, predecessor_pairs = verify_williams(phase3)
    require(len(phase3["profiles"]) == 3, "profile count drift")
    require(len(phase3["evaluation_masters"]) == len(set(phase3["evaluation_masters"])) == 3, "evaluation master drift")
    require(set(phase3["evaluation_masters"]).isdisjoint(calibration["calibration_masters"]), "calibration/evaluation identity overlap")
    require(len(phase3["safety_suite_excluded_from_efficacy"]) == 4, "safety suite count drift")
    safety = {item["id"]: item for item in phase3["safety_suite_excluded_from_efficacy"]}
    require("0.19*q_replay" in safety["cumulative_replay_spike_prac"]["construction"], "replay fixture not executable")
    require("q_replay>20/19" in safety["cumulative_replay_spike_prac"]["distinguishability_precondition"], "replay fixture precondition drift")
    require("exactly three" in safety["saturation_tail_absorption"]["construction"], "absorbing fixture not executable")
    require("r=(u+0.1)/2" in safety["bounded_long_setup_backstop"]["construction"], "generation fixture not executable")
    require("u>0.1" in safety["bounded_long_setup_backstop"]["distinguishability_precondition"], "generation fixture precondition drift")
    confirm = phase3["confirm"]
    require(confirm["minimum_prac_hcms_to_best_simple_ratio"] == 1.10, "materiality threshold drift")
    require(confirm["maximum_q_replay"] == 1.25, "replay envelope threshold drift")
    require(confirm["maximum_q_generation"] == 3.50, "generation envelope threshold drift")
    require(confirm["maximum_prac_replay_overage_cells"] == 0, "replay safety weakened")
    require(confirm["maximum_prac_generation_overage_cells"] == 0, "generation safety weakened")
    require(confirm["minimum_clean_removal_safety_failures"] == 2, "clean safety-removal distinction weakened")
    require(confirm["maximum_full_post_no_fit_paths"] == 0, "absorbing full path weakened")
    require(confirm["minimum_retry_removal_post_no_fit_paths"] >= 3, "retry removal not exercised")
    require(confirm["maximum_retry_removal_recovered_candidates"] == 0, "retry removal allowed utility credit")

    phase3_runner = root / phase3["runner_path"]
    calibration_attempt = root / phase3["calibration_attempt_dir"]
    evaluation_attempt = root / phase3["evaluation_attempt_dir"]
    require(not phase3_runner.exists(), "Phase-3 runner exists before theory review")
    require(not calibration_attempt.exists(), "calibration attempt exists before theory review")
    require(not evaluation_attempt.exists(), "evaluation attempt exists before theory review")
    require(config["target_confidence_bridge"]["status"] == "closed_during_phase2_and_phase3", "target bridge opened early")

    gateway_text = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py").read_text(encoding="utf-8")
    inference_text = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_inference_server.py").read_text(encoding="utf-8")
    require("DEFAULT_BUDGET_S = 9000.0" in gateway_text, "gateway budget source drift")
    require("Attack code cannot cancel an in-flight RemoteEnv operation" in inference_text, "remote cancellation source drift")

    print("prac24_phase2_author_check_v1=PASS")
    print(f"source_bindings={source_count}")
    print(f"evidence_bindings={evidence_count}")
    print("precursor_status=invalid_disclosed")
    print("diagnosis=retrospective_only")
    print("calibration_unit=complete_unbudgeted_hcms_trace_profile_position_stratum")
    print("calibration_controller=noncircular_trace_capture")
    print(f"calibration_cells_per_stratum={n}")
    print(f"cell_risk_alpha={alpha:.6f}")
    print(f"order_statistic_rank={rank}")
    print("censoring=positive_infinity")
    print("risk_multipliers=separate_replay_generation")
    print("absorbing_no_fit=true")
    print("calibration_evaluation_path_cap=16")
    print("contribution_components=4")
    print("clean_component_removals=4")
    print("removal_controls=present")
    print(f"williams_orders={orders}")
    print(f"directed_predecessor_pairs={predecessor_pairs}")
    print("minimum_primary_ratio=1.100000")
    print("maximum_q_replay=1.250000")
    print("maximum_q_generation=3.500000")
    print("target_remote_cancellation=false")
    print("official_score_claim=withheld")
    print("attack_unchanged=true")
    print("phase3_artifacts=absent")
    print("review=not_dispatched")


if __name__ == "__main__":
    main()
