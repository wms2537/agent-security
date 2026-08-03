# Theory review — Burst-2 Validation Fill v2

Date: 2026-08-03

Reviewer path: direct fallback re-review after the sterile subagent review path stalled in round 1.

Material under review: `research-log/271-hypothesis-iter-11-burst2-validation-fill-v2.md`

Line count:

```text
git show HEAD:research-log/271-hypothesis-iter-11-burst2-validation-fill-v2.md | wc -l
182
```

## Status

DONE

## Blind assessment

Overall: RIGOROUS

This verdict is for the narrowed calibration claim, not for a claim that K=2 is guaranteed to win or that public notebook metadata identifies the leaderboard leader.

### Round-1 issue resolution

1. Public notebook audit overclaim: RESOLVED. V2 states public audit is a mechanism prior only and explicitly does not link it to the live leaderboard leader.
2. K=2 interface freeze: RESOLVED. V2 excludes K=4, slow-row multipost, extra template race, measured dense prefix, and replay-cost multiplier changes.
3. Split-by-latency behavior: RESOLVED. V2 specifies that split switching is disabled for K>1 because the burst message has one frozen shape.
4. `>=100` interpretation: RESOLVED. V2 treats it as a target-owned success bin, not a calibrated public-notebook estimate.
5. Second-event prevalence risk: RESOLVED. V2 promotes this to evidence, rationale, threats, failure modes, and metrics.

### Mechanisms and confounds stress-tested

- Mechanism: candidate-internal post cardinality is the only intended active change. PASS.
- Mechanism: K=1 byte-equivalence is required as a local gate. PASS.
- Mechanism: K=2 keeps the v35 validation-fill/replay-safe loop. PASS.
- Confound: public notebooks may include additional mechanisms. V2 controls by excluding them and using target-owned bins. PASS.
- Confound: remote second-event prevalence is hidden. V2 acknowledges this and makes the target result decisive. PASS.
- Confound: wrapper/CSV errors could mimic mechanism failure. V2 gates on commit-run output/source checks. PASS.
- Confound: replay-cost identifiability remains hidden. V2 avoids a new replay-safety claim and inherits the v35 ledger. PASS WITH LIMITATION.

### Taxonomy verification

The classification `Optimization Bottleneck × Empirical Mapping × replace` is accurate. The hypothesis replaces one local candidate structure under a fixed controller. It is not Bridge × Synthesis because it excludes the obvious public-stack additions.

### Anti-stacking check

Pass.

The hypothesis has one component, a measured competition bottleneck, explicit local ablations, and a target-owned end-to-end result claim. The public audit informs candidate selection but is not imported as a stack of components.

### Occam's Razor

Pass.

K=2-only is the simplest above-ceiling density test after K=4 failures. Testing slow-row Harmony multipost first would be more complex and less attributable.

### Strongest objection considered

The strongest objection is that public high scores, if related to pulled notebooks at all, may depend on `SLOW_MULTIPOST_N=4` or other components rather than `BURST_K=2`.

This objection does not invalidate the v2 hypothesis because v2 no longer claims public code proves the result. It asks a narrower target-owned question: whether isolated K=2 under our restored controller is sufficient. If the omitted components are necessary, the experiment will produce a partial or failure result and still teach us which dimension to attack next.

## Actionable coaching

Implementation should be minimal:

1. Add a `BUNDLE_POSTS` constant.
2. Add a formatter where `K=1` is byte-equivalent to current `_msg`.
3. Route `_emit`, warmup, and fill candidates through the formatter.
4. Disable split-template routing when `K>1`.
5. Keep `_event_count` but retain candidates on `event_count > 0`.
6. Add local checks for K=1 byte equivalence and K=2 serialization/event-count behavior.

Do not add slow-row Harmony multipost or K=4 markers in this iteration.
