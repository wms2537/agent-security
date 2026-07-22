# PRAC-24 theory review round 8

Status: DONE

File line count: **527**. Verified against `git show HEAD:research-log/164-hypothesis-iter-8-prac24.md | wc -l`.

## Blind assessment

### Justification Correctness

The conditional mathematics is correct:

- With 19 calibration scores and one exchangeable test score, the 19th order statistic gives marginal coverage \(19/20=0.95\).
- On \(Z^R_{\text{new}}\le q_{\text{replay}}\), \(A(k)\le q_{\text{replay}}L(k)\le2\) for every admitted prefix.
- On \(Z^G_{\text{new}}\le q_{\text{generation}}\), the pre-path charge covers the complete return-ready atomic path.
- The replay-spike inequalities and long-setup fixture inequalities are algebraically correct.
- The entry correctly refuses to turn separate marginal 0.95 statements into a joint or family-wise 0.95 guarantee.

The profile evidence is real and reproducible: the bound hashes match, the author checker returns `PASS`, and the diagnostic reproduces `187/189`, `0/36`, four generation overages, 420 post-no-fit paths, 59.767 seconds, and the 1.392971 ratio.

However, the theorem’s empirical applicability is not justified. Calibration cells at lines 275–284 are four HCMS traces in fixed positions. Evaluation cells at lines 287–300 place HCMS after different predecessor methods. Because the calibrated quantities are wall-clock costs, predecessor-dependent cache, scheduler, allocation, or thermal effects can change the score distribution. Position stratification does not repair a predecessor-protocol mismatch. Lines 410–415 acknowledge these effects but provide no design that removes them. Thus the exchangeability premise at lines 194–202 is not presently credible for the actual calibration/evaluation protocol.

### Mathematical Depth & Validity Domains

The replay mapping is substantive rather than decorative: it maps a dependent candidate stream into a complete-cell maximum cumulative-prefix ratio. Symbols are generally bound to concrete operational quantities, and the entry clearly states marginality, censoring, support, prefix-coupling, and non-transfer boundaries.

The missing object is the probability-generating mechanism for “exchangeable” traces. The masters are fixed and authored, not sampled from a declared population, and predecessor protocols differ. Without a sampling frame or process-isolation argument, \(\Pr\) in lines 198–202 is formally conditional but empirically floating.

### Logical Soundness

Most deductions follow, and the document correctly distinguishes theorem-backed marginal coverage from the stricter empirical zero-overage gate.

The principal logical gap is that “every validity gate passes” at lines 13–14 cannot currently include exchangeability: no observable gate establishes it, and the protocol supplies a concrete reason it may fail. If that assumption fails, both calibrated multipliers lose their stated coverage interpretation.

### Assumption Completeness

The assumption list is unusually complete. The load-bearing assumption is within-stratum exchangeability. Its violation invalidates the finite-sample coverage result entirely, not merely its target transfer.

Wall-clock stationarity and absence of predecessor carryover are also required in practice but are not isolated by the current calibration design.

### Taxonomy Verification

The classification is defensible:

- Failure/Risk Gap, secondarily Resource Bottleneck
- Robustification, secondarily Formal Derivation
- Dominant operation: replace

The contribution begins from a resource-safety failure and replaces point/candidate reasoning with prefix-level admission and an absorbing transition. It is not primarily Bridge Opportunity × Synthesis/Unification.

### Anti-Stacking Check

- **Measured bottleneck per component:** mostly satisfied with real sourced measurements. The exception is the “high-ceiling monotone salvage” row at lines 319–324: its stated mechanism is candidate-boundary amortization, but its evidence is an end-to-end retrospective raw ratio, not a measurement of candidate-boundary cost. Lines 454–455 admit that authored profiles may encode the apparent gain.
- **Per-component ablation:** satisfied for prefix envelope, absorbing no-fit, and atomic generation through clean fixtures. The first row is a compound mechanism with two different controls, not one clean removal. It should be split into high ceiling and salvage/state-transition components or explicitly treated as an inherited base policy with two separate contrasts.
- **End-to-end constrained claim:** satisfied. The claimed contribution is the measured system result under two-second generation/replay constraints, not merely the combination.

The strict engineering anti-stacking gate therefore remains incomplete.

### Occam’s Razor

The design appropriately tests fixed-8 and fixed-24/no-salvage alternatives and rejects HCMS complexity if its gain is below 1.10.

A still-simpler explanation remains plausible: the authored reset-heavy and cliff profiles may create the HCMS advantage. The entry acknowledges this but does not separate it from candidate-boundary amortization.

### Alternative Explanations

The alternatives at lines 446–459 are strong and materially relevant. The most important are non-exchangeable fixed masters, scheduler drift, authored-profile favoritism, and target latency outside controlled support.

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. **Repair or narrow the exchangeability claim** — lines 194–220, 275–300, 374–378, and 410–415. Calibrate under the same predecessor protocol as evaluation, stratify by predecessor, randomize from a sealed sampling frame, or process-isolate cells with evidence that predecessor effects cannot persist. Otherwise remove the operational 0.95 interpretation and treat the multipliers as empirical heuristics.

2. **Make the engineering component contract mechanically unambiguous** — lines 317–325 and 350–365. Split “high-ceiling monotone salvage” into separately measured mechanisms with one clean contrast each, or designate it as an inherited base rather than one of four new components. Define the exact confirmation predicate for every removal.

3. **Measure the claimed candidate-boundary bottleneck directly** — lines 319–321 and 446–455. Report boundary/reset cost or candidate yield per boundary under matched traces; the retrospective aggregate raw ratio does not uniquely identify that mechanism.

## Actionable coaching

- Use calibration schedules mirroring the four Williams evaluation orders, or launch every calibration/evaluation cell in a fresh process with an explicit cache/state reset. Then define exchangeability over a sealed master sampling frame.
- Add a direct profile table for the inherited HCMS structure: boundary constructions, reset time, eligible yield, raw per boundary, and matched fixed-8/fixed-24 contrasts.
- Treat the q-dependent adverse fixtures as deterministic conformance tests. Add at least one held-out, fixed-before-calibration stress profile if the paper will claim empirical component necessity rather than mere implementation correctness.
- State the abstaining procedure’s guarantee explicitly: marginal conformal coverage is not coverage conditional on observing a finite sub-ceiling \(q\).
- Define the \(K=0\) replay-score convention, even if current profiles guarantee \(K\ge1\).
