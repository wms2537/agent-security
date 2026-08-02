# Kaggle Commit-Run Gate — v37 Measured Dense Replacement

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 10 · **Status:** completed

## Context

T124 pushed the measured dense replacement notebook as Kaggle kernel version 37 after T122 local implementation checks and T123 code review/hardening. This is a commit-run artifact gate only, not a leaderboard submission.

## Content

Kernel push:

```text
comp/.venv/bin/kaggle kernels push -p submission/kernel
```

Output:

```text
Kernel version 37 successfully pushed.
```

Status poll:

```text
whymelabs/ai-agent-security-attack has status "KernelWorkerStatus.COMPLETE"
```

Downloaded output:

```text
Output file downloaded to kaggle_outputs/v37-measured-dense/attack.py
Output file downloaded to kaggle_outputs/v37-measured-dense/submission.csv
Kernel log downloaded to kaggle_outputs/v37-measured-dense/ai-agent-security-attack.log
```

Artifact checks:

```text
csv_rows 5
csv_header Id,Score
csv_empty_cells 0
csv_widths [2]
source_strip_match True
output_attack_sha256 499476b7e455dedf2639b939d59e97f1c3632dbf71ff3661abacb88a49a207f3
```

Static source checks found the expected measured-dense markers in the downloaded `attack.py`:

- `DENSE_ENABLED = False`
- `MEASURED_DENSE_REPLACEMENT_ENABLED = True`
- `MEASURED_DENSE_MIN_KEPT_TO_USE = 93`
- `MEASURED_DENSE_MAX_KEPT = 96`
- `MEASURED_DENSE_PROBE_BASE = 760000`
- `MEASURED_DENSE_FRAME_OFFSET = 50000`

Targeted log/source checks:

- `rg -n "Traceback|ERROR|Error|Exception|Submission Format Error|ModuleNotFoundError|NameError|SyntaxError" kaggle_outputs/v37-measured-dense/ai-agent-security-attack.log || true` returned no matches.
- `rg -n "_emit_dense" kaggle_outputs/v37-measured-dense/attack.py || true` returned no matches.

## Gate Check

- Kernel status: PASS — status command returned `KernelWorkerStatus.COMPLETE`.
- Output schema: PASS — downloaded `submission.csv` has 5 rows, header `Id,Score`, width `[2]`, and zero empty cells.
- Source match: PASS — downloaded `attack.py` strip-matches local `experiments/attack.py`.
- Frozen constants: PASS — downloaded `attack.py` contains the measured constants and old `DENSE_ENABLED = False`.
- Blind dense absence: PASS — `_emit_dense` is absent from downloaded attack source.
- Runtime log: PASS — targeted error/traceback grep over the downloaded commit-run log returned no matches.

## Problem alignment

This provides target-owned commit-run evidence that the measured dense replacement artifact has correct notebook/source/schema shape before any leaderboard submission.

## Decision

T124 passes. The artifact is eligible for T125 competition submission under the existing user authorization and confidence-before-submission rule.

## Next Steps

Submit kernel version 37 using `submission.csv`, then record the result against report `254` bins: success `>=100.000`, partial `[86.670,100.000)`, failure blank/error or `<86.670`.
