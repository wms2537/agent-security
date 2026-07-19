# ORF-B theory review round 11 — RIGOROUS

**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed

## Context

The user authorized ten additional hypothesis-review rounds, raising the limit
from 10 to 20. Round 11 was charged at dispatch against immutable commit
`74d1836`, containing the 500-line v9 hypothesis and its v7 machine artifacts.
The dispatch used only the sterile theory-review template plus the four round-10
issues. No held-out, beacon, evaluator, profile, submission, or Kaggle action was
authorized or performed.

## Reviewer report (verbatim)

**Status: DONE**

Repository note: `reference/mathematical-thinking.md` and `reference/idea-taxonomy.md` are absent from this checkout. I nevertheless evaluated the mathematical structure directly and cross-checked the taxonomy terminology against the project’s prior review record. This does not prevent assessment of the hypothesis itself.

## 1. Blind assessment

The reviewed hypothesis has **500 lines**, matching the committed file. I also verified all four declared artifact hashes, the `core/cells.py` hash, the reference-checker output, and `git diff --check`.

### Previous-review dispositions

1. **RESOLVED — SDK score/hash semantics.**  
   At lines 164–188, `candidate_id` is explicitly separate from the actual 16-hex SDK `cell_signature` hash. Lines 185–188 require within-trajectory uniqueness and invalidate collisions. Lines 197–199 bind `core/cells.py`. The checker recomputes predicates, signatures, `get_score_cell_hash`, singleton raw scores, and cross-fixture uniqueness from preserved traces.

2. **RESOLVED — mixture scheduler.**  
   Lines 248–281 define the composition space, cycle-local initialization, `t=0..7`, eligibility, deficit rule, tie-breaking, immutable cycle, repetition via `j mod 8`, and advancement on emitted attempts—including zero yield—but not precheck stops. All 3,003 compositions execute to `count==h`. Minor notation issue: line 259 should literally write `argmax_{i in eligible}`; the surrounding text, frozen contract, and checker make the intended domain unambiguous.

3. **RESOLVED — external crash reconciliation.**  
   Lines 333–374 make idempotent create and linearizable keyed listing mandatory preconditions. Lines 358–371 persist intent before external calls and specify list-before-create recovery. Freeze is forbidden if those semantics cannot be established. This is exactly the conditional closure requested previously.

4. **RESOLVED — preserved evidence.**  
   Lines 24–37 and 190–199 name and hash the fixtures. Lines 461–487 give a reproducible checker invocation. The hashes and reported output reproduce exactly.

### Justification correctness

The scientific mechanism is the relaxation of a feasible action class:

- The global policy is restricted to diagonal actions `(m,…,m)`.
- The adaptive oracle can choose from the product action space `(m_z)_z`.
- Therefore the adaptive feasible set contains the global one.

For a global maximizer \(m_g\), I re-derived

\[
A-G=\sum_z\left[\max_m S_z(m)-S_z(m_g)\right]\ge0.
\]

This proves direction only, not 5% magnitude, exactly as lines 73–75 state. The materiality test \(100(A-G)\ge5G\) is algebraically equivalent to \((A-G)/G\ge0.05\) when \(G>0\).

I also re-derived the score identity. With exactly \(e\) severity-5 predicates, each contributes 16. A singleton distinct score cell contributes one novelty bonus of 2, giving \(q=16e+2\). The actual SDK implementation and fixtures support this, conditional on the required trajectory-wide uniqueness assertion.

The homogeneous proof is sound:

- Probe cost is \(87b\) and probe score is \(16(87)+2(7)=1406\).
- Remaining replay capacity is \(T=8100/b-87\in[588,1533]\).
- Candidate, generation, and saturation constraints are looser.
- For \(m\ge2\),
  \[
  \lfloor T/m\rfloor(16m+2)\le17T<18(T-1)\le18\lfloor T\rfloor.
  \]
- Hence \(m=1\) uniquely maximizes every homogeneous profile.

Thus the negative result is correctly characterized as an implementation invariant, not evidence for the 5% primary magnitude.

The conditional Clopper–Pearson statement is also correct: with 64 successes, the one-sided 95% lower endpoint solves \(p^{64}=0.05\), yielding \(0.05^{1/64}=0.9542702976\ldots\). The entry correctly makes this depend on random-oracle-equivalent outputs, fresh target randomness, and outcome-independent selection. NIST describes the beacon as publishing fresh 512-bit public values, although the current service remains labeled beta/work in progress. [NIST Beacon project](https://csrc.nist.gov/Projects/interoperable-randomness-beacons/beacon-20)

No equation is decorative. Each either defines the estimand, determines execution, states a decision rule, or proves the homogeneous invariant.

### Mathematical depth and validity domains

All important symbols are concretely bound:

- \(z\): one synthetic keyed profile.
- \(m\): one of seven legal fill lengths.
- \(S_z(m)\): exact capped post-probe score for that profile and length.
- \(A\): sum of profile-wise maxima.
- \(G\): best sum under a single shared length.
- \(T,O,M\): explicitly secondary aggregate controls.
- \(P/U\): probe-generation share.

The structural insight is feasible-set containment, not symbol manipulation. The validity domain is unusually narrow but explicit: deterministic synthetic profiles, oracle observation of all seven action values, independent per-profile budgets, exact frozen SDK semantics, and no shared live-system effects. Violating these assumptions changes the estimand into a learning or live-systems problem rather than merely adding noise.

### Logical soundness

The reasoning is internally sound under its stated domain. The entry does not infer the 5% magnitude from \(\Delta\ge0\), does not treat the homogeneous equality as replication, and does not elevate calibration into confirmation.

The claim verbs remain predictive. It does not claim population causality, live performance, learnability, private transfer, or Kaggle improvement.

### Assumption completeness

The load-bearing assumptions are present at lines 131–150 and 416–427:

- SHA-256 random-oracle behavior over distinct inputs.
- Fresh public target randomness.
- No concealed label, prefix, support, or parameter search.
- Deterministic stationary traces.
- Additive independent per-profile resources.
- No cache, concurrency, shared overhead, or deadline-tail effects.
- Fully observed counterfactual values for all seven actions.
- Frozen SDK and numeric execution.
- Honest repository/thread custody.
- Verified POSIX and external idempotency/linearizability semantics.

Violating the first three removes the probability interpretation. Violating the next five destroys the finite score table. Violating the custody assumptions removes held-out/reporting assurance but does not retroactively alter a locally preserved scientific outcome.

### Fixed bias surface

Lines 392–414 explicitly cover all eight required classes:

- **Selection:** engineered support and the conditional independence requirement are named.
- **Confounding:** pairing isolates action-scope relaxation only on the finite table; engineered cliffs, floors, saturation, and novelty remain explanations of magnitude.
- **Assignment:** paired deterministic evaluation removes order effects only without interference.
- **Protocol deviation:** markers, hashes, total schedulers, and no retry make deviations observable or invalid.
- **Missing data:** incomplete prefixes cannot enter metrics.
- **Measurement:** the real SDK predicate/signature/scorer path defines the outcome.
- **Analysis flexibility:** one primary contrast and frozen outcome map.
- **Selective reporting:** suppression is mitigated under honest operation but not cryptographically prevented.

This is complete and appropriately specific.

### Taxonomy verification

The classification matches the actual contribution:

- **Evidence Gap:** the missing quantity is the held-out magnitude of finite-table conditional regret.
- **Empirical Mapping:** the central result maps that magnitude; exhaustive search is secondary machinery.
- **Replace:** one shared argmax is locally replaced by profile-conditioned argmaxes.

It is not Bridge Opportunity × Synthesis/Unification. No components from separate methods or domains are being integrated, so the heightened tripwire is not triggered.

### Anti-stacking check

The heterogeneous-positive/homogeneous-zero prediction is genuinely about conditioning the action scope. A plain portfolio or union does not itself predict material superiority only under crossed heterogeneity and exact equality under the homogeneous construction.

The negative half is intentionally an invariant, not independent corroboration. The entry states this correctly.

### Occam’s Razor

The irreducible scientific hypothesis is already given at lines 450–454: profile-wise maxima may materially exceed one common maximum on the engineered table and coincide on the homogeneous table. The custody and schema machinery is infrastructure and is explicitly excluded from the scientific contribution.

A still simpler explanation—generic flexibility of 320 decisions versus one—can explain confirmation. That is not an unaddressed rival because the claimed estimand is precisely the value of that restriction, not a unique causal account of why the value exceeds 5%.

### Alternative explanations

A material outcome could be driven by cliff prevalence, cost-band separation, integer floors, saturation, novelty bonuses, generic choice flexibility, or their interactions. Lines 429–434 explicitly acknowledge these and refuse population-mechanism identification.

### Overall: RIGOROUS

The hypothesis is correct, testable, and appropriately scoped. The prior four blockers are resolved.

The strongest objection is that the table is deliberately engineered so a positive result may be a near-tautological consequence of heterogeneity plus greater oracle flexibility. That objection defeats any broad mechanism, population, or deployment claim, but it does **not** defeat this entry: the claim is restricted to the magnitude on one frozen future table, identifies action-scope relaxation as the estimand, labels the calibration conditional, and expressly disclaims mechanism identification and transfer.

## 2. Actionable coaching

- Change line 259 to `argmax_{i in eligible}` so the hypothesis pseudocode is literally identical to the contract and checker.
- Restore the missing taxonomy and mathematical-thinking reference files to the repository so future reviews can verify against the canonical definitions rather than prior-review usage.
- Prefer “oracle value of profile-conditioned action scope” over “oracle information value”; the experiment grants counterfactual action values and does not test whether the probes alone identify the best action.
- Before freeze, preserve the external interface capability evidence as a hashed artifact and test list-after-create behavior in the authorized disposable preflight.
- If a later paper makes a mechanism claim, add factorial ablations for cliffs, floors, saturation, novelty, and cost bands. The current design can establish the combined finite-table magnitude but cannot attribute it.
- Add property-based evaluator tests for score-cell collisions, all precheck-stop branches, crash-after-accepted-create recovery, and homogeneous constraint dominance.

## Gate check

- Reviewer report line count: `git show 74d1836:research-log/018-hypothesis-iter-4-v9-conditional-regret.md | wc -l` -> `500`.
- Immutable target: `git diff --stat 74d1836..512885e -- research-log/018-hypothesis-iter-4-v9-conditional-regret.md experiments/configs/orf-heldout-v7.json experiments/configs/orf-heldout-v7-artifacts.schema.json experiments/poc/orf_v7_contract_reference.py experiments/fixtures/orf-heldout-v7-golden-fixtures.json` -> empty.
- Deterministic reference checker -> `sdk_golden_cases=2`, `mixture_compositions=3003 cycles_exact=3003`, `terminal_artifact_samples=3 schema_valid=true`, `source_hashes=6 valid=true`, `protocol_errors=24 validators=18 aligned=true`, `heldout_run_absent=true`.
- Review accounting: round 11 was charged at dispatch; budget is 11/20.

## Problem alignment

A rigorous finite-table conditional-regret hypothesis tests whether profile-wise
candidate-structure selection has material benchmark-shaped value beyond one
shared structure while preserving the project’s explicit non-transfer caveat.

## Decision

The scrutinized `RIGOROUS` verdict closes the Phase-2 theory gate. V9 remains
immutable. The workflow may advance to Phase 3 PoC design, but no held-out
evaluator, freeze, beacon target, profile evaluation, submission, or Kaggle action
is authorized by this review.
