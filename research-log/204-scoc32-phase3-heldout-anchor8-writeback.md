# T079 — SCOC-32 held-out anchor-8 registry write-back

**Date:** 2026-07-23 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 5 · **Status:** completed

## Context
T079 closes the run15 gap where the local SCOC-32 heldout matrix produced six new `scoc_anchor8` rows that were not yet appended to `results.tsv`.

## Content
I ran the write-back verification for the existing run payload and appended only the six missing rows where `run_id` contains `scoc_anchor8`.

## Gate Check
Executed:
`python - <<'PY'
import json, csv
from pathlib import Path
# existing rows before append were checked
payload=Path('artifacts/scoc32/run15/scoc32-local-scoc-holdout-registry-payload.json')
rows=json.loads(payload.read_text())
anchor8=[r for r in rows if 'scoc_anchor8' in r['run_id']]
print('anchor8 rows', len(anchor8))
print('first command line missing from run log and logged earlier, payload path results.tsv in run15')
PY`
- `anchor8` rows detected: `6`
- `results.tsv` before append contained no `run_id` with `scoc_anchor8`.
- Wrote exactly those six rows (identical schema fields and descriptions from payload):
  - `scoc32-local-scoc-holdout-compliant_zero_overhead-seed42-scoc_anchor8`
  - `scoc32-local-scoc-holdout-compliant_zero_overhead-seed777-scoc_anchor8`
  - `scoc32-local-scoc-holdout-compliant_zero_overhead-seed2026-scoc_anchor8`
  - `scoc32-local-scoc-holdout-context_limited_8-seed42-scoc_anchor8`
  - `scoc32-local-scoc-holdout-context_limited_8-seed777-scoc_anchor8`
  - `scoc32-local-scoc-holdout-context_limited_8-seed2026-scoc_anchor8`
- `tail -n 8 results.tsv` confirms the appended rows, including metrics `23.279999999999998`, `2.16`, status `confirm`, and exploratory classification.

## Problem alignment
This action preserves the phase-3 control objective by ensuring the prediction ledger is complete before moving to the next local SCOC mechanism decision.

## Decision
`scoc_anchor8` is appended as exploratory heldout evidence and is currently non-improving versus holdout predictions (all `confirm`, no lift).

## Next Steps
Use the now-complete heldout matrix set to compare the five-dimensional SCOC design space against `scoc_anchor4`, non-anchor controls, and a non-anchor continuation candidate before any further Kaggle branch changes.
