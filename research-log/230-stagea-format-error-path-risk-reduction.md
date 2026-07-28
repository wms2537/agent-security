# Stage A submission-format root-cause audit (2026-07-28)

Scope: compare `31b46a8` (lb-81.225 baseline) to current `HEAD` and trace failure cluster `v15/v17/v19`.

Findings:

1. `experiments/attack.py` changed substantially since lb-81.225 (Stage-A simplification), but it still returns `list[AttackCandidate]` in the required format. No row-schema rewrite, no submission-file code path.
2. `comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py` changed only by one internal variable-line refactor; no submission format contract changes.
3. `submission/build_notebook.py` is the only code that touches submission-file plumbing. The regression window aligns with commit `68a53b3`-like behavior:
   - added/retained write to both `/kaggle/working/submission.csv` and `submission.csv`,
   - then validated both paths and used combined fallback/finalization logic.

Why this is a likely cause of `Submission Format Error`:
- failure payloads reported `totalBytes=0` for those refs, which matches a notebook-run contract/path write failure pattern more than attack logic corruption.
- those same refs are in the stage where notebook CSV hardening was active and attack output path was not.

Mitigation applied:
- committed `538d429` and pushed:
  - **only** write/validate/check `/kaggle/working/submission.csv`,
  - removed the second path loop that could fail independently,
  - kept `serve()`-time exception fallback to a valid 4-row placeholder file.

Next required control:
- submit a small-control run first (same attack, one fixed count) with this notebook build, then proceed to 1950-count sweep only if output artifact is accepted.
