# ORF fresh-bundle provenance fix

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** implemented and locally verified, scientific core unexecuted

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

Implementation is complete in `experiments/orf_bundle.py`, with synthetic tests
in `experiments/test_orf_bundle.py` and both future runners hardened. The helper
uses exclusive sibling staging, bundle-owned first-line logging, canonical
`COMPLETE.json`, exact file/binding/artifact verification, fsync, and Linux
`renameat2(RENAME_NOREPLACE)` with no overwrite fallback. Both future runners
open their transaction before scientific computation; the core command and
attempt identity are exact and preregistered.

Independent local verification after implementation:

- static compilation passed for the helper, tests, baseline runner, and core
  runner;
- bundle tests: `Ran 10 tests` / `OK`, including 24 injected structural failure
  boundaries plus success, repeat, corruption, missing, extra, malformed,
  noncanonical, binding-race, identity, and no-replace cases;
- core toy arithmetic: `Ran 4 tests` / `OK`;
- `experiments/runs/` still contains only the two historical support-calibration
  directories; the core and future-baseline final attempts are absent;
- the frozen Phase-4 config/support and all six historical baseline evidence
  files have an empty diff from `HEAD`.

The implementation gate passes. T016 remains closed until a fresh sterile code
review returns `SOUND`.

## Problem alignment

Scientific claims are meaningful only if a result bundle proves which exact
command, code, inputs, and outputs completed together; this fix prevents a failed
run from impersonating evidence for the candidate-structure policy.

## Decision

Keep the reusable protocol and both future runners for sterile re-review.

## Next Steps

Commit the verified source/test repair and re-dispatch the sterile code reviewer.
No scientific, held-out, network, or Kaggle action.
