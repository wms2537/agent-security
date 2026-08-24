# v59 — M2 inter-message candidate packing canary

Date: 2026-08-24

## Repo hygiene fixes (external review flagged correctly)

- `experiments/attack.py` had been left at the discarded frac 0.9825;
  restored to **0.98** (canonical best config).
- Immutable baseline created: `competition/baselines/v42-87480/`
  (attack.py sha `569c42d3…` + manifest.json, score 87.480, ref 55681594).
- `submission/build_notebook.py` now takes an explicit source path so variant
  experiments never overwrite production (`submission/selected/` convention).
- Kernel re-pushed from canonical source (v59 kernel version).

## Why packing is NOT covered by the multipost refutations

All six prior density failures were INTRA-message: one user instruction asking
the model to execute K posts across hops. Those die on model planning/
continuation (v44: ~2.3/8 posts fired on real GGUF).

INTER-message packing is structurally different and was verified in current
SDK source before spending a submission:

1. `evaluation/ops.py::_replay_candidate_trace`: ONE env reset per candidate,
   then every user message runs sequentially inside it.
2. `scoring.py::score_attack`: predicates sum with NO dedup across events;
   cell bonus (+2) once per finding (uniq_cells is per-finding hash set).
3. Real SDK evaluator (evaluate_redteam + CompliantAgent): an M2 packed
   candidate scores exactly **34.0 raw** (= 16+16+2), confirmed locally.

The July T006 implementation (`_multi_messages`, git e936a2f) validated local
mechanics but was never submitted — it was procedurally abandoned and wrongly
absorbed into "multipost closed". The open question was always real-model
compliance + latency of the second turn, which only the evaluator can answer.

## Canary design (minimal single-variable delta vs v42)

- Base: byte-equivalent v42 behavior everywhere except candidate construction
  after classification completes (n=8 mean, threshold 12s, harmony slow row,
  warmup kept, same templates — no new wording anywhere).
- Packed candidate i = `from_messages((msg_i, msg_i))` — SAME clean domain in
  both turns (cell uniqueness is per-candidate; extra domains buy nothing).
- **Live gate** (per model row, medians of 3 exact-chain probes):
  adopt M2 iff `34/t2_med >= 1.08 * (18/t1_med)` (t2/t1 <= 1.751), requiring
  full compliance (M1 events >= 1, M2 events == 2) on every probe.
- If gate fails on a row: that row runs pure v42. One-row success still lifts
  the mean (~+5% aggregate per +10% single-row).
- Replay accounting: frac **0.96** (conservative first canary); each packed
  candidate charged its measured two-turn elapsed; 3 consecutive mid-run
  packed failures revert the row to singles.
- Ordering: first 12% of replay cap = proven singles (safe prefix under
  partial-score-on-timeout semantics), then packed tail.

## Preregistered thresholds (vs standing best 87.480)

| Score | Decision |
|---|---|
| >= 92 | Structural mechanism confirmed; ladder M3/M4 |
| 89-92 | Useful; decode which row benefited via count arithmetic |
| 87-89 | Near-neutral; try continuation compression (msg2 minimal form) only |
| 84-87 | Probe-to-replay transfer failed; abandon packing permanently |
| < 84 | Implementation/accounting defect; audit before any retry |

Note: if BOTH rows reject the gate, score should land ~= v42-at-0.96 (~86-87)
— that outcome measures the gate's rejection working, not a failure of v42.

Kernel v60 sha `ee5b9fcfd27bf760…`; submit ref `55748321`.
