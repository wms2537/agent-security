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

## Held-out round 5 returned verdict

The reviewer returned the following report verbatim:

Status: DONE

Reviewed `research-log/010-hypothesis-iter-4-v3-heldout.md`: **395 lines**, verified with both `wc -l` and `git show HEAD:... | wc -l`. The locked JSON has 76 lines and SHA-256 `2a920b17630c00485ddb854825fff7ee2e714dd5bddb3bab50d74df26f2ccddd`. All four source hashes in the contract match the files on disk.

### 1. Blind Assessment

#### Justification Correctness

**NEEDS_REVISION.**

The claim is now appropriately narrow: it predicts performance on a specified synthetic split, not live-model or leaderboard behavior. The circular theorem-like condition has been removed, and the equations at lines 97–103 mostly define an algorithm rather than pretending to prove an effect.

I re-derived the load-bearing mechanics:

- With one unique finding containing exactly \(e\) severity-5 predicates, \(q=16e+2\) follows from the SDK scorer, provided the exclusivity and global-uniqueness assertions hold.
- In the homogeneous block, \(c(m)=bm\), \(q(m)=16m+2\), and therefore \(q/c=16/b+2/(bm)\), strictly decreasing in \(m\). Since \(R=8100<G=9000\), \(b\in[5,12]\), the candidate cap is unbound (`floor(8100/b)≤1620`), and raw is below 200,000. Static \(m=1\) therefore dominates not merely every other pure length but every mixture: for a fixed number of message units it maximizes the number of `+2` candidate bonuses. The negative consequence is valid.
- The timing correction `-sigma²/2` makes each lognormal factor mean one. Bursts deliberately raise the mean by \(p(B-1)\).
- The entropy expression is normalized to \([0,1]\), assuming \(p_m\) means the fraction of profiles whose tied-resolved per-profile no-probe optimum is \(m\).

Three central defects remain.

First, the primary comparison does not isolate the proposed mechanism. ORF differs from static in at least three ways: it measures all lengths, it retains and scores a fixed 21-candidate multi-length probe portfolio, and it selects the fill length per profile. Lines 294–297 incorrectly call this only “measurement and selection.” A win could arise partly from the fixed probe mixture or a nonadaptive mixed-length allocation. A same-probe/global-fill comparator is required before attributing the result to adaptive information value.

Second, the uncertainty analysis has no coherent estimand. The claim at lines 162–171 is about one fixed deterministic 256-profile split. Once opened, its mean difference is exact; a bootstrap is not sampling uncertainty for that finite-set claim. If the intended estimand is the generator population, fixing the static length selected on the original held-out sample inside every bootstrap conditions away its selection uncertainty. Each resample must reselect the best static length, or static selection must use an independent split.

Third, the policy specification is internally inconsistent. Lines 87–89 say `n_z(m)` accounts for the raw cap and lines 92 and 101 say filling stops when the first constraint binds, but `n_z(m)` at lines 98–100 contains no raw-cap stopping term. `min(H, ...)` caps reported score, not emitted candidates or timing workload. This matters especially for the descriptive timing stress.

The evidence chain is mostly auditable, but its exact source ranges are incomplete. `scoring.py:41-91` omits `SEVERITY_W` at line 14 and the 200,000 normalization/cap mechanics at lines 30–31 and 95–101. The severity-5 EXFIL construction depends on `core/predicates.py:263-281`, which is neither cited nor hashed.

#### Mathematical Depth & Validity Domains

**NEEDS_REVISION.**

The useful abstraction is the distribution over profile parameters \((a,b,d,k,\lambda)\). It is a mixed discrete-continuous measure whose support is specified, and each draw maps deterministically to a seven-action cost/response curve. This is structurally intelligible; the notation is not floating.

However:

- Equal weighting and the probabilities/ranges in lines 120–139 have no provenance or coverage argument beyond “span” assertions. Why 40% no cliff, these cliff weights, or these log-uniform boundaries? Because the claimed mean gain is distribution-dependent, weights are load-bearing, not incidental.
- Three probes per length are identical in the primary test. Thus there is no estimation problem and repetitions two and three provide no information; they are an arbitrary tax. Their validity domain is deterministic stationarity only.
- Entropy measures diversity of winning labels, not separation between actions. High entropy can coexist with negligible oracle-static margin. The gain criterion handles the outcome, but entropy does not independently validate the mechanism.
- The bootstrap lower bound is mathiness under the fixed-split wording: it creates the appearance of inferential uncertainty without defining a sampled population.
- The optional timing model lacks a complete executable meaning: exact latent-key serialization, Normal sampler, burst substream, candidate ordinal semantics, and generation-timeout behavior are unspecified. `ordinal-or-block` at lines 227–230 is not an exact key derivation.

#### Logical Soundness

**NEEDS_REVISION.**

The basic chain—heterogeneous optima can make adaptive selection repay a charged probe cost—is plausible, but the current experiment only establishes the end-to-end compound policy comparison.

Socratic challenges:

- Why assume a static *single length* is the correct nonadaptive null? A precommitted mixture or a policy retaining identical probes could predict a gain on heterogeneous profiles and a loss on the homogeneous block.
- Why call a public deterministic seed “unopened”? Anyone can compute its outcomes from lines 116–134. `opened:false` is metadata, not blinding, and “refuse a second invocation” can be bypassed with another output path or implementation.
- If the fixed split is the target, what random quantity is the bootstrap interval covering?
- If the generator population is the target, why is the empirical best-static action treated as fixed after being selected on the same sample?
- If a profile assertion fails, does “zero-valued profile row” zero only the affected policy or every policy? Zeroing both can conceal an ORF-specific failure.

The claim verbs remain predictive and do not exceed the project’s question type.

#### Assumption Completeness

Missing or insufficiently bounded assumptions include:

1. **Held-out integrity:** lines 110–158 rely on voluntary non-use of a public seed. Violation destroys the only claim to unseen evidence.
2. **Generator-design independence:** the weights, ranges, three-probe tax, 0.75 eligibility gate, and 10% threshold may have been informed by prior synthetic outcomes; this history is not disclosed.
3. **Treatment isolation:** retained probes and adaptive filling are assumed to be one indivisible mechanism.
4. **Estimand:** fixed-split performance and generator-population performance are conflated.
5. **Static/oracle definitions:** no exact formulas specify static capacity, per-profile oracle score, or whether oracle eligibility matches ORF.
6. **Regret:** “mean oracle regret” is undefined—mean of profile percentages and ratio of aggregate means are different statistics.
7. **Failure semantics:** shared generator failures versus policy-specific failures are not distinguished.
8. **Timing-stress execution:** generation overrun, partial generation, and RNG substreams are unspecified.

#### Taxonomy Verification

**PASS.**

`Evidence Gap × Optimization/Search / Empirical Mapping × replace` is defensible and matches the actual move: replace a fixed length with response-dependent selection and measure it. Resource Bottleneck could reasonably be dominant rather than secondary, but this is not Bridge × Synthesis and there is no tripwire-evasion concern.

#### Anti-Stacking Check

**FAIL.**

The claimed distinguishing prediction at lines 347–351 only rules out adding actions followed by another single fixed length. It does not rule out a plain nonadaptive combination of those actions.

A fixed mixed-length portfolio, or the same 21 retained probes followed by the globally chosen static fill, could also improve on the best pure static length in heterogeneous profiles and lose to \(m=1\) in the homogeneous block. Therefore the opposite-sign prediction is not yet specific to online adaptation.

#### Occam’s Razor Check

**FAIL.**

Simpler alternatives should be tested first:

- one probe per length, since repetitions are identical;
- the same probe portfolio with global-static fill;
- the best precommitted mixed-length allocation;
- direct per-profile oracle selection minus an explicitly computed observation tax.

Without these, the extra machinery is not demanded by the evidence.

#### Alternative Explanations

A confirmed headline result could arise from:

- scoring and retaining the fixed multi-length probe portfolio;
- an advantageous nonadaptive length mixture;
- arbitrary generator weights chosen to make different lengths frequent;
- candidate/raw-cap geometry rather than reset amortization or cliffs;
- the `+2` per-finding novelty bonus;
- undetected unique-hash or predicate-construction errors;
- choosing the static comparator and then conditioning on that choice in the bootstrap.

The homogeneous block catches gross accounting leakage, but not these alternatives.

#### Fixed Bias-Surface Audit

All eight required headings are present, but several are substantively incorrect or incomplete:

- **Selection, lines 290–293:** addresses post-generation row selection but not researcher selection of generator support, weights, gates, or a publicly computable seed.
- **Confounding, lines 294–297:** falsely treats a compound intervention as a single isolated method difference.
- **Assignment, lines 298–300:** adequate for the deterministic paired comparison.
- **Protocol deviation, lines 301–303:** unenforceable one-open rule; no frozen command for the mandatory homogeneous block or optional stress run.
- **Missing data, lines 304–306:** zeroing scope is ambiguous and could mask policy-specific failures.
- **Measurement, lines 307–309:** appropriate synthetic scope, but source coverage is incomplete.
- **Analysis flexibility, lines 310–312:** contradicted by undefined regret/oracle formulas and the bootstrap estimand ambiguity.
- **Selective reporting, lines 313–315:** intention is adequate, but no output schema or negative/stress command operationalizes it.

#### Previous-review issue disposition

| Prior issue | Status | Judgment |
|---|---|---|
| 1. Circular margin and deterministic table | **RESOLVED** | The tautology is deleted, the prediction is unconditional, and prior constructed tables are demoted to unit tests. |
| 2. Held-out family, weighting rationale, homogeneous control | **IMPROVED** | A randomized split and valid negative block are added, but the public seed is not truly blind and the generator weights/ranges lack rationale. |
| 3. Timing dependence, calibration, clamp, void bound | **IMPROVED** | Removing replay safety from confirmation is correct. The retained descriptive protocol still lacks exact substreams and generation-timeout semantics; it remains deliberately uncalibrated. |
| 4. Synthetic/model-specific wording | **RESOLVED** | Claim scope is consistently synthetic and explicitly excludes live targets. |
| 5. SDK and measured-artifact evidence | **IMPROVED** | Hashes and log references are present, but scorer line ranges omit weights/cap, predicates are uncited, and no raw measured trace artifact supports the profile distribution. |
| 6. Commands, versions, bootstrap, disjoint boundaries | **IMPROVED** | Python, held-out commands, bootstrap indices, and non-overlapping regions are frozen. Negative/stress commands and several exact statistics remain unspecified. |

#### Overall

**NEEDS_REVISION**

Required fixes, ordered by severity:

1. **Lines 37–44, 80–103, 173–184, 294–297, 347–351:** add a same-probes/global-static-fill control and a strongest feasible precommitted nonadaptive mixed-length control. Make the adaptive-selection contrast primary for the mechanism claim.
2. **Lines 110–158, 282–286; JSON lines 4 and 35–38:** replace the public “unopened” seed with a real commit–reveal or post-freeze randomness-beacon protocol and an atomic, path-independent opening ledger.
3. **Lines 146–150 and 186–193:** choose one estimand. For a fixed split, drop inferential CI language. For generator-population inference, independently select the static control or reselect it inside every bootstrap resample.
4. **Lines 87–103, 177–197, 319–333:** define raw-cap stopping, static scores, per-profile oracle, regret aggregation, eligibility, and policy-specific failure semantics exactly.
5. **Lines 116–139, 162–168, 290–293:** justify or externally derive the generator ranges and weights. If it is purely coverage-based, use explicit strata, state their weights, report stratum-wise results, and avoid “benchmark-shaped” implications unsupported by traces.
6. **Lines 207–240 and 259–286; JSON lines 60–68:** specify exact RNG keys/samplers, candidate indexing, generation timeout behavior, negative/stress commands, output schema, and all decision thresholds in the machine-readable contract.
7. **Lines 62–76 and 244–257:** cite/hash scorer weights and cap lines plus the EXFIL predicate source. Label 8100 solely as a synthetic design constraint, not measured safety evidence.

### 2. Actionable Coaching

- Use three primary policies: zero-probe best pure static; identical 21-probe portfolio plus global-static fill; identical probes plus per-profile adaptive fill. The last contrast identifies adaptation while the first preserves the end-to-end system comparison.
- Add one-probe ORF as an Occam ablation. In a deterministic profile it should dominate three-probe ORF unless the repetition tax is itself part of the intended constraint.
- Formalize:
  - `S_static,z(m)`;
  - `S_oracle,z=max_m S_static,z(m)`;
  - aggregate gain;
  - one unambiguous regret statistic;
  - actual emitted count when score saturation occurs.
- Commit a seed hash, freeze code and predictions, then reveal a seed derived from a later public beacon or independent custodian. Log opening in an immutable manifest not controlled by `--out`.
- If the scientific target is the generator distribution, use a separate selector-training split for the static comparator and evaluate both policies on untouched evaluation profiles. This avoids nonregular “max over seven means” bootstrap complications.
- Convert arbitrary coverage probabilities into a factorial or stratified design: no-cliff/cliff location × low/high overhead × low/high curvature. Report each cell and sensitivity under several preregistered weightings.
- Hash the full prose specification if JSON remains incomplete, or move generator draw order, error rules, RNG keys, commands, output schema, and disconfirm thresholds into a schema-validated contract.

## Round 5 gate decision

The adverse `NEEDS_REVISION` verdict stands. The reported hypothesis line count and
contract hash are verified. The v3 hypothesis and `orf-heldout-v1` contract remain
immutable; the held-out seed was never instantiated. Phase 2 stays closed while a
new superseding, commit-reveal design is prepared under the remaining authorized
review budget.

## Beacon-held-out round 6 dispatch

The superseding entry
`research-log/011-hypothesis-iter-4-v4-beacon-heldout.md` and machine contract
`experiments/configs/orf-heldout-v2.json` were committed at `7bd49e5` before
dispatch. Deterministic verification found 573 hypothesis lines, 180 contract
lines, contract SHA-256
`5bcdc78af0e406ddf52f6f3cc70ef2bfb497fa3d811b8b5df5f795e6019401ac`, 40
equal-weight strata, 320 specified but uninstantiated primary profiles, 3,003
enumerated mixture controls, a unique `m=1` homogeneous optimum at both support
endpoints, valid JSON, and matching source hashes.

The sterile theory-review prompt contains the artifact path, empirical/systems
claim type, predictive question type, and the seven round-5 blockers in the
template's previous-review slot. No project learnings or assurances are included.
Dispatch consumes round 6/10. No NIST target pulse has been selected, no opening
ledger or profile exists, and no implementation, experiment, external submission,
or Kaggle action has occurred.

## Beacon-held-out round 6 returned verdict

The reviewer returned the following report verbatim:

**Status: DONE**

Reviewed [research-log/011-hypothesis-iter-4-v4-beacon-heldout.md](/home/soh/agent-security/research-log/011-hypothesis-iter-4-v4-beacon-heldout.md:1), verified at **573 lines**. Also reviewed the complete 180-line machine-readable contract and checked every cited repository SHA-256; all five hashes match the current files.

## 1. Blind assessment

### Overall: NEEDS_REVISION

The primary contrast is now structurally meaningful and most previous confounds are removed. However, the executable beacon protocol is currently unsatisfiable as written, the negative control is ambiguously defined across prose and contract, and no evidence or derivation supports the load-bearing 5% effect prediction.

### Previous-review disposition

1. **Same-probes/global-static and nonadaptive mixture controls: RESOLVED.**
   Lines 38–45, 65–80, and 240–261 make `ADAPTIVE` versus identical-probe `PROBE_GLOBAL` primary and add a fully enumerated denominator-eight mixture class.

2. **Real commit–reveal/beacon and atomic ledger: IMPROVED.**
   The public seed is gone and a future pulse plus fixed ledgers is a genuine advance. It is not resolved because the timestamp rule cannot accept the NIST response as specified, `FREEZE.json` lacks a complete machine-readable exclusive-creation schema, and reveal/evaluate do not explicitly require a clean worktree at the frozen implementation commit.

3. **Single estimand/no incoherent CI: RESOLVED.**
   Lines 63, 81–82, and 376–380 consistently define one realized finite split and no inferential interval.

4. **Stopping, static scores, oracle, regret, eligibility, failures: IMPROVED.**
   The principal formulas and failure semantics are now precise. The unresolved negative-split meaning of `PROBE_GLOBAL` prevents a fully resolved rating.

5. **Generator ranges and weights: RESOLVED.**
   Lines 263–302 use 40 explicit equal-weight coverage strata, require stratum-wise results, and restrict conclusions to designed support rather than target prevalence.

6. **RNG, indexing, commands, schema, thresholds: IMPROVED.**
   RNG keys, samplers, commands, row counts, and thresholds are much better. Exact profile/candidate indexing, finding/hash construction, prediction-ledger schema, output types/order, numeric serialization, and error-code vocabulary remain absent.

7. **Scorer/predicate/caps hashes and 8100 scope: RESOLVED.**
   Lines 89–145 and 446–466 correctly derive the SDK objective, cite the relevant sources, and label 8100 solely as a synthetic design constraint. All recorded source hashes match.

### Justification correctness

The load-bearing score derivation is correct under the stated synthetic construction:

\[
\text{normalized}(Q)=\min(1000,Q/200),
\]

so maximizing normalized score is equivalent to maximizing \(S=\min(200000,Q)\). A successful unique-hash candidate with \(e_z(m)\) severity-5 predicates contributes \(q_z(m)=16e_z(m)+2\). The ceiling in the saturation term is correct because the candidate that first reaches or crosses \(H\) is retained.

The resource count

\[
n_z(m)=\max(0,\min\{C-p_z,\lfloor(G-g_z)/c_z(m)\rfloor,
\lfloor(R-r_z)/c_z(m)\rfloor,\lceil(H-Q_z)/q_z(m)\rceil\})
\]

is also correct only in the deterministic, additive, stationary regime where one probe reveals the exact cost and future yield of every fill candidate.

The primary comparison reduces to

\[
A=\sum_z\max_m S_z(m),\qquad G=\max_m\sum_zS_z(m).
\]

Therefore \(A\ge G\) is an identity, not an empirical discovery. Equality holds exactly when a common fill length can attain every profile’s maximum; a 5% result means

\[
A-G\ge 0.05G,
\]

so the global choice accumulates at least that much aggregate regret. This does isolate response-dependent selection from the shared probe portfolio, but the only falsifiable scientific content is the magnitude threshold. No cited trace, replication, pilot, support-volume argument, or analytical bound justifies **5%**. Lines 290–296 explicitly concede that the ranges are stress-support choices, and the evidence chain supports score mechanics rather than effect magnitude.

The homogeneous proof is valid if `PROBE_GLOBAL` is reselected within the negative split. After seven probes, the remaining replay budget in message-cost units is

\[
T=8100/b-87\in[588,1533].
\]

Thus the candidate cap \(1993\), generation budget, and saturation do not bind. Pure \(m=1\) gives \(18\lfloor T\rfloor\), while for \(m>1\),

\[
\lfloor T/m\rfloor(16m+2)
<18\lfloor T\rfloor.
\]

Hence \(m=1\) strictly wins. But the contract defines `PROBE_GLOBAL` only as maximizing over the **primary split** (JSON line 115). Reusing that primary-selected length on the negative split does not imply equality. The prose and `negative_equality` metric instead assume a separately reselected negative optimum. This must be resolved explicitly.

### Fatal beacon-contract defect

The NIST API returns `pulse.timeStamp` as an ISO-8601 string such as `"2026-07-19T05:53:00.000Z"`, while JSON lines 38–39 require adding `600000` to the anchor timestamp and later require `pulse.timeStamp == target_unix_ms`. Strict string-versus-integer equality can never pass. NIST documents the request parameter as Unix milliseconds but returns the pulse timestamp in its schema representation; `/pulse/time/...` may also return the nearest pulse, making the explicit parsed-timestamp equality check essential. See the [official NIST description](https://csrc.nist.gov/Projects/interoperable-randomness-beacons/beacon-20) and [live API shape](https://beacon.nist.gov/beacon/2.0/pulse/last).

The protocol also freezes a clean `HEAD` only at `freeze`. It does not explicitly require and enforce a clean worktree and the same frozen `HEAD` at `reveal` and `evaluate`. A modified uncommitted evaluator could therefore consume the pulse under the written checks. JSON line 139 vaguely declares implementation violations invalid, but no reveal/evaluate rule defines the required check.

### Mathematical depth and validity domains

The equations generally carry the argument rather than decorate it. Symbols are mostly concretely bound, and entropy is correctly demoted to a descriptive metric.

The missing validity domains are load-bearing:

- Probe measurements and all future fills must be exactly stationary.
- Costs and scores must be deterministic and additive across candidates.
- A single probe must reveal the exact future \(c_z(m)\) and \(e_z(m)\).
- Candidate order must have no interaction with score, latency, guardrails, or profile state.
- Every retained finding must have one unique score-cell hash and exactly the claimed predicates.
- No hidden shared overhead, concurrency, cache, or deadline dependence may exist.
- NIST outputs must be forward-unpredictable under the trusted-provider assumption.
- Frozen code, contract, predictions, and output schemas must be the code actually executed.

Violating the first four invalidates the interpretation as an online selection mechanism; violating finding/hash assumptions invalidates \(q_z(m)\); violating beacon/code-freeze assumptions invalidates held-out status.

### Logical soundness

The conditional mechanism is sound: material positive regret against an oracle-best global action implies profile-dependent action value within the synthetic model.

The unsupported leap is from “the crossed support can create heterogeneous optima” to “the aggregate gap will be at least 5%.” Heterogeneity alone does not imply material separation; profiles can have different tie-resolved optima with nearly identical scores.

The description also calls the profiles “unseen” while the full generator, support, and deterministic outcome equations are known. Only realized parameter draws are unseen. That distinction matters because the hypothesis can be analytically tailored to the generator even without opening the beacon.

### Threats-to-validity audit

Lines 470–497 do contain all eight required categories, one numbered item each: selection, confounding, allocation/assignment, protocol deviation, missing data, measurement, analysis flexibility, and selective reporting.

Two entries are incomplete:

- **Protocol deviation:** no explicit clean-HEAD/worktree verification at reveal and evaluation.
- **Selective reporting:** mandatory output fields do not prevent fetching the public target pulse independently, previewing the deterministic split, and declining to evaluate or publish. A locally committed freeze is not a third-party timestamped preregistration.

### Taxonomy verification

The narrow taxonomy is defensible:

- Opportunity: Evidence Gap, with Resource Bottleneck secondary.
- Paradigm: Optimization/Search plus Empirical Mapping.
- Dominant operation: replace a global argmax with profile-conditioned argmax.

This is a genuine local decision-scope change, not Bridge Opportunity × Synthesis/Unification. The grand “frontier” naming exceeds the actual contribution, but that is not itself a correctness defect.

### Anti-stacking check

Passes narrowly. A plain combination of the same probes and fill components does not predict a difference against `PROBE_GLOBAL`, because that control has the identical retained probes and resources. The distinguishing prediction is specifically conditional selection on heterogeneous profiles plus equality on the homogeneous split.

The result would still be a deterministic oracle-information advantage, not evidence that a noisy deployable selector works.

### Occam’s Razor check

The protocol is disproportionately elaborate for a claim about one arbitrary finite synthetic draw. A simpler first-principles formulation is the aggregate conditional-regret identity

\[
\Delta(D)=\sum_z\max_mS_z(m)-\max_m\sum_zS_z(m),
\]

followed by an exhaustive deterministic map of where \(\Delta(D)\) is materially positive over the declared support. The beacon is useful only as an anti-tuning check; it does not add population validity.

The 3,003-policy control is useful for limiting an end-to-end claim, but its denominator-eight boundary has no scientific justification beyond feasibility. It should not be described as globally strongest.

### Alternative explanations

A confirmed result could arise because:

- Equal weighting deliberately assigns substantial mass to abrupt compliance cliffs.
- The selector receives noiseless exhaustive oracle information and evaluates fills on the same stationary profile.
- Integer floors, caps, and saturation amplify small action differences.
- The result is the generic optimization gap from allowing 320 decisions instead of one.
- The chosen global comparator class is constrained, while adaptive uses per-profile choices.
- Synthetic predicate/hash construction guarantees linear score additivity absent in live traces.

These explanations do not invalidate the narrow arithmetic claim, but they block broader mechanism language unless explicitly treated as the validity domain.

### Required fixes, severity order

1. **Repair the beacon timestamp and freeze enforcement** at hypothesis lines 304–353 and JSON lines 27–60. Define exact ISO-8601 parsing to UTC milliseconds, validate millisecond alignment, specify exact `FREEZE.json` fields and exclusive atomic creation, and require clean worktree plus frozen `HEAD` at freeze, reveal, and evaluate.

2. **Define the negative global policy unambiguously** at lines 355–374 and JSON lines 97–116, 132, and 166–167. Either define `PROBE_GLOBAL_NEG` as a negative-split-specific global argmax, or reuse the primary global length and drop the exact-equality theorem.

3. **Justify or relabel the 5% prediction** at lines 55–61, 81–87, 290–296, and 537–549. Provide an analytical support-volume/regret argument or independently sourced frozen evidence. Otherwise label 5% as a normative materiality threshold rather than mechanism-derived expectation.

4. **Complete the executable schema** at lines 89–127 and 412–444 and JSON lines 15–25 and 160–171: exact profile-index mapping, candidate ordinals, trace/finding construction, literal sentinel, unique-hash rule, row ordering/types, numeric serialization, error-code enum, and exact summary metric keys.

5. **Define the prediction ledger and selective-opening safeguards** at JSON lines 33–36. Name its path, schema, hash, freeze binding, and publication/timestamp mechanism. Require preservation/reporting of every freeze even if evaluation is never completed.

## 2. Actionable coaching

- Express the mechanism through the regret decomposition
  \[
  A-G=\sum_z[\max_mS_z(m)-S_z(m_G)].
  \]
  Predeclare the fraction of profiles/strata with positive regret and the distribution of action-separation margins. This directly measures the proposed structure; entropy does not.

- For NIST, parse `timeStamp` canonically, derive `target_unix_ms`, and then reject the “next closest” API behavior unless the parsed returned timestamp exactly equals the target. Preserve and hash the raw response before parsing.

- Add a split-specific policy namespace: `PROBE_GLOBAL_PRIMARY` and `PROBE_GLOBAL_NEGATIVE`. This removes an otherwise experiment-invalidating ambiguity.

- Bind all later commands to `FREEZE.json`: current `HEAD`, clean worktree, contract hash, evaluator/test hashes, prediction-ledger hash, and source hashes must match before reveal or evaluation reads the pulse.

- Make the synthetic finding generator auditable by emitting or hashing candidate-level records. Aggregate TSV rows cannot independently verify predicate exclusivity and global hash uniqueness.

- Treat the present experiment as a best-case deterministic oracle-information test. A subsequent hypothesis should use independent/noisy continuation outcomes after probes; otherwise the same-profile argmax does not test estimation robustness.

- Consider an exhaustive deterministic support map before the beacon run. It would reveal whether 5% is structurally robust or merely dependent on a small set of cliff-heavy cells without consuming the held-out pulse.

## Round 6 gate decision

The adverse `NEEDS_REVISION` verdict stands. The reviewer-reported 573 hypothesis
lines, 180 contract lines, contract SHA-256, and all five source hashes were
independently verified against commit `7bd49e5`. The v4 hypothesis and v2 contract
remain immutable, the future beacon target does not exist, and Phase 2 remains
closed.

## Beacon-held-out round 7 dispatch

The superseding entry
`research-log/012-hypothesis-iter-4-v5-beacon-heldout.md` and machine contract
`experiments/configs/orf-heldout-v3.json` were committed at `f4098e9` before
dispatch. Deterministic verification found 511 hypothesis lines, 265 contract
lines, contract SHA-256
`15cca91e5865b652453104c873b0e2acb3a95dd65eeb27e070c3177cc59596e5`, a valid
live NIST ISO-to-integer parse without target derivation, contiguous profile indices
0–319, 3,003 enumerated mixture controls, strict negative `m=1` at both support
endpoints, zero seed fields, valid JSON, and matching source hashes.

The sterile re-review contains the five round-6 blockers in the template's allowed
previous-review slot and no project learnings or assurances. Dispatch consumes
round 7/10. No freeze, pulse target, opening ledger, profile, implementation,
experiment, external submission, or Kaggle action exists.

## Beacon-held-out round 7 returned verdict

The reviewer returned the following report verbatim:

**Status: DONE**

The hypothesis entry contains **511 lines**; `git show HEAD:research-log/012-hypothesis-iter-4-v5-beacon-heldout.md | wc -l` also returns 511. The referenced contract contains 265 lines, parses as JSON, and its five declared source hashes match the current files.

## Blind assessment

### Previous-review disposition

1. **Beacon timestamp and freeze enforcement — RESOLVED.** The contract now specifies exact `%fZ` parsing, integer UTC-millisecond conversion without floating timestamps, millisecond and minute alignment, ordered `FREEZE.json` fields, exclusive creation, clean `HEAD=I` at freeze, and clean `HEAD=A` plus the exact `I→F→A` chain before combined reveal/evaluation. The live [NIST pulse](https://beacon.nist.gov/beacon/2.0/pulse/last) uses the expected `...00.000Z` representation, and [NIST’s API documentation](https://csrc.nist.gov/Projects/interoperable-randomness-beacons/beacon-20) confirms millisecond POSIX requests and “specific time or next closest” behavior. A new reveal-ledger contradiction remains below.

2. **Negative global policy — RESOLVED.** `PROBE_GLOBAL_NEGATIVE` is independently selected on the negative split; no primary length is reused.

3. **5% prediction — RESOLVED as requested.** It is explicitly a low-confidence normative materiality threshold, not a mechanism-derived expectation. No empirical or analytical support for expecting 5% is claimed.

4. **Executable schema — IMPROVED, not resolved.** Many previously absent details were added, but the contract is still not a single-valued executable specification.

5. **Prediction ledger/selective opening — RESOLVED for preregistration custody.** Path, header, exact unresolved rows, whole-file hash, freeze binding, public message, ACK, terminal abandonment, and preservation obligations are present. Post-evaluation row resolution remains unspecified as a new issue.

### Justification correctness

The load-bearing algebra is sound under the stated real-arithmetic model:

- A retained candidate with \(e\) severity-5 predicates contributes \(16e\), and a unique non-null cell hash adds 2, hence \(q_z(m)=16e_z(m)+2\). The source-hashed scorer implements exactly this reduction.
- For any fixed split and common score table,
  \[
  A-G=\sum_z\left[\max_m S_z(m)-S_z(m_G)\right]\ge 0.
  \]
  This is an identity, not evidence that the realized advantage is material.
- For the negative split, the seven probes consume \(87b_z\) replay units and contribute common raw score \(16(87)+2(7)=1406\). With \(T=8100/b_z-87\in[588,1533]\), replay binds before generation, candidate count, or saturation. For \(m>1\),
  \[
  \lfloor T/m\rfloor(16m+2)\le17T<18(T-1)\le18\lfloor T\rfloor ,
  \]
  so \(m=1\) uniquely maximizes the fill under exact arithmetic. The zero aggregate difference follows because both selectors use the same \(m=1\).
- \(\binom{14}{6}=3003\) denominator-eight mixtures is correct.

These equations carry the argument; they are not merely decorative. The unsupported element is the 5% magnitude, which is now honestly normative.

There is, however, no implementation-aware floating-point error bound connecting the negative proof to the specified Python `float` computations. The margins are large enough that the conclusion is almost certainly robust, but an exact-integer prediction should not rest on “almost certainly.” Either derive an IEEE-754 error envelope or compute the resource capacities in an exact representation.

### Mathematical depth and validity domains

The central abstraction is conditional regret: the value of expanding the action class from one split-wide action to one action per profile. Its validity is limited to deterministic, stationary, fully observed profile tables with additive per-profile budgets and independent per-profile scoring. It does not support noisy inference, online learning, deployment, a target-population expectation, or generalization beyond the selected equal-stratum support.

Notation is not fully disciplined. `G(D)` denotes the global policy aggregate at lines 56 and 70, while `G=9000` denotes generation budget at line 125; later `A/G` again means the aggregate comparator. Rename one. A proof should not require readers to infer which incompatible meaning of \(G\) applies.

### Logical soundness

The most serious defect is the outcome logic.

The claim is “gain ≥5%,” and the finite outcome is measured exactly. Therefore every valid result below 5% falsifies that magnitude prediction. Lines 274–283 and contract lines 204–211 instead call \(0<\text{gain}<5\%\) **INCONCLUSIVE** and reserve **DISCONFIRMED** for exactly zero. What uncertainty remains after an exact finite evaluation that could make 3% consistent with “at least 5%”? None. This outcome partition weakens falsifiability and creates selective interpretive protection.

A second contradiction makes the reveal state machine non-executable as written. Hypothesis lines 338–345 and contract line 98 require `OPENED.json` and `EVALUATION_STARTED.json` to be created before deriving the master digest, while the `OPENED.json` schema at contract lines 99–114 requires `master_digest_hex`. Both requirements cannot be satisfied. Moreover, two independent filesystem files cannot be created as one atomic transaction; the terminal semantics for a crash between them must be defined.

A third defect is schema underdetermination:

- Candidate IDs require “zero-padded” profile and candidate ordinals but specify no widths.
- Exact `policy_id`, `policy_parameter`, phase, row-status, and decision vocabularies are absent.
- `fill_length` is declared integer even for policies for which it is inapplicable; no sentinel is specified.
- Primary null-cliff serialization is unspecified.
- Negative fields are simultaneously declared integers and literal `NA`.
- Mixture tie-breaking does not say lexicographically smallest or largest.
- “At least 17 significant digits” permits multiple ratio strings and is not canonical.
- `primary_gain_numerator` and denominator are not algebraically defined.
- Nested summary objects (`row_counts`, stratum metrics, histogram, secondary metrics, binding and failure counts) have keys but no internal schemas.
- `freeze-anchor.json` and `revealed-pulse.json` are called typed/preserved artifacts without exact content schemas.

Finally, the frozen prediction rows have no deterministic post-run resolution rule. The contract does not define how exact outcomes populate `metric_value`, `signal`, and `status`, or how those changes are committed while preserving the frozen pre-run hash.

Claim verbs are otherwise appropriately predictive—principally “will achieve” and “will have.” “Conditioning effect” should remain restricted to the deterministic paired policy contrast and not be allowed to imply a population or live-system causal effect.

### Assumption completeness

Load-bearing assumptions include:

- One probe reveals future cost and yield exactly and permanently.
- Cost/yield are deterministic, stationary, additive, and order-independent.
- Profiles have independent budgets and per-profile score caps.
- All action candidates are evaluated under identical scorer semantics.
- The same score table is reused by both selectors.
- No concurrency, caching, shared overhead, deadline jitter, or cross-profile state exists.
- Profile support and equal weighting are the estimand, not a prevalence model.
- The beacon is forward-unpredictable; HTTPS, thread timestamps, local git history, and the user ACK are honest.
- CPython, `random.Random`, `math.log/exp`, and float-floor behavior reproduce the specified selector.
- The global-score denominator is positive; here the always-positive \(m=1\) probe guarantees it.
- No earlier iteration tuned support or threshold to a realized target pulse.

Violations of the first six invalidate the claimed replay-selection interpretation. Violations of custody assumptions invalidate held-out status. Runtime/numeric violations invalidate the exact negative check.

### Threat audit

- **Selection:** The beacon prevents tuning to one realized draw, but not analytical or prior-iteration tuning of the deliberately stress-weighted support. Scope restriction addresses generalization, not design-selection bias.
- **Confounding:** The primary same-probe contrast isolates decision scope well. Per-profile caps, integer floors, cliff prevalence, and scorer novelty bonuses remain alternative drivers of magnitude.
- **Assignment:** Fully paired policy evaluation and policy-free keyed substreams are appropriate; randomized assignment is unnecessary for this deterministic finite estimand.
- **Protocol deviation:** The intended `I→F→A` custody is strong, but the contradictory opening state machine and underspecified raw-pulse artifacts prevent mechanical enforcement.
- **Missing data:** Any missing/duplicate row or exception invalidates confirmation, which is appropriate. Partial-output schemas still need exact definition.
- **Measurement:** Source hashes and candidate-level scorer assertions are strong. The measured construct remains an oracle synthetic objective, not live replay value.
- **Analysis flexibility:** Contrast, support, weighting, and threshold are fixed. The “inconclusive” subthreshold category reintroduces interpretive flexibility.
- **Selective reporting:** Single-freeze publication and terminal abandonment are substantial safeguards. The unresolved post-run prediction-ledger transition is a remaining gap.

### Taxonomy verification

The defensible classification is:

- **Opportunity:** Evidence Gap, with Resource Bottleneck secondary.
- **Method:** **Empirical Mapping dominant**, Optimization/Search secondary. The current “Optimization/Search plus Empirical Mapping” does not identify the required dominant paradigm.
- **Operation:** Replace a split-wide argmax with a profile-conditioned argmax.

This is not Bridge × Synthesis, so the tripwire is not triggered.

### Anti-stacking check

Pass. The distinguishing prediction is genuine: identical probes and resource state can yield a material adaptive/global contrast under heterogeneous profiles but exact equality under homogeneous profiles. A fixed probe portfolio or generic mixture does not itself predict this paired decision-scope contrast.

### Occam’s razor

The simpler sufficient hypothesis is:

> On this frozen finite support, profile-specific optimal actions incur at least 5% less aggregate conditional regret than the best single action; on the homogeneous control, regret is zero.

The SDK, beacon, and custody machinery are measurement and anti-tuning infrastructure, not part of the scientific mechanism. The named “replay value” should not obscure that the tested mechanism is an oracle conditional-regret table.

### Alternative explanations for confirmation

A ≥5% result could arise from:

- Deliberately equal-weighting cliff-heavy or otherwise unrealistic strata.
- Per-profile saturation caps and integer resource floors.
- Exact stationarity and noiseless one-probe revelation.
- The generic weak dominance of a larger, oracle action class.
- The scorer’s per-candidate uniqueness bonus.
- Prior analytical selection of factor ranges across hypothesis iterations.
- Restricting the nonadaptive mixture comparator to denominator eight.

All are compatible with confirmation and prevent broader deployment or population claims.

### Overall: **NEEDS_REVISION**

Required fixes, in severity order:

1. **Correct the decision partition** at hypothesis lines 274–283 and contract lines 204–211. Every exact gain below 5% must disconfirm the ≥5% materiality prediction. Report zero versus positive-subthreshold as descriptive subtypes, not different falsification status.
2. **Repair the opening state machine** at hypothesis lines 328–347 and contract lines 96–122. Define an executable sequence in which target bytes are preserved, the master is derived, `OPENED.json` is exclusively created with that digest, `EVALUATION_STARTED.json` is then exclusively created, and no profile generation begins until both exist. Define terminal behavior between each transition.
3. **Finish the schemas** at contract lines 23–35 and 219–256: exact padding widths, identifiers/enums, conditional sentinels, nested summary schemas, canonical decimal formatting, numerator/denominator formulas, tie direction, and exact raw anchor/pulse artifacts.
4. **Define prediction-ledger resolution** at contract lines 132–140: exact outcome-to-row mapping, signal/status values, numeric formatting, update timing, and commit/progress obligations.
5. **Remove notation collision and bridge real arithmetic to execution** at hypothesis lines 47–56, 122–139, and 250–266. Rename the generation budget or comparator aggregate and add a float-error bound or exact capacity arithmetic.
6. **Make the taxonomy dominant/secondary ordering explicit** at hypothesis lines 468–474.

## Actionable coaching

Use two outcome fields rather than one overloaded label:

- `materiality_prediction = CONFIRMED | DISCONFIRMED`
- `contrast_subtype = ZERO | POSITIVE_SUBTHRESHOLD | MATERIAL`

That preserves useful scientific distinctions without insulating the 5% prediction from falsification.

Represent the custody protocol as an explicit monotone state machine:

`IMPLEMENTED → FROZEN → ACKNOWLEDGED → OPENED → EVALUATION_STARTED → COMPLETED`

Every transition should name its exclusive artifact, required predecessor hashes, allowed git diff, and terminal crash state.

Replace prose-only “schema” strings with actual JSON Schema definitions or an equally deterministic validator specification. Add golden fixtures for one primary profile, one negative profile, one zero-event candidate, one mixture, one invalid artifact, and the complete summary key tree.

For the negative proof, either use exact rational/dimensionless capacity calculations or add a conservative floating-error proof showing that the smallest \(m=1\) advantage remains far above the maximum rounding perturbation.

Finally, describe the scientific contribution as a preregistered finite conditional-regret stress test. Any stronger “replay value” language should be reserved for a later noisy, live, externally weighted experiment.

## Round 7 gate decision

The adverse `NEEDS_REVISION` verdict stands. The reported 511 hypothesis lines,
265 contract lines, contract SHA-256, JSON validity, and all five source hashes
were independently verified against commit `f4098e9`. The v5 hypothesis and v3
contract remain immutable. Phase 2 stays closed and no freeze, target, profile,
experiment, or Kaggle action exists.

## Conditional-regret round 8 dispatch

The superseding entry
`research-log/013-hypothesis-iter-4-v6-conditional-regret.md`, contract
`experiments/configs/orf-heldout-v4.json`, and artifact schema
`experiments/configs/orf-heldout-v4-artifacts.schema.json` were committed at
`3033b15` before dispatch. They have 498, 204, and 231 lines respectively. Contract
SHA-256 is
`1ed7ad83db5ea6a0cff25192534f162f102d3635048d97cdebb90551ee84da30`; schema
SHA-256 is
`bd8ddcabef0c9b08ba6b4efeabe6cb2cf4894b16517b1b38de2585b760058a32`.

Pre-review verification passed Draft 2020-12 validation of six complete sample
artifact trees and the live NIST envelope, exact-Fraction negative endpoint proof,
exhaustive binary materiality partition, 3,003 mixture count, JSON/source/schema
hash checks, and zero seed fields. The sterile re-review contains only the six
round-7 blockers in the allowed slot. Dispatch consumes round 8/10. No evaluator,
freeze, pulse target, opening, profile, experiment, submission, or Kaggle action
exists.

## Conditional-regret round 8 returned verdict

The reviewer returned the following report verbatim:

- **Status:** DONE

The hypothesis entry has **498 lines**, matching `git show HEAD:research-log/013-hypothesis-iter-4-v6-conditional-regret.md | wc -l`. I reviewed all 498 lines, the complete 204-line contract, and the complete 231-line artifact schema. Both JSON files parse; the artifact schema passes the Draft 2020-12 metaschema check; its recorded SHA-256 and all five source hashes match the current files.

## Blind assessment

### Previous-review disposition

1. **Decision partition — RESOLVED.** Hypothesis lines 80–93 and contract lines 86–97 make every valid sub-5% result `DISCONFIRMED`; zero and positive-subthreshold are descriptive subtypes only.

2. **Opening state machine — IMPROVED, not resolved.** Target bytes now precede master derivation; `OPENED.json` precedes `EVALUATION_STARTED.json`; profile generation is gated on both. However, the target-fetch transition remains non-executable under crash recovery: after the HTTP response is received but before `revealed-pulse.raw.json` is durably created, the next invocation cannot distinguish “never fetched” from “fetched then crashed.” Retrying violates the claimed one-fetch rule; abandoning cannot distinguish a legitimate first invocation. See hypothesis 370–380 and contract 162–166.

3. **Schemas — IMPROVED, not resolved.** Widths, major enums, canonical decimals, JSON object trees, and raw pulse preservation were added. The specification is still not single-valued; details follow below.

4. **Prediction-ledger resolution — IMPROVED, not resolved.** Valid-result mappings and commit obligations are now concrete. Invalid-result resolution contradicts the terminal-output model: resolution requires summary validation, while shared failures preserve partial data and may produce no schema-valid summary.

5. **Notation and capacity arithmetic — RESOLVED.** `B_gen`, `S_global(D)`, `A(D)`, and `Delta(D)` are distinct, and all capacity floors operate on exact `Fraction` values. A new cross-platform `math.log/exp` reproducibility issue remains, but the previous capacity-floor defect is fixed.

6. **Taxonomy ordering — RESOLVED.** Empirical Mapping is explicitly dominant and Optimization/Search secondary.

### Justification correctness

The core score and regret algebra is correct:

\[
q_z(m)=16e_z(m)+2
\]

follows from the source-hashed scorer for positive-yield findings with unique non-null score-cell hashes, and

\[
A(D)-S_{\mathrm{global}}(D)
=\sum_z\left[\max_m S_z(m)-S_z(m_{\mathrm{global}})\right]\ge0
\]

is an exact identity on the common score table. The denominator is positive because the \(m=1\) probe always succeeds.

The negative-control proof is substantively correct under the operational arithmetic. With \(T=8100/b_F-87\in[588,1533]\), \(m=1\) strictly dominates every \(m>1\). The asserted nonbinding conditions also hold, although they should be written into the proof: replay capacity is at most 1533 versus candidate capacity 1993; generation capacity exceeds replay capacity; and maximum additional raw score is below \(18\cdot1533=27{,}594\), far below the remaining saturation margin \(198{,}594\).

The primary 5% prediction has no substantive justification. The document establishes only nonnegativity. Crossed heterogeneous support does not mathematically imply a 5% ratio: saturation, floors, or near-common optima can make regret arbitrarily small. Calling 5% “normative” explains the decision threshold, not why the predictive claim is plausible. This is acceptable as a low-confidence conjecture only if clearly treated as such; it is not a mechanism-derived prediction.

### Mathematical depth and validity domains

The conditional-regret abstraction is well bound to a concrete finite score table. Its domain is correctly restricted to deterministic, stationary, fully observed profiles with additive independent resources and oracle per-profile action selection. It says nothing about learning, noisy selection, population prevalence, or deployment.

The remaining numeric validity defect is that “CPython 3.14.3” does not uniquely specify `math.log/exp` results across platforms and libm implementations. `Fraction.from_float` makes capacity arithmetic exact only after those floats exist; it does not make parameter or cliff-event generation reproducible. Because `floor(m*exp(...))` is discontinuous at integers, an unbounded libm discrepancy can change event counts. Hypothesis 150–164 and contract 21–27, 136–144 need a pinned runtime/container and libm, a correctly-rounded reference implementation, or a certified distance-from-integer check.

### Logical soundness

The scientific outcome partition is now sound. The terminal protocol is not.

The largest contradiction spans hypothesis 331–345 and 356–383, contract 146–178, and schema 102–210:

- Ledger mutation is forbidden before summary validation.
- Shared crashes preserve partial outputs and produce `ABANDONED.json`.
- The summary schema nevertheless requires complete fixed row counts, all 40 strata, all metrics and hashes, `source_hash_check=true`, and `negative_difference_integer=0`.
- Thus many protocol-invalid outcomes cannot produce the prerequisite validated summary and consequently cannot receive the promised `status=crash` ledger resolution.
- An abandonment during `IMPLEMENTED→FROZEN` is also unrepresentable: `ABANDONED.json` excludes `IMPLEMENTED` as `last_completed_state` and requires a freeze hash that does not yet exist.
- No artifact or unambiguous rule marks the `COMPLETED` transition after summary, ledger, log, progress, and commit.

These gaps weaken missing-data and selective-reporting guarantees.

### Assumption completeness

Most load-bearing scientific assumptions are explicitly listed. Missing or insufficiently enforced assumptions include:

- Bitwise stability of `math.log/exp`, not merely CPython identity.
- Exact semantics for crashes before a pulse-preservation artifact exists.
- Honest completion and publication of terminal outcomes; local git commits alone are mutable and omittable.
- A deterministic definition of all secondary summaries and resource-binding ties.
- A guarantee that protocol-invalid outcomes can always be serialized and resolve both prediction rows.

### Fixed eight-part bias surface

- **Selection:** The target realization is held out, but the public generator, equal weighting, ranges, cliff prevalence, and 5% threshold remain analytically selectable. The stated finite-support scope is appropriate; the beacon does not neutralize design-selection bias.
- **Confounding:** Pairing isolates the intended relaxation from one global action to per-profile oracle actions. Magnitude remains driven by engineered heterogeneity, saturation, integer floors, and novelty bonuses.
- **Assignment:** Complete paired evaluation and policy-free substreams are appropriate for a deterministic finite estimand.
- **Protocol deviation:** Not adequately controlled because target-fetch crash state and pre-freeze abandonment are not durably representable.
- **Missing data:** Invalid runs are declared non-evaluable, but the summary/ledger contradiction prevents deterministic terminal recording of many such runs.
- **Measurement:** SDK scoring and predicate construction are well anchored by matching source hashes. Exact reproducibility remains underdetermined by the numeric environment.
- **Analysis flexibility:** The primary estimand and binary decision are fixed. Secondary metrics, resource binding, and several schema cross-fields remain flexible.
- **Selective reporting:** Pre-pulse ACK and hashes are useful custody evidence. They do not “prevent” suppression of an unfavorable terminal result because only pre-outcome information is externally posted and later obligations are local.

### Schema defects

The most consequential remaining underdetermination is at contract 126–135 and schema 115–210:

- `reset_band`, `linear_band`, and `curvature_band` lack closed, split-conditional vocabularies.
- Candidate and phase ordinal origins, ranges, and relationships are unspecified.
- `mixtures.tsv.selected` has no exact type or spelling.
- Conditional relationships among `status`, `error_code`, `attempted`, `retained`, score hash, and returned counts are not defined.
- The single-valued `binding` enum has no precedence rule when multiple capacities tie.
- The formulas for positive-regret fractions, stratum gain, all four secondary rational metrics, and probe-cost share are absent.
- `percent_fixed_12` is syntactically constrained but not linked to its numerator and denominator.
- Forty stratum objects need not be unique or ordered; six histogram objects need not be the frozen bins or sum to 320.
- The selected mixture array need not sum to eight.
- `failure_counts_by_error_code` does not require every enum key despite the prose claiming all keys, including zeros, are mandatory.
- The invalid-summary case is not modeled separately from the complete valid-summary case.

These are not cosmetic limitations of JSON Schema: several underlying formulas and conditional semantics are absent from the contract itself.

### Taxonomy verification

The taxonomy is defensible:

- Opportunity: Evidence Gap dominant; Resource Bottleneck secondary.
- Method: Empirical Mapping dominant; Optimization/Search secondary.
- Operation: replace one split-global argmax with profile-conditioned argmaxes.

### Anti-stacking check

Pass. The intervention is one structural relaxation, not a stack of components. Same-probe global and adaptive policies make the paired conditional-regret contrast interpretable. The denominator-eight mixture is correctly described as a restricted secondary comparator, not a universal nonadaptive optimum.

### Occam’s razor

The core scientific statement is simple: measure finite oracle conditional regret on one heterogeneous table and verify zero regret on a homogeneous table. The extensive beacon, schema, and custody machinery is infrastructure, not mechanism. That distinction is stated correctly, though the infrastructure currently exceeds what its incomplete terminal semantics can guarantee.

### Alternative explanations

A positive result can be explained by engineered equal weighting of heterogeneous/cliff-heavy cells, the generic advantage of 320 oracle decisions over one, saturation and integer floors, the uniqueness bonus, perfect probe stationarity, or restriction of the mixture class. The document acknowledges most of these and appropriately limits scope.

### Overall: NEEDS_REVISION

Required fixes, in severity order:

1. **Close invalid and terminal outcomes** across hypothesis 331–345, 356–383; contract 146–178; schema 102–210. Define a minimal schema-valid terminal outcome for every failure, make invalid ledger resolution depend on that artifact rather than an impossible complete summary, permit pre-freeze abandonment, and define the durable `COMPLETED` transition.

2. **Make target fetch crash-safe** at hypothesis 370–380 and contract 162–166. Add an exclusive pre-fetch attempt artifact/state so a crash after the GET cannot permit another fetch.

3. **Finish the machine specification** at contract 126–135 and schema 115–210. Add the missing TSV enums/types/conditional rules, binding-tie semantics, exact metric formulas, array ordering/uniqueness/bin constraints, mixture-sum validation, and mandatory failure keys.

4. **Make numeric execution reproducible** at hypothesis 150–164 and contract 21–27, 136–144. Pin the mathematical runtime or use reproducible correctly-rounded functions, and certify cliff-floor stability.

5. **Provide actual support for the primary prediction** at hypothesis 55–74 and 221–251. Supply either a deterministic lower bound over the frozen support or a preregistered, non-target calibration ensemble with sensitivity to factor weights and saturation. Otherwise retain it explicitly as an unsupported low-confidence conjecture.

6. **Correct the selective-reporting claim** at hypothesis 442–445 and contract 156–167. Post every terminal artifact hash/status to the same externally timestamped thread or weaken “prevent” to “mitigate under honest reporting.”

## Actionable coaching

Model terminal outputs as a discriminated union: a compact `OUTCOME.json` with `VALID` and `PROTOCOL_INVALID` branches. The valid branch can require the complete summary; the invalid branch should require the last durable state, error code, available hashes, partial-row counts, and prediction-ledger resolution. This removes the current pressure to fabricate complete metrics after a crash.

Add `TARGET_FETCH_STARTED.json` by exclusive creation before network access. Entry with this marker but no raw pulse must abandon; entry without it may perform the sole fetch.

Move every cross-field rule into named validator predicates with golden positive and negative fixtures. In particular, define secondary numerator/denominator formulas and make binding either a set of all active constraints or a single enum with frozen precedence.

For the primary magnitude, a calibration distribution over independently derived non-target masters would provide honest predictive justification without changing the finite target estimand. Report the fraction clearing 5%, the minimum observed margin, and sensitivity to stratum weighting.

## Round 8 gate decision

The adverse `NEEDS_REVISION` verdict stands. The reported 498 hypothesis lines,
204 contract lines, 231 schema lines, contract/schema hashes, JSON validity, Draft
2020-12 metaschema validity, and five source hashes were independently verified
against commit `3033b15`. The v6 artifacts remain immutable. Phase 2 is closed;
no implementation, freeze, target, profile, experiment, submission, or Kaggle
action exists.
