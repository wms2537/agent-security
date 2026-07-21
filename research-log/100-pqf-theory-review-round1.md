# PQF theory review round 1 — final context-complete verdict

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6
**Task:** T038 · **Status:** NEEDS_REVISION

**Reviewer-reported hypothesis line count:** 545  
**Git-committed hypothesis line count:** 545  
**Line-count check:** PASS  
**Cumulative hypothesis-review budget:** 22/30

The same reviewer read both canonical SciAgent references completely and
finalized the blind verdict. The report is preserved verbatim below.

---

## Verbatim reviewer report

## Status: DONE

Hypothesis file line count: **545 lines**.

Both canonical reference files were read completely.

# 1. Blind Assessment

## Justification Correctness: NEEDS_REVISION

The structural proposition at lines 140–168 is correct. Re-derivation:

1. \(q\) partitions histories into fibers containing histories with identical verifier-owned ledger state.
2. If \(c\) is constant on each fiber, define \(\kappa(z)\) as the common action for any history mapped to \(z\).
3. Fiber constancy makes this definition well-defined.
4. Since \(Q=\operatorname{image}(q)\), every \(z\in Q\) has a preimage, and \(c=\kappa\circ q\).
5. Any second factor map must agree on every reachable \(z\), proving uniqueness on \(Q\).
6. Conversely, \(c=\kappa\circ q\) immediately makes equal-\(q\) histories receive equal actions.

Finiteness of \(H\) is unnecessary, but harmless. The proposition carries the narrow information-flow argument and is not decorative math. It does not establish receipt soundness, quotient sufficiency, or system safety, which the entry correctly acknowledges.

The empirical causal justification nevertheless fails:

- **The treatment bundles multiple causes.** Lines 187–196 call the independent variable the observation boundary, but lines 264–269 simultaneously change receipt access, advisory arbitration, priority policy, and availability of `CHECK`. The design can identify the effect of replacing one whole controller with another, not the causal effect of information minimization.
- **Baseline failure is constructed into the test.** Under lines 255–269, `premature_terminal` and first-decision `oscillating` force worker self-judgment to issue `STOP_SUCCESS` before any required effect. Failure clause 1 then fires for every such master. These two tapes alone force \(F_\text{worker}\ge 0.5\), making the 0.10 baseline-risk gate vacuous.
- **One “fixed” advisory is post-treatment.** Lines 223–230 claim tapes are held fixed, but `adaptive_flip_after_first_verified_transition` at lines 260–261 depends on accepted receipts. Receipt acceptance can change because PQF invokes `CHECK`. Thus realized advisory labels are downstream of controller assignment.
- **The full-state comparator is policy-confounded.** It is programmed to honor advisory claims before its PQF fallback. Its failure demonstrates the chosen arbitration rule, not that exposure to extra information itself causes failure.
- **Transition semantics are incomplete.** Lines 271–276 do not define what `CONTINUE` does when completion or terminal fault leaves no next canonical world transition. This directly affects post-terminal-overrun failures and cost.
- **Oracle mutation coverage is incomplete.** Six failure clauses appear at lines 205–214, but only five clause mutants are required at lines 422 and 483. The feasible-incomplete-budget and infeasible-without-fault clauses are not independently tested.

The fixed bias surface does contain all eight required categories, one line each. Formal completeness passes, but several controls do not work substantively: the complete cross-product cannot repair construct selection that guarantees baseline errors; the adaptive tape violates matching; and the five-mutant oracle does not cover six clauses.

The cited evidence chain is accurately scoped as motivation. The papers support the existence of termination poisoning, loop risks, runtime enforcement, extractor noise, and deterministic verification. They do not support PQF’s effect size, perfect receipt soundness, or quotient sufficiency. No independent replication is cited.

## Mathematical Depth & Validity Domains: NEEDS_REVISION

The factorization has a sound structural interpretation: \(q\) collapses raw histories into equivalence classes of verifier-visible progress, and \(\kappa\) acts on those classes. The notation is concrete and unpacked.

However, the claims of a **“minimum”** or **“minimal”** quotient at lines 330 and 365 are false or at least unproved. The displayed policy does not use all seven fields at their stated resolution:

- `plan_digest` does not appear in any branch predicate.
- `open_obligation_ids` may be derivable from the trusted plan and completed IDs.
- Exact obligation/effect sets are finer than the completion predicate used by the controller.
- Many distinct quotient values necessarily map to the same action.

Geometrically, \(q\) induces a finer partition of history space than the fixed controller’s action partition. It is a chosen projection, not a demonstrated coarsest sufficient projection.

The receipt-stress gradient at lines 70–73 also lacks a valid ordering argument. Delaying every receipt and withholding one receipt until `CHECK` are not nested perturbations. Either may be more expensive depending on graph position and timing. Receipt sufficiency does not imply the claimed monotonicity.

Missing validity regimes include:

- exact receipt-delivery and grace-period indexing;
- semantics after world completion/fault;
- guaranteed non-vacuous coverage of equal-\(q\) cross-advisory pairs;
- information leakage through identifier choice and timing counters;
- content influence mediated through worker-selected actions and verifier state;
- semantics of the floating `raw_abstract_observation_label`.

## Logical Soundness: NEEDS_REVISION

The preregistered decision rule is inconsistent:

- Lines 42–48 and 300–318 define support using only the primary PQF/worker thresholds and validity gates.
- Lines 448–453 call a full-state match a conclusive disconfirmation.
- Lines 508–510 say it merely leaves the mechanism without discriminating evidence.
- Lines 65–69 say a hard-cap match removes demonstrated value, but hard-cap performance is not a primary support gate.

These alternatives permit incompatible post-result interpretations.

The causal chain also proves less than its prose suggests. Factorization eliminates advisory variation only conditional on fixed \(q\). It does not eliminate content influence through action selection, real effects, receipt timing, or verifier state. Those paths are mostly removed from the finite model rather than controlled experimentally.

The causal verb itself does not exceed the declared causal question because the headline is explicitly restricted to fixed interventions. The defect is that the intervention is mislabeled as an observation-boundary effect rather than a controller-bundle effect.

## Assumption Completeness: NEEDS_REVISION

A1–A7 have unusually clear scope boundaries, but several load-bearing assumptions are absent:

- advisory realization is exogenous to controller assignment;
- all actions have defined semantics after a world-terminal event;
- hand-authored tapes form a meaningful intervention population rather than guaranteed-error fixtures;
- every relevant quotient state is crossed with every advisory value;
- implementation independence makes the oracle construct-independent;
- each outcome clause has a uniquely decisive validation fixture;
- the full-state comparator is a defensible model of content-aware control.

A1–A5 also make the positive claim conditional on a complete trusted plan, authoritative state, sound receipts, adequate budget, and correct oracle. That is acceptable for the finite claim, but the negative control only demonstrates dependence on receipt soundness; it does not establish robustness to receipt errors.

## Taxonomy Verification: VERIFIED WITH LABEL NORMALIZATION

The canonical classification is:

- **Opportunity pattern:** Failure/Risk Gap
- **Method paradigm:** Robustification
- **Dominant operation:** `replace`
- **Secondary operation:** `decouple`
- **Secondary paradigm:** Artifact/System

The entry’s `Extrapolation/Robustification` wording should be normalized to the canonical `Robustification` label, but its substance is accurate. PQF addresses a specific termination-integrity risk by replacing worker-controlled termination with verifier-grounded control and decoupling progress authority from worker content.

It is not Bridge Opportunity × Synthesis/Unification, and its dominant operation is not integrate/unify/merge. The formal Bridge×Synthesis local-move tripwire therefore does not apply. This is not a relabeling designed to evade the tripwire.

## Anti-Stacking Check: FAIL

The distinguishing prediction at lines 501–506 is not exclusive to PQF.

A plain composition of a receipt checker, hard cap, and termination policy that branches only on verified receipt state is quotient-factored and predicts identical fixed-\(q\) advisory invariance. That invariance follows from the input contract; it is implementation conformance, not a prediction unavailable to the stacked alternative.

Likewise, the full-state comparator’s variation is programmed into its policy. A controller can receive additional inputs and ignore them. Lines 508–510 effectively concede this.

Thus the reframing/robustification anti-stacking requirement is not met even though the taxonomy itself is correctly non-Bridge/non-Synthesis.

## Occam’s Razor Check: FAIL

A simpler hypothesis predicts the same primary result:

```text
STOP_FAULT if verified fault
STOP_SUCCESS if verified complete
STOP_BUDGET if budget exhausted
otherwise CONTINUE
```

A stall/check predicate can be added only if an ablation shows it is necessary. The current benchmark does not establish why the controller must receive seven fields rather than a few verifier-owned predicates, or which benefit comes from receipts, content blindness, policy priority, and `CHECK`.

## Alternative Explanations: INADEQUATELY CONTROLLED

The predicted result could arise because:

- two advisory tapes guarantee immediate worker failure;
- PQF receives authoritative state while the worker does not;
- the policies use different arbitration priorities;
- `CHECK`, rather than content blindness, recovers progress;
- the task grammar and oracle are both derived from the same trusted plan;
- the adaptive advisory changes downstream of controller behavior;
- canonical action tapes remove the worker action-selection channel;
- the finite grammar is deliberately friendly to identifier-only completion.

The rival-explanations section names several of these, but the comparators do not separate them causally.

## Overall: NEEDS_REVISION

The core idea is salvageable, so `FUNDAMENTALLY_FLAWED` would be too strong. The present design cannot receive `RIGOROUS` because its causal mechanism is not identified and its anti-stacking prediction fails.

Required revisions, ordered by severity:

1. **Correct or isolate the causal estimand** — lines 187–196, 264–269, 320–341.
2. **Remove the guaranteed-failure baseline construction or explicitly recast the study as deterministic adversarial unit testing** — lines 239–269, 289–314.
3. **Make advisory assignment exogenous** — lines 223–230, 260–261.
4. **Define all terminal, receipt, and no-next-event transition semantics** — lines 271–280, 462–471.
5. **Add independent validation for all six outcome clauses** — lines 205–214, 422, 483.
6. **Resolve the contradictory support/disconfirmation rules** — lines 42–48, 65–69, 448–453, 508–510.
7. **Withdraw or prove quotient minimality** — lines 330, 365.
8. **Replace the anti-stacking prediction with one a receipt-plus-cap composition does not share** — lines 492–510.
9. **Define the raw full-state label and construct non-vacuous crossed quotient/advisory tests** — lines 57–64, 193–195.
10. **Justify or remove the receipt-stress monotonicity claim** — lines 70–73.

# 2. Actionable Coaching

- Use a factorial ablation: receipt access absent/present × advisory branch absent/present × `CHECK` absent/present, all under the same budget and arbitration structure.
- If visibility cannot be varied without changing policy, claim the causal effect of the complete controller bundle and make information minimization a secondary mechanism hypothesis.
- Precompute adaptive advisory sequences from an exogenous canonical schedule, or model them explicitly as sequential adversary policies rather than fixed tapes.
- Replace always-wrong tapes with preregistered advisory-error regimes spanning false-success, false-fault, and false-nonterminal rates. Include benign noisy advisories.
- Because the system is finite and deterministic, derive outcomes from a complete transition table first. Use execution to validate implementation against that derivation.
- Prove minimality through field-removal counterexamples or replace “minimal quotient” with “chosen verifier-owned projection.”
- Test a coarser predicate controller before the seven-field design.
- Add false-positive receipt rates to the robustness surface. A single negative control demonstrates brittleness but does not characterize its boundary.
- Make each oracle failure clause uniquely decisive in at least one fixture and give it its own mutant.
- Either identify a prediction not shared by a content-blind receipt-and-cap composition or present PQF honestly as an engineering composition with per-component bottlenecks and ablations.

---

## Orchestrator disposition

The verdict is adverse and valid. PQF v1 remains immutable. Phase 2 does not
pass. The next task is a structural v2 redesign at the owning phase, not a prose
patch and not a Phase-3 run.
