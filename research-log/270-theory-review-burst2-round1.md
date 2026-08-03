# Theory review — Burst-2 Validation Fill round 1

Date: 2026-08-03

Reviewer path: direct fallback review after sterile subagent `theory_review_burst2` stalled twice and was interrupted.

Material under review: `research-log/269-hypothesis-iter-11-burst2-validation-fill.md`

Line count:

```text
git show HEAD:research-log/269-hypothesis-iter-11-burst2-validation-fill.md | wc -l
176
```

## Status

DONE

## Blind assessment

Overall: NEEDS_REVISION

### Justification correctness

The core hypothesis is salvageable, but the evidence chain overstates one load-bearing premise.

The audit establishes that a recent/high-signal public notebook contains `BURST_K=2`. It does **not** establish that this notebook caused, matched, or belongs to the `112.865` leaderboard entry. Kaggle `kernels list --sort-by scoreDescending` sorts public notebook metadata, not the competition leaderboard. Therefore, the current version must not imply that `dimong4` explains the leaderboard frontier.

The correct statement is narrower:

> Public notebooks expose a plausible above-ceiling mechanism prior; only our own target-owned submission can measure whether isolated K=2 transfers.

### Mathematical depth and validity domains

No decorative math problem. The hypothesis uses operational arithmetic and threshold bins, not unsupported formalism.

Validity domains need tightening:

- K=2 is justified only inside the v35 validation-fill/replay-safe controller.
- The public-audit evidence is a mechanism prior, not a score estimate.
- The hidden replay-cost model remains unidentifiable; the hypothesis must avoid claiming replay safety beyond the inherited v35 ledger and the terminal target result.

### Logical soundness

The `K=4 failed -> K=2 may be safer` logic is coherent, but not sufficient alone for a `>=100` prediction. The revision must state that `>=100` is the target bin, not a well-calibrated expectation derived from known K=2 event rates.

### Assumption completeness

Missing or under-specified assumptions:

1. K=2 must not silently change the v35 controller beyond message shape.
2. Split-by-latency behavior for K>1 must be specified. If disabled for K=2, that is an interface choice and must be declared as part of the candidate-shape replacement.
3. Keep-if-at-least-one-event means the returned set may include single-event K=2 candidates; the success condition therefore depends on second-event replay prevalence, which is hidden.

### Taxonomy verification

The `Optimization Bottleneck × Empirical Mapping × replace` classification is acceptable. This is not Bridge × Synthesis as long as the branch changes only one local structure and does not import the slow-row Harmony multipost component.

### Anti-stacking check

Mostly acceptable, but the planned ablation language needs to be stricter:

- `K=1` byte-equivalence must be tested mechanically.
- `K=2` must have exact URL/post counts.
- The implementation must not include `SLOW_MULTIPOST_N=4` or any K=4 dense fallback in this hypothesis.

### Occam's Razor

The simpler test is exactly K=2 alone. The hypothesis should explicitly reject adding slow-row Harmony multipost or extra template races in iteration 11.

### Alternative explanations

The current entry lists alternatives, but one must be promoted: public notebook performance, if any, may come from additional mechanisms not isolated here. That alternative directly threatens the predicted magnitude.

## Required fixes

1. Revise the evidence chain so public-notebook audit is a mechanism prior only, not a leaderboard-score explanation.
2. Freeze the K=2 implementation interface: no K=4, no slow-row Harmony multipost, no extra template race, no replay-cost multiplier change.
3. Specify split-by-latency behavior under K=2.
4. Clarify that the `>=100` threshold is the target-owned success bin, not a calibrated estimate from public notebook metadata.
5. Promote the second-event-prevalence risk: returned candidates may be retained after one event, while above-100 requires enough second events during replay.

## Actionable coaching

The revision should preserve the small experiment. Do not overcompensate by adding more components. The strongest version is:

> K=2-only, v35 controller, exact local mechanics, one commit-run confidence gate, then one target-owned submission if the output contract is clean.

If K=2 fails visibly, retire candidate-internal post cardinality below K=4 as insufficient under our runner and pivot to another dimension.
