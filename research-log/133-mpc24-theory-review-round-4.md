# MPC-24 theory review round 4

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** completed — needs revision

## Context

The reviewer evaluated immutable `research-log/130-hypothesis-iter-4-mpc24.md`
from commit `21c3352` using the sterile SciAgent engineering/predictive review
contract and all six round-3 issues. The dispatch was charged before review,
bringing Cycle-3 hypothesis-review usage to `4/12`.

## Review integrity

- Reviewer-reported line count: `745`.
- Orchestrator verification:
  `git show 21c3352:research-log/130-hypothesis-iter-4-mpc24.md | wc -l`
  returned `745`.
- Orchestrator verification:
  `git show 21c3352:research-log/130-hypothesis-iter-4-mpc24.md | sha256sum`
  returned
  `ac1592714ba28df9b740a5edb6592a0dc2e729a8d6afb5ca2aa5f4f7f48ea9e3`.
- Orchestrator verification:
  `git diff --exit-code 21c3352 -- research-log/130-hypothesis-iter-4-mpc24.md`
  exited zero with empty output.

## Reviewer report (verbatim)

Status: DONE

File reviewed: `research-log/130-hypothesis-iter-4-mpc24.md`  
Line count: **745**. This matches `git show HEAD:research-log/130-hypothesis-iter-4-mpc24.md | wc -l`; the working-tree copy is unchanged.

## 1. Blind Assessment

### Previous-review issue disposition

1. **Observed extrema presented as future bounds — RESOLVED.**  
   Lines 334–336 explicitly classify the sentinel values as point estimates, not bounds, intervals, expectations, or dominance guarantees. The old extrema rule is gone.

2. **Fallback portfolios and accounting incomplete — IMPROVED.**  
   Lines 338–419 now specify prior-return immutability, current-prefix selection, generation/replay/slot charges, and permanent state downgrades. It is not fully resolved because the pre-attempt admission rules at lines 387–397 remain non-operational: neither the cost nor eligibility of the next path is known before it is attempted.

3. **Provisional joint-cap objective absent — IMPROVED.**  
   Lines 293–336 add `n_hat_m` and `P_hat_m` and charge the sentinel. However, the rule is not total: `P_hat_8` is defined only for eligible 8-prefixes, while line 328 can reference it whenever 24 is eligible. Eligibility is not prefix-monotone.

4. **Frozen branch profiles absent — RESOLVED for the requested categories.**  
   The nine fixtures cover sentinel 24/8/1/drop, first-fill and later regression, incomplete sentinel, replay binding, and candidate binding. A new uncovered eligibility edge remains, described below.

5. **Engineering evidence paths/hashes/commit absent — IMPROVED.**  
   Lines 233–266 now bind samples, summary, audit, config, and source files. `COMPLETE.json` transitively binds the profile runner and config. It still does not record the generating git commit or bind the full SDK/mock-agent source set used by the run; current source hashes do not prove those were the bytes used during measurement.

6. **Trace differencing versus event count and generation-to-replay transfer unclear — RESOLVED.**  
   Lines 148–171 and 421–429 correctly separate exported event identity from `tool_events_added` counting and explicitly state the weak public-replay transfer assumption.

### Justification Correctness

**NEEDS_REVISION.**

The boundary-density algebra is correct. From lines 211–226:

\[
\frac{16m+2}{h+ma}>\frac{18}{h+a}
\]

cross-multiplies, with positive denominators, to

\[
16(m-1)h-2(m-1)a
=2(m-1)(8h-a)>0,
\]

hence \(h>a/8\) for \(m>1\). More generally, comparing any \(m>k\) gives the same sign condition \(2(m-k)(8h-a)>0\). Thus the structural reading is sound: under full coverage, common reset cost, and linear incremental cost, packing more messages amortizes candidate-boundary cost.

That argument does not validate the actual replay ledger. The bound profile contradicts the fixed `rho=1.10` transfer used at lines 299–323:

- For the 90 measured arm-8/arm-24 generation/replay pairs, **84/90 (93.3%)** have replay/generation cost ratio greater than 1.10.
- The observed range is **1.0726 to 3.9801**.
- Every profile/master arm-8 or arm-24 group has a maximum ratio above 1.10.

More importantly, `mpc24_evidence_audit.py` computes the reported `1.507376725838` result using separately measured replay costs. The proposed MPC objective instead substitutes `1.10 × generation time`. The headline engineering ratio therefore evaluates an oracle with actual replay measurements, not the frozen controller’s replay proxy. Lines 245–260 cannot support the objective at lines 293–323 as written.

The checker passing does not resolve this: it checks synthetic fixtures designed around the frozen rule, not whether the rule agrees with the measured replay-cost surface.

### Mathematical Depth & Validity Domains

**NEEDS_REVISION.**

The notation is unusually concrete: \(E_{zji}\), \(s_{zji}\), \(x(m)\), coverage, cost, and proxy value all have operational meanings. The rate equation is not decorative mathiness; it identifies the reset-cost structure and explicitly states its full-coverage/linear-cost domain.

The weak target-facing assumptions, however, lack usable validity regimes:

- Lines 523–525 assume one sentinel is directionally informative about later paths but specify no conditional stationarity, exchangeability, minimum correlation, or drift diagnostic.
- Lines 526–528 assume generation-to-replay transfer despite the retained data showing large replay/generation discrepancies.
- Lines 534–535 assume the 0.90×1.10 ledger avoids a void without a calibrated tail probability or even consistency with the bound profile.
- Lines 538–539 give no operational limit on acceptable temporal drift.

Calling these assumptions “uncalibrated” is honest, but it is not a validity domain.

### Logical Soundness

**NEEDS_REVISION.**

Two totality failures matter:

1. **Undefined initial-state expression, lines 305–332.**  
   A path can have five successes in its first eight messages and thirteen successes in messages 9–24. Then:

   - `coverage(8)=5/8<0.75`, so `P_hat_8` is undefined;
   - `coverage(24)=18/24=0.75`, so 24 is eligible.

   Line 328 nevertheless evaluates `P_hat_24 >= 1.10*P_hat_8`. The checker silently implements a different rule by requiring both `24 in estimates` and `8 in estimates`. The prose, config, and checker are therefore not the same policy.

2. **Non-implementable look-ahead stopping, lines 387–397.**  
   “Cannot admit the current state” and “no eligible prefix could fit” require the next path’s unknown runtime, coverage, and prefix cost. The author checker obtains the future fixture’s `attempt_cost` before charging it, which is oracle information unavailable online. “On uncertainty, shorten or stop” does not choose uniquely between those actions.

### Assumption Completeness

**NEEDS_REVISION.**

Most major assumptions are named, including transfer, drift, collisions, and shared service load. The missing load-bearing assumption is a concrete within-run relation between sentinel and fill paths. “Directional usefulness” does not define the regime in which one sample can select between two arms.

Violating sentinel-to-fill stationarity, replay-cost calibration, or temporal comparability invalidates the official prediction rather than merely weakening it. These are central, not peripheral assumptions.

### Fixed Bias Surface

**Formally complete.**

Lines 601–627 walk all eight required categories separately: selection, confounding, assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting. The limitations are described accurately.

The list does not cure adaptive reuse: the Phase-3 profiles and masters are the same three profile families and masters that produced and informed the controller. Phase 3 is principally a mechanics regression test, not independent validation.

### Taxonomy Verification

The stated **Puzzle/Contradiction × Optimization/Search × replace** classification is defensible. The contribution replaces fixed-8 with an adaptive multiplicity policy and does not bridge literatures or integrate attack families. “Resource Bottleneck” is a plausible secondary opportunity label, but Puzzle/Contradiction is supported by the explicit boundary-versus-density tradeoff. No Bridge×Synthesis tripwire applies.

### Anti-Stacking Check

1. **Specific measured bottleneck per component: FAIL/PARTIAL.**  
   The 24/8 selector targets measured heterogeneity. The trace differencer has a correctness fixture. But fallback benefit and replay-ledger adequacy are not measured per component, and the replay measurements actively challenge the chosen 1.10 multiplier.

2. **Per-component ablation planned: FAIL.**  
   Lines 437–455 mention local no-fallback/no-ledger diagnostics, but the frozen Phase-3 comparators at lines 475–504 are only `fixed_8`, `fixed_24`, and `mpc24`. There are no frozen ablation cells, metrics, or decision thresholds for fallback or ledger removal. Attribution and state-machine fixtures are correctness tests, not ablations.

3. **End-to-end contribution under a constraint: PASS.**  
   The claim is the official artifact result under generation, replay, candidate, and validity constraints, not novelty from merely combining modules.

Thus the engineering anti-stacking test does not pass all three required conditions.

### Occam’s Razor

Fixed-8 is correctly identified as the simpler hypothesis at lines 586–599, and a fixed-8 comparator plus an adverse fixture are predeclared. This part is sound.

However, using the same authored profiles and masters that motivated MPC makes the planned Phase-3 Occam adjudication weak. A genuinely held-out mechanism regime is needed before claiming the controller earned its complexity.

### Alternative Explanations

Lines 570–584 give a strong list: drift, stochasticity, fixed-8/fixed-24 sufficiency, template variation, wording, row weights, unmodeled novelty, and capacity change. The scope restraint is appropriate.

The official threshold remains poorly justified. Lines 14–28 predict `>69.570`, while lines 185–188, 256–260, 506–508, and 702–716 concede there is no calibrated mapping from the raw proxy or authored profiles to official public score. The claim is falsifiable, but the exact threshold is a conjecture rather than an evidence-supported predictive consequence.

### Overall

**NEEDS_REVISION**

Required fixes, ordered by severity:

1. **Repair the replay-cost model and re-evaluate the actual MPC policy** — lines 293–323, 421–429, 534–535. The retained evidence shows `rho=1.10` is usually below measured replay/generation ratios, and the reported 1.507 ratio uses a different, oracle replay-cost calculation.

2. **Make the controller total and implementation-unique** — lines 305–332 and 387–397. Define the 24-eligible/8-ineligible case and replace oracle pre-attempt admission with an observable sequential rule.

3. **Supply real per-component evidence and frozen ablations** — lines 437–455 and 475–504. Add exact no-fallback/no-ledger or equivalent diagnostic arms, metrics, thresholds, and measured bottleneck numbers.

4. **Bind measurement provenance completely** — lines 233–266 and 728–729. Record the generating commit, environment/time, runner, config, SDK, fixtures, guardrail, and mock-agent hashes in the profile completion artifact.

5. **Give the official-score prediction an evidential bridge or narrow it** — lines 14–28 and 702–720. No current result maps the controller’s proxy gain to exceeding 69.570.

6. **Operationalize the target-facing assumptions** — lines 523–550. State observable validity/rejection regimes for sentinel-to-fill dependence, replay transfer, ledger safety, and temporal drift.

## 2. Actionable Coaching

- Define initial selection as a total function. For example, explicitly require both 8 and 24 to be eligible before comparing them, then freeze what happens when only 24 is eligible. Add the late-recovery fixture described above.

- Replace oracle admission with a sequential deadline rule: start only from an observable cost envelope, check the real deadline after every interaction, and abort at the longest already verified prefix. Freeze how the envelope is estimated and updated.

- Model replay cost structurally as at least `fresh-environment construction/reset + per-message replay cost`, rather than a scalar multiple of generation time. Calibrate a one-sided envelope on held-out runs and report its miss rate.

- Recompute selector choice, candidate count, timeout rate, and MPC/fixed-8 ratio using the exact frozen replay proxy—not separately observed future replay costs.

- Add local ablations with predeclared outcomes:

  - fixed-8 / fixed-24 / full MPC;
  - selector without monotone fallback;
  - controller without indexed attribution;
  - controller without the replay ledger, locally only;
  - full MPC with a calibrated ledger.

- Use new masters and at least one unanticipated profile family for Phase 3. Current profiles are valuable mechanics tests but are not independent evidence.

- Either calibrate proxy portfolio value against authenticated historical public scores or make the primary claim the controlled Phase-3 result. Promote an official `>69.570` prediction only after the bridge is measured.

- Preserve the complete eight-category bias surface; it is one of the strongest parts of the entry.

## Gate Check

- Review integrity: **PASS** — 745 reviewer/committed lines and SHA-256 match.
- Theory-review verdict: **NEEDS_REVISION**.
- Cycle-3 hypothesis review: `4/12` spent.
- Phase-2 gate: **FAIL / remains open**.
- Phase 3, attack implementation and Kaggle mutation remain closed.

## Problem alignment

Rejecting the 1.10 generation-time replay proxy prevents a controller whose
evidence uses actual replay costs from being deployed with a different,
systematically optimistic online ledger. Totality and ablation defects likewise
prevent a conformance test from being mistaken for an end-to-end value test.

## Decision

Accept the adverse verdict. Preserve v4 immutably. Before another review,
rebuild the replay-cost model from the retained measured pairs, make every
online decision observable and total, bind complete run provenance, freeze real
component ablations, and either construct an evidence-backed official-score
bridge or narrow the claim.
