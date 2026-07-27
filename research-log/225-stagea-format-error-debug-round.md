# Stage A Submission-format debugging (July 27 run block)

**Date:** 2026-07-28
**Phase:** Stage A control recovery
**Cycle:** 3
**Iteration:** 8 (format integrity)
**Status:** in-progress

## Finding 1 — Commit runs are clean, so placeholder path is correct

- Current kernel version output was downloaded with:
  `comp/.venv/bin/kaggle kernels output whymelabs/ai-agent-security-attack/11 -p /tmp/stagea-v14-output -q`
- Output files exist as expected:
  - `/tmp/stagea-v14-output/attack.py`
  - `/tmp/stagea-v14-output/submission.csv`
  - `/tmp/stagea-v14-output/ai-agent-security-attack.log`
- `submission.csv` content is exact 5-line scaffold:
  - `Id,Score`
  - `gpt_oss_public,0.0`
  - `gpt_oss_private,0.0`
  - `gemma_public,0.0`
  - `gemma_private,0.0`

This matches the expected Kaggle CSV schema for commit-run placeholder behavior.

## Finding 2 — New attempts are not scoring, not timing out in commit-run

Latest references from `comp/.venv/bin/kaggle competitions submissions -c ai-agent-security-multi-step-tool-attacks --format csv`:

- `55028345` `format-fixed v14 csv hardening run`
- `55025140` `fallback-fix v13 test localfile`
- `55024720` `fallback-fix v12 staged`
- `55018092` `Stage A fixed single-post format-fixed CSV schema`
- `55002770` `Stage A fixed-count N1950 (three-arm minimal control)`

All have `SubmissionStatus.COMPLETE` with empty public/private scores, which is consistent with submission-format/evaluation-write failure rather than a scored leaderboard artifact.

## Finding 3 — Why we cannot see root cause from CLI yet

- `comp/.venv/bin/kaggle competitions episodes <ref>` still returns `No episodes found` for these refs.
- This competition command surface does not expose replay detail for these failed refs in current CLI path.
- So format error remains at the “submission result unavailable” layer, not confirmed as candidate/evaluation logic yet.

## Likely explanation now

`submission.csv` in the commit phase is valid, and the hardening path in `submission/build_notebook.py` now validates/normalizes before/after serve. The remaining evidence is therefore most consistent with non-commit evaluation failure in the replay phase:

- failure before final write in the competition rerun gateway/runtime path, or
- package-level mismatch in rerun import path (old/unmodified evaluator package behavior), which means local gateway edits are not directly exercised by rerun.

## Practical rule for next steps

Before any further score-seeking submission, require one explicit positive control:

1. Build + kernel push + commit output check (must pass).
2. Submit only when run logs explicitly show that the commit-produced `submission.csv` and rerun contract path are present and validated.
3. Record each result in `competition/leaderboard_experiments.tsv` immediately after submission status updates.

This prevents another blind cycle of repeated-format attempts.

## Decision

Keep the existing Stage-A attack policy unchanged for now (three-arm fixed-count single-post) and do not infer mechanism changes from these failures until rerun write-path telemetry is available.
