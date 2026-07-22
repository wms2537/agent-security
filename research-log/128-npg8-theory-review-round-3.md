# NPG-8 theory review round 3

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 1 · **Status:** completed — needs revision

## Context

The reviewer evaluated immutable `research-log/125-hypothesis-iter-3-npg8.md`
from commit `51f8104` using the sterile SciAgent engineering/predictive review
contract and all six round-2 issues. The dispatch was charged before review,
bringing Cycle-3 hypothesis review usage to `3/12`.

## Review integrity

- Reviewer-reported line count: `674`.
- Orchestrator verification:
  `git show 51f8104:research-log/125-hypothesis-iter-3-npg8.md | wc -l`
  returned `674`.
- Orchestrator verification:
  `git show 51f8104:research-log/125-hypothesis-iter-3-npg8.md | sha256sum`
  returned
  `0346d0c472bb3d75ca812b44f7180f281c0fdf80a5490a708ee3ed530be54c29`.

## Reviewer report (verbatim)

**Status: DONE**

Reviewed the complete 674-line artifact at `research-log/125-hypothesis-iter-3-npg8.md`.

## 1. Blind assessment

### Previous-review disposition

| # | Disposition | Finding |
|---|---|---|
| 1 | **RESOLVED** | Lines 142–161 define interaction-scoped event slicing, exact-host matching, and the required `[4,0,0,0] → 0.25` behavior. The frozen fixtures reproduce it. |
| 2 | **IMPROVED** | The unsupported 73.050 chain is withdrawn and the active packed-policy comparator charges search, returned probes, fill, replay, and caps. However, nonactivation and first-fill fallback portfolios are not defined or charged end to end, and the quantities called lower/upper are not valid future bounds. |
| 3 | **RESOLVED** | Lines 374–391 make only the permitted conditional statement: if unmeasured boundary cost is common and nonnegative, `n_N≤n_B` prevents greater aggregate hidden boundary cost. Multiplicity-dependent and drifting costs are explicitly excluded. |
| 4 | **IMPROVED** | The config freezes budgets, profiles, masters, thresholds, and post-validation recomputation. The active stable path is accounted for, but provisional selection and fallback/guard paths remain incompletely specified and untested. |
| 5 | **RESOLVED** | Lines 41–56 and 526–539 correctly restrict the official result to prediction. Mechanism attribution belongs to controlled comparisons. |
| 6 | **RESOLVED** | `Puzzle/Contradiction × Optimization/Search × replace` matches the actual local intervention. |

### Justification correctness

The boundary-density algebra is correct within its stated domain:

\[
\frac{16m+2}{h+ma}>\frac{18}{h+a}
\]

is equivalent, for \(m>1\), to

\[
(16m+2)(h+a)-18(h+ma)
=2(m-1)(8h-a)>0,
\]

hence \(h>a/8\). This is genuine structural reasoning, not decorative mathematics. It explains why a candidate boundary can be worth amortizing while correctly withholding any target-level conclusion when coverage or cost is nonlinear.

I independently verified the retained controlled-SDK evidence:

- the 360-row sample and summary hashes match the recorded artifacts;
- fixed-8 exceeds fixed-1 in 9/9 cells;
- ratios are exactly 2.934027…–6.878306…;
- the best arm exceeds fixed-8 in 6/9 cells, up to 2.500404…;
- the claimed nested-screen savings range is reproducible.

The active-path arithmetic is also internally correct: `G_N` is post-validation, returned probes consume both replay capacity and candidate slots, and the fixed-1 counterfactual starts at `t_start`.

The load-bearing defect is that lines 282–295 do not define statistical or deterministic bounds. The minimum raw and maximum cost from two validation paths are merely observed extrema. Even under iid stationarity, a future observation falls below the minimum of two previous continuous observations with probability \(1/3\); over many fill candidates, the probability that all future observations remain inside those extrema approaches zero. “Within-run stationarity” does not convert extrema into bounds.

Consequently:

- `qL(m*)` is not a lower bound on future fill raw;
- `cU(m*)` is not an upper bound on future cost;
- `qU(1)` and `cL(1)` do not define an upper fixed-1 portfolio;
- `P_NPG_lower ≥ 1.10 P_FIXED1_upper` is not a conservative dominance test under the stated assumptions.

The first-fill guard checks only one future candidate. Lines 369–372 say later candidates are measured, but provide no raw/coverage regression rule after that first candidate. The actual packed portfolio may therefore fall below the claimed estimate after activation.

A second correctness defect is incomplete fallback accounting. Lines 275 and 348 select `m=1` after paying screen or validation cost, but do not define:

- which screen/validation prefixes are returned;
- whether prior packed prefixes are converted to `m=1`;
- the exact remaining generation, replay, and candidate budgets;
- the resulting fallback fill count and portfolio value.

The first-fill fallback at lines 357–367 is similarly underspecified for the five earlier probes. Therefore the claim at lines 22–24 that fallback rules are charged, and the disposition at line 591, are not yet true.

### Mathematical depth and validity domains

The \(h>a/8\) derivation has concrete meanings and an explicit validity regime. The notation for attribution, raw score, budgets, and candidate counts is generally well bound.

Two abstractions remain insufficiently unpacked:

1. Lines 267–275 say the provisional arm maximizes a “joint-cap lower total” without giving its exact formula. It is unclear how screen-probe raw, replay cost, generation remainder, and candidate count enter for each prospective arm.
2. The “lower” and “upper” labels imply order bounds that the stated stationarity assumption cannot support.

These are operational, not cosmetic, ambiguities: two conforming implementations could choose different arms.

### Logical soundness

The source-to-mechanism chain is sound through:

```text
fresh candidate construction
→ potentially amortizable boundary cost
→ packed candidates can improve constrained raw in a defined regime
→ target multiplicity should be measured
```

It does not support:

```text
two validation extrema
→ conservative bounds for hundreds of future fills
```

Nor does the current specification establish that falling back after search preserves the incumbent policy value. Those are the principal logical gaps.

The official claim itself remains properly falsifiable and predictive. Its low confidence and historical confounding are stated honestly.

### Assumption completeness

The twelve assumptions cover source identity, prefix ordering, observability, host attribution, target drift, private transfer, boundary-cost form, ledger continuity, comparator relevance, novelty, and independence across replay environments.

Missing or inadequate validity conditions are:

- a support bound, deterministic repeatability, or calibrated tolerance model that would justify extrapolating two extrema to the entire fill;
- generation-to-replay exchangeability for the public replay, not only public-to-private continuation transfer;
- the behavior required when any post-guard candidate violates `qL`, coverage, or the projected cost envelope;
- the exact fallback-portfolio contract after each possible failure stage.

Violating any of these can reverse the activation decision or erase the incumbent fallback.

### Taxonomy verification

**PASS.**

- Opportunity: Puzzle/Contradiction is defensible because the novelty reward conflicts with the cost of acquiring candidate boundaries.
- Method: Optimization/Search accurately describes target-conditioned multiplicity selection.
- Operation: `replace` accurately describes substituting one nested path for independent arm screens.

This is not Bridge Opportunity × Synthesis/Unification.

### Anti-stacking check

The core NPG contribution mostly passes:

- one measured bottleneck is identified;
- nested versus independent screening and NPG versus fixed-8 are planned;
- shared-prefix cost saving and exact `[4,0,0,0]` attribution are predictions a plain independent-arm stack does not make;
- the contribution is framed as constrained end-to-end policy value.

The complete component plan does not yet pass. Lines 403 and 413–415 promise a frozen first-fill stress condition and no-guard diagnostic, but the Phase-3 config contains no profile where screening and validation pass and the first fill subsequently regresses. It also lacks validation-failure, late-fill-regression, incomplete-path, and fallback-accounting cells.

### Occam’s Razor check

Fixed-8 is correctly identified as the strongest simpler alternative, and the frozen comparison charges search cost.

However, the three deterministic Phase-3 profiles are already algebraically constructed so that the author checker proves NPG selects the oracle arm. Re-running those tables validates implementation consistency, not whether adaptation is useful on the target. Fixed-8 remains a viable explanation for any official gain unless target-linked controlled evidence shows meaningful arm heterogeneity. The artifact correctly avoids a causal leaderboard claim, but its Occam gate is weaker than its prose suggests.

### Alternative explanations

The artifact appropriately lists drift, stochastic variation, fixed-8 sufficiency, template variation, private-row imbalance, extra predicates, and changed capacity.

Additional possibilities requiring explicit handling are:

- NPG never activates and the result is primarily incumbent behavior minus screen overhead;
- NPG activates because two validation extrema were favorable, followed by regression in later fills;
- fallback overhead, rather than multiplicity, determines the score;
- public replay differs from target generation even before considering the private guardrail.

### Overall

**NEEDS_REVISION**

Issues ordered by severity:

1. **Lines 22–24, 126–128, 282–295, 314–346, 369–372, and 482–484:** observed extrema from two paths are not conservative future bounds. Replace the bound language and decision rule with a validity-supported construction, or add a sequential rule that preserves the claimed portfolio dominance.
2. **Lines 275, 339–350, and 355–372:** define and charge every `m=1` fallback portfolio exactly, including which probe prefixes are returned, remaining budgets, fill count, and value.
3. **Lines 267–275:** specify the provisional joint-cap objective algebraically. The frozen checker and future implementation must compute that exact expression.
4. **Lines 403, 413–415, and 433–460:** add frozen profiles for validation rejection, first-fill regression, later regression, incomplete paths, and both fallback branches. The promised first-fill stress condition currently does not exist.
5. **Lines 220–228:** bind the real engineering evidence directly by artifact path, freeze commit, and sample/summary hashes. The numbers are reproducible, but the hypothesis itself does not identify their source.
6. **Lines 476–484:** distinguish trace differencing via `export_trace_dict()` from `interact()`’s returned event counts, and state the public generation-to-replay transfer assumption explicitly.

## 2. Actionable coaching

Use one of two honest gate formulations:

- **Deterministic-envelope formulation:** activate only in an explicitly bounded regime where every subsequent candidate must satisfy the validation envelope; on any violation, stop, convert eligible paths to `m=1`, and recompute the exact fallback portfolio.
- **Predictive-estimate formulation:** rename the extrema as plug-in estimates, remove “lower,” “upper,” and “conservative,” and use a calibrated tolerance or sequential risk budget. Two validation paths are inadequate for a high-confidence tail statement.

Freeze an exact fallback function such as:

```text
fallback(stage, completed_paths, current_time, replay_spent):
  convert each eligible completed path to its successful m=1 prefix
  charge its measured replay estimate and one candidate slot
  recompute G, R and K
  fill only with verified m=1 candidates
  emit exact returned count and projected total
```

Then compare that complete fallback portfolio with the original fixed-1 policy and explicitly accept or reject the search overhead.

Extend Phase 3 with branch-complete fixtures:

- screen selects 1;
- screen selects 8, validation rejects;
- validation accepts 8, first fill rejects;
- first fill accepts, later fill regresses;
- incomplete screen path;
- replay ledger becomes binding after returned probes;
- candidate cap binds;
- fixed-8 beats NPG after search cost.

Finally, treat the current deterministic profiles as implementation conformance tests. Competition-facing confidence should come from source-authentic or target-linked measurements, not from profiles whose expected oracle choices are already encoded in the frozen table.

## Gate Check

- Review integrity: **PASS** — 674 reviewer/committed lines and SHA-256 match.
- Theory-review verdict: **NEEDS_REVISION**.
- Cycle-3 hypothesis review: **3/12 spent**.
- Phase-2 gate: **FAIL / remains open**.
- Phase 3, attack implementation and Kaggle mutation remain closed.

## Problem alignment

Rejecting an extrema-as-bound activation rule prevents an apparently safe gate
from selecting a packed portfolio on evidence that fails with probability
increasing toward one as fill length grows. Exact fallback accounting also
protects the incumbent from hidden search overhead.

## Decision

Accept the adverse verdict. Preserve v3 immutably and replace it in v4. The
next design must remove unsupported bound semantics, define the provisional
objective and every fallback branch exactly, add branch-complete fixtures,
bind the 360-row evidence, and state the public generation-to-replay transfer
assumption before another review.
