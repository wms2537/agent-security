# ORF Phase-4 generalization implementation

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** implemented, unexecuted and pending focused review

## Context

The design/predictions were committed at `6fc4df8`. A delegated implementation
attempt was interrupted after producing no workspace changes. The orchestrator
then implemented the same frozen design without generating a fixed master.

## Content

The 404-line runner validates all fixed hashes/config/labels, opens the
transaction before generation, uses the immutable support generator/scorer, and
passes exact row replication with weights 4/1 into the reviewed core evaluator.
It asserts 320 physical profiles, 64 no-cliff + 256 cliff, balanced effective
weight 256 + 256 = 512 per master, and emits 960 full score rows plus three exact
master records. Its SHA-256 is
`25f88db03417e7892481e55a76db0d8e7defa4b2c4966dbf2315315b1093b59f`.

The 84-line toy suite SHA-256 is
`10d61b0f604ebab11017a0348445d77651b5ad09ef9ece48502a7a1750009eaa`.

## Deviations and test repair

The first toy-only invocation failed two test fixtures: the manually typed
digest for the already frozen `...|000` label was wrong, and a handcrafted
three-column table was passed to the reviewed seven-action evaluator. No runner
or scientific output was produced. The fixtures were corrected to the computed
SHA-256 and seven columns; the scientific design was unchanged. This is one
implementation-test repair, not a scientific retry.

## Gate Check

- Static compilation passes for runner and tests.
- Final toy invocation: `Ran 5 tests in 0.000s` / `OK`, covering exact label
  hashing, crossed weight balance, replication/manual A-G equivalence,
  immutable unsaturated scorer behavior, and output schema width.
- Existing reviewed core toys remain 4/4.
- `git diff --check` passes.
- `experiments/runs/orf-p4-generalization-v1` is absent; the three fixed masters
  remain ungenerated/unscored.

Local implementation checks pass. T026 will review the new label/weight/evidence
orchestration before execution.

## Problem alignment

The runner changes both public labels and resource/weight regime while keeping
the exact reviewed action-scope comparison.

## Decision

Commit the unexecuted runner/tests and request focused sterile review.

## Next Steps

Do not generate the fixed masters before T026 is `SOUND`.
