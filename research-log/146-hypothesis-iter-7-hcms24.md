# Hypothesis iteration 7 — High-Ceiling Monotone Salvage-24

**Date:** 2026-07-22  
**Phase:** 2 — Hypothesis Formation  
**Cycle:** 3  
**Research iteration:** 3/5  
**Claim type:** predictive empirical/systems engineering  
**Question type:** predictive  
**Status:** immutable candidate for independent theory review

## 1. Prediction first

On the first exact fresh controlled Phase-3 batch specified here,
`hcms_calibrated` will:

1. achieve aggregate constrained raw at least `1.10` times the larger aggregate
   of `fixed8_calibrated` and `fixed24_no_salvage_calibrated` across the 36
   primary repetitions per method;
2. cover every returned candidate's actual replay cost with its calibrated
   surrogate and have zero method-cell actual-replay overages;
3. have zero generation overages, invalid attributions, duplicate identities,
   timeouts, incomplete paired repetitions or malformed artifacts; and
4. pass one separate delayed-cliff safety fixture whose raw is excluded from
   every efficacy aggregate.

The end-to-end `hcms_scalar` removal will have at least one method-cell whose
aggregate actual replay exceeds the frozen two-second replay budget.

The four paired method orders will put every method once in every ordinal
position and every directed predecessor pair exactly once.

Confidence is **medium** for the HCMS/simple-policy ratio, **high within the
controlled mock domain** for calibrated replay coverage, and **medium** for at
least one scalar overage. Failure of any item rejects the joint two-component
claim; there is no partial confirmation by averaging away an invalidity.

No official score, leaderboard improvement, private-guardrail transfer or
population effect is predicted.

## 2. Why v6 is retired rather than edited

Round 6 returned `NEEDS_REVISION`. The verbatim report is
`research-log/143-mpc24-theory-review-round-6.md`. The frozen adverse audit then
gave the selector its strongest symmetric simple comparator:

| Retrospective policy | Aggregate raw |
|---|---:|
| MPC with calibrated ledger | `17,446` |
| fixed ceiling 24 with identical salvage | `17,446` |
| fixed 8 with identical calibrated ledger | `12,090` |
| fixed 24 without salvage | `10,036` |

MPC and the symmetric ceiling returned the same first state in `9/9` cells;
selector incremental gain was exactly zero. The best of 106 primitive static
8/24 sequences was `[24]`. The preregistered decision therefore retired the
selector. HCMS is a new simpler direction, not v6 renamed.

The antecedent profile bundle is explicitly a failed artifact: its original
status is `FAIL` and only `6/9` frozen decisions passed. Its post-hoc reuse may
motivate and adversarially simplify a fresh hypothesis; it cannot confirm this
one.

## 3. Round-6 issue disposition

1. **Comparator implementation uniqueness — resolved by construction.** All
   methods call one shared kernel for clocks, interaction checks, indexed event
   attribution, identity allocation, charging, actual replay measurement,
   stopping, sequence truncation and artifact writing. Section 8 lists every
   allowed method-specific field.
2. **Delayed fallback contamination — resolved.** The delayed-cliff fixture is
   a separate safety suite and contributes no raw, candidate count, ratio or
   component estimate to the primary aggregate.
3. **Same-trace replay removal — resolved in the planned experiment.**
   `hcms_scalar` is a distinct end-to-end method. Its ledger controls its own
   returns and capacity; its own candidates are replayed. Same-trace miss counts
   remain antecedent diagnostics only.
4. **Unsupported 1.05 margin — replaced with a disclosed 1.10 engineering
   floor.** The smaller antecedent removal gain is `44.301%`; 10% preserves
   less than one quarter of that effect after domain shift and is the minimum
   gain required to pay for persistent state and calibrated accounting.
5. **Predecessor carryover — resolved at design level.** A four-treatment
   Williams schedule balances both position and all 12 directed predecessor
   pairs exactly once.
6. **Validity regimes — made explicit in Sections 12–13.** There is no
   sentinel-to-fill inference. Exact eligibility, timing-tail rejection,
   scorer identity, stationarity limits and replay validity are operational.
7. **Failed antecedent status — disclosed in Sections 2, 5 and 16.** It is
   post-hoc mechanism evidence, never fresh confirmation.

## 4. Frozen artifacts

- normative config: `experiments/configs/hcms24-c3-v1.json`, SHA-256
  `e71c8a6afb70459077a303652e21063a9c71f60d0650a502de8f63fbfb3c0e59`;
- deterministic author checker:
  `experiments/poc/hcms24_phase2_reference_v1.py`, SHA-256
  `039b9fe4ac827dbff30094870d9d850584d8aad43c18c9905940bd43272a75e4`;
- frozen selector/Occam audit:
  `experiments/poc/mpc24_symmetry_occam_audit.py`, SHA-256
  `1482abbf1693d9e146177ba547cccccdb5cfff6309e4794f0a558771c2d1c5c2`;
- audit result: `research-log/145-mpc24-symmetry-occam-audit-result.md`,
  SHA-256
  `6a2b3a50363eba2929d66b204942c1518bbd3d74a9858a93468c37e5ca5c92cd`.

The competition attack remains the committed incumbent from `f25fcd2`, SHA-256
`8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d`.
This hypothesis does not alter it.

The config binds six authoritative SDK sources and seven evidence artifacts.
The checker recomputes every bound hash and reruns both antecedent audits.

## 5. Evidence and the narrow inference it supports

### 5.1 Source mechanics

The bound gateway, environment, sandbox, predicate, scoring and cell sources
establish the legal multi-message range, per-message interaction path, trace
objects, host/cell identity, replay path and score implementation. Within the
frozen source identity, a returned finding with `m` messages, exactly one unique
qualifying host event per message and no other score term has raw

\[
q(m)=16m+2.
\]

If any identity, event-class, uniqueness or cap condition fails, the experiment
uses the actual scorer output and marks the identity check failed. The equation
is not extrapolated to other scoring regimes.

### 5.2 Failed antecedent profile

The retained 360-row artifact contains three profiles, three masters, five
replicates, four arms and generation/replay phases. Its full frontier favors 24
in six cells and 8 in three natural context-cliff cells. This heterogeneity is
real in the artifact, but it was discovered while the artifact disconfirmed its
original prediction. It is exploratory mechanism evidence only.

### 5.3 Replay calibration

Scalar `1.10*c_m` is below actual replay in `84/90` retained 8/24 pairs. The
engineering surrogate

\[
r(m)=1.25c_m+6.25c_1
\]

covers `81/81` calibration pairs and `54/54` held-out pairs. The maximum
held-out actual/surrogate ratio is `0.801015756432`. `c_1` is a correlated scale
surrogate, not separately identified reset or boundary cost.

### 5.4 Symmetric adverse audit

Under one retrospective kernel, HCMS equals MPC, beats fixed 8 by
`1.443010752688`, and beats no-salvage 24 by `1.738142686329`. Calibrated HCMS
has zero actual replay-overage cells while end-to-end retrospective scalar HCMS
has seven of nine. Because prefix data are independent-arm proxies and costs
are already observed, these are design priors, not Phase-3 effects.

## 6. Structural intuition, not proof of superiority

For a fully successful `m`-message candidate with common per-candidate reset
cost `h` and linear per-message cost `a`, raw rate is

\[
R_m=\frac{16m+2}{h+ma}.
\]

For `m>k`, positive denominators give

\[
(16m+2)(h+ka)-(16k+2)(h+ma)=2(m-k)(8h-a).
\]

Thus `R_m>R_k` iff `h>a/8` in this restricted full-coverage linear-cost model.
This explains why a high ceiling can amortize a candidate boundary. It neither
identifies `h`, proves 24 optimal, handles cliffs, nor establishes target
transfer. The empirical burden remains entirely on exact nested prefixes,
actual replay and the fresh end-to-end comparisons.

## 7. Operational objects

For method `u`, profile `z`, master `j`, paired order `r`, path `p` and message
index `i`:

- `E_uzjrpi` is the indexed trace suffix added by interaction `i`;
- `s_uzjrpi=1` iff that suffix contains exactly one qualifying event bound to
  the deterministic unique host for `(u,z,j,r,p,i)`;
- prefix `m` is exact iff `s_i=1` for every `i<=m`;
- `c_uzjrp(m)` is observed generation time spent attempting through message
  `m`, including failed or later-discarded interactions;
- `q_uzjrp(m)` is actual controlled scorer raw for the returned prefix;
- `r_hat_uzjrp(m)` is the method's replay ledger charge;
- `r_actual_uzjrp(m)` is measured by replaying that exact returned prefix in a
  fresh environment;
- `S_uzjrp` is the monotone ceiling before path `p`.

No aggregate event count can substitute for the vector `(s_1,...,s_m)`.

## 8. One shared kernel, four exact policies

The runner must implement one function with method configuration as data. Its
observable pseudocode is:

```text
state <- method.initial_state
while candidate slots remain:
    if observed_generation_remaining <= 0.1s: stop method-cell
    proposed <- method.proposal(state)
    start a fresh generation environment
    for i in 1..proposed:
        if observed_generation_remaining <= 0.1s: break path
        perform exactly one interaction
        charge observed elapsed generation time
        bind the indexed trace suffix to message i
    returned <- method.salvage(completed indexed prefixes)
    if no permitted exact prefix exists: drop; apply named transition
    else if method replay-ledger charge does not fit: drop; apply transition
    else:
        allocate deterministic unique identities
        return exactly that prefix
        charge one slot and method replay ledger
        apply named transition
after generation:
    replay every returned candidate in its own fresh environment
    record actual replay time, coverage, score and any total replay overage
```

Common behavior includes clocks, reserves, interaction loop, suffix
differencing, exact eligibility, identity allocation, candidate charge, actual
replay, stop semantics, truncation and artifact schema.

The only policy differences are:

| Method | Proposal/state | Permitted return | Ledger |
|---|---|---|---|
| `hcms_calibrated` | start 24; propose state; `state=min(state,return)`, drop→1 | longest exact of 24/8/1 | calibrated |
| `fixed8_calibrated` | start 8; propose min(8,state); same monotone transition | longest exact of 8/1 | calibrated |
| `fixed24_no_salvage_calibrated` | propose 24; remain 24 after drop | exact 24 or drop | calibrated |
| `hcms_scalar` | byte-identical HCMS proposal, salvage and transition | longest exact of 24/8/1 | scalar 1.10 |

The checker proves that `hcms_scalar` differs from HCMS only in its ledger.

## 9. Clock and replay semantics

Each method repetition receives:

- generation ledger `G=2.0s`;
- replay ledger `R=2.0s`;
- observed interaction reserve `rho=0.1s`;
- candidate cap `K=2000`;
- outer process timeout `120s`.

The enforced invariant is `0<rho<G<outer`. A path may start at time zero.
Admission never reads future time or eligibility. All attempted generation time
is charged, even if the path is dropped or salvaged shorter.

Replay ledger charge controls how many candidates the method returns. Actual
replay is subsequently measured for those endogenous candidates. A method-cell
overages if the sum of its actual replay costs exceeds `R`; replay is not
silently truncated to make the method look feasible.

The configured mock latencies have nominal single-interaction delays below
`rho`, but scheduler overhead is not bounded. Therefore zero generation
overage is a falsifiable empirical validity condition, not a theorem.

## 10. Fresh primary batch

Primary profiles:

1. `steady_linear_new`: compliant agent, `0.007s` latency;
2. `reset_dominant_new`: amortizing agent, `0.041s` fixed plus `0.0007s` per
   action;
3. `immediate_context_cliff_new`: exact behavior through message 8, then cliff,
   `0.0013s` latency.

Masters are `101`, `211`, and `307`, none used in the antecedent bundle.

Every profile/master cell runs four paired orders. Let
`A=hcms_calibrated`, `B=fixed8_calibrated`,
`C=fixed24_no_salvage_calibrated`, `D=hcms_scalar`. The Williams orders are:

```text
A B D C
B C A D
C D B A
D A C B
```

Every method occurs once at each position. The 12 transitions are exactly the
12 possible directed unequal predecessor pairs, each once. Each method thus
has `3 profiles × 3 masters × 4 orders = 36` primary repetitions.

Every method constructs fresh generation and replay environments. No method
inherits candidates, state, identities or ledger balances from its predecessor.
The order design controls first-order carryover; it does not prove absence of
higher-order scheduler or thermal effects.

## 11. Safety suite separated from efficacy

After the primary bundle is complete, one delayed-context fixture permits a
full 24 prefix on its first path and at most an exact 8 prefix later. HCMS must
transition `24→8` and never rise. This fixture tests state-machine integration.

Its raw, candidates, replay cost and timing are written under a distinct safety
namespace and are excluded mechanically from every primary sum and ratio. A
failure rejects correctness but a success supplies no efficacy contribution.

## 12. Component evidence and removals

| Component | Prior measured bottleneck | Exact removal | Fresh decision |
|---|---|---|---|
| high-ceiling monotone salvage | 24-favoring `6/9`, natural cliffs `3/9`; raw 17,446 vs fixed8 12,090 and no-salvage 10,036 | `fixed8_calibrated`; `fixed24_no_salvage_calibrated` | HCMS ≥1.10× best removal aggregate |
| calibrated replay accounting | scalar miss `84/90`; retrospective scalar overage `7/9`, calibrated `0/9`; held-out envelope `54/54` | full `hcms_scalar` method | calibrated coverage 1.0/overage 0; scalar overage ≥1 method-cell |

The two correctness controls—indexed attribution and observable deadline—have
fixtures but no contribution claim. The delayed fixture is also not a third
component.

The end-to-end claim is constrained raw under exact generation, replay,
candidate, identity and validity constraints. It is not novelty by counting
modules.

## 13. Validity domains and rejection conditions

1. **Source identity.** Bound SDK files and incumbent attack hash must match.
2. **Exact scorer identity.** `16m+2` applies only under all five config-listed
   event, identity, uniqueness, penalty and cap conditions.
3. **Nested observability.** Phase 3 must measure 8 as the actual first eight
   interactions of the same attempted 24 path; independent-arm substitution is
   forbidden.
4. **Monotone environment.** The primary profiles are stable or worsening
   within a method repetition. If a shorter return would later recover to a
   longer exact prefix, permanent downgrade may be conservative and the result
   does not generalize to that recovering regime.
5. **No cross-method memory.** Fresh environments and identities isolate
   method state; any leak invalidates the affected cell.
6. **Timing tail.** `rho` is not a hard OS bound. Any generation overage or
   outer timeout rejects the batch.
7. **Replay transfer.** Calibration is valid only if every HCMS actual replay
   is covered and aggregate actual replay stays within `R` in all 36 cells.
8. **Method symmetry.** Except for named policy/removal fields, the same kernel
   bytes and artifact schema must serve all methods.
9. **Freshness.** New masters/profiles must not be inspected through Phase-3
   output before the one committed run.
10. **Completeness.** All 144 primary method repetitions must exist, plus exact
    order/position/predecessor ledgers; partial bundles are invalid.
11. **No target transfer.** Controlled confirmation does not imply public or
    private leaderboard gain.
12. **No recovery inference.** The delayed safety fixture tests worsening only;
    it says nothing about nonmonotone recovery.

## 14. Quantitative rationale and failure bands

Antecedent ratios are `1.4430` versus fixed 8 and `1.7381` versus no-salvage.
They come from inspected independent-arm data, so the fresh expected effect is
not asserted to equal either. The 10% floor is an engineering materiality
criterion: it retains less than one quarter of the smaller relative gain while
requiring the added state/replay code to buy a visible improvement.

| Outcome | Decision |
|---|---|
| ratio ≥1.10, calibrated coverage/validity pass, scalar overage ≥1 | confirm narrow two-component controlled hypothesis; eligible for Phase 3→4 checkpoint only |
| ratio in `[1.00,1.10)` with validity pass | safe but insufficient; prefer the best simple policy, reject HCMS complexity |
| ratio <1.00 | refute HCMS value |
| calibrated miss/overage, invalidity, timeout, incomplete pairing | invalidate joint claim regardless of raw |
| scalar overage 0 | replay component not distinguished; reject joint two-component claim |

There is one exact execution. No tuning, threshold rewrite, profile replacement
or retry after seeing primary outputs is permitted.

## 15. Fixed eight-category bias surface

1. **Selection bias.** The motivating artifact and its 24/8 split are selected
   post hoc from a failed run. Fresh profile/master identifiers reduce reuse but
   remain authored mocks, not a population sample.
2. **Confounding.** Wall time, cache, scheduler and thermal state can affect
   discrete candidate counts. The Williams design balances position and
   first-order predecessor; higher-order and secular drift remain.
3. **Assignment bias.** Orders are fixed rather than randomly sampled. Exact
   balance aids auditability but conditions inference on this schedule.
4. **Protocol deviation.** A hash, method-interface, order, clock, profile,
   ledger or run-count deviation invalidates the bundle; it cannot be repaired
   in place.
5. **Missing data.** Any absent or malformed repetition makes the primary
   result invalid. No available-case aggregate is allowed.
6. **Measurement bias.** Wall time is noisy; replay surrogate is calibrated on
   related authored profiles; trace differencing can misattribute events. Exact
   indexed fixtures, actual replay and rejection rules expose but do not erase
   these risks.
7. **Analysis flexibility.** Methods, orders, profiles, masters, ratios,
   overage rules and failure bands are frozen before runner implementation and
   output. No alternate primary endpoint exists.
8. **Selective reporting.** COMPLETE, invalid, safety and per-method artifacts
   must be published together locally. Safety raw cannot be promoted, and a
   good ratio cannot hide scalar nondistinction or calibrated invalidity.

## 16. Taxonomy, Occam and alternatives

### Taxonomy

- opportunity: **Resource Bottleneck**;
- method paradigm: **Optimization/Search**, secondary Artifact/System;
- dominant operation: **replace**.

HCMS replaces adaptive selection with a local monotone ceiling policy. It is
not Bridge Opportunity × Synthesis/Unification, so that tripwire does not apply.

### Occam's razor

The v6 selector lost and is removed. HCMS must still beat both simpler adverse
policies. If it gains less than 10%, the best valid simple policy wins even if
HCMS is numerically higher. This is a precommitted complexity penalty.

### Alternative explanations

- authored fresh profiles still encode the known ceiling/cliff story;
- calibrated accounting may merely be more conservative and return fewer
  candidates without improving useful score;
- fixed 8 may dominate under the two-second budget despite four-second priors;
- no-salvage may look bad only because exact 24 is an intentionally strict
  removal;
- scheduler drift or higher-order carryover may affect capacity floors;
- `c_1` may work as generic scale correlation with no boundary mechanism;
- real target guardrails may recover, oscillate, fail before 8, or have replay
  tails outside the authored domain;
- official cells may reward a different attack template rather than allocation.

The strongest objection is that HCMS is almost definitionally rewarded by one
reset profile and one cliff profile. That objection is not defeated by this
design; it bounds the claim to this fresh controlled mechanism grid. Target
deployment requires a later, separately frozen confidence bridge.

## 17. Author verification

Exact command:

```bash
comp/.venv/bin/python -I experiments/poc/hcms24_phase2_reference_v1.py \
  --config experiments/configs/hcms24-c3-v1.json
```

Expected frozen output begins `hcms24_phase2_author_check_v1=PASS` and includes:

```text
antecedent_status=FAIL_disclosed
selector_status=retired_zero_value
shared_kernel_methods=4
exact_prefix_coverage=1.000000
contribution_components=2
primary_profiles=3
safety_profiles_excluded=1
williams_orders=4
directed_predecessor_pairs=12
position_balance=1_each
predecessor_balance=1_each
minimum_primary_ratio=1.100000
replay_removal=end_to_end_hcms_scalar
official_score_claim=withheld
attack_unchanged=true
```

## 18. Gate and next action

This artifact must be committed before review. A fresh sterile reviewer must
receive this full document, the canonical SciAgent mathematical/taxonomy
references, and all seven round-6 defects for disposition.

Only a scrutinized `RIGOROUS` verdict opens Phase 3. Until then:

- the Phase-3 runner and run directory must not exist;
- `experiments/attack.py` must not change;
- no Kaggle push, commit-run or submission may occur;
- no official result is inferred.

Cycle-3 hypothesis-review usage is `6/12` before dispatch and `7/12` when that
review is dispatched.
