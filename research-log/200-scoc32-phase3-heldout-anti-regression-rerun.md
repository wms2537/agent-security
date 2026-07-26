# T075 — SCOC-32 held-out anti-regression rerun for `scoc_long_fill`

**Date:** 2026-07-23 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 5/5 · **Status:** completed

## Context

`T074` recorded a `46.32` spike in `run10` for two `compliant_zero_overhead/scoc_long_fill` rows (`seed=42`, `seed=2026`).

After that, `results.tsv` now contains updated `run11` rows for all `scoc32-local-scoc-holdout-*` entries with all values corrected to the expected regime.
To remove ambiguity between a cached/artefactual effect and a real run effect, I ran an explicit anti-regression rerun in a separate directory with a clean command-first provenance log.

## Command run

- `printf 'CMD: PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/scoc32_holdout_matrix.py --out-dir artifacts/scoc32/run12' > artifacts/scoc32/run12/run.log`
- `{ PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/scoc32_holdout_matrix.py --out-dir artifacts/scoc32/run12 >> artifacts/scoc32/run12/run.log 2>&1; echo \"EXIT:$?\" >> artifacts/scoc32/run12/run.log; }`

## Evidence

- `cat artifacts/scoc32/run12/run.log` shows a valid first line and successful completion (`EXIT:0`).
- `jq length artifacts/scoc32/run12/scoc32-local-scoc-holdout-registry-payload.json` returned `24`.
- Payload metric-value counts are exactly: `23.279999999999998` (12 rows) and `2.16` (12 rows).
- `scoc_long_fill` payload values are only `2.16` and `23.279999999999998` (no `46.32`), and all 24 rows have `signal=confirm`.
- The run has the same mechanism scenarios (`compliant_zero_overhead` and `context_limited_8`) and tags (`scoc_off`, `scoc_default`, `scoc_probe12`, `scoc_long_fill`) as T074 for strict comparability.

## Problem alignment

This closes the only known local anomaly blocking the Phase-3 interpretation and keeps the branch in the SCOC contribution scope with full coverage accounting, instead of retreating on noisy payload artifacts.

## Decision

T075 is complete. `scoc_long_fill` is not a sustained failure mode under the current harness revision; the `46.32` behavior is interpreted as stale run-level artefact rather than a replicable anti-contribution.
The practical next step is a confidence-oriented Kaggle check using the current SCOC implementation rather than further synthetic anomaly chases.

## Next steps

- Proceed with a fast confidence gate: local notebook rebuild + Kaggle confidence run using current SCOC branch settings.
- Record any public scoring change only if runtime/return telemetry confirms source-compatible mechanism behavior for the same run directory family.
