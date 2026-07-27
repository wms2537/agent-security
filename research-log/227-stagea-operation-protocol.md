# Stage A Operations Protocol — "Do It Properly" Playbook

**Date:** 2026-07-28  
**Phase:** Stage A recovery (competition-facing)  
**Scope:** repository-side validation, evidence logging, and controlled submission policy

## What we found this cycle

- `submission/build_notebook.py` currently:
  - writes a valid 5-row placeholder `submission.csv`,
  - validates row count and IDs,
  - runs the local inference server in a try/except guard, and
  - on exception writes a schema-valid fallback CSV + `result.json`.
- The five latest Stage-A submissions (`55002770`, `55018092`, `55024720`, `55025140`, `55028345`) are all `SubmissionStatus.COMPLETE` with empty `publicScore` and `privateScore`.
- Kaggle CLI replay telemetry is still limited for this branch (`No episodes found` in the current command path), so root-cause of the blank outcome is not directly visible.
- The local command `python -m py_compile ...` and `python submission/build_notebook.py` currently pass.
- The current kernel/output sanity pass still shows the expected local artifact files and no traceback in commit-run logs.

## Direct answer: submission.csv vs other parts

Current evidence says the issue is **not** a plain `submission.csv` schema regression.
It is currently most consistent with a **rerun/runtime-level failure class** outside the commit artifact shape that we can currently observe from local commands.

In practical terms:

- Keep `submission.csv` schema/serialization checks as-is.
- Stop spending cycles on repeated local CSV rewrites.
- Shift effort to controlled comparison submissions and strict attribution logic.

## Proper execution protocol (non-negotiable)

Before any interpretation, every next submission batch must pass all gates:

1. **Static checks**
   - `python -m py_compile experiments/attack.py submission/build_notebook.py`
   - `python submission/build_notebook.py`
2. **Build validation**
   - Confirm generated notebook artifacts exist:
     - `submission/kaggle_notebook.ipynb`
     - `submission/kernel/kaggle_notebook.ipynb`
   - Confirm build prints "attack.py parses OK".
3. **Commit artifacts**
   - Ensure Git working tree has the intended source only.
   - Push/commit and record kernel/ref hashes in the run ledger.
4. **Kaggle commitment is measurement only**
   - Commit-run success is required but is **not** score attribution evidence.
5. **Two-point live comparison batch**
   - Submit:
     - A) a known-good historical control reference
     - B) current Stage-A control
   - Record both results in `competition/leaderboard_experiments.tsv`.
6. **Interpretation rule**
   - If A and B both fail with shared blank outcomes, pause attack changes and treat this as a shared runtime/telemetry path blocker.
   - Only if B fails while A scores should attack logic be treated as the likely cause.
7. **No blind changes after failure**
   - Do not alter attack structure until the above decision point is reached.

## Current decision state

- `competition/source_contract.md` and `research-log/224` already encode the two-point comparison gate.
- Current evidence should be interpreted as:
  - **format integrity checkpoint = passing**
  - **rerun outcome = unresolved**
  - **next useful action = controlled batch comparison**

## Files to touch in every Stage-A controlled cycle

- `competition/source_contract.md` (submission gate)
- `research-log/224-stagea-submission-confidence-checklist.md` (gates + decision)
- `research-log/225/226` (failure evidence as it accrues)
- `competition/leaderboard_experiments.tsv` (single row per submission variable change)
- `research-log/progress.md` (one-line progress row for each control/submission milestone)

