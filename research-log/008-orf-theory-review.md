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

## Final round 4 returned verdict

The reviewer returned the following report verbatim:

Status: DONE

File reviewed: `research-log/009-hypothesis-iter-4-v2.md` — **346 lines**, matching both `wc -l` and `git show HEAD:research-log/009-hypothesis-iter-4-v2.md | wc -l`.

### 1. Blind Assessment

#### Justification Correctness

**Verdict: NEEDS_REVISION.**

I independently re-derived the frozen arithmetic. Under the stated model:

- Best-static means are `{14,535; 21,666.5; 32,868; 40,820; 36,184.5; 44,390; 51,914}`, so `m=32` is correct.
- ORF selects `{1,32,8,4}` and scores `{14,100; 152,250; 47,934; 64,080}`, mean `69,591`.
- Oracle mean is `71,851.5`; the claimed `34.05%` static gain and `3.15%` regret are correct.
- The P4 derivation at lines 315–322 is correct.
- The lognormal parameterization at lines 164–167 indeed has mean 1 and CV 0.10.

However, the central quantitative antecedent is circular. At lines 80–92,

`S_oracle - D_ORF ≥ 1.20 S_best-static`

with `D_ORF = S_oracle - S_ORF` reduces exactly to

`S_ORF ≥ 1.20 S_best-static`.

Why should this count as a mechanism-based sufficient condition when it is algebraically identical to the desired conclusion? It does not derive the effect from independently knowable response-curve properties, probe cost, or an estimation-error bound. This is mathiness: the equation appears to justify the 20% claim but merely restates it.

The score model at lines 40–54 is now correct in structure: full set-level scoring is primary, and `16e+2` is restricted to explicit uniqueness/exclusivity conditions. The adaptation control is also substantially improved: ORF and the best static comparator share the same seven actions.

The remaining empirical problem is that the four deterministic profiles are constructed with known heterogeneous optima and then analytically scored. Running them can catch an implementation bug, but it cannot establish that a relevant public-model response curve exists. The frozen “confirmation” is therefore a unit test of a predetermined table, not target-model predictive evidence.

The replay-risk design remains insufficiently calibrated. The 0.90 clamp is motivated by one non-void submission, while the CV 0.10 lognormal model has no cited empirical calibration. The result is extremely sensitive to dependence: independent per-candidate noise averages away over hundreds of candidates, whereas run-level correlated drift can create substantial timeout risk. The entry neither specifies that dependence structure completely nor derives the clamp from a target void probability.

#### Mathematical Depth & Validity Domains

**Verdict: NEEDS_REVISION.**

Most notation is now bound to concrete quantities. `Q(A)`, `q(m)`, candidate count, generation cost, replay allowance, cap, and regret all have operational meanings. The equations at lines 62–69 carry the decision rule rather than decorating it.

The exception is the oracle-margin equation at lines 80–92. `D_ORF` is defined using the outcome it is supposed to justify, so it is not an independently measurable error or tax bound.

The validity-domain section at lines 220–249 is much stronger and correctly limits:

- reduced-score exactness;
- within-run stationarity;
- synthetic deterministic compliance;
- action-set affordability;
- measured-clamp coverage;
- public observability;
- profile-suite scope;
- score saturation.

But the stochastic domain remains incomplete:

- Is each `Z` independent across candidates, lengths, phases, and profiles?
- Is there any shared run-level or temporal component?
- How are common-random-number traces indexed when policies consume different candidate counts?
- What empirical evidence makes CV 0.10 the relevant regime?
- What target void probability is the 0.90 clamp intended to control?

Without these, the noisy result is not reproducible from the prose and its operating envelope is underdefined.

#### Logical Soundness

**Verdict: NEEDS_REVISION.**

The core mechanism is logically plausible: heterogeneous profile optima plus sufficient oracle advantage can let online selection recover more than its probe tax, and the same-action-set static control isolates adaptation from action availability.

Two leaps remain:

1. Lines 80–92 assume the desired effect through the definition of `D_ORF`.
2. Lines 94–96 call the claim “public/model-specific,” but the primary profiles are constructed local profiles. Lines 161, 230–232, and 329–331 correctly admit that they do not establish target-model behavior. The main claim should use the same synthetic-mechanics language.

The decision thresholds also overlap at exactly 5% aggregate regret: lines 279–285 permit confirmation at `≤5%`, while lines 287–290 describe `5–10%` as inconclusive. Exact boundaries must be disjoint.

#### Assumption Completeness

**Verdict: NEEDS_REVISION.**

The eight listed assumptions cover most internal mechanics. Still missing or insufficiently specified are:

- a profile-generating or sampling process that is independent of the desired ORF result;
- the stochastic dependence structure of timing noise;
- an evidence-based basis for CV 0.10 and the 0.90 clamp;
- exact trace-indexing and substream derivation;
- a target void-risk criterion and uncertainty bound on that risk;
- an explicit distinction between synthetic implementation confirmation and live public-model predictive confirmation in the claim itself.

Violation of profile heterogeneity invalidates the benefit entirely: if one length dominates the target distribution, ORF loses to it through probe tax. Violation of timing stationarity or independence can invalidate the void analysis even while score-selection mechanics remain correct.

#### Taxonomy Verification

**Verdict: PASS.**

`Evidence Gap × Optimization/Search × replace` matches the actual gap and contribution. ORF replaces a fixed action with exhaustive online response measurement and selection. This is not Bridge Opportunity × Synthesis/Unification, nor is “replace” being used to conceal an integration move.

#### Anti-Stacking Check

**Verdict: PASS, conditionally.**

The same-full-action-set static `m=32` control at lines 305–311 is genuinely distinguishing. Merely adding intermediate lengths does not predict both the 20% aggregate margin and the sequence `{1,32,8,4}`. This resolves the earlier action-availability confound.

The anti-stacking pass does not rescue the evidentiary weakness: the distinguishing outcome is hard-coded into the constructed profile table rather than predicted on an independently generated or observed curve set.

#### Occam’s Razor Check

**Verdict: FAIL for the present empirical framing.**

For these exact deterministic profiles, a simpler account predicts the entire result: evaluate the frozen table directly. No empirical run is needed except as software verification.

The scientifically meaningful hypothesis is narrower and harder: response-profile heterogeneity exists on the live public target, persists long enough for probing to inform filling, and has enough margin to repay exhaustive probing. The current deterministic suite does not test that proposition.

A necessary negative consequence is also clear: on a homogeneous or single-dominant profile distribution, ORF should underperform the best static action by approximately its charged probe tax. That boundary should be a first-class control.

#### Alternative Explanations

The predicted local gain can arise because:

- the four profiles were explicitly chosen to have different optima;
- equal weighting makes rare or artificial regimes as influential as plausible common ones;
- the constants were selected with the complete analytic outcome visible;
- any exact exhaustive optimizer would produce the same result;
- an oracle lookup keyed to known simulator identity would remove probe cost;
- the independent, light-tailed noise model makes the replay clamp appear safer than correlated or bursty latency would;
- unique-hash construction, rather than structure selection, could inflate raw if its assertions fail.

The same-action-set static control rules out “intermediate lengths alone” as the local explanation, which is a real improvement.

#### Fixed Bias-Surface Audit

All eight required surfaces appear, so the audit is not formally partial. It remains substantively incomplete in three places:

- **Selection, lines 253–254:** freezing purpose-built profiles prevents post-run dropping but does not address choosing profiles and equal weights to guarantee heterogeneous optima.
- **Protocol deviation/analysis flexibility, lines 262–272:** the entry claims commands are fixed, but no commands are listed. Stochastic trace indexing, substream derivation, simulator version, and exact paired-bootstrap resampling algorithm remain open.
- **Measurement, lines 267–269:** SDK scoring validates score mechanics, but constructed profiles cannot measure live public-model curve existence. The claim must not call that model-specific confirmation.

Missing-data handling is now correct: timeout and crashes remain whole-run zeros.

#### Previous-review issue disposition

| Prior issue | Disposition | Re-review judgment |
|---|---|---|
| 1. Quantitative antecedent and frozen constants | **IMPROVED** | Constants and expected scores are frozen, but lines 80–92 replace the qualitative antecedent with a tautology, not an independent sufficient condition. Purpose-built profiles remain outcome-constructed. |
| 2. Public/private transfer or claim narrowing | **RESOLVED** | Lines 94–96, 183–196, 216–218, and 292–294 exclude hidden-private transfer from confirmation and treat Kaggle as a case study. |
| 3. Calibrated replay risk/no-void | **IMPROVED** | False max-of-two coverage is removed; timeout is a whole-run zero. The 0.90 clamp, CV 0.10, dependence model, and ≤2/200 criterion are not calibrated to a stated risk target. |
| 4. Exact set-level score model | **RESOLVED** | Lines 40–54 define the full SDK score and restrict `16e+2` to checked uniqueness/exclusivity conditions. |
| 5. Early-stop assumptions | **RESOLVED** | Both early stops are removed; all seven lengths are exhausted. |
| 6. Best-static and exhaustive controls | **RESOLVED** | ORF itself is exhaustive, every fixed length is reported, and the primary control is the best static action over the full set. |
| 7. Bias audit and full protocol | **IMPROVED** | Replication, pairing, estimator, aggregation, and whole-run timeout semantics are present, but selection mitigation and stochastic implementation details remain inadequate. |
| 8. Synthetic versus target confirmation | **RESOLVED**, with wording correction needed | The staging is explicit and Kaggle is not broad confirmation. “Public/model-specific” at line 94 should be replaced with “synthetic policy-mechanics.” |

#### New issues introduced by this revision

1. **Circular oracle-margin condition, lines 80–92:** the antecedent is algebraically the conclusion.
2. **Deterministic confirmation is analytically predetermined, lines 117–157 and 313–327:** it supplies implementation verification, not empirical evidence.
3. **Unspecified stochastic dependence and clamp calibration, lines 159–181 and 226–240.**
4. **Claim-language mismatch, lines 94–96:** “public/model-specific” exceeds what the constructed profiles measure.
5. **Unsupported evidence references, lines 50, 109–111, and 237–240:** the SDK scorer and non-void v2 observation need direct source/artifact citations in the evidence chain.

#### Overall

**NEEDS_REVISION**

Required fixes, ordered by severity:

1. **Lines 80–92, 198–218, 313–327:** replace the circular condition with a decomposition using independently specified quantities, such as an oracle-static margin minus separately bounded probe, selection, and estimation losses. Treat the frozen table as a deterministic theorem/unit test, not confirmatory empirical evidence.
2. **Lines 117–157, 244–246, 251–275:** add an independently generated or held-out profile family, or preregister target-derived public response curves before evaluating ORF. Define the sampling/weighting rationale and include a homogeneous/single-dominant negative-control regime.
3. **Lines 159–181, 226–240:** fully specify timing dependence, trace indexing, and substream derivation; calibrate CV/tails from measured traces; derive the 0.90 clamp for a stated target void probability; report a confidence bound on void risk rather than treating ≤2/200 as a guarantee.
4. **Lines 94–96 and 329–340:** label local confirmation consistently as synthetic policy-mechanics validation. If a public/model-specific claim is desired, add a preregistered target trace test that can confirm or disconfirm curve heterogeneity before the external leaderboard case study.
5. **Lines 50–54, 237–240, 267–269:** cite the exact SDK source and measured profile artifacts supporting scoring, budgets, and clamp motivation.
6. **Lines 262–272 and 287–290:** freeze actual commands/software versions/bootstrap algorithm and make all confirm/inconclusive/disconfirm boundaries non-overlapping.

### 2. Actionable Coaching

- Recast the deterministic section as a proposition: given frozen response tables and exact costs, exhaustive ORF returns the analytically derived choices and scores. Use the simulator only to verify implementation equivalence.
- State a non-circular sufficient condition. For example, define an oracle-static margin `M`, an independently bounded probe loss `B_p`, selection loss `B_s`, and estimation loss `B_e`; require `M-(B_p+B_s+B_e) ≥ 0.20 S_static`.
- Build a preregistered response-curve generator with held-out seeds and regimes spanning one dominant optimum, several optima, cliffs, smooth curves, saturation, and correlated latency shocks. Use calibration profiles only to set the clamp; evaluate the hypothesis on untouched profiles.
- Model latency hierarchically: candidate-level variation plus shared run-level drift and burst events. Choose `R` so an analytic, bootstrap, or simulation upper confidence bound on `P(total replay > 9000)` lies below a declared tolerance.
- If external submissions are scarce, preserve one as a case study but log the public search trace, chosen length, candidate count, measured costs, and static counterfactuals. Do not use leaderboard delta alone to identify the mechanism.
- Add direct evidence links to the SDK scorer, T005 clamp result, and T006 score-geometry result so the justification chain is auditable from the entry.

## Gate decision after final review

The adverse `NEEDS_REVISION` verdict stands. The reported line count is verified by
`git show HEAD:research-log/009-hypothesis-iter-4-v2.md | wc -l`, which returns
`346`, matching the reviewer. The immutable superseding hypothesis was not edited.
The review budget is exhausted at 4/4, so Phase 2 remains closed and no ORF
implementation or confirmatory experiment is authorized.

## User authorization for held-out revision reviews

The user authorized the next held-out revision verbatim: “Authorize one additional
hypothesis-review round, raising the limit from 4 to 10, to write and review a
held-out ORF hypothesis. No Kaggle action is authorized.” The recorded review
ceiling is therefore 10; reviews remain sequential and consume one round per
dispatch. The Kaggle prohibition is explicit and binding.

## Held-out round 5 dispatch

The sterile theory re-review was dispatched against the committed 395-line
superseding entry `research-log/010-hypothesis-iter-4-v3-heldout.md`, which cites the
locked contract `experiments/configs/orf-heldout-v1.json` (SHA-256
`2a920b17630c00485ddb854825fff7ee2e714dd5bddb3bab50d74df26f2ccddd`). The prompt
contains the six round-4 blockers in the allowed previous-review slot. This consumes
review round 5/10; the held-out seed remains unopened.
