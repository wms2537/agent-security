# Stage B Four-Endpoint V36 Submission

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 9 · **Status:** failed

## Context

Report 240 completed local implementation gates for the exact four-endpoint density controller. T118 required a Kaggle commit run, output inspection, and only then a competition submission.

## Content

Kaggle kernel version `36` was pushed and reached `KernelWorkerStatus.COMPLETE`.

Downloaded commit-run artifacts:

- `/tmp/kaggle-v36-output.aj5wSk/attack.py`
- `/tmp/kaggle-v36-output.aj5wSk/submission.csv`
- `/tmp/kaggle-v36-output.aj5wSk/ai-agent-security-attack.log`

The downloaded `attack.py` has a different raw SHA only because the notebook wrapper adds one leading and one trailing newline. Mechanical comparison confirms the source body matches after stripping wrapper newlines.

The code-competition submission was accepted and later completed with no score:

- Submission ref: `55177045`
- Description: `Guarded four-endpoint density rc320 v36`
- Final status: `SubmissionStatus.COMPLETE`
- Public/private score: blank

## Gate Check

- Kernel push: `comp/.venv/bin/kaggle kernels push -p submission/kernel` -> `Kernel version 36 successfully pushed`.
- Kernel status: `comp/.venv/bin/kaggle kernels status whymelabs/ai-agent-security-attack` -> `KernelWorkerStatus.COMPLETE`.
- Output pull: `comp/.venv/bin/kaggle kernels output whymelabs/ai-agent-security-attack -p /tmp/kaggle-v36-output.aj5wSk` -> downloaded `attack.py`, `submission.csv`, and log.
- Submission schema: local CSV checker -> `submission_rows 5`, `submission_header Id,Score`, `submission_empty_cells 0`, `submission_widths 2,2,2,2,2`.
- Source match: source comparison -> `source_strip_match True`, `remote_leading_newline True`, `remote_trailing_newline_count_delta 2`.
- Dense source markers: `rg` over output artifacts -> `DENSE_TARGET_COUNT = 320`, `DENSE_MIN_EVENTS = 4`.
- Submission poll: `comp/.venv/bin/kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v` -> `55177045,submission.csv,2026-08-02 04:08:21.400000,Guarded four-endpoint density rc320 v36,SubmissionStatus.PENDING,,`
- Final submission poll: `comp/.venv/bin/kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v` -> `55177045,submission.csv,2026-08-02 04:08:21.400000,Guarded four-endpoint density rc320 v36,SubmissionStatus.COMPLETE,,`

## Problem alignment

This is a live target measurement showing that blind rc320 four-endpoint density crosses a hidden rerun/runtime/replay boundary even though local mechanics and commit-run schema pass.

## Decision

Record v36 as a failed blind dense branch. Disable blind dense emission as the active default before any new push. Any future density attempt must be validation-fill/resource-measured rather than probe-then-blind-emit.
