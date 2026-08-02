# Theory Review — Measured Density Overlay v2

**Date:** 2026-08-02 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 10 · **Status:** needs-revision

## Context

Report 247 superseded report 245 after the round-1 `NEEDS_REVISION` verdict. A sterile re-review was dispatched with the previous issue list.

## Gate Check

- Committed line-count evidence: `git show HEAD:research-log/247-hypothesis-iter-10-measured-density-overlay-v2.md | wc -l` -> `212`.
- Reviewer-reported line count: `212`.

## Verdict

```text
Status: DONE
Line count: 212

Previous issues:
1. IMPROVED — lines 107-115 add a component table, but line 113 still lacks a numeric observed generation-time bottleneck; it states the desired score-rate condition rather than an observed bottleneck.
2. RESOLVED — lines 109-114 now specify removal/fallback ablations per listed component, and lines 197-199 gate positive, no-fire, and score-rate-stop ablations.
3. RESOLVED — lines 19, 105, 116, 125, and 208 explicitly disclaim replay-cost/proxy claims and narrow to public-score prediction.
4. RESOLVED — lines 40-61 freeze min events, dense caps, safety caps, budget fraction, and stopping threshold before implementation.
5. IMPROVED — lines 183-190 add Occam alternatives and select the smaller overlay, but line 189’s rejection of single-post micro-tuning is weak because the live success threshold is >=90, not the public-leader target.
6. RESOLVED — lines 122 and 208 limit interpretation to one Kaggle public-score decision and target-owned evidence, not a general model claim.

New issues:
- Lines 111-113: measured-bottleneck evidence is still incomplete. “Blank” is categorical, and the score-rate row has no observed elapsed-time or generation-rate measurement supporting the 1.15x stop.
- Lines 19, 21-28, 153-158: the conditional claim depends on “enough multi-event dense candidates,” but the success bins do not require a minimum retained-dense count for interpretation.
- Line 181: anti-stacking distinction is not fully identifiable from the first public score; a plain v35 plus capped/unmeasured dense fallback variant could also predict visible completion or fallback.
- Line 189: Occam rejection of single-post micro-tuning needs evidence for the claimed single-post ceiling or must explain why a simpler >=90 attempt is not first.

Blind assessment:
- Justification Correctness: fail with evidence — line 113 substitutes a proposed score-rate rule for observed bottleneck evidence; line 189 uses a weak alternative rejection.
- Engineering Tests: fail with evidence — lines 107-115 improve component coverage, but not every component has numeric observed bottleneck evidence; line 113 is the clearest gap.
- Confounds: pass with evidence — lines 120-127 explicitly address selection, confounding, assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting.
- Taxonomy: pass with evidence — lines 173-178 characterize the change as replacing blind dense replication and decoupling dense discovery from replication.
- Anti-stacking: fail with evidence — line 181 distinguishes intent, but the first-score prediction is still not cleanly separable from a simpler v35+dense fallback combination.
- Occam/Alternatives: fail with evidence — lines 183-190 add alternatives, but the simplest single-post option is rejected on insufficiently aligned grounds.
- Overall: NEEDS_REVISION

Actionable coaching:
- Add observed elapsed-time/rate numbers for score-rate stop from a named artifact.
- Define how to interpret >=90 if dense-kept is zero or below a frozen minimum.
- Add a direct anti-stacking comparator: v35 plus unmeasured capped dense fallback.
- Either run single-post micro-tuning first or document evidence that it cannot meet >=90.
```

## Decision

Write a second superseding revision. Required changes:

- add a named local rate-profile artifact;
- raise success to strictly above the single-post ceiling;
- require a frozen minimum dense-kept count before overlay candidates are returned;
- add a direct unmeasured-capped-dense comparator;
- document the source-derived single-post ceiling.
