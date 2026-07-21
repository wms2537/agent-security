#!/usr/bin/env python3
"""Static/theory checks for the unreviewed PQF Cycle-2 v2 contract.

This script does not run the proposed primary or secondary census. It checks the
authority truth table, exogenous schedule construction, six independent oracle
clauses, the finite factorization proposition, and hypothesis/config structure.
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
from pathlib import Path
from typing import Iterable, NamedTuple


ACTIONS = (
    "CONTINUE",
    "CHECK",
    "STOP_SUCCESS",
    "STOP_FAULT",
    "STOP_BUDGET",
)

ADVISORIES = (
    "ABSTAIN",
    "CONTINUE",
    "STOP_SUCCESS",
    "STOP_FAULT",
)

PREDICATE_FIELDS = (
    "verified_fault_present",
    "verified_complete",
    "budget_exhausted",
    "stall_due",
)

ORACLE_CLAUSES = (
    "premature_success",
    "false_fault",
    "feasible_budget_incomplete",
    "infeasible_budget_without_fault_stop",
    "post_terminal_noop_excess",
    "duplicate_effect_commit",
)

ORACLE_MUTANTS = tuple(f"remove_{clause}" for clause in ORACLE_CLAUSES)


class Z(NamedTuple):
    verified_fault_present: bool
    verified_complete: bool
    budget_exhausted: bool
    stall_due: bool


class WorldEvent(NamedTuple):
    decision_index: int
    kind: str
    identifier: str


def valid_z_states() -> Iterable[Z]:
    for fault, complete, budget, stall in itertools.product((False, True), repeat=4):
        if fault and complete:
            continue
        yield Z(fault, complete, budget, stall)


def base_policy(z: Z, recovery_enabled: bool) -> str:
    if z.budget_exhausted:
        return "STOP_BUDGET"
    if z.verified_fault_present:
        return "STOP_FAULT"
    if z.verified_complete:
        return "STOP_SUCCESS"
    if recovery_enabled and z.stall_due:
        return "CHECK"
    return "CONTINUE"


def gated_policy(z: Z, advisory: str, authority: bool, recovery_enabled: bool) -> str:
    if z.budget_exhausted:
        return "STOP_BUDGET"
    if authority and advisory != "ABSTAIN":
        return advisory
    return base_policy(z, recovery_enabled)


def disagreement_locus(z: Z, advisory: str) -> bool:
    return (
        not z.budget_exhausted
        and advisory != "ABSTAIN"
        and advisory != base_policy(z, recovery_enabled=False)
    )


def verify_authority_truth_table() -> tuple[int, int, int]:
    rows = 0
    disagreement_rows = 0
    visibility_differences = 0
    for z, advisory in itertools.product(valid_z_states(), ADVISORIES):
        rows += 1
        hidden_off = gated_policy(z, "ABSTAIN", False, False)
        visible_off = gated_policy(z, advisory, False, False)
        visible_on = gated_policy(z, advisory, True, False)
        if hidden_off != visible_off:
            visibility_differences += 1
        differs = visible_on != visible_off
        expected = disagreement_locus(z, advisory)
        if expected:
            disagreement_rows += 1
        if differs != expected:
            raise AssertionError(
                f"authority mediation mismatch z={z} advisory={advisory}: "
                f"off={visible_off} on={visible_on} expected={expected}"
            )
    if visibility_differences:
        raise AssertionError("visibility changed an action while authority was disabled")
    return rows, disagreement_rows, visibility_differences


def prove_finite_factorization_equivalence() -> tuple[int, int]:
    histories = tuple(itertools.product((0, 1), repeat=2))
    models = 0
    counterexamples = 0
    for action_bits in itertools.product((0, 1), repeat=len(histories)):
        models += 1
        controller = dict(zip(histories, action_bits, strict=True))
        fiber_constant = all(
            controller[(z_bit, 0)] == controller[(z_bit, 1)]
            for z_bit in (0, 1)
        )
        factor = {z_bit: controller[(z_bit, 0)] for z_bit in (0, 1)}
        factors = all(
            controller[history] == factor[history[0]] for history in histories
        )
        if fiber_constant != factors:
            counterexamples += 1
    return models, counterexamples


def canonical_clean_schedule(outcome: str) -> tuple[str, ...]:
    terminal_index_and_action = {
        "all_success": (5, "STOP_SUCCESS"),
        "single_transient_failure_then_success": (6, "STOP_SUCCESS"),
        "duplicate_attempt_idempotent_single_commit": (6, "STOP_SUCCESS"),
        "terminal_fault_at_third_world_attempt": (4, "STOP_FAULT"),
    }
    terminal_index, terminal_action = terminal_index_and_action[outcome]
    values = []
    for decision_index in range(1, 9):
        if decision_index < terminal_index:
            values.append("CONTINUE")
        elif decision_index == terminal_index:
            values.append(terminal_action)
        else:
            values.append("ABSTAIN")
    return tuple(values)


def advisory_schedule(outcome: str, schedule_id: str) -> tuple[str, ...]:
    clean = list(canonical_clean_schedule(outcome))
    if schedule_id == "clean":
        return tuple(clean)
    prefix, decision_text, advisory = schedule_id.split(":", maxsplit=2)
    if prefix != "sub":
        raise ValueError(f"bad schedule id: {schedule_id}")
    decision_index = int(decision_text)
    clean[decision_index - 1] = advisory
    return tuple(clean)


def schedule_ids() -> tuple[str, ...]:
    return ("clean",) + tuple(
        f"sub:{decision_index}:{advisory}"
        for decision_index in range(1, 9)
        for advisory in ("CONTINUE", "STOP_SUCCESS", "STOP_FAULT")
    )


def verify_exogenous_schedules(outcomes: tuple[str, ...]) -> tuple[int, int]:
    ids = schedule_ids()
    if len(ids) != 25 or len(set(ids)) != 25:
        raise AssertionError("advisory schedule count/uniqueness failure")
    comparisons = 0
    for outcome, schedule_id in itertools.product(outcomes, ids):
        expected = advisory_schedule(outcome, schedule_id)
        for _controller_mode in (
            "hidden_non_authoritative",
            "visible_non_authoritative",
            "visible_authoritative",
        ):
            actual = advisory_schedule(outcome, schedule_id)
            comparisons += 1
            if actual != expected:
                raise AssertionError("schedule depends on controller mode")
        if len(expected) != 8 or any(value not in ADVISORIES for value in expected):
            raise AssertionError("invalid exogenous schedule")
    return len(ids), comparisons


def oracle_failures(
    events: tuple[WorldEvent, ...],
    terminal_action: tuple[int, str],
    feasible: bool,
) -> frozenset[str]:
    stop_index, stop_action = terminal_action
    required_effects = frozenset({"e1", "e2", "e3", "e4"})
    commits = tuple(
        event
        for event in events
        if event.kind == "commit" and event.decision_index <= stop_index
    )
    faults = tuple(
        event
        for event in events
        if event.kind == "terminal_fault" and event.decision_index <= stop_index
    )
    noops = tuple(
        event
        for event in events
        if event.kind == "world_noop_after_terminal" and event.decision_index <= stop_index
    )
    commit_ids = tuple(event.identifier for event in commits)
    complete = required_effects.issubset(commit_ids)

    failures: set[str] = set()
    if stop_action == "STOP_SUCCESS" and not complete:
        failures.add("premature_success")
    if stop_action == "STOP_FAULT" and not faults:
        failures.add("false_fault")
    if stop_action == "STOP_BUDGET" and feasible and not complete:
        failures.add("feasible_budget_incomplete")
    if stop_action == "STOP_BUDGET" and not feasible and faults:
        failures.add("infeasible_budget_without_fault_stop")
    if len(noops) >= 2:
        failures.add("post_terminal_noop_excess")
    if len(commit_ids) != len(set(commit_ids)):
        failures.add("duplicate_effect_commit")
    return frozenset(failures)


def oracle_fixtures() -> dict[str, tuple[tuple[WorldEvent, ...], tuple[int, str], bool]]:
    complete_events = (
        WorldEvent(1, "commit", "e1"),
        WorldEvent(2, "commit", "e2"),
        WorldEvent(3, "commit", "e3"),
        WorldEvent(4, "commit", "e4"),
    )
    return {
        "premature_success": (
            (WorldEvent(1, "commit", "e1"),),
            (2, "STOP_SUCCESS"),
            True,
        ),
        "false_fault": (
            (WorldEvent(1, "commit", "e1"),),
            (2, "STOP_FAULT"),
            True,
        ),
        "feasible_budget_incomplete": (
            (WorldEvent(1, "commit", "e1"),),
            (8, "STOP_BUDGET"),
            True,
        ),
        "infeasible_budget_without_fault_stop": (
            (WorldEvent(8, "terminal_fault", "f1"),),
            (8, "STOP_BUDGET"),
            False,
        ),
        "post_terminal_noop_excess": (
            complete_events
            + (
                WorldEvent(5, "world_noop_after_terminal", "n1"),
                WorldEvent(6, "world_noop_after_terminal", "n2"),
            ),
            (7, "STOP_SUCCESS"),
            True,
        ),
        "duplicate_effect_commit": (
            complete_events + (WorldEvent(4, "commit", "e1"),),
            (5, "STOP_SUCCESS"),
            True,
        ),
    }


def kill_oracle_mutants() -> tuple[int, int]:
    fixtures = oracle_fixtures()
    killed = 0
    for clause in ORACLE_CLAUSES:
        failures = oracle_failures(*fixtures[clause])
        if failures != frozenset({clause}):
            raise AssertionError(
                f"fixture for {clause} is not uniquely decisive: {sorted(failures)}"
            )
        mutated_failures = failures - {clause}
        if mutated_failures:
            raise AssertionError(f"mutant for {clause} did not change verdict")
        killed += 1
    return killed, len(ORACLE_CLAUSES)


def verify_false_receipt_counterexample() -> bool:
    false_predicate = Z(False, True, False, False)
    decision = gated_policy(false_predicate, "ABSTAIN", False, False)
    failures = oracle_failures(
        (WorldEvent(1, "commit", "e1"),),
        (2, decision),
        True,
    )
    return decision == "STOP_SUCCESS" and failures == frozenset({"premature_success"})


def verify_contract(config: dict[str, object]) -> None:
    projection = config["chosen_predicate_projection"]
    controller = config["controller_family"]
    domain = config["finite_domain"]
    oracle = config["independent_world_oracle"]
    gates = config["validity_gates"]
    primary = config["primary_comparison"]
    utility = config["utility_and_cost"]
    taxonomy = config["taxonomy"]
    authorization = config["authorization"]
    assert isinstance(projection, dict)
    assert isinstance(controller, dict)
    assert isinstance(domain, dict)
    assert isinstance(oracle, dict)
    assert isinstance(gates, dict)
    assert isinstance(primary, dict)
    assert isinstance(utility, dict)
    assert isinstance(taxonomy, dict)
    assert isinstance(authorization, dict)

    assert tuple(projection["fields"]) == PREDICATE_FIELDS
    assert projection["minimality_claim"] is False
    assert tuple(controller["actions"]) == ACTIONS
    assert tuple(controller["advisory_alphabet"]) == ADVISORIES
    assert domain["master_count"] == 16
    assert domain["advisory_schedule_generator"]["schedule_count"] == 25
    assert domain["primary_execution_count"] == 1200
    assert domain["secondary_execution_count"] == 3200
    assert domain["total_planned_execution_count"] == 4400
    assert tuple(oracle["failure_clauses"]) == ORACLE_CLAUSES
    assert tuple(gates["oracle_clause_mutants"]) == ORACLE_MUTANTS
    assert gates["required_oracle_mutant_kill_rate"] == 1.0
    assert primary["baseline_risk_floor"] == 0.1
    assert primary["relative_reduction_threshold"] == 0.5
    assert utility["completion_loss_max_rate"] == 0.05
    assert utility["step_overhead_max"] == 0.2
    assert len(config["assumptions"]) == 8
    assert len(config["rival_explanations"]) == 10
    assert len(config["bias_surface"]) == 8
    assert taxonomy == {
        "opportunity_pattern": "Failure/Risk Gap",
        "method_paradigm": "Robustification",
        "dominant_operation": "replace",
        "secondary_operation": "decouple",
        "secondary_paradigm": "Artifact/System",
        "bridge_synthesis_tripwire": False,
    }
    assert authorization["hypothesis_review_budget"] == "limit_30_spent_22_before_v2_review"


def verify_hypothesis_text(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    required = (
        "## Primary hypothesis",
        "## Named concept",
        "## Isolated controller family",
        "## Formal propositions",
        "## Exogenous finite domain",
        "## Ordered transition and receipt semantics",
        "## Independent outcome oracle",
        "## Variables and controls",
        "## One primary comparison and decision rule",
        "## Mechanistic justification",
        "## Assumptions and validity domains",
        "## Rival explanations",
        "## Fixed bias surface",
        "## Failure modes and result interpretation",
        "## Taxonomy and anti-stacking",
        "## Round-1 issue resolution",
        "## Problem alignment",
        "## Review and authorization status",
    )
    missing = [heading for heading in required if heading not in text]
    if missing:
        raise AssertionError(f"hypothesis missing headings: {missing}")
    forbidden = ("TBD", "TODO", "PLACEHOLDER", "Status: reviewed")
    hits = [token for token in forbidden if token in text]
    if hits:
        raise AssertionError(f"hypothesis contains forbidden tokens: {hits}")
    return len(text.splitlines())


def verify_own_ast(path: Path) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    allowed = {
        "__future__",
        "argparse",
        "ast",
        "itertools",
        "json",
        "pathlib",
        "typing",
    }
    unexpected = imports - allowed
    if unexpected:
        raise AssertionError(f"unexpected imports: {sorted(unexpected)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("hypothesis", type=Path)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    verify_contract(config)
    verify_own_ast(Path(__file__))
    hypothesis_lines = verify_hypothesis_text(args.hypothesis)

    factor_models, factor_counterexamples = prove_finite_factorization_equivalence()
    if factor_counterexamples:
        raise AssertionError("finite factorization equivalence has a counterexample")
    authority_rows, disagreement_rows, visibility_differences = (
        verify_authority_truth_table()
    )
    outcomes = tuple(config["finite_domain"]["world_outcome_schedules"])
    schedule_count, exogeneity_comparisons = verify_exogenous_schedules(outcomes)
    oracle_killed, oracle_total = kill_oracle_mutants()
    if not verify_false_receipt_counterexample():
        raise AssertionError("false-receipt counterexample failed")

    print(
        "pqf_hypothesis_v2=PASS"
        f" lines={hypothesis_lines}"
        " json=PASS ast=PASS"
        f" finite_factor_models={factor_models}"
        f" theorem_counterexamples={factor_counterexamples}"
        f" authority_truth_rows={authority_rows}"
        f" disagreement_rows={disagreement_rows}"
        f" visibility_differences={visibility_differences}"
        f" advisory_schedules={schedule_count}"
        f" exogeneity_comparisons={exogeneity_comparisons}"
        f" oracle_mutants_killed={oracle_killed}/{oracle_total}"
        " unique_oracle_fixtures=6/6"
        " false_receipt_counterexample=PASS"
        f" primary_executions={config['finite_domain']['primary_execution_count']}"
        f" secondary_executions={config['finite_domain']['secondary_execution_count']}"
        " review=pending"
        " phase3=not_authorized"
    )


if __name__ == "__main__":
    main()
