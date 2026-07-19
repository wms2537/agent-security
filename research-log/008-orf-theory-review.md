# Online Replay Frontier — theory review record

**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** blocked at user checkpoint

## Round 1

The sterile theory-review dispatch was sent against
`research-log/007-hypothesis-iter-4.md` after the hypothesis was committed and
frozen. The dispatch consumed review round 1 as required.

**Returned status, verbatim:** `Agent errored: Request blocked.`

No blind assessment or coaching was produced, so there is no scientific verdict to
interpret and no hypothesis revision is permitted from this result. The hypothesis
remained unreviewed. A second and final sterile dispatch requested only
methodological review of the offline benchmark optimization claim.

## Round 2 recovery

The second dispatch consumed the final pre-registered review round at dispatch time,
as recorded in `state.json` and `research-log/progress.md`. On session recovery no
reviewer agent or reviewer result was available, and no blind assessment exists in
the workspace. This is therefore not a `RIGOROUS`, `NEEDS_REVISION`, or
`FUNDAMENTALLY_FLAWED` verdict; it supplies no scientific evidence about the
hypothesis.

## Gate Check

- Review accounting: `python -m json.tool state.json | rg -A2
  'hypothesis_review_rounds'` reports `"limit": 2` and `"spent": 2`.
- Verdict artifact: `rg -n 'RIGOROUS|NEEDS_REVISION|FUNDAMENTALLY_FLAWED'
  research-log/008-orf-theory-review.md` finds only this recovery statement, not a
  reviewer verdict.
- Phase-2 gate: **not passed**. No implementation or confirmatory experiment is
  authorized.

## Problem alignment

Holding the review gate prevents an unreviewed leaderboard mechanism from being
mistaken for the independently justified proprietary moat required by `PROBLEM.md`.

## Decision

Pause T009 at a user checkpoint. The user may explicitly authorize one replacement
review round for the infrastructure-blocked dispatches, or conclude this hypothesis
without implementation. The existing review budget is not changed automatically.

## User authorization

The user authorized the recommended single replacement review round verbatim:
“yes, go on”. In the immediately preceding checkpoint, “yes” referred to the stated
proposal to raise the T009 hypothesis-review limit from 2 to 3 because the prior
dispatches produced no scientific verdict. No other budget or external action was
authorized.

## Replacement round 3 dispatch

The sterile theory reviewer was dispatched against the unchanged, committed
`research-log/007-hypothesis-iter-4.md`. The replacement dispatch consumed the
authorized third review round. Its blind assessment must be verified before any
Phase-2 gate decision.

## Replacement round 3 returned verdict

The reviewer returned the following report verbatim:

Status: DONE

File reviewed: `research-log/007-hypothesis-iter-4.md` — **232 lines**, matching `git show HEAD:... | wc -l`.

### 1. Blind Assessment

#### Justification Correctness

**Verdict: NEEDS_REVISION.**

The bedrock chain is only partly established:

- SDK source verifies the 32-message limit, 2,000-candidate cap, separate 9,000-second generation/replay deadlines, reset-per-candidate replay, severity weights, and 200,000-raw cap.
- T005 establishes a 1.205× capacity change only on a controlled latency mock.
- T006 establishes multi-message score geometry and routing on controlled agents.
- Nothing cited establishes that real gpt-oss/Gemma have an exploitable intermediate optimum, that two latency probes safely predict replay capacity, or that the public curve orders private-guardrail outcomes similarly.

The central conditional claim is not logically supported. A “context reliability cliff” or “superlinear cost” alone does not imply a ≥15% gain over `{1,24}`. A cliff at 8 with negligible reset overhead can leave `m=1` optimal for both policies; a mildly superlinear curve can have an intermediate optimum less than 15% better than 24. The necessary margin conditions are missing at lines 80–84.

The objective also contains two incorrect or unstated “exactness” assumptions:

- At lines 50–53, `16e+2` is not generally the exact raw score of a finding. The scorer adds 2 per **globally unique cell hash**, not automatically per finding, and sums every predicate, not only EXFIL. The formula needs guaranteed unique hashes and exclusion/accounting of other predicates.
- At lines 55–66, the same observed `t⁺(m)` sizes generation and every replay. Yet probes observe public-generation timing, while candidates replay under public and hidden private guardrails. This transfer is not established.

The equations carry the proposed decision rule and are not merely decorative. The defect is semantic: calling the max of two timings a “conservative empirical bound” risks lending false safety to an in-sample extremum that has no future-coverage guarantee.

#### Mathematical Depth & Validity Domains

**Verdict: NEEDS_REVISION.**

Strengths:

- Symbols are mostly bound to gateway-observable quantities.
- The constrained-frontier interpretation at lines 73–76 is structurally meaningful.
- The entry correctly distinguishes empirical extrema from confidence intervals.

Load-bearing validity domains remain absent:

- persistence of reliability failure after the first failed length;
- approximate unimodality needed by the two-decrease early stop;
- stationarity from probes through fill and replay;
- public-to-private transfer of event yield, not merely timing;
- uniqueness of score-cell hashes across returned candidates;
- exclusivity or complete accounting of non-EXFIL predicates;
- a quantitative oracle margin large enough to imply the claimed 15% improvement after probe cost and estimation regret.

The max-of-two construction is especially weak. Under ordinary exchangeability, future samples frequently exceed an observed maximum of two; across hundreds or thousands of candidates it is not a defensible replay-time safety device. The 1% margin is asserted rather than calibrated.

#### Logical Soundness

**Verdict: NEEDS_REVISION.**

Major logical gaps:

- Lines 103–116 define profiles partly by their desired optimizer and outcome. “The exhaustive optimum lies at 4 or 8” plus “ORF improves by at least 15%” is close to constructing the conclusion, not predicting it.
- Exact simulator constants remain unset at lines 118–120. Therefore the claimed preregistration at lines 155 and 169 is incomplete, and effect sizes can still be selected after theory review.
- The external Kaggle test cannot identify the claimed mechanism, as the entry itself admits at lines 190–193.
- Stopping after a reliability failure at lines 67–69 assumes failures do not recover at longer lengths. Assumption 3 only discusses consecutive objective declines, not reliability-stop monotonicity.
- Local confirmation at lines 177–188 verifies behavior on constructed profiles, not the real-target claim at lines 80–84.

#### Assumption Completeness

**Verdict: NEEDS_REVISION.**

Missing assumptions that can invalidate the claim:

1. Public measurements preserve the private guardrail’s chain-length ranking and reliability sufficiently for aggregate four-cell optimization.
2. Probe latency remains representative through the fill and subsequent replay phases.
3. Score-cell hashes are unique across candidates whenever the `+2` term is applied.
4. Other predicates do not alter raw score, or are included explicitly.
5. Reliability does not recover after the first failed length.
6. The objective is sufficiently unimodal for the early-stop rule.
7. The best intermediate length exceeds the fixed-policy objective by enough to absorb estimation error, probing cost, and ORF regret while retaining a 15% net gain.
8. The four synthetic profiles and their equal weighting have a stated relationship to the intended target regime.

#### Taxonomy Verification

**Verdict: PASS, with a minor qualification.**

`Evidence Gap × Optimization/Search × replace` is defensible: the gap is an unmeasured live response curve, and the contribution replaces fixed routing with online selection. `Scope Mismatch` and `Resource Bottleneck` are plausible secondary labels, but the entry is not Bridge Opportunity × Synthesis/Unification, nor is it mislabeled to evade that tripwire. The heightened Bridge×Synthesis local-move requirement does not apply.

#### Anti-Stacking Check

**Verdict: PASS narrowly.**

The prediction at lines 205–209 genuinely distinguishes ORF’s intermediate action set from a plain combination of only the existing one- and 24-message components. Removing intermediate lengths is a valid anti-stacking ablation.

However, that ablation does **not** isolate online frontier identification. It tests whether intermediate actions help. A fixed `M=8` policy could produce the same gain on the selected cliff/superlinear profiles. This is an attribution and Occam defect, despite passing the formal anti-stacking gate.

#### Occam’s Razor Check

**Verdict: FAIL pending controls.**

Simpler explanations must be tested first:

- a fixed intermediate length such as 8;
- the best static length across profiles;
- exhaustive evaluation of only seven allowed lengths;
- a lookup rule based on the existing M=6 probe.

The current comparison conflates three changes: adding intermediate actions, measuring more lengths, and applying early-stopped optimization. With only seven lengths, the justification does not establish why the more fragile early-stop/max-of-two procedure is preferable to exhaustive probing.

#### Alternative Explanations

The predicted gain could arise because:

- the action set now contains M=8 or M=32, independently of online identification;
- the simulator constants were chosen to favor intermediate actions;
- a single fixed M=8 policy is already adequate;
- unique URL/cell construction increases novelty rather than the frontier rule;
- public timing differs from private replay behavior;
- timer order or remote-load drift favors one policy;
- timeout handling differs from the real gateway.

The missing-data statement at lines 165–166 is particularly problematic: a real replay deadline failure can invalidate/void the submission, not merely contribute one zero-event observation. The simulator and analysis must encode the whole-run consequence.

#### Fixed Bias-Surface Audit

All eight required labels appear, but several entries are substantively inadequate:

- **Selection, lines 155–157:** profiles are purpose-built and constants remain unset.
- **Confounding, lines 158–159:** ORF and control differ simultaneously in action set, probe count, and selection rule, preventing mechanism attribution.
- **Assignment, lines 160–161:** one deterministic seed plus alternating order does not quantify timing noise or drift.
- **Missing data, lines 165–166:** timeout-as-zero does not match the gateway’s invalidation behavior.
- **Measurement, lines 167–168:** the synthetic scorer checks mechanics but cannot support target-model or private-transfer claims.
- **Analysis flexibility, lines 169–171:** exact constants, replication count, estimator, ratio aggregation, and uncertainty handling are not fixed.

Protocol-deviation and selective-reporting provisions are adequate.

#### Overall

**NEEDS_REVISION**

Required fixes, ordered by severity:

1. **Lines 80–84, 103–120:** Replace the qualitative cliff/superlinearity antecedent with sufficient quantitative conditions, and lock every simulator constant before review. A qualitative curve shape does not entail a 15% effect.
2. **Lines 149–151, 190–193, 224–226:** Either establish and test public-to-private yield/ranking transfer or narrow the claim to the observable public/model-specific objective. Timing transfer alone cannot support the aggregate four-cell claim.
3. **Lines 55–71, 139–144, 182, 215–216:** Replace max-of-two plus an arbitrary 1% margin with a calibrated replay-risk design. Demonstrate that the returned candidate count satisfies the no-void constraint under timing noise.
4. **Lines 50–66:** Correct the score model to use set-level unique hashes and all predicates, or state and verify the uniqueness/exclusivity conditions that reduce it to `16e+2`.
5. **Lines 67–69, 145–148:** State and test the monotonicity/unimodality assumptions required by both early-stop rules, or exhaust all seven lengths.
6. **Lines 99–116, 180–183, 205–209:** Add best-static-intermediate and exhaustive-search controls. The present ablation isolates availability of intermediate lengths, not online identification.
7. **Lines 153–173:** Rewrite the bias-surface audit so each mitigation matches how that bias operates here; encode replay timeout as a whole-run failure and fully specify replication, ordering, estimator, and aggregation.
8. **Lines 177–220:** Separate “synthetic policy-mechanics validation” from “target-model predictive confirmation.” A single leaderboard result can be an external case study, not broad confirmation.

The approach is salvageable; its core idea is not fundamentally flawed.

### 2. Actionable Coaching

- Rewrite the prediction around an explicit margin decomposition: the oracle intermediate must beat `{1,24}` by a preregistered margin greater than ORF’s maximum probe cost, estimation error, and allowed regret. Then the 15% net claim follows from specified conditions rather than curve-shape rhetoric.
- Freeze a response-profile table now: reset overhead, per-turn latency, curvature/cliff location, event yield, timing noise, public/private shift, and expected oracle scores for every `m`.
- Use a factorial or held-out curve family rather than four handpicked exemplars. Report worst-case regret and profile-level results; do not rely solely on an arbitrary equal-weight mean.
- Compare: `{1,24}`, fixed M=8, best static `m`, exhaustive seven-length selection, ORF without early stopping, and full ORF. This isolates action-set, adaptation, and early-stop contributions.
- Model scorer output as
  `16·Σ_j e_j + 2·|{unique score-cell hashes}|`
  unless other predicates fire, in which case use the complete SDK predicate sum.
- For replay safety, estimate a one-sided bound on total replay cost under an explicit tail/stationarity assumption and stress-test bursty latency. If such a bound is unaffordable, narrow the contribution to score/regret and retain a separately validated conservative replay clamp.
- Simulate public and private curves separately. Pre-register concordant and discordant regimes; ORF should not claim aggregate benefit where the hidden private ordering reverses.
- If exhaustive probing is affordable for seven lengths, test it first. ORF’s early stopping earns its complexity only if it preserves exhaustive-search regret while materially reducing probe cost.

## Gate decision after replacement review

The adverse `NEEDS_REVISION` verdict stands. The reported line count is verified by
`git show HEAD:research-log/007-hypothesis-iter-4.md | wc -l`, which returns `232`.
The immutable hypothesis entry was not edited. The review budget is exhausted at
3/3, so T009 returns to a user checkpoint: Phase 2 remains closed and no ORF
implementation or confirmatory experiment is authorized.

## User authorization for final scientific re-review

The user approved the proposed final scientific re-review verbatim: “yes, go on, I
approve it”. In context, this authorizes a superseding ORF hypothesis and raises
only `hypothesis_review_rounds.limit` from 3 to 4. It does not authorize an
experiment, Kaggle push, or Kaggle submission.

## Final round 4 dispatch

The final sterile theory re-review was dispatched against the committed 346-line
superseding entry `research-log/009-hypothesis-iter-4-v2.md`. The dispatch includes
the prior eight-issue list in the template's allowed re-review slot and consumes
review round 4/4. The hypothesis is now immutable pending the verdict.
