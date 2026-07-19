# ORF public non-target core PoC

**Date:** 2026-07-19 · **Phase:** 3 · **Cycle:** 1 · **Iteration:** 4 · **Status:** preregistered, not run

## Context

The immutable v9 ORF hypothesis passed theory review round 11 as RIGOROUS. Phase
3 now tests the smallest scientific assumption that is legal without the
separately prohibited beacon/freeze/held-out chain: whether the exact ORF
score-table mechanics produce material conditional regret on an untouched public
non-target realization while the homogeneous invariant and actual SDK score
identity remain exact.

The repository was missing the SciAgent-standard `environment.md` and
`evaluation-contract.md`; both are repaired before execution. This PoC cannot
confirm the future beacon-held-out v9 claim.

## Design

The primary probe fixes the public ASCII label
`orf-public-poc-v1|master|000` before execution and hashes it once with SHA-256.
It evaluates replicate 0 from every one of the 40 crossed strata, for 40 profiles
total. This is one-eighth of the planned 320-profile target while preserving the
full factorial support. For each profile, immutable functions from
`experiments/poc/orf_support_calibration.py` compute exact score tables for
lengths `{1,2,4,8,16,24,32}` at `H=200000`. The primary metric is
`100*(A-G)/G`, where `A` sums per-profile maxima and `G` is the best one-length
aggregate with smaller-length tie-breaking.

Two controls are mandatory. First, 64 independently keyed homogeneous profiles
must yield exact adaptive-minus-global regret zero and both policies must select
length 1. Second, the two preserved actual-SDK fixtures must recompute their
predicates, actual 16-hex score-cell hashes, uniqueness, and raw identity
`q=16e+2`.

## Prediction and rationale

Before the run, the predicted primary value is **35.0%**, with low confidence.
The valid exploratory calibration v2 (entry 015) found 64/64 independent public
masters above 5%, with an equal-weight `H=200000` minimum of 34.575811113981% and
median 40.924155277025%. This PoC uses a distinct label never present in that
calibration and only one replicate per stratum, so the calibration supports the
direction but not a tight magnitude. A broad preregistered 20–50% interval
therefore defines a prediction-ledger confirmation; a value at least 5% but
outside that interval is partial; every valid value below 5% disconfirms the
core materiality assumption.

Secondary predictions are exact: homogeneous raw regret `0` and exactly `2`
actual-SDK fixture cases verified.

## Transferability argument

The 40-profile probe preserves every factor cell, the action set, exact score
identity, resource equations, saturation, tie-breaking, and generator family of
the 320-profile synthetic design. It is therefore capable of detecting whether
the proposed action-scope effect survives the whole designed heterogeneity
support rather than one cherry-picked slice. Replicate aggregation can change
the globally best length and the exact regret magnitude, so this probe supports
mechanics and plausibility only. It cannot establish the future master outcome,
real-model response-profile prevalence, probe learnability, shared-resource or
deadline behavior, private-guardrail transfer, or Kaggle performance.

## Pre-specified decision

- **Confirmed:** protocol valid, gain in `[20,50]`%, homogeneous difference 0,
  both homogeneous choices length 1, and two SDK cases pass. Recommend Phase 4.
- **Partially confirmed:** protocol valid and gain at least 5% but outside
  `[20,50]`%; revisit only the expected-magnitude model before Phase 4.
- **Violated:** protocol valid and gain below 5%; record a refutation and return
  to Phase 2.
- **Protocol-invalid:** any wrong count, hash, score identity, nonzero homogeneous
  difference, wrong homogeneous choice, numeric stability failure, or prohibited
  action. No scientific inference.

The user's advance authorization is: “then go on with next phases up until phase
6 then, define a goal”. It permits continuation after a successful gate within
the already stated no-Kaggle/no-held-out-action boundary; it does not turn a
partial, violated, or invalid result into a go decision.

## Gate Check

Pending execution and independent verification.

## Problem alignment

This tests whether profile-conditioned candidate-structure selection has a
material benchmark-shaped synthetic advantage over a copied one-length policy,
without pretending the public probe is the live leaderboard.

## Decision

Preregister and commit the immutable design, prediction ledger, environment, and
evaluation contract before dispatching one `RUN_ID=poc` implementer.

## Next Steps

Implement, run, and independently verify the public non-target PoC. No beacon,
held-out, external-post, or Kaggle action is allowed.
