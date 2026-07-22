# HCMS-24 Phase-3 PoC result

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** violated / discarded

## Context

The HCMS-24 joint engineering hypothesis was frozen in
`research-log/146-hypothesis-iter-7-hcms24.md`, independently judged
`RIGOROUS` in report 149, and implemented under the frozen design in report
150. Five successive sterile code-review rounds ended with the exact verdict
`No findings. No pre-run code fix remains. SOUND` in report 160. Only then was
the first canonical scientific attempt admitted.

## Execution and provenance

Scientific attempt 1/3 used the command already present as line one of
`run.log`:

```text
comp/.venv/bin/python -I experiments/poc/hcms24_phase3_v1.py --config experiments/configs/hcms24-c3-v1.json --attempt-dir experiments/runs/hcms24-c3-poc-v1
```

The process exited zero after `466.829215854` seconds and published
`COMPLETE.json` last. Direct audit established:

- `MANIFEST_HASHES_OK`: all 11 named artifacts match their sealed SHA-256;
- `PUBLICATION_ORDER_OK`: no artifact is newer than `COMPLETE.json`;
- the directory contains exactly the manifest plus its 11 named artifacts;
- runner SHA-256 is
  `7b030c67a7f18c4bce77db67f7db757b817aede7cbaf75aa1195a09d42f6b1f6`;
- config SHA-256 is
  `e71c8a6afb70459077a303652e21063a9c71f60d0650a502de8f63fbfb3c0e59`;
- an independent reload and decision reconstruction returned
  `OFFLINE_RECONSTRUCTION_PASS invalid 1.3918315252074027 187 189`;
- the runner's independent manifest validator returned
  `MANIFEST_VALIDATOR_PASS 11 invalid`; and
- the reconciled grid contains 145 method cells (144 primary plus one safety),
  771 candidates and 1,449 attempted paths.

This is a complete, source-bound invalid scientific result, not a crashed or
corrupt attempt. It is immutable and will not be overwritten or relabeled.

## Prediction versus reality

| Frozen metric | Prediction | Actual | Signal |
|---|---:|---:|---|
| HCMS / best simple aggregate | `>=1.10` | `1.391831525207` (`39258 / 28206`) | confirm in the controlled harness |
| HCMS candidate replay coverage | `1.0` | `187/189 = 0.989417989418` | disconfirm |
| HCMS aggregate replay-overage cells | `0` | `0/36` | confirm |
| scalar-removal replay-overage cells | `>=1` | `19/36` | confirm |
| primary timeout/duplicate/generation-overage count | `0` | `4` generation overages | disconfirm |

All 144 primary repetitions completed. Attribution fixtures passed `3/3`,
deadline fixtures passed `3/3`, Williams position checks passed `144/144`,
directed-predecessor checks passed `108/108`, and exception, attribution,
duplicate, timeout, incomplete and score-identity counts were all zero.

The ratio is diagnostic rather than confirmatory because the joint protocol
declared any calibrated replay miss or generation overage invalid. Three of
five individual predictions were right, but the two high-confidence validity
predictions were wrong; the joint hypothesis is not partially rescued by the
large raw ratio.

## Failure localization

### Replay-calibration failure

Two primary HCMS candidates exceeded their own calibrated replay charges even
though their method-cell aggregate stayed below two seconds:

| Profile / master / order / candidate | Prefix | Charge (s) | Actual (s) | Actual / charge |
|---|---:|---:|---:|---:|
| immediate cliff / 211 / 0 / 7 | 8 | `0.201492933` | `0.208157787` | `1.03308` |
| immediate cliff / 307 / 0 / 3 | 8 | `0.173873153` | `0.177321964` | `1.01984` |

The excluded delayed-cliff safety cell had a larger miss on its first prefix-24
candidate: `0.272488356 / 0.247143118 = 1.10255`. Thus the antecedent `54/54`
calibration coverage did not transfer to fresh endogenous candidates. A point
surrogate can fit the mean/observed calibration set while failing the strict
one-sided coverage estimand.

### Generation-admission failure

Four primary cells crossed the two-second generation deadline by 2.1--21.7 ms.
Each had admitted a final path because more than the fixed `0.1`-second reserve
remained; fresh environment construction/reset then consumed the remaining
time before even one interaction completed:

| Profile / master / method | Time before final path (s) | Final path cost (s) | Terminal (s) |
|---|---:|---:|---:|
| steady / 211 / fixed8 | `1.886622190` | `0.113953851` | `2.005357818` |
| steady / 307 / fixed8 | `1.879681542` | `0.118751598` | `2.002080786` |
| reset / 101 / fixed8 | `1.891058159` | `0.123366442` | `2.021733888` |
| reset / 211 / HCMS | `1.879839289` | `0.108884886` | `2.003870708` |

The separate safety path has the same defect (`1.887956115 + 0.138545331`,
terminal `2.032595770`). Its returned transition was exactly the required
`24,8,8,8,8,8,8,8,8`, but the cell correctly failed because the resource
invariant did not hold. The problem is not just post-loop bookkeeping jitter:
the frozen before-path rule admitted a fresh construction whose observable
cost tail exceeded its reserve.

## Interpretation

The controlled evidence supports retaining the high-ceiling monotone-salvage
candidate structure as a promising base: its raw diagnostic advantage is
39.18% over the strongest simple comparator, and the scalar accounting removal
fails severely. It does **not** support the reviewed joint HCMS-24 claim.

The load-bearing false assumption is deterministic point-cost admission. Both
failures are instances of the same resource-risk error: the controller compares
random future work with a fixed point reserve or point replay surrogate while
claiming one-sided deadline/coverage safety. Increasing `0.1` after seeing this
run or multiplying the ledger by the observed maximum would be post-hoc
threshold fitting and is forbidden. The next hypothesis must replace point
admission with a separately calibrated one-sided resource-risk envelope,
include construction/reset/controller costs in the estimand, freeze a nonzero
violation-risk target, and test it on fresh data with the HCMS structure held
fixed.

This recurrence increments the existing project lesson that replay-deadline
safety requires a calibrated tail/dependence model and explicit void-risk
target. It is the fifth recurrence, now with prospective evidence rather than a
review-only warning.

## Gate Check

- PoC supports all core assumptions: **FAIL**. Coverage is `187/189`, primary
  generation-overage count is four, safety validity is false, and sealed status
  is `invalid`.
- Metrics verified directly: **PASS**. `run.log`, independent hash audit,
  offline reconstruction and manifest validation agree.
- Phase-3 go/no-go: the user's recorded Cycle-3 autonomy instruction is to
  proceed with rigorous creative iteration and to pivot when useful. This
  authorizes the recommended **revise hypothesis** branch, but cannot convert
  the invalid PoC into support or authorize a competition submission without
  the separate confidence gate.

## Problem alignment

Rejecting an unsafe controller prevents a locally attractive `1.392x` mock
ratio from reaching Kaggle without the replay/deadline evidence required by
`PROBLEM.md`.

## Decision

Mark HCMS-24's joint claim `refuted`, discard this run for confirmation, preserve
its candidate-structure signal only as motivation, and loop to Phase 2 under
the same research iteration. The next task is a targeted source/literature and
trace diagnosis followed by one superseding, risk-limiting admission hypothesis.
No debug rerun, attack mutation, Kaggle push, commit run or submission is
authorized by this result.

## Next Steps

1. Search primary recent work on online one-sided runtime prediction,
   risk-limiting/conformal resource allocation, and deadline-aware admission.
2. Compare replacement candidates with the SciAgent critique rubric and choose
   one single structural dimension rather than stacking margins.
3. Freeze a fresh-data prediction and validity contract; then perform the
   Phase-2 self-critique and sterile theory review before any new run.
