#!/usr/bin/env python3
"""Deterministic author checker for the AHCMS-24 v4 hypothesis."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


BUDGET_NS = 2_000_000_000


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
    require("write and fsync" in sampling["manifest_generation"], "manifest not durable")
    require("3 unique masters per profile" in sampling["manifest_generation"], "master count drift")
    require("secrets.randbelow" in sampling["master_draw"], "master draw not uniform rejection")
    require("never redraw" in sampling["retry_rule"], "outcome-dependent redraw allowed")
    require("all 9 profile-master units" in sampling["capture_order"], "capture frame drift")
    require("fresh secrets.randbelow(i+1)" in sampling["capture_order"], "capture shuffle drift")
    require("24,8,1" in sampling["arm_order"], "arm set drift")
    require("no redraw" in sampling["outcome_blinding"], "outcome blinding absent")
    values = list(range(9))
    identity = fisher_yates(values, list(range(8, 0, -1)))
    reverse = fisher_yates(values, [0] * 8)
    require(sorted(identity) == values and sorted(reverse) == values, "shuffle loses units")
    require(identity != reverse, "shuffle reference degenerate")
    return hashlib.sha256((repr(identity) + "|" + repr(reverse)).encode()).hexdigest()


def run_factorial_audit(root: Path) -> None:
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
        "primary_post_no_fit_paths=415",
        "primary_post_no_fit_seconds=59.181928537553",
        "hcms_post_no_fit_paths=146",
        "hcms_post_no_fit_seconds=18.366501234705",
        "hcms_raw_retention=0.999541494727",
        "absorbing_efficiency_ratio_lower=1.355754716874",
        "replay_envelope_same_trace_estimable=false",
        "atomic_gate_same_trace_estimable=false",
        "round9_occam_decision=claim_absorbing_no_fit_only",
        "inference=retrospective_mechanism_selection_only",
    }
    require(required <= observed, "round-9 audit output drift")


def generation_work(path_durations_ns: list[int]) -> int:
    require(all(isinstance(value, int) and value > 0 for value in path_durations_ns), "bad generation duration")
    return sum(path_durations_ns)


def replay_work(accepted_durations_ns: list[int]) -> int:
    require(all(isinstance(value, int) and value >= 0 for value in accepted_durations_ns), "bad replay duration")
    return sum(accepted_durations_ns)


def is_overage(work_ns: int) -> bool:
    require(isinstance(work_ns, int) and work_ns >= 0, "bad work sum")
    return work_ns > BUDGET_NS


def verify_resource_accounting() -> int:
    cases = 0
    for durations, expected_work, expected_overage in (
        ([1], 1, False),
        ([1_000_000_000, 999_999_999], 1_999_999_999, False),
        ([1_000_000_000, 1_000_000_000], 2_000_000_000, False),
        ([1_000_000_000, 1_000_000_001], 2_000_000_001, True),
    ):
        work = generation_work(durations)
        require(work == expected_work and is_overage(work) == expected_overage, "generation boundary error")
        cases += 1
    for durations, expected_work, expected_overage in (
        ([], 0, False),
        ([0], 0, False),
        ([2_000_000_000], 2_000_000_000, False),
        ([1_200_000_000, 800_000_001], 2_000_000_001, True),
    ):
        work = replay_work(durations)
        require(work == expected_work and is_overage(work) == expected_overage, "replay boundary error")
        cases += 1
    for bad in ([0], [-1], [1.5]):
        try:
            generation_work(bad)  # type: ignore[arg-type]
        except AssertionError:
            cases += 1
        else:
            raise AssertionError("invalid generation duration accepted")
    for bad in ([-1], [1.5]):
        try:
            replay_work(bad)  # type: ignore[arg-type]
        except AssertionError:
            cases += 1
        else:
            raise AssertionError("invalid replay duration accepted")
    return cases


def primary_pass(raw_a: int, work_a: int, raw_r: int, work_r: int) -> bool:
    require(raw_a >= 0 and raw_r > 0 and work_a > 0 and work_r > 0, "primary domain error")
    return 10 * raw_a * work_r >= 11 * raw_r * work_a


def retention_pass(raw_a: int, raw_r: int) -> bool:
    require(raw_a >= 0 and raw_r > 0, "retention domain error")
    return 1000 * raw_a >= 995 * raw_r


def tail_support_pass(work_a: int, work_r: int) -> bool:
    require(0 < work_a <= work_r, "tail work domain error")
    return 10 * (work_r - work_a) >= work_r


def denominator_outcome(raw_a: int, raw_r: int, raw_tail: int, best_simple_raw: int) -> dict[str, str]:
    require(min(raw_a, raw_r, raw_tail, best_simple_raw) >= 0, "negative raw")
    require(raw_r == raw_a + raw_tail, "raw prefix identity failed")
    if raw_r == 0:
        require(raw_a == raw_tail == 0, "zero retry raw inconsistent")
        return {
            "decision": "DISCONFIRM",
            "delta_e": "NA_zero_retry_raw",
            "rho_raw": "NA_zero_retry_raw",
            "rho_tail": "NA_zero_retry_raw",
            "legacy_rho_simple": "NA_zero_simple_raw" if best_simple_raw == 0 else "0",
        }
    return {
        "decision": "CONTINUE",
        "delta_e": "DEFINED",
        "rho_raw": "DEFINED",
        "rho_tail": "DEFINED",
        "legacy_rho_simple": "NA_zero_simple_raw" if best_simple_raw == 0 else "DEFINED_RETIRED",
    }


def verify_denominator_totality() -> int:
    cases = (
        (0, 0, 0, 0, "DISCONFIRM", "NA_zero_retry_raw", "NA_zero_simple_raw"),
        (995, 1000, 5, 0, "CONTINUE", "DEFINED", "NA_zero_simple_raw"),
        (995, 1000, 5, 800, "CONTINUE", "DEFINED", "DEFINED_RETIRED"),
        (1, 1, 0, 0, "CONTINUE", "DEFINED", "NA_zero_simple_raw"),
    )
    for raw_a, raw_r, raw_tail, simple, decision, delta, legacy in cases:
        observed = denominator_outcome(raw_a, raw_r, raw_tail, simple)
        require(observed["decision"] == decision, "zero-raw decision drift")
        require(observed["delta_e"] == delta, "Delta_E totality drift")
        require(observed["legacy_rho_simple"] == legacy, "rho_simple totality drift")
        if raw_r > 0:
            require(raw_a / raw_r == 1.0 - raw_tail / raw_r, "retention identity drift")
    return len(cases)


def feasible(generation_overages: int, replay_overages: int) -> bool:
    require(generation_overages >= 0 and replay_overages >= 0, "negative overage count")
    return generation_overages == replay_overages == 0


def pareto_dominates_simple(raw_a: int, work_a: int, raw_s: int, work_s: int, simple_feasible: bool) -> bool:
    require(min(raw_a, raw_s) >= 0 and min(work_a, work_s) > 0, "Pareto domain error")
    return simple_feasible and raw_s >= raw_a and work_s <= work_a and (raw_s > raw_a or work_s < work_a)


def simple_control_gate(
    raw_a: int,
    work_a: int,
    raw_s: int,
    work_s: int,
    generation_overages_s: int,
    replay_overages_s: int,
) -> tuple[bool, str]:
    simple_feasible = feasible(generation_overages_s, replay_overages_s)
    if not simple_feasible:
        return True, "infeasible_published"
    efficiency_pass = 10 * raw_a * work_s >= 11 * raw_s * work_a
    dominated = pareto_dominates_simple(raw_a, work_a, raw_s, work_s, True)
    if raw_s == 0 and raw_a > 0:
        label = "positive_over_zero"
    else:
        label = "finite_cross_product"
    return efficiency_pass and not dominated, label


def verify_simple_control_rule() -> tuple[int, int]:
    fixtures = (
        ((100, 100, 500, 10, 1, 0), True, "infeasible_published"),
        ((100, 100, 0, 1, 0, 0), True, "positive_over_zero"),
        ((110, 100, 100, 100, 0, 0), True, "finite_cross_product"),
        ((100, 100, 100, 100, 0, 0), False, "finite_cross_product"),
        ((100, 100, 101, 99, 0, 0), False, "finite_cross_product"),
        ((120, 110, 110, 100, 0, 0), False, "finite_cross_product"),
    )
    for args, expected, label in fixtures:
        observed, observed_label = simple_control_gate(*args)
        require(observed == expected and observed_label == label, "simple-control fixture failed")
    exhaustive = 0
    for raw_a in range(1, 9):
        for work_a in range(1, 9):
            for raw_s in range(0, 9):
                for work_s in range(1, 9):
                    margin = 10 * raw_a * work_s >= 11 * raw_s * work_a
                    dominated = pareto_dominates_simple(raw_a, work_a, raw_s, work_s, True)
                    require(not (margin and dominated), "material efficiency passed a dominating simple")
                    exhaustive += 1
    return len(fixtures), exhaustive


def verify_primary_thresholds() -> int:
    cases = 0
    for raw_a, work_a, raw_r, work_r, expected in (
        (11, 10, 10, 10, True),
        (109, 100, 100, 100, False),
        (100, 90, 100, 100, True),
    ):
        require(primary_pass(raw_a, work_a, raw_r, work_r) == expected, "primary threshold error")
        cases += 1
    for raw_a, raw_r, expected in ((995, 1000, True), (994, 1000, False), (1, 1, True)):
        require(retention_pass(raw_a, raw_r) == expected, "retention threshold error")
        cases += 1
    for work_a, work_r, expected in ((90, 100, True), (91, 100, False), (1, 10, True)):
        require(tail_support_pass(work_a, work_r) == expected, "tail threshold error")
        cases += 1
    return cases


def reference_raw_score(findings: list[tuple[str, tuple[int, ...]]]) -> int:
    weights = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
    severity_total = sum(weights[severity] for _, severities in findings for severity in severities)
    unique_cells = {cell for cell, _ in findings}
    return severity_total + 2 * len(unique_cells)


def verify_raw_prefix_scoring() -> int:
    fixtures = (
        (
            [("cell_a", (5,)), ("cell_b", (1,))],
            [("cell_a", (5,)), ("cell_b", (1,)), ("cell_c", (4,))],
        ),
        (
            [("cell_a", (5,))],
            [("cell_a", (5,)), ("cell_a", (5,))],
        ),
        (
            [],
            [("cell_z", (3, 2))],
        ),
    )
    for prefix, retry in fixtures:
        raw_a = reference_raw_score(prefix)
        raw_r = reference_raw_score(retry)
        require(raw_a <= raw_r, "prefix raw is not monotone")
        raw_tail = raw_r - raw_a
        require(raw_r == raw_a + raw_tail and raw_tail >= 0, "marginal tail identity failed")
    prefix, retry = fixtures[1]
    standalone_tail = reference_raw_score(retry[len(prefix) :])
    require(standalone_tail != reference_raw_score(retry) - reference_raw_score(prefix), "duplicate fixture did not expose nonadditivity")
    two_units = [[("same_cell", (5,))], [("same_cell", (5,))]]
    per_unit_total = sum(reference_raw_score(unit) for unit in two_units)
    cross_unit_score = reference_raw_score([finding for unit in two_units for finding in unit])
    require(per_unit_total != cross_unit_score, "cross-unit fixture did not expose scoring boundary")
    return len(fixtures)


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
    require(hypothesis_lines == 686, "hypothesis line-count drift")
    for required_text in (
        "Supersedes:** `research-log/171-hypothesis-iter-8-ahcms24-v3.md`",
        "**Absorbing HCMS-24 (AHCMS-24).**",
        "## 8. Exact resource accounting",
        "## 9. Raw, efficiency and total denominator rules",
        "## 10. Endpoint-aligned Occam controls",
        "NA_zero_retry_raw",
        "NA_zero_simple_raw",
        "10 * R_a * W_s >= 11 * R_s * W_a",
        "strict greater-than",
        "projected aggregate replay work",
        "## 14. Fixed eight-category bias surface",
        "## 20. Round-10 issue disposition encoded by v4",
        "Review remains `10/12`",
        "Phase 2 remains closed",
    ):
        require(required_text in hypothesis, f"hypothesis contract missing: {required_text}")

    require(config["schema_version"] == "ahcms24-c3-v4", "wrong schema")
    require(config["short_name"] == "AHCMS-24", "concept drift")
    require(config["supersedes"] == "experiments/configs/ahcms24-c3-v3.json", "lineage missing")
    require(config["hypothesis_path"] == hypothesis_path.relative_to(root).as_posix(), "hypothesis path drift")
    require(config["official_score_claim"] == "withheld_until_separate_target_confidence_bridge", "official claim opened")
    require(config["target_void_proof_claim"] == "forbidden_remote_env_operations_are_not_cancellable", "remote overclaim")
    require(sha256(root / "experiments/attack.py") == config["base_attack_sha256"], "attack changed")

    source_count = verify_bindings(root, config["source_bindings"], "source")
    evidence_count = verify_bindings(root, config["evidence_bindings"], "evidence")
    lineage_count = verify_bindings(root, config["superseded_lineage_bindings"], "lineage")
    run_factorial_audit(root)

    require(config["path_cap"] == config["candidate_cap"] == 16, "support cap drift")
    require(config["prefixes_descending"] == [24, 8, 1], "prefix set drift")
    budgets = config["controlled_budgets_s"]
    require(budgets["generation_work_per_unit"] == budgets["aggregate_replay_work_per_unit"] == 2.0, "budget drift")
    numeric = config["numeric_contract"]
    require("time.monotonic_ns" in numeric["duration_storage"], "integer timing absent")
    require("2000000000" in numeric["budget_storage"], "integer boundary absent")
    require("Python integers" in numeric["decision_arithmetic"], "integer decisions absent")

    sampling_digest = verify_sampling(config)
    trace = config["matched_trace_unit"]
    require("q-independent" in trace["definition"] and "16 path slots" in trace["definition"], "trace support drift")
    require("no evaluated method is executed during capture" in trace["process_boundary"], "method contaminates capture")
    require("all 16 path slots" in trace["retry_trace"], "retry tail not captured")
    require("same stored table" in trace["policy_projection"], "methods not matched")
    require("invalidates" in trace["missing_rule"], "missing rows can be dropped")

    methods = config["methods"]
    require(set(methods) == {"ahcms_absorbing", "hcms_retry_removal", "fixed8_absorbing", "fixed24_no_salvage_absorbing"}, "method set drift")
    for field in ("policy", "replay_ledger", "generation_gate"):
        require(methods["ahcms_absorbing"][field] == methods["hcms_retry_removal"][field], f"primary pair differs: {field}")
    require(methods["hcms_retry_removal"]["status"] == "single clean removal of absorbing_no_fit", "removal drift")

    accounting = config["resource_accounting"]
    require("candidate-or-drop" in accounting["generation_duration_boundary"], "generation end boundary absent")
    require("including any path" in accounting["selected_paths"], "trigger path excluded")
    require("2000000000" in accounting["generation_overage_formula"], "generation overage not integer")
    require("ordered multiset" in accounting["accepted_candidates"], "accepted occurrence set ambiguous")
    require("final scorer completion" in accounting["replay_duration_boundary"], "replay end boundary absent")
    require("empty sum equal to 0" in accounting["per_unit_aggregate_replay_work_formula"], "empty replay undefined")
    require("2000000000" in accounting["aggregate_replay_overage_formula"], "replay overage not integer")
    require("not live method wall-clock" in accounting["interpretation"], "wall-clock overclaim")

    totality = config["decision_totality"]
    require("DISCONFIRM" in totality["zero_retry_raw"], "zero retry raw not decided")
    require("NA_zero_retry_raw" in totality["zero_retry_raw"], "zero retry sentinel absent")
    require("rho_raw=1-rho_tail" in totality["retention_identity"], "retention redundancy absent")
    require("rho_simple is retired" in totality["legacy_rho_simple"], "raw-only control retained")
    require("NA_zero_simple_raw" in totality["legacy_rho_simple"], "simple zero sentinel absent")
    require(totality["decision_order"].startswith("first validate"), "decision order open")

    occam = config["occam_rule"]
    require(occam["simple_controls"] == ["fixed8_absorbing", "fixed24_no_salvage_absorbing"], "simple controls drift")
    require("O_G(m)=0 and O_R(m)=0" in occam["feasible"], "feasibility incomplete")
    require("R_ahcms*W_s >= 1.10*R_s*W_ahcms" in occam["efficiency_materiality"], "endpoint margin absent")
    require("Pareto-dominates" in occam["pareto_dominance"], "Pareto rule absent")
    require("either it is infeasible" in occam["confirmation"], "simple decision not total")

    components = config["contribution_components"]
    require(len(components) == 1 and components[0]["id"] == "absorbing_no_fit", "component count drift")
    require(components[0]["clean_removal"] == "hcms_retry_removal", "clean removal drift")
    diagnostics = config["unclaimed_diagnostics"]
    require("not part of AHCMS behavior" in diagnostics["replay_envelope"], "replay envelope claimed")
    require("not part of AHCMS behavior" in diagnostics["atomic_gate"], "atomic gate claimed")
    require("zero estimable complete 2^3 cells" in diagnostics["factorial_status"], "factorial gap hidden")

    phase3 = config["phase3"]
    confirm = phase3["confirm"]
    require(len(phase3["profiles"]) == 3 and len(phase3["methods"]) == 4, "grid drift")
    require(confirm["minimum_absorbing_to_retry_efficiency_ratio"] == 1.10, "primary threshold drift")
    require(confirm["minimum_absorbing_raw_retention"] == 0.995, "retention threshold drift")
    require(confirm["minimum_retry_tail_generation_fraction"] == 0.10, "tail threshold drift")
    require(confirm["retry_tail_recovered_raw_fraction_role"] == "consistency_diagnostic_not_independent_evidence", "redundant tail promoted")
    require(confirm["minimum_absorbing_to_each_feasible_simple_efficiency_ratio"] == 1.10, "simple threshold drift")
    require(confirm["require_no_feasible_simple_pareto_dominates_absorbing"] is True, "Pareto gate disabled")
    require(confirm["projected_method_cells"] == 36, "cell count drift")
    require(confirm["contribution_components"] == confirm["clean_component_removals"] == 1, "component gate drift")
    require("retry raw is zero" in phase3["decision_bands"]["disconfirm"], "zero-raw escape hatch")

    accounting_cases = verify_resource_accounting()
    denominator_cases = verify_denominator_totality()
    simple_fixtures, simple_exhaustive = verify_simple_control_rule()
    primary_cases = verify_primary_thresholds()
    raw_prefix_cases = verify_raw_prefix_scoring()

    runner = root / phase3["runner_path"]
    attempt = root / phase3["attempt_dir"]
    require(not runner.exists(), "Phase-3 runner exists before review")
    require(not attempt.exists(), "Phase-3 attempt exists before review")
    require(config["target_confidence_bridge"]["status"] == "closed_during_phase2_and_phase3", "target bridge opened")

    gateway = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py").read_text()
    inference = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_inference_server.py").read_text()
    require("DEFAULT_BUDGET_S = 9000.0" in gateway, "gateway budget source drift")
    require("Attack code cannot cancel an in-flight RemoteEnv operation" in inference, "cancellation source drift")
    scorer = (root / "comp/sdk/aicomp_sdk/scoring.py").read_text()
    require("total += SEVERITY_W.get" in scorer and "2.0 * len(uniq_cells)" in scorer, "raw scorer source drift")

    print("ahcms24_phase2_author_check_v4=PASS")
    print(f"hypothesis_lines={hypothesis_lines}")
    print(f"source_bindings={source_count}")
    print(f"evidence_bindings={evidence_count}")
    print(f"lineage_bindings={lineage_count}")
    print("round10_issues_addressed=3")
    print("simple_control_endpoint=feasible_efficiency_plus_pareto")
    print("legacy_rho_simple_decision_role=retired")
    print("generation_overage_boundary_ns=2000000000_strict_greater")
    print("aggregate_replay_overage_boundary_ns=2000000000_strict_greater")
    print("generation_metric=projected_work_not_wall_clock")
    print("replay_metric=accepted_candidate_actual_replay_projected_sum")
    print(f"resource_accounting_fixture_cases={accounting_cases}")
    print(f"denominator_totality_cases={denominator_cases}")
    print("zero_retry_raw=disconfirm")
    print("zero_simple_raw=positive_over_zero_or_diagnostic_sentinel")
    print(f"simple_control_fixture_cases={simple_fixtures}")
    print(f"simple_control_exhaustive_cases={simple_exhaustive}")
    print(f"primary_threshold_cases={primary_cases}")
    print(f"raw_prefix_scoring_cases={raw_prefix_cases}")
    print("retention_tail_relation=consistency_not_independent_evidence")
    print("full_two_cubed_factorial_estimable_cells=0")
    print("sampling_manifest=single_draw_no_retry")
    print(f"fisher_yates_demo_digest={sampling_digest}")
    print("fresh_units=3_profiles_x_3_masters")
    print("method_predecessor=none_matched_trace_projection")
    print("contribution_components=1")
    print("clean_component_removals=1")
    print("official_score_claim=withheld")
    print("attack_unchanged=true")
    print("phase3_artifacts=absent")
    print("review=not_dispatched")


if __name__ == "__main__":
    main()
