# Stage B Four-Endpoint V36 Submission

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 9 · **Status:** in-progress

## Context

Report 240 completed local implementation gates for the exact four-endpoint density controller. T118 required a Kaggle commit run, output inspection, and only then a competition submission.

## Content

Kaggle kernel version `36` was pushed and reached `KernelWorkerStatus.COMPLETE`.

Downloaded commit-run artifacts:

- `/tmp/kaggle-v36-output.aj5wSk/attack.py`
- `/tmp/kaggle-v36-output.aj5wSk/submission.csv`
- `/tmp/kaggle-v36-output.aj5wSk/ai-agent-security-attack.log`

The downloaded `attack.py` has a different raw SHA only because the notebook wrapper adds one leading and one trailing newline. Mechanical comparison confirms the source body matches after stripping wrapper newlines.

The code-competition submission was accepted:

- Submission ref: `55177045`
- Description: `Guarded four-endpoint density rc320 v36`
- Status at first poll: `SubmissionStatus.PENDING`

## Gate Check

- Kernel push: `comp/.venv/bin/kaggle kernels push -p submission/kernel` -> `Kernel version 36 successfully pushed`.
- Kernel status: `comp/.venv/bin/kaggle kernels status whymelabs/ai-agent-security-attack` -> `KernelWorkerStatus.COMPLETE`.
- Output pull: `comp/.venv/bin/kaggle kernels output whymelabs/ai-agent-security-attack -p /tmp/kaggle-v36-output.aj5wSk` -> downloaded `attack.py`, `submission.csv`, and log.
- Submission schema: local CSV checker -> `submission_rows 5`, `submission_header Id,Score`, `submission_empty_cells 0`, `submission_widths 2,2,2,2,2`.
- Source match: source comparison -> `source_strip_match True`, `remote_leading_newline True`, `remote_trailing_newline_count_delta 2`.
- Dense source markers: `rg` over output artifacts -> `DENSE_TARGET_COUNT = 320`, `DENSE_MIN_EVENTS = 4`.
- Submission poll: `comp/.venv/bin/kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v` -> `55177045,submission.csv,2026-08-02 04:08:21.400000,Guarded four-endpoint density rc320 v36,SubmissionStatus.PENDING,,`

## Problem alignment

This is a live target measurement of the exact density mechanism needed to move beyond the v35 single-post floor and toward public scores above `100`.

## Decision

Wait for ref `55177045` to finish, then update `results.tsv`, `competition/leaderboard_experiments.tsv`, `state.json`, and the search decision.
