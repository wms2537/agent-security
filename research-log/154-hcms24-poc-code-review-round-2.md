# HCMS-24 Phase-3 PoC code review round 2

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Fixed commit:** `34c62a4` · **Status:** NEEDS_REVISION before execution

A fresh read-only specification review inspected the immutable audit repair. It
ran only the 13 toy tests and did not create the canonical attempt.

## Final reviewer report (verbatim)

- HIGH — Reload reconciliation is not decision-complete. It trusts cell replay/validity fields and checks only three summary raw totals, without independently recomputing coverage, overages, invalidity counts, status, Williams/grid coordinates, or safety outcome from reloaded evidence (`experiments/poc/hcms24_phase3_v1.py:1564-1624`; requirement `research-log/153-hcms24-poc-audit-repair.md:24-28`). A constructor bug could therefore alter scientific admissibility while passing reload.

- HIGH — A nonzero derived `malformed_artifact_count` cannot produce the required invalid COMPLETE bundle: reload requires it to equal zero before stdout and `publish_complete` (`experiments/poc/hcms24_phase3_v1.py:1624`, `:2028-2044`), contrary to invalid-outcome publication semantics (`research-log/146-hypothesis-iter-7-hcms24.md:392-394`).

Prior blockers 1–3 are otherwise resolved: runtime/fixture bindings verify, emitted attribution/scorer evidence is independently usable, and exceptions link finalized partial rows. Reachable TSV round-trips, shell-redirection/tee synchronization, COMPLETE-last ordering, and the exact `3×3×4×4 = 144` primary cells plus one excluded safety cell are sound. All 13 toy tests passed; no scientific runner or canonical attempt was created.

**NEEDS_REVISION**

## Additional adverse-axis findings retained by the main agent

The evidence-semantics axis raised three credible defects that the repair must
also close rather than rely on the abbreviated aggregate report:

1. An exception during generation or replay can omit the active path,
   generated-but-unreplayed candidates, and current replay evidence because
   they have not yet reached the shared partial lists. The existing exception
   toy manually appends rows and does not exercise the real kernel loss point.
2. Candidate validation does not bind `generation_trace.user_messages` and
   `replay_trace.user_messages` to the emitted exact message prefix.
3. Reload must verify the exact frozen coordinate grid and safety coordinate,
   compare exception/cell coordinates, and recompute exception IDs rather than
   accepting ID membership alone.

## Disposition

Scientific execution remains forbidden. Repair all five items at their owning
logic and adversarial tests, then perform a fresh immutable targeted review.
Scientific attempts remain `0/3`; no attack or Kaggle action occurred. This
implementation review does not consume a hypothesis-review round.
