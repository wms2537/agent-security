Status: DONE

File line count: **533**, verified against `git show HEAD:research-log/167-hypothesis-iter-8-prac24-v2.md | wc -l`.

## Blind assessment

### Previous-review issue dispositions

1. **Exchangeability claim — RESOLVED.**  
   Lines 124–152 and 225–254 replace predecessor-sensitive method executions with an independently randomized 19/3 role split over a common, role-blind potential-trace table. Conditional on that table, the role permutation—not target-model sampling—defines the probability space. Arbitrary host drift may change table values, but does not bias roles if the capture kernel and orchestration are genuinely role-blind. Lines 391–415 correctly state the validity domain and invalidate inference upon leakage or redraw.

2. **Engineering component contract — RESOLVED as to the previous wording defect.**  
   Lines 258–281 demote HCMS to an inherited base. Lines 314–349 give three named components, one-field removals, and exact predicates. The prior compound “high-ceiling monotone salvage” component is gone.

3. **Candidate-boundary bottleneck — RESOLVED by withdrawal.**  
   Lines 269–271 and 446–454 explicitly disclaim candidate-boundary amortization and assign HCMS no component credit. Direct boundary measurement is no longer required for the narrowed claim.

### Justification Correctness

The finite-population result is correct, although its tie argument should be stated more precisely.

For a fixed evaluation slot, consider its score plus the 19 calibration scores. Under the uniform role permutation, the evaluation position is uniformly distributed among those 20 positions. Failure of \(Z_{\mathrm{eval}}\le\max Z_{\mathrm{cal}}\) requires the evaluation score to be the unique strict maximum, whose probability is at most \(1/20\). Hence coverage is at least \(19/20\); ties can only improve it. The phrase “rank is uniform” at lines 229–232 is not literally well-defined under ordinary tied ranks, but the claimed inequality remains valid.

I also re-derived:

- From \(Z^R_{\mathrm{eval}}\le q_R\), every policy-prefix ratio satisfies \(A(k)/L(k)\le q_R\); admission \(q_RL(k)\le2\) therefore implies \(A(k)\le2\).
- From \(Z^G_{\mathrm{eval}}\le q_G\), each selected arm has \(g\le q_Gb(m)\). The remaining-budget precheck gives the claimed induction against generation overage.
- Replay-spike: full actual replay is \(0.19q_R\lfloor10/q_R\rfloor\le1.9\), whereas the \(q_R=1\) removal incurs \(1.9q_R>2\) exactly when \(q_R>20/19\).
- Long-setup: when \(u=q_Gb(24)>0.1\), \(r=(u+0.1)/2\) satisfies \(0.1<r<u\), and \(d=r+0.05>r\); thus full refuses while the point-reserve removal starts and overruns.

The cited engineering measurements are real and reproducible. The frozen hashes match, the author checker passes, and the sealed diagnostic recomputes `187/189`, `0/36`, `1.102552878986`, 420 tail paths, `59.767362233368` seconds, four generation overages, and `44/84`.

The remaining defect is empirical rather than algebraic: the measurements and proposed removals do not show that all three components independently earn their place in the end-to-end system.

### Mathematical Depth & Validity Domains

The probability object is now concrete: a finite uniform measure over role permutations of 22 captured units per profile. The dependent candidate stream is substantively mapped to one maximum cumulative-prefix score rather than treated as exchangeable candidate rows. Symbols \(a\), \(\ell\), \(Z^R\), \(g\), \(b\), \(Z^G\), and \(q\) are operationally bound.

Validity domains are unusually explicit: role blindness, uniform assignment, no redraw, matched support, censoring to infinity, potential consistency, complete-arm timing, marginal-only coverage, offline scope, and no target transfer are all stated. This is not decorative mathematics.

The only mathematical wording correction needed is the tied-rank point above.

### Logical Soundness

The theorem-to-budget deductions follow. The inference boundaries—no joint 0.95 statement, no simultaneous coverage, no conditioning on a finite or sub-ceiling \(q\), and no target guarantee—are correctly enforced.

The engineering inference does not follow:

- The complete-trace replay envelope’s own evidence at line 318 includes **zero aggregate HCMS replay overages in 36 primary cells**. `187/189` is a failure of the superseded candidate-wise validity criterion, while the single excluded safety ratio `1.10255` did not produce a full-cell overage.
- All four observed generation overages cited for the atomic gate occurred after the first no-fit—the exact tail already eliminated by the absorbing transition. Thus the absorbing and atomic components do not presently have independently measured system bottlenecks.
- Lines 329–349 create q-dependent fixtures after calibration. These prove implementation conformance, but they guarantee a contrast by construction whenever their threshold precondition holds. They do not demonstrate that removing the component harms the held-out policy result.

Consequently, lines 322–325 and 451–459 overstate what the evidence establishes.

### Assumption Completeness

The assumptions needed for the finite-population result are substantially complete. The load-bearing ones are:

- role labels cannot affect capture directly or through runner control flow;
- capture and arm-order randomization are independent of role;
- no outcome-dependent redraw occurs;
- policy projection cannot alter stored outcomes;
- the claim remains restricted to the controlled deterministic-profile table.

Violation of any of the first four destroys the marginal coverage interpretation.

For the engineering composition, a missing assumption is being used implicitly: that bespoke conformance failure is sufficient to establish component necessity. That is not an accepted engineering validity condition; necessity must be shown on a predeclared relevant evaluation or stress distribution, not merely on an adaptively parameterized unit fixture.

### Taxonomy Verification

The classification is defensible:

- **Opportunity:** Failure/Risk Gap, secondarily Resource Bottleneck
- **Paradigm:** Robustification, secondarily Formal Derivation
- **Dominant operation:** replace

The contribution replaces point/candidate resource accounting and retry behavior. It is not Bridge Opportunity × Synthesis/Unification, so the heightened bridge-template tripwire does not apply.

### Anti-Stacking Check

1. **Specific measured bottleneck per component: FAILS for the joint three-component claim.**
   - Absorbing no-fit passes: 420 paths and 59.767 seconds for three candidates is direct.
   - Replay envelope is weakly supported: the primary aggregate endpoint had 0/36 overages.
   - Atomic gate is not independently identified: all four observed overages lie in the tail already removed by absorption. `44/84 > 0.1s` shows reserve underestimation, but not a residual overage after absorption.

2. **Per-component ablation: FAILS.**  
   Lines 327–349 specify conformance fixtures excluded from efficacy, not component removals evaluated on the same held-out profile traces. Because two fixtures are functions of the observed \(q\), their divergence is algebraically manufactured. This is useful software testing, but not empirical ablation evidence.

3. **End-to-end constrained claim: PASSES.**  
   The stated contribution is the constrained system result and not the act of combining components.

The strict engineering anti-stacking gate therefore remains open.

### Occam’s Razor

A materially simpler hypothesis fits the existing primary evidence: inherited HCMS plus absorbing no-fit. The retrospective artifact reports no aggregate HCMS replay overages, and absorption removes the tail containing every observed generation overage. The current evidence does not yet demand both calibrated envelopes in addition to absorption.

The full three-component design may ultimately be justified as prospective risk control, but that must be demonstrated against q-independent held-out stress evidence or factorial removal results. A fixture constructed from the component’s own calibrated \(q\) cannot defeat the simpler explanation.

### Alternative Explanations

- Absorbing no-fit alone may explain controlled non-overage.
- Authored steady/reset/cliff profile composition may drive the 1.10 HCMS ratio.
- The replay and atomic fixtures may show only implementation conformance, not occurrence on the controlled or target distributions.
- The max-over-policies calibration may make a simple fixed policy outperform HCMS.
- Host drift does not invalidate randomized-role inference, but can still limit transfer.
- Nine evaluation traces can establish their realized aggregate, not a stable expected advantage over a broader master/profile population.

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. **Replace conformance-only removals with genuine held-out component ablations** — lines 314–349 and 451–459. Project each one-field removal over the same nine evaluation traces and report its intended endpoint: replay overages/slack for \(q_R=1\), post-no-fit paths/time/raw for retry, and generation overages/slack for the 0.1-reserve gate. Keep bespoke fixtures as implementation tests only.

2. **Establish distinct bottlenecks or reduce the component claim** — lines 316–320. In particular, test whether the atomic gate adds anything after absorption and whether the replay envelope prevents any held-out aggregate failure. If not, demote them to conservative guardrails or remove them from the claimed engineering contribution.

3. **Test the simpler absorbing-only explanation first** — lines 322–325 and 461–470. The current evidence supports it at least as well as the three-component account.

4. **Correct the tied-rank wording** — lines 229–238. Prove the bound through the probability of a unique strict maximum rather than claiming an unqualified uniform rank under ties.

## Actionable coaching

- Because all policies already project the same complete trace table, run a preregistered \(2^3\) factorial projection over replay envelope on/off, absorption on/off, and atomic gate on/off. This is cheap and directly reveals redundancy and interactions.
- Add q-independent stress traces fixed before calibration. A stress distribution may be adversarial, but its values must not be constructed from the realized \(q\) if it is to count as component evidence.
- If the replay removal remains safe on all held-out traces, describe the envelope as a theoretically motivated guardrail with marginal finite-population coverage, not an empirically necessary engineering component.
- For the atomic gate, report the residual generation-overage rate after absorption with the atomic gate removed. This is the clean contrast currently missing.
- If the 1.10 result is intended to generalize beyond the realized nine traces, define the master-distribution estimand and add uncertainty or replication. Otherwise consistently call it a fixed-sample matched-trace result.
- If a simultaneous system-safety guarantee is later desired, recalibrate a joint resource score or adjust the risk allocation. The present separate 0.95 marginals correctly do not support simultaneous 0.95 coverage.
