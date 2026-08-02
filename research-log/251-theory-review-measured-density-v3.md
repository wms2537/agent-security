# Theory Review — Measured Density Overlay v3

**Date:** 2026-08-02 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 10 · **Status:** needs-revision

## Context

Report 250 superseded report 247 after the round-2 `NEEDS_REVISION` verdict. A sterile v3 re-review was dispatched.

## Gate Check

- Committed line-count evidence: `git show HEAD:research-log/250-hypothesis-iter-10-measured-density-overlay-v3.md | wc -l` -> `191`.
- Reviewer-reported line count: `191`.

## Verdict

```text
Status: DONE
Line count: 191
Previous issues:
1. RESOLVED — lines 84-92 name report 249 and give the score-rate profile/ratios used for the `1.15x` stop; report 249 itself contains the elapsed/rate table.
2. RESOLVED — lines 46 and 60-62 freeze `MEASURED_DENSE_MIN_KEPT_TO_USE = 24` and discard overlay candidates below that; lines 116-130 define failure/partial/success interpretation.
3. RESOLVED — lines 136-144 define the plain v35 plus capped unmeasured dense comparator; line 178 makes it a required disabled local comparator.
4. RESOLVED — lines 77-83 derive the pure single-post ceiling as `90.000` and set success to `90.090`; lines 146-149 explicitly reject single-post micro-tuning under that threshold.
New issues:
- lines 34, 62, 67, 138: taxonomy is still overlay-plus-v35 fallback, i.e. a Bridge/Synthesis-style stack, not a clean replace/decouple mechanism.
- lines 138-142: anti-stacking distinguishers are local code invariants; the public-score part, visible `>=90.090`, is also what a plain capped v35+v36-style stack could predict. This weakens the one-future-Kaggle-score distinction from line 28.
- lines 46, 98-100, 148: the `24` dense-kept minimum is not mathematically tied to the success threshold. Using the file’s cited `0.130640` score/candidate and v35 `86.670`, `24` dense candidates imply about `89.805`, below `90.090`; if the intended yield is the report-249 dense4 `0.330`, state that directly and justify why `24`/`96` are smallest useful constants.
Blind assessment:
- Justification Correctness: fail with evidence — the single-post ceiling is well justified at lines 77-83, but the frozen dense minimum/cap is not justified against the success threshold at lines 46 and 148.
- Engineering Tests: fail with evidence — component ablations are planned at lines 96-101 and 174-180, but the minimum-kept component has no numeric bottleneck beyond “reviewer flagged zero-kept ambiguity” at line 100.
- Confounds: pass with evidence — lines 103-112 explicitly handle selection, confounding, assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting, while lines 28 and 92 avoid replay-safety overclaiming.
- Taxonomy: fail with evidence — lines 34, 62, and 67 keep v35 fallback and add an overlay before it, so this is not cleanly replace/decouple.
- Anti-stacking: fail with evidence — lines 138-142 distinguish by local no-fire/retention behavior, but the future public-score prediction is not uniquely separated from a plain capped dense-plus-v35 combination.
- Occam/Alternatives: fail with evidence — single-post micro-tuning is properly rejected at lines 77-83 and 146-149, but `24` kept and `96` cap are asserted as smallest useful without threshold math.
- Overall: NEEDS_REVISION

Actionable coaching:
- Recast the mechanism as replacing blind dense admission, or admit it is a stacked overlay and use the stricter Bridge/Synthesis framing.
- Add threshold math for `24` and `96`, using one declared per-dense expected score.
- Make the anti-stacking prediction depend on an outcome the unmeasured capped comparator would not also predict, or narrow it to a local engineering comparator only.
- Keep the single-post ceiling section; that repair is strong.
```

## Decision

Write v4. Required fixes:

- replace `MEASURED_DENSE_MIN_KEPT_TO_USE = 24` with a threshold-derived value;
- state that fallback is an inherited safety control, not the proposed component;
- make the distinguishing prediction an evidence package: local comparator plus public score, not public score alone.
