# AHCMS-24 Phase-3 PoC code-review round-1 audit

**Date:** 2026-07-23 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 3 · **Status:** completed — execution remains closed

## Context

T060 committed the unexecuted AHCMS-24 runner and synthetic test surface. T061
required a fresh sterile source/specification review before the one-use
scientific command could become admissible. Lower-rung verification passed on
commit `d71040facee87ea0cd8e588f16eede8fad81944a`; dispatch commit
`ebffcdfad430807e3ef6454361a00e15fee08d2d` changed only state/progress.

The sterile reviewer wrote report 183 and returned `NEEDS_REVISION`. An adverse
review is evidence and cannot be discarded because the synthetic suite is
green. This audit independently checks the report rather than trusting the
reviewer's summary.

## Integrity verification

The review target line counts match committed HEAD: 1,703 runner lines and 716
test lines, 2,419 total. Report 183 has 308 lines and SHA-256
`65416cc10439208390509b755ee7accc205b32f3414239f6c35f9dcf64db638e`.
It contains one `DONE` status, an overall `NEEDS_REVISION` verdict, three HIGH
findings, one MEDIUM finding, per-checklist evidence, separate coaching, exact
commands, and an explicit no-science/no-Kaggle absence statement.

The main-agent source audit returned:

```text
ahcms24_review_round1_integrity=PASS verdict=NEEDS_REVISION findings=4 high=3 medium=1 reviewed_lines=2419 report_sha256=65416cc10439208390509b755ee7accc205b32f3414239f6c35f9dcf64db638e f1_boundary_reproduced=true f2_command_origin_gap_reproduced=true f3_retirement_order_reproduced=true f4_inode_gap_reproduced=true canonical_attempt_absent=true
```

`git diff --exit-code HEAD --` over both review targets, report 181, immutable
v5, config, ledger, and attack returned no diff. The only pre-record workspace
change was report 183.

## Finding dispositions

### F1 HIGH — inherited point-charge clock starts at the wrong boundary

**Accepted.** In `capture_generation_arm`, `calibrated_started_ns` is read only
after `generation_reset_complete`. In the bound historical `run_method_cell`,
`calibrated_generation_started` is read immediately after environment
construction and before `generation_reset`, so the inherited cumulative point
cost includes reset and both reset checkpoints. The prospective code therefore
undercharges every exact prefix. It can change longest-fitting acceptance,
true no-fit location, absorbing-tail support, accepted raw, every aggregate
metric, and CONFIRM/DISCONFIRM while remaining internally self-consistent.

This is the strongest blocker. Existing tests inject cumulative costs directly
and do not use a fake clock/reset to verify the historical point-clock origin.

### F2 HIGH — exact command provenance is asserted, not authenticated

**Accepted.** The runner validates config/attempt path strings but never checks
`sys.orig_argv`, isolated mode, or the interpreter identity. It writes the
frozen `EXPECTED_COMMAND` literal as the first log line. Direct import, missing
`-I`, a different interpreter, or different raw tokenization can therefore
produce a bundle claiming the frozen invocation. Source hashes do not prove
process invocation.

### F3 HIGH — staging is retired before all late failure surfaces close

**Accepted.** `run_scientific` calls `retire_capture_staging` before terminal
log construction/fsync, live-binding plus metric-log reload, and COMPLETE
publication. A late failure consumes the one-use attempt after its durable
per-unit recovery evidence has been deleted. This contradicts the recorded
failure-retention role of staging and the T061 gate.

### F4 MEDIUM — attempt-directory identity is not pinned

**Accepted.** Safe creation closes the original directory descriptor. Later
operations reopen the pathname, with no saved `(st_dev, st_ino)` or parent-entry
identity check. A concurrent rename/replacement can redirect later evidence or
publication to another same-path directory. Static pre-existing/symlink tests
do not exercise this race.

## Branch-of-origin routing

All four defects are owned by the Phase-3 evidence implementation. They do not
change the reviewed claim, thresholds, sample, profiles, controls, endpoint, or
transferability statement, so no Phase-2 hypothesis rewrite is justified.

One cohesive repair should:

1. move the point-charge origin before the reset checkpoint and add a fake-clock
   equality/one-quarter-nanosecond flip test;
2. authenticate the actual isolated interpreter and exact raw argv before
   attempt creation, with negative subprocess tests;
3. keep staged evidence recoverable across every pre-COMPLETE late failure and
   inject failures at log, live-binding, reload, retirement, and publication
   boundaries; and
4. pin the attempt transaction to its original directory descriptor/inode and
   reject a post-creation rename/replacement test.

The repair must preserve the existing complete-prefix, scorer, metric,
projection, and publication tests and must remain scientifically unexecuted.
A fresh sterile round-2 review of the committed repair is mandatory.

## Budget gate

Report 182 records that T060 consumed the full `2/2`
implementation-correction allowance. Scientific debug remains `0/3`; the
hypothesis-review extension and code-review judgment do not silently increase
the implementation-fix allowance. Under SciAgent's fixed-budget rule, the
orchestrator cannot authorize a third correction itself.

The recommended user decision is to raise the implementation-correction limit
from 2 to 4: one cohesive repair attempt plus one reserved fallback. If that is
not authorized, the current implementation must be retired as
`implementation_defeated` and the remaining research iteration used for a
different strategy. The canonical PoC cannot run in either case until a
committed repair receives `SOUND`.

## Gate Check

- Review integrity: **PASS**, command/output above.
- Review verdict: **NEEDS_REVISION**, three HIGH plus one MEDIUM.
- T061: **failed**; `SOUND` gate not met.
- Scientific attempts: **0/3**; canonical attempt absent.
- Frozen results/attack: unchanged.
- Kaggle action: none.
- Submission confidence: not passed.

## Problem alignment

Rejecting a self-consistent but source-misaligned and weakly authenticated PoC
protects the competition decision from false resource/benefit evidence; this
directly serves the mechanical-correctness, resource-safety, structural-evidence
and target-derived gates in `PROBLEM.md`.

## Decision

Do not execute AHCMS-24. Preserve report 183 verbatim, close T061 adverse, and
open T062 at the explicit implementation-correction budget checkpoint.

## Next Steps

1. Obtain an explicit implementation-correction extension from `2` to `4`, or
   retire this implementation and pivot.
2. If extended, repair all four findings as one source-bound change without
   scientific execution.
3. Run deterministic/adversarial checks, commit, and obtain a fresh sterile
   code/spec review before considering the canonical command.
