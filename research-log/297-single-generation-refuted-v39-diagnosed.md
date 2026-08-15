# Single-generation / reasoning-suppression lever refuted; v39 crash diagnosed

Date: 2026-08-15

Pursued open-question item 2 (log 296): can a candidate fire in fewer/cheaper
model generations to halve replay cost?

## Env loop fact

`SandboxEnv.interact`: each `next_action` is one model generation; a
ToolCallDecision ALWAYS triggers another generation (loop only stops on
FinalResponseDecision or hop limit). So single-post = 2 generations minimum
(tool call, then final response). Cannot be reduced to 1 by candidate wording.

## Real gpt-oss replay measurement (hop-8, 4 trials)

| variant | median replay | fired |
|---|---|---|
| current_frame (v42) | ~6.5s (noisy 6-14) | 4/4 |
| commentary_prefill (v39) | 24.85s | 4/4 |
| analysis_closed | ~7.0s | 4/4 |
| reasoning_low | 6.81s | 4/4 |

## Conclusions

1. Reasoning-suppression injections do NOT reduce replay time; gpt-oss runs ~2
   generations of analysis+output regardless. current_frame is near-optimal.
2. **v39 (56.475) diagnosed**: commentary-channel prefill is 3.3x SLOWER
   (24.85s vs 6.5s) -> returned ~1/3 the candidates. v39 failed on replay SPEED,
   not firing (fired 4/4). The harmony analysis-channel frame is fastest.
3. Single-generation lever closed. Per-candidate replay ~6.5s (gpt) / ~8.5s
   (gemma) is a floor for single-post; cannot be reduced.

## Remaining open question (still unresolved)

The 970 (ours) vs ~1267 (frontier) findings/row gap for the same single-post
candidate is NOT explained by any candidate-level mechanism now tested (density,
multipost, frame, wording, reasoning-suppression, single-gen all closed). The
gap must lie in one of:

- **Scoring aggregation I have not verified** (public score may not be
  mean-of-2-public-rows x 18 raw/finding). Cannot verify offline without the live
  Kaggle metric definition.
- **Real-competition firing rate < 100%** making the fill GENERATION-bound (higher
  firing -> more fired candidates before the generation wall). Our box shows ~100%
  single-post firing, but hidden eval cells may differ. If generation-bound, a
  properly-calibrated cheaper validation (hop-1 WITHOUT over-charging, unlike v45)
  or a higher-firing candidate would help.
- Unpublished mechanism / CPU allocation.

## State

attack.py = v42 (87.255). Single-generation lever refuted; no code change.
