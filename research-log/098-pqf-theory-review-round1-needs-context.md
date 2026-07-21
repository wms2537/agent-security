# PQF theory review round 1 — NEEDS_CONTEXT / provisional NEEDS_REVISION

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6
**Task:** T038 · **Status:** reviewer context incomplete; adverse provisional assessment stands

**Reviewer-reported hypothesis line count:** 545  
**Git-committed hypothesis line count:** 545  
**Line-count check:** PASS  
**Budget after this dispatch:** 21/30

The reviewer could not locate the two canonical SciAgent references because they
live at `/home/soh/.codex/skills/sciagent/reference/` rather than inside the
research repository. It nevertheless completed a detailed provisional blind
assessment and returned `NEEDS_REVISION`. The full report is preserved verbatim
below before any context-completion dispatch or artifact revision.

---

## Verbatim reviewer report

## Status: NEEDS_CONTEXT

The hypothesis entry is complete and has **545 lines**. However, the two mandated reference files are absent from the repository, `/home/soh`, and git history:

- `reference/mathematical-thinking.md`
- `reference/idea-taxonomy.md`

The assessment below is therefore provisional, using the explicit standards in the task brief. Exact taxonomy adjudication cannot be completed against the missing canonical definitions.

## 1. Blind Assessment

### Justification Correctness: NEEDS_REVISION

The factorization proposition at lines 140–168 is correct: a map factors through \(q\) iff it is constant on \(q\)-fibers, with uniqueness correctly restricted to `image(q)`. It does not establish the systems claim, and the entry properly says so.

The empirical causal justification fails in more important ways:

1. **The primary contrast does not isolate the stated independent variable.** Lines 187–196 call the treatment the “termination observation boundary,” but lines 264–269 change the decision rule, receipt access, advisory arbitration, and recovery behavior simultaneously. `worker_self_judgment` directly maps advisory claims to stops; PQF uses verifier receipts, a different priority policy, and `CHECK`. The effect is identifiable only for the whole controller bundle, not for information minimization.

2. **The baseline risk and much of the headline effect are built into the fixtures.** Under lines 255–269, `premature_terminal` and `oscillating` emit `CLAIMS_SUCCESS` at the first nonterminal/odd decision, and worker self-judgment immediately emits `STOP_SUCCESS`. By failure clause 1 at lines 205–214, every such run fails. Those two tapes alone force \(F_\text{worker}\ge 0.5\), making the 0.10 eligibility gate vacuous. `persistent_nonterminal` and `adaptive_flip...` are likewise designed to keep the worker running. This is closer to a deterministic unit test of stipulated policies than evidence for the proposed causal mechanism.

3. **The supposedly matched advisory is post-treatment in one condition.** Lines 223–230 say the advisory tape is fixed across controllers, but lines 260–261 define `adaptive_flip_after_first_verified_transition` using the first accepted receipt. Receipt acceptance can change after treatment because PQF invokes `CHECK`, while worker controllers do not. The realized advisory sequence is therefore controller-dependent.

4. **The full-state comparator does not resolve the confound.** Giving a controller extra fields does not cause it to use them. The comparator is explicitly programmed to honor advisory claims before the PQF fallback (lines 264–269), so its sensitivity is a policy construction, not evidence that merely exposing content causes failure.

5. **The state machine is undefined after a world-terminal event.** Lines 271–276 say `CONTINUE` consumes the next canonical world transition, but terminal-fault and completed schedules have no next transition. Receipt-delay cases can make PQF continue after world completion. Whether this is a no-op, an invalid transition, a charged controller step, or an absent event determines failure clause 5 and step overhead.

6. **Six outcome clauses have only five clause mutants.** Lines 205–214 define six distinct failure clauses, whereas lines 422 and 483 require only five oracle mutants. The config likewise contains only one `remove_budget_incomplete` mutant for the two distinct feasible/infeasible budget clauses. Oracle sensitivity is therefore not established clause by clause.

The cited papers accurately motivate termination poisoning, loop bounds, runtime enforcement, extractor noise, and deterministic verification at the abstract level. They do not supply evidence for PQF’s effect, perfect receipt soundness, quotient sufficiency, or the chosen thresholds. No replication evidence is cited; all six references are arXiv preprints.

### Mathematical Depth & Validity Domains: NEEDS_REVISION

The structural proposition is valid but elementary and largely restates the implementation signature. It carries only the invariance claim, not safety or utility.

The word **minimal** is unjustified at lines 330 and 365. The seven-field \(q\) is not the coarsest abstraction sufficient for the fixed controller:

- `plan_digest` is not consulted by the displayed policy.
- `open_obligation_ids` is derivable from the trusted plan and completed obligations under A1.
- Exact obligation/effect sets are finer than the Boolean predicates the policy actually branches on.
- Many distinct values of \(q\) map to the same action.

Structurally, \(q\) induces a finer partition of history space than the action-equivalence partition induced by `kappa`. Thus the entry has shown a quotient, not a minimal quotient. Calling it minimal without a necessity proof or field ablation is a mathematical defect.

The receipt-stress ordering at lines 70–73 also lacks a validity regime. “Delay every receipt by one decision” and “drop one receipt until a check” are not nested perturbations; either can cost more depending on graph location and check timing. Receipt sufficiency does not imply the asserted monotone gradient.

The following validity domains remain unspecified:

- exact delivery/indexing semantics at world completion or fault;
- whether cross-tape equal-\(q\) pairs are guaranteed to exist rather than making invariance vacuous;
- how much information obligation identifiers and timing counters leak;
- whether worker-influenced action proposals can change verifier state and hence carry content influence through \(q\);
- what “raw abstract observation label” means—the field is included in the full-state comparator but has no alphabet, generation rule, or policy use.

### Logical Soundness: NEEDS_REVISION

There is a contradiction in the decision rule:

- Lines 42–48 and 300–318 make support depend only on the PQF/worker primary thresholds and validity gates.
- Lines 448–453 say a full-state controller matching PQF is a conclusive disconfirmation.
- Lines 508–510 say the same result merely leaves the information-boundary mechanism without discriminating evidence.
- A hard-cap match is also said to remove demonstrated value at lines 65–69, but it is not a support gate.

The outcome classification is therefore not uniquely preregistered and permits incompatible interpretations after results.

The proposition “removes that path” only at fixed \(q\) (lines 324–327). It does not remove content influence mediated through worker-selected actions, actual effects, receipt timing, or verifier state. The execution model omits those channels, so the broader causal wording is stronger than the modeled mechanism.

### Assumption Completeness: NEEDS_REVISION

A1–A7 are unusually explicit and have bounded domains, but important load-bearing assumptions are missing or false:

- advisory realizations are exogenous to controller assignment;
- every controller action has defined semantics after completion/fault;
- the hand-authored advisory policies are a meaningful intervention population rather than guaranteed-error fixtures;
- equal-\(q\) counterfactual pairs cover the relevant reachable states;
- separate code/import boundaries make the oracle construct-independent, rather than merely implementation-independent;
- every outcome clause is independently testable.

A1–A5 are so strong that the positive result is conditional on a perfect plan, authoritative state, sound receipt acceptance, sufficient budget, and correct oracle. That scope is allowed, but the study must not imply robustness to verifier error from one deliberately failing negative control.

### Taxonomy Verification: NEEDS_CONTEXT / PROVISIONALLY PLAUSIBLE

Against the brief’s definitions, `Failure/Risk Gap × Extrapolation/Robustification` with `replace`/`decouple` is plausible at the concept level. The intervention does target a known termination-poisoning risk by replacing worker authority.

However, the measured endpoint depends on a composition of trusted planning, receipt verification, identifier projection, `CHECK`, budgets, and a separate oracle. The entry has not shown that the end-to-end gain belongs specifically to the local replace/decouple move. The missing canonical taxonomy file prevents a definitive ruling on whether this must instead be treated as engineering synthesis.

### Anti-Stacking Check: FAIL

The prediction at lines 501–506 is not genuinely distinguishing.

A plain composition of a receipt checker, hard cap, and termination policy that branches only on verified receipt state is quotient-factored and predicts the same fixed-\(q\) invariance. Exact invariance follows by construction from forbidding advisory inputs; it is an implementation conformance property, not a prediction unavailable to the stacked version.

The full-state comparator’s variation is likewise programmed into its priority rule. A full-state controller may simply ignore its extra fields and be invariant. The entry acknowledges this at lines 508–510, which concedes that the proposed prediction does not distinguish architecture from use policy.

### Occam’s Razor Check: FAIL

A simpler controller predicts the same result:

```text
STOP_FAULT if verified_fault
STOP_SUCCESS if verified_complete
STOP_BUDGET if budget exhausted
otherwise CONTINUE
```

Add one stall/check bit only if dropout recovery is separately demonstrated as necessary. The fixed policy does not require seven exposed fields, and the primary benchmark does not separate receipt verification, content blindness, checking, and policy priority. This simpler formulation and its component ablations should be tested first.

### Alternative Explanations: INADEQUATELY CONTROLLED

The observed outcome could arise because:

- two advisory tapes force the baseline to stop incorrectly at decision one;
- PQF receives authoritative state while the worker baseline does not;
- PQF uses a different arbitration policy;
- `CHECK`, rather than content blindness, recovers progress;
- the task grammar and independent oracle are both authored from the same trusted plan, even without code reuse;
- the adaptive advisory changes downstream of controller behavior;
- the quotient is sufficient only because the canonical action tape removes the worker’s action-selection problem.

Several appear in the rival list, but the current controls expose rather than eliminate them.

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. **Identify the causal estimand and isolate it** — lines 187–196, 264–269, 320–341. Either rename the treatment as the entire controller bundle or introduce a design that holds receipts, recovery, and arbitration fixed while varying advisory visibility/use.
2. **Remove the guaranteed-failure baseline construction or narrow the claim to a unit-test theorem** — lines 239–269 and 289–314. The current tapes force the baseline-risk floor and largely preordain the result.
3. **Make advisory assignment exogenous** — lines 223–230 and 260–261. Precompute the adaptive sequence from an exogenous canonical schedule or explicitly model it as a sequential adversary rather than a fixed matched tape.
4. **Fully specify terminal and receipt timing semantics** — lines 271–280 and 462–471. Define every `CONTINUE`/`CHECK` transition after completion or fault and the exact indexing of delayed receipts and grace periods.
5. **Repair the oracle test mismatch** — lines 205–214, 422, and 483. Provide six independently killable clause mutants and fixtures in which each clause is uniquely decisive.
6. **Resolve the preregistered-decision contradiction** — lines 42–48, 65–69, 448–453, and 508–510. State exactly whether hard-cap/full-state equality invalidates support, disconfirms the joint claim, or only weakens mechanism attribution.
7. **Withdraw or prove minimality** — lines 330 and 365. Show field necessity/coarsest sufficient partition, or call \(q\) a chosen verifier-owned projection.
8. **Replace the anti-stacking prediction** — lines 492–510. Current invariance is equally predicted by a receipt-plus-cap composition.
9. **Define the floating full-state input and non-vacuous pair coverage** — lines 57–64 and 193–195. Specify raw-label semantics and generate crossed advisory counterfactuals at each reachable quotient.
10. **Justify or drop the receipt-stress gradient** — lines 70–73. The profiles need a pointwise information-ordering/coupling before monotonicity follows.

## 2. Actionable Coaching

- Use a factorial ablation: receipts absent/present × advisory branch absent/present × `CHECK` absent/present, all under the same budget and world tape. Make the primary claim the system-bundle effect if a pure visibility effect cannot be identified.
- Replace always-wrong tapes with preregistered error-rate and duration regimes, including benign noisy advisories. Report a response surface over false-success, false-fault, and false-nonterminal rates.
- For the deterministic finite domain, derive expected outcomes from a complete transition table before execution. Treat runtime execution as implementation validation of that derivation, not as independent empirical confirmation.
- Define an explicit sequential causal graph: controller assignment → action/check → receipt availability → quotient/advisory → next action. This will reveal which variables are confounders, mediators, or post-treatment outcomes.
- If minimality matters, compare the seven-field projection with a coarser predicate state and field-removal mutants. A field is necessary only if merging histories that differ solely in that field forces different correct actions.
- Add false-positive receipt rates to the main robustness surface, not merely one negative control. False positives are the asymmetric load-bearing failure mode.
- Either embrace an engineering-composition claim and provide measured per-component bottlenecks/ablations, or make a genuinely local claim about information-flow restriction without attributing the whole end-to-end result to it.
- Keep the literature claims at “motivation.” The current sources do not establish the defense mechanism, effect size, or real-world receipt assumptions.

---

## Orchestrator disposition

The `NEEDS_CONTEXT` status is valid: the missing canonical paths were not supplied
by the literal template. The provisional adverse issues are also valid and may
not be discarded. A context-completion dispatch may only finalize taxonomy and
the blind status; it cannot erase these issues without a revised hypothesis.

No Phase-3 advance is permitted.
