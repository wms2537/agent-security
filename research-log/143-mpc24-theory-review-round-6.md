# Counterbalanced MPC-24 theory review round 6

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** NEEDS_REVISION

The following independent sterile review is recorded verbatim.

---

**Status: DONE**

Reviewed `research-log/140-hypothesis-iter-6-mpc24-counterbalanced.md` in full.

**Line count: 540** in both the worktree and `HEAD`.

## 1. Blind Assessment

### Previous-review issue disposition

| Previous issue | Disposition | Judgment |
|---|---|---|
| 1. Canonical clock and sentinel admissibility | **RESOLVED** | Lines 233–258 define one controlled generation ledger, replay ledger, reserve, outer timeout, and cap. The checker rejects conflicting root budgets and proves time-zero start admissibility via `0 < 0.1 < 6 < 120`. I reran it successfully. This proves that a sentinel may start, not that all 24 interactions necessarily complete, but the online abort rule makes completion an outcome rather than a logical prerequisite. |
| 2. Wall-time confounding | **IMPROVED** | Lines 299–329 add four paired repetitions and ordinal-position balance. However, the four schedules are cyclic rotations of one order. Consequently, when not first, MPC is always preceded by `static`, fixed-8 by MPC, fixed-24 by fixed-8, and static by fixed-24. Method-specific cache/thermal carryover remains confounded with method. This is position-balanced, not carryover-balanced. |
| 3. Unmeasured fallback contribution | **IMPROVED** | Lines 295–297 and 348–355 demote fallback to a correctness control. But the deliberately delayed-cliff safety fixture remains one of the four profiles included in the primary efficacy aggregate at lines 305–325. If salvage changes MPC raw there, fallback still contributes to the headline gain despite the semantic demotion. |
| 4. Attribution/ledger fixtures versus end-to-end removals | **IMPROVED** | Attribution, state, and deadline fixtures are now honestly labeled diagnostics. The replay ledger is not repaired: lines 26 and 343–347 test scalar-1.10 retrospectively “on the same traces.” That is a coverage diagnostic, not an end-to-end controller removal, because changing the ledger changes selection, candidate count, paths generated, and possibly state transitions. |
| 5. Fixed-24/static strongest-simple comparison | **RESOLVED** | Lines 13–20 and 331–337 require MPC to exceed the maximum aggregate of fixed-8, fixed-24, and a frozen static 8/24 sequence. The claim is correctly scoped to those enumerated policies. |
| 6. `c(1)` interpretation and taxonomy | **RESOLVED** | Lines 195–197 call `c(1)` a correlated scale surrogate without causal boundary-cost interpretation. Lines 435–444 correctly classify the work as Resource Bottleneck × Optimization/Search × replace. |

### Justification Correctness

The boundary-density algebra at lines 159–173 is correct. For `m>k`,

\[
(16m+2)(h+ka)-(16k+2)(h+ma)
=2(m-k)(8h-a),
\]

so with positive denominators, `rate_m > rate_k` exactly when `h>a/8`. The entry correctly limits this to full coverage, a common boundary cost, and linear incremental message cost. It also correctly denies that this identifies `h` or proves that 24 is optimal. The equation carries a modest structural argument and is not mathiness.

The empirical artifacts contain real, traceable measured numbers:

- The selector source has 360 sample rows and measured selections of 24 in 6/9 cells and 8 in 3/9.
- The replay calibration reruns successfully with scalar misses `84/90`, calibration coverage `81/81`, held-out coverage `54/54`, and maximum held-out actual/surrogate ratio `0.801015756432`.
- The author checker passes the hashes, clock, method-position counts, taxonomy, and comparator fields.

However, these facts do not justify the full quantitative prediction. The only prior value estimate is MPC/fixed-8 `1.443010752688`, computed offline using independent-arm prefix-8 timing. It provides no estimate against fixed-24 or the new static mixture, under nested Phase-3 timing, on the new profiles. Nothing at lines 175–209 or 331–337 derives or empirically supports the `>=1.05` MPC/best-simple margin. “Low confidence” does not replace a quantitative rationale.

The replay component test is also incorrectly classified. Applying scalar-1.10 to traces generated under the calibrated controller cannot estimate the system result with the scalar ledger. It can show that scalar accounting would miss replay costs on those traces; it cannot show how the scalar controller would select, fill, transition, or score.

Finally, the cited selector artifact’s own `summary.json` has `status: FAIL` and `sdk_decisions_passed: 6/9`. The 24/8 split remains a real observation and may legitimately seed a new hypothesis, but lines 175–184 should disclose that it is a post-hoc reuse of a disconfirming artifact, not present it as an unqualified positive profile.

### Mathematical Depth & Validity Domains

The notation is mostly operational:

- `E_ji` is the event suffix belonging to message `i`.
- `s_ji` is a host-specific success indicator.
- `x_j(m)` counts successful messages.
- `coverage_j(m)` is the successful-message proportion.
- `c_j(m)` is cumulative observed generation time.
- `q_j(m)` is the controlled raw value of one returned prefix.
- `n_m` is the point-estimated additional feasible count under generation, replay, and candidate ledgers.
- `P_m` is estimated portfolio raw, explicitly not a bound or expectation.

The principal validity-domain omissions are:

1. **Sentinel-to-fill stability, lines 266–285.** Why should one sentinel’s `c_m`, coverage, and `q_m` predict additional paths? The controller requires at least local stability or a defined nonstationarity regime. The delayed profile deliberately violates part of this relation, but the assumption is never stated generally.

2. **Reserve validity, lines 241–264.** `rho=0.1` is an admission reserve, but no assumption says one interaction’s wall time is bounded by `rho`. Without that regime, a path admitted with slightly more than 0.1 seconds remaining may overshoot `G`. An observed-only rule can be testable without a hard guarantee, but the prediction of zero overages relies on a missing timing-tail assumption.

3. **Threshold validity, lines 148–149 and 278–280.** Neither `coverage>=0.75` nor `P24>=1.10 P8` has an empirical, decision-theoretic, or robustness rationale. They are frozen, which controls analysis flexibility, but their regime of usefulness is not justified.

4. **Score identity, lines 145–149.** `q=16x+2` is concrete but its exact scorer validity conditions—unique hosts, relevant event class, absence of other reward/penalty terms, and cap behavior—are not stated alongside the formula.

The mathematics is not pretending to prove superiority, which is good. The actual breakthrough, if any, is the controller and resource accounting, not the algebra.

### Logical Soundness

Several implications do not follow:

- Lines 295–297 say fallback supplies no gain claim, yet lines 305–325 include its purpose-built delayed fixture in the headline sum. If the fixture moves the ratio, the result cannot be attributed only to selector plus resource estimation.
- Lines 343–347 call same-trace scalar replay checking a removal. A counterfactual controller cannot generally be evaluated on another controller’s endogenous traces.
- Section 5 specifies MPC’s sentinel, selection, prefix return, and state transition, but never gives implementation-unique fixed-8, fixed-24, or static-policy rules. It is unclear whether controls salvage incomplete prefixes, how they estimate replay capacity, what happens on low coverage, whether they pay a first-candidate calibration cost, and how static-sequence truncation is handled. “Same ledgers” at lines 49–50 does not resolve these decisions.
- The `>=1.05` margin is a leap from an offline MPC/fixed-8 statistic to a different comparator set and execution design.
- The cyclic Latin square balances position but not predecessor carryover, despite wall time directly determining discontinuous candidate counts through floors.

### Assumption Completeness

The 13 listed regimes are useful, and the fixed bias surface includes all eight required categories: selection, confounding, assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting.

Load-bearing missing assumptions remain:

- sentinel measurements are informative for subsequent paths within the cell;
- baseline policies use equivalent attribution, admission, replay, salvage, and charging rules;
- cache/thermal/carryover effects are absent, reset, or balanced;
- `rho` adequately covers the controlled interaction-time tail if zero overage is predicted;
- the purpose-built delayed fixture cannot materially supply the primary gain unless fallback is treated as a contribution component.

Violating the first two invalidates the selector comparison entirely. Violating carryover balance makes the wall-time result inseparable from schedule effects.

### Taxonomy Verification

The classification is correct:

- **Opportunity:** Resource Bottleneck.
- **Method paradigm:** Optimization/Search, with Artifact/System as a plausible secondary label.
- **Dominant operation:** replace.

This is not Bridge Opportunity × Synthesis/Unification and does not trigger the local-move tripwire. The replacement is genuinely local: an online controller replaces fixed multiplicity.

The claim verbs remain predictive and do not exceed the project’s predictive question type. No target causal effect or population transfer is claimed.

### Anti-Stacking Check

1. **Specific measured bottleneck per component: PARTIAL.**

   - Replay accounting has a measured failure rate: scalar-1.10 misses 84/90 pairs.
   - Selector evidence has measured 24/8 heterogeneity, but not the magnitude of constrained-raw loss caused by using one fixed policy. A winner count is weaker than a measured bottleneck share or regret artifact.
   - The source numbers and hashes are real, but the failed origin status should be disclosed.

2. **Per-component ablation: FAIL.**

   - Selector versus fixed/static controls is an end-to-end comparison.
   - Replay scalar checking on calibrated-controller traces is not an end-to-end ledger removal.
   - Fallback is excluded from the component list while remaining able to affect the primary aggregate.

3. **End-to-end system claim under a stated constraint: PASS.**

Because all three tests must pass, the engineering anti-stacking gate fails.

### Occam’s Razor

Adding fixed-24 and a static mixture is a material improvement. Nonetheless, the simplest surviving explanation is still that one frozen simple allocation wins on these authored profiles. The design tests that only for one arbitrary 3:1 sequence. The motivating 6/9 versus 3/9 split suggests a 2:1 mixture, not 3:1, and no evidence identifies `[24,24,24,8]` as the strongest static mixture or phase ordering.

The primary claim carefully says “best among” the three listed policies, so this is not a semantic contradiction. It does mean “strongest simple comparator” at lines 331–337 overstates the explored class.

### Alternative Explanations

The predicted result could arise because:

- the delayed safety fixture mechanically rewards MPC salvage;
- fixed/static policies receive less favorable incomplete-path handling;
- cyclic predecessor carryover changes wall time and candidate-count floors;
- the chosen static ratio or phase is suboptimal;
- authored profiles encode the desired 24/8 heterogeneity;
- the conservative calibrated surrogate alters capacity without improving end-to-end score relative to a correctly rerun scalar controller;
- a generic scale correlation, rather than any boundary mechanism, explains `c(1)`—which the revision now appropriately acknowledges.

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. **Make every comparator implementation-unique and symmetric** — lines 49–50, 74–80, and 233–297. Specify admission, path stopping, prefix salvage/drop, coverage eligibility, replay estimation, candidate charging, sequence truncation, and overage handling for fixed-8, fixed-24, and static.

2. **Remove efficacy contamination by the delayed fallback fixture or restore fallback as a contribution component** — lines 295–325 and 348–355. A safety-only fixture should not influence the primary selector/resource-estimation endpoint. Otherwise supply prior measured fallback evidence and run a true end-to-end no-fallback ablation.

3. **Execute the replay-ledger removal end to end** — lines 26, 343–347, and 446–449. Run a separate MPC controller whose selection and capacity use scalar-1.10; same-trace miss counting may remain a correctness diagnostic but cannot satisfy the component-ablation gate.

4. **Justify the quantitative primary prediction** — lines 13–20, 199–209, and 331–337. Provide pre-run estimates against fixed-24 and the frozen static policy under the actual nested controller, or narrow the prediction to a supported comparison/threshold.

5. **Balance first-order carryover, not only position** — lines 314–329 and 418–423. The cyclic schedule gives each method a fixed predecessor. Use a Williams/balanced crossover order, explicit resets/washout, or deterministic injected costs.

6. **State the missing validity regimes** — lines 241–285 and 357–385: sentinel-to-fill stability, reserve/timing-tail conditions, threshold rationale, and exact scorer assumptions.

7. **Disclose the antecedent artifact’s failed status** — lines 175–184 and 211–218. Explain that the 24/8 split is exploratory evidence extracted from a disconfirming run and is used only to motivate the fresh preregistered batch.

## 2. Actionable Coaching

- Define a shared policy interface and give pseudocode for all four methods. Keep only the multiplicity decision different; everything else—clock reads, coverage, salvage, replay accounting, identity allocation, and stop conditions—should be literally shared code.

- Separate the delayed-cliff integration run from the 12-cell primary comparison. Report it as a required safety suite. If delayed behavior remains in the primary grid, add MPC-without-salvage as a real fifth controller ablation.

- Replace the scalar same-trace test with two outputs:

  1. a diagnostic paired miss table on common traces; and  
  2. a separate end-to-end scalar-ledger controller run measuring aggregate raw, selected states, overages, and invalidity.

- Use a four-sequence Williams design so every directed predecessor pair occurs once, or add method-state reset and cooldown checks. Retain ordinal-position counts and report predecessor-conditioned timing spreads.

- Freeze a simple-policy search over proportions and cyclic phases using antecedent data only, then carry forward the single best static policy. If `[24,24,24,8]` remains chosen, explain why it beats the natural 2:1 alternative implied by the 6/9–3/9 split.

- Add a quantitative prediction table for MPC, fixed-8, fixed-24, and static: expected aggregate, evidence source, extrapolation needed, and uncertainty. The 5% materiality threshold should follow either from these estimates or from a stated engineering complexity cost.

- Retain the correct boundary-density derivation, but add one sentence that it is intuition only. Put the empirical burden on nested timing, replay coverage, and end-to-end comparisons rather than extending the algebra.

---

## Gate consequence

- Verdict: `NEEDS_REVISION`.
- Review integrity: committed line count `540`; SHA-256 `11d184befb428646b77d2af43ac3a44d75dd64a8967bb4905b22b64f668f84ea`; immutable diff empty.
- Cycle-3 hypothesis-review budget remains `6/12` spent; the charge occurred at dispatch.
- Phase 2 remains open. Phase 3, attack implementation, Kaggle mutation, and submission remain closed pending a scrutinized `RIGOROUS` verdict.
