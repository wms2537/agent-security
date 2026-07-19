# Experiment: ORF Phase-4 reviewed core

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** preregistered, not run

## Context

T016 closed `SOUND` in sterile review round 3 after both provenance HIGHs were
repaired. T017 is the first and only primary execution of the reviewed
per-profile action-scope core. It reads the already committed public non-target
960-row baseline table; no held-out target, generator opening, beacon, network,
or Kaggle action is permitted.

## Design

For each of the three frozen primary masters, recompute `G` as the exact maximum
of the seven column totals and `A` as the sum of exact per-row seven-action
maxima, with smaller fill length breaking ties in both policies. The only policy
change is one global action per master versus one action per profile. Evaluate
three separately derived 64-profile homogeneous masters as the distinguishing
negative: both policies must select length one throughout and have zero regret.

The final attempt identity is exactly
`experiments/runs/orf-p4-core-v1`. The directory must be absent before execution.
The canonical command is exactly:

```text
comp/.venv/bin/python -I experiments/orf-p4-core/run_core.py --config experiments/configs/orf-phase4-v1.json --baseline-tables experiments/orf-p4-baseline/score-tables.tsv --attempt-dir experiments/runs/orf-p4-core-v1
```

The reviewed bundle must publish exactly `core-by-master.tsv`,
`homogeneous-by-master.tsv`, `core-summary.json`, `notes.md`, `run.log`, and
`COMPLETE.json`, with the completion manifest last and all bindings/artifacts
verified.

Pre-run bindings:

- core runner SHA-256:
  `41aa108f5f18c60a7072666d32fe010b447a1617c7c5938a1f54573b01e74715`
- bundle helper SHA-256:
  `8c4b9cd3bf4ea0053e96a851b88a60bb6a92972b2e7f8a6e3a4c6bd91550aedd`
- frozen config SHA-256:
  `e3ebe822094c91d6b6e83de6bc55324e43301b74df9a6e3bc3ee3e932b0ba748`
- immutable support SHA-256:
  `fdc68ce08923be8d693155bb2641841a3a706164ebcb9d05e6a330a1d8c67fe9`
- committed baseline table SHA-256:
  `331e8b5e16b42d8781df68fd49aa9cd83a4d77c8f5ec0ab9de15e09137e59cbf`

## Prediction and rationale

The primary prediction is mean adaptive gain **40%**, medium confidence, with a
confirmation interval of `[30%,50%]`. This was frozen in the Phase-4 config from
the untouched calibration-v2 distribution, before these three public labels
were evaluated adaptively. The distinguishing structural predictions are:

- all-three-primary-masters materiality-clear fraction: `1.0`, where clear means
  gain at least 5%;
- homogeneous zero-regret fraction: `1.0`;
- homogeneous all-row/global-length-one fraction: `1.0`.

`results.tsv` receives all four unresolved rows before execution.

Decision rules are fixed before the run:

- **confirm/keep:** valid verified bundle, mean gain in `[30%,50%]`, all primary
  masters at least 5%, and both homogeneous fractions exactly 1;
- **partial/prediction miss:** valid bundle and all masters at least 5%, but mean
  outside `[30%,50%]`; preserve the result and treat the numeric forecast as
  wrong;
- **disconfirm/stop:** valid bundle but mean below 5% or any master below 5%; do
  not advance through the pre-authorized checkpoint;
- **invalid/stop:** any input/bundle/hash/schema/arithmetic/control mismatch.

No retry is allowed for a scientific outcome. A failed invocation may be
diagnosed only under the already frozen two-fix-attempt limit and may never
reuse the same final attempt identity.

## Gate Check

- T016 is `SOUND` and the reviewed core remains unexecuted.
- The exact final attempt is absent.
- All five pre-run SHA-256 bindings match the reviewed/frozen values.
- The public primary labels, actions, thresholds, predictions, decision rules,
  command, and expected bundle are fixed before dispatch.

## Problem alignment

This run tests whether profile-conditioned structure selection has material
finite-table value against the exact strongest shared-action comparator, while
the homogeneous negative distinguishes genuine conditional regret from a
universal larger-action effect.

## Decision

Run the exact canonical command once, then independently verify the complete
bundle and recompute every reported aggregate from its TSV artifacts.

## Next Steps

Commit this preregistration and unresolved ledger rows, dispatch the one-use
public non-target core run, and stop before T018 unless all fixed gates pass.
