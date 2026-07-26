# T074 — SCOC-32 held-out long-horizon continuation matrix

**Date:** 2026-07-23 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 5/5 · **Status:** completed

## Context

After T070-T073, the next readiness check was a held-out continuation matrix under the fixed `scoc` variants, three representative seeds, and the two SCOC profiles that mattered most for Phase-3 prediction stability:

- `compliant_zero_overhead`
- `context_limited_8`

## Pre-registered expectation

The SCOC-32 hypothesis predicted base local normalized score at fixed budget:

- `compliant_zero_overhead`: 23.28 per row
- `context_limited_8`: 2.16 per row

The run was registered as a fixed 24-row run-set and no changes were made to `results.tsv` until payload capture completed.

## Commands run

- `comp/.venv/bin/python experiments/scoc32_holdout_matrix.py --out-dir artifacts/scoc32/run10`
- `cat artifacts/scoc32/run10/run.log`
- `cat artifacts/scoc32/run10/scoc32-local-scoc-holdout-matrix.tsv | head`
- `cat artifacts/scoc32/run10/scoc32-local-scoc-holdout-registry-payload.json`

## Evidence

The held-out run produced exactly 24 rows:

- `artifacts/scoc32/run10/scoc32-local-scoc-holdout-matrix.tsv` (24 rows, both scenarios × 3 seeds × 4 tags)
- `artifacts/scoc32/run10/scoc32-local-scoc-holdout-matrix.json` (full row payload)
- `artifacts/scoc32/run10/scoc32-local-scoc-holdout-registry-payload.json` (24 ledger rows)
- `results.tsv` `run_id` matches `scoc32-local-scoc-holdout-*` now include metric/signal/runtime with the observed values.

### Scenario outcome summary

- `compliant_zero_overhead`: 10/12 rows matched 23.279999999999998 exactly; 2/12 rows (`seed=42`, `seed=2026`, `tag=scoc_long_fill`) returned 46.32 (partial signal because pre-registered match target was 23.28).
- `context_limited_8`: all 12 rows confirmed at 2.16.

## Prediction vs. reality

**Prediction (before run):** held-out compliant and context-limited rows should cluster tightly on the respective predicted baselines.

**Reality:** partial confirmation for most compliant rows and one non-trivial class of partial anomalies under `scoc_long_fill`; context-limited rows confirmed cleanly. The anomaly pattern is likely a configuration-specific interaction and should be treated as low-confidence evidence rather than a confirmed gain.

## Decision

T074 is complete and recorded in protocol state. The held-out matrix is useful for narrowing continuation experiments but does not yet justify a direct Kaggle confidence push on this branch without a separate anti-regression run focused on the `scoc_long_fill` path.

## Next steps

- add a one-item diagnostic rerun isolating only `compliant_zero_overhead/scoc_long_fill` at fixed seeds (both SCOC and non-SCOC) to determine whether the 46.32 behavior is deterministic by config,
- keep `results.tsv` ledger entries in-place as exploratory evidence for this run,
- continue Phase-3 mechanics until a robust net-normalized gain profile is shown before any submission attempt.
