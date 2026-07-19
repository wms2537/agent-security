# ORF Phase-4 code review round 2

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Verdict:** NEEDS_REVISION

## Context

This sterile re-review examined immutable repair commit `bb896ab`; dispatch
commit `5b30f21` changed only state/progress metadata. The reviewer was forbidden
from running either scientific runner or creating an attempt directory.

## Verbatim reviewer report

NEEDS_REVISION

Status: DONE. Target files match commit `bb896ab`; `5b30f21` changes only
state/progress metadata.

Code reviewed:

- `orf_bundle.py`: 478 lines
- `test_orf_bundle.py`: 246
- `run_baseline.py`: 446
- `run_core.py`: 742
- `test_toy_core.py`: 58
- Total code: 1,970 lines

Evidence/context reviewed:

- Frozen config: 107 lines
- Historical baseline evidence: 994 lines
- Research logs 023/026/027: 363 lines
- Total evidence/context: 1,464 lines
- Grand total: 3,434 lines

Checks run:

- Read-only static compilation: 5/5 files passed
- Bundle tests: 10/10 passed, including 24 injected boundaries
- Core toy tests: 4/4 passed
- Historical baseline evidence/config/support unchanged from `1b0a7c5`
- Core attempt and all core scientific outputs remain absent
- No baseline/core scientific runner was executed
- Worktree remained clean

Prior HIGH disposition: RESOLVED. The repair now creates staging and owned
`run.log` before science, writes and fsyncs artifacts only in staging, hashes
bindings and artifacts, writes canonical `COMPLETE.json` last, directory-fsyncs,
publishes with `renameat2(RENAME_NOREPLACE)`, self-verifies, and converts injected
failures into unverifiable failed siblings without `COMPLETE.json`.

### HIGH — attempt-path symlinks defeat exact identity enforcement

Affected code:

- `experiments/orf_bundle.py:97-104`
- `experiments/orf_bundle.py:194-201`
- `experiments/orf_bundle.py:286-290`

`_resolve_under()` resolves the supplied attempt path before checking it.
Consequently, the later `attempt.is_symlink()` check examines the resolved target,
not the path supplied by the runner.

Concrete mechanism:

1. Before the core run, create dangling symlink
   `experiments/runs/orf-p4-core-v1 -> alternate`.
2. `Path.resolve(strict=False)` converts the canonical attempt into absent direct
   child `experiments/runs/alternate`.
3. `AttemptBundle` publishes there successfully.
4. The manifest records identity `alternate`, while the canonical command still
   names `orf-p4-core-v1`.
5. `verify_complete_bundle()` resolves both supplied and expected paths through
   the symlink to `alternate` and accepts them as equal.

Thus a nonsymlink-path requirement and exact preregistered identity can both be
bypassed. The current expected path is absent and not contaminated, but the
implementation does not structurally preserve that guarantee through execution.
Existing tests cover ordinary identity mismatch but not symlink aliases.

Required repair:

- Inspect the raw direct-child path with `lstat`/`is_symlink()` before any
  resolution.
- For creation, reject any lexically existing entry, including dangling
  symlinks, using `lexists`.
- Compare the lexical canonical child path, not merely resolved targets.
- Add constructor and verifier tests for dangling and live symlink aliases;
  neither may publish or verify.

The remaining audit areas pass: no leakage or held-out action, exact split/seed
handling, correct Fraction metrics and tie rules, unchanged action-table fairness,
no training, exact bindings and file-set/hash/command checks.

Evidence is not yet sufficient for the Phase-4 gate because exact attempt
identity remains bypassable.

## Gate Check

The prior HIGH provenance issue is resolved, but the new HIGH lexical-identity
issue keeps T016 and T017 closed. No scientific evidence was generated.

## Problem alignment

The preregistered run identity is part of the evidentiary claim. Accepting a
symlink alias would allow the command label and published attempt identity to
refer to different lexical paths.

## Decision

Open T024 for a source-level lexical-identity repair and adversarial symlink tests.

## Next Steps

Reject dangling/live attempt aliases before resolution, compare lexical direct
children exactly, run only bundle/toy/static tests, then request another sterile
review. No scientific, held-out, network, or Kaggle action.
