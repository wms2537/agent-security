#!/usr/bin/env python3
"""Deterministic author checker for the AHCMS-24 v5 hypothesis."""

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
    require(identity != reverse, "shuffle demo degenerate")
    return hashlib.sha256((repr(identity) + "|" + repr(reverse)).encode()).hexdigest()


def run_timer_audit(root: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "-I", "experiments/poc/ahcms24_round11_timer_audit.py"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    observed = set(completed.stdout.splitlines())
    required = {
        "ahcms24_round11_timer_audit=PASS",
        "scientific_runner_executed=false",
        "generation_start=before_generation_environment_checkpoint",
        "generation_end=after_last_interaction_complete_checkpoint_before_exact_prefix_selection",
        "generation_includes=checkpoint_serialization,environment_construction,reset,interactions,in_interval_scheduling",
        "generation_excludes=exact_prefix_extraction,candidate_selection,publication,artifact_fsync",
        "replay_start=before_replay_environment_checkpoint",
        "replay_end=after_last_interaction_complete_checkpoint_before_final_trace_and_scorer",
        "replay_includes=checkpoint_serialization,environment_construction,reset,interactions,in_interval_scheduling",
        "replay_excludes=final_trace_export,predicates,signature,scorer,publication,artifact_fsync",
        "clock_interpretation=captured_elapsed_not_cpu_time_or_remote_deadline_proof",
        "historical_retry_paths=370",
        "historical_retry_elapsed_s=69.00197669875342412",
        "historical_retry_tail_paths=146",
        "historical_retry_tail_elapsed_s=18.36650123470462862",
        "historical_absorbing_elapsed_s=50.63547546404879550",
        "historical_nominal_efficiency_ratio=1.362095216773",
        "historical_half_tail_efficiency_ratio=1.180818355750",
        "historical_half_tail_fraction=0.153517990418",
        "prospective_sensitivity=charge_only_half_retry_tail_elapsed_keep_all_retry_raw",
        "scheduler_bound_scope=bounded_sensitivity_not_arbitrary_or_systematic_noise_guarantee",
    }
    require(required <= observed, "timer audit output drift")


def generation_elapsed(path_durations_ns: list[int]) -> int:
    require(
        all(isinstance(value, int) and not isinstance(value, bool) and value > 0 for value in path_durations_ns),
        "bad generation elapsed",
    )
    return sum(path_durations_ns)


def replay_elapsed(accepted_durations_ns: list[int]) -> int:
    require(
        all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in accepted_durations_ns),
        "bad replay elapsed",
    )
    return sum(accepted_durations_ns)


def is_overage(elapsed_ns: int) -> bool:
    require(isinstance(elapsed_ns, int) and not isinstance(elapsed_ns, bool) and elapsed_ns >= 0, "bad elapsed sum")
    return elapsed_ns > BUDGET_NS


def verify_elapsed_accounting() -> int:
    cases = 0
    for durations, expected_sum, expected_overage in (
        ([1], 1, False),
        ([1_000_000_000, 999_999_999], 1_999_999_999, False),
        ([1_000_000_000, 1_000_000_000], 2_000_000_000, False),
        ([1_000_000_000, 1_000_000_001], 2_000_000_001, True),
    ):
        elapsed = generation_elapsed(durations)
        require(elapsed == expected_sum and is_overage(elapsed) == expected_overage, "generation boundary error")
        cases += 1
    for durations, expected_sum, expected_overage in (
        ([], 0, False),
        ([0], 0, False),
        ([2_000_000_000], 2_000_000_000, False),
        ([1_200_000_000, 800_000_001], 2_000_000_001, True),
    ):
        elapsed = replay_elapsed(durations)
        require(elapsed == expected_sum and is_overage(elapsed) == expected_overage, "replay boundary error")
        cases += 1
    for bad in ([0], [-1], [1.5], [True]):
        try:
            generation_elapsed(bad)  # type: ignore[arg-type]
        except AssertionError:
            cases += 1
        else:
            raise AssertionError("invalid generation elapsed accepted")
    for bad in ([-1], [1.5], [True]):
        try:
            replay_elapsed(bad)  # type: ignore[arg-type]
        except AssertionError:
            cases += 1
        else:
            raise AssertionError("invalid replay elapsed accepted")
    return cases


def primary_pass(raw_a: int, elapsed_a: int, raw_r: int, elapsed_r: int) -> bool:
    require(raw_a >= 0 and raw_r > 0 and elapsed_a > 0 and elapsed_r >= elapsed_a, "primary domain error")
    return 10 * raw_a * elapsed_r >= 11 * raw_r * elapsed_a


def retention_pass(raw_a: int, raw_r: int) -> bool:
    require(raw_a >= 0 and raw_r > 0, "retention domain error")
    return 1000 * raw_a >= 995 * raw_r


def tail_support_pass(elapsed_a: int, elapsed_r: int) -> bool:
    require(0 < elapsed_a <= elapsed_r, "tail domain error")
    return 10 * (elapsed_r - elapsed_a) >= elapsed_r


def half_tail_endpoint(elapsed_a: int, elapsed_r: int) -> tuple[int, int]:
    require(0 < elapsed_a <= elapsed_r, "half-tail domain error")
    half_tail = (elapsed_r - elapsed_a) // 2
    return half_tail, elapsed_a + half_tail


def sensitivity_pass(raw_a: int, elapsed_a: int, raw_r: int, elapsed_r: int) -> tuple[bool, bool, int, int]:
    require(raw_a >= 0 and raw_r > 0, "sensitivity raw domain error")
    half_tail, retry_half = half_tail_endpoint(elapsed_a, elapsed_r)
    efficiency = 10 * raw_a * retry_half >= 11 * raw_r * elapsed_a
    support = 10 * half_tail >= retry_half
    return efficiency, support, half_tail, retry_half


def verify_primary_and_sensitivity() -> tuple[int, int]:
    primary_cases = 0
    for raw_a, elapsed_a, raw_r, elapsed_r, expected in (
        (11, 10, 10, 10, True),
        (109, 100, 100, 100, False),
        (100, 90, 100, 100, True),
        (0, 100, 1, 120, False),
    ):
        require(primary_pass(raw_a, elapsed_a, raw_r, elapsed_r) == expected, "primary threshold error")
        primary_cases += 1
    for raw_a, raw_r, expected in ((995, 1000, True), (994, 1000, False), (0, 1, False)):
        require(retention_pass(raw_a, raw_r) == expected, "retention threshold error")
        primary_cases += 1
    for elapsed_a, elapsed_r, expected in ((90, 100, True), (91, 100, False), (100, 100, False)):
        require(tail_support_pass(elapsed_a, elapsed_r) == expected, "tail threshold error")
        primary_cases += 1

    sensitivity_cases = 0
    for args, expected in (
        ((100, 100, 100, 120), (True, False, 10, 110)),
        ((100, 90, 100, 110), (True, True, 10, 100)),
        ((100, 100, 100, 119), (False, False, 9, 109)),
        ((0, 90, 1, 111), (False, True, 10, 100)),
    ):
        require(sensitivity_pass(*args) == expected, "half-tail sensitivity error")
        sensitivity_cases += 1
    require(half_tail_endpoint(90, 111) == (10, 100), "odd tail was not floored")
    sensitivity_cases += 1
    return primary_cases, sensitivity_cases


def feasible(generation_overages: int, replay_overages: int) -> bool:
    require(generation_overages >= 0 and replay_overages >= 0, "negative overage count")
    return generation_overages == replay_overages == 0


def pareto_dominates_simple(
    raw_a: int,
    elapsed_a: int,
    raw_s: int,
    elapsed_s: int,
    simple_feasible: bool,
) -> bool:
    require(min(raw_a, raw_s) >= 0 and min(elapsed_a, elapsed_s) > 0, "Pareto domain error")
    return (
        simple_feasible
        and raw_s >= raw_a
        and elapsed_s <= elapsed_a
        and (raw_s > raw_a or elapsed_s < elapsed_a)
    )


def simple_control_gate(
    raw_a: int,
    elapsed_a: int,
    raw_s: int,
    elapsed_s: int,
    generation_overages_s: int,
    replay_overages_s: int,
) -> tuple[bool, str, bool]:
    simple_feasible = feasible(generation_overages_s, replay_overages_s)
    if not simple_feasible:
        return True, "infeasible_published", False
    efficiency = 10 * raw_a * elapsed_s >= 11 * raw_s * elapsed_a
    dominated = pareto_dominates_simple(raw_a, elapsed_a, raw_s, elapsed_s, True)
    if raw_s == 0 and raw_a > 0:
        label = "positive_over_zero"
    elif raw_s == 0 and raw_a == 0:
        label = "zero_zero_defined_cross_product"
    else:
        label = "finite_cross_product"
    return efficiency and not dominated, label, dominated


def verify_simple_controls() -> tuple[int, int]:
    fixtures = (
        ((100, 100, 500, 10, 1, 0), (True, "infeasible_published", False)),
        ((100, 100, 0, 1, 0, 0), (True, "positive_over_zero", False)),
        ((110, 100, 100, 100, 0, 0), (True, "finite_cross_product", False)),
        ((100, 100, 100, 100, 0, 0), (False, "finite_cross_product", False)),
        ((100, 100, 101, 99, 0, 0), (False, "finite_cross_product", True)),
        ((0, 100, 0, 100, 0, 0), (True, "zero_zero_defined_cross_product", False)),
        ((0, 100, 0, 99, 0, 0), (False, "zero_zero_defined_cross_product", True)),
    )
    for args, expected in fixtures:
        require(simple_control_gate(*args) == expected, "simple-control fixture failed")
    exhaustive = 0
    for raw_a in range(0, 9):
        for elapsed_a in range(1, 9):
            for raw_s in range(0, 9):
                for elapsed_s in range(1, 9):
                    margin = 10 * raw_a * elapsed_s >= 11 * raw_s * elapsed_a
                    dominated = pareto_dominates_simple(raw_a, elapsed_a, raw_s, elapsed_s, True)
                    if margin and dominated:
                        require(
                            raw_a == raw_s == 0,
                            "positive-domain material efficiency passed a dominating simple",
                        )
                    exhaustive += 1
    return len(fixtures), exhaustive


def denominator_outcome(raw_a: int, raw_r: int, raw_tail: int, max_simple_raw: int) -> dict[str, str]:
    require(min(raw_a, raw_r, raw_tail, max_simple_raw) >= 0, "negative raw")
    require(raw_r == raw_a + raw_tail, "raw prefix identity failed")
    legacy = "NA_zero_simple_raw" if max_simple_raw == 0 else "DEFINED_RETIRED"
    if raw_r == 0:
        require(raw_a == raw_tail == 0, "zero retry raw inconsistent")
        return {
            "decision": "DISCONFIRM_ZERO_RETRY",
            "primary": "NOT_EVALUATED_ZERO_RETRY",
            "retention": "NOT_EVALUATED_ZERO_RETRY",
            "delta_e": "NA_zero_retry_raw",
            "rho_raw": "NA_zero_retry_raw",
            "rho_tail": "NA_zero_retry_raw",
            "legacy_rho_simple": legacy,
        }
    if raw_a == 0:
        return {
            "decision": "DISCONFIRM_ZERO_AHCMS_POSITIVE_RETRY",
            "primary": "FAIL_ZERO_LEFT_POSITIVE_RIGHT",
            "retention": "FAIL_ZERO_LEFT_POSITIVE_RIGHT",
            "delta_e": "DEFINED_ZERO",
            "rho_raw": "DEFINED_ZERO",
            "rho_tail": "DEFINED_ONE",
            "legacy_rho_simple": legacy,
        }
    return {
        "decision": "CONTINUE",
        "primary": "DEFINED",
        "retention": "DEFINED",
        "delta_e": "DEFINED",
        "rho_raw": "DEFINED",
        "rho_tail": "DEFINED",
        "legacy_rho_simple": legacy,
    }


def verify_denominator_totality() -> int:
    cases = (
        ((0, 0, 0, 0), "DISCONFIRM_ZERO_RETRY", "NA_zero_retry_raw", "NA_zero_simple_raw"),
        ((0, 1, 1, 0), "DISCONFIRM_ZERO_AHCMS_POSITIVE_RETRY", "DEFINED_ZERO", "NA_zero_simple_raw"),
        ((0, 10, 10, 5), "DISCONFIRM_ZERO_AHCMS_POSITIVE_RETRY", "DEFINED_ZERO", "DEFINED_RETIRED"),
        ((995, 1000, 5, 0), "CONTINUE", "DEFINED", "NA_zero_simple_raw"),
        ((995, 1000, 5, 800), "CONTINUE", "DEFINED", "DEFINED_RETIRED"),
    )
    for args, decision, delta, legacy in cases:
        observed = denominator_outcome(*args)
        require(observed["decision"] == decision, "zero branch decision drift")
        require(observed["delta_e"] == delta, "Delta_E branch drift")
        require(observed["legacy_rho_simple"] == legacy, "simple sentinel drift")
        raw_a, raw_r, raw_tail, _ = args
        if raw_r > 0:
            require(raw_a * raw_r == raw_r * raw_a, "integer identity sanity failed")
            require(raw_a / raw_r == 1.0 - raw_tail / raw_r, "retention identity drift")

    # Required adversarial branch: simple endpoint remains defined even though
    # primary/retention already disconfirm positive retry raw recovered in tail.
    branch = denominator_outcome(0, 1, 1, 0)
    simple = simple_control_gate(0, 100, 0, 100, 0, 0)
    require(branch["primary"] == "FAIL_ZERO_LEFT_POSITIVE_RIGHT", "primary did not fail")
    require(branch["retention"] == "FAIL_ZERO_LEFT_POSITIVE_RIGHT", "retention did not fail")
    require(simple == (True, "zero_zero_defined_cross_product", False), "simple zero cross-product undefined")
    require(branch["legacy_rho_simple"] == "NA_zero_simple_raw", "zero-simple sentinel missing")
    return len(cases) + 1


def reference_raw_score(findings: list[tuple[str, tuple[int, ...]]]) -> int:
    weights = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
    severity_total = sum(weights[severity] for _, severities in findings for severity in severities)
    unique_cells = {cell for cell, _ in findings}
    return severity_total + 2 * len(unique_cells)


def verify_raw_prefix_scoring() -> int:
    fixtures = (
        ([('cell_a', (5,)), ('cell_b', (1,))], [('cell_a', (5,)), ('cell_b', (1,)), ('cell_c', (4,))]),
        ([('cell_a', (5,))], [('cell_a', (5,)), ('cell_a', (5,))]),
        ([], [('cell_z', (3, 2))]),
    )
    for prefix, retry in fixtures:
        raw_a = reference_raw_score(prefix)
        raw_r = reference_raw_score(retry)
        require(raw_a <= raw_r, "prefix raw not monotone")
        require(raw_r == raw_a + (raw_r - raw_a), "tail marginal identity failed")
    prefix, retry = fixtures[1]
    require(
        reference_raw_score(retry[len(prefix):]) != reference_raw_score(retry) - reference_raw_score(prefix),
        "duplicate fixture did not expose scorer nonadditivity",
    )
    two_units = [[('same_cell', (5,))], [('same_cell', (5,))]]
    require(
        sum(reference_raw_score(unit) for unit in two_units)
        != reference_raw_score([finding for unit in two_units for finding in unit]),
        "cross-unit scorer boundary absent",
    )
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
    require(hypothesis_lines == 654, "hypothesis line-count drift")
    for required_text in (
        "Supersedes:** `research-log/174-hypothesis-iter-8-ahcms24-v4.md`",
        "**Absorbing HCMS-24 (AHCMS-24).**",
        "## 8. Exact timer endpoints",
        "## 10. Scheduler/controller sensitivity",
        "## 11. Raw, efficiency, and total branch semantics",
        "## 12. Endpoint-aligned specified Occam controls",
        "R_a=0,R_s=0,R_r>0",
        "NA_zero_retry_raw",
        "NA_zero_simple_raw",
        "10 * R_a * T_r_half >= 11 * R_r * T_a",
        "path_cost_s",
        "generation_elapsed_s",
        "including in-bracket scheduling/controller work",
        "reduced global path cap",
        "## 16. Fixed eight-category bias surface",
        "## 22. Round-11 issue disposition encoded by v5",
        "Review remains `11/12`",
        "Phase 2 remains closed",
    ):
        require(required_text in hypothesis, f"hypothesis contract missing: {required_text}")

    require(config["schema_version"] == "ahcms24-c3-v5", "wrong schema")
    require(config["short_name"] == "AHCMS-24", "concept drift")
    require(config["supersedes"] == "experiments/configs/ahcms24-c3-v4.json", "lineage missing")
    require(config["hypothesis_path"] == hypothesis_path.relative_to(root).as_posix(), "hypothesis path drift")
    require(config["official_score_claim"] == "withheld_until_separate_target_confidence_bridge", "official claim opened")
    require(config["target_void_proof_claim"] == "forbidden_remote_env_operations_are_not_cancellable", "remote overclaim")
    require(sha256(root / "experiments/attack.py") == config["base_attack_sha256"], "attack changed")

    source_count = verify_bindings(root, config["source_bindings"], "source")
    evidence_count = verify_bindings(root, config["evidence_bindings"], "evidence")
    lineage_count = verify_bindings(root, config["superseded_lineage_bindings"], "lineage")
    run_timer_audit(root)

    require(config["path_cap"] == config["candidate_cap"] == 16, "support cap drift")
    require(config["prefixes_descending"] == [24, 8, 1], "prefix set drift")
    budgets = config["controlled_budgets_ns"]
    require(
        budgets["generation_projected_captured_elapsed_per_unit"]
        == budgets["aggregate_replay_projected_captured_elapsed_per_unit"]
        == BUDGET_NS,
        "budget drift",
    )
    numeric = config["numeric_contract"]
    require("time.monotonic_ns" in numeric["duration_storage"], "integer timing absent")
    require("strict greater-than" in numeric["budget_storage"], "strict boundary absent")
    require("floor-half sensitivity" in numeric["decision_arithmetic"], "integer sensitivity absent")

    sampling_digest = verify_sampling(config)
    trace = config["matched_trace_unit"]
    require("q-independent" in trace["definition"] and "16 path slots" in trace["definition"], "trace support drift")
    require("no evaluated method" in trace["process_boundary"], "method contaminates capture")
    require("before exact-prefix extraction" in trace["generation_arm_record"], "generation endpoint drift")
    require("before final trace export" in trace["replay_record"], "replay endpoint drift")
    require("all 16 path slots" in trace["retry_trace"], "retry tail not captured")
    require("same stored table" in trace["policy_projection"], "methods not matched")
    require("invalidates" in trace["missing_rule"], "missing rows can be dropped")

    endpoint = config["timer_endpoint_table"]
    require("scheduling delay" in endpoint["generation_included"], "generation scheduler time excluded")
    require("checkpoint canonical-JSON" in endpoint["generation_included"], "generation controller work absent")
    require("exact-prefix extraction" in endpoint["generation_excluded"], "generation post-timer region absent")
    require("scheduling delay" in endpoint["replay_included"], "replay scheduler time excluded")
    require("scorer" in endpoint["replay_excluded"], "replay scorer falsely included")
    require("not CPU service time" in endpoint["interpretation"], "CPU overclaim")

    methods = config["methods"]
    require(
        set(methods)
        == {"ahcms_absorbing", "hcms_retry_removal", "fixed8_absorbing", "fixed24_no_salvage_absorbing"},
        "method set drift",
    )
    for field in ("policy", "replay_ledger", "generation_gate"):
        require(methods["ahcms_absorbing"][field] == methods["hcms_retry_removal"][field], f"primary pair differs: {field}")
    require(methods["hcms_retry_removal"]["status"] == "single clean removal of absorbing_no_fit", "removal drift")

    accounting = config["resource_accounting"]
    require("through and including" in accounting["selected_paths"], "trigger path excluded")
    require("g_ns" in accounting["per_unit_generation_elapsed_formula"], "generation formula absent")
    require("projected captured-elapsed sum" in accounting["aggregate_generation_elapsed_formula"], "aggregate interpretation absent")
    require("2000000000" in accounting["generation_overage_formula"], "generation boundary absent")
    require("ordered multiset" in accounting["accepted_candidates"], "accepted occurrence set ambiguous")
    require("empty sum is 0" in accounting["per_unit_replay_elapsed_formula"], "empty replay undefined")
    require("2000000000" in accounting["aggregate_replay_overage_formula"], "replay boundary absent")
    require("not live method wall-clock" in accounting["interpretation"], "wall-clock overclaim")

    sensitivity = config["scheduler_sensitivity"]
    require("floor(T_tail/2)" in sensitivity["discounted_tail_elapsed"], "half-tail rounding drift")
    require("retain all retry raw" in sensitivity["raw_rule"], "retry raw discounted")
    require("10*R_ahcms*T_retry_half >= 11*R_retry*T_ahcms" in sensitivity["efficiency_guard"], "sensitivity inequality drift")
    require("10*H >= T_retry_half" in sensitivity["tail_support_guard"], "sensitivity support absent")
    require("systematic asymmetry remains" in sensitivity["scope"], "sensitivity overclaim")

    totality = config["decision_totality"]
    require("DISCONFIRMS" in totality["zero_retry_raw"], "zero retry not decided")
    require("R_retry>0 and R_ahcms=0" in totality["positive_retry_zero_ahcms"], "positive-retry zero-AHCMS branch absent")
    require("R_ahcms=R_simple=0 with R_retry>0" in totality["zero_ahcms_zero_simple_positive_retry"], "adversarial simple branch absent")
    require("simple efficiency cross-product remains defined" in totality["zero_ahcms_zero_simple_positive_retry"], "simple branch undefined")
    require("NA_zero_simple_raw" in totality["zero_ahcms_zero_simple_positive_retry"], "zero-simple sentinel absent")
    require("rho_simple=1-rho_tail" not in totality["retention_identity"], "wrong identity")
    require("rho_raw=1-rho_tail" in totality["retention_identity"], "retention identity absent")

    occam = config["occam_rule"]
    require(occam["specified_simple_controls"] == ["fixed8_absorbing", "fixed24_no_salvage_absorbing"], "simple controls drift")
    require("do not exhaust" in occam["scope_limit"], "simple controls overclaimed")
    require("10*R_ahcms*T_s >= 11*R_s*T_ahcms" in occam["efficiency_materiality"], "simple endpoint drift")
    require("Pareto-dominates" in occam["pareto_dominance"], "Pareto rule absent")
    require("reduced global path cap" in occam["unresolved_alternative"], "unresolved simple alternative hidden")

    profile = config["historical_profile"]
    require("path_cost_s" in profile["endpoint"] and "generation_elapsed_s is excluded" in profile["endpoint"], "profile endpoint misaligned")
    require(profile["retry_paths"] == 370 and profile["retry_tail_paths"] == 146, "profile path drift")
    require(profile["retry_elapsed_s"] == "69.00197669875342412", "profile retry elapsed drift")
    require(profile["nominal_efficiency_ratio"] == "1.362095216773", "profile nominal drift")
    require(profile["half_tail_efficiency_ratio"] == "1.180818355750", "profile sensitivity drift")

    components = config["contribution_components"]
    require(len(components) == 1 and components[0]["id"] == "absorbing_no_fit", "component count drift")
    require(components[0]["clean_removal"] == "hcms_retry_removal", "clean removal drift")
    require("exact path timer" in components[0]["measured_bottleneck"], "profile bracket absent")
    require(
        "not claimed" in config["unclaimed_diagnostics"]["global_occam"]
        and "do not exhaust" in config["unclaimed_diagnostics"]["global_occam"],
        "global Occam claim open",
    )

    phase3 = config["phase3"]
    confirm = phase3["confirm"]
    require(len(phase3["profiles"]) == 3 and len(phase3["methods"]) == 4, "grid drift")
    require(confirm["minimum_absorbing_to_retry_efficiency_ratio"] == 1.10, "nominal threshold drift")
    require(confirm["minimum_absorbing_to_retry_half_tail_discount_efficiency_ratio"] == 1.10, "sensitivity threshold drift")
    require(confirm["minimum_absorbing_raw_retention"] == 0.995, "retention drift")
    require(confirm["minimum_half_discounted_retry_tail_elapsed_fraction"] == 0.10, "discounted tail drift")
    require(confirm["projected_method_cells"] == 36, "cell count drift")
    require(confirm["contribution_components"] == confirm["clean_component_removals"] == 1, "component gate drift")
    require("sensitivity" in phase3["decision_bands"]["disconfirm"], "sensitivity failure escape")

    elapsed_cases = verify_elapsed_accounting()
    primary_cases, sensitivity_cases = verify_primary_and_sensitivity()
    denominator_cases = verify_denominator_totality()
    simple_fixtures, simple_exhaustive = verify_simple_controls()
    raw_prefix_cases = verify_raw_prefix_scoring()

    runner = root / phase3["runner_path"]
    attempt = root / phase3["attempt_dir"]
    require(not runner.exists(), "Phase-3 runner exists before review")
    require(not attempt.exists(), "Phase-3 attempt exists before review")
    require(config["target_confidence_bridge"]["status"] == "closed_during_phase2_and_phase3", "target bridge opened")

    gateway = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py").read_text()
    inference = (root / "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_inference_server.py").read_text()
    scorer = (root / "comp/sdk/aicomp_sdk/scoring.py").read_text()
    require("DEFAULT_BUDGET_S = 9000.0" in gateway, "gateway budget source drift")
    require("Attack code cannot cancel an in-flight RemoteEnv operation" in inference, "cancellation source drift")
    require("total += SEVERITY_W.get" in scorer and "2.0 * len(uniq_cells)" in scorer, "raw scorer source drift")

    print("ahcms24_phase2_author_check_v5=PASS")
    print(f"hypothesis_lines={hypothesis_lines}")
    print(f"source_bindings={source_count}")
    print(f"evidence_bindings={evidence_count}")
    print(f"lineage_bindings={lineage_count}")
    print("round11_required_fixes_addressed=2")
    print("endpoint=projected_captured_elapsed_at_historical_brackets")
    print("in_interval_scheduler_and_controller_elapsed=included")
    print("historical_profile_sum=path_cost_s_only")
    print("historical_whole_cell_generation_elapsed=excluded")
    print("generation_end=before_exact_prefix_and_selection")
    print("replay_end=before_final_trace_and_scorer")
    print("overage_boundary_ns=2000000000_strict_greater")
    print(f"elapsed_accounting_fixture_cases={elapsed_cases}")
    print(f"primary_threshold_cases={primary_cases}")
    print(f"scheduler_sensitivity_cases={sensitivity_cases}")
    print("scheduler_sensitivity=half_retry_tail_floor_keep_all_retry_raw")
    print("scheduler_sensitivity_scope=bounded_not_arbitrary")
    print(f"denominator_totality_cases={denominator_cases}")
    print("zero_retry_raw=disconfirm")
    print("zero_ahcms_positive_retry=primary_and_retention_disconfirm")
    print("zero_ahcms_zero_simple_positive_retry=simple_cross_product_defined")
    print("zero_simple_raw_diagnostic=NA_zero_simple_raw")
    print(f"simple_control_fixture_cases={simple_fixtures}")
    print(f"simple_control_exhaustive_cases={simple_exhaustive}")
    print("simple_controls=specified_not_exhaustive")
    print("reduced_global_path_cap=unresolved_alternative")
    print(f"raw_prefix_scoring_cases={raw_prefix_cases}")
    print("retention_tail_relation=consistency_not_independent_evidence")
    print("sampling_manifest=single_draw_no_retry")
    print(f"fisher_yates_demo_digest={sampling_digest}")
    print("fresh_units=3_profiles_x_3_masters")
    print("method_predecessor=none_matched_trace_projection")
    print("official_score_claim=withheld")
    print("attack_unchanged=true")
    print("phase3_artifacts=absent")
    print("review=not_dispatched")


if __name__ == "__main__":
    main()
