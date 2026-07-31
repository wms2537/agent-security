# Stage B incumbent fallback guard

**Date:** 2026-07-31 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 8 · **Status:** completed local repair, remote not submitted

## Finding

Review of the submitted v33 artifact found that a weak probe (zero or one
EXFILTRATION event) would still fill with the two-call wording. That would make
the density experiment capable of discarding the known single-post floor before
the target had demonstrated a second event.

## Repair

The candidate admission rule now requires the selected probe to produce at least
two scored EXFILTRATION predicates. Otherwise the fill emits the proven plain
single-post candidate at the same fixed count. This is the fallback explicitly
required by the preregistration and does not add a competing optimization
component.

## Verification

```text
two PASS two_call inj_done 2
fallback PASS single_post_fallback call_syntax 0
fallback_notebook_contract=PASS direct_serve=PASS schema_rows=4
```

The two-event path still uses one user message and two distinct URLs; the
fallback path uses one user message and one URL. Both paths compile and produce
nonempty `AttackCandidate` objects. The rebuilt notebooks remain direct-serve
with the four-row `Id,Score` placeholder.

## Decision

Keep the current v33 target result as the measurement of the unguarded
preregistered artifact. Commit the fallback repair as the candidate v34
artifact, but do not submit it until v33 resolves; the next remote comparison
must keep the candidate count fixed and change only this admission guard.

## Problem alignment

The repair reduces void risk while preserving the incumbent control, directly
serving the competition objective of maximizing valid score rather than merely
maximizing local event density.
