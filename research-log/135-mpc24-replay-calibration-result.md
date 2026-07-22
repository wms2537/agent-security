# MPC-24 replay calibration audit result

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** completed — exploratory predictions confirmed

## Context

The audit was frozen at commit `8955330` with a calibration/holdout split,
structural proxy, exact predictions and blank `results.tsv` rows before its
single execution. It analyzes retained controlled data and cannot confirm an
official target claim.

## Exact execution

Command:

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_replay_calibration_audit.py
```

Output:

```text
mpc24_replay_calibration_audit=PASS
freeze_commit=121993c9b25c28d002803cd8f1a2c4af23bab158
output_commit=7bcd13b91eb8e28649067d20693cff3bcaae7c9b
provenance_dependencies=9
artifact_rows=360
scalar_1_10_violations_8_24=84/90
calibration_pairs=81
holdout_pairs=54
gamma=1.250000
kappa=6.250000
calibration_envelope_coverage=81/81
holdout_envelope_coverage=54/54
max_holdout_actual_to_proxy=0.801015756432
proxy_controller_select24=6/9
proxy_controller_select8=3/9
proxy_controller_ge_fixed8=9/9
proxy_controller_gt_fixed8=6/9
proxy_controller_to_fixed8_ratio=1.443010752688
prefix8_timing_scope=independent_proxy_not_nested_measurement
official_target_inference=none
runtime_s=0.025844213
```

Frozen script SHA-256:
`dd6e18ccf9562177ad245155ebf02605e19c04e2cc7b0ae136acf2176fd4f7c1`.

## Prediction versus reality

| Metric | Prediction | Result | Signal |
|---|---:|---:|---|
| held-out replay-envelope coverage | `1.0` | `54/54 = 1.0` | confirm |
| held-out cells MPC >= fixed-8 | `9/9 = 1.0` | `9/9 = 1.0` | confirm |
| proxy-valued MPC/fixed-8 aggregate | `>=1.10` | `1.443010752688` | confirm |

The same frozen proxy is used for selector choice and portfolio capacity. Actual
held-out replay costs grant no candidate capacity; they only test coverage.

## What changed in the model

V4 treated replay as `1.10*generation`, which underestimates 84/90 retained
8/24 pairs. The structural proxy is now

```text
r_proxy(m) = 1.25*c_generation(m) + 6.25*c_generation(1).
```

The second term represents a target-scaled candidate-boundary cost. It covers
all 81 calibration and 54 held-out controlled pairs. It is not a probability
bound for official target models.

## Provenance recovery

The audit reconstructs and verifies:

- frozen generating code/config commit `121993c9...`;
- output commit `7bcd13b9...`;
- runner/config/COMPLETE/run-log/samples/summary hashes;
- nine transitive mock-agent, environment, guardrail, predicate, scorer and
  cell dependencies at the freeze commit;
- recorded Python `3.14.3` environment metadata.

This closes the reproducibility gap without rewriting the historical bundle.

## Limitations

- calibration and held-out replicates share three authored profile families and
  masters;
- prefix-8 time inside a 24 path remains an independent-arm proxy;
- fixed-8 and MPC values are descriptive reuses of the same controlled artifact;
- no official target, private guardrail or leaderboard score was observed;
- `kappa=6.25` is an engineering envelope coefficient, not a calibrated target
  tail probability.

## Gate Check

- Frozen primary and secondary predictions: all confirmed.
- Status remains `exploratory`; these rows cannot confirm v5.
- Review budget remains `4/12`.
- Phase 3, attack implementation and Kaggle mutation remain closed.

## Problem alignment

The result replaces a systematically optimistic ledger with a measured,
boundary-aware proxy while preserving the observed 24/8 competition-value
signal under exact joint budgets.

## Decision

Use this proxy in a superseding v5 specification. V5 must make Phase 3 use new
masters and a new delayed-regression profile, freeze real fallback/ledger
ablations, make every online step observable and total, and narrow its primary
claim to controlled validation. An official `>69.570` claim remains downstream
and requires a separate confidence bridge.
