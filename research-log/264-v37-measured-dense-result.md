# v37 Measured Dense Replacement Result

**Date:** 2026-08-03 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 10 · **Status:** completed

## Context

Reports `254` and `258` preregistered measured dense replacement with success `>=100.000`, partial `[86.670,100.000)`, and failure blank/error or `<86.670`. Reports `261` through `263` recorded a clean v37 commit-run gate, submission ref `55189377`, and long-pending state.

## Content

Live Kaggle status:

```text
ref,fileName,date,description,status,publicScore,privateScore
55189377,submission.csv,2026-08-02 15:35:06.693000,Measured dense replacement v37,SubmissionStatus.COMPLETE,84.735,
55158967,submission.csv,2026-08-01 09:25:20.083000,Public-control validation-fill GPU recovery v35,SubmissionStatus.COMPLETE,86.670,
```

Arithmetic:

```text
delta_vs_v35 -1.935
relative_vs_v35_pct -2.233
miss_vs_prediction -15.265
```

Prediction vs. reality: disconfirmed. The artifact completed visibly, so the kernel wrapper and submission format were correct. But the public score `84.735` is below the v35 fallback floor `86.670`, therefore it is a failure under the preregistered report `254` bins.

## Interpretation

Measured dense replacement solved the previous blank/error class but did not improve score. The most likely explanation is that the measured dense branch consumed generation/replay budget or displaced higher-throughput single-post candidates without enough replay-scored dense events to compensate. Because Kaggle does not expose per-candidate replay logs, the precise mixture cannot be identified from this result alone.

The result does falsify the operational claim that retaining `93-96` locally firing dense candidates plus remaining fallback budget would reach the competition-relevant `100` range. It also shows that visible completion is insufficient; density must beat fallback throughput, not merely avoid blanking.

## Gate Check

- Terminal status: PASS — `comp/.venv/bin/kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v | rg "55189377|55158967|ref,fileName"` returned ref `55189377` COMPLETE with public score `84.735` and v35 ref `55158967` COMPLETE with `86.670`.
- Preregistered bin: FAILURE — `84.735 < 86.670`.
- Ledger update: PASS — `results.tsv` row `lb-stageb-measured-density-fill` updated to `metric_value=84.735`, `signal=disconfirm`, `status=discard`.

## Problem alignment

This target-owned result directly advances the core competition question by rejecting a measured-density replacement that local mechanics favored but remote scoring penalized.

## Decision

Close T125 as failed. Move to Phase 5 analysis before any further implementation or submission. No new measured-density tweak is justified without a new structural hypothesis and budget approval.

## Next Steps

Analyze iteration 10, fill the search diagnosis outcome as `refuted`, and decide whether the project must conclude due exhausted research budget or request a fresh explicitly approved iteration on a different dimension.
