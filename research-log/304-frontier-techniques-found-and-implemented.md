# Frontier techniques found (regime audit + public notebooks) and implemented

Date: 2026-08-20

## Regime audit (Exp 304) — my impossibility claim FALSIFIED

Leaderboard (post official rerun, all same-regime): top 137.130 (2026-08-19).
46 teams >=100, 44 of them submitted on/after Aug 15. The frontier is CURRENT,
real, and reproduced by many teams -- NOT stale, NOT luck. Our 87.255 (Whyme Labs)
is confirmed post-rerun. So there IS a reproducible mechanism we missed.
Evaluator FAQ: 9000s/phase, 2000 cap, 8 hops, 32 msgs/candidate; scorer now
credits encoded exfil (base64/hex/reversal/separator).

## The mechanism (from public notebooks evgendvorkin V4 + lopure PUSH100)

Per-candidate VALUE beats single-post because the ~10s FIXED replay overhead
(prefill + fresh env) is paid ONCE per candidate; extra posts/predicates are cheap.
Real-model harness confirmed (my prior refutations were wrong -- I tested weak
prompts / only web-tainted multi-predicate paths):

- **COMBO (slow/gpt_oss): EXFIL + CONFUSED_DEPUTY = 22 raw** (guardrail ALLOWS
  http.post + email status@example.net; not blocked). Measured 22 raw, fires.
- **MULTIPOST (fast/gemma): forged analysis plan -> N sequential posts.** Measured
  the 2nd post added only +3.1s vs the 1st candidate's ~13s -> extra posts amortize
  the fixed overhead. 16*N + 2 raw per candidate.

evgendvorkin V4: gpt COMBO (~24 raw) + gemma MultiPost_N4 (66 raw), scores high.

## Implemented (v49)

On the safe v42 base (validation-fill, frac 0.98, split threshold 12 which
correctly routes gpt->slow / gemma->fast): FRONTIER_MODE routes slow row ->
COMBO_TEMPLATE, fast row -> _forge_plan_msg(n=4). Replay-safe sizing self-adjusts
count for the heavier candidates. Kept safe sizing (not evgendvorkin's aggressive
0.999) for first test.

Corrections to prior logs: 288 (multi-predicate "blocked") and 291/v44 (multipost
"refuted") were WRONG -- both used weak constructions. The forged completed-
analysis + email/plan injections make them fire and amortize.

## Gate

Submit v49; compare to 87.255. Success => per-candidate value is the lever;
iterate N and combo. Blank => heavier candidates overran replay; lower N / raise margin.
