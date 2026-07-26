# T078 — SCOC-32 periodic-anchor continuation stress test

## Date
2026-07-23

## Phase / Cycle / Iteration
P3 / 3 / 5/5

## Context
SCOC-32 currently has no confirmed local gain versus the incumbent single-post/multi controls. The only remaining local gap is whether long-context candidate success can be stabilized with a periodic anchor refresh while preserving the continuation-dominant structure. The mechanism hypothesis here is narrow:

- `scoc_anchor_period=4` should keep context anchored sufficiently often to preserve execution in longer chains under reset-only execution,
- without introducing enough overhead to erase the raw-per-second advantage.

## Planned run (pre-registered)
- Add a periodic anchor parameter to SCOC continuation synthesis (`AttackConfig.scoc_anchor_period`), and validate with the existing local holdout scaffold.
- Reuse `ATTACK_CONFIG_BASE` settings and only add `scoc_anchor_period=4` in the new tag.
- Record results as exploratory and compare against `run11` baseline holdout rows.

## Predicted runs
Expected baseline-comparison predictions (6-row heldout matrix slice):

- `scoc32-local-scoc-holdout-compliant_zero_overhead-seed{42,777,2026}-scoc_anchor4`: `predicted_value=23.28`
- `scoc32-local-scoc-holdout-context_limited_8-seed{42,777,2026}-scoc_anchor4`: `predicted_value=2.16`

Each row is pre-registered in `results.tsv` as `exploratory` before execution.
