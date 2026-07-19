# ORF Phase-4 code review round 3

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Verdict:** SOUND

## Context

This sterile review examined immutable repair commit `06239e3`; dispatch commit
`b70c4c2` changed only state/progress metadata. Scientific execution remained
forbidden.

## Verbatim reviewer report

SOUND

Status: DONE. Reviewed repair commit `06239e3`; dispatch commit `b70c4c2`
changes only `state.json` and progress metadata.

Code line counts:

- `experiments/orf_bundle.py`: 605
- `experiments/test_orf_bundle.py`: 366
- `experiments/orf-p4-baseline/run_baseline.py`: 446
- `experiments/orf-p4-core/run_core.py`: 742
- `experiments/orf-p4-core/test_toy_core.py`: 58
- Total code: 2,217 lines

Evidence/context line counts:

- Frozen config: 107
- Historical baseline evidence: 994
- Logs 026/027/028/029: 435
- Total evidence/context: 1,536
- Grand total: 3,753 lines

Checks performed:

- Read-only static compilation: 5/5 passed
- Bundle suite: 15/15 passed
- Core toy arithmetic: 4/4 passed
- Historical baseline evidence, config, and support are unchanged from
  `1b0a7c5`
- Scientific runners/config are unchanged from the previously audited `bb896ab`
- `git diff --check` passed
- Core attempt and all core scientific outputs remain absent
- `experiments/runs/` still contains only the two historical calibration runs
- Worktree remained clean
- No scientific runner was executed or scientific result aggregated

Severity findings: none.

Prior HIGH dispositions:

- Stale/partial reusable outputs: RESOLVED. Both runners enter a fresh bundle
  with an owned first-line log before scientific computation. Outputs remain in
  exclusive staging; files and log are fsynced and hashed; canonical
  `COMPLETE.json` is written last; publication is an atomic no-replace rename;
  failures are demoted to unverifiable siblings without `COMPLETE.json`.
- Symlink/lexical identity bypass: RESOLVED. Raw attempt paths retain lexical
  direct-child identity at `orf_bundle.py:104-141`. Construction rejects live
  and dangling entries using `lexists/lstat` at `403-425`. Verification
  independently rejects aliasing for both actual and expected paths and compares
  their lexical identities at `313-320`.

T024 falsification attempts passed:

- Live and dangling construction aliases fail.
- Alias targets remain untouched.
- Actual-path and expected-path verifier aliases fail.
- A symlink installed immediately before publication causes
  `RENAME_NOREPLACE` to fail; the target remains absent and staging becomes one
  failed sibling without `COMPLETE.json`.
- Verification opens directories and files with `O_NOFOLLOW`, binds the opened
  directory to the initial inode, requires regular stable files, rechecks named
  inode identity, and confirms final directory identity.
- Abort handling uses `lstat`, refuses changed identities, removes
  `COMPLETE.json` before demotion, and does not traverse aliases.

Scientific re-audit also passes:

- No tuning or held-out information reaches validation metrics.
- Exact public partitions, SHA labels, 960-row ordering, and homogeneous streams
  are enforced.
- `A`, `G`, per-master gain, mean ordering, inclusive threshold, tie-breaking,
  and homogeneous invariants remain exact.
- There is no training; the core changes only action scope over the identical
  frozen table.
- The baseline exhausts all seven actions and is not handicapped.
- Core bindings include the exact runner, helper, config, support, and committed
  baseline table; the manifest additionally hashes the owned log and every
  output.

Evidence is sufficient to close T016 and permit the separately authorized
public non-target Phase-4 core run. No held-out, beacon, Kaggle, network, or
external action is implied.

## Gate Check

T016 passes with a `SOUND` verdict after both HIGH findings were resolved and
retested. The core attempt remains absent at gate closure.

## Problem alignment

The reviewed implementation isolates the candidate-structure action-scope
change while binding the exact public inputs and outputs into one verifiable
attempt.

## Decision

Close T016 and permit preregistration of T017 under the existing public
non-target authorization.

## Next Steps

Append unresolved predictions and a run-specific record, commit them, then run
the exact canonical core command once. No held-out, network, or Kaggle action.
