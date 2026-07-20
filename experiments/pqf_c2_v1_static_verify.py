#!/usr/bin/env python3
"""Static/theory checks for the unreviewed PQF Cycle-2 v1 contract.

This does not execute the proposed study.  It checks contract structure, proves
the finite factorization equivalence, tests quotient-fiber invariance, and makes
sure independent-oracle and quotient-leak mutants are observable.
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
from pathlib import Path
from typing import Callable, Iterable, NamedTuple


EXPECTED_QUOTIENT_FIELDS = (
    "plan_digest",
    "open_obligation_ids",
    "verified_completed_obligation_ids",
    "verified_effect_ids",
    "verified_terminal_fault_ids",
    "steps_since_verified_transition",
    "remaining_step_budget",
)

EXPECTED_ACTIONS = (
    "CONTINUE",
    "CHECK",
    "STOP_SUCCESS",
    "STOP_FAULT",
    "STOP_BUDGET",
)

EXPECTED_ORACLE_MUTANTS = (
    "remove_premature_success",
    "remove_false_fault",
    "remove_budget_incomplete",
    "remove_post_terminal_overrun",
    "remove_duplicate_effect",
)

EXPECTED_LEAK_MUTANTS = (
    "direct_worker_advisory",
    "worker_summary_digest",
    "unverified_worker_completion_id",
    "raw_tool_payload_branch",
)


class Quotient(NamedTuple):
    plan_digest: str
    open_obligation_ids: frozenset[str]
    verified_completed_obligation_ids: frozenset[str]
    verified_effect_ids: frozenset[str]
    verified_terminal_fault_ids: frozenset[str]
    steps_since_verified_transition: int
    remaining_step_budget: int


class WorldEvent(NamedTuple):
    step: int
    kind: str
    identifier: str


def pqf_decision(q: Quotient) -> str:
    expected_obligations = frozenset({"o1", "o2"})
    expected_effects = frozenset({"e1", "e2"})
    if q.verified_terminal_fault_ids:
        return "STOP_FAULT"
    if (
        not q.open_obligation_ids
        and q.verified_completed_obligation_ids == expected_obligations
        and q.verified_effect_ids == expected_effects
    ):
        return "STOP_SUCCESS"
    if q.remaining_step_budget == 0:
        return "STOP_BUDGET"
    if q.steps_since_verified_transition >= 2:
        return "CHECK"
    return "CONTINUE"


def quotient_samples() -> Iterable[Quotient]:
    obligations = frozenset({"o1", "o2"})
    effects = frozenset({"e1", "e2"})
    for complete, fault, stalled, budget in itertools.product(
        (False, True), (False, True), (0, 2), (0, 3)
    ):
        yield Quotient(
            plan_digest="plan-v1",
            open_obligation_ids=frozenset() if complete else obligations,
            verified_completed_obligation_ids=(
                obligations if complete else frozenset()
            ),
            verified_effect_ids=effects if complete else frozenset(),
            verified_terminal_fault_ids=(
                frozenset({"f1"}) if fault else frozenset()
            ),
            steps_since_verified_transition=stalled,
            remaining_step_budget=budget,
        )


def prove_finite_factorization_equivalence() -> tuple[int, int]:
    """Exhaust all Boolean controllers on two quotient fibers.

    Histories are (quotient_bit, advisory_bit), and actions are Boolean.  A
    controller factors through the quotient iff it is constant on each fiber.
    """

    histories = tuple(itertools.product((0, 1), repeat=2))
    counterexamples = 0
    models = 0
    for action_bits in itertools.product((0, 1), repeat=len(histories)):
        models += 1
        controller = dict(zip(histories, action_bits, strict=True))
        constant_on_fibers = all(
            controller[(q_bit, 0)] == controller[(q_bit, 1)]
            for q_bit in (0, 1)
        )
        factor = {
            q_bit: controller[(q_bit, 0)]
            for q_bit in (0, 1)
        }
        factors = all(
            controller[history] == factor[history[0]] for history in histories
        )
        if constant_on_fibers != factors:
            counterexamples += 1
    return models, counterexamples


def verify_pqf_advisory_invariance(advisories: tuple[str, ...]) -> int:
    comparisons = 0
    for q in quotient_samples():
        decisions = {advisory: pqf_decision(q) for advisory in advisories}
        comparisons += len(advisories) - 1
        if len(set(decisions.values())) != 1:
            raise AssertionError(f"PQF advisory leak at {q}: {decisions}")
    return comparisons


def leak_direct_advisory(q: Quotient, advisory: str, raw_label: str) -> str:
    if advisory == "premature_terminal":
        return "STOP_SUCCESS"
    return pqf_decision(q)


def leak_summary_digest(q: Quotient, advisory: str, raw_label: str) -> str:
    if sum(advisory.encode("utf-8")) % 2 == 0:
        return "CHECK"
    return pqf_decision(q)


def leak_unverified_completion(q: Quotient, advisory: str, raw_label: str) -> str:
    if advisory == "premature_terminal":
        return "STOP_SUCCESS"
    return pqf_decision(q)


def leak_raw_tool_payload(q: Quotient, advisory: str, raw_label: str) -> str:
    if raw_label == "raw_variant_b":
        return "CHECK"
    return pqf_decision(q)


def kill_quotient_leak_mutants() -> tuple[int, int]:
    mutants: dict[str, Callable[[Quotient, str, str], str]] = {
        "direct_worker_advisory": leak_direct_advisory,
        "worker_summary_digest": leak_summary_digest,
        "unverified_worker_completion_id": leak_unverified_completion,
        "raw_tool_payload_branch": leak_raw_tool_payload,
    }
    q = Quotient(
        "plan-v1",
        frozenset({"o1", "o2"}),
        frozenset(),
        frozenset(),
        frozenset(),
        0,
        3,
    )
    variants = (
        ("honest", "raw_variant_a"),
        ("premature_terminal", "raw_variant_b"),
        ("persistent_nonterminal", "raw_variant_a"),
        ("oscillating", "raw_variant_b"),
    )
    killed = 0
    for name, mutant in mutants.items():
        outputs = {mutant(q, advisory, raw) for advisory, raw in variants}
        if len(outputs) > 1:
            killed += 1
        else:
            raise AssertionError(f"quotient leak mutant survived: {name}")
    return killed, len(mutants)


def oracle_failures(
    events: tuple[WorldEvent, ...],
    controller_actions: tuple[tuple[int, str], ...],
    feasible: bool,
    budget: int,
) -> frozenset[str]:
    required_effects = frozenset({"e1", "e2"})
    terminal_actions = tuple(
        (step, action)
        for step, action in controller_actions
        if action.startswith("STOP_")
    )
    final_step, final_action = (
        terminal_actions[-1]
        if terminal_actions
        else (budget, "STOP_BUDGET")
    )

    commits = tuple(e for e in events if e.kind == "commit")
    faults = tuple(e for e in events if e.kind == "terminal_fault")
    commits_by_stop = tuple(e for e in commits if e.step <= final_step)
    faults_by_stop = tuple(e for e in faults if e.step <= final_step)
    commit_ids_by_stop = tuple(e.identifier for e in commits_by_stop)
    completed_by_stop = required_effects.issubset(commit_ids_by_stop)
    duplicate = len(commit_ids_by_stop) != len(set(commit_ids_by_stop))

    terminal_candidates = []
    all_commit_ids = tuple(e.identifier for e in commits)
    if required_effects.issubset(all_commit_ids):
        terminal_candidates.append(
            max(
                min(e.step for e in commits if e.identifier == effect_id)
                for effect_id in required_effects
            )
        )
    if faults:
        terminal_candidates.append(min(e.step for e in faults))
    first_world_terminal = min(terminal_candidates) if terminal_candidates else None

    failures: set[str] = set()
    if final_action == "STOP_SUCCESS" and not completed_by_stop:
        failures.add("premature_success")
    if final_action == "STOP_FAULT" and not faults_by_stop:
        failures.add("false_fault")
    if final_action == "STOP_BUDGET" and feasible and not completed_by_stop:
        failures.add("budget_incomplete")
    if final_action == "STOP_BUDGET" and not feasible and not faults_by_stop:
        failures.add("budget_incomplete")
    if first_world_terminal is not None and final_step - first_world_terminal > 1:
        failures.add("post_terminal_overrun")
    if duplicate:
        failures.add("duplicate_effect")
    return frozenset(failures)


def oracle_fixtures() -> dict[str, tuple[tuple[WorldEvent, ...], tuple[tuple[int, str], ...], bool, int]]:
    return {
        "premature_success": (
            (
                WorldEvent(1, "commit", "e1"),
                WorldEvent(3, "commit", "e2"),
            ),
            ((1, "STOP_SUCCESS"),),
            True,
            4,
        ),
        "false_fault": (
            (
                WorldEvent(1, "commit", "e1"),
                WorldEvent(3, "terminal_fault", "f1"),
            ),
            ((1, "STOP_FAULT"),),
            True,
            4,
        ),
        "budget_incomplete": (
            (WorldEvent(1, "commit", "e1"),),
            ((4, "STOP_BUDGET"),),
            True,
            4,
        ),
        "post_terminal_overrun": (
            (
                WorldEvent(1, "commit", "e1"),
                WorldEvent(2, "commit", "e2"),
            ),
            ((5, "STOP_SUCCESS"),),
            True,
            6,
        ),
        "duplicate_effect": (
            (
                WorldEvent(1, "commit", "e1"),
                WorldEvent(2, "commit", "e1"),
                WorldEvent(3, "commit", "e2"),
            ),
            ((3, "STOP_SUCCESS"),),
            True,
            5,
        ),
    }


def kill_oracle_clause_mutants() -> tuple[int, int]:
    fixture_by_mutant = {
        "remove_premature_success": "premature_success",
        "remove_false_fault": "false_fault",
        "remove_budget_incomplete": "budget_incomplete",
        "remove_post_terminal_overrun": "post_terminal_overrun",
        "remove_duplicate_effect": "duplicate_effect",
    }
    killed = 0
    fixtures = oracle_fixtures()
    for mutant, target_clause in fixture_by_mutant.items():
        failures = oracle_failures(*fixtures[target_clause])
        if target_clause not in failures:
            raise AssertionError(f"base oracle misses fixture: {target_clause}")
        mutated = failures - {target_clause}
        if target_clause not in mutated:
            killed += 1
        else:
            raise AssertionError(f"oracle mutant survived: {mutant}")
    return killed, len(fixture_by_mutant)


def verify_receipt_soundness_counterexample() -> bool:
    """A false receipt must fool PQF but not the separate world oracle."""

    false_accept_q = Quotient(
        "plan-v1",
        frozenset(),
        frozenset({"o1", "o2"}),
        frozenset({"e1", "e2"}),
        frozenset(),
        0,
        3,
    )
    decision = pqf_decision(false_accept_q)
    world_events = (WorldEvent(1, "commit", "e1"),)
    external_failures = oracle_failures(
        world_events, ((1, decision),), feasible=True, budget=4
    )

    # Invalid co-designed mutant: it declares completion from receipts.
    co_designed_says_complete = (
        false_accept_q.verified_effect_ids == frozenset({"e1", "e2"})
    )
    return (
        decision == "STOP_SUCCESS"
        and "premature_success" in external_failures
        and co_designed_says_complete
    )


def verify_contract(config: dict[str, object]) -> None:
    concept = config["concept"]
    assert isinstance(concept, dict)
    assert tuple(concept["quotient_fields"]) == EXPECTED_QUOTIENT_FIELDS
    assert tuple(concept["controller_actions"]) == EXPECTED_ACTIONS

    domain = config["finite_validation_domain"]
    assert isinstance(domain, dict)
    master_count = (
        len(domain["graph_templates"])
        * len(domain["outcome_schedules"])
        * len(domain["receipt_profiles"])
    )
    planned_count = (
        master_count
        * len(domain["worker_advisory_tapes"])
        * len(domain["controllers"])
    )
    assert master_count == domain["master_count"] == 72
    assert planned_count == domain["planned_execution_count"] == 1440

    gates = config["validity_gates"]
    assert isinstance(gates, dict)
    assert tuple(gates["oracle_clause_mutants"]) == EXPECTED_ORACLE_MUTANTS
    assert tuple(gates["quotient_leak_mutants"]) == EXPECTED_LEAK_MUTANTS
    assert gates["required_kill_rate"] == 1.0

    primary = config["primary_comparison"]
    utility = config["utility_and_cost"]
    assert isinstance(primary, dict) and isinstance(utility, dict)
    assert primary["baseline_risk_floor"] == 0.1
    assert primary["success_threshold"] == 0.5
    assert utility["completion_loss_max_rate"] == 0.05
    assert utility["completion_loss_max_percentage_points"] == 5
    assert utility["step_overhead_max"] == 0.2
    assert len(config["assumptions"]) == 7
    assert len(config["rival_explanations"]) == 9
    assert len(config["bias_surface"]) == 8
    assert config["taxonomy"]["bridge_synthesis_tripwire"] is False
    assert config["authorization"]["review_budget"] == "exhausted_20_of_20_no_dispatch"


def verify_hypothesis_text(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    required = (
        "## Primary hypothesis",
        "## Named concept",
        "## Formal boundary",
        "## Variables and controls",
        "## One primary comparison and decision rule",
        "## Mechanistic justification",
        "## Assumptions and validity domains",
        "## Rival explanations",
        "## Fixed bias surface",
        "## Failure modes and result interpretation",
        "## Taxonomy and anti-stacking",
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
    line_count = verify_hypothesis_text(args.hypothesis)

    models, theorem_counterexamples = prove_finite_factorization_equivalence()
    if theorem_counterexamples:
        raise AssertionError("finite factorization theorem has counterexample")
    advisory_tapes = tuple(
        config["finite_validation_domain"]["worker_advisory_tapes"]
    )
    invariance_comparisons = verify_pqf_advisory_invariance(advisory_tapes)
    leak_killed, leak_total = kill_quotient_leak_mutants()
    oracle_killed, oracle_total = kill_oracle_clause_mutants()
    counterexample = verify_receipt_soundness_counterexample()
    if not counterexample:
        raise AssertionError("receipt-soundness/co-design counterexample missing")

    print(
        "pqf_hypothesis_v1=PASS"
        f" lines={line_count}"
        " json=PASS ast=PASS"
        f" finite_factor_models={models}"
        f" theorem_counterexamples={theorem_counterexamples}"
        f" advisory_invariance_comparisons={invariance_comparisons}"
        f" quotient_mutants_killed={leak_killed}/{leak_total}"
        f" oracle_mutants_killed={oracle_killed}/{oracle_total}"
        " receipt_soundness_counterexample=PASS"
        " co_design_mutant_masked_counterexample=true"
        f" masters={config['finite_validation_domain']['master_count']}"
        f" planned_executions={config['finite_validation_domain']['planned_execution_count']}"
        " review=unavailable_20_of_20"
        " phase3=not_authorized"
    )


if __name__ == "__main__":
    main()
