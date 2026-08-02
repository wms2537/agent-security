# V36 Failure Analysis

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 9 · **Status:** completed

## Context

V36 tested `DENSE_TARGET_COUNT = 320` exact single-message four-endpoint candidates. Local SDK mechanics proved one candidate could produce four EXFILTRATION predicates and raw score `66.0`, and the Kaggle commit run produced a schema-valid placeholder submission.

## Content

The live submission completed with blank public/private score:

- Submission ref: `55177045`
- Final status: `SubmissionStatus.COMPLETE`
- Public score: blank
- Private score: blank

This is not a local `submission.csv` schema issue. The commit-run artifact passed:

- five CSV rows;
- `Id,Score` header;
- no empty cells;
- source body matching after the notebook wrapper's known leading/trailing newline normalization;
- dense constants present;
- no traceback in the visible commit-run log.

The failure is therefore attributed to the hidden competition rerun path. The most likely cause is that the dense branch was admitted remotely and returned 320 blind four-endpoint candidates, then replay/runtime crossed a hidden boundary. If the dense branch had not admitted, the v35 fallback should have produced a visible high-80s score.

## Gate Check

- Final status evidence: `comp/.venv/bin/kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v` -> `55177045,submission.csv,2026-08-02 04:08:21.400000,Guarded four-endpoint density rc320 v36,SubmissionStatus.COMPLETE,,`
- Prior clean commit-run evidence: report 241 records `submission_rows 5`, `submission_header Id,Score`, `submission_empty_cells 0`, `source_strip_match True`, and dense markers.
- Current public notebook audit: `kaggle kernels list --competition ai-agent-security-multi-step-tool-attacks --sort-by scoreDescending --page-size 10 --format json` returned the same public high-80 family; pulled `nctuan/jed-v25` has `BURST_K = 1`, `SLOW_MULTIPOST_N = 1`, and only overrides `FRAME_TEMPLATE` plus `REPLAY_SAFE_FRAC`.

## Problem alignment

This prevents repeating a known blanking branch and narrows the above-floor mechanism: density must be resource-measured during fill, not admitted once and emitted blindly.

## Decision

Refute blind four-endpoint rc320. Restore the active default to the v35 validation-fill floor before any further Kaggle push. The next density repair, if attempted, must be a validation-fill density controller that charges exact dense-candidate elapsed cost and only keeps fired candidates.
