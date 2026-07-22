#!/usr/bin/env python3
"""Deterministic author checker for the superseding PRAC-24 v2 hypothesis."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
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


def fisher_yates(values: list[int], draws: list[int]) -> list[int]:
    result = list(values)
    require(len(draws) == max(0, len(result) - 1), "wrong Fisher-Yates draw count")
    for offset, index in enumerate(range(len(result) - 1, 0, -1)):
        draw = draws[offset]
        require(0 <= draw <= index, "Fisher-Yates draw out of range")
        result[index], result[draw] = result[draw], result[index]
    return result


def verify_sampling_contract(config: dict[str, Any]) -> str:
    sampling = config["sampling_frame"]
    require("exactly once" in sampling["manifest_generation"], "sampling manifest can be redrawn")
    require("write and fsync" in sampling["manifest_generation"], "sampling not frozen before capture")
    require("secrets.randbelow" in sampling["master_draw"], "master draw is not uniform rejection sampling")
    require("never redraw" in sampling["retry_rule"], "outcome-dependent sampling retry allowed")
    require("first 19 permuted masters are calibration and last 3 evaluation" in sampling["role_assignment"], "role split drift")
    require("fresh secrets.randbelow(i+1)" in sampling["role_assignment"], "role permutation not uniform")
    require("without exposing role to the trace kernel" in sampling["capture_order"], "capture kernel sees split role")
    require("never calibration/evaluation role" in sampling["label_blinding"], "trace kernel role blinding absent")
    require("independent uniform role permutation" in sampling["sampling_interpretation"], "exchangeability source undefined")
    values = list(range(22))
    identity = fisher_yates(values, list(range(21, 0, -1)))
    reverse = fisher_yates(values, [0] * 21)
    require(sorted(identity) == values and sorted(reverse) == values, "Fisher-Yates reference lost units")
    require(identity != reverse, "Fisher-Yates reference is degenerate")
    return hashlib.sha256((repr(identity) + "|" + repr(reverse)).encode("utf-8")).hexdigest()


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
        "primary_generation_overage_cells=4/144",
        "post_first_no_fit_paths=420",
        "post_first_no_fit_seconds=59.767362233368",
        "later_recovery_candidates=3",
        "absorbing_hcms_to_best_simple_ratio=1.392971246006",
        "inference=retrospective_diagnosis_only",
    }
    require(required <= observed, "resource diagnostic output drift")


def verify_fixture_algebra(config: dict[str, Any]) -> tuple[int, int]:
    q_values = [20.0 / 19.0 + index / 10000.0 for index in range(1, 1900)]
    replay_cases = 0
    for q_value in q_values:
        if q_value > 1.25:
            break
        full_count = min(10, math.floor(10.0 / q_value))
        full_actual = full_count * 0.19 * q_value
        removal_actual = 10 * 0.19 * q_value
        require(full_actual <= 1.9 + 1e-12, "full replay fixture exceeds 1.9")
        require(removal_actual > 2.0, "replay removal does not cross")
        replay_cases += 1
    generation_cases = 0
    base24 = float(config["base_models"]["atomic_generation_s"]["24"])
    for index in range(1, 3501):
        q_value = index / 1000.0
        u_value = q_value * base24
        if u_value <= 0.1:
            continue
        remaining = (u_value + 0.1) / 2.0
        duration = remaining + 0.05
        require(0.1 < remaining < u_value, "generation fixture admission order wrong")
        require(duration > remaining, "generation fixture does not cross")
        generation_cases += 1
    require(replay_cases > 100 and generation_cases > 100, "fixture algebra coverage too small")
    return replay_cases, generation_cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--hypothesis", required=True)
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    hypothesis_path = Path(args.hypothesis).resolve()
    root = config_path.parents[2]
    config = json.loads(config_path.read_text(encoding="utf-8"))
    hypothesis = hypothesis_path.read_text(encoding="utf-8")

    require(hypothesis_path.parent == root / "research-log", "hypothesis outside research log")
    require(len(hypothesis.splitlines()) == 533, "hypothesis line-count drift")
    for required_text in (
        "Supersedes:** `research-log/164-hypothesis-iter-8-prac24.md`",
        "uniform Fisher--Yates role permutation",
        "no method predecessor exists",
        "HCMS exact-prefix behavior is an inherited base",
        "## 17. Fixed eight-category bias surface",
        "contribution_components=3",
        "Writing v2 does not spend a review round",
    ):
        require(required_text in hypothesis, f"hypothesis contract missing: {required_text}")

    require(config["schema_version"] == "prac24-c3-v2", "wrong schema")
    require(config["short_name"] == "PRAC-24", "concept drift")
    require(config["supersedes"] == "experiments/configs/prac24-c3-v1.json", "lineage missing")
    require(config["official_score_claim"] == "withheld_until_separate_target_confidence_bridge", "official claim opened")
    require(config["target_void_proof_claim"] == "forbidden_remote_env_operations_are_not_cancellable", "target hard-safety overclaim")
    require(sha256(root / "experiments/attack.py") == config["base_attack_sha256"], "competition attack changed")
    source_count = verify_bindings(root, config["source_bindings"], "source")
    evidence_count = verify_bindings(root, config["evidence_bindings"], "evidence")
    lineage_count = verify_bindings(root, config["superseded_lineage_bindings"], "lineage")
    run_diagnostic(root)

    require(config["path_cap"] == config["candidate_cap"] == 16, "trace support cap drift")
    require(config["prefixes_descending"] == [24, 8, 1], "prefix set drift")
    budgets = config["controlled_budgets_s"]
    require(float(budgets["generation"]) == float(budgets["aggregate_replay"]) == 2.0, "controlled budget drift")
    require(float(budgets["trace_capture_outer"]) == 120.0, "capture outer drift")

    sampling_digest = verify_sampling_contract(config)
    trace = config["matched_trace_unit"]
    require("q-independent" in trace["definition"], "trace depends on q")
    require("16 path slots" in trace["definition"] and "24,8,1" in trace["definition"], "trace table incomplete")
    require("no method is executed during capture" in trace["process_boundary"], "policy contaminates capture")
    require("same evaluation table" in trace["policy_projection"], "methods not trace matched")
    require("positive_infinity" in trace["missing_rule"], "censoring erased")
    require("seventeenth" in trace["support_rule"], "evaluation can escape support")

    calibration = config["risk_calibration"]
    n = int(calibration["calibration_units_per_profile"])
    alpha = float(calibration["cell_risk_alpha"])
    rank = math.ceil((n + 1) * (1.0 - alpha))
    require((n, alpha, rank) == (19, 0.05, 19), "calibration rank drift")
    require(calibration["evaluation_units_per_profile"] == 3, "evaluation sample drift")
    require(calibration["order_statistic_rank"] == rank, "stored rank mismatch")
    require("prac_hcms, prac_fixed8 and prac_fixed24_no_salvage" in calibration["replay_score"], "all-policy score absent")
    require(calibration["empty_replay_convention"].startswith("if every PRAC policy has K=0"), "K=0 undefined")
    require(calibration["separate_multipliers"] == ["q_replay", "q_generation"], "risk multipliers merged")
    require("not conditional" in calibration["conditioning_warning"], "finite-q conditioning overclaim")
    require("all evaluation results publish regardless of q" in calibration["conditioning_warning"], "q-based selective reporting")

    inherited = config["inherited_policy"]
    require(inherited["status"] == "inherited_not_a_prac_contribution_component", "HCMS still claimed as component")
    require(inherited["causal_claim"].startswith("none"), "candidate-boundary mechanism still claimed")
    require(len(inherited["comparators"]) == 2, "inherited policy lacks Occam controls")

    components = config["contribution_components"]
    require({item["id"] for item in components} == {
        "complete_trace_prefix_envelope",
        "absorbing_no_fit",
        "return_ready_atomic_gate",
    }, "component contract drift")
    require(len({item["clean_removal"] for item in components}) == 3, "component removals not unique")
    require(all(item["single_role"] and item["measured_bottleneck"] and item["confirmation_predicate"] for item in components), "component field missing")

    methods = config["methods"]
    require(set(methods) == {"prac_hcms", "prac_fixed8", "prac_fixed24_no_salvage", "point_hcms_retry"}, "method set drift")
    require(methods["point_hcms_retry"]["status"] == "legacy_bundled_diagnostic_not_component_evidence", "legacy diagnostic credited")

    phase3 = config["phase3"]
    require(len(phase3["profiles"]) == 3, "profile count drift")
    require("no method order or predecessor exists" in phase3["evaluation_design"], "predecessor mismatch reintroduced")
    require(len(phase3["conformance_suite_excluded_from_efficacy"]) == 4, "conformance suite drift")
    confirm = phase3["confirm"]
    require(confirm["minimum_prac_hcms_to_best_simple_ratio"] == 1.10, "materiality threshold drift")
    require(confirm["maximum_q_replay"] == 1.25 and confirm["maximum_q_generation"] == 3.50, "q ceiling drift")
    require(confirm["profiles"] == 3 and confirm["sampled_units_per_profile"] == 22, "sample grid drift")
    require(confirm["calibration_units_per_profile"] == 19 and confirm["evaluation_units_per_profile"] == 3, "split grid drift")
    require(confirm["evaluation_method_cells"] == 36, "method cell count drift")
    require(confirm["component_predicates_pass"] == 3, "joint component gate weakened")
    replay_cases, generation_cases = verify_fixture_algebra(config)

    runner = root / phase3["runner_path"]
    attempt = root / phase3["attempt_dir"]
    require(not runner.exists(), "Phase-3 runner exists before theory review")
    require(not attempt.exists(), "Phase-3 attempt exists before theory review")
    require(config["target_confidence_bridge"]["status"] == "closed_during_phase2_and_phase3", "target bridge opened")

    gateway_text = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py").read_text(encoding="utf-8")
    inference_text = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_inference_server.py").read_text(encoding="utf-8")
    require("DEFAULT_BUDGET_S = 9000.0" in gateway_text, "gateway budget source drift")
    require("Attack code cannot cancel an in-flight RemoteEnv operation" in inference_text, "remote cancellation source drift")

    print("prac24_phase2_author_check_v2=PASS")
    print("hypothesis_lines=533")
    print(f"source_bindings={source_count}")
    print(f"evidence_bindings={evidence_count}")
    print(f"lineage_bindings={lineage_count}")
    print("round8_issues_addressed=3")
    print("sampling_manifest=single_draw_no_retry")
    print("split=19_calibration_3_evaluation_per_profile")
    print(f"fisher_yates_demo_digest={sampling_digest}")
    print("capture_role_blinded=true")
    print("method_predecessor=none_matched_trace_projection")
    print("calibration_unit=complete_all_policy_potential_trace")
    print(f"cell_risk_alpha={alpha:.6f}")
    print(f"order_statistic_rank={rank}")
    print("empty_replay_score=0.0")
    print("censoring=positive_infinity")
    print("finite_q_conditioning_claim=forbidden")
    print("inherited_hcms_component_credit=false")
    print("contribution_components=3")
    print("clean_component_removals=3")
    print(f"replay_fixture_algebra_cases={replay_cases}")
    print(f"generation_fixture_algebra_cases={generation_cases}")
    print("evaluation_method_cells=36")
    print("official_score_claim=withheld")
    print("attack_unchanged=true")
    print("phase3_artifacts=absent")
    print("review=not_dispatched")


if __name__ == "__main__":
    main()
