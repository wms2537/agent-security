# Theory Review — Measured Dense Replacement v4

**Date:** 2026-08-02 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 10 · **Status:** needs-revision

## Context

Report 252 superseded report 250 after the round-3 `NEEDS_REVISION` verdict. A sterile v4 re-review was dispatched.

## Gate Check

- Committed line-count evidence: `git show HEAD:research-log/252-hypothesis-iter-10-measured-density-overlay-v4.md | wc -l` -> `206`.
- Reviewer-reported line count: `206`.

## Verdict

```text
Status: DONE
Line count: 206
Previous issues:
1. RESOLVED — lines 11-15 rename the mechanism and narrow fallback as inherited control; lines 112-119 state Optimization Bottleneck / Engineering replacement / replace and explicitly say v35 fallback is not the novelty claim.
2. RESOLVED — lines 120-126 now say public score alone cannot attribute the mechanism and require a local no-fire fixture, local positive fixture, and public score together.
3. IMPROVED — lines 70-89 add threshold math for `84` and discuss `96`, but not resolved: line 67 says `2,000 * 0.090 = 90.000`, which is arithmetically inconsistent, and lines 82-89 show `96` is sufficient but not why it is the chosen cap.

New issues:
- lines 65-67: core scoring-unit error/inconsistency. If `MAX_REPLAY_FINDINGS = 2,000` and single-post contribution is `0.090`, the product is `180.000`, not `90.000`; if public-row averaging is intended, it must be stated and applied consistently to dense contributions in lines 72-79.
- lines 74-79 and 58-59: the `20%` fallback-displacement model is asserted but not tied to the actual return/order/budget mechanics.
- lines 82-89: `96` is not mathematically selected; under the stated four-event equation, strong success needs `ceil((100.000 - 69.336) / 0.330) = 93`, so `96` is an unexplained margin.
- lines 47-53 and 91-99: several frozen constants are operationally plausible but not mathematically justified, especially `MEASURED_DENSE_SCORE_RATE_GAIN = 1.15`, probe reps, max attempts, probe base, and frame offset.

Blind assessment:
- Justification Correctness: fail with evidence — the central ceiling calculation at lines 65-67 is internally inconsistent, and the threshold derivation at lines 78-79 depends on that scoring unit.
- Engineering Tests: pass with evidence — lines 103-109 give component evidence and comparators; lines 189-195 require positive, no-fire, capped-unmeasured, and score-rate-stop checks.
- Confounds: pass with evidence — lines 130-137 cover selection, confounding, assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting; line 28 limits scope.
- Taxonomy: pass with evidence — lines 112-119 frame the method as engineering replacement with v35 fallback as inherited regression control.
- Anti-stacking: pass with evidence — lines 120-126 require local comparator distinction plus public score and explicitly reject public-score-only attribution.
- Occam/Alternatives: fail with evidence — lines 161-163 reject single-post micro-tuning using the challenged `90.000` ceiling, and lines 82-89 do not justify why the cap is `96` rather than the derived minimum or a stated safety margin.
- Overall: NEEDS_REVISION

Actionable coaching:
- Fix the public-score formula first, including any two-row averaging, then recompute single-post and dense candidate contributions.
- Re-derive `84` and `96` under one consistent scoring unit.
- Tie the `20%` displacement assumption to concrete implementation mechanics or add a sensitivity table.
- Either justify `96` as a named safety margin or choose the mathematically derived cap.
- Label non-theory operational constants as implementation defaults unless they affect the prediction.
```

## Decision

Write v5. Required corrections:

- use `0.090` consistently and stop calling `90.000` a source ceiling;
- set the primary target to `>=100.000`;
- require four-event dense candidates and derive `93` minimum retained dense candidates under the 20% fallback-displacement model;
- define `96` as a three-candidate slack margin over the derived minimum;
- label non-threshold constants as operational defaults.
