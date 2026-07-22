# RCMF theory review round 2

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 1 · **Status:** completed — needs revision

## Context

This is the second and final budgeted theory review of the Cycle-3 competition
hypothesis. The reviewed artifact is the immutable
`research-log/121-hypothesis-iter-2-rcmf.md` at commit `dc65853`. It supersedes
the rejected PORF v1 and narrows the intervention to one replay-construction
multiplicity selector.

The reviewer was dispatched with the sterile SciAgent theory-review template,
the canonical mathematical-thinking and idea-taxonomy references, and the ten
round-1 issues in the template's permitted previous-issue slot. The dispatch
was charged before the verdict, exhausting the Cycle-3 hypothesis-review
budget at 2/2.

## Review integrity

- Reviewer-reported line count: `681`.
- Orchestrator verification:
  `git show dc65853:research-log/121-hypothesis-iter-2-rcmf.md | wc -l`
  returned `681`.
- Orchestrator verification:
  `sha256sum research-log/121-hypothesis-iter-2-rcmf.md` returned
  `194e37bb36d30ea9847407b325b498a1795360dd77ec49b9deb3806728c1c27a`.
- This matches the immutable dispatch record in commit `68baa9a`.

## Reviewer report (verbatim)

**Status: DONE**

**File reviewed:** `research-log/121-hypothesis-iter-2-rcmf.md`  
**Line count:** **681**, matching `git show HEAD:research-log/121-hypothesis-iter-2-rcmf.md | wc -l`.

# 1. Blind Assessment

## Overall: NEEDS_REVISION

The revision is substantially more disciplined than v1: it links the 69.570 baseline to the exact artifact, replaces raw-rate optimization with the correct joint-cap objective, narrows the system to one selector, distinguishes controlled mechanics from target evidence, and makes self-caused failure disconfirming. It nevertheless retains two load-bearing correctness defects:

1. `min(e,m)` does **not** enforce at most one credited event per requested message.
2. The 5% leaderboard derivation compares against the wrong counterfactual and then multiplies by two unmeasured transfer assumptions.

These are not cosmetic. The first can select an arm with poor message-level coverage; the second means `73.050` still lacks a valid quantitative chain.

## Previous-review issue disposition

| # | Disposition | Reason |
|---|---|---|
| 1 | **IMPROVED** | `>=95` is withdrawn and the exact 69.570 artifact is linked, but the new 5% chain remains unsupported because the 20% gate is relative to a post-probe `m=1` counterfactual, not the historical full-budget baseline; row share and private retention are also unmeasured. |
| 2 | **IMPROVED** | The universal guarantee and arbitrary +4% stress are removed; the argument is now explicitly conditional. However, remote tails remain unmeasured, and the historical baseline's actual candidate count is unknown, so the no-timeout conjunct still has only conditional support. |
| 3 | **RESOLVED** | Lines 202–214 optimize total raw under generation, replay, and candidate-count constraints; the cap-binding diagnostic is explicit. |
| 4 | **RESOLVED for the stated one-component scope** | The immutable 360-row artifact exists, reports real paired wall-clock numbers, is source-linked in note 120, and precedes implementation. `FIXED-1` is the removal ablation and the contribution is stated end-to-end. This pass is limited to controlled SDK mechanics, not target transfer. |
| 5 | **IMPROVED** | Profiles are correctly demoted to mechanism/stress tests and several parameters are frozen, but the future Phase-3 specification is still incomplete despite lines 412–414 claiming completeness. |
| 6 | **RESOLVED** | Lines 241–249 specify one permanent fallback with no larger-arm continuation. |
| 7 | **IMPROVED** | Decisive outcomes now make self-caused invalidity/timeouts disconfirming and official comparison language is mostly predictive. Lines 639–642 still claim an official confirmation would show that the policy “improves” score for the proposed reason. |
| 8 | **RESOLVED** | Other authors' scores are removed from the quantitative chain and explicitly treated only as plausibility priors. |
| 9 | **UNCHANGED in substance** | `min(e,m)` caps the aggregate count, not the count attributable to each requested message. |
| 10 | **RESOLVED** | `m=1` now participates in the same exact candidate, screen/validation, min-raw, max-cost, and joint-cap construction. |

## Justification Correctness

The source-level mechanism is plausible: generation reuses an environment, whereas replay constructs a fresh environment/agent per candidate. The local artifact is real and traceable: note 120 reports 360 rows, absolute paired timings, three masters, retained failed predictions, hashes, and commit provenance.

The following steps were independently unpacked:

1. **Candidate raw score.** If \(k\) requested messages each produce at least one credited severity-5 EXFIL finding and the candidate has one unique-cell bonus, the conservative score is \(16k+2\). This requires \(k\) to count distinct successful requested messages—not total EXFIL events.
2. **Joint capacity.**  
   \[
   n(m)=\min\{K,\lfloor G/c_g(m)\rfloor,\lfloor R/(1.1c_g(m))\rfloor\}
   \]
   correctly represents the intersection of candidate, generation, and replay-ledger constraints under the stated cost proxy.
3. **Total-value objective.** \(V(m)=q(m)n(m)\) correctly fixes the previous raw-per-second error and permits the candidate cap to alter the optimum.
4. **Common-overhead lemma.** From \(q_m/c_m\ge q_1/c_1\), \(q_m\ge q_1\), and \(h\ge0\):
   \[
   q_m(c_1+h)-q_1(c_m+h)
   =(q_mc_1-q_1c_m)+h(q_m-q_1)\ge0.
   \]
   The lemma is algebraically correct, but it applies only where the zero-surcharge rate premise holds. The entry appropriately concedes that the actual selector uses total raw and integer caps.
5. **5% arithmetic.** \(0.20\times0.25=0.05\) and \(1.05\times69.570=73.0485\) are arithmetically correct. The premises being multiplied are not established, and the 20% quantity is not relative to the historical baseline.

The principal correctness defect is at lines 150–167, 245–247, 506–507, and 542–544. Why is `min(e,m)` treated as per-message coverage? For \(m=4\), if the first message emits four EXFIL events and the other three emit none, then `e=4`, `min(e,m)=4`, and `f=1`. The true requested-message coverage is \(1/4\). The arm incorrectly passes the 0.75 admissibility gate. Disjoint URLs do not repair this unless each event is explicitly matched to its requested message or URL.

The second defect is at lines 219–237 and 338–357. Why should a 20% advantage over `m=1` **after RCMF has spent screen and validation time** imply a 20% gain over the historical baseline, which did not pay those costs? It does not. Line 622 only later requires local fallback capacity of at least 95% of reconstructed baseline. Even granting that unsupported target transfer, \(1.20\times0.95=1.14\): the active pair improves 14%, not 20%; at a 25% aggregate contribution that yields only 3.5%, not 5%.

The equations generally carry the argument rather than decorate it. The defect is not excessive mathiness; it is that one abstraction (`e`) is bound to the wrong construct and the leaderboard calculation multiplies non-comparable quantities.

## Mathematical Depth and Validity Domains

Most symbols are concretely bound, and the entry distinguishes empirical extrema from statistical bounds. That is a genuine improvement. The finite-arm problem is also correctly viewed as optimization over the intersection of three capacity constraints.

Validity domains are candidly stated for stationarity, common nonnegative boundary overhead, evaluator identity, private transfer, and replay drift. However:

- The maximum of five screen samples or three validation samples is not a tail guarantee. Under iid continuous exchangeability, a sample maximum from \(n\) observations has only \(n/(n+1)\) one-step predictive coverage: 5/6 for screening and 3/4 for validation. The entry disclaims a confidence guarantee, but then has no target-tail support for the no-timeout prediction.
- The common-\(h\) lemma does not control multiplicity-dependent replay drift \(d_z(m)\), private-guardrail latency, or nonstationarity. Those are exactly the target risks.
- Lines 194–235 do not state unambiguously whether `G` is recomputed after validation. Using the pre-validation remainder would overstate fill capacity.

The conceptual contribution is a finite constrained selector, not a deep mathematical structure. That is acceptable for engineering, but it should not be presented as stronger theory than it is.

## Logical Soundness

The mechanism chain is sound only up to “candidate construction creates a potentially amortizable fixed cost.” It does not logically reach the numerical leaderboard threshold.

The most serious leap is:

> held-out projected long-arm advantage → 20% improvement in an active model's historical rows → active pair owns at least 25% of baseline → private replay retains gain → aggregate improves 5%.

Only the first term is observed online, and even it uses the post-probe comparator. The remaining links are assumptions. Low confidence and explicit disclosure make the wager honest, but do not make the justification evidentially valid.

A second leap occurs at lines 367–373. The exact target-linked baseline's actual candidate count is explicitly unknown at lines 307–310. `c_m^upper >= c_1^upper` establishes fewer projected boundaries than a contemporaneous RCMF `m=1` policy, not necessarily fewer than the historical artifact's unknown actual `N_1`.

## Assumption Completeness

The assumption list is unusually thorough, but several assumptions are either missing or too weak to support the scope:

- Missing: the end-to-end RCMF policy after screen/validation retains enough capacity relative to the historical full-policy baseline for the 20% arm advantage to imply a 5% aggregate gain.
- Missing: event attribution is identifiable per requested message; aggregate event count is insufficient.
- Ambiguous: `G` is recomputed after validation and before the activation decision.
- Stated but wholly unmeasured: active model pair contributes at least 25% of baseline.
- Stated but wholly unmeasured: long-chain gain transfers to private replay.
- Stated but unsupported in the remote regime: historical and current timing/candidate-count stationarity.

Violating event attribution invalidates selection correctness. Violating the post-probe baseline relationship, row-share, or private-transfer assumptions invalidates the 73.050 derivation. Violating replay stationarity invalidates the no-timeout rationale.

## Taxonomy Verification

- **Opportunity pattern:** Scope Mismatch is defensible because attack-visible timing omits the evaluator's broader candidate boundary.
- **Method paradigm:** Optimization/Search is correct.
- **Dominant operation:** `decouple` is inaccurate. The algorithm does not independently control or estimate construction cost; it replaces fixed `m=1` scope with a constrained adaptive selector. `replace`—or secondarily `adapt`—better describes the actual move.

This is not Bridge Opportunity × Synthesis/Unification, so the heightened Bridge×Synthesis tripwire does not apply. The taxonomy error is minor and does not appear chosen to evade that tripwire.

## Anti-Stacking Check

1. **Measured bottleneck:** Pass, limited to controlled SDK mechanics. The 360-row bundle reports real paired wall-clock values and source-authentic replay construction. It does not measure target magnitude or a naturally occurring target context cliff.
2. **Ablation:** Pass at the claimed component granularity: removing the selector yields `FIXED-1`; fixed-arm and rate baselines diagnose simpler alternatives.
3. **End-to-end claim:** Pass: the stated contribution is the official constrained score/non-void result, not the combination itself.

Thus the formal engineering anti-stacking gate passes. It does not repair the target-threshold or event-attribution errors.

## Occam's Razor

A fixed `m=4` or `m=8` policy could produce the same official outcome. The local constructed profiles show that different regimes can favor different arms, but no target evidence establishes that those regimes occur or vary enough to repay online search.

The revision correctly mandates fixed-arm comparisons. However, “RCMF equals the best feasible fixed arm” at lines 427–430 must include the selector's screen/validation opportunity cost. Merely choosing the same arm as an oracle fixed policy is not equal end-to-end performance.

The simplest serious alternative is:

> use one conservatively chosen fixed multiplicity under the inherited ledger.

That alternative must be beaten end-to-end under equal total budget before adaptivity earns its complexity.

## Alternative Explanations

An official score above 73.050 could arise from:

- target/model/evaluator temporal drift;
- ordinary stochastic score variation;
- a fixed `m=4` or `m=8` policy being sufficient;
- improved message density independent of hidden construction overhead;
- uneven contribution of the active model's public/private rows;
- unexpected extra EXFIL events, currently misread as message coverage;
- the target's baseline template winner or capacity differing from the historical run.

The entry names most of these, but one official historical comparison cannot distinguish them. Therefore lines 639–642 exceed the predictive design when they say confirmation would show that replay-boundary selection “improves” the score for the proposed reason.

## Required revisions, ordered by severity

1. **Replace aggregate event capping with true per-message attribution.**  
   **Locations:** lines 150–167, 245–247, 505–507, 542–544.  
   Define \(s_i=\mathbf 1\{\)at least one credited EXFIL associated with requested message/URL \(i\)\(\}\), then \(\bar e=\sum_i s_i\). Add a concentrated-extra-event adversarial fixture.

2. **Repair the 73.050 derivation using an end-to-end comparator.**  
   **Locations:** lines 22–39, 219–237, 338–357, 551–553, 621–622.  
   The comparison must include template probes, RCMF screen, validation, discarded candidates, fallback, and final fill on the intervention side, against the full historical/reconstructed baseline policy—not `m=1` after RCMF has already paid its search cost. Measure or conservatively bound row share and private transfer; otherwise withdraw the claimed quantitative derivation.

3. **Resolve the replay-risk comparator and remote-tail gap.**  
   **Locations:** lines 307–310, 362–394, 523–550.  
   Do not infer actual \(N_m\le N_1\) from a historical `N_1` that was never observed. Either obtain candidate-count/timing telemetry, enforce a deterministic construction-overhead reserve, or state only a relative conditional risk argument without treating it as quantitative support for no timeout.

4. **Complete the claimed frozen Phase-3 specification.**  
   **Locations:** lines 396–414 and 427–430.  
   “Fixed replay construction,” “same costs,” “large time budgets,” and “the committed config” do not give exact numbers or an unambiguous path. State every numeric cost/budget, repetition count, table, result metric, and whether `G` is recomputed after validation. Define whether “equals best fixed arm” means selected arm or end-to-end raw after search cost.

5. **Narrow residual causal/mechanistic language.**  
   **Locations:** lines 501 and 637–644.  
   An official score confirms the preregistered prediction only. It cannot show that replay-boundary selection caused the score change. Make protocol invalidity consistently disconfirm the composite primary prediction while remaining invalid for mechanism analysis.

6. **Correct the dominant-operation label.**  
   **Locations:** lines 473–486.  
   Use `replace` for replacing fixed candidate scope with the selector; the method does not actually decouple or separately estimate the hidden cost.

# 2. Actionable Coaching

1. Use message-indexed success:
   \[
   s_i=\mathbf 1\{\exists\text{ qualifying EXFIL event matching URL }u_i\},\quad
   \bar e=\sum_{i=1}^{m}s_i,\quad f=\bar e/m.
   \]
   Keep official raw event count separately from selection coverage. Test `[4,0,0,0]` events across four messages; it must yield \(f=0.25\), not 1.

2. Define two end-to-end policy values:
   - `P_BASE`: total returned raw under the exact baseline, including its original probes.
   - `P_RCMF`: total returned raw after all RCMF screens, validation, discards, fallback, and fill.

   Activation or target derivation should compare lower-bound `P_RCMF` directly with upper-bound `P_BASE`. Do not multiply an arm-only margin by historical aggregate score.

3. If the only defensible capacity floor is 95%, propagate it honestly. A 20% long-arm advantage over a 95%-capacity post-probe control implies 14% active-pair gain, not 20%.

4. Add internal ablations even if the selector remains one claimed component:
   - screen-only versus held-out validation;
   - joint-cap versus rate;
   - fallback versus no fallback;
   - adaptive selector versus best fixed arm, charging all search costs.

5. Treat the three/five-sample extrema as engineering heuristics. If a probabilistic safety claim is desired, preregister an order-statistic/tolerance-bound design or sequential risk-control rule with an explicit coverage level and validity assumptions.

6. Rewrite the final interpretation as: “A score ≥73.050 confirms the frozen artifact-level prediction; controlled local ablations determine whether its mechanics behave as designed; neither establishes causal attribution for the remote score.”

## Gate Check

- Theory-review verdict: **NEEDS_REVISION**, with detailed scrutiny and all ten
  prior issues dispositioned.
- Hypothesis-review budget: **2/2 spent**; no third dispatch is permitted
  without explicit user authorization.
- Phase-2 gate: **FAIL / remains open**. A `RIGOROUS` verdict is absent.
- Phase 3, RCMF implementation, Kaggle push, Kaggle commit run, and competition
  submission remain prohibited by the SciAgent justification gate.

## Problem alignment

Rejecting an aggregate-event selector and a non-comparable leaderboard
projection prevents us from spending competition compute on a policy whose
central selection statistic and expected-benefit calculation are unsound.

## Decision

Accept the adverse verdict. Do not implement v2 and do not mutate Kaggle. Route
the defects to Phase 2, which owns the hypothesis and quantitative
justification. A superseding v3 requires additional user-authorized hypothesis
review budget before it can advance.

## Next Steps

If the user grants more hypothesis-review budget, write one immutable v3 that:

1. attributes qualifying events to exact requested message/URL indices and
   includes the `[4,0,0,0] -> 0.25` adversarial fixture;
2. replaces the arm-only 73.050 derivation with a complete `P_RCMF` versus
   `P_BASE` end-to-end comparison charging all probes, validation, discarded
   candidates, fallback, and fill;
3. either obtains target telemetry, reserves replay construction cost
   deterministically, or explicitly narrows the no-timeout claim to a
   conditional risk statement;
4. freezes every Phase-3 number and recomputes `G` after validation;
5. charges all search cost when comparing adaptivity to fixed 4/8 arms; and
6. uses `replace`, not `decouple`, as the dominant operation.
