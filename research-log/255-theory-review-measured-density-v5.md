# Theory Review — Measured Dense Replacement v5

**Date:** 2026-08-02 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 10 · **Status:** rigorous

## Context

Report 254 superseded report 252 after the round-4 `NEEDS_REVISION` verdict. A sterile v5 re-review was dispatched with the remaining issue list.

## Gate Check

- Committed line-count evidence: `git show HEAD:research-log/254-hypothesis-iter-10-measured-density-overlay-v5.md | wc -l` -> `197`.
- Reviewer-reported line count: `197`.

## Verdict

```text
Status: DONE
Line count: 197
Previous issues:
1. RESOLVED — scoring units are now consistent: single-post event candidate is `0.090`, four-event dense is `0.330`, and the 2,000 single-post cap is corrected to `180.000`, not `90.000` at lines 9-13.
2. RESOLVED — the 20% fallback-displacement model is recomputed in one unit: `0.8 * 86.670 = 69.336`, dense candidate `0.330`, and `ceil((100 - 69.336) / 0.330) = 93` at lines 67-75.
3. RESOLVED — cap `96` is justified as a three-candidate slack margin above the derived minimum `93`, with resulting score math shown at lines 77-82.
4. RESOLVED — non-threshold constants are separated as operational defaults at lines 49-58, and the score-rate gate is explicitly excluded from threshold math at lines 88-95.
New issues: none
Blind assessment:
- Justification Correctness: pass with evidence from corrected scoring unit and threshold math at lines 9-15 and 65-84.
- Engineering Tests: pass with evidence from component table and ablation/comparator plan at lines 96-104, plus confidence gates at lines 176-189.
- Confounds: pass with evidence; selection, confounding, assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting are explicitly listed at lines 123-132.
- Taxonomy: pass with evidence; this is framed as Optimization Bottleneck / Engineering replacement / replace at lines 105-113.
- Anti-stacking: pass with evidence; inherited v35 fallback is not claimed as novelty, and local no-fire, positive, and capped-unmeasured comparators are specified at lines 113-121.
- Occam/Alternatives: pass with evidence; single-post micro-tuning is called simpler and not source-impossible, but deferred based on latest live evidence at lines 152-154.
- Overall: RIGOROUS

Stress-tested bottlenecks/components/confounds: blind dense replacement, candidate-level measured retention, minimum dense threshold, score-rate gate, inherited fallback dominance, replay selection risk, assignment uncertainty, and selective reporting.

Strongest objection considered: the public score cannot attribute mechanism because fallback may dominate or measured candidates may fail replay. That objection does not defeat rigor here because the file explicitly admits it at lines 121 and 125-130, scopes the claim to one future public result plus local ablations at line 27, and predefines failure/partial/success bins at lines 134-150.

Actionable coaching:
- Implement only the frozen constants and gates in this file.
- Keep v35 fallback labeled regression control, not novelty.
- Do not patch the 20% displacement assumption after seeing the result.
- Preserve v34/v36 blanks as negative evidence in the final ledger.
```

## Decision

Phase 2 passes for Iteration 10. Proceed to Phase 3/4 local implementation gates using only the frozen constants and confidence gate in report 254.
