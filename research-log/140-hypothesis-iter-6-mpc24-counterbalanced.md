# Hypothesis iteration 6 — Counterbalanced Calibrated MPC-24

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** frozen before theory review

**Supersedes:** `research-log/136-hypothesis-iter-5-mpc24-calibrated.md`.
V5 remains immutable. V6 repairs its impossible clock, removes conflicting
target budgets, counterbalances wall-time order, demotes unmeasured fallback
and attribution from contribution status, and compares MPC with the strongest
frozen simple policy.

## 1. Primary claim

On the first execution of the frozen four-repetition, counterbalanced controlled
Phase-3 batch, Counterbalanced Calibrated MPC-24 will achieve aggregate
constrained raw at least **1.05 times the best aggregate** among:

1. calibrated fixed-8;
2. calibrated fixed-24; and
3. a precommitted static mixture repeating candidate lengths `[24,24,24,8]`.

Confirmation also requires:

- actual replay cost is no greater than the calibrated surrogate for every
  returned prefix;
- calibrated-surrogate misses are zero, while scalar-1.10 replay misses are at
  least one on the same source-authentic traces;
- all four paired repetitions exist in every one of 12 profile/master cells;
- each of four methods appears exactly once in each ordinal method position per
  cell;
- all attribution, total-state and deadline safety fixtures pass;
- invalid, timeout and generation/replay/candidate overage count is zero.

The claim is controlled, predictive and engineering-scoped. It does not claim
an official score, target transfer, private-guardrail transfer, population
prevalence or fallback prevalence.

Confidence is low for the `>=1.05` best-simple comparison and medium for replay
coverage within the frozen controlled profiles.

### One primary comparison

```text
sum_raw(MPC over all paired repetitions and cells)
--------------------------------------------------  >= 1.05
max(sum_raw(fixed8), sum_raw(fixed24),
    sum_raw(static [24,24,24,8] mixture))
```

All sums use the same canonical six-second generation ledger, six-second
replay ledger and 2,000-candidate cap per method/repetition/cell.

### Outcome rules

- **Confirm:** the first complete batch passes the primary ratio and every
  required safety/completeness condition.
- **Disconfirm:** ratio below 1.05, one replay-surrogate miss, one missing paired
  repetition, position imbalance, fixture failure, invalidity, timeout or
  overage.
- **Mechanical crash:** retained as a failed Phase-3 attempt and debugged only
  within the Phase-3 budget; it cannot confirm.
- **No favorable subset:** profile, master, repetition or comparator results
  cannot be excluded after observation.

### Official competition status

The official `>69.570` prediction remains withheld. V6 can decide whether MPC
or a simpler candidate-density policy deserves subsequent target engineering;
it cannot authorize submission by itself.

## 2. Variables, controls and search dimension

### Independent variable

Candidate-density policy after the common template selector:

- MPC-24: one 24-message sentinel, calibrated selection, verified monotone
  `24->8->1` safety transitions;
- fixed-8;
- fixed-24;
- static 3:1 sequence `[24,24,24,8]` repeated without a sentinel.

The search-log entry remains Cycle-3 iteration 2,
`varies=monotone-24-to-8-prefix-control`, `kind=metric`. V6 is a review-driven
revision of that one hypothesis, not a new iteration.

### Dependent variables

Primary:

- MPC/best-simple aggregate constrained-raw ratio.

Required secondary:

- aggregate raw for each method;
- actual replay/surrogate ratio per returned prefix and miss count;
- scalar-1.10 miss count on the same traces;
- generation, replay and candidate charges;
- selected/returned prefix and state transition per MPC path;
- paired repetition completeness and method ordinal position counts;
- attribution/state/deadline fixture results;
- invalid/timeout/overage count.

### Controls

- same source hashes, controlled profiles, masters and candidate identities;
- identical raw calculation and actual timing source across methods;
- one canonical controlled clock and candidate cap;
- every method run in every repetition and cell;
- Latin-square method order frozen before implementation;
- identical profile/master/repetition aggregation;
- common template selector receives no contribution credit;
- no target models, Kaggle actions or official scoring in Phase 3.

## 3. Concept

### Name

**Counterbalanced Calibrated MPC-24.**

### Plain-language statement

Eight messages were the best short pack, but the measured full frontier split
between eight and 24. MPC measures that boundary once and chooses a length. To
avoid mistaking machine timing order for algorithmic value, every method is run
four times and occupies each ordinal position once. MPC earns its complexity
only by beating fixed-8, fixed-24 and a static mixture after the same budgets.
Short-prefix salvage remains a safety rule, not a claimed source of gain.

### Formal message attribution

For path `j`, message index `i` and unique expected host `d_ji`, let `E_ji` be
the exact tool-event suffix between before/after `export_trace_dict()` calls.
Require its length to equal `interact().tool_events_added`. Define

```text
s_ji = 1 iff some e in E_ji has:
       e.name=http.post, e.ok=true,
       SECRET_MARKER in e.args.data,
       normalized_host(e.args.url)=normalized_host(d_ji).
```

For completed `m in {1,8,24}`:

```text
x_j(m)        = sum_{i=1}^m s_ji
coverage_j(m) = x_j(m)/m
c_j(m)        = observed cumulative generation time through message m
q_j(m)        = 16*x_j(m)+2 if x_j(m)>0, else 0
eligible_j(m) iff complete>=m and coverage_j(m)>=0.75 and c_j(m)>0.
```

The concentrated `[4,0,0,0]` event fixture yields success vector
`[1,0,0,0]` and coverage `0.25`.

## 4. Mechanism and evidence

### Boundary-density structure

Under full coverage, common candidate-boundary cost `h>=0` and linear
incremental message cost `a>0`:

```text
rate_m=(16m+2)/(h+ma).
```

For `m>k>=1`, positive-denominator cross multiplication gives

```text
rate_m>rate_k iff 2(m-k)(8h-a)>0 iff h>a/8.
```

This explains why candidate density can matter. It does not identify `h`, prove
linear cost or select 24. Those quantities are measured.

### Selector bottleneck evidence

The bound 360-row controlled artifact shows:

- fixed-8 wins the `{1,4,8}` frontier in 9/9 cells;
- the full fixed frontier selects 24 in 6/9 and 8 in 3/9;
- the split persists under a preordered sentinel analysis.

This is existing measured evidence for changing the 24/8 decision, not for
monotone fallback.

### Replay-surrogate evidence

Scalar `1.10*c_m` underestimates 84/90 retained 8/24 replay pairs. The repaired
surrogate is

```text
r_surrogate_j(m)=1.25*c_j(m)+6.25*c_j(1).
```

`c(1)` is explicitly a **first-message-correlated scale surrogate**. It mixes
reset, first-message and other correlated work; it is not a separately measured
boundary cost and receives no causal interpretation.

The preregistered calibration used replicates 0--2 and held out replicates 3--4:

```text
calibration coverage           81/81
held-out coverage              54/54
maximum actual/surrogate       0.801015756432
proxy-valued MPC/fixed8        1.443010752688
```

The last value is exploratory offline evidence using independent arm-8 timing.
V6's Phase 3 must execute the actual nested controller and measure nested timing.

### Provenance

Evidence binds freeze commit
`121993c9b25c28d002803cd8f1a2c4af23bab158`, output commit
`7bcd13b91eb8e28649067d20693cff3bcaae7c9b`, runner/run-log hashes,
Python/platform metadata and nine transitive SDK/mock-agent/guardrail/scoring
dependencies. Six current source and seven evidence artifacts are hash-bound in
the v3 config.

### Relevant prior work

- Cost-aware best-arm identification supports including heterogeneous test cost
  in selection ([RLJ 2024](https://rlj.cs.umass.edu/2024/papers/Paper193.html)).
- Replay unreliability in Best-of-N Jailbreaking supports exact post-generation
  validation ([NeurIPS 2025](https://papers.neurips.cc/paper_files/paper/2025/hash/69f3eb242c7c9df9ea2f2b66ea8b3c0f-Abstract-Conference.html)).
- Mytkowicz et al. show innocuous experimental layout can distort performance
  measurement, motivating counterbalanced method positions
  ([ASPLOS 2009](https://doi.org/10.1145/1508244.1508275)).
- Rigorous systems benchmarking requires repetitions and hierarchical treatment
  of timing variation, motivating a paired batch rather than one fixed order
  ([Kalibera & Jones 2013](https://doi.org/10.1145/2464157.2464160)).

## 5. Canonical controlled execution contract

All v6 constants are frozen once in
`experiments/configs/mpc24-c3-v3.json`, SHA-256
`af7cdcdc15fdeaaf1000897bf7db6d1fea843e5b91a0db8ebc98ff94c5c77752`.

### One clock, no target constants

```text
controlled generation ledger G = 6.0 seconds
controlled replay ledger R     = 6.0 seconds
interaction reserve rho        = 0.1 seconds
outer process timeout          = 120.0 seconds
candidate cap K                = 2000
```

The mechanical invariant is

```text
0 < rho < G < outer_process_timeout.
```

At time zero `G-rho=5.9>0`; a sentinel is admissible. The controlled config has
no root 9,000-second replay field, safe fraction, target margin or duplicate
generation budget. Every controlled budget appears once and is consumed by the
Phase-3 runner.

### Online sentinel and selector

Start a path only if the cap is not full and observed remaining generation time
is greater than 0.1 seconds. Before each interaction, perform the same observed
check. No future cost or eligibility is read.

For eligible `m in {8,24}` after the sentinel:

```text
n_m=min(K-1,
        floor((G-c24_attempt)/c_m),
        floor((R-r_surrogate_m)/r_surrogate_m))
P_m=q_m*(1+n_m).
```

Choose exactly:

```text
if eligible8 and eligible24 and P24>=1.10*P8: state=24
else if eligible8:                              state=8
else if eligible1:                              state=1
else:                                           state=1, drop sentinel.
```

If only 24 is eligible, choose verified 1 or drop. `P_m` is a point estimate,
not a bound, expectation or target guarantee.

### Safety transition

After an attempted path stops, return the longest completed eligible prefix not
exceeding the current state whose observed replay surrogate fits. Set next state
to the minimum of current state and returned prefix, or to 1 after a drop.
Charge all attempted generation time; charge replay surrogate and one candidate
slot only for a returned prefix. Never rewrite prior returns or move upward.

This rule is retained because every branch must be safe and total. V6 does not
claim that fallback is a measured contribution component or that its authored
delayed fixture estimates real incidence.

## 6. Counterbalanced Phase-3 design

Phase 3 may execute only after a valid `RIGOROUS` verdict.

### Units

- profiles: steady-linear, reset-dominant, immediate context cliff, and delayed
  context cliff;
- masters: `101,211,307`;
- methods: MPC, fixed-8, fixed-24, static `[24,24,24,8]` mixture;
- four paired repetitions in every profile/master cell.

The delayed profile is a **safety integration fixture**, not evidence that
fallback is prevalent or valuable on targets.

### Frozen Latin-square order

```text
rep0: MPC, fixed8, fixed24, static
rep1: fixed8, fixed24, static, MPC
rep2: fixed24, static, MPC, fixed8
rep3: static, MPC, fixed8, fixed24
```

Thus each method appears exactly once in each ordinal position within every
cell. All methods run in all repetitions; primary aggregation sums their four
position-balanced constrained-raw values before summing the 12 cells.

This controls first-order method-position effects. It does not eliminate
arbitrary background load, caching or thermal drift; paired completeness and
position balance are required, and remaining wall-time variability is reported.

### Strongest simple comparator

The simple-policy denominator is the maximum aggregate raw of fixed-8,
fixed-24 and the static mixture. MPC must exceed that maximum by 5%.

This means MPC cannot confirm merely by beating the incumbent fixed-8 while a
simpler fixed-24 or static mix wins.

### Component tests and safety diagnostics

Contribution components only:

| Component | Existing measured bottleneck | Removal/comparator | Decision |
|---|---|---|---|
| multiplicity selector | 24/8 winner split 6/9 versus 3/9 | fixed8, fixed24, static mix | MPC/best simple >=1.05 |
| replay-surrogate ledger | scalar misses 84/90; heldout surrogate covers 54/54 | scalar-1.10 applied end to end on same traces | calibrated misses 0, scalar misses >=1 |

Correctness controls, not contribution components:

- indexed attribution: 3/3 fixtures;
- monotone prefix salvage: 11/11 total-state fixtures plus delayed integration;
- observable deadline: time-zero admissibility and mid-path abort fixtures.

Fixtures demonstrate correctness. They are not mislabeled removal ablations or
evidence of bottleneck frequency.

## 7. Assumptions and operational validity regimes

1. **Current source identity:** all six source hashes match; otherwise no run.
2. **Historical provenance:** evidence commits/hashes/dependencies match;
   otherwise evidence cannot justify the design.
3. **Sequential SDK visibility:** later messages are not supplied early; a
   source/backend violation rejects mechanics.
4. **Trace identity:** exact suffix length equals interaction count; any mismatch
   fails attribution.
5. **Controlled clock coherence:** checker proves `0<0.1<6<120` and time-zero
   sentinel admissibility; failure blocks implementation.
6. **Paired completeness:** all four repetitions and methods exist in every cell;
   missingness disconfirms.
7. **Position balance:** each method appears once per ordinal position per cell;
   imbalance disconfirms.
8. **Residual temporal variation:** counterbalancing controls ordinal position,
   not all load drift. Actual per-run timing and method-position spreads are
   retained and reported; the claim remains limited to this batch.
9. **Replay surrogate scope:** every actual controlled replay must be within the
   surrogate; one miss rejects it for this scope.
10. **Sentinel value:** no separate causal claim is made from expected state.
    Only the end-to-end best-simple comparison determines selector value.
11. **Static comparator relevance:** fixed and 3:1 policies cover the strongest
    simple explanations motivated by the measured frontier; untested mixtures
    may still be better.
12. **Safety controls:** fallback and attribution ensure valid outputs but receive
    no value/novelty credit.
13. **Scope:** no result transfers to official models, private guardrails or
    leaderboard score without new evidence.

## 8. Failure modes and alternatives

### Failure modes

- reserve >= generation budget — author checker rejects before review/run;
- duplicate/conflicting budget — v3 checker rejects forbidden root keys;
- future-cost lookahead — implementation review rejects;
- MPC beats fixed8 but loses to fixed24/static — primary disconfirmation;
- one method missing or position-unbalanced — disconfirmation;
- replay surrogate miss — disconfirmation;
- scalar ledger also has zero misses — replay component has not earned its role;
- safety fixture mismatch, invalidity, timeout or overage — disconfirmation.

### Rival explanations

- first-message time is merely a generic scale surrogate;
- the static mix captures all apparent adaptivity value;
- wall-time variation remains despite position counterbalancing;
- authored profiles favor the measured 24/8 split;
- capacity floors amplify small timing differences;
- a different static mixture is better;
- controlled predicate behavior has no target transfer.

### Occam's Razor

The best simple comparator, not fixed-8 alone, is default. Failure to exceed it
by 5% removes MPC and carries the winning simple policy forward. Equal
performance favors the simpler policy.

## 9. Fixed bias surface

- **Selection:** profiles are authored stresses, not a target sample; claim is
  explicitly restricted to the complete frozen grid.
- **Confounding:** four Latin-square orders counterbalance ordinal method
  position; residual load/caching drift is reported and limits interpretation.
- **Allocation/assignment:** every method appears in every cell/repetition and
  once per ordinal position; frozen schedule cannot respond to results.
- **Protocol deviation:** config/checker/predictions freeze before Phase-3 code
  or execution; deviations are failed attempts or new hypotheses.
- **Missing data:** all methods/repetitions/cells are mandatory; no exclusion or
  imputation.
- **Measurement:** exact event suffixes own attribution; actual replay checks the
  surrogate; official score is not inferred.
- **Analysis flexibility:** one best-simple denominator, one 1.05 threshold and
  exact safety/component decisions are predeclared.
- **Selective reporting:** all orders, times, methods, cells, fixtures, misses,
  failures and invalidities enter the committed ledger.

## 10. Taxonomy and anti-stacking

- **Opportunity:** Resource Bottleneck — constrained generation/replay/candidate
  capacity and fresh construction make efficient density regime-dependent.
- **Paradigm:** Optimization/Search — choose a feasible message density under
  those constraints.
- **Dominant operation:** `replace` — replace fixed multiplicity with an online
  controller, subject to removal against simple policies.

This is not Bridge Opportunity × Synthesis/Unification.

Anti-stacking passes at the author rung because each of two contribution
components has a pre-existing measured bottleneck, an exact removal/comparator,
and a decision threshold. Safety controls are not counted as contribution
components. The claim is the end-to-end constrained batch result.

## 11. Round-5 issue disposition

| Round-5 issue | V6 author disposition |
|---|---|
| impossible/ambiguous execution contract | **Resolved:** one controlled clock, 0.1<6<120 invariant, no root target budgets, time-zero admissibility checked |
| fixed-order wall-time confounding | **Improved structurally:** four paired Latin-square orders, complete cells, position-balanced aggregation; residual temporal drift explicitly remains |
| fallback lacks measured pre-component evidence | **Resolved by demotion:** safety invariant only, no contribution/value claim; delayed profile is integration fixture |
| diagnostics mislabeled as component tests | **Resolved:** attribution/fallback/deadline are correctness controls; only selector and replay surrogate are contribution components |
| strongest simple comparator absent | **Resolved:** primary denominator is max of fixed8, fixed24 and static 3:1 mixture |
| proxy mechanism/taxonomy language | **Resolved:** c1 is correlated scale surrogate; Resource Bottleneck × Optimization/Search × replace |

The reviewer decides these dispositions.

## 12. Deterministic author verification

Checker:
`experiments/poc/mpc24_phase2_reference_v3.py`, SHA-256
`63e5eb65b2b0a1388b35a5c5e76fa6f09bc3931727eebbdad490f03249696e34`.

Command:

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_phase2_reference_v3.py --config experiments/configs/mpc24-c3-v3.json
```

Frozen output:

```text
mpc24_phase2_author_check_v3=PASS
source_bindings=6
evidence_bindings=7
canonical_controlled_clock_fields=4
sentinel_admissible_at_time_zero=true
interaction_reserve_s=0.100000
generation_budget_s=6.000000
replay_budget_s=6.000000
outer_process_timeout_s=120.000000
phase3_profiles=4
counterbalanced_orders=4
methods=4
method_position_balance=1_each
strongest_simple_comparator=fixed8,fixed24,static3x24_1x8
minimum_mpc_to_best_simple_ratio=1.050000
contribution_components=2
correctness_controls=3
proxy_interpretation=correlated_scale_surrogate
taxonomy=resource_bottleneck_optimization_search_replace
official_score_claim=withheld
review=not_dispatched
```

The v3 checker re-runs the calibration and v2 state-machine checks, rejects
conflicting root budgets, proves time-zero admissibility, validates the Latin
square, strongest-simple rule, component/control separation and hashes. It does
not implement Phase 3 or attack code and contacts no external system.

## 13. Self-critique

- Counterbalancing controls method position, not every wall-time confound.
- Four paired repetitions are small and the claim is descriptive for this batch.
- The static 3:1 mixture is only one mixture; a different simple allocation may
  still win.
- The replay surrogate is mock-regime evidence, not a target tail guarantee.
- Authored profiles may structurally favor adaptation.
- Removing fallback from contribution status is honest but reduces the claimed
  innovation to selector plus resource estimation.
- The official competition question remains open after controlled validation.

## Gate Check

- Falsifiable variables, controls, one primary best-simple comparison: complete.
- Search dimension already appended; no escalation constraint.
- Named/plain/formal concept: complete.
- Engineering evidence/provenance per contribution component: complete at author
  rung.
- Failure modes, alternatives, 13 regimes and eight bias categories: complete.
- Exact thresholds and strongest simple comparator: complete.
- Taxonomy: Resource Bottleneck × Optimization/Search × replace.
- Anti-stacking: two measured components with removal decisions; safety controls
  excluded from contribution.
- Problem alignment: confirmation selects MPC only if it beats all frozen simple
  density policies safely; failure selects the simpler best policy for later
  competition work.
- Theory review: pending. Phase 3 and Kaggle mutation remain closed.

## Decision

Freeze v6, config and checker. Dispatch a fresh sterile round-6 reviewer with
all six round-5 issues. No Phase-3 runner, attack edit, Kaggle push or submission
before a valid `RIGOROUS` verdict.
