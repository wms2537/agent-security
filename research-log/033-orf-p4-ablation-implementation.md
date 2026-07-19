# ORF Phase-4 ablation implementation

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** implemented, unexecuted and pending sterile review

## Context

The numeric attribution predictions and exact five transforms were committed in
research-log/032 before implementation. Two delegated implementation attempts
were stopped without producing workspace changes, so the orchestrator
implemented the same frozen design directly. Neither attempt consumed a
scientific run or review budget.

## Content

`experiments/orf-p4-ablations/run_ablations.py` is a 715-line one-use runner. It:

- validates all seven frozen input/evidence hashes and the exact canonical
  command/attempt identity;
- opens the reviewed transactional bundle before reading or aggregating data;
- strictly parses all baseline identity, sequence, cost, event, and score fields;
- independently reproduces all default scores and recovers exact `a,b,d` from
  the quadratic costs before applying any transform;
- loads the reviewed core evaluator without modifying it;
- implements the five named OAT transforms and no other policy change;
- requires a 4,800-row modified-table artifact and 15 exact master summaries;
- recomputes the default reference and checks it against the committed core
  evidence; and
- binds the runner/helper/config/support/baseline/core-runner/core-COMPLETE/core-
  summary plus all attempt outputs.

The runner SHA-256 is
`568d285ab34e9fec5e8b5c808ebbe31a0fead84386dc9934bbbd53e3a002f933`.
The 150-line toy-test SHA-256 is
`a4036d1b10d6432c80af21788ba5c35c8d9c133e1afa5115cdaa1dc5fb9d362d`.

## Gate Check

- Static compilation passed for both files.
- `test_toy_ablations.py` returned `Ran 5 tests in 0.001s` / `OK` for exact
  coefficient recovery, immutable-support scorer parity, single-change
  invariants for every ablation, reviewed evaluator/tie behavior, and exact
  rendered schema width.
- `git diff --check` passes.
- `experiments/runs/orf-p4-ablations-v1` remains absent; no primary label was
  evaluated and no scientific output exists.

Local implementation checks pass, but new transform logic requires sterile
review T025 before the scientific batch.

## Problem alignment

The implementation exposes complete modified tables so each attribution result
can be independently recomputed rather than trusted from a summary.

## Decision

Commit the unexecuted runner/tests and dispatch a targeted evidence-validity
review.

## Next Steps

Run no primary data until T025 returns `SOUND`; then add the committed runner
hash to the execution checkpoint and invoke the exact command once.
