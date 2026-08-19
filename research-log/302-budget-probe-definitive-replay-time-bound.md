# Budget probe definitive: replay-time-bound, adaptive optimal, zero headroom

Date: 2026-08-19

## Result

v48 blind-emit 1250/row (no validation, deterministic firing) = **81.810**.
- ~1818 total findings -> ~909/row.
- Adaptive v42 = 87.255 -> ~970/row.
- Blind emitted 1250/row but only ~909 SCORED -> replay is TIME-bound and the
  gateway scores PARTIAL (replays until deadline, scores what completes; NO blank).
- **Adaptive (87.255) BEATS blind (81.810).** Emitting more scored fewer.

## Definitive conclusions

1. **Zero budget headroom.** Adaptive validation-fill already uses the full replay
   time budget and is OPTIMAL. The "adaptive under-fills due to gRPC-inflated cost
   estimate" hypothesis is refuted -- blind (which skips validation) scored LOWER.
2. **Replay is TIME-bound at ~970/row**, and over-emitting does not help (scores
   partial ~909/row).
3. **New fact:** over-emitting count does NOT blank -- it scores partial. So the
   earlier blanks (v36 K=4, v38 K=2, v44 multipost) were per-candidate DENSITY
   failures, not count/budget overflow.

## Final answer to "how do others score ~114 (1267/row)?"

They replay ~30% MORE candidates in the SAME fixed replay-time budget. That
requires each candidate to replay ~30% FASTER (~7.1s vs our ~9.3s). Same
candidate + same CPU = same speed, so their edge is a genuinely FASTER-REPLAYING
candidate (or different CPU allocation). We have exhaustively proven no faster
single-post candidate exists (density, wording, reasoning-suppression, hop-1,
harmony variants all refuted on the real models). And it is NOT: budget headroom
(this probe), firing loss (deterministic 100%), a better fill strategy (adaptive
beats blind), or a scoring misread (diagnostic confirmed).

So the frontier's advantage is a faster-replay mechanism not reproducible from the
SDK copy, public notebooks, the paper, the 0-second video, the real-model CPU
harness, or any probe. 87.255 is our genuine, fully-budget-utilized optimum.

## State

Active kernel = v42 (BLIND_COUNT=0), standing 87.255. Investigation definitively
closed on every accessible axis.
