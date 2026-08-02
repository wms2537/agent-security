# Theory Review — Measured Density Fill Round 1

**Date:** 2026-08-02 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 10 · **Status:** needs-revision

## Context

Report 245 preregistered Measured Density Fill. The first sterile reviewer did not return a verdict and was interrupted; the second sterile reviewer returned the assessment below. The hypothesis review budget is charged to `15/32`.

## Gate Check

- Committed line-count evidence: `git show HEAD:research-log/245-hypothesis-iter-10-measured-density-fill.md | wc -l` -> `190`.
- Reviewer-reported line count: `190`.

## Verdict

```text
Status: DONE
Line count: 190
Blind assessment:
- Justification Correctness: fail — The hypothesis correctly narrows the failed component to “probe admission followed by blind dense emission” at lines 15 and 34, but the engineering bottleneck table at lines 93-98 does not give a measured bottleneck for every component. “Blank” v34/v36 outcomes are real failure evidence, but not a quantified bottleneck explaining why measured generation-side admission should fix hidden replay blanking; lines 28 and 108 explicitly admit the hidden replay boundary remains unidentified.
- Engineering Tests: fail — Planned checks exist at lines 93-98 and 168-178, but the “Density scoring” ablation is only a local threshold sweep and not a removal/fallback ablation of the scoring component. The implementation gate also leaves `dense_min_events`, caps, and stopping thresholds to be frozen later rather than preregistered here.
- Confounds: pass — Lines 103-110 explicitly cover selection, confounding, assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting.
- Taxonomy: pass — Lines 156-160 classify this as an Optimization Bottleneck / engineering replacement / replace+decouple. That is mostly accurate because the stated operation replaces blind dense replication with measured admission, rather than merely bridging two unrelated methods.
- Anti-stacking: pass — Lines 162-164 make a distinct prediction versus plain v35 fallback plus v36 dense prompts: candidate-level measured retention should produce a visible non-blank submission even when dense is attempted.
- Occam/Alternatives: fail — The file does not preregister a simpler first test, such as v35 fallback plus a very small capped number of measured dense candidates, or an admission-only local/live smoke variant before full fill-controller behavior. The closest controls are disable-branch fallback and no-fire fixtures at lines 95 and 97, but those do not test the simpler live alternative.
- Overall: NEEDS_REVISION

Exact issues with file locations:
- Lines 91-99: replace the “Measured bottlenecks” table with one row per implemented component that includes a numeric observed bottleneck, source artifact, and how the component targets that number.
- Lines 95-98: make every planned ablation a true removal/fallback ablation; the density-scoring threshold sweep is not enough.
- Lines 75-82 and 108: either justify why generation-side measured cost is a valid proxy for replay-safety, or narrow the claim so it only says “reduces blind emission,” not replay-cost control.
- Lines 146-150 and 168-178: freeze `dense_min_events`, dense cap, safety cap, and stopping threshold before implementation, not later in the implementation log.
- Lines 180-182: add an Occam-first alternative and explain why it is skipped or make it the first implementation target.
- Line 186: weaken “identifying a policy that increases expected score density while reducing blank-submission risk” to what one public score can support: evidence that one preregistered measured-fill submission was visible and above/below thresholds.

Actionable coaching:
- Add exact v34/v36/v35 source rows from `results.tsv` or `leaderboard_experiments.tsv`.
- Pre-register the smallest live measured-density variant first.
- Freeze all caps and thresholds in this hypothesis file.
- Keep the claim to first-submission predictive performance, not mechanism attribution.
- Add a true ablation for density scoring: measured dense disabled, measured dense admitted without score-rate stop, and no-fire fallback.
```

## Decision

Write a superseding hypothesis. The revision must narrow the claim, freeze all dense caps/thresholds, and make the first implementation a small capped overlay rather than a full measured-density controller.
