# ORF fresh-bundle provenance fix

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** in progress, scientific core unexecuted

## Context

Code review 026 passed scientific arithmetic and data hygiene but blocked the
phase because reusable output paths can retain stale or mixed evidence after a
failed invocation. T023 owns the branch-of-origin fix in experiment execution,
not a downstream prose disclaimer.

## Content

The revised execution contract is:

1. Every future run names one preregistered final attempt directory beneath
   `experiments/runs/`; it must not exist.
2. The runner creates one fresh sibling staging directory and owns its `run.log`,
   whose first line is the exact command.
3. All scientific outputs are written only inside staging. A failure preserves a
   uniquely named failed-attempt directory without `COMPLETE.json`; the final path
   remains absent.
4. On success, close the log, hash the runner, bundle helper, config, immutable
   support, committed baseline table, log, and every output artifact.
5. Publish canonical `COMPLETE.json` last, fsync files/directory, then atomically
   rename the staging directory to the absent final directory. Never overwrite a
   completed attempt.
6. A standalone verifier accepts only the exact expected file set and matching
   hashes. Missing, extra, corrupt, partial, or stale bundles fail.

The existing kept baseline remains historical evidence from commit `1b0a7c5`;
review 026 found its current artifacts internally consistent. The baseline runner
will be hardened for future invocations without rerunning or rewriting that
one-use result. The upcoming core run will use the new bundle protocol from its
first execution.

## Pre-specified structural tests

Toy-only temporary-directory tests must:

- inject failure before and between output writes and prove the final path is
  absent and no failed attempt verifies;
- publish a complete fake bundle and verify it;
- reject a second attempt without changing any completed-file hash;
- corrupt each artifact and reject verification;
- reject missing, extra, malformed-manifest, and mismatched-binding cases.

No test may read/aggregate `score-tables.tsv`, generate a Phase-4 master, or run
the core program.

## Gate Check

Pending implementation, deterministic/failure tests, and sterile re-review.

## Problem alignment

Scientific claims are meaningful only if a result bundle proves which exact
command, code, inputs, and outputs completed together; this fix prevents a failed
run from impersonating evidence for the candidate-structure policy.

## Decision

Implement the reusable protocol and harden both future baseline and core paths.

## Next Steps

Run toy/failure tests only, commit, and re-dispatch the sterile code reviewer.
No scientific, held-out, network, or Kaggle action.
