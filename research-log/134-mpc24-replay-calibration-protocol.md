# MPC-24 replay calibration audit protocol

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** frozen before execution

## Context

Round 4 found that 84/90 retained 8/24 pairs exceed the v4 scalar replay
proxy `1.10 * generation_time`, while the descriptive 1.507 ratio used actual
future replay measurements. V4 is immutable and rejected. Before v5, one
read-only exploratory audit will test a structural online proxy against a
held-out replicate split of the already-retained controlled artifact.

This is the first exploratory evidence audit in Cycle-3 research iteration 2.
It cannot confirm an official claim.

## Frozen model

The replay proxy separates message-processing scale from fresh-candidate
boundary overhead:

```text
r_proxy(m) = gamma * c_generation(m) + kappa * c_generation(1)
gamma      = 1.25
```

Replicates `0,1,2` calibrate `kappa`. For each profile/master/arm in
`{1,8,24}` compute

```text
residual = (r_actual(m) - gamma*c_generation(m)) / c_generation(1).
```

`kappa` is the maximum positive calibration residual, enlarged by 25%, then
rounded upward to the next `0.25`. Replicates `3,4` are held out from this fit.

The structural interpretation is concrete: `gamma*c_m` scales message work;
`kappa*c_1` represents a target-scaled fresh-environment boundary term. It is a
controlled-profile envelope, not a target probability bound.

## Frozen predictions

Primary audit prediction, high confidence:

```text
heldout_envelope_coverage = 1.0 across 54 held-out profile/master/replicate/arm pairs
```

Secondary competition-value predictions, low confidence:

```text
proxy controller selects 24 in 6/9 and 8 in 3/9 cells
proxy controller is >= fixed8 in 9/9 held-out cells
proxy controller/fixed8 aggregate ratio >= 1.10
```

The controller portfolio must use `r_proxy` both to select and to evaluate
capacity. Actual held-out replay costs are used only to score envelope coverage,
never to grant candidate capacity.

Disconfirm any prediction at its literal threshold. A coverage miss rejects
this proxy. A value miss retains the proxy candidate but removes MPC's measured
advantage and favors fixed-8.

## Provenance contract

The audit binds:

- pre-run freeze commit `121993c9b25c28d002803cd8f1a2c4af23bab158`;
- output commit `7bcd13b91eb8e28649067d20693cff3bcaae7c9b`;
- runner, config, COMPLETE, run log, samples and summary hashes;
- mock agents, environment builder, public guardrail, env API/sandbox,
  predicates, scorer and cell source at the freeze commit;
- recorded Python `3.14.3`, Linux platform, runtime and memory from summary.

This reconstructs the generating state without modifying the old COMPLETE
artifact.

## Exact command

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_replay_calibration_audit.py
```

The script is frozen but unexecuted at this record. It writes no files, imports
no model service, performs no Kaggle action and reads only committed evidence.

## Gate Check

- Prediction recorded before execution: complete.
- Calibration/holdout split and proxy formula: frozen.
- Existing v4 remains immutable.
- Review budget remains `4/12`; no dispatch.
- Phase 3, attack implementation and Kaggle mutation remain closed.

## Problem alignment

A replay proxy consistent with source-authentic measured costs is necessary
before message-density gains can be treated as feasible competition value.

## Decision

Commit the protocol, unexecuted audit and blank prediction-ledger rows. Then run
the exact command once and accept its signal.
