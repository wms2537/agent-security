# Kaggle commit-run gate — Burst-2 Validation Fill v38

Date: 2026-08-03

## Push

Command:

```text
comp/.venv/bin/kaggle kernels push -p submission/kernel
```

returned:

```text
Kernel version 38 successfully pushed.
```

Status polling:

```text
comp/.venv/bin/kaggle kernels status whymelabs/ai-agent-security-attack
```

returned `KernelWorkerStatus.COMPLETE`.

## Output download

Command:

```text
mkdir -p kaggle_outputs/v38-burst2-commit
comp/.venv/bin/kaggle kernels output whymelabs/ai-agent-security-attack -p kaggle_outputs/v38-burst2-commit
```

downloaded:

```text
kaggle_outputs/v38-burst2-commit/ai-agent-security-attack.log
kaggle_outputs/v38-burst2-commit/attack.py
kaggle_outputs/v38-burst2-commit/submission.csv
```

## Output contract

CSV/source check returned:

```text
csv_rows 5
csv_header Id,Score
csv_widths [2]
csv_empty_cells 0
csv_rows_data [['gpt_oss_public', '0.0'], ['gpt_oss_private', '0.0'], ['gemma_public', '0.0'], ['gemma_private', '0.0']]
remote_attack_exists True
source_strip_match True
needle BUNDLE_POSTS = 2 1
needle BUNDLE_POSTS_MAX = 2 1
needle MEASURED_DENSE 0
needle SLOW_MULTIPOST 0
needle _dense_msg 0
needle _measured_dense 0
needle Perform exactly 4 0
```

Actual run-log grep:

```text
rg -n "Traceback|Submission Format|Did not find|FAILED|ERROR|Error|Exception" kaggle_outputs/v38-burst2-commit/ai-agent-security-attack.log || true
```

returned no matches. The log contains only standard notebook warnings, setup lines, `attack.py written`, and `placeholder submission.csv written`.

## Decision

The commit-run gate passes. The artifact is eligible for the competition-submission confidence checklist.
