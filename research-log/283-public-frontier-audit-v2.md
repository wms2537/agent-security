# Public frontier audit v2 — zero-cost, no submission

Date: 2026-08-05

User chose zero-cost research before any further submission. Pulled the live
leaderboard and the top public notebooks via the Kaggle CLI.

## Leaderboard frontier (2026-08-05)

Top public scores: 114.590 (ADARSH REDDY B), 112.165, 111.870, 110.250, ...,
Pilkwang Kim **109.485**. Our standing: v35 = 86.670.

## Top public notebooks vs our v35

Pulled full source of pilkwang / dimong4 / nctuan. All three are the SAME
"break-60" validation-fill family — identical docstring, identical primitive
(one `http.post`, `SECRET_MARKER` -> EXFILTRATION 16 raw + cell +2 = 18
raw/candidate, public score = mean(gpt_oss_public, gemma_public)).

| notebook | delta vs our v35 |
|---|---|
| pilkwang/ai-agent-v3-1-2-single-post-exfiltration | **byte-identical constants** (TEMPLATE, FRAME_TEMPLATE, MARGIN_S=47, REPLAY_SAFE_FRAC=0.97, SPLIT_BY_LATENCY, ...). Author LB=109.485 via a private iteration beyond this public notebook. |
| dimong4/ai-agent-security (top-voted, 220) | `SLOW_MULTIPOST_N=4`, `SPLIT_CLASSIFY_N=5` — K=4 on slow rows (the density we refuted: v36 blank, v37 84.735, v38 blank). |
| nctuan/jed-v25 | `FRAME_TEMPLATE = TEMPLATE` (verbose, not the bare harmony frame) + `REPLAY_SAFE_FRAC = 0.98`. |

## Key conclusions

1. **We are at public parity.** Our v35 == pilkwang's public v3.1.2 exactly. The
   86.670 we score is what this code yields on the current grader. No public
   notebook is the 109 solution; the frontier authors' 109+ are private
   iterations of this same family.

2. **Confirmed lever: verbose frame beats the bare harmony frame on slow rows.**
   The pilkwang docstring states the system is *fire-rate-limited, not
   budget-limited*, and that bare tool-syntax "fires less reliably" than the
   verbose imperative. nctuan operationalizes this: `FRAME_TEMPLATE = TEMPLATE`.
   Our v35 still routes slow gpt_oss rows to the bare `FRAME_TEMPLATE`
   (`http.post url=.. data=..<|end|>...`), and our v39 independently confirmed
   that making the gpt_oss frame *more* bare/structured (commentary prefill)
   tanked to 56.475. Three independent signals point the same way.

3. **Confirmed lever: fill/margin tightening.** Docstring: MARGIN_S is "the
   primary tuning knob"; yusuke laddered 50->45->44->42->37, each tighter rung
   gaining points to the timeout edge. nctuan runs `REPLAY_SAFE_FRAC = 0.98`
   (vs our 0.97). Both widen the returned firing-candidate count.

4. **Density is a dead end, reconfirmed.** dimong4's SLOW_MULTIPOST_N=4 is the
   same K=4 we already refuted; votes != score.

## Realistic path to the frontier

No single public change jumps to 109; the frontier is reached by laddering the
count knobs on the verbose-frame single-post base. Concretely, in priority:

- **E1 (highest EV, grounded):** `FRAME_TEMPLATE = TEMPLATE` — verbose imperative
  on slow rows too. Single variable. Backed by pilkwang's A/B, nctuan's shipped
  config, and our v39 counter-evidence. Expected: higher gpt_oss row -> higher
  mean.
- **E2:** tighten fill by rungs — `REPLAY_SAFE_FRAC 0.97 -> 0.98` (nctuan), later
  `MARGIN_S 47 -> 42 -> 37`. Monotone count gain until the timeout cliff; each
  rung is one submission.

Each experiment is still one ~day-long, quota-costing submission (no local firing
observability), but these are now evidence-grounded monotone probes, not blind
template guesses. Reaching ~109 realistically means several laddered submissions.

## State

No code change or submission in this entry. attack.py remains the v35 floor.
Pulled notebooks saved under `research-log/public-audit-v2/` for reference.

## Recommendation

Proceed E1 first (verbose frame), then ladder E2. Await user go-ahead before the
E1 submission.
