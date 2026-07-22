# AHCMS-24 implementation retirement and Phase-2 pivot

**Date:** 2026-07-23 · **Phase:** 3 → 2 · **Cycle:** 3 · **Iteration:** 3 · **Status:** completed

## Context

T060 froze and implemented the reviewed AHCMS-24 Phase-3 probe without running
its canonical scientific attempt.  T061 then obtained a fresh sterile code/spec
review.  Report 183 returned `NEEDS_REVISION` with three HIGH findings and one
MEDIUM finding, all independently reproduced in report 184:

1. the point-ledger cumulative clock begins after reset instead of at the
   historical pre-reset landmark;
2. the command line is printed from a literal rather than authenticated from
   the actual isolated process invocation;
3. per-unit staging is removed before all late validation and publication
   failures have closed; and
4. later evidence operations do not retain an inode-pinned canonical attempt
   descriptor.

The two allowed implementation corrections were already consumed in T060.
Report 185 froze a cohesive repair architecture without editing the runner or
tests, but the correction-limit extension was not supplied.  The SciAgent
keep/prune rule requires an experiment that cannot be made admissible within
its implementation-fix allowance to be classified `implementation_defeated`
and left behind.  Continuing the research goal is not permission to relabel a
third correction as a new experiment.

## Content

### What is retired

The retired object is specifically the committed **AHCMS-24 Phase-3 v1 evidence
implementation**:

```text
runner  experiments/poc/ahcms24_phase3_v1.py
tests   experiments/poc/test_ahcms24_phase3_v1.py
design  research-log/181-poc-ahcms24-design.md
review  research-log/183-ahcms24-poc-code-review-round-1.md
audit   research-log/184-ahcms24-poc-review-round1-audit.md
repair  research-log/185-ahcms24-poc-repair-design.md
```

The files remain in Git as auditable failed-work evidence.  They are not
deleted, rewritten, run, or admitted as a competition mechanism.

### What is not refuted

No fresh AHCMS scientific environment was constructed, no q-independent master
was drawn, and the canonical attempt directory
`experiments/runs/ahcms24-c3-poc-v1` does not exist.  Therefore there is no
valid observed AHCMS metric and no evidence that contradicts the reviewed
absorbing-stop hypothesis.  The correct search outcome is `inconclusive`, not
`refuted`:

```text
hypothesis status     scientifically untested
implementation status implementation_defeated
search-log outcome    inconclusive
scientific debug      0/3
implementation fixes  2/2 exhausted
```

This distinction matters.  It preserves the narrow scientific premise for a
future implementation only if the user later reopens its correction budget,
while preventing the defective code from influencing a Kaggle decision now.

### Why pivoting is the competition-beneficial choice

Running v1 would create numbers whose point ledger and provenance are known to
be wrong.  Repairing it without authority would violate the fixed SciAgent
budget.  Waiting would spend no evidence budget but would also stop progress.
The only honest productive branch is the fallback already frozen in report
185: return to Phase 2 and evaluate the next structurally different competition
strategy.

The remaining ordered portfolio is:

| Candidate | Role in the competition system | Existing evidence | Principal unresolved risk | Phase-2 treatment |
|---|---|---|---|---|
| Replay-safe core-first single-post floor | conservative incumbent/fallback that protects a valid result when higher-ceiling arms fail | public 84--89 expectation and strongest feasibility/evidence score in report 115 | may protect reliability without exceeding the current public frontier | compare as the first next strategy and mandatory control |
| Silent unique-domain wording as a raced arm | representation/termination change intended to reduce output and replay cost while keeping domain uniqueness | retained in report 115 as a separate arm, not a fixed universal policy | target response/scorer benefit is uncertain and wording gains may not transfer | compare against the floor with one-variable attribution |

These are not yet a new hypothesis.  T063 will first audit their exact committed
code, profile and public evidence against the current 69.570 incumbent, the
88.515 public author frontier recorded in Cycle 3, and the seven submission
confidence gates.  Only after that audit may one falsifiable hypothesis and a
new `search_log` entry be frozen.  This prevents a portfolio label from hiding
another component stack.

### Budget accounting

- Research iterations remain `4/5`.  This is a Phase-3 pre-science failure
  looping to Phase 2, not a Phase-5 re-entry or Phase-4 core-fail loop.
- Hypothesis reviews remain `12/12`.  T063 may perform deterministic evidence
  selection, but no new theory-review dispatch is allowed without an explicit
  extension.
- AHCMS scientific debug remains `0/3` because no scientific run occurred.
- AHCMS implementation corrections remain `2/2`; retirement does not reset or
  rename that allowance.

## Gate Check

Deterministic retirement verification checks all of the following in one pass:

- `state.json.phase == "2"` and T062 is done;
- exactly one next open task exists, T063 in Phase 2;
- the AHCMS Cycle-3 `search_log` outcome is `inconclusive`;
- `tried_and_failed` contains exactly one report-186 AHCMS entry classified
  `implementation_defeated`;
- the review budget remains `12/12` and research budget remains `4/5`;
- the canonical attempt is absent; and
- `results.tsv` and `experiments/attack.py` retain their pre-transition hashes.

Expected exact output:

```text
ahcms24_t062_retirement_check=PASS correction_limit=2/2 implementation=retired_implementation_defeated scientific_result=absent search_outcome=inconclusive phase=2 next_task=T063 canonical_attempt_absent=true results_immutable=true attack_immutable=true
```

## Problem alignment

This retirement prevents known-invalid local evidence from authorizing a
competition change, preserves the incumbent, and directs the last available
research capacity toward a structurally different candidate that must still
pass every source, mechanics, resource, structural, regression, target-derived
and submission-benefit gate in `PROBLEM.md`.

## Decision

Retire AHCMS-24 Phase-3 v1 as `implementation_defeated`, fill its search outcome
as `inconclusive`, preserve its scientific hypothesis as untested, and return
to Phase 2.  Do not run the AHCMS canonical command, modify the competition
attack, push a Kaggle kernel, or submit.

## Next Steps

1. T063 performs a deterministic evidence-and-mechanism audit of the
   replay-safe core-first floor versus the silent unique-domain arm and the
   current incumbent.
2. Freeze only the strongest one-variable competition hypothesis, with its
   complete-policy comparator, resource accounting, target bridge and explicit
   component-removal prediction.
3. Stop before theory-review dispatch if the review budget remains exhausted.
