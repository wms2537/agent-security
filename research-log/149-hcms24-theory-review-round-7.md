# HCMS-24 theory review round 7

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Status:** RIGOROUS

The following independent sterile review is recorded verbatim.

---

**Status: DONE**

Reviewed immutable commit `a8da04e` only.

- Hypothesis: 475 lines; SHA-256 `5db694ca4eec48836b060082a45a8687c14a46177652ede274e0a5c66b281063`
- Config SHA-256: `e71c8a6afb70459077a303652e21063a9c71f60d0650a502de8f63fbfb3c0e59`
- Checker SHA-256: `039b9fe4ac827dbff30094870d9d850584d8aad43c18c9905940bd43272a75e4`
- Immutable diff: empty
- Read-only checker rerun: `hcms24_phase2_author_check_v1=PASS`

## 1. Blind Assessment

### Prior-defect disposition

| Prior defect | Disposition | Evidence |
|---|---|---|
| 1. Comparator implementation uniqueness/symmetry | **RESOLVED** | Sections 8–9 specify one shared kernel for clocks, attribution, identity allocation, replay, stopping, and artifact production. Lines 231–240 and config lines 59–87 enumerate the only policy differences. Fixed-8 retains calibrated accounting and monotone salvage while removing ceiling 24; fixed-24/no-salvage retains ceiling 24 and calibrated accounting while removing prefix salvage and permanent downgrade. |
| 2. Delayed safety contamination | **RESOLVED** | Lines 297–305 place the delayed-cliff case in a separate namespace and mechanically exclude all of its raw, candidates, timing, and replay cost from efficacy. Config lines 166–169 preserve the separation. |
| 3. Replay removal end to end | **RESOLVED** | `hcms_scalar` is a full method whose scalar ledger controls its own fit-before-return decisions, candidate count, state evolution, and stopping. Its own returned candidates are then replayed. The checker verifies that proposal, permitted prefixes, salvage, and transition match HCMS and only the ledger differs. |
| 4. Evidence-backed quantitative margin | **RESOLVED** | The smallest matched antecedent advantage is `44.301%` over fixed-8; the fresh `10%` floor retains only `22.57%` of that observed effect. The entry correctly presents 10% as a conservative engineering materiality threshold—not a confidence bound—and rejects lesser gains under Occam. |
| 5. First-order predecessor carryover | **RESOLVED** | The four Williams orders are position-balanced and contain all 12 directed unequal predecessor pairs exactly once. I independently checked the enumerated sequences; the checker also recomputes both properties. |
| 6. Timing/prefix/scorer/stationarity validity regimes | **RESOLVED** | Sections 9 and 13 explicitly cover time-zero admission, unbounded scheduler tails, rejection on overage, truly nested prefixes, five scorer-identity conditions, monotone/worsening applicability, replay transfer, freshness, completeness, and no recovery or target inference. |
| 7. Failed/post-hoc antecedent disclosure | **RESOLVED** | Lines 40–61, 129–156, 351–357, and 370–374 repeatedly identify the source run as `FAIL`, `6/9`, post-hoc, independent-arm evidence that may motivate but cannot confirm the hypothesis. |

### Justification correctness

The empirical mechanism is coherent:

- Ceiling 24 amortizes per-candidate overhead where long chains remain exact.
- Exact prefix salvage prevents a failed suffix from destroying an already valid prefix.
- Permanent downgrade avoids repeatedly paying for a now-invalid longer path in stable-or-worsening regimes.
- Calibrated replay accounting limits returns before acceptance; it is not merely evaluated retrospectively.
- The scalar removal is endogenous, so its predicted replay overage is a valid system-level removal test.

The no-salvage comparison is fair for the stated integrated-policy claim. It removes both within-path salvage and its resulting permanent downgrade while retaining ceiling 24, the common kernel, and calibrated ledger. Fixed-8 separately removes the high ceiling while retaining salvage. Beating the maximum of both requires HCMS to beat each removal. The design does not separately identify “salvage alone” versus “downgrade alone,” but it does not claim to.

The replay ledger truly controls capacity: ledger fit is checked before a candidate is returned, the selected ledger is charged online, and a method stops or changes state through its own resulting history. Actual replay is a later validity measurement, not the admission rule.

### Mathematical depth and validity domains

I re-derived lines 163–173:

\[
\begin{aligned}
&(16m+2)(h+ka)-(16k+2)(h+ma)\\
&=16h(m-k)+2a(k-m)\\
&=2(m-k)(8h-a).
\end{aligned}
\]

For `m>k` and positive denominators, `R_m>R_k` iff `h>a/8`. Every symbol has an operational interpretation, and the entry correctly limits the result to full coverage with common fixed cost and linear per-message cost. It does not infer that `h` is identified, that 24 is optimal, or that target transfer follows. The equation supplies structural intuition rather than decorative proof.

The calibrated formula is also honestly interpreted: `c1` is a correlated scale surrogate, not a separately identified reset cost.

### Logical soundness and operational totality

The hypothesis has:

- one exact primary comparison;
- complete success, insufficiency, refutation, and invalidation bands;
- explicit all-or-nothing treatment of the joint claim;
- 144 required primary repetitions;
- one separate safety suite;
- no retry, profile replacement, or threshold change after output;
- actual scoring when the restricted `16m+2` identity fails.

The shared-kernel specification is sufficiently total for Phase 2. Phase 3 still must verify that the implementation literally honors it; author-check PASS alone does not establish future implementation symmetry.

### Assumption completeness

The load-bearing assumptions are stated with consequences:

- authored controlled profiles represent only the specified mechanism grid;
- behavior is stable or worsening within a repetition;
- nested prefixes come from the same path;
- timing tails may violate the reserve, in which case the batch is rejected;
- calibration transfers only if every HCMS candidate is covered and every HCMS cell remains within replay budget;
- environments, identities, and state do not leak across methods;
- the scorer identity holds only under its enumerated conditions;
- no controlled result transfers to official targets.

No unstated assumption is needed to interpret the narrow controlled prediction.

### Fixed bias surface

1. **Selection:** Post-hoc failed antecedent and authored mocks are explicitly disclosed; inference is restricted to the fresh controlled grid.
2. **Confounding:** Position and first-order predecessor are balanced; scheduler, thermal, higher-order, and secular effects remain disclosed.
3. **Assignment:** The fixed Williams schedule is acknowledged as non-random and conditions the inference.
4. **Protocol deviation:** Hash, runner-interface, clock, profile, order, ledger, and count deviations invalidate the bundle.
5. **Missing data:** No available-case aggregation; any missing repetition invalidates the result.
6. **Measurement:** Wall-time noise, related-profile calibration, and attribution errors are explicitly addressed with actual replay, indexed traces, fixtures, and rejection.
7. **Analysis flexibility:** Methods, thresholds, profiles, masters, orders, endpoints, and failure bands are frozen.
8. **Selective reporting:** Complete, invalid, safety, and per-method artifacts must be retained together; efficacy cannot hide invalidity.

### Taxonomy

The classification is accurate:

- Opportunity: **Resource Bottleneck**
- Primary paradigm: **Optimization/Search**
- Secondary paradigm: Artifact/System
- Dominant operation: **replace**

This is a local replacement of the failed adaptive selector with a simpler monotone ceiling policy, not Bridge × Synthesis.

### Engineering anti-stacking

All three tests pass.

1. **Measured bottleneck per component**

   - HCMS policy: 24-favoring `6/9`, cliff cells `3/9`, and matched retrospective raw `17,446` versus `12,090` and `10,036`.
   - Replay accounting: scalar misses `84/90`, scalar system overages `7/9`, calibrated overages `0/9`, and held-out coverage `54/54`.

2. **Exact removals**

   - Fixed-8 and fixed-24/no-salvage remove the two load-bearing faces of the integrated HCMS policy.
   - `hcms_scalar` is a full endogenous controller removal differing only in its replay ledger.

3. **End-to-end claim**

   - The claim is constrained aggregate raw plus replay feasibility and correctness under frozen generation, replay, identity, candidate, and timing limits—not novelty from combining modules.

### Occam’s razor

The failed MPC selector has been removed. HCMS corresponds to the simplest surviving ceiling-24 monotone-salvage policy from the adverse audit. It must exceed both simpler removals by at least 10%; otherwise the best simple policy wins. This is a genuine precommitted complexity penalty.

### Alternative explanations and strongest objection

The strongest objection is that the authored primary grid nearly encodes the desired story: steady/reset profiles reward ceiling 24, while the cliff profile rewards salvage. This objection would defeat any claim of competition improvement, population generalization, or target-agent efficacy.

It does not defeat the claim actually written, because the hypothesis is explicitly restricted to the one fresh controlled mechanism grid, acknowledges the authored design, withholds official-score inference, and requires a later separately frozen target-confidence bridge. Confirmation would establish controlled mechanism integration and resource feasibility only.

Higher-order scheduler effects remain another plausible explanation, but the design balances position and every first-order predecessor, rejects timing invalidity, and makes no broader stochastic or causal-population claim.

### Required fixes

None before entering Phase 3.

### Overall: RIGOROUS

## 2. Actionable Coaching

These are implementation safeguards, not hypothesis-gate defects:

1. Make timer boundaries explicit in the Phase-3 runner and code review. Preserve the antecedent calibration convention exactly—especially whether fresh replay-environment construction and reset are included.
2. Assert from emitted artifacts that safety rows cannot enter primary aggregates, rather than relying only on namespace naming.
3. Verify the runner has one kernel function with policy data, and diff the effective non-ledger fields of HCMS versus scalar at runtime.
4. Report per-profile and per-method-cell results alongside the aggregate so a 10% pass cannot obscure mechanism reversal in one profile.
5. Keep any subsequent Kaggle or target-agent confidence bridge as a separately frozen hypothesis; this review authorizes no target-transfer inference.

---

## Gate consequence

- Review integrity passed against immutable commit `a8da04e`.
- Verdict: `RIGOROUS` with explicit scrutiny.
- Cycle-3 hypothesis-review usage remains `7/12`; charged at dispatch.
- Phase 2 passes for the narrow controlled hypothesis.
- Phase 3 may open only for the public non-target PoC in the reviewed scope.
- No target-transfer inference, attack mutation, Kaggle push or submission follows from this verdict.
