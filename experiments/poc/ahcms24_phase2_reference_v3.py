#!/usr/bin/env python3
"""Deterministic author checker for the AHCMS-24 v3 hypothesis."""

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


def verify_sampling(config: dict[str, Any]) -> str:
    sampling = config["sampling_frame"]
    require("exactly once" in sampling["manifest_generation"], "sampling may be redrawn")
    require("write and fsync" in sampling["manifest_generation"], "manifest not durable before capture")
    require("3 unique masters per profile" in sampling["manifest_generation"], "master count drift")
    require("secrets.randbelow" in sampling["master_draw"], "master sampling not uniform rejection")
    require("never redraw" in sampling["retry_rule"], "outcome-dependent redraw allowed")
    require("all 9 profile-master units" in sampling["capture_order"], "capture frame drift")
    require("fresh secrets.randbelow(i+1)" in sampling["capture_order"], "capture permutation not uniform")
    require("24,8,1" in sampling["arm_order"], "arm set drift")
    require("no redraw" in sampling["outcome_blinding"], "outcome blinding absent")
    values = list(range(9))
    identity = fisher_yates(values, list(range(8, 0, -1)))
    reverse = fisher_yates(values, [0] * 8)
    require(sorted(identity) == values and sorted(reverse) == values, "Fisher-Yates loses units")
    require(identity != reverse, "Fisher-Yates reference degenerate")
    return hashlib.sha256((repr(identity) + "|" + repr(reverse)).encode("utf-8")).hexdigest()


def run_factorial_audit(root: Path) -> set[str]:
    completed = subprocess.run(
        [sys.executable, "-I", "experiments/poc/prac24_round9_factorial_audit.py"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    observed = set(completed.stdout.splitlines())
    required = {
        "prac24_round9_factorial_audit=PASS",
        "scientific_runner_executed=false",
        "full_two_cubed_factorial_estimable_cells=0",
        "absorption_same_trace_estimable=true",
        "absorption_estimable_primary_cells=96",
        "primary_post_no_fit_paths=415",
        "primary_post_no_fit_seconds=59.181928537553",
        "hcms_post_no_fit_paths=146",
        "hcms_post_no_fit_seconds=18.366501234705",
        "hcms_raw_retention=0.999541494727",
        "absorbing_efficiency_ratio_lower=1.355754716874",
        "replay_removal_same_capture_pairs=0",
        "dropped_paths_without_replay_outcome=426",
        "replay_envelope_same_trace_estimable=false",
        "atomic_gate_same_trace_estimable=false",
        "round9_occam_decision=claim_absorbing_no_fit_only",
        "inference=retrospective_mechanism_selection_only",
    }
    require(required <= observed, "round-9 factorial audit output drift")
    return observed


def verify_efficiency_identity() -> int:
    cases = 0
    for raw_absorb in (1.0, 10.0, 99.0):
        for work_absorb in (0.5, 2.0, 10.0):
            for raw_tail in (0.0, 0.1, 5.0):
                for work_tail in (0.25, 1.0, 20.0):
                    full_raw = raw_absorb + raw_tail
                    full_work = work_absorb + work_tail
                    lhs = raw_absorb / work_absorb > full_raw / full_work
                    rhs = raw_absorb / work_absorb > raw_tail / work_tail
                    require(lhs == rhs, "efficiency/tail-yield identity failed")
                    cases += 1
    return cases


def verify_strict_maximum_bound() -> int:
    cases = 0
    examples = (
        (1.0, 1.0, 1.0),
        (1.0, 2.0, 2.0),
        (1.0, 2.0, 3.0),
        (3.0, 2.0, 1.0),
    )
    for values in examples:
        failures = 0
        for evaluation_index, evaluation in enumerate(values):
            calibration = [value for index, value in enumerate(values) if index != evaluation_index]
            failures += evaluation > max(calibration)
        require(failures <= 1, "more than one unique-strict-maximum failure")
        require(failures / len(values) <= 1.0 / len(values), "finite-population bound failed")
        cases += 1
    return cases


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
    hypothesis_lines = len(hypothesis.splitlines())
    require(hypothesis_lines == 632, "hypothesis line-count drift")
    for required_text in (
        "Supersedes:** `research-log/167-hypothesis-iter-8-prac24-v2.md`",
        "**Absorbing HCMS-24 (AHCMS-24).**",
        "factorial cells are zero",
        "## 10. Component contract and anti-stacking gate",
        "## 13. Corrected finite-population statement",
        "unique strict maximum",
        "## 14. Fixed eight-category bias surface",
        "contribution component",
        "Review remains `9/12`",
        "No Phase-3 runner, attack mutation, Kaggle action or",
    ):
        require(required_text in hypothesis, f"hypothesis contract missing: {required_text}")

    require(config["schema_version"] == "ahcms24-c3-v3", "wrong schema")
    require(config["short_name"] == "AHCMS-24", "concept drift")
    require(config["supersedes"] == "experiments/configs/prac24-c3-v2.json", "lineage missing")
    require(
        config["primary_claim_scope"] == "fresh_controlled_q_independent_matched_trace_phase3_only",
        "claim scope drift",
    )
    require(
        config["official_score_claim"] == "withheld_until_separate_target_confidence_bridge",
        "official claim opened",
    )
    require(
        config["target_void_proof_claim"] == "forbidden_remote_env_operations_are_not_cancellable",
        "target hard-safety overclaim",
    )
    require(sha256(root / "experiments/attack.py") == config["base_attack_sha256"], "attack changed")

    source_count = verify_bindings(root, config["source_bindings"], "source")
    evidence_count = verify_bindings(root, config["evidence_bindings"], "evidence")
    lineage_count = verify_bindings(root, config["superseded_lineage_bindings"], "lineage")
    run_factorial_audit(root)

    require(config["path_cap"] == config["candidate_cap"] == 16, "support cap drift")
    require(config["prefixes_descending"] == [24, 8, 1], "prefix set drift")
    budgets = config["controlled_budgets_s"]
    require(float(budgets["generation"]) == float(budgets["aggregate_replay"]) == 2.0, "budget drift")
    require(float(budgets["trace_capture_outer"]) == 120.0, "outer capture drift")

    sampling_digest = verify_sampling(config)
    trace = config["matched_trace_unit"]
    require("q-independent" in trace["definition"], "trace depends on q")
    require("16 path slots" in trace["definition"] and "24,8,1" in trace["definition"], "trace support incomplete")
    require("no evaluated method is executed during capture" in trace["process_boundary"], "method contaminates capture")
    require("all 16 path slots" in trace["retry_trace"], "retry tail not observed")
    require("same stored table" in trace["policy_projection"], "methods not trace matched")
    require("invalidates" in trace["missing_rule"], "missing data can be dropped")
    require("no projection may escape capture support" in trace["support_rule"], "projection support open")

    inherited = config["inherited_controller"]
    require(inherited["status"].startswith("all fields inherited"), "inherited fields claimed")
    require("not target tail guarantees" in inherited["known_limit"], "target limitation absent")

    methods = config["methods"]
    require(
        set(methods)
        == {
            "ahcms_absorbing",
            "hcms_retry_removal",
            "fixed8_absorbing",
            "fixed24_no_salvage_absorbing",
        },
        "method set drift",
    )
    require(
        methods["hcms_retry_removal"]["status"] == "single clean removal of absorbing_no_fit",
        "removal contract drift",
    )
    for field in ("policy", "replay_ledger", "generation_gate"):
        require(
            methods["ahcms_absorbing"][field] == methods["hcms_retry_removal"][field],
            f"primary pair differs outside absorption: {field}",
        )

    components = config["contribution_components"]
    require(len(components) == 1 and components[0]["id"] == "absorbing_no_fit", "component count drift")
    require(components[0]["clean_removal"] == "hcms_retry_removal", "clean removal drift")
    require("415 post-first-no-fit paths" in components[0]["measured_bottleneck"], "profile number absent")
    require("at least 1.10" in components[0]["confirmation_predicate"], "component threshold absent")

    diagnostics = config["unclaimed_diagnostics"]
    require("not part of AHCMS behavior" in diagnostics["replay_envelope"], "replay envelope still claimed")
    require("not part of AHCMS behavior" in diagnostics["atomic_gate"], "atomic gate still claimed")
    require("forbidden" in diagnostics["q_dependent_fixtures"], "q-dependent efficacy allowed")
    require("zero estimable complete 2^3 cells" in diagnostics["factorial_status"], "factorial nonidentification absent")

    proof = config["round9_proof_correction"]
    require("unique strict maximum" in proof["statement"], "tie correction absent")
    require("ties can only improve" in proof["statement"], "tie direction absent")
    require("uniform rank under ties" in proof["forbidden_wording"], "bad wording not forbidden")

    phase3 = config["phase3"]
    require(len(phase3["profiles"]) == 3 and len(phase3["methods"]) == 4, "phase3 grid drift")
    require("no method order or predecessor exists" in phase3["evaluation_design"], "predecessor reintroduced")
    require("same nine traces" in phase3["primary_comparison"], "primary pair not matched")
    confirm = phase3["confirm"]
    require(confirm["minimum_absorbing_to_retry_efficiency_ratio"] == 1.10, "efficiency threshold drift")
    require(confirm["minimum_absorbing_raw_retention"] == 0.995, "retention threshold drift")
    require(confirm["minimum_retry_tail_generation_fraction"] == 0.10, "tail threshold drift")
    require(confirm["maximum_retry_tail_recovered_raw_fraction"] == 0.005, "tail raw threshold drift")
    require(confirm["minimum_absorbing_hcms_to_best_simple_raw_ratio"] == 1.10, "Occam threshold drift")
    require(confirm["sampled_units_per_profile"] == 3 and confirm["matched_trace_units"] == 9, "sample grid drift")
    require(confirm["projected_method_cells"] == 36, "method cell count drift")
    require(confirm["contribution_components"] == confirm["clean_component_removals"] == 1, "component gate drift")
    require("nofit absent" in phase3["decision_bands"]["inconclusive"], "absent bottleneck escape hatch")

    efficiency_cases = verify_efficiency_identity()
    strict_maximum_cases = verify_strict_maximum_bound()

    runner = root / phase3["runner_path"]
    attempt = root / phase3["attempt_dir"]
    require(not runner.exists(), "Phase-3 runner exists before theory review")
    require(not attempt.exists(), "Phase-3 attempt exists before theory review")
    require(config["target_confidence_bridge"]["status"] == "closed_during_phase2_and_phase3", "target bridge opened")

    gateway_text = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py").read_text(encoding="utf-8")
    inference_text = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_inference_server.py").read_text(encoding="utf-8")
    require("DEFAULT_BUDGET_S = 9000.0" in gateway_text, "gateway budget source drift")
    require("Attack code cannot cancel an in-flight RemoteEnv operation" in inference_text, "remote cancellation source drift")

    print("ahcms24_phase2_author_check_v3=PASS")
    print(f"hypothesis_lines={hypothesis_lines}")
    print(f"source_bindings={source_count}")
    print(f"evidence_bindings={evidence_count}")
    print(f"lineage_bindings={lineage_count}")
    print("round9_issues_addressed=4")
    print("full_two_cubed_factorial_estimable_cells=0")
    print("factorial_nonidentification_disclosed=true")
    print("sampling_manifest=single_draw_no_retry")
    print("fresh_units=3_profiles_x_3_masters")
    print(f"fisher_yates_demo_digest={sampling_digest}")
    print("capture_q_independent=true")
    print("method_predecessor=none_matched_trace_projection")
    print("primary_comparison=absorbing_hcms_vs_retry_hcms")
    print("contribution_components=1")
    print("clean_component_removals=1")
    print("replay_envelope_component_credit=false")
    print("atomic_gate_component_credit=false")
    print(f"efficiency_identity_cases={efficiency_cases}")
    print(f"strict_maximum_tie_cases={strict_maximum_cases}")
    print("finite_population_claim_supports_engineering=false")
    print("projected_method_cells=36")
    print("official_score_claim=withheld")
    print("attack_unchanged=true")
    print("phase3_artifacts=absent")
    print("review=not_dispatched")


if __name__ == "__main__":
    main()
