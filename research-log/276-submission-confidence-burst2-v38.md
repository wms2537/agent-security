# Submission confidence checklist — Burst-2 Validation Fill v38

Date: 2026-08-03

Candidate: Kaggle kernel version `38`, `whymelabs/ai-agent-security-attack`

## Checklist

| Gate | Evidence | Status |
| --- | --- | --- |
| Hypothesis preregistered before implementation | report 271 supersedes report 269; results row `lb-stagec-burst2-validation-fill` predicts `100.000` before target submission | PASS |
| Theory gate | report 272 returns `Overall: RIGOROUS` for the narrowed calibration claim | PASS |
| Local mechanics | report 273 records `burst2_gate_pass: 1` | PASS |
| Code review | report 274 returns `Overall: SOUND` | PASS |
| Notebook rebuild | report 273/274: `attack.py parses OK` | PASS |
| Commit-run terminal | report 275: v38 `KernelWorkerStatus.COMPLETE` | PASS |
| CSV format | report 275: `csv_rows 5`, `csv_header Id,Score`, `csv_widths [2]`, `csv_empty_cells 0` | PASS |
| Source identity | report 275: `source_strip_match True` | PASS |
| K=2 active | report 275: `BUNDLE_POSTS = 2` and `BUNDLE_POSTS_MAX = 2` present once in downloaded source | PASS |
| Refuted branches absent | report 275: no `MEASURED_DENSE`, `SLOW_MULTIPOST`, `_dense_msg`, `_measured_dense`, or K=4 marker | PASS |
| Run log clean | report 275: actual commit-run log grep found no traceback/error/submission-format markers | PASS |

## Remaining risk

The remaining uncertainty is target-owned and cannot be resolved from commit-run logs:

- second-event prevalence during replay;
- K=2 replay-time cost versus returned candidate count;
- public/private row transfer.

These are exactly the variables the Kaggle submission is intended to measure. The branch is small, source-compliant, locally gated, and has a public-code mechanism prior. It is eligible for one competition submission.

## Decision

Submit v38 to the competition with message:

```text
Burst2 validation-fill v38
```
