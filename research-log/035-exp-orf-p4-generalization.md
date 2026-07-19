# Experiment: ORF Phase-4 public generalization regime

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** preregistered, not generated or run

## Context

T020 is the frozen Medium-intensity generalization benchmark. It uses three
domain-separated public masters that are disjoint from the primary/core and
calibration labels, changes the resource regime to unsaturated, and balances
cliff presence by weighting no-cliff profiles four and cliff profiles one. No
held-out/beacon target is opened or approximated.

## Design

Generate exactly 320 profiles for each config-fixed preimage:

- `orf-public-phase4-generalization-v1|master|000`
- `orf-public-phase4-generalization-v1|master|001`
- `orf-public-phase4-generalization-v1|master|002`

using `SHA256(ASCII preimage)` and the immutable support generator. Score every
profile at `H=10^18`. Apply exact weight four where `cliff=-1` and weight one
otherwise, yielding balanced effective weight 256 no-cliff + 256 cliff per
master. `ADAPTIVE` takes a per-profile seven-action argmax; `PROBE_GLOBAL` takes
one seven-action argmax over weighted column totals. Both use the reviewed core
evaluator by exact row replication and smaller-length tie-breaking.

The exact final attempt is
`experiments/runs/orf-p4-generalization-v1`; the exact command is:

```text
comp/.venv/bin/python -I experiments/orf-p4-generalization/run_generalization.py --config experiments/configs/orf-phase4-v1.json --attempt-dir experiments/runs/orf-p4-generalization-v1
```

The bundle must contain a 960-row physical-profile score table with weights, a
three-row exact master result table, canonical summary, notes, owned log, and
completion manifest. Runner/helper/config/support/reviewed-core and committed
core evidence are bound.

## Prediction and rationale

The frozen primary prediction is mean generalization gain **35%**. Calibration
v2's 64 distinct balanced-cliff/unsaturated masters had minimum
31.742795824917%, median 35.872519911259%, maximum 40.000092337209%, and 64/64
cleared 5%. Before generating these labels, the confirm interval is fixed as
`[30%,45%]`, and the all-master-clear prediction is `1.0`.

- **confirm/keep:** verified bundle, mean in `[30,45]`, all three gains ≥5%;
- **partial/prediction miss:** all three gains ≥5% but mean outside the interval;
- **disconfirm/stop:** any master below 5%;
- **invalid/stop:** label/generator/weight/score/bundle mismatch.

Two unresolved `results.tsv` rows are committed now. No scientific retry is
allowed for an outcome.

## Gate Check

- T019 attribution was sterile-reviewed, executed once, and independently
  verified across 4,800 rows.
- Generalization labels, hashes, weights, H, N, prediction, interval, threshold,
  command, evidence set, and decision rules are fixed before generation.
- The exact final attempt is absent.

## Problem alignment

This checks whether the conditional-structure advantage survives both disjoint
public labels and a changed weighting/resource regime, instead of only the
primary construction.

## Decision

Implement and toy-test the exact regime without generating the three fixed
masters, then inspect the source before the one-use run.

## Next Steps

Commit this preregistration, implement the unexecuted runner, freeze its source
hash, and run the exact public batch once. No held-out or Kaggle action.
