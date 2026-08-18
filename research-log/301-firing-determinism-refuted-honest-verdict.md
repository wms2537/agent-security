# Firing determinism refuted; honest final verdict on the frontier gap

Date: 2026-08-18

## Test

Mirror the gateway replay (fresh env per candidate, seed 123, public guardrail,
8 hops, temp 0) on real gpt-oss:
- SAME candidate x10: fired 10/10, exactly 1 post each.
- 6 distinct candidates: fired 6/6.

## Conclusion: log 300's firing-consistency hypothesis is WRONG

Firing is perfectly deterministic and 100% consistent. Root cause confirmed in
code: generation_kwargs {"do_sample": False} -> temperature 0.0 (greedy);
SandboxEnv.reset() fully clears history/guardrail/agent and re-seeds to 123 --
identical to the fresh env used in replay; both generation and replay use
ATTACK_SEED=123. So a validated-firing candidate fires identically in replay.
There is NO firing loss and NO llama.cpp CPU non-determinism here.

Therefore we are NOT leaving replay budget to firing waste. We return ~835 (gpt)
/ ~930 (gemma) candidates, ALL fire, and that is the full replay budget at this
CPU's per-candidate cost. We are genuinely replay-bound with 100% efficiency.

## Every hypothesis now refuted with ground truth

| hypothesis | verdict |
|---|---|
| faster/shorter candidate | refuted (current frame is fastest, ~6s floor) |
| reasoning suppression | refuted (all injections slower) |
| density / multi-post | refuted (single-post 2.61 raw/s optimal) |
| multi-predicate | guardrail-blocked |
| hop-1 / cheaper validation | replay-bound (v45) |
| firing consistency | refuted (100% deterministic) |
| generation inefficiency | refuted (replay-bound, full budget) |
| scoring aggregation wrong | refuted (diagnostic confirmed 835/930) |

## Honest verdict

The frontier (~1267 findings/row) returns ~30% more scored candidates than we do
for the SAME single-post primitive, on the SAME fixed replay budget and CPU. Under
everything I can measure -- confirmed scoring model, proven per-candidate replay
floor, 100% deterministic firing, full budget use -- this SHOULD be impossible.
That it is not means one of these, none reproducible from my position:

1. The leaders use a candidate that genuinely replays faster in a way my
   exhaustive real-model tests did not find.
2. The effective replay budget / cap differs from the local SDK copy (DEFAULT
   9000s; the public 0-second-bypass video cited 1800s -- a mismatch I could not
   reconcile).
3. An unpublished mechanism.

I cannot honestly claim to know how they do it. I have rigorously ruled out every
mechanism testable from here. 87.255 is our genuine, fully-efficient result for
the single-post primitive; the frontier's edge is outside what the SDK copy,
public notebooks, the paper, the video, the real-model CPU harness, and the
row-isolation diagnostics reveal.

## State

Active kernel = v42, standing 87.255. Investigation exhausted.
