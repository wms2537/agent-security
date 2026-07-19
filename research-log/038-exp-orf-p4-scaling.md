# Experiment: ORF Phase-4 nested-scale robustness

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed, confirmed and kept

## Context

T021 is the final planned Phase-4 scientific run. It tests whether the material
direction depends on using all 320 primary profiles or remains present in
strictly nested 40- and 160-profile subsets. It reads the already committed
public baseline table and does not generate a new label.

## Design

For each of the three primary masters and each frozen replicate count `k` in
`[1,4,8]`, include exactly replicate indices `0..k-1` within every one of the 40
strata. This yields nested physical sets of 40, 160, and 320 profiles. On each of
the nine cells, run the reviewed exact adaptive-versus-global evaluator over the
same seven committed score columns and smaller-length tie rule.

The exact attempt is `experiments/runs/orf-p4-scaling-v1`; command:

```text
comp/.venv/bin/python -I experiments/orf-p4-scaling/run_scaling.py --config experiments/configs/orf-phase4-v1.json --baseline-tables experiments/orf-p4-baseline/score-tables.tsv --attempt-dir experiments/runs/orf-p4-scaling-v1
```

The bundle must contain nine exact cell records with A/G/regret/gain/actions,
canonical by-scale summary, notes, owned log, and completion manifest. It binds
runner/helper/config/baseline/reviewed core and committed core evidence.

## Prediction and rationale

The config-frozen primary metric is
`all_scale_master_cells_clear_fraction`, predicted **1.0**: all nine gains must
be at least 5%. The Phase-3 40-profile PoC gained 49.277%, the full primary cells
gain 38.111–41.438%, and calibration v2 cleared 64/64 default masters, so the
material direction is expected at every nested scale. Scale means and full cell
range are descriptive, not separately predicted.

- **confirm/keep:** exact clear fraction 1.0 and valid bundle;
- **disconfirm/stop:** any of nine cells below 5%;
- **invalid/stop:** any nesting/order/table/bundle mismatch.

One unresolved ledger row is committed before implementation/execution. No
scientific outcome retry is allowed.

## Gate Check

- T027 returned `SOUND` with no findings before execution.
- The exact command exited 0 on its first invocation and published the five
  expected files with a verified COMPLETE manifest and seven exact bindings.
- Independent audit selected/recomputed all nine cells from the bound baseline:
  1,560 selected row appearances, exact A/G/regret/gain/action counts, exact
  nesting, and full-scale equality.
- Mean gains are 48.952971791444% at N=40, 42.794164975019% at N=160, and
  40.249038022308% at N=320. The nine-cell range is
  `[38.111186959411%,52.609341554583%]`.
- All nine cells clear 5%, so the exact primary fraction is 1.0.
- Immutable paths have an empty diff from preregistration commit `a796796`; no
  retry or deviation occurred.

## Problem alignment

This tests whether the finite-table moat's direction is robust to evidence-set
size rather than appearing only after aggregating the maximum planned sample.

## Decision

**Keep.** Material direction is robust at every nested scale; magnitude declines
as the crossed design averages more replicates but remains near 40% at full N.

## Next Steps

Commit the verified bundle and resolved ledger, then perform T022's complete
Phase-4 provenance/results audit and comparison summary.

## Prediction vs. Reality

Predicted all-nine-clear fraction was 1.0; actual was exactly
`1.000000000000`. The scale means were deliberately descriptive rather than
numerically forecast. Runtime was 0.031398170 seconds and peak memory was
0.583507538 GB.

The decreasing mean is compatible with small-N strata exhibiting more realized
heterogeneity before replicate averaging. Because the subsets are nested rather
than independent, this is robustness evidence, not a learning curve or
population convergence estimate.
