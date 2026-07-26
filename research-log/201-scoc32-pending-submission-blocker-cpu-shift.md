# T076 — SCOC-32 Kaggle submission blocker investigation and CPU submission attempt

## Why this task
After local mechanics stabilized, the next gate step was a live confidence check via code submission. Two attempts were blocked before scoring by Kaggle API constraints.

## Commands executed

- `python submission/build_notebook.py`
- `comp/.venv/bin/kaggle kernels push -p submission/kernel --timeout 120 --accelerator 'none'`
- `comp/.venv/bin/kaggle kernels status whymelabs/ai-agent-security-attack`
- `comp/.venv/bin/kaggle kernels files whymelabs/ai-agent-security-attack/8`
- `comp/.venv/bin/kaggle competitions submit -c ai-agent-security-multi-step-tool-attacks -k whymelabs/ai-agent-security-attack -f submission.csv -v 8 -m "SCOC32 chain exploratory run 3"` (initial)
- `comp/.venv/bin/kaggle kernels push -p submission/kernel --accelerator 'none'`
- `comp/.venv/bin/kaggle kernels status whymelabs/ai-agent-security-attack/9`
- `comp/.venv/bin/kaggle competitions submit -c ai-agent-security-multi-step-tool-attacks -k whymelabs/ai-agent-security-attack -f submission.csv -v 9 -m "SCOC32 chain exploratory run 5 CPU"`
- repeated:
  - `comp/.venv/bin/kaggle competitions submissions -c ai-agent-security-multi-step-tool-attacks --page-size 40 -v`

## Evidence of API blocker

A direct API call through the Kaggle SDK showed the true queue error on GPU submissions:

```text
text {"error":{"code":400,"message":"Submission not allowed:  Your Notebook cannot use P100 GPUs in this competition.","status":"FAILED_PRECONDITION"}}
```

## Fix applied

To resolve the accelerator-policy mismatch, both metadata files were updated to CPU-only before re-submission:
- `kernel-metadata.json`
- `submission/kernel/kernel-metadata.json`

Patched fields:
- `"enable_gpu": false`
- `"machine_shape": "Cpu"`

A fresh push created kernel version 9.

## Outcome

- New submission ref created: `54923079` with message `SCOC32 chain exploratory run 5 CPU`.
- Current status remains `SubmissionStatus.PENDING` for refs:
  - `54923079` (run-5 CPU)
  - `54922298` (run-3)
  - `54920038` (run-2026-07-23)

No public/private scores are available yet, so confidence gate cannot be closed on live evidence at this moment.
