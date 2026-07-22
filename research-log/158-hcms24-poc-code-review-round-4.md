# HCMS-24 Phase-3 PoC code review round 4

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Fixed commit:** `ec42e03` · **Status:** NEEDS_REVISION before execution

The fresh reviewer passed compilation and all 15 toys, confirmed a clean
worktree and absent attempt, and found two pre-run blockers.

## Findings

1. **HIGH — cumulative cost field is on the wrong TSV schema.** The runner
   declares `cumulative_costs_json` in `CANDIDATE_FIELDS`, not `PATH_FIELDS`,
   while path rows emit and reconstruction requires it. TSV filtering would
   silently drop the vector from every real path and write an unused blank
   candidate column. The candidate-cap-zero bundle toy did not exercise a
   nonempty path round trip.
2. **HIGH — returned generation decision has an asynchronous evidence-loss
   window.** Candidate selection and path append lack an immediate protected
   checkpoint. A timeout can lose the selected candidate or expose a returned
   path without its logical candidate. Exception-time reconstruction is not
   guarded, so that bijection failure can escape instead of yielding an
   invalid auditable cell.

The reviewer found the remaining policy reconstruction, replay-row
deduplication, completed-only exception timing, exact malformed-name equality,
status/provenance and log/COMPLETE ordering sound.

**Verdict: NEEDS_REVISION**

## Disposition

Move the field to `PATH_FIELDS`; add a real nonempty-path TSV round-trip; make
candidate decision plus path publication checkpointed and preserve a complete
decision snapshot; and guard exception-time reconstruction with deterministic
invalid fallback. Scientific attempts remain `0/3`; no attack or Kaggle action
occurred.
