# Hypothesis iteration 8 v5 — Bracket-aligned Absorbing HCMS-24

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** authoring, not independently reviewed

**Supersedes:** `research-log/174-hypothesis-iter-8-ahcms24-v4.md`.

**Frozen contract:** `experiments/configs/ahcms24-c3-v5.json`.

**Review state:** writing and author-checking v5 does not spend a review round. Review remains `11/12` until a later sterile dispatch.

## 1. Why v4 is superseded

Sterile round-11 review accepted the endpoint-aligned fixed8/fixed24 Occam rule, the positive-domain efficiency algebra, scorer reconstruction, matched-trace attribution, one-component removal, taxonomy, and fixed-sample/remote scope.

Two defects still closed Phase 2.

First, v4 called a monotonic-clock interval “work” while claiming that scheduler delay and controller work were excluded. A monotonic clock measures elapsed time between reads. Any sleep, garbage collection, preemption, scheduling delay, trace export, or controller snapshot serialization inside those reads is part of the value. V4 also ended its proposed generation timer after candidate assembly even though historical `path_cost_s` ends before exact-prefix extraction, and ended replay after scoring even though historical `actual_replay_s` ends before final trace export and scoring. The old seconds therefore did not support the new endpoint as written.

Second, v4 said `R_a=R_s=0` implied `R_r=0`. That is false: retry can obtain all positive raw after the absorbing trigger. The branch is scientifically disconfirming through the primary and retention rules, but the simple-control cross-product remains defined.

V5 changes no AHCMS mechanism, profile family, sampled-unit count, raw threshold, target claim, attack implementation, or Phase-3 execution state. It:

1. adopts the exact historical path/replay timer brackets;
2. renames the construct **projected captured elapsed**, includes all in-bracket scheduling and controller work, and excludes only code proven outside the reads;
3. recomputes the retrospective ratio from `path_cost_s` alone rather than whole-cell `generation_elapsed_s`;
4. adds a prospective half-tail elapsed-discount sensitivity guard;
5. makes the positive-retry/all-zero-AHCMS-and-simple branch explicit; and
6. narrows the Occam claim to two specified controls, acknowledging a reduced global path cap as unevaluated.

No fresh scientific outcome has been observed.

## 2. Hypothesis

### 2.1 One-sentence claim

On nine fresh, q-independent complete controlled potential traces, replacing HCMS retry-after-first-replay-no-fit with an absorbing transition will improve aggregate raw per projected captured generation-path elapsed by at least `1.10x` relative to otherwise identical retry HCMS, retain at least `99.5%` of positive retry raw, remain at least `1.10x` efficient after discounting half of every retry-only tail nanosecond while crediting all retry raw, produce zero projected generation and aggregate-replay elapsed-overage units, and pass the same constrained raw/elapsed endpoint against both specified simple absorbing controls.

This is a predictive fixed-sample controlled-systems claim. It is not a CPU-time, target-model, population, hard-deadline, Kaggle-score, or leaderboard claim.

### 2.2 Quantified expectations

- nominal AHCMS/retry efficiency ratio: predicted `1.25`, confirm at `>=1.10`;
- half-tail-discount AHCMS/retry efficiency ratio: predicted `1.12`, confirm at `>=1.10`;
- AHCMS/retry raw retention: predicted `0.998`, confirm at `>=0.995`;
- nominal retry-tail captured-elapsed fraction: predicted `>=0.20`, confirm at `>=0.10`;
- half-discounted retry-tail fraction: predicted `>=0.10`, confirm at `>=0.10`;
- AHCMS versus each specified feasible simple control: predicted efficiency ratio `>=1.20`, confirm at `>=1.10` plus no Pareto dominance; and
- AHCMS projected generation/aggregate-replay elapsed overage units: predicted and required exactly zero.

The floors are preregistered engineering choices informed by retrospective profiling. They are not theorem-derived. The historical trace is not fresh confirmation.

### 2.3 Primary comparison and mandatory sensitivity

Let `a` denote AHCMS and `r` otherwise identical retry HCMS. Let `R_m` be integer raw and `T_m` the aggregate projected captured generation-path elapsed in integer nanoseconds.

After validity and positive-retry-raw gates, the headline inequality is

```text
10 * R_a * T_r >= 11 * R_r * T_a.
```

Because `T_a,T_r>0`, this is exactly

```text
(R_a/T_a) / (R_r/T_r) >= 1.10.
```

Define the retry-only tail and its conservative half charge:

```text
T_tail   = T_r - T_a,
H        = floor(T_tail / 2),
T_r_half = T_a + H.
```

All quantities are integer nanoseconds. V5 additionally requires

```text
10 * R_a * T_r_half >= 11 * R_r * T_a.
```

All retry raw remains credited. The sensitivity therefore asks whether the claim survives even if half of every measured retry-only tail nanosecond is treated as scheduling/controller inflation rather than useful evidence of the mechanism.

Retention, nominal and discounted tail support, AHCMS feasibility, complete specified-simple projections, and the constrained Occam rule are mandatory guards on this one result. The nominal and sensitivity inequalities are nested views of the same effect, not two independent discoveries.

## 3. Named concept

### 3.1 Name

**Absorbing HCMS-24 (AHCMS-24).**

### 3.2 Plain language

HCMS proposes long candidates and salvages exact shorter prefixes. Once an otherwise valid candidate no longer fits the accumulated replay ledger, later path attempts spend captured elapsed after replay capacity has already saturated. AHCMS makes that first ledger no-fit absorbing: it returns the accepted prefix and never attempts a later path in that controlled unit. The HCMS policy, 24/8/1 prefix logic, point ledger, generation reserve, scorer, caps, timing brackets, and evidence format stay inherited and identical.

### 3.3 Formal transition

For trace unit `u`, path slots are `t=1,...,16`. Let `C_(t-1)` be cumulative inherited point replay charge before slot `t`, and let `c_t>0` be the charge of an otherwise exact eligible candidate. Define

```text
tau_u = min{t : C_(t-1) + c_t > 2.0 seconds},
```

with `tau_u=+infinity` if the set is empty.

- retry HCMS records `drop_ledger_no_fit` at `tau_u` and may select later slots under inherited limits;
- AHCMS records the identical drop and terminates after the `tau_u` path.

Thus AHCMS is an event-aligned prefix projection of retry HCMS on one complete stored potential trace. No fitted quantity, q-dependent threshold, timing observation, or post-outcome rule changes the transition.

## 4. Variables, controls and search dimension

### 4.1 Independent variable

One binary field only:

```text
after_first_replay_no_fit in {absorb, retry}.
```

### 4.2 Dependent variables

1. aggregate integer raw `R_m`;
2. per-unit and aggregate projected captured generation-path elapsed `T_m(u),T_m`;
3. per-unit projected accepted-candidate aggregate replay elapsed `L_m(u)`;
4. raw-per-generation-elapsed efficiency `E_m=R_m/T_m`;
5. post-trigger retry path count, captured elapsed, and marginal raw;
6. nominal and half-discounted retry-tail fractions;
7. generation and replay elapsed-overage counts `O_G(m),O_R(m)`;
8. feasibility and raw/elapsed Pareto relations versus each specified simple control; and
9. timeout, missing, duplicate, attribution, support, numeric-domain, timer-landmark, and publication-invalidity counts.

### 4.3 Controls

AHCMS and retry HCMS share byte-identical complete traces, HCMS transitions, 24/8/1 arms, point replay-charge formula, two-second point ledger, `0.1`-second pre-path reserve, 16-slot/candidate caps, scorer, cell identity, profile, master, capture/arm order, timer landmarks, budget, raw reconstruction, and publication rules. They differ only after first `drop_ledger_no_fit`.

### 4.4 `varies` and kind

The existing Cycle-3 search entry remains

```text
varies = complete-cell-resource-risk-admission-and-absorbing-stop
kind   = metric.
```

V5 repairs the measurement contract for the same active hypothesis. It does not spend another research iteration or interleave a competitor.

## 5. Source-audited engineering profile

### 5.1 Evidence identity

The old HCMS attempt is sealed and invalid for its original joint claim. It is used only as retrospective component profiling. `experiments/poc/ahcms24_round11_timer_audit.py` binds:

- historical runner SHA-256 `7b030c67a7f18c4bce77db67f7db757b817aede7cbaf75aa1195a09d42f6b1f6`;
- sealed `COMPLETE.json` SHA-256 `34e9dc0274e0828f325cb280b2f392a6e867fabf4315c0c962cf3746dc200b07`; and
- unchanged attack SHA-256 `8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d`.

It parses the runner AST and verifies timer-marker ordering. It never executes the scientific runner.

### 5.2 Exact-bracket recomputation

For primary HCMS only, the audit sums all 370 `path_cost_s` rows. It does not use `generation_elapsed_s`, because whole-cell elapsed also spans post-timer exact-prefix selection, candidate/path assembly, publication checkpoints, and inter-path controller work not present in the prospective sum.

The exact-bracket profile is:

```text
retry paths                                      370
retry captured generation-path elapsed           69.00197669875342412 s
post-first-no-fit retry-tail paths                146
retry-tail captured elapsed                       18.36650123470462862 s
absorbing projected captured elapsed              50.63547546404879550 s
absorbing raw / retry raw                         39240 / 39258
nominal raw-per-captured-elapsed ratio             1.362095216773
delete-largest-tail-interval ratio                 1.358645048025
half-tail-discount ratio                           1.180818355750
half-discounted tail fraction                      0.153517990418
```

The profile measures the named bottleneck at the same generation-path bracket used prospectively: 146 retry-only paths consume 18.37 captured seconds for one 18-raw recovery. It does not identify how much of any interval was CPU, simulated sleep, controller serialization, or scheduling.

Replay-envelope and atomic-gate variants still lack an exact same-trace removal and receive no component credit.

## 6. Mechanistic justification

The inherited point replay ledger is monotone. A no-fit at `tau_u` says the current otherwise-exact candidate cannot be accepted under remaining point budget. Later candidates can occasionally have lower charge and recover raw, but the historical recovery density is low. Absorption trades sparse recovery for deleting every later selected path.

Because AHCMS and retry share stored outcomes through the trigger,

```text
T_r = T_a + T_tail,
R_r = R_a + R_tail,
```

with nonnegative integer tail quantities. For `T_a>0,T_tail>0`,

```text
R_a/T_a > R_r/T_r
iff R_a*T_tail > R_tail*T_a
iff R_a/T_a > R_tail/T_tail.
```

This identity says exactly when suffix removal improves raw per captured elapsed. It neither proves the `1.10` floor nor removes scheduler noise. Fresh traces can disconfirm the magnitude.

If `T_tail=0`, both nominal and discounted tail-support rules fail and the joint claim is disconfirmed. No division by tail elapsed is used.

The half-tail stress replaces `T_tail` by `floor(T_tail/2)` while preserving `R_tail`. It is adversarial to AHCMS because it raises retry efficiency. Passing means the `1.10` claim does not depend on the first half of measured retry-only elapsed. Failing means the observed nominal advantage is too sensitive for confirmation.

## 7. q-independent matched-trace design

### 7.1 Freeze and sampling

One canonical attempt writes and fsyncs `SAMPLING.json` before capture:

1. three unique uniform-rejection masters for each of three frozen profiles;
2. one independent Fisher--Yates permutation of all nine units;
3. one independent Fisher--Yates permutation of arms `24,8,1` at each unit-path; and
4. hashes of code, config, predictions, timer contract, thresholds, and sampled identities.

No master, unit order, arm order, failure, duration, or trace may be redrawn after any outcome. A crash consumes the canonical attempt.

### 7.2 Complete potential trace

Each unit executes in a fresh spawned child with no evaluated method label. Every one of 16 slots captures fresh arms `24,8,1`; capture continues after first no-fit so retry's suffix exists before projection.

Every arm stores:

1. the exact timer-start and timer-end landmark identifiers;
2. positive generation captured-elapsed nanoseconds;
3. the subsequently derived exact flags and candidate-or-drop outcome; and
4. all raw reconstruction inputs.

Every exact eligible returned candidate additionally stores nonnegative replay captured-elapsed nanoseconds at the replay bracket and the subsequently derived scorer output, whether or not a method later accepts it.

Missing arm, missing eligible replay, child failure, timeout, malformed attribution, timer-landmark mismatch, or out-of-support state invalidates the entire attempt. No unit is dropped or imputed.

### 7.3 Offline projection

After capture, four deterministic methods walk the same table:

1. `ahcms_absorbing`;
2. `hcms_retry_removal`;
3. `fixed8_absorbing`; and
4. `fixed24_no_salvage_absorbing`.

For method `m`, prior projected generation elapsed before slot `t` is the sum of previously selected stored path intervals. The inherited reserve admits another path only when

```text
2_000_000_000 ns - prior selected elapsed > 100_000_000 ns.
```

An admitted path is noncancellable in projection and may end above two seconds, which becomes an overage observation. Projection cannot alter captured durations or outcomes.

There is no live evaluated-method predecessor, cache, thermal order, or scheduling contrast. All 36 projections publish even when a method is infeasible.

## 8. Exact timer endpoints

### 8.1 Measurement table

| Quantity | Start event | End event | Included in bracket | Excluded after/before bracket | Interpretation |
|---|---|---|---|---|---|
| `g_ns[u,t,a]` | immediately before `generation_environment_construction` checkpoint | monotonic-ns read after interaction loop and its final completed `generation_interaction_complete` checkpoint, before `indexed_exact_flags` | checkpoint canonical-JSON serialization, fresh environment construction, reset, in-loop trace exports, interactions, suffix/cumulative-cost updates, GC/sleep/preemption/scheduling between reads | pre-start host/message construction; exact flags, prefix selection, state transition, candidate/path assembly, publication checkpoints, artifact serialization/fsync | captured generation-path elapsed |
| `ell_ns[u,c]` | immediately before `replay_environment_construction` checkpoint | monotonic-ns read after interaction loop and its final completed `replay_interaction_complete` checkpoint, before final trace export | checkpoint canonical-JSON serialization, fresh environment construction, reset, in-loop trace exports, interactions, suffix updates, GC/sleep/preemption/scheduling between reads | final trace export, exact flags, replay-evaluation checkpoint, predicates, signature, scorer, publication, artifact serialization/fsync | captured candidate replay elapsed |

If an interaction loop completes zero interactions, the timer end remains immediately after that loop; “final completed checkpoint” is simply absent. The endpoint does not move.

### 8.2 Historical/prospective equivalence

The historical runner used `time.monotonic()` floating-point seconds. Prospective capture uses `time.monotonic_ns()` integer nanoseconds at the same landmarks. Both query the same monotonic elapsed-time construct; the change avoids float conversion in decisions.

Prospective `phase_state` is always enabled for captured arms, so the same in-flight checkpoint calls and canonical snapshot serialization are inside both brackets. Hash/AST checks fail closed if landmark ordering changes.

### 8.3 Honest interpretation

An elapsed clock cannot separate active CPU service from descheduling or sleep. Therefore:

- in-bracket scheduling/preemption is included, not excluded;
- in-bracket controller snapshot/trace work is included;
- post-bracket selection/scoring/publication is excluded only because source ordering proves it occurs later;
- sums across independently captured arms are projected sums, not a simultaneously observed method runtime; and
- no two-second controlled endpoint proves safety under a remote 9000-second phase.

## 9. Integer resource accounting

### 9.1 Raw scoring boundary

For each method-unit, raw is recomputed once over its complete accepted finding sequence using bound `score_attack_raw`: integer severity weights plus twice integer unique-cell count. The SDK float must be finite, nonnegative, and exactly integral. Store `R_m(u)` as an integer and define

```text
R_m = sum_u R_m(u).
```

Units are never merged into one scorer call. Candidate scores are never summed because the uniqueness term is set-based. Define tail raw only as

```text
R_tail = sum_u [R_r(u) - R_a(u)].
```

Do not separately score a tail sequence.

### 9.2 Projected generation captured elapsed

Let `P_m(u)` be the ordered selected slots through and including a triggering no-fit, excluding every path after absorption or another inherited terminal condition. Let `a_m(u,t)` be the stored arm selected at a slot. Define

```text
T_m(u) = sum_{t in P_m(u)} g_ns[u,t,a_m(u,t)],
T_m    = sum_u T_m(u),
O_G(m) = sum_u 1{T_m(u) > 2_000_000_000}.
```

Every selected `g_ns` must be a positive Python integer. Equality at exactly two billion nanoseconds passes. Only strict greater-than is an overage.

`T_m` is a projected sum of independently captured elapsed intervals. It is not actual method wall-clock or CPU work.

### 9.3 Projected aggregate replay captured elapsed

Let `A_m(u)` be the ordered multiset of exact eligible occurrences admitted by inherited point replay ledger. A no-fit occurrence and later unselected trace occurrences are excluded. Legal duplicate occurrences remain separate elapsed occurrences while raw identities remain set-aware.

Define

```text
L_m(u) = sum_{c in A_m(u)} ell_ns[u,c],
O_R(m) = sum_u 1{L_m(u) > 2_000_000_000}.
```

Every `ell_ns` is a nonnegative Python integer. The empty sum equals zero. Equality passes; strict greater-than is overage.

`L_m(u)` is not scorer-inclusive because the source-audited historical replay timer ended before scoring. It is not target replay wall-clock or a cancellation guarantee.

## 10. Scheduler/controller sensitivity

### 10.1 Threat model

The primary attribution removes retry paths, but those paths may receive disproportionate host descheduling or controller overhead. Nine fixed units do not average this threat away. Random arm/unit order reduces systematic order coupling but does not prove absence.

### 10.2 Prespecified bounded perturbation

For the primary pair, shared-prefix projection requires `T_r>=T_a`. Define

```text
T_tail   = T_r - T_a,
H        = T_tail // 2,
T_r_half = T_a + H.
```

The floor is conservative: when the tail has an odd nanosecond, less elapsed is credited to retry. All retry raw remains unchanged.

Require both

```text
10 * R_a * T_r_half >= 11 * R_r * T_a
10 * H >= T_r_half.
```

The second inequality is the `0.10` tail-support floor under the same discounted denominator.

### 10.3 Validity domain

Passing supports this statement only: the fixed-sample effect survives a perturbation treating 50% of all retry-only tail elapsed as measurement inflation. It does not survive arbitrary deletion by definition; if all tail elapsed were discarded, retry and AHCMS would have equal elapsed and retry weakly greater raw.

Greater-than-50% or systematic method-correlated scheduling/controller inflation remains a limitation and forbids a broad performance claim. This is an explicit error envelope, not an assertion that noise is absent.

## 11. Raw, efficiency, and total branch semantics

Every `R_m` is a nonnegative integer. Every `T_m` is a positive integer. Decision order is fixed:

1. validate sampling, hashes, timer landmarks, completeness, identities, integer domains, and four projections;
2. apply the `R_r=0` branch;
3. on `R_r>0`, evaluate nominal primary, sensitivity primary, retention, and tail predicates;
4. evaluate AHCMS feasibility; and
5. evaluate both specified simple controls.

### 11.1 Zero retry raw

If `R_r=0`, prefix scorer monotonicity requires `R_a=R_tail=0`. The completed valid result is **DISCONFIRM**. Report

```text
Delta_E = NA_zero_retry_raw
rho_raw = NA_zero_retry_raw
rho_tail = NA_zero_retry_raw.
```

This is not invalid measurement: it is valid evidence that the retained system has no useful raw.

### 11.2 Positive retry raw

Only when `R_r>0` may display

```text
Delta_E = (R_a*T_r)/(R_r*T_a),
rho_raw = R_a/R_r,
rho_tail = R_tail/R_r.
```

All decisions remain integer cross-products.

Exact per-unit prefix reconstruction requires `R_a(u)<=R_r(u)` and gives

```text
R_r = R_a + R_tail,
rho_raw = 1 - rho_tail.
```

`rho_tail` is a consistency identity, not independent confirmation.

### 11.3 `R_a=0,R_r>0`

If retry raw is positive but AHCMS raw is zero, then with positive elapsed

```text
10*R_a*T_r = 0 < 11*R_r*T_a,
```

and

```text
1000*R_a = 0 < 995*R_r.
```

The nominal primary, sensitivity primary, and retention predicates disconfirm. There is no denominator exception.

### 11.4 `R_a=0,R_s=0,R_r>0`

For a specified feasible simple control with zero raw, its efficiency cross-product is still defined:

```text
10*R_a*T_s >= 11*R_s*T_a
0 >= 0.
```

Whether its Pareto rule passes depends on elapsed strictness, but the joint hypothesis has already disconfirmed through the positive-retry primary and retention rules. The retired raw-only diagnostic is exactly

```text
rho_simple = NA_zero_simple_raw.
```

No statement implies `R_r=0`.

### 11.5 Retired simple raw ratio

`rho_simple=R_a/max_s R_s` has no decision role. If emitted for backward-readable diagnostics and maximum specified-simple raw is zero, use `NA_zero_simple_raw`, never infinity, one, or zero.

## 12. Endpoint-aligned specified Occam controls

The two specified simple controls are fixed8 absorption and fixed24/no-salvage absorption. They test two named simplifications; they are not component removals and do not exhaust all simpler policies.

Define

```text
F_m = [O_G(m)=0 and O_R(m)=0].
```

Every simple projection must be complete and published. A complete simple with `F_s=false` is observed infeasible, not missing; it cannot dominate feasible AHCMS under the constrained endpoint.

For each feasible specified simple `s`, require

```text
10 * R_a * T_s >= 11 * R_s * T_a.
```

This is `E_a>=1.10 E_s` without a raw denominator. At `R_s=0`, it remains defined.

A feasible specified simple Pareto-dominates AHCMS iff

```text
R_s >= R_a and T_s <= T_a
and (R_s > R_a or T_s < T_a).
```

Confirmation requires no specified feasible simple dominance. This Pareto assertion is a consistency/interpretability guard rather than an independent effect where material efficiency already implies it.

A reduced global path cap is a plausible untested simpler alternative. Passing fixed8/fixed24 means only that these two policies do not explain away the result. V5 makes no global Occam-optimality or exhaustive-simplicity claim.

## 13. Confirmation, disconfirmation, invalidity

### 13.1 Confirm only if every predicate passes

1. nine traces and 36 method projections are complete and numerically valid;
2. all timer landmark/source identity checks pass;
3. `R_r>0`;
4. nominal primary: `10*R_a*T_r>=11*R_r*T_a`;
5. half-tail sensitivity primary: `10*R_a*T_r_half>=11*R_r*T_a`;
6. retention: `1000*R_a>=995*R_r`;
7. nominal tail support: `10*(T_r-T_a)>=T_r`;
8. discounted tail support: `10*H>=T_r_half`;
9. raw/elapsed prefix reconstruction passes;
10. AHCMS selects zero post-trigger paths;
11. `O_G(a)=O_R(a)=0`;
12. both specified simple controls are complete and each passes Section 12; and
13. timeout, duplicate, attribution, support, malformed, and publication-invalidity counts are zero.

### 13.2 Disconfirm

A complete valid attempt disconfirms if any confirmation predicate fails. Specifically: zero retry raw, zero AHCMS with positive retry raw, absent no-fit, submaterial nominal or sensitivity efficiency, excessive raw loss, weak nominal/discounted tail, any AHCMS overage, or a stronger specified feasible simple is a scientific negative.

### 13.3 Invalid

Sampling redraw, incomplete capture, timeout, child failure, non-integer/out-of-domain duration, source/landmark drift, out-of-support projection, identity/attribution error, missing method cell, contract/hash drift, or incomplete publication invalidates the joint attempt. Invalid is never relabeled disconfirm or confirm.

### 13.4 Inconclusive

Reserved only for external interruption before any complete canonical fixed sample exists. A completed attempt is confirm, disconfirm, or invalid.

## 14. Component and anti-stacking contract

AHCMS has one contribution component:

| Component | Exact-bracket profile | Role | Clean removal | Prospective predicate |
|---|---|---|---|---|
| absorbing no-fit | HCMS retry tail: 146 paths / 18.3665 captured s / 18 raw; exact-bracket nominal ratio 1.3621; half-tail ratio 1.1808 | stop future paths after first point-ledger saturation | otherwise identical retry HCMS | nominal+sensitivity efficiency `>=1.10`, retention `>=0.995`, nominal+discounted tail `>=0.10`, AHCMS feasible, specified simple rule |

The engineering tests are satisfied before implementation:

1. a source-audited exact-bracket profile measures path count, captured elapsed, and marginal raw at the component's failure surface;
2. the primary pair toggles only absorption on the same future complete traces; and
3. the claim is the constrained end-to-end fresh system result, not “we combined parts.”

Replay envelopes and atomic gates remain deleted from behavior, novelty, and component count. q-dependent fixtures may test software conformance but never efficacy. This is one local replacement.

## 15. Distinguishing prediction

A generic larger reserve or lower global path cap predicts fewer attempts by path count or slack regardless of event semantics. AHCMS predicts a discontinuity at one named event:

- before first replay-ledger no-fit, AHCMS and retry are identical;
- after it, AHCMS selects zero paths regardless of remaining projected elapsed;
- the removed suffix has sufficiently low raw density that both nominal and half-tail-discount efficiency exceed `1.10` while positive retry raw retention exceeds `0.995`.

Fixed8/fixed24 provide two specified policy-complexity stresses. A reduced global cap could make a different event-independent prediction and remains untested; V5 does not claim to defeat it.

## 16. Fixed eight-category bias surface

1. **Selection:** three profiles are purposeful and do not estimate target prevalence. Masters are drawn once with no outcome/timing-dependent replacement.
2. **Confounding:** all methods project the same complete arms; primary pair differs only after absorption. In-bracket scheduler/controller elapsed can still disproportionately affect the removed tail, so the half-tail guard bounds rather than denies this alternative.
3. **Allocation / assignment:** independent recorded Fisher--Yates unit and arm orders precede capture; every method receives every completed unit offline.
4. **Deviation from protocol:** code, hashes, endpoints, sensitivity, thresholds, and sampling freeze before capture. A crash consumes the attempt.
5. **Missing data:** missing arm, replay, duration, timer marker, or method cell invalidates the attempt. Infeasible controls remain reported.
6. **Measurement:** integer monotonic-ns differences measure captured elapsed at source-audited brackets, including in-bracket scheduling/controller work. Raw is per-unit set-aware recomputation. Neither is silently called CPU work or target latency.
7. **Analysis flexibility:** one primary pair, fixed nominal/sensitivity inequalities, fixed decision order, and two named simple controls exist before outcomes. No q fit, subgroup selection, bootstrap, timing trimming, rerun, or best-simple-by-raw choice is allowed.
8. **Selective reporting:** all sampled units, arms, durations, projections, zero branches, infeasible controls, sensitivity results, and invalid artifacts publish.

## 17. Assumptions and validity domains

1. **Potential consistency:** stored arms remain valid under offline projection only for frozen deterministic controlled profiles. No live target consistency is claimed.
2. **Complete support:** every required 24/8/1 arm and eligible replay exists at every slot; otherwise invalid.
3. **Timer equivalence:** historical and prospective clocks use the same start/end landmarks. `monotonic` versus `monotonic_ns` changes representation, not construct.
4. **Checkpoint equivalence:** prospective `phase_state` is enabled and invokes the same canonical snapshot serialization inside each bracket.
5. **Elapsed interpretation:** monotonic differences include all time between reads. They are not CPU time. Arbitrary systematic scheduling asymmetry is outside the claim.
6. **Bounded perturbation:** the confirmation claim is required to survive a 50% retry-tail elapsed discount. This floor is normative, not a probabilistic coverage theorem.
7. **Raw integrality/monotonicity:** bound SDK scoring on accepted per-unit sequences is integer and monotone under the AHCMS/retry prefix. Any `R_a(u)>R_r(u)` is invalid.
8. **Exact trigger:** only an otherwise exact eligible candidate exceeding inherited point ledger triggers absorption.
9. **Prefix attribution:** absorption changes only post-trigger selection, not pre-trigger elapsed, candidate, or raw.
10. **Constrained feasibility:** zero controlled elapsed overages is not remote deadline safety.
11. **Fixed-sample scope:** nine units describe one controlled realized grid, not a population or Kaggle effect.
12. **Specified-Occam scope:** fixed8/fixed24 eliminate only two simpler policies. Reduced global cap and other policies remain open.

Assumptions 1–9 are load-bearing for the local causal attribution. Assumptions 10–12 narrow the conclusion now; they are not deferred prose patches.

## 18. Alternative explanations and failure modes

1. **No saturation:** if no first no-fit occurs, the profiled bottleneck did not recur; disconfirm.
2. **Valuable recovery:** retry tail raw may defeat efficiency or retention; disconfirm.
3. **Scheduler/controller inflation:** nominal advantage may disappear under half-tail discount; disconfirm. Stronger asymmetry remains outside supported scope even if the guard passes.
4. **Specified simple adequacy:** fixed8/fixed24 may defeat materiality or dominate; disconfirm.
5. **Unspecified simple adequacy:** a lower global path cap could perform similarly; not tested, so no exhaustive simplicity claim.
6. **Profile construction:** controlled reset/cliff profiles can create the result; no wider prevalence claim.
7. **Replay mismatch:** inherited point admission can yield actual aggregate replay elapsed overage; any AHCMS overage disconfirms.
8. **Post-bracket overhead reversal:** exact-prefix selection, scorer, publication, or artifact I/O could reverse actual wall-clock ranking; those quantities are outside the endpoint.
9. **Target scaling reversal:** two-second controlled behavior may not matter under remote 9000-second phases; separate reviewed bridge required.

Implementation traps include: moving a timer read; disabling checkpoints; timing candidate assembly or scorer while claiming historical alignment; summing whole-cell and path elapsed; stopping trace capture at absorption; executing methods live; omitting replay for eligible later candidates; excluding trigger path; accepting no-fit candidate; using `>=` at overage; scoring units jointly; rounding half-tail upward; dropping delayed arms; retrying consumed attempt; or mutating attack before review/Phase-3/target gates.

## 19. Literature and source boundary

The mechanism does not rely on a conformal theorem. Retained primary sources delimit stronger risk claims:

- Romano, Patterson and Candès, *Conformalized Quantile Regression*, NeurIPS 2019, establishes marginal coverage under exchangeability, not cellwise hard safety: https://proceedings.neurips.cc/paper_files/paper/2019/file/5103c3584b063c431bd1268e9b5e76fb-Paper.pdf
- Angelopoulos et al., *Conformal Risk Control*, ICLR 2024, controls expected loss under exchangeability, not zero strict-deadline misses: https://proceedings.iclr.cc/paper_files/paper/2024/file/f3549ef9b5ff520a7e41ff3cc306ab2b-Paper-Conference.pdf
- Angelopoulos, Barber and Bates, *Online conformal prediction with decaying step sizes*, ICML 2024, gives retrospective sequence-average behavior, not next-run deadline certainty: https://proceedings.mlr.press/v235/angelopoulos24a.html
- Howard et al., *Time-uniform Chernoff bounds via nonnegative supermartingales*, 2020, requires a justified conditional process before stopping guarantees apply: https://doi.org/10.1214/18-PS321
- Shojaei, *Conformal Recovery-Deadline Certificates for Runtime Assurance of Adapting Controllers*, arXiv:2606.25371v1, separates statistical autonomy from verified backstop and is not proof here: https://arxiv.org/abs/2606.25371

Bound competition source establishes 9000-second generation/replay phases, cumulative replay, and noncancellable in-flight `RemoteEnv` calls. It does not turn a two-second captured-elapsed endpoint into remote safety.

## 20. Taxonomy

- opportunity pattern: **Resource Bottleneck**, secondarily Failure/Risk Gap;
- method paradigm: **Artifact/System**, secondarily Robustification; and
- dominant operation: **replace**.

AHCMS replaces retry-after-saturation with one absorbing transition. It is not Bridge Opportunity × Synthesis/Unification and adds no integrated stack.

## 21. Self-critique

### 21.1 Falsifiability

Every valid completed outcome maps deterministically. Zero retry raw, zero AHCMS with positive retry raw, sub-threshold nominal or sensitivity efficiency, excess raw loss, absent/weak tail, any AHCMS overage, or a stronger specified simple defeats confirmation.

### 21.2 Mathematical ownership

The efficiency identity follows by multiplying positive integer denominators. The zero branches are evaluated before display ratios. The sensitivity uses floor integer division and keeps retry raw, making it conservative. Re-derivation does not rely on a floating approximation.

### 21.3 Construct validity

V5 no longer calls the endpoint scheduler-free work. Every included/excluded region follows source order. The profile and prospective generation metric both sum the same `path_cost` bracket. Replay ends before scorer in both.

The largest remaining limitation is not hidden: a 50% discount is a bounded stress, not a stochastic noise guarantee. Actual CPU or target latency is unmeasured.

### 21.4 Occam and redundancy

Absorption is the sole contribution. Nominal and sensitivity views are nested, retention/tail raw are algebraically related, and Pareto is a consistency guard. Fixed8/fixed24 are specified controls only; reduced global cap remains open.

### 21.5 Problem alignment

Confirmation would establish that one source-compatible event-aligned stop preserves controlled portfolio value while materially reducing a precisely measured captured-elapsed endpoint under fixed resource constraints. That informs competition allocation, but cannot replace 9000-second scaling, Kaggle commit-run evidence, or the final submission-confidence gate.

## 22. Round-11 issue disposition encoded by v5

### 22.1 Boundary-consistent elapsed construct

- The construct is renamed captured elapsed, not work or CPU time.
- Generation and replay endpoints exactly match the pinned historical timer landmarks.
- In-bracket checkpoint serialization, trace/controller work, sleep, preemption, and scheduling are included.
- Post-bracket exact-prefix selection/candidate assembly and final replay scoring are excluded because historical timers excluded them.
- Historical ratio is recomputed solely from `path_cost_s`, never whole-cell `generation_elapsed_s`.
- A half-tail discount guard explicitly bounds one large class of tail-specific elapsed inflation.

### 22.2 Correct positive-retry zero-AHCMS/simple branch

At `R_a=R_s=0,R_r>0`, primary and retention inequalities disconfirm; the simple cross-product is the defined equality `0>=0`; Pareto remains elapsed-dependent; and retired raw-only diagnostic is `NA_zero_simple_raw`. No inference sets `R_r` to zero.

### 22.3 Reviewer coaching on simple alternatives

Fixed8/fixed24 are called specified controls rather than an exhaustive Occam set. A reduced global path cap is recorded as a plausible unevaluated alternative. No global simplicity claim is made.

## Gate Check

- Falsifiable variables, controls, and one primary comparison: **author PASS**.
- Named concept and formal absorbing transition: **author PASS**.
- Source-audited exact-bracket profile and one clean removal: **author PASS**.
- Exact elapsed/replay brackets, overage formulas, and scheduler interpretation: **author PASS**.
- Prespecified half-tail sensitivity with validity domain: **author PASS**.
- Endpoint-aligned specified-simple rule and all zero branches: **author PASS**.
- Failure modes, fixed bias surface, taxonomy, and anti-stacking: **author PASS**.
- Target/Kaggle bridge: **closed**.
- Independent theory review: **not dispatched; Phase 2 remains closed**.

## Decision

Freeze v5 for deterministic author verification. A passing checker proves internal contract consistency only. It does not clear Phase 2, admit Phase 3, authorize attack mutation, or establish Kaggle submission confidence.

## Next Steps

1. Run a deterministic v5 checker over source landmarks, exact-bracket profile, elapsed thresholds, half-tail arithmetic, zero branches, scorer boundaries, and specified-simple Pareto cases.
2. Bind config, checker, hypothesis, and audit identities in a verification log.
3. Only after lower-rung checks pass, open the final sterile theory review as a separate task and charge review `12/12` at dispatch.
