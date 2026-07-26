# Stage A Kaggle Kernel Version 10 Completion

**Date:** 2026-07-26 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 7 · **Status:** completed

## Context

Report 222 preregistered the Stage A fixed-count single-post kernel. The confidence gate allows Kaggle pushes and commit runs as measurement actions, but competition submission remains held until committed evidence supports it.

## Content

Kaggle kernel version 10 was pushed from `submission/kernel` after commit `fff6124`.

Bound files:

- `experiments/attack.py` SHA-256: `1fd0bae4c668a5d9e9cd403a9941e8ef97a0a98d9ad49b66e014b42dc5465248`
- `submission/kernel/kaggle_notebook.ipynb` SHA-256: `9ea1ae68a031f1bca215df12524ba3df6f137cad7f956bbaa9b3680661753730`
- `submission/kernel/kernel-metadata.json` SHA-256: `5a2e616ac2f559e6ead0a3d1590c3c3a33ea8ee6b389dc2ecd88ad4e04b5728f`

The push is an execution check only. No competition submission has been made for Stage A.

## Gate Check

- Push: `comp/.venv/bin/kaggle kernels push -p submission/kernel` returned `Kernel version 10 successfully pushed`.
- Status check 1: `comp/.venv/bin/kaggle kernels status whymelabs/ai-agent-security-attack` returned `KernelWorkerStatus.RUNNING`.
- Status check 2: `comp/.venv/bin/kaggle kernels status whymelabs/ai-agent-security-attack` returned `KernelWorkerStatus.RUNNING`.
- Status check 3: `comp/.venv/bin/kaggle kernels status whymelabs/ai-agent-security-attack` returned `KernelWorkerStatus.COMPLETE`.
- Output command: `comp/.venv/bin/kaggle kernels output whymelabs/ai-agent-security-attack -p /tmp/stagea-v10-output --force` downloaded:
  - `/tmp/stagea-v10-output/attack.py`
  - `/tmp/stagea-v10-output/submission.csv`
  - `/tmp/stagea-v10-output/ai-agent-security-attack.log`

## Version 10 Evidence

- `attack.py` is clean and contains the Stage A three-arm policy only.
- `ai-agent-security-attack.log` has no exception or traceback and no runtime failure marker.
- `submission.csv` is the scaffold placeholder (`Id,Score` rows with zeros), which is expected for a commit-run; no submission scoring occurs in this output channel.

## Problem alignment

This confirms the committed Stage A kernel asset executes in Kaggle commit-run mode and supports the next confidence step: controlled competition submission of version 10.

## Decision

Competition submission was not made in this step by design. The next step is a controlled leaderboard submission of version 10 once a confidence checklist is captured.

## Next Steps

1. Write the submission-confidence checklist.
2. Submit version 10 with a narrow, preregistered message only if the checklist is complete.
3. Poll leaderboard submission result and update `competition/leaderboard_experiments.tsv` + `results.tsv`.
