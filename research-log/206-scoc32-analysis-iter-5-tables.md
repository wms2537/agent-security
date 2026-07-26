# SCOC-32 Phase-5 analysis tables

**Date:** 2026-07-26 · **Phase:** 5 · **Cycle:** 3 · **Iteration:** 5/5 · **Status:** analyzer-replacement completed

## Statistical declaration

```text
independent_unit: one preserved mechanism-harness rerun for mechanism ratio; one official public leaderboard submission for live bundle
n_units: mechanism ratio n=2 reruns; live bundle n=1 public submission per ref
comparison_family: 2 descriptive comparisons (mechanism ratio vs 1.25 gate; bundled public score vs 69.570 incumbent)
correction: none - descriptive gate checks, no p-value claim
```

No inferential p-value claim is made. The mechanism result is a preregistered deterministic gate check over two preserved reruns. The public leaderboard result is an official tuning signal, but it is unpaired and bundles multiple implementation changes, so it is not component attribution evidence.

## Analyzer dispatch note

The required Phase-5 analyzer subagent was dispatched for `research-log/206-scoc32-analysis-iter-5-tables.md` and the two SCOC figures, but produced no files after three 30-second checks and was interrupted. The orchestrator generated this bounded replacement and verifies it directly in `research-log/207-scoc32-phase5-analysis-iter-5.md`.

## Ledger counts

`results.tsv` has 148 data rows and 149 total lines including the header.

| Status | Rows | Included in SCOC rankings/statistics/figures? |
|---|---:|---|
| keep | 27 | Only if in-scope for the active SCOC claim; historical ORF keep rows are excluded from SCOC evidence |
| exploratory | 95 | No |
| preregistered | 11 | No |
| discard | 7 | No |
| crash | 6 | No |
| mechanics-only | 1 | No |
| superseded | 1 | No |

| Signal | Rows |
|---|---:|
| confirm | 105 |
| partial | 20 |
| null | 18 |
| disconfirm | 5 |

| Confidence | Confirmed / total resolved | Confirm rate |
|---|---:|---:|
| high | 23 / 30 | 0.766667 |
| medium | 12 / 22 | 0.545455 |
| low | 70 / 96 | 0.729167 |

The `medium` tier is under-calibrated for this project history. The high rate is acceptable, and the low rate is inflated by many intentionally easy match-baseline/exploratory checks, not by successful risky predictions.

## Mechanism table at m=32

Source files:

- `artifacts/scoc32/run03/scoc32-mechanism-harness.tsv`
- `artifacts/scoc32/run04/scoc32-mechanism-harness.tsv`

| Rerun | CHAIN_FULL raw/s | CHAIN_SCOC raw/s | CHAIN_GENERIC raw/s | SCOC/full ratio | Generic/SCOC ratio | SCOC coverage | Frozen gate |
|---|---:|---:|---:|---:|---:|---:|---|
| run03 | 13224.396069 | 14363.784627 | 14364.666321 | 1.086158079 | 1.000061383 | 1.000000 | FAIL (< 1.25) |
| run04 | 13158.699273 | 13475.494739 | 13330.177920 | 1.024074983 | 0.989216858 | 1.000000 | FAIL (< 1.25) |

Descriptive ratio summary:

| Quantity | Value |
|---|---:|
| Mean SCOC/full ratio | 1.055116531 |
| Sample SD across two reruns | 0.043899378 |
| Mean gap to frozen 1.25 gate | -0.194883469 |
| Minimum observed coverage | 1.000000 |

Gate result: coverage confirmed, mechanism efficiency refuted. The run03 `CHAIN_GENERIC >= CHAIN_SCOC` condition also triggers the frozen generic-compression retraction for contribution credit.

## Public leaderboard bundle table

Read-only command refreshed on 2026-07-26:

`comp/.venv/bin/kaggle competitions submissions -c ai-agent-security-multi-step-tool-attacks --format csv --page-size 20`

| Ref | Description | Status | Public score | Role |
|---:|---|---|---:|---|
| 54923079 | SCOC32 chain exploratory run 5 CPU | COMPLETE | 81.225 | Current best bundled system |
| 54920038 | SCOC32 chain exploratory run 2026-07-23 | COMPLETE | 81.090 | Bundled system |
| 54922298 | SCOC32 chain exploratory run 3 | COMPLETE | 79.920 | Bundled system |
| 54808132 | Prior verified-fill incumbent | COMPLETE | 69.570 | Prior incumbent |
| 54799835 | v1 multi-post/reserve | COMPLETE | 36.705 | Superseded |

The best bundled public score improves over the `69.570` incumbent by:

```text
(81.225 - 69.570) / 69.570 = 0.167529109 = 16.752911%
```

This is useful competition tuning evidence for the whole committed attack bundle. It is not valid evidence that SCOC caused the gain, because the submissions changed multiple mechanisms and no component-fixed official ablation or episode trace exists.

## Figure list and legends

### `paper/figures/scoc32_mechanism_comparison`

Files:

- `paper/figures/scoc32_mechanism_comparison.svg`
- `paper/figures/scoc32_mechanism_comparison.png`
- `paper/figures/scoc32_mechanism_comparison.source.csv`

Legend:

Fig. 1 | SCOC fails the frozen mechanism gate. Bars show `CHAIN_SCOC / CHAIN_FULL` raw-per-second ratios for two preserved m=32 mechanism-harness reruns. The dashed line marks the preregistered 1.25x contribution gate. Statistics: n = 2 preserved mechanism reruns, error bars are not shown because each bar is one rerun, no inferential test; descriptive gate comparison only, p = not applicable. Source data are provided as a Source Data file.

### `paper/figures/scoc32_public_leaderboard_bundle`

Files:

- `paper/figures/scoc32_public_leaderboard_bundle.svg`
- `paper/figures/scoc32_public_leaderboard_bundle.png`
- `paper/figures/scoc32_public_leaderboard_bundle.source.csv`

Legend:

Fig. 2 | The live bundle improves public score without component attribution. Bars show official public scores for the superseded v1 submission, the `69.570` prior incumbent, and three completed SCOC-era bundled submissions. Statistics: n = 1 official public submission per bar, error bars are not shown, no inferential test; descriptive leaderboard comparison only, p = not applicable. Source data are provided as a Source Data file.

## Prediction versus reality

Prediction: one exact successful anchor plus destination-only operands would preserve at least 0.95 coverage and raise raw replay efficiency by at least 1.25x over full repetition, while remaining distinct from generic shorthand.

Reality: coverage held, but the mechanism failed the efficiency and distinctiveness tests. The two preserved ratios were 1.086 and 1.024, both below 1.25; in one rerun generic shorthand slightly exceeded SCOC. Local paired SCOC-off/on normalized scores were flat at 23.28. The public bundle improved to 81.225, but it cannot identify SCOC's contribution.

## Summary

SCOC-32 did not work as a proprietary mechanism. The component preserved exact chain coverage, which confirms that conversation history can carry enough syntax/state to reproduce the tool path, but it did not produce enough raw-per-second advantage to matter under the frozen winning bridge. Its mean descriptive ratio was only 1.055x, far below the 1.25x gate, and generic shorthand matched or exceeded it in run03.

The only positive result is the complete-system public leaderboard score of 81.225. That is operationally valuable because it improves the repo's live public incumbent by 16.752911%, but it is unattributed: selector, routing, accounting, candidate count, and SCOC-path changes moved together. It should be retained as the current public tuning best and excluded from SCOC contribution claims.

The most informative failure is not low coverage; it is failed distinctiveness. SCOC's proposed state-conditioned continuation did not separate from shorter message encoding strongly enough to justify another submission or another mechanism review. The problem-facing lesson is that harness/context state remains a real frontier, but contribution credit requires component-fixed official ablations or a mechanism profile that isolates the named bottleneck before leaderboard score is used.
