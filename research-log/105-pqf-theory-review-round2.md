# PQF theory review round 2 — final verdict

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6  
**Task:** T040 · **Status:** NEEDS_REVISION  
**Reviewer-reported hypothesis line count:** 611  
**Git-committed hypothesis line count:** 611  
**Line-count check:** PASS  
**Cumulative hypothesis-review budget:** 23/30

The fresh reviewer read the immutable v2 hypothesis, normative configuration,
the two complete canonical SciAgent references, and all ten previous issues.
The report is preserved verbatim below.

---

## Verbatim reviewer report

## Status: DONE

Hypothesis file line count: **611 lines**. This matches both the working tree and `git show HEAD`.

## 1. Blind Assessment

### Previous-review issue disposition

| # | Status | Current v2 location and judgment |
|---|---|---|
| 1 | **RESOLVED** | Lines 112–154 and 308–369 now isolate one Boolean authority bit between matched visible controllers. The estimand is the finite-domain total effect of that gate, not receipt verification or recovery. |
| 2 | **IMPROVED** | Lines 25–26, 28–30, and 579–584 honestly recast the study as a deterministic causal unit test. However, lines 43–53 and 248–255 incorrectly imply that the 0.10 baseline-risk floor is not constructed. Under the intended oracle semantics, the index-1 `STOP_SUCCESS`, index-1 `STOP_FAULT`, and index-2 `STOP_FAULT` substitutions alone force at least \(48/400=0.12\) authority-on failures. |
| 3 | **RESOLVED** | Lines 223–236 define schedules before assignment as pure functions of master, schedule, and index. They no longer depend on treatment-realized receipts or actions. The schedules are still control-referenced, but not post-treatment. |
| 4 | **IMPROVED** | Lines 257–283 define terminal no-ops, receipt priority, and stop behavior. Totality still fails at budget exhaustion: after eight charged actions, decision 9 derives `budget_exhausted` but looks up `u_9` before selecting `STOP_BUDGET`; only indices 1–8 are defined. Secondary dropout/no-recovery cells can reach this path. `CHECK` rescan payload and `stall_due` semantics are also unspecified. |
| 5 | **IMPROVED** | Lines 292–306 and 527 now name six clauses and require six mutants. But the contract contains only the Boolean assertion `unique_fixture_per_clause: true`; it does not specify the six fixture traces and expected labels. Author-side mutation assertions are not independent validation. |
| 6 | **RESOLVED** | Lines 342–369 and 488–502 provide one coherent joint rule. Secondary results neither rescue nor disconfirm it. |
| 7 | **RESOLVED** | Lines 89–106 explicitly withdraw minimality and call `z` a chosen projection. |
| 8 | **UNCHANGED** | Lines 534–558 substitute first-disagreement mediation for the former invariance prediction, but a receipt-plus-cap controller with the same gated override predicts exactly the same mediation. Declaring that any comparator with the gate has “adopted the move” is circular, not a distinguishing prediction. |
| 9 | **RESOLVED** | The raw full-state comparator was removed, and the contract requires every valid `z` state crossed with every advisory value. |
| 10 | **RESOLVED** | Lines 68–71 explicitly withdraw delay/dropout monotonicity. |

### Justification Correctness: NEEDS_REVISION

The isolated controller contrast is causally clean within its stipulated finite population. Proposition 2 is correct by exhaustive case split, and Proposition 3 follows by induction under deterministic transitions.

The primary empirical result, however, is largely built into the schedule construction:

- At decision 1, every master is incomplete and fault-free. Replacing the clean action with `STOP_SUCCESS` or `STOP_FAULT` therefore creates two authority-on failures per master.
- At decision 2, the clean decision-1 action was `CONTINUE`, and no terminal fault can yet have occurred under the named third-attempt fault schedule. `STOP_FAULT` creates another failure per master under the intended meaning of `false_fault`.
- Those three schedules yield \(3/25=0.12\) failure per master, already exceeding the 0.10 eligibility floor.
- The clean advice is copied from the canonical authority-off action. By Proposition 3, clean authority-on and authority-off traces must therefore be identical. Both completion loss and step overhead are exactly zero by construction, so the 5-point and 20% guardrails are not empirical risks.

Why call these “materiality requirements” if the protocol entails them? The census can detect implementation defects, but it does not provide meaningful confirmatory evidence for the advertised thresholds.

The evidence chain is appropriately narrowed to motivation. The cited arXiv preprints support termination poisoning, effective bounds, runtime mediation, trace enforcement, extractor sensitivity, and deterministic verification. None independently establishes PQF’s effect size, schedule population, oracle validity, or transfer; no replication evidence is given.

The fixed bias surface lists all eight required categories. Confounding, assignment, missing-data, analysis-flexibility, and reporting controls are adequate for the finite crossover. Selection and measurement controls remain substantively weak: exhaustiveness inside an author-constructed schedule frame does not validate that frame, and mutation sensitivity does not establish oracle correctness.

### Mathematical Depth & Validity Domains: NEEDS_REVISION

Unpacked:

- `z` partitions histories into equivalence classes with the same four verifier predicates.
- Proposition 1 says an action policy factors through those classes exactly when it is constant within each class. This theorem is correct.
- `D(z,u)` is the support of the Boolean override: away from budget exhaustion, authority matters exactly when non-abstaining advice differs from the base action.
- Proposition 3 lifts that decision-local identity to matched prefixes through determinism.

Propositions 2–3 carry the narrow implementation-conformance argument. Proposition 1 is now largely vestigial: since `K` is defined syntactically as a function of `z`, factorization is already true by construction. It must not be presented as evidence for termination integrity or effect magnitude.

Missing validity domains or definitions include:

- advisory behavior beyond index 8;
- exact graph edges, obligation/effect mappings, and complete world-transition tapes;
- the `stall_due` predicate and `CHECK` rescan payload;
- rejected, duplicated, or stale receipt transition rules;
- whether `false_fault` fires when no terminal fault ever exists;
- the six concrete oracle fixture traces and expected labels;
- which outcome clauses are reachable in the primary population.

The formulas are elementary and mostly bound to concrete meanings. The defect is not algebraic error but using definitional equalities around a nearly predetermined empirical claim.

### Logical Soundness: NEEDS_REVISION

The causal verb does not exceed the declared causal question: the claim is explicitly restricted to matched finite interventions.

The main logical contradiction is between lines 51–53/248–255 (“eligibility is not guaranteed”) and the early-stop substitutions that entail the risk floor under the intended oracle.

There is also an executability contradiction between:

- an eight-entry advisory schedule at lines 229–230 and 333;
- lookup before controller action at lines 261–264; and
- budget exhaustion becoming visible only at the next decision after the eighth decrement.

The contract additionally names graph and world templates without defining them or binding them to immutable specifications. Names such as `diamond_4` are not executable semantics.

### Assumption Completeness: NEEDS_REVISION

A1–A8 are well scoped, and receipt soundness is honestly identified as load-bearing.

Missing assumptions concern:

- total schedule semantics at and beyond the budget boundary;
- a canonical, immutable interpretation of every graph/world label;
- exact `stall_due` and rescan behavior in the 3,200 secondary cells;
- oracle specificity as well as mutant sensitivity;
- the representational meaning of equal weighting over positions and replacement values.

Violating A2, A4, A6, or transition totality invalidates the causal interpretation entirely. Violating A7 invalidates any interpretation beyond deterministic adversarial unit testing.

### Taxonomy Verification: MOSTLY VERIFIED

`Failure/Risk Gap × Robustification` accurately reflects the gap and intended contribution. This is not Bridge Opportunity × Synthesis/Unification, so the heightened Bridge tripwire does not apply.

The dominant operation is more naturally **decouple** than **replace**: the central contribution separates visibility from authority. This does not appear to be tripwire evasion because neither label triggers Bridge×Synthesis scrutiny.

### Anti-Stacking Check: FAIL

A plain composition containing:

1. a receipt-derived base policy,
2. a hard budget cap, and
3. a Boolean advisory override

predicts both zero effect when the override is disabled and first-disagreement mediation when it is enabled. Sparse location dependence is likewise a direct property of that multiplexer.

The argument that a comparator adopting the gate is “no longer plain” merely defines all matching alternatives as instances of PQF. It does not produce a prediction unavailable to a stack.

If treated instead as engineering, it also fails that route: there is no measured pre-build bottleneck per component and no per-component ablation plan for receipts, cap, recovery, and authority.

### Occam’s Razor Check: FAIL

The simplest hypothesis is:

> A controller that conditionally substitutes advice for its base action can differ from the base controller only at reachable advice/base disagreements; disabling substitution prevents those differences.

That statement predicts the structural findings without quotient terminology, 4,400 executions, or a six-clause aggregate. A truth table plus exhaustive transition-model check is enough to verify it.

If the intended contribution is empirical risk reduction, the simpler explanation is that early terminal substitutions are directly labeled failures while the matched base controller uses sound oracle-grade state.

### Alternative Explanations: INADEQUATELY CONTROLLED

The predicted result can arise because:

- the schedule population deliberately inserts terminal actions before completion/fault;
- clean utility equality is copied from the authority-off trajectory;
- the base policy and oracle share the same trusted plan/world semantics;
- equal weighting over action values and positions is an arbitrary design measure, not an observed advisory-error distribution;
- the result is implementation conformance to a Boolean gate rather than evidence of a newly discovered safety mechanism.

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. **Remove the predetermined confirmatory claim or reclassify it as formal conformance/model checking.** Lines 34–53, 225–255, 342–369, 488–532.
2. **Replace the anti-stacking prediction with a genuinely distinguishing one, or make a compliant engineering claim with measured bottlenecks and component ablations.** Lines 534–558.
3. **Make the contract total and self-contained:** define graph/world tapes, schedule values beyond index 8 or stop before lookup, `stall_due`, rescan events, and all receipt transitions. Hypothesis lines 212–283; contract lines 115–206.
4. **Specify independently checkable oracle evidence:** six concrete gold traces, exact expected clause vectors, negative cases, and unambiguous state-based definitions. Hypothesis lines 285–306, 419–430, 527; contract lines 208–239 and 273–289.
5. **Correct the false claim that the risk floor is not guaranteed and analytically derive all thresholds before execution.** Lines 43–53 and 248–255.
6. **Clarify which six clauses are reachable in the primary domain and avoid implying broad six-clause validation when some appear fixture-only.** Lines 292–324 and 515–529.

## 2. Actionable Coaching

- Choose one honest path:
  - **Verification path:** state Propositions 2–3 as the contribution and use exhaustive model checking only to validate an implementation.
  - **Empirical path:** derive advisory schedules from an independently justified error process, external trace corpus, or held-out generator not defined from the authority-off trajectory.
- Write the causal estimand explicitly as an average of paired potential outcomes over units `(master, schedule)`. This would clarify what is causal without adding decorative mathematics.
- Before running, analytically bound `F_on`, `F_off`, clean completion, and clean steps. Delete every threshold already entailed by construction.
- Replace ambiguous oracle prose with predicates such as: `false_fault := STOP_FAULT ∧ no_terminal_fault_observed_at_or_before_stop`.
- Put complete graph edges, transition tapes, receipt payloads, and expected terminal states directly in the normative contract or bind them by immutable paths and hashes.
- Validate the oracle with an independently authored reference model or exhaustive gold-labeled trace table. Mutants test clause sensitivity, not overall correctness.
- For anti-stacking, compare against the strongest receipt-plus-cap controller under the same trusted state. If no prediction separates PQF from that comparator, narrow novelty to an interface invariant or implementation verification result.
- Describe the cited literature as recent, unreplicated preprint motivation. It should not bear any causal or quantitative claim.

---

## Orchestrator disposition

The verdict is adverse and valid. The clean causal isolation, exogeneity,
decision rule and removal of minimality/monotonicity survive review. The v2
empirical claim does not: the risk floor and utility guardrails are entailed by
construction, the total transition contract is incomplete, and the proposed
anti-stacking prediction remains shared by a receipt-plus-cap stack.

PQF v2 remains immutable. No Phase-3 action is opened. The next task must change
the scientific claim or the intervention population, not patch prose around the
same fixed schedule.
