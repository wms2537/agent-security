# Experiment: ORF Phase-4 reviewed core

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed, confirmed and kept

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

- The exact command exited 0 on its first invocation and published the exact six
  expected files to the previously absent final attempt.
- Independent `verify_complete_bundle` returned `PASS`; manifest status is
  `COMPLETE`, its command/attempt/file set/bindings match exactly, and every
  artifact digest verifies.
- An independent TSV audit recomputed all 960 rows: adaptive scores
  `11,886,082`, `12,187,804`, `12,113,766`; global scores `8,403,762`,
  `8,824,632`, `8,579,258`; regrets `3,482,320`, `3,363,172`, `3,534,508`.
- Exact per-master gains are 41.437632336565%, 38.111186959411%, and
  41.198294770946%; their exact mean is 40.249038022308%.
- All three primary masters clear 5%; all three homogeneous records have exact
  zero regret, global length one, and 64/64 adaptive length-one choices.
- `run.log` has 11 lines with the canonical command first. Output mtimes span
  0.125 seconds, consistent with reported runtime 0.132034047 seconds.
- The eight immutable Phase-4 paths have an empty diff from preregistration
  commit `20b73f4`.

## Problem alignment

This run tests whether profile-conditioned structure selection has material
finite-table value against the exact strongest shared-action comparator, while
the homogeneous negative distinguishes genuine conditional regret from a
universal larger-action effect.

## Decision

**Keep.** The run satisfies every preregistered confirm rule and requires no
retry or deviation.

## Next Steps

Commit the verified bundle and resolved ledger. T018 may apply the user's advance
authorization because the baseline/core gates passed. No held-out or Kaggle
action becomes authorized.

## Prediction vs. Reality

The predicted mean was 40.0%; actual was 40.249038022308%, a difference of
`+0.249038022308` percentage points and inside the frozen `[30%,50%]` interval.
The predicted clear fraction and both homogeneous fractions were all `1.0`, and
all three actuals were exactly `1.000000000000`. Peak memory was 0.515918732 GB
and runtime was 0.132034047 seconds.

This confirms robust finite public-table conditional regret for the reviewed
action-scope change. It does not establish live-model heterogeneity,
learnability, private transfer, a live deadline, held-out performance, or Kaggle
performance.
