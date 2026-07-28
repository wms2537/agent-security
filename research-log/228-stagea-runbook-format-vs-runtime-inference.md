# Stage A Runbook: Format vs Runtime Failure Inference (July 28, 2026)

## What we verified

- `submission/build_notebook.py` currently writes a 5-row placeholder `submission.csv` and validates it before and after server start:
  - `Id,Score`
  - `gpt_oss_public,0.0`
  - `gpt_oss_private,0.0`
  - `gemma_public,0.0`
  - `gemma_private,0.0`
- `python -m py_compile experiments/attack.py submission/build_notebook.py` passes.
- `PYTHONPATH=comp/sdk comp/.venv/bin/python -m aicomp_sdk.cli.main validate redteam experiments/attack.py` passes.
- Kaggle kernel commit output (`kaggle kernels output ...`) is clean for versioned runs:
  - `attack.py`, placeholder `submission.csv`, and log all present.
  - No startup/import traceback in commit-run log.
- `submission/kernel` is committed and pushed; recent refs are:
  - `55002770`, `55018092`, `55024720`, `55025140`, `55028345`.
- All these refs now show:
  - `SubmissionStatus.COMPLETE`
  - empty `publicScore` and `privateScore`.
- `kaggle competitions episodes <ref>` remains unhelpful (`No episodes found`) for this branch.

## What this means

The error pattern is no longer consistent with a plain `submission.csv` schema regression.

Interpretation:

- `submission.csv` formatting is likely correct.
- The failure is likely in the rerun/evaluation runtime path or platform-level runtime compatibility, not in placeholder CSV shape.
- We should not spend cycles adding further CSV rewrites unless a new, direct rerun failure signal appears.

## Execution rule (non-negotiable)

Before any further Kaggle iteration:

1. Static + build checks pass.
2. Controlled two-point comparison is submitted in one batch:
   - historical control reference,
   - current Stage-A control.
3. If both fail with blank scores, treat as shared runtime blocker and pause attack changes.
4. Resume only if control and Stage-A diverge as expected.

## Status class for current thread

- Decision after evidence: **format is no longer primary issue**
- Primary working class: **rerun/runtime incompatibility investigation**
- Next action: keep mechanism changes frozen and execute only the next approved controlled comparison batch when/if the user requests.
