# T078 — SCOC-32 periodic-anchor holdout results

**Date:** 2026-07-23 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 5 · **Status:** completed

## Context
T078 requested a new `scoc_anchor4` branch (`scoc_anchor_period=4`) to test whether periodic exact anchors recover long-chain continuation gains before any Kaggle decision.

## Content
Implemented branch was already wired into `AttackConfig` and `scoc32_holdout_matrix.py` and registered as six rows in `results.tsv` before execution.

## Gate Check
Executed:
`PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/scoc32_holdout_matrix.py --out-dir artifacts/scoc32/run14`
- `run14` completed with `EXIT:0`.
- Registry payload reports 30 rows written, including six `scoc_anchor4` rows.
- `WROTE payload 30 rows ...` and `results payload path results.tsv` both appeared in `artifacts/scoc32/run14/run.log`.

## Problem alignment
This run tests a narrow SCOC-32 mechanism refinement (`scoc_anchor_period`) while preserving the same budget envelope, budget-safe objective, and non-attributed local-only evaluation gate.

## Decision
Prediction was pre-registered as no change versus the holdout baseline (`23.28` for compliant-zero overhead, `2.16` for context-limited-8).

**Prediction vs. reality**
- `scoc_anchor4` in `run14` matched baseline predictions on all 6 runs:
  - compliant-zero-overhead seeds 42/777/2026: `23.279999999999998`
  - context_limited_8 seeds 42/777/2026: `2.16`
- No run exceeded baseline; `scoc_anchor4` is not a winning holdout improvement.

## Next Steps
Mark T078 as completed but the branch is exploratory-only; carry forward SCOC32 development by testing either (a) alternative anchor schedules under the same budget constraints or (b) a non-anchor continuation mechanism and compare by `heldout` gain against the same `scoc_off/scoc_default/scoc_probe12/scoc_long_fill` slice.
