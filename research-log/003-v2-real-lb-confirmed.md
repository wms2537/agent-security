# v2 real LB confirmed: 36.7 → 69.6

**Date:** 2026-07-18 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 2 · **Status:** completed

## Result
| Submission | Approach | Public LB |
|---|---|---|
| v1 (05:37) | multi-post-8 EXFIL + 22% CONFUSED_DEPUTY reserve + hedges | **36.705** |
| v2 (12:49) | single-post EXFIL, per-model raw/s selection, verified fill, void-safe 0.90 | **69.570** |

**+89% (nearly 2×)**, bottom-of-board → mid-pack. Top of leaderboard ≈ 103.67.

## What this confirms (the root-cause thesis held)
The four fixes from `002-rootcause-and-rebuild.md` were correct in aggregate:
1. **Optimize the 4-cell mean, not one compliant-mock cell.** The 198.6 mock number
   was never the score; the LB is the mean of four independently-capped cells.
2. **N is latency-bound, so single-post > multi-post.** Dropping multi-post-8 for
   single clean posts raised the number of firing candidates per cell.
3. **Cut the ~28% dead budget** (CONFUSED_DEPUTY/hedge/launder that fire ≈0 on the
   real models); exfil already reaches the private cells (user-originated payload).
4. **Per-model phrasing** (harmony for gpt-oss selected by raw/s; JSON envelope
   available for gemma) instead of gpt-oss-only templates.

## Gap analysis — 69.6 vs top 103.7 (next levers)
69.6 as a 4-cell mean ⇒ ~278 raw-equivalent across cells. To close the ~34-point
gap, the remaining lever is the same one that matters most: **more verified-firing
candidates per cell = lower per-candidate replay latency + higher real fire-rate.**
Unknowns we could not measure offline (no GPU) that the real run now gives signal on:
- **Which template actually won per model, and its measured latency/fire-rate.** The
  kernel log prints `[attack] selected=… raw/s=… unit=…s returned=…`; pull the v2 run
  log to read the real per-model selection and candidate counts (T002).
- **Whether the private cells fired** (they must, for 69.6 to be a 4-cell mean — an
  all-public-only mean would be ~46, so private is contributing). Confirms the
  user-originated-payload transfer thesis; a per-cell breakdown would quantify it.
- **Void margin.** v2 did NOT void (COMPLETE), so 0.90 REPLAY_SAFE was safe; there may
  be room to push toward 0.95 for more N — but only after reading the real latency.

## Decision
v2 is the new baseline. Next iteration is data-driven off the v2 kernel log: read the
real per-model `selected`/`unit`/`returned`, then (a) trim the template bank to the
proven winners to cut probe cost, (b) consider a modestly higher REPLAY_SAFE, and
(c) attack latency directly (shorter CoT-collapsing forms) to raise N.
