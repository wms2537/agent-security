# 2026-07-28 — Submission-Format Error Inference + "How to do it properly" Gate

## 1) What we verified this cycle

Repository checks done:

- `submission/build_notebook.py` writes and validates a 5-line placeholder CSV:
  - `Id,Score`
  - `gpt_oss_public,0.0`
  - `gpt_oss_private,0.0`
  - `gemma_public,0.0`
  - `gemma_private,0.0`
- Local compile checks for the current kernel artifacts pass.
- `kaggle kernels output whymelabs/ai-agent-security-attack/11` has no runtime traceback in log.
- Recent submissions are in `COMPLETE` state with blank public/private score:
  - `55028345`, `55025140`, `55024720`, `55018092`, `55002770`.
- `kaggle competitions submissions -c ai-agent-security-multi-step-tool-attacks --format json`
  confirms those refs have empty `publicScore`/`privateScore`.
- `kaggle competitions episodes <ref>` still returns “No episodes found” in this CLI path.

## 2) Inference from evidence

The Kaggle error is not a commit/build artifact; the commit output shape is valid.

Most likely root class:

- competition rerun/runtime failure before a valid final `submission.csv` is produced,
  which appears upstream as blank public/private score for the ref.

Why this is the stronger explanation:

- Placeholder CSV file shape is currently valid and parser-clean locally.
- The local write/readback hardening in:
  - `submission/build_notebook.py`
  - `comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py`
  is stricter than before and should prevent plain schema regressions.
- We cannot retrieve rerun telemetry (episodes/logs) from CLI for this competition branch.

Therefore, the next diagnostic assumption is:

- **submission.csv is no longer the primary suspected failure point**
- **runnable rerun path behavior is now the primary suspect**

## 3) Practical “do it properly” gate before the next submission

Before any next Kaggle submit, run all gates below:

1. `python -m py_compile experiments/attack.py submission/build_notebook.py`
2. `python submission/build_notebook.py` (watch for build or serve traceback)
3. Download notebook output and confirm:
   - both `/kaggle/working/submission.csv` and top-level `submission.csv` at output root exist,
   - exactly 5 lines and exact IDs.
4. Log the current commit SHA and attack SHA into `competition/leaderboard_experiments.tsv`.
5. Submit one controlled baseline in a single batch:
   - a) known-good historical control strategy (reference hash),
   - b) current Stage-A control strategy.
6. Compare: if both fail similarly, the issue is likely platform/gateway/runtime path;
   if only current fails, isolate Stage-A variant changes.

## 4) Current status

- `55002770` through `55028345`: **blocked: submit-format-like outcome (blank score)**
- Stage-A mainline is now treated as **format unresolved due runtime opacity**, not as "submission file confirmed broken".
- Next move: controlled one-batch comparison submit to identify whether fault is
  (a) old/new attack behavior or (b) shared rerun path.

## 5) Explicit classification

The current evidence classifies this incident as:

- **Not yet attributable to:** malformed `submission.csv` fields, wrong column order, wrong row count, or invalid local compile output.
- **Still open:** rerun/runtime path behavior in the Kaggle scoring environment that is not observable through available CLI episode traces for this competition branch.

This is why the next controlled step is not further local schema edits.

## 6) Immediate action required to do it properly

Do not change attack mechanics until:

1. both a historical control and current Stage-A control are submitted as a paired comparison,
2. their outcomes are recorded in `competition/leaderboard_experiments.tsv`,
3. the shared-failure test is resolved:
   - shared blank-score outcomes => shared runtime block, pause attack iteration,
   - only Stage-A blank => isolate Stage-A changes only.

This keeps the work aligned with the source contract and prevents another blind iteration.
