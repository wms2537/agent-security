Status: DONE

File reviewed: `research-log/178-hypothesis-iter-8-ahcms24-v5.md`  
Line count: **654**, matching both working tree and `git show HEAD`.  
SHA-256: `1877c5023d16addcd029a9a9d9cacbbe34b5213deef9faa8bd9c86f8dc0025bb`

## 1. Blind Assessment

### Previous-review issue disposition

1. **Boundary-consistent construct and profile — RESOLVED.**  
   Lines 160–181 recompute the profile using only historical `path_cost_s`; lines 255–280 specify the identical prospective landmarks and correctly include in-bracket scheduling, preemption, sleep, and checkpoint serialization. Lines 342–360 bound the interpretation through a mandatory 50% retry-tail discount. The construct is now honestly “projected captured elapsed,” not CPU work or scheduler-free time.

2. **All-zero AHCMS/simple branch — RESOLVED.**  
   Lines 405–436 correctly state that `R_a=R_s=0,R_r>0` disconfirms the primary and retention predicates, leaves the simple-control cross-product defined as `0>=0`, and emits `NA_zero_simple_raw`. The executable checker includes this exact adversarial case and an exhaustive simple-control grid.

No new assessment-blocking defect was introduced.

### Justification Correctness

The causal mechanism is valid within the deliberately narrow controlled-trace estimand. AHCMS and retry share all stored outcomes through the first replay-ledger no-fit, after which AHCMS deletes only the retry suffix. Therefore:

\[
T_r=T_a+T_{\text{tail}},\qquad
R_r=R_a+R_{\text{tail}}.
\]

For positive elapsed and retry raw,

\[
\frac{R_a/T_a}{R_r/T_r}
=\frac{R_aT_r}{R_rT_a},
\]

so the preregistered integer test

\[
10R_aT_r\ge 11R_rT_a
\]

is exactly the `>=1.10` efficiency condition.

Expanding the comparison gives

\[
R_a(T_a+T_{\text{tail}})
>(R_a+R_{\text{tail}})T_a
\iff
R_aT_{\text{tail}}>R_{\text{tail}}T_a.
\]

Thus suffix deletion helps precisely when the retained-prefix raw density exceeds suffix raw density. The equation carries the mechanism; it does not pretend to prove the empirical magnitude.

The half-tail sensitivity is correctly adversarial:

\[
H=\lfloor(T_r-T_a)/2\rfloor,\quad T_r^{1/2}=T_a+H.
\]

Reducing retry elapsed while keeping all retry raw increases retry efficiency, making the AHCMS comparison harder. Floor division is conservative for AHCMS.

I reran both bound checks. They reproduced:

- retry paths: `370`;
- retry captured elapsed: `69.00197669875342412 s`;
- retry-tail paths/elapsed: `146 / 18.36650123470462862 s`;
- absorbing elapsed: `50.63547546404879550 s`;
- retry/absorbing raw: `39258 / 39240`;
- nominal ratio: `1.362095216773`;
- half-tail ratio: `1.180818355750`;
- all zero-branch and 5,184 simple-control fixtures passing.

I also independently recomputed raw with the bound set-aware scorer per unit: retry `39258`, absorbing `39240`, marginal loss `18`.

The fixed eight-category bias surface is complete. It explicitly covers selection, confounding, assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting, with an operational response for each.

### Mathematical Depth & Validity Domains

The notation is mostly concrete:

- `R_m` is reconstructed integer raw;
- `T_m` is a sum of selected generation-path clock intervals;
- `L_m` is accepted-candidate replay elapsed;
- `P_m(u)` and `A_m(u)` identify the exact contributing path/candidate occurrences;
- overage indicators use strict `>2_000_000_000`.

The mathematics is appropriately limited to accounting identities, decision boundaries, and a bounded perturbation. It is not decorative theory.

Validity domains are explicit:

- positive elapsed for efficiency ratios;
- `R_r>0` before displayed raw ratios;
- deterministic frozen profiles for offline potential consistency;
- complete 24/8/1 support;
- exact timer-landmark equivalence;
- fixed nine-unit scope;
- no CPU-time, population, hard-deadline, target-model, or Kaggle inference.

The one minor notation blemish is that `q-independent` uses `q` without defining it in this entry. It is not load-bearing because the operational contract independently forbids fitted quantities and outcome-dependent thresholds, but it should be expanded for self-containment.

### Logical Soundness

The logical chain holds:

1. Complete stored traces observe every suffix that retry could select.
2. Both primary methods are identical through the trigger.
3. Absorption truncates only the observed suffix.
4. Raw is rescored per complete accepted unit sequence, avoiding invalid candidate-score addition.
5. A complete valid result deterministically maps to confirm or disconfirm; invalid acquisition is never relabeled.
6. Scope limitations are part of the claim, not deferred qualifications.

The zero domains are totalized correctly. `R_r=0` disconfirms; `R_a=0,R_r>0` fails primary and retention without denominator escape; zero-simple raw never creates an infinite or fabricated ratio.

The predictive claim verb is compatible with `PROBLEM.md`: it predicts one controlled local ablation and does not infer leaderboard or population causality.

### Assumption Completeness

The twelve assumptions cover potential consistency, trace completeness, timing and checkpoint equivalence, elapsed interpretation, the bounded perturbation, scorer monotonicity, trigger identity, prefix attribution, constrained feasibility, fixed-sample scope, and limited Occam scope.

Violations of assumptions 1–9 invalidate local attribution. Assumptions 10–12 instead bound the conclusion. This distinction is correct.

### Taxonomy Verification

The classification is accurate:

- **Resource Bottleneck**, secondarily Failure/Risk Gap;
- **Artifact/System**, secondarily Robustification;
- dominant operation **replace**.

The intervention replaces one retry transition with an absorbing transition. It is not Bridge Opportunity × Synthesis/Unification, so the heightened local-move tripwire does not apply.

### Anti-Stacking Check

All three engineering tests pass:

1. **Measured component bottleneck:** one component is tied to `146` retry-tail paths, `18.3665 s` captured elapsed, and `18` marginal raw, from a sealed source-audited profile.
2. **Per-component ablation:** otherwise identical retry HCMS is the exact one-field removal.
3. **End-to-end constrained claim:** the contribution is the fresh system result under raw retention, elapsed efficiency, sensitivity, overage, completeness, and specified-control constraints.

Replay envelopes and atomic gates receive no contribution credit.

### Occam’s Razor Check

Absorption is already a single local transition replacement. Fixed8 and fixed24/no-salvage test two simpler policies on the same endpoint.

A reduced global path cap remains a credible simpler rival. The revision handles this honestly: it neither calls the controls exhaustive nor claims global simplicity. That rival therefore limits interpretation but does not contradict the narrow preregistered comparison.

### Alternative Explanations

The entry addresses:

- absence of saturation;
- valuable retry recovery;
- scheduler/controller inflation;
- specified and unspecified simpler policies;
- purposeful profile construction;
- replay-ledger mismatch;
- excluded post-bracket overhead;
- remote-scale reversal.

The strongest objection is tail-specific scheduler or controller inflation. It defeats any CPU-work interpretation, but that is no longer the claim. The measured construct expressly includes such elapsed time, and confirmation must survive deleting 50% of the retry tail while retaining all retry raw. Arbitrary greater asymmetry remains outside scope. Thus the objection narrows external interpretation but does not invalidate the stated fixed-sample captured-elapsed claim.

The cited conformal literature is correctly boundary-setting rather than load-bearing: exchangeability supports marginal/expected-risk guarantees, while the recovery-deadline paper explicitly separates statistical coverage from verified hard safety. None is misused to certify this system.

### Overall: RIGOROUS

The hypothesis is falsifiable, boundary-consistent, causally identifiable on its stated matched traces, algebraically correct, fully totalized, explicitly scoped, and supported by a real per-component profile plus clean removal. Phase 2 may advance on this narrow claim; this verdict does not establish CPU savings, remote deadline safety, Kaggle benefit, or population transfer.

## 2. Actionable Coaching

- Define `q` at first use, or replace `q-independent` with the exact operational statement: no calibration quantity, threshold, sample identity, or projection rule is fitted from these nine outcomes.
- Make the timer audit derive absorbing raw from the bound candidate traces rather than hard-coding `39240`, even though independent rescoring confirms the value.
- Add a reduced-global-path-cap control in Phase 4 if later prose seeks a stronger minimality claim.
- If the claim is ever expanded from captured elapsed to CPU service or real wall-clock latency, add an appropriate independent measurement; the present monotonic-clock endpoint cannot support that expansion.
- Keep any remote/Kaggle bridge as a separately reviewed claim.
