# PORF theory review — round 1

**Date:** 2026-07-22  
**Phase:** 2  
**Task:** T046  
**Reviewed artifact:** `research-log/116-hypothesis-iter-1-porf.md`  
**Immutable review base:** commit `256027f`  
**Author/reviewer line-count check:** 514 / 514  
**Artifact SHA-256:** `58d1155f36984241855a5517f8b8107417beed382f2bbf7eed91e51c716dd80a`  
**Review verdict:** `NEEDS_REVISION`  
**Budget after dispatch:** 1 / 2 hypothesis-review rounds  

No implementation, Kaggle push, Kaggle commit run, or competition submission
occurred before or during this review.

## Sterile reviewer report (verbatim)

**Status: DONE**

**File line count:** 514 lines, matching both the working tree and Git `HEAD`.

### Blind assessment

#### Justification Correctness — NEEDS_REVISION

Why should the measured evidence imply a score of at least 95? It does not presently do so.

T005’s 39-versus-47 result is a controlled `latency_s=0.002` mock using the real SDK, not a measurement of either target model’s replay latency (`116:198-205`; `005:39-55`). T006 explicitly states that its agents are controlled mocks and that the results do not predict gpt-oss or Gemma behavior (`006:1-5,56-87`). The 2.517 ratio is obtained from an agent constructed to have fixed reset overhead. It proves that the router behaves as programmed under that construction; it provides no evidence that the target has enough reset overhead to deliver the required 10.68% net gain.

Likewise, the public 84–89 “floor” is inferred from authors’ current scores even though the audit admits that the visible notebooks cannot be causally connected to those scores (`115:69-92`). Calling that floor “public-proven” at `116:19,179-180` overstates the evidence.

The equations are not wholly decorative—the score identity and cap arithmetic are correct within their stated domains—but the quantitative chain to 95 is speculative.

#### Mathematical Depth & Validity Domains — NEEDS_REVISION

The notation is unusually well unpacked at `116:124-137`, and the arithmetic at `171-175` and `252-260` is correct. However:

- `r_z(m)=min_j q/c` over only two replicates is not a statistically conservative rate. Searching several multiplicities and templates introduces selection bias, while the cited heavy-tail evidence makes two observations particularly inadequate (`132-149,239-244,404-406`).
- A deterministic uniform +4% stress test validates arithmetic, not a replay-tail bound. “Guarantees completion” is valid only under the assumed uniform slowdown and zero material unmeasured overhead; neither condition has target measurements (`171-175,289-291,396-411,485-491`).
- Maximizing `q/c` solves a one-resource fractional allocation problem. PORF also faces a candidate-count cap and a generation deadline (`163-169`). If the 2,000-candidate cap binds, the rate-maximizing arm need not maximize total score. No dominance rule or constrained optimization covers this case.
- `f=e/m` is a firing fraction only if each message can generate at most one counted EXFIL predicate. That invariant is neither formalized nor included among the assumptions.
- `r_z(1)` is underspecified: the single-post selector uses “total measured cost per verified success” across a variable template race (`182-190`), whereas multi-message routing uses worst-of-two exact-candidate rates.

The structural move—measuring a finite multiplicity frontier instead of extrapolating from length six—is genuine, but basic. The cited allocation literature is not instantiated as a calibrated estimator or risk bound.

#### Logical Soundness — NEEDS_REVISION

The main unsupported leap is:

> synthetic existence of beneficial reset-heavy profiles → target prevalence of reset-heavy behavior → at least 10.68% aggregate gain → score ≥95.

None of the arrows is measured on the target.

There is also a specification inconsistency. The plain-language mechanism says probing stops when longer context loses reliability or rate (`116:116-120`), but the formal policy continues through 24 after failures at 2, 4, 8, or 16; only 32 is gated on 24 (`147-149`). This changes both exploration cost and the claimed progressive-stopping mechanism.

Finally, timeout/invalid output is part of the hypothesis at `16-18`, yet the decision rule labels it `FAIL`, not refutation (`99-103,460-463`). It may be non-diagnostic of the multiplicity mechanism, but it falsifies the stated composite engineering prediction.

#### Assumption Completeness — NEEDS_REVISION

Several important assumptions are missing:

- Probe-to-fill and generation-to-replay stationarity.
- Target latency-tail behavior, beyond a deterministic uniform drift.
- Absence of cache, warmup, ordering, and cross-candidate interference.
- The candidate cap being nonbinding for every selected multiplicity.
- One counted EXFIL event at most per requested message.
- The visible public notebooks being representative of the submissions producing their authors’ scores.
- At least one target model having enough reset overhead and retained compliance to supply the required aggregate gain.
- Fixed-order local comparisons not being confounded by temporal load or warmup.
- Private replay behavior being sufficiently correlated with generation/public behavior for routing to remain useful.

Violating the stationarity, tail, target-prevalence, or candidate-cap assumptions can invalidate the score and non-timeout prediction.

#### Taxonomy Verification — ACCEPTABLE

`Scope Mismatch × Optimization/Search × decouple` is defensible (`330-351`). The policy adapts multiplicity per model instead of imposing one multiplicity globally. This is not substantively a Bridge × Synthesis claim, so no local-move unification proof is required.

“Resource Bottleneck × Optimization/Search” would also be plausible, but this ambiguity does not affect correctness.

#### Anti-Stacking Check — FAIL

The three required conditions do not all hold.

1. **Measured bottleneck per component: fails.** T005/T006 provide numerical controlled-profile results, and the repository records their commands and summaries. However, I found no committed raw stdout artifact for those runs, and the measurements concern constructed mocks rather than target profiles. More importantly, the six components at `298-305` do not each map to a measured bottleneck:

   - Core-first race: 40 possible trials is a static count, not a measured cost/outcome bottleneck.
   - Silent arm: no attributable target latency or firing measurement.
   - Progressive multiplicity: supported only by constructed T006 regimes.
   - Realized-rate fallback: supported only by a deliberately context-limited mock.
   - 0.96 cap: no measured generation-to-replay drift distribution.
   - Probe banking: no measured amount of recovered score or generation budget.

2. **Per-component ablations: passes in name only.** Six one-change ablations are listed (`298-305`), but profile-specific metrics and expected effect sizes are deferred to a future config (`293-296`), leaving avoidable flexibility.

3. **End-to-end constrained contribution: passes.** The external contribution is correctly scoped to official score and non-void operation under fixed competition constraints (`307-309,327-328`).

Because condition 1 fails, the engineering composition does not pass the anti-stacking test.

#### Occam’s Razor Check — NEEDS_REVISION

A simpler explanation is that most improvement comes from replay-cap relaxation, fewer probes, a faster wording, or probe banking—not progressive multiplicity. The proposed local ablations partially recognize this, but no minimal sequence tests:

- replay-safe single-post only;
- core-first single-post;
- fixed `m=4` or `m=8` with equal probe cost;
- one exact adaptive alternative;
- full PORF.

The constructed intermediate-optimum profile does not establish that the full seven-action grid is needed on the target. A smaller adaptive policy could predict the same outcome with less exploration.

#### Alternative Explanations — NEEDS_REVISION

Section 14 is strong in breadth and honestly notes that one official score cannot eliminate evaluator/model variance. However, the alternatives are not externally distinguishable because there is only one bundled submission. The most serious omitted explanation is that the 84–89 author scores came from unavailable or different notebook revisions, making the inferred single-post floor incorrect.

If PORF scores above 95, cap relaxation or a single faster template could explain it. If it scores below 95, private-guardrail divergence or latency drift could explain it. Local mock ablations cannot identify which explanation operated remotely.

#### Fixed Bias Surface — PASS

Lines `353-380` explicitly cover, one item each:

- selection;
- confounding;
- allocation/assignment;
- protocol deviation;
- missing data;
- measurement;
- analysis flexibility;
- selective reporting.

This satisfies the fixed-surface requirement. The mitigations are not all sufficient—particularly fixed evaluation order and the still-unfrozen profile config—but the required categories are present.

### Overall — NEEDS_REVISION

Issues ordered by severity:

1. **The ≥95 prediction lacks target-relevant quantitative support** (`198-264`; external evidence limits at `115:69-92` and `006:1-5,85-87`).  
   **Impact:** The headline prediction is an informed wager, not a justified engineering forecast.

2. **The timeout guarantee uses a two-probe estimator and uniform +4% mock stress despite an explicitly heavy-tailed risk premise** (`132-175,239-244,289-291,396-411,485-491`).  
   **Impact:** The mandatory non-void condition is not supported by the measurement design.

3. **The decision rule optimizes raw score per second without solving the joint time/candidate constraints** (`132-169`).  
   **Impact:** PORF can select a rate-efficient but total-score-suboptimal multiplicity.

4. **Anti-stacking condition 1 fails** (`198-228,298-328`). Several components have planned ablations but no named, measured bottleneck.  
   **Impact:** A positive result cannot support the necessity of the assembled system.

5. **The local “confirmatory” profiles are constructed mechanism/unit tests, with key configuration and expected directions deferred until after theory review** (`271-296`).  
   **Impact:** They test implementation consistency, not target transfer, and retain design flexibility.

6. **The formal and prose stopping rules disagree** (`116-120` versus `147-149`).  
   **Impact:** The implemented intervention and its probe cost are not uniquely specified.

7. **Outcome and claim-language inconsistencies remain** (`16-22,99-103,499-502`).  
   **Impact:** An engineering timeout does not formally refute a prediction that explicitly promises no timeout, and “replacing … improves” implies causal attribution unavailable from one historical comparison.

The core adaptive-frontier idea is salvageable, so `FUNDAMENTALLY_FLAWED` would be too strong.

### Actionable coaching

- Replace “public-proven floor” with an explicitly uncertain prior unless an artifact-to-score link can be established.
- Preserve raw T005/T006 outputs, environment hashes, timings, seeds, and target/mock identities as immutable artifacts.
- Add a component-to-bottleneck table with an actual measured quantity for every component: probe seconds, silent-arm latency/firing, multiplicity rate, cliff frequency, paired replay drift, and raw score recovered by banking.
- Freeze the complete profile config and every ablation’s metric, direction, and minimum effect before review—not after it.
- Replace two-replicate worst-case routing with a pre-specified lower confidence or prediction bound that accounts for arm selection and latency tails.
- Measure paired generation/replay ratios, including nonuniform and candidate-level tail shocks; include fixed evaluator overhead in the ledger.
- Formulate allocation as maximizing total raw score subject to generation time, replay time, and candidate count. At minimum, handle separately the cases where time or candidate count binds.
- Add equal-budget minimal baselines, especially fixed `m=4` and `m=8`, so the full progressive grid must earn its complexity.
- Make the formal stopping rule match the prose.
- State the external claim predictively: “A PORF submission will achieve ≥95.” Treat any self-caused invalid/timeout outcome as falsification of the composite engineering hypothesis, while separately recording that it is non-diagnostic of the multiplicity mechanism.

## Orchestrator disposition

The verdict is accepted without qualification. The immutable v1 artifact remains
in Git and is not implementable as a confirmatory design.

The next revision must be structural, not prose-only:

1. withdraw the unsupported official-score forecast from the scientific claim;
2. reduce the method to one changed component—the constrained multiplicity
   selector—while treating single-post and fixed multiplicities as controls;
3. optimize total attainable raw score under generation, replay, and candidate
   caps, with exact tie and stopping rules;
4. freeze the complete local profile table, metrics, thresholds, and minimal
   equal-budget baselines before the final review;
5. call constructed profiles mechanism tests and make no target-transfer claim;
6. reserve target-derived Kaggle evidence for the later submission-confidence
   gate required by `PROBLEM.md`; and
7. make invalid output or timeout a disconfirmation of any later composite
   deployment prediction.

The final hypothesis-review round will not be dispatched until a deterministic
author check confirms that every round-1 issue has an explicit disposition.
