# Stage A Submission-Confidence Checklist (v11)

Date: 2026-07-28
Hypothesis: `stagea-fixed-count-single-post-throughput`
Commit: `08758cc81b54e120afc12c2f72b0dee181bcd7db`
Kernel: `whymelabs/ai-agent-security-attack` (v11)

## Checklist

| Gate | Required condition | Evidence | Status |
| --- | --- | --- | --- |
| Source artifact | Stage-A attack and notebook are built from the same committed source and immutable control hash set is recorded | `08758cc81b54e120afc12c2f72b0dee181bcd7db`, `research-log/222`, `research-log/223`, `state.json` task T091/T092 | PASS |
| Local control and syntax | `python -m py_compile experiments/attack.py submission/build_notebook.py` succeeds | Prior Stage-A preregistration already recorded as pass; no code change since commit | PASS |
| Mechanics evidence | Removed old controller branches and unidentifiable replay sizing; no per-candidate verification in fill path; fixed N policy | `rg` branch grep in `stagea_static_20260726` and fixed-count smoke row in `stagea_fake_env_1950_20260726` | PASS |
| Kaggle execution readiness | Commit-run executes and emits `attack.py`, `submission.csv`, and log without runtime exception | `comp/.venv/bin/kaggle kernels status ...` moved to COMPLETE; output in `/tmp/stagea-v10-output` has no tracebacks | PASS |
| Placeholder semantics | Commit output is expected placeholder (`submission.csv` with zeros) and not mistaken for official score | Output inspection shows 5-line placeholder file | PASS |
| Regression guard | New experiment advances toward a minimal single-post control and does not mix un-anchored mechanisms | Stage A preserves 3-arm fixed count, no SCOC, no timing sizing, one-factor control variable | PASS |
| Evidence hygiene | No secrets, no unreviewed local-mechanism confounds; active evidence rows updated in mechanics ledger | `competition/mechanics_experiments.tsv`, `research-log/223`, `state.json`, `research-log/progress.md` | PASS |

## Decision

Do not submit blindly after confidence checks. This cycle confirms commit integrity, but current competition rows (`55002770`, `55018092`, `55024720`, `55025140`, `55028345`) are blank-score failures in rerun phase.

Next decision gate: submit exactly two one-off comparison runs:

1) historical known-good control (81.225 baseline family),
2) current Stage-A control.

If both fail similarly (blank scores), treat as shared rerun path/runtime blocker and pause attack changes. If only current fails, isolate Stage-A strategy changes only.
