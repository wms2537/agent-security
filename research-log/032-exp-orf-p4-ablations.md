# Experiment: ORF Phase-4 attribution ablations

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** preregistered, implementation not started

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

- T018 advanced only after the exact baseline, SOUND code review, primary core,
  homogeneous controls, manifest, and independent audit passed.
- All five numeric predictions, mechanisms, labels, master set, action engine,
  command, final identity, expected evidence, and invalidity rule are fixed.
- The final ablation attempt is absent; no ablation score has been computed.

## Problem alignment

This batch identifies which environmental mechanisms produce the observed moat,
separating robust conditional structure value from a result driven by one
engineered cliff or scoring constant.

## Decision

Implement the five exact transforms and toy tests without evaluating the three
primary masters. Review the implementation before the one-use batch.

## Next Steps

Commit this preregistration, dispatch implementation only, freeze its source hash
after tests/review, then execute the exact batch once. No held-out or Kaggle
action.
