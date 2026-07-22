# Calibrated MPC-24 theory review round 5

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** completed — needs revision

## Context and integrity

The reviewer evaluated immutable
`research-log/136-hypothesis-iter-5-mpc24-calibrated.md` at commit `c7f20ee`.
The round was charged before dispatch, bringing usage to `5/12`.

- Reviewer line count: `640`.
- `git show c7f20ee:research-log/136-hypothesis-iter-5-mpc24-calibrated.md | wc -l`
  returned `640`.
- `git show c7f20ee:research-log/136-hypothesis-iter-5-mpc24-calibrated.md | sha256sum`
  returned
  `ddd18c6c264e45c029c16e6649c1a86b0a225832168f560a01c624eefed11441`.
- `git diff --exit-code c7f20ee -- research-log/136-hypothesis-iter-5-mpc24-calibrated.md`
  exited zero with empty output.

## Reviewer report (verbatim)

**Status: DONE**

Reviewed `research-log/136-hypothesis-iter-5-mpc24-calibrated.md` in full. **Line count: 640**, matching `git show HEAD:research-log/136-hypothesis-iter-5-mpc24-calibrated.md | wc -l`.

## 1. Blind Assessment

### Previous-review issue disposition

| Prior issue | Disposition | Basis |
|---|---|---|
| 1. Repair replay-cost model and re-evaluate actual MPC with the exact online proxy | **IMPROVED** | The scalar model is replaced by `1.25*c_m + 6.25*c_1`, and the same proxy now drives selection and capacity (lines 221–251). The 1.443 ratio no longer uses oracle replay cost. However, it remains an offline, proxy-valued recomputation using independent-arm prefix timing, not an execution of the actual MPC controller; the artifact itself says `prefix8_timing_scope=independent_proxy_not_nested_measurement`. |
| 2. Make controller total and implementation-unique, including the 24-eligible/8-ineligible edge and observable admission | **IMPROVED** | The edge is explicitly total (lines 327–338), and sequential admission uses only observed time (lines 292–309). It is not resolved because the frozen Phase-3 budget makes that admission rule impossible, and the bound config contains conflicting replay-budget fields. |
| 3. Supply measured per-component evidence and frozen ablations with exact metrics and thresholds | **IMPROVED** | The table and five thresholds are now exact (lines 374–399). But monotone fallback has no prior measured bottleneck; its only support is a future profile intentionally authored to reward it. Attribution and no-ledger “ablations” are fixtures/projections rather than end-to-end component removals. |
| 4. Bind measurement provenance completely | **RESOLVED** | Lines 254–271 bind generating/output commits, runner, environment, evidence artifacts, SDK/source files, fixtures, guardrail, and mock-agent dependencies. The bound checker reran successfully, and both commits exist. |
| 5. Bridge or narrow the official-score prediction | **RESOLVED** | The official-score claim is explicitly withheld and the claim is narrowed to controlled validation (lines 31–33, 63–68). |
| 6. Operationalize sentinel/fill dependence, replay transfer, ledger safety, and drift | **IMPROVED** | Replay misses, ledger overages, missing cells, and selector states now have rejection rules (lines 448–478). However, “no unobservable temporal-drift assumption is needed” is false for a wall-time-dependent, fixed-order experiment, and matching an expected initial state does not by itself validate sentinel-to-fill predictiveness. |

### Justification Correctness

The boundary-density algebra is correct. With positive denominators,

\[
(16m+2)(h+ka)-(16k+2)(h+ma)
=2(m-k)(8h-a).
\]

For `m>k`, `h>=0`, and `a>0`, strict superiority is therefore equivalent to `h>a/8`; equality holds at `h=a/8`. The entry correctly limits this result to full coverage, common boundary cost, and linear incremental cost (lines 172–192), and correctly says it does not prove that MPC should choose 24.

The replay formula is an empirical engineering envelope, not a derivation. That is acceptable for this claim type, but its mechanistic interpretation is overstated. `c(1)` contains both boundary/reset work and first-message work, so `6.25*c(1)` does not identify a boundary cost. The held-out coverage supports a conservative correlated surrogate over those mock-agent regimes, not the asserted decomposition (lines 223–238).

The fatal correctness defect is the frozen timing contract:

- Before starting, MPC stops if `now >= generation_deadline - 90 s` (lines 294–309).
- Phase 3 freezes the generation budget at **6 seconds** (lines 429–433).

At the start, with six seconds remaining, `now >= deadline-90` is necessarily true. No sentinel can begin, so the 12 cell outcomes, initial-state predictions, transition claims, and aggregate ratio cannot be produced. The bound config confirms `max_next_interaction_reserve_s=90` and `phase3.generation_budget_s=6`; its author checker passes because it never asserts `reserve < phase3 generation budget`.

The config also contains both a root replay budget of `9000`, a `0.90` replay-safe fraction, and a Phase-3 replay budget of `6`, while Sections 6 and 8 do not uniquely state which values enter `R`. Thus the policy is either impossible under the stated Phase-3 deadline or not implementation-unique.

### Mathematical Depth & Validity Domains

The notation is mostly concrete:

- `s_ji` is one message’s correctly attributed success indicator.
- `x_j(m)` is successful-message count, not event count.
- `q_j(m)` is raw score for one returned prefix.
- `c_j(m)` is observed cumulative generation time.
- `P_hat_m` is a point estimate of total portfolio raw under repeated sentinel-like costs.

The entry appropriately denies that `P_hat` is a bound, expectation, or target guarantee (lines 339–341). The equations carry operational content and are not decorative mathiness.

The validity domain of the replay envelope is also honestly limited to the controlled mock-agent evidence. What is not valid is the stronger structural reading of `c(1)` as a separately measured boundary term.

The mathematical content does not establish controller superiority; the entry largely acknowledges this. The contribution is engineering composition, not a theoretical breakthrough.

### Logical Soundness

Several steps do not support their stated consequence:

1. **Execution contradiction:** the 90-second admission reserve prevents any Phase-3 path under a six-second generation budget.

2. **Sentinel-to-fill logic:** requiring the expected initial state in nine cells and an expected downgrade in three cells (lines 461–463) checks scripted behavior, not whether sentinel estimates predict later fill value. The end-to-end comparison helps, but the claimed dependence mechanism is not separately validated.

3. **Timing control:** the entry says frozen source/profile identity removes temporal drift (lines 480–482). It does not. Wall time can change with order, caching, scheduler load, thermal state, and background activity. Since capacity contains floor operations, small timing differences can cause discrete candidate-count changes. The fixed method order (lines 114–115) can therefore be a method-order confound.

4. **Designed-positive fallback test:** the delayed profile is explicitly authored so the sentinel permits 24 and later paths permit only 8 (lines 417–425). The no-fallback ablation must then drop later paths by definition. This is a useful integration fixture, but weak empirical evidence that fallback addresses a discovered engineering bottleneck.

### Assumption Completeness

Important assumptions are stated, but three load-bearing ones are absent or invalid:

- A coherent relation among deadline, generation ledger, and per-interaction reserve.
- Temporal exchangeability or controlled ordering of timing measurements across methods.
- Identification of `c(1)` as boundary work rather than a correlated mixture.

The scope boundary is otherwise commendably explicit: the result does not generalize to official models, private guardrails, or a population.

The fixed bias surface contains all eight required headings, so it passes the formal completeness check. Its confounding and measurement entries are substantively insufficient because “same run” and “same timing measurement” do not control fixed-order wall-time drift.

### Taxonomy Verification

The stated taxonomy at lines 540–551 is not quite accurate.

- **Method paradigm:** `Optimization/Search` is defensible.
- **Dominant operation:** `replace` is defensible because the controller replaces fixed-8.
- **Opportunity:** the dominant gap is **Resource Bottleneck**, not Puzzle/Contradiction. The motivating facts are replay/generation/candidate limits and regime-dependent efficient multiplicity. A split optimum is a tradeoff, not itself contradictory evidence.

This is not Bridge Opportunity × Synthesis/Unification under either classification, so the heightened local-move tripwire is not triggered. The misclassification does not appear to dodge that tripwire, but it should be corrected.

### Anti-Stacking Check

The engineering composition does not yet pass all three required tests.

1. **Measured bottleneck per component: FAIL.**

   - Selector: supported by measured 24/8 heterogeneity.
   - Replay ledger: supported by 84/90 scalar misses.
   - Monotone fallback: no pre-existing measured delayed-fill failure; its evidence is a future authored profile designed for the component.
   - Indexed attribution: supported only by a hand-constructed fixture, not a profile artifact showing an observed system bottleneck.

   Combining selector and monotone fallback in one table row hides that they are independently ablated components with different evidence requirements.

2. **Per-component ablation: PARTIAL.**

   Exact thresholds exist. However, aggregate attribution is guaranteed to misclassify its constructed fixture by definition, and no-ledger only “projects” an overage. These are diagnostics, not end-to-end removals under the primary protocol.

3. **End-to-end claim under a constraint: PASS.**

   The primary claim is the measured constrained system result, not novelty by component enumeration.

Because all three tests must pass, the anti-stacking gate fails.

### Occam’s Razor

The entry appropriately keeps fixed-8 as the default and precommits to rejecting MPC if the thresholds fail.

However, fixed-24 is listed as a comparator (lines 80 and 435) without any acceptance or rejection threshold. MPC can therefore “confirm” even if the simpler fixed-24 policy has higher aggregate constrained raw. A static 8/24 policy or simple fixed mixture is also not tested, despite being the obvious explanation for gains on a grid where nine of twelve cells are predicted to prefer 24.

The statement that MPC “earns complexity” by beating only fixed-8 (lines 514–518) is therefore too strong. It earns the narrower claim “better than fixed-8 on this grid,” not superiority over the strongest simple policy.

### Alternative Explanations

Several are correctly listed, especially authored-profile favoritism, budget sensitivity, lack of target transfer, and proxy overconservatism. Missing or insufficiently addressed alternatives are:

- Fixed method order or transient system load produced favorable capacity floors.
- A static fixed-24 or simple precommitted 8/24 policy explains the aggregate gain.
- `c(1)` works because it is a generic conservative scale surrogate, not because it measures boundary work.
- The fallback gain is a deterministic consequence of the authored delayed profile rather than evidence of an encountered bottleneck.

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. **Repair the impossible and ambiguous execution contract** — lines 282–309, 313–323, and 429–433. Define one canonical Phase-3 generation budget, replay budget, safe fraction, and deadline. Ensure the frozen reserve is strictly smaller than available controlled time, and add a checker invariant proving a sentinel is admissible at time zero.

2. **Control wall-time confounding** — lines 114–117, 469–482, and 506–512. Counterbalance or randomize method order with a frozen seed, use paired repetitions, or replace wall time with a deterministic injected cost for the controlled claim. “Same run” is not sufficient.

3. **Supply genuine pre-component measured evidence for fallback or remove/demote it** — lines 374–380, 388–409, and 417–425. A profile deliberately authored to reward fallback is an implementation fixture, not prior measurement of a bottleneck. Split selector and fallback into separate component rows.

4. **Turn diagnostic fixtures into honest component tests** — lines 386–399. Either execute attribution and ledger removals end-to-end on source-authentic traces or classify them as correctness invariants rather than empirical contribution components.

5. **Add a decision rule against the strongest simple comparator** — lines 20–25, 80–82, 388–399, and 514–518. At minimum, predeclare how fixed-24 results affect acceptance; preferably include a static 8/24 policy or fixed mixture.

6. **Correct mechanism and taxonomy language** — lines 223–238 and 540–551. Call `c(1)` a first-message-correlated boundary surrogate unless boundary time is separately measured, and classify the opportunity as Resource Bottleneck.

## 2. Actionable Coaching

- Separate the clocks explicitly: `D_global` for the external wall-clock deadline, `G_controlled` for the six-second experimental ledger, and `ρ` for a source-supported maximum interaction duration. Freeze an invariant such as `0 < ρ < G_controlled < D_global`, and test it mechanically.

- Make the “first execution” a preregistered batch containing paired repetitions. Counterbalance method order across masters and profiles. For timing methodology, useful references are Mytkowicz et al., *Producing Wrong Data Without Doing Anything Obviously Wrong* (ASPLOS 2009), and Kalibera & Jones, *Rigorous Benchmarking in Reasonable Time* (ISMM 2013).

- Rebuild the component table with one row each for selector, fallback, replay ledger, and attribution. Each row should name an artifact, measured incidence/magnitude, source commit, metric, removal, and decision threshold. If no pre-component fallback trace exists, remove fallback from the contribution claim and retain delayed fallback only as a safety fixture.

- Add calibrated fixed-8, calibrated fixed-24, and a frozen static 8/24 policy. Require MPC to beat the best simple admissible policy, or narrow the claim explicitly to comparison with the incumbent fixed-8 only.

- If boundary interpretation matters, measure reset/construction separately—e.g., replay construction with zero messages, then incremental 1/8/24-message work. Otherwise preserve the empirical envelope but drop causal language about what `6.25*c(1)` “represents.”

- Extend the author checker to reject inconsistent budgets, assert sentinel admissibility at time zero under the exact Phase-3 constants, verify every configured budget field is consumed exactly once, and reject unused root-level target constants in a controlled-only config.

## Gate Check

- Review integrity: PASS — `640/640`, matching SHA and immutable target.
- Verdict: **NEEDS_REVISION**.
- Review budget: `5/12` spent.
- Phase-2 gate remains closed.
- Phase 3, attack implementation and Kaggle mutation remain closed.

## Problem alignment

Rejecting an impossible six-second/90-second contract and fixed-order timing
comparison prevents a formally complete but non-executable PoC from consuming
engineering time or being mistaken for competition evidence.

## Decision

Accept the verdict. Preserve v5 immutably. V6 must use one canonical controlled
budget, counterbalanced paired timing, demote fallback/attribution to safety
controls unless prior measurements exist, compare against fixed-24 and a frozen
static mixture, and correct the proxy/taxonomy language before re-review.
