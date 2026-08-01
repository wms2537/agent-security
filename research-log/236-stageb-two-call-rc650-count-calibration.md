# Stage B two-call rc650 count calibration

**Date:** 2026-08-01 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 8 · **Status:** preregistered before remote run

## Context

The v33 single-message two-call control completed as ref `55138755` with public score `65.320` at `return_count=500`. This is a regression against the historical `81.225` incumbent, but it is not a format failure or a zero-density result.

The target-derived density is:

```text
per_candidate=0.130640
density_vs_single=1.451555555556
rc650_projection=84.916
rc700_projection=91.448
rc650_single_post_fallback=58.500
threshold_density_for_81.225_at_rc650=1.388461538462
```

## Arithmetic correction

Report 233 paired two statements that should not have been paired: at `N=500`, `1.5` successful events per candidate predicts roughly `65`, not a score above `81.225`. To beat `81.225` at `N=500`, the run would need near-full two-event behavior, about `1.91` single-post equivalents per candidate.

Therefore v33 disconfirms the original `rc500` competitive-score threshold, but it supports a useful target response profile: the selected structure produced about `45.16%` more public score per candidate than a single-post candidate.

## Next experiment

Run one guarded count calibration at `return_count=650`.

The only source change from the prepared v34 artifact is the fixed count `500 -> 650`; the two-event admission guard remains in place. This means:

- if the selected probe has at least two EXFILTRATION events, fill with single-message two-call candidates;
- if the selected probe has zero or one event, fill with the known single-post floor;
- no full-fill verification or generation-side replay-cost sizing is reintroduced.

## Prediction

Primary prediction: if v33 density transfers, public score will be approximately `84.916`, beating the `81.225` incumbent.

Fallback diagnostic prediction: if the guard selects single-post fallback, public score will be approximately `58.500`.

Failure prediction: a blank/error result means the rc650 two-call replay boundary is unsafe or the guard is insufficient under hidden target replay; no rc700+ submission is allowed until a visible rc650 result exists.

Confidence is low-to-medium. The expected value is positive because the observed density only needs to remain above `1.3885x` single-post at rc650 to beat the incumbent, but replay cost may be nonlinear because a single user message can still induce additional model/tool turns.

## Submission confidence gate

This candidate may be submitted only after all of these deterministic checks pass:

```text
py_compile experiments/attack.py
local two-call and fallback fixtures
submission/build_notebook.py
direct-serve notebook contract
downloaded Kaggle kernel output schema
```

## Problem alignment

This directly serves the competition objective in `PROBLEM.md`: use target-owned feedback to calibrate a source-compliant candidate policy that improves score density without relying on hidden replay-time estimates.
