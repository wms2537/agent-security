# Stage A run: v17 count-sweep baseline with return_count=1950

Date: 2026-07-28

## Scope

- Single-post fixed-count control experiment
- Only changed control variable relative to previous diagnostic: fixed `return_count` increased from 500 to 1950
- No per-candidate verification, no replay-cost sizing loop, no SCOC branch

## Code changes

- `experiments/attack.py`
  - `AttackConfig.return_count` changed from `500` to `1950`
- Rebuilt notebooks via:

```bash
python submission/build_notebook.py
```

- Pushed updated kernel:

```bash
kaggle kernels push -p submission/kernel
```

Kernel push output:

- `Kernel version 19 successfully pushed`
- Kernel output downloaded successfully (`attack.py`, `submission.csv`, log)

## Submission record

- Competition submit run:

```bash
kaggle competitions submit -c ai-agent-security-multi-step-tool-attacks \
  -k whymelabs/ai-agent-security-attack -v 19 \
  -f submission.csv -m "StageA count sweep 1950 single-post fixed"
```

- New reference: `55053373`

## Status checks

- `kaggle competitions submissions -c ... --format csv` reports
  - `55053373` status: `SubmissionStatus.PENDING`
  - `55050300` status: still `SubmissionStatus.PENDING`
  - `55046504` remains `COMPLETE` with `45.000` (this is the expected 0.225/1950 mapping from `return_count=500`, i.e., 500 findings × 18/200)

## Interpretation

- Current result is consistent with score arithmetic, not submission-format failure.
- The only validated control changed between v16 and v17 is candidate count (500→1950).
- Next actionable step: wait for `55053373` completion to measure throughput recovery at 1950 fixed count.

## Files updated

- `experiments/attack.py`
- `submission/kaggle_notebook.ipynb`
- `submission/kernel/kaggle_notebook.ipynb`
- `ai-agent-security-attack.ipynb`
- `competition/leaderboard_experiments.tsv`

