# max_new_tokens sweep: replay cost is FIXED per-candidate overhead, not tokens

Date: 2026-08-19

User asked to try a faster candidate with fewer max tokens.

## Two blockers found

1. The replay's `max_new_tokens` is FIXED at 1024 by the gateway model server
   (`GgufModelSpec.max_new_tokens = 1024`, gpt_oss/gemma model servers). The
   attack side CANNOT set it -- it is not passed from the candidate or
   AttackRunConfig; HFBackendConfig is frozen and the spec owns it.

2. Even if we could, it does not help. Real gpt-oss replay (hop-8), 3 trials:

   | max_new_tokens | median replay | fired |
   |---|---|---|
   | 32  | 6.51s | 3/3 |
   | 64  | 6.29s | 3/3 |
   | 128 | 6.15s | 3/3 |
   | 256 | 5.75s | 3/3 |

   FLAT (~5.75-6.51s) across an 8x token range -- if anything it drops slightly
   with more tokens (noise). Output token count does NOT drive replay time.

## Conclusion

Per-candidate replay cost is dominated by FIXED overhead -- prompt prefill + the
two model generation turns (tool call + forced final response) + env / guardrail /
tool execution -- not by how many tokens the model emits. This is why every
"faster/terser candidate" attempt failed (reasoning suppression, wording,
prefill): there are no cuttable tokens to cut; the cost is structural.

The ~6s (my box) / ~9-10s (competition) per-candidate replay is an immovable
floor. Combined with the budget probe (replay-time-bound, zero headroom), the
frontier's ~30% more findings/row cannot come from a faster candidate on our side.

## State

Active kernel = v42, standing 87.255. "Fewer max tokens" refuted on both axes
(not settable; and flat anyway). Replay floor confirmed structural.
