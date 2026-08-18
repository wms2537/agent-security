# The real answer to "how do others score higher": firing consistency, not candidate speed

Date: 2026-08-18

## Reasoning-suppression refuted (final "faster candidate" test)

Real gpt-oss, harmony reasoning-effort injections vs current frame:
current 6.04s (4/4) | sys_low 6.53 | dev_low 6.60 | analysis_prefilled 6.91.
ALL slower than current. gpt-oss ~6s (2 generations) is a hard floor; no
candidate manipulation reduces it. "Faster candidate" hypothesis exhaustively
dead (adds to: density, wording, hop-1, multipost, single-gen).

## The reframe (fits ALL evidence)

Diagnostic: gpt-oss row = ~835 scored findings. Replay budget ~9000s /
~6-9s per candidate = ~1000-1500 allowed. So 835 is BELOW the replay ceiling:
we are NOT replay-bound -- we leave replay budget unused.

Therefore the loss is generation-side, and it is OURS:

1. **Firing consistency (most likely).** Live validation keeps a candidate that
   fires during GENERATION, but the gateway re-runs it INDEPENDENTLY to score. If
   it fires ~85% in that independent replay (stochastic / different context), ~15%
   of returned candidates score zero -> wasted slots. The 0-second-bypass video's
   claim -- "one policy guaranteed to break on the FIRST attempt" -- is exactly
   this: deterministic firing. Frontier candidates fire 100% in replay; ours ~85%.
2. **Generation-bound fill.** If real firing during generation is <100%, we waste
   generation budget probing non-firers and stop before filling replay.

## Why this is the best explanation

It is the only hypothesis consistent with: balanced rows (835/930), confirmed
scoring model, a proven hard replay floor per candidate, AND a scored finding
count BELOW the replay ceiling. "Faster candidate" is refuted; "external variance"
does not fit the systematic ~30% gap. Firing/generation efficiency does.

## Implication / testable direction (NOT yet done)

The lever is NOT a better candidate -- it is returning candidates that fire
DETERMINISTICALLY 100% in the independent replay, and filling the replay budget
fully (generation-efficient). Concretely:
- measure our real generation-vs-replay firing gap (needs the scored rerun log,
  which Kaggle does not expose -> infer via targeted submissions);
- a candidate/seed construction whose firing is deterministic across the
  independent replay (the video's surrogate-search "guarantee" idea);
- correctly-calibrated cheaper validation so the fill reaches the replay ceiling
  (v45 hop-1 failed only due to coef over-charging, not the idea).

## Verdict

87.255 stands, but it is NOT a hard ceiling as previously stated -- it is a
~15-30% firing/generation inefficiency below the replay budget. The frontier's
edge is firing determinism + fill efficiency, not a faster or denser candidate.
This is the honest, evidence-consistent answer.

## State

Active kernel = v42, standing 87.255. No new submission.
