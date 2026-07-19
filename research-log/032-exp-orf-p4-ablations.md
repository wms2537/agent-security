# Experiment: ORF Phase-4 attribution ablations

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed, confirmed and kept

## Context

T019 is the frozen one-at-a-time attribution batch after the reviewed core
confirmed 40.249038022308% mean public-table gain. It does not tune or add to the
policy. Each condition changes exactly one generator/score mechanism on the same
three primary masters and retains the seven-action adaptive-versus-global
estimand.

## Design

The implementation must parse the committed 960-row baseline table, verify the
original default scores, and reconstruct each profile's exact polynomial
coefficients from its seven exact costs. It must use the reviewed
`evaluate_master_score_tables` engine from `run_core.py`. The five frozen changes
from the Phase-4 config are:

1. `no_cliff`: replace every event vector by `e(m)=m`; retain realized costs.
2. `no_curvature`: set exact `d=0` and recompute `a+b*m`; retain events.
3. `no_reset`: set exact `a=0` and recompute `b*m+d*m^2`; retain events.
4. `no_novelty`: replace each positive `16e+2` raw finding by `16e`; retain
   costs, events, caps, budgets, and saturation.
5. `unsaturated`: replace `H=200000` by `H=10^18`; retain everything else.

No factor may be retuned. The single batch uses exact final attempt
`experiments/runs/orf-p4-ablations-v1` and exact command:

```text
comp/.venv/bin/python -I experiments/orf-p4-ablations/run_ablations.py --config experiments/configs/orf-phase4-v1.json --baseline-tables experiments/orf-p4-baseline/score-tables.tsv --attempt-dir experiments/runs/orf-p4-ablations-v1
```

The bundle must include per-profile modified score tables sufficient for an
independent 4,800-row recomputation, a 15-row ablation-by-master table, canonical
summary, notes, owned log, and completion manifest. The runner/helper/frozen
config/support/baseline table/reviewed core runner and committed core evidence
must all be bound.

## Prediction and rationale

Numeric predictions are frozen together before implementation or execution:

| Ablation | Predicted mean gain | Confidence | Rationale |
|---|---:|---|---|
| `no_cliff` | 7% | low | Calibration-v2 no-cliff-only/H200k median was 6.991608265969%. |
| `no_curvature` | 35% | low | Cliffs and reset/linear heterogeneity remain; removing curvature should reduce but not erase action-scope value. |
| `no_reset` | 22% | low | Removing fixed overhead should push many smooth profiles toward small actions, while cliffs and curvature retain heterogeneity. |
| `no_novelty` | 40% | medium | Removing the additive two-point novelty term is small relative to `16e` and should leave the action ranking nearly unchanged. |
| `unsaturated` | 44% | medium | Calibration-v2 equal-weight median rose from 40.924155277025% at H200k to 44.204209608439% unsaturated. |

The expected attribution pattern is that cliff removal causes the largest loss,
no-reset/no-curvature cause intermediate losses, no-novelty is near the core,
and unsaturation is near or above the core. These are forecasts, not pass
thresholds; every valid result is kept and misses are reported.

Five unresolved `results.tsv` rows are appended now. A condition is invalid if
it changes any non-named mechanism, fails exact default-score/coefficient checks,
or publishes an invalid bundle. No scientific retry is allowed for an outcome.

Pre-implementation input hashes:

- config `e3ebe822094c91d6b6e83de6bc55324e43301b74df9a6e3bc3ee3e932b0ba748`
- support `fdc68ce08923be8d693155bb2641841a3a706164ebcb9d05e6a330a1d8c67fe9`
- baseline table `331e8b5e16b42d8781df68fd49aa9cd83a4d77c8f5ec0ab9de15e09137e59cbf`
- reviewed core runner `41aa108f5f18c60a7072666d32fe010b447a1617c7c5938a1f54573b01e74715`
- bundle helper `8c4b9cd3bf4ea0053e96a851b88a60bb6a92972b2e7f8a6e3a4c6bd91550aedd`
- core COMPLETE `a6630cde76050ed5c6a227bf79cc809d12ddcad14a9e67551ebd37123d3a2809`
- core summary `93e2030dbc1718947208ae041b5884046e0eb078a61815dee290d75946e77d88`

## Gate Check

- T025 returned `SOUND` with no findings at any severity before execution.
- The exact command exited 0 on its first invocation and published the exact six
  expected files with a verified `COMPLETE` manifest and all eight bindings.
- Independent audit checked all 4,800 ordered OAT rows, all 33,600 scores, all 15
  master aggregates, exact fractions/action counts, and every named-only
  transform against the 960 committed originals.
- Actual mean gains were no-cliff 7.622073949240%, no-curvature
  37.860007927303%, no-reset 18.973588191963%, no-novelty 40.094682770562%,
  and unsaturated 44.355152104598%.
- Deltas from the 40.249038022308% core were respectively -32.626964073068,
  -2.389030095004, -21.275449830344, -0.154355251746, and +4.106114082290
  percentage points. Every master in every condition remained above 5%.
- The eight immutable experiment paths have an empty diff from preregistration
  commit `e0b9520`; no retry or deviation occurred.

## Problem alignment

This batch identifies which environmental mechanisms produce the observed moat,
separating robust conditional structure value from a result driven by one
engineered cliff or scoring constant.

## Decision

**Keep.** The valid batch supports the frozen qualitative attribution pattern,
with cliff behavior dominant, reset overhead substantial, curvature modest,
novelty negligible, and saturation suppressing some conditional value.

## Next Steps

Commit the verified bundle and resolve the five ledger rows. Proceed to the
preregistered distinct-regime T020 generalization run; no held-out or Kaggle
action.

## Prediction vs. Reality

| Ablation | Predicted | Actual | Error (actual - predicted) |
|---|---:|---:|---:|
| `no_cliff` | 7.0% | 7.622073949240% | +0.622073949240 pp |
| `no_curvature` | 35.0% | 37.860007927303% | +2.860007927303 pp |
| `no_reset` | 22.0% | 18.973588191963% | -3.026411808037 pp |
| `no_novelty` | 40.0% | 40.094682770562% | +0.094682770562 pp |
| `unsaturated` | 44.0% | 44.355152104598% | +0.355152104598 pp |

All five numeric forecasts were directionally and quantitatively close. OAT
effects are not additive: cliff removal produced by far the largest loss;
removing reset was next; curvature removal was modest; novelty removal barely
changed the result; removing saturation increased it. This remains attribution
inside a purpose-built public synthetic environment, not evidence of live
factor prevalence.
