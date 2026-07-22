# Hypothesis iteration 8 v4 — Endpoint-total Absorbing HCMS-24

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** authoring, not independently reviewed

**Supersedes:** `research-log/171-hypothesis-iter-8-ahcms24-v3.md`.

**Frozen contract:** `experiments/configs/ahcms24-c3-v4.json`.

**Review state:** writing and author-checking v4 does not spend a review round.
Review remains `10/12` until a later sterile dispatch.

## 1. Why v3 is superseded

The round-10 reviewer accepted all four round-9 repairs: a genuine same-trace
absorption removal, one measured bottleneck and one contribution, the
absorbing-only Occam move, and the unique-strict-maximum tie correction.  It
also found the algebra, historical profile, matched-trace attribution,
taxonomy, scope and anti-stacking structure sound.

Three specification defects remained:

1. the raw-only simple-control ratio did not compare the headline
   raw-per-generation-work endpoint;
2. generation and replay overage cells lacked exact work formulas, clock
   boundaries and strict threshold semantics; and
3. the decision was undefined when retry or simple raw was zero.

V4 changes no mechanism, profile, sampled unit, threshold, target claim or
Phase-3 execution state.  It replaces the comparator and makes the measurement
and decision functions total before any fresh outcome exists.

## 2. Hypothesis

### 2.1 One-sentence claim

On nine fresh, q-independent complete controlled potential traces, replacing
HCMS retry-after-first-replay-no-fit with an absorbing transition will improve
aggregate raw per projected generation-work second by at least `1.10x`
relative to otherwise identical retry HCMS, retain at least `99.5%` of positive
retry raw, produce zero projected generation-work and aggregate-replay overage
cells, and pass the same constrained efficiency/Pareto endpoint against both
simple absorbing controls.

This is a predictive fixed-sample systems claim.  It is not a target-model,
population, hard-deadline, Kaggle-score or leaderboard claim.

### 2.2 Quantified expectations

- AHCMS/retry efficiency: predicted `1.25`, confirm at `>=1.10`;
- AHCMS/retry raw retention: predicted `0.998`, confirm at `>=0.995`;
- retry-tail generation-work fraction: predicted `>=0.20`, confirm at
  `>=0.10`;
- AHCMS versus each feasible simple control: predicted efficiency ratio
  `>=1.20`, confirm at `>=1.10` plus no simple Pareto dominance; and
- AHCMS projected generation-work and aggregate-replay overage cells: predicted
  and required exactly zero.

The effect sizes are preregistered engineering floors informed by retrospective
profiling.  They are not derived theorems and the retrospective run is not
fresh confirmation.

### 2.3 Primary comparison

Let `a` denote AHCMS and `r` otherwise identical retry HCMS.  After validity
and positive-retry-raw gates, the single headline comparison is

```text
R_a * W_r >= 1.10 * R_r * W_a.
```

Because all method work is required positive, this is exactly

```text
(R_a/W_a) / (R_r/W_r) >= 1.10.
```

Retention, retry-tail support, AHCMS feasibility, complete simple-control
projection and the constrained Occam rule are mandatory guards on this one
comparison, not alternative headline tests.

## 3. Named concept

### 3.1 Name

**Absorbing HCMS-24 (AHCMS-24).**

### 3.2 Plain language

HCMS proposes long candidates and salvages exact shorter prefixes.  Once an
otherwise valid candidate no longer fits the accumulated replay ledger, later
attempts spend generation work after replay capacity has already saturated.
AHCMS makes that first ledger no-fit absorbing: it returns the accepted prefix
and never attempts a later path in the same controlled unit.  The HCMS policy,
24/8/1 prefix logic, point ledger, generation reserve, scorer, caps and evidence
format remain inherited and identical.

### 3.3 Formal transition

For trace unit `u`, path slots are `t=1,...,16`.  Let `C_(t-1)` be cumulative
inherited point replay charge before slot `t`, and let `c_t>0` be the charge of
an otherwise exact eligible candidate.  Define

```text
tau_u = min{t : C_(t-1) + c_t > 2.0 seconds},
```

with `tau_u=+infinity` if the set is empty.

- retry HCMS records `drop_ledger_no_fit` at `tau_u` and may select later slots
  under the inherited limits;
- AHCMS records the identical drop and terminates after the `tau_u` path.

Thus AHCMS is an event-aligned prefix projection of retry HCMS on the same
complete stored potential trace.  No fitted quantity, q-dependent threshold or
post-outcome rule changes the transition.

## 4. Variables, controls and search dimension

### Independent variable

One binary field only:

```text
after_first_replay_no_fit in {absorb, retry}.
```

### Dependent variables

1. aggregate integer raw `R_m`;
2. projected generation work `G_m(u)` and `W_m`;
3. projected accepted-candidate aggregate replay work `Q_m(u)`;
4. raw-per-generation-work efficiency `E_m`;
5. post-trigger retry paths, work and recovered raw;
6. generation and aggregate-replay overage counts `O_G(m),O_R(m)`;
7. feasibility and raw/work Pareto relations versus each simple control; and
8. timeout, missing, duplicate, attribution, support, numeric-domain and
   publication-invalidity counts.

### Controls

AHCMS and retry HCMS share byte-identical complete traces, HCMS transitions,
24/8/1 arms, replay-charge formula, two-second point ledger, `0.1`-second
pre-path reserve, 16-slot and candidate caps, scorer, cell identity, profile,
master, arm and capture order, controlled budgets, work/raw reconstruction and
publication rules.  They differ only after the first `drop_ledger_no_fit`.

### `varies` and kind

The existing Cycle-3 search entry remains

```text
varies = complete-cell-resource-risk-admission-and-absorbing-stop
kind   = metric.
```

V4 repairs the contract for the same active hypothesis and does not add a new
research iteration or interleave a competing hypothesis.

## 5. Existing engineering profile

The prior HCMS attempt is sealed, complete and invalid for its original joint
claim.  It is used only as retrospective component profiling.  The read-only
round-9 audit verifies all bound hashes and reconstructs:

```text
absorption_same_trace_estimable=true
primary_post_no_fit_paths=415
primary_post_no_fit_seconds=59.181928537553
primary_later_recovery_candidates=3
primary_later_recovery_raw=54
hcms_post_no_fit_paths=146
hcms_post_no_fit_seconds=18.366501234705
hcms_absorption_raw_loss=18
hcms_raw_retention=39240/39258=0.999541494727
absorbing_efficiency_ratio_lower=1.355754716874
full_two_cubed_factorial_estimable_cells=0
```

The component therefore targets a measured tail: 415 paths and 59.18 seconds
for only three recovered candidates across the primary grid; HCMS itself spent
18.37 seconds after the trigger for one 18-raw candidate.  Only absorption has
an exact same-trace removal.  Replay-envelope and atomic-gate variants remain
unidentified and receive no component credit.

## 6. Mechanistic justification

The inherited point replay ledger is monotone.  A no-fit at `tau_u` signals
that the current otherwise-exact candidate cannot be accepted under the
remaining point budget.  Later candidates can occasionally have smaller charge
and recover raw, but the measured recovery density is low.  Absorption trades
that sparse recovery for deletion of every later selected path.

On the common trace, with integer raw and work,

```text
W_r = W_a + W_tail,
R_r = R_a + R_tail,
```

where both tail quantities are nonnegative.  For `W_a>0` and `W_tail>0`,

```text
R_a/W_a > R_r/W_r
iff R_a*W_tail > R_tail*W_a
iff R_a/W_a > R_tail/W_tail.
```

This identity says exactly when removal improves efficiency.  It does not
imply the `1.10` magnitude.  Fresh traces can disconfirm that empirical floor.

If `W_tail=0`, retry-tail support is zero and the joint hypothesis is
disconfirmed.  No division by `W_tail` is needed in the decision.

## 7. q-independent matched-trace design

### 7.1 Freeze and sampling

One canonical attempt writes and fsyncs `SAMPLING.json` before capture:

1. three unique uniform-rejection masters for each of three frozen profiles;
2. one independent Fisher--Yates permutation of all nine units;
3. one independent Fisher--Yates arm permutation at every unit-path; and
4. hashes of code, config, predictions, thresholds and sampled identities.

No master, order, failed unit or trace can be redrawn after an outcome.  A crash
consumes the canonical attempt.

### 7.2 Complete potential trace

Each unit executes in one fresh spawned child with no method label.  Every one
of 16 path slots captures fresh arms `24,8,1`; capture continues after the first
no-fit so retry's tail exists before projection.  Every arm records the exact
candidate-or-drop outcome and positive generation-work nanoseconds.  Every
exact eligible candidate records actual replay-work nanoseconds and scorer
output, whether or not a later method projection accepts it.

Missing arm, missing required replay, child failure, timeout, malformed
attribution or out-of-support state invalidates the entire attempt.  No unit is
dropped or imputed.

### 7.3 Offline projection

After capture ends, the four deterministic methods walk the same stored table:

1. `ahcms_absorbing`;
2. `hcms_retry_removal`;
3. `fixed8_absorbing`; and
4. `fixed24_no_salvage_absorbing`.

For method `m`, cumulative projected generation work before slot `t` is the sum
of its previously selected stored path durations.  The inherited point reserve
admits a next path only when `2.0 seconds - prior work > 0.1 seconds`.
Noncancellable selected work may finish above two seconds and is then counted
as an overage outcome.  Projection cannot alter a captured arm.

There is no live method predecessor, order, cache, scheduling or thermal
contrast.  All 36 method-unit projections must publish even when a method is
infeasible.

## 8. Exact resource accounting

### 8.1 Integer clock representation

Every duration is stored as an integer difference from `time.monotonic_ns()`.
Generation path durations must be positive.  Replay durations must be
nonnegative.  Negative, missing, non-integer or overflowed durations are
invalid evidence.  The two-second boundary is exactly `2_000_000_000` ns.

For each method-unit, raw is recomputed once over that unit's complete accepted
finding sequence using the bound `score_attack_raw`: integer severity weights
plus twice its integer unique-cell count.  The SDK float must be finite,
nonnegative and exactly integral; integer `R_m(u)` is stored and
`R_m=sum_u R_m(u)`.  Units are never merged into one scorer call.  Standalone
candidate scores are never summed because the unique-cell term is set-based.
Retry-tail raw is `sum_u[R_r(u)-R_a(u)]`.  All decision sums and cross products
are integer operations; floating ratios are display-only.

### 8.2 Projected generation work

For unit `u`, slot `t` and stored arm `a`, `g[u,t,a]` starts immediately before
constructing that arm's fresh controlled `RemoteEnv` and ends when the complete
return-ready candidate-or-drop object exists.  It includes environment
construction, reset, indexed interactions, exact-prefix extraction and
candidate assembly.  It excludes offline policy projection, controller
bookkeeping, artifact serialization/fsync, queueing and scheduler delay.

Let `P_m(u)` be the ordered slots selected through and including a triggering
no-fit path, excluding paths after absorption or another inherited terminal
condition.  Let `a_m(u,t)` be the stored arm selected at the slot.  Define

```text
G_m(u) = sum_{t in P_m(u)} g[u,t,a_m(u,t)],
W_m    = sum_u G_m(u),
O_G(m) = sum_u 1{G_m(u) > 2_000_000_000}.
```

Equality at exactly two seconds passes.  Only strict greater-than is an
overage.  `G_m(u)` and `W_m` are projected generation work, not live elapsed
wall-clock or target latency.

### 8.3 Projected aggregate replay work

Let `A_m(u)` be the ordered multiset of exact eligible candidate occurrences
admitted by the inherited point replay ledger.  The no-fit occurrence is not
accepted.  A duplicate occurrence, if legal and accepted, remains a separate
work occurrence; candidate identity/scoring rules still determine its raw.

For accepted occurrence `c`, `ell[u,c]` begins immediately before constructing
its fresh replay `RemoteEnv` and ends after final scorer completion.  It
includes replay construction, reset, interactions, guardrail and scoring work;
it excludes offline projection, artifact serialization/fsync, queueing and
scheduler delay.  Define

```text
Q_m(u) = sum_{c in A_m(u)} ell[u,c],
O_R(m) = sum_u 1{Q_m(u) > 2_000_000_000}.
```

The empty replay sum is zero.  Equality passes; strict greater-than is an
overage.  `Q_m(u)` sums actual captured candidate replay durations selected by
an offline method, so it is projected aggregate replay work—not method
wall-clock, target latency, cancellation or a hard remote deadline guarantee.

## 9. Raw, efficiency and total denominator rules

Let

```text
R_m(u) = score_attack_raw of method m's accepted finding sequence in unit u,
R_m = sum_u R_m(u),
E_m = R_m / W_m.
```

Every `R_m` must be finite and nonnegative; every `W_m` must be finite and
strictly positive.  A work-domain failure is invalid because the measurement
artifact cannot represent the specified endpoint.

Decision order is fixed:

1. validate sampling, completeness, identities, integer domains and all four
   projections;
2. if `R_r=0`, classify the complete valid attempt **DISCONFIRM** and report
   `Delta_E=rho_raw=rho_tail=NA_zero_retry_raw`;
3. only for `R_r>0`, compute the positive-domain primary and retention metrics;
4. apply tail, feasibility and simple-control predicates.

`R_r=0` is disconfirming rather than invalid: the trace can be perfectly valid,
but an all-zero retry system provides neither useful efficiency nor raw to
retain.  Because AHCMS is a prefix of retry, exact reconstruction also requires
`R_a=0` in this branch.

For `R_r>0`, define

```text
Delta_E = (R_a * W_r) / (R_r * W_a),
rho_raw = R_a / R_r,
R_tail  = R_r - R_a,
rho_tail = R_tail / R_r,
phi_tail = (W_r - W_a) / W_r.
```

Within every unit, AHCMS's accepted sequence is a prefix/subsequence of retry
under the same cell identities, so scorer monotonicity requires
`R_a(u)<=R_r(u)`.  Define `R_tail=sum_u[R_r(u)-R_a(u)]`; do not separately
rescore tail candidates because a cell already present before the trigger earns
no second uniqueness bonus.  Exact reconstruction gives
`R_r=R_a+R_tail` and `rho_raw=1-rho_tail`.  Likewise
`W_r=W_a+W_tail` with nonnegative work.  V4 retains `rho_tail` only as a
reconstruction consistency assertion, not a second independent piece of
confirmation evidence.

The v3 statistic `rho_simple=R_a/max_s R_s` is retired because it compared raw
while the headline concerns constrained efficiency/work.  It is never used in
v4.  If emitted only for backward-readable diagnostics and `max_s R_s=0`, its
value is the literal sentinel `NA_zero_simple_raw`, not infinity, one, or zero.

## 10. Endpoint-aligned Occam controls

The two simple controls remain fixed8 absorption and fixed24/no-salvage
absorption.  They test whether HCMS state and salvage complexity are needed;
they are not component removals.

Define controlled feasibility

```text
F_m = [O_G(m)=0 and O_R(m)=0].
```

Every simple projection must be complete and published.  A complete simple
control with `F_s=false` is an observed infeasible control, not missing data;
it cannot dominate a feasible AHCMS under the constrained endpoint.

For every feasible simple control `s`, require the exact integer inequality

```text
R_a * W_s >= 1.10 * R_s * W_a.
```

The checker represents `1.10` as the integer inequality

```text
10 * R_a * W_s >= 11 * R_s * W_a.
```

This is `E_a>=1.10 E_s` without a ratio denominator.  When `R_s=0` and
`R_a>0`, report `positive_over_zero`; the inequality passes and no undefined
ratio is formed.  If both are zero, the earlier `R_r=0` rule already
disconfirms the joint claim.

The raw/work Pareto definition is exact.  A feasible simple `s` dominates
AHCMS iff

```text
R_s >= R_a and W_s <= W_a
and (R_s > R_a or W_s < W_a).
```

Confirmation requires that no feasible simple dominates AHCMS.  This Pareto
guard is logically implied in ordinary positive cases by the `1.10` efficiency
margin, but is retained as a transparent consistency assertion, not a second
independent effect.

Thus the simple-control gate passes for each control exactly when it is either
complete but infeasible, or feasible and both the efficiency materiality and
non-domination predicates pass.  The comparison now uses the same raw/work,
efficiency and resource-constraint endpoint as the headline.

## 11. Confirmation, disconfirmation and invalidity

### Confirm only if every predicate passes

1. all nine traces and 36 method projections are complete and numerically
   valid;
2. `R_r>0`;
3. `10*R_a*W_r >= 11*R_r*W_a`;
4. `R_a/R_r >= 0.995`;
5. `(W_r-W_a)/W_r >= 0.10`;
6. exact raw/work prefix reconstruction and the retention identity pass;
7. AHCMS has zero post-trigger paths;
8. `O_G(a)=0` and `O_R(a)=0`;
9. both simple controls are complete and each passes the constrained rule in
   Section 10; and
10. timeout, duplicate-identity, attribution, support, malformed and
    publication-invalidity counts are zero.

Thresholds `0.995` and `0.10` are evaluated as integer cross products
`1000*R_a>=995*R_r` and `10*(W_r-W_a)>=W_r`.

### Disconfirm

A complete valid attempt disconfirms if retry raw is zero or any predicate
above fails.  In particular, absent no-fit support, sub-material efficiency,
excess raw loss, zero/weak retry tail, any AHCMS overage, a feasible simple
control with insufficient efficiency margin, or simple Pareto dominance is a
scientific negative—not inconclusive.

### Invalid

Sampling redraw, incomplete arm/replay capture, timeout, child failure,
non-integer or out-of-domain measurements, out-of-support projection, missing
method cell, identity/attribution error, contract/hash drift or incomplete
publication invalidates the joint attempt.  Invalidity cannot be relabeled as
disconfirmation or confirmation.

### Inconclusive

Reserved only for external interruption before any complete canonical fixed
sample exists.  A scientifically completed attempt has exactly one of confirm,
disconfirm or invalid.

## 12. Component and anti-stacking contract

AHCMS has exactly one contribution component:

| Component | Measured bottleneck | Role | Clean removal | Prospective predicate |
|---|---|---|---|---|
| absorbing no-fit | primary: 415 tail paths / 59.1819 s / 54 raw; HCMS: 146 / 18.3665 s / 18 raw | stop future work after first replay-ledger saturation | otherwise identical retry HCMS | primary efficiency `>=1.10`, retention `>=0.995`, tail work `>=0.10`, AHCMS feasible, constrained simple rule passes |

The three engineering tests are satisfied on paper:

1. the profile artifact measures the component's existing work/raw bottleneck;
2. the primary pair toggles only absorption on the same future complete traces;
3. the contribution claim is the constrained end-to-end system result.

Replay envelopes and atomic gates remain deleted from the behavior, novelty and
component count.  q-dependent fixtures may test software conformance but can
never establish efficacy or necessity.  This is one local replacement, not a
stack.

## 13. Distinguishing prediction

A generic larger reserve or replay multiplier predicts fewer paths whenever
slack is small.  AHCMS predicts a discontinuity at one named event:

- before the first replay-ledger no-fit, AHCMS and retry are identical;
- after it, AHCMS selects zero further paths irrespective of remaining work;
- the removed tail has sufficiently low yield that efficiency rises by at
  least `1.10x` while at least `99.5%` of positive retry raw remains.

The simple controls provide a separate Occam stress: if fixed8 or fixed24 is
feasible and matches the endpoint without HCMS complexity, the claim fails.

## 14. Fixed eight-category bias surface

1. **Selection:** three controlled profiles are purposeful and do not estimate
   target prevalence.  Masters are drawn once from the frozen domain with no
   outcome-dependent replacement.
2. **Confounding:** every method is projected from the same complete trace; the
   primary pair differs only at absorption.  Simple controls use the same work,
   raw and feasibility accounting.
3. **Allocation / assignment:** independent recorded Fisher--Yates orders cover
   units and arms; every method receives every unit after capture.
4. **Deviation from protocol:** code, contract, thresholds and sampling are
   bound before capture.  A crash consumes the attempt.
5. **Missing data:** missing arms, replay, durations or method cells invalidate
   the whole attempt; infeasible controls are retained as outcomes.
6. **Measurement:** integer monotonic-nanosecond boundaries and integer raw are
   reconstructed from stored rows; controller, serialization and queueing
   exclusions are named rather than silently treated as wall-clock.
7. **Analysis flexibility:** one primary cross product, exact ordered decision,
   fixed simple controls and integer thresholds exist before outcomes.  No q,
   fitted margin, subgroup, bootstrap or best-control-by-raw selection exists.
8. **Selective reporting:** all units, projections, zero-raw branches,
   infeasible controls, tail rows and invalid artifacts publish.

## 15. Assumptions and validity domains

1. **Potential consistency:** stored arm outcomes remain valid under offline
   projection only for the frozen deterministic controlled profiles; no live
   model consistency is claimed.
2. **Complete support:** every required 24/8/1 arm and eligible replay exists
   for all 16 slots; otherwise the attempt is invalid.
3. **Integer timing fidelity:** `monotonic_ns` differences measure the named
   controlled work boundaries.  They exclude and make no claim about scheduler
   delay, artifact I/O or target network time.
4. **Raw integrality and monotonicity:** the bound SDK source computes each
   unit's accepted-set raw from additive integer severity and a monotone
   unique-cell set.  Disagreement with any per-unit integer reconstruction or
   `R_a(u)>R_r(u)` is invalid.
5. **Exact trigger:** `drop_ledger_no_fit` is otherwise exact and eligible but
   exceeds the inherited point ledger; other failures cannot trigger AHCMS.
6. **Prefix attribution:** absorption changes only post-trigger selection and
   cannot change pre-trigger candidates, work or raw.
7. **Constrained comparison:** feasibility means zero projected controlled work
   overages, not hard remote safety.
8. **Fixed-sample scope:** nine units describe one realized controlled grid;
   they do not estimate a profile/master population or Kaggle effect.

Assumptions 1–6 are load-bearing for causal attribution of the local removal.
Assumptions 7–8 bound the conclusion rather than being deferred future work.

## 16. Alternative explanations and failure modes

1. **No fresh saturation:** no trigger means the profiled bottleneck did not
   recur; disconfirm.
2. **Valuable recovery:** retry tail raw may defeat retention or efficiency;
   disconfirm.
3. **Unnecessary HCMS:** a feasible fixed control may defeat materiality or
   dominate AHCMS; disconfirm.
4. **Profile artifact:** reset/cliff profiles may create the result; no wider
   prevalence claim is made.
5. **Work mismatch:** excluded controller/I/O/scheduler costs could reverse live
   elapsed performance; the claim says projected controlled work only.
6. **Point/actual replay mismatch:** inherited admission may still select a set
   whose actual replay sum exceeds the controlled bound; any AHCMS occurrence
   disconfirms.
7. **Target scaling reversal:** the 2-second controlled mechanism may not matter
   under 9000-second remote phases; a separate reviewed target bridge is
   mandatory.

Implementation traps include stopping capture at absorption, executing methods
live, omitting replay for eligible but later unaccepted candidates, excluding
the triggering path from work, counting the no-fit candidate as accepted,
using `>=` instead of `>` for overages, summing point charges instead of actual
replay durations, selecting a best simple by raw, converting nanoseconds to
float before decisions, retrying a consumed attempt, or mutating the attack
before the Phase-2/3 and target-confidence gates pass.

## 17. Literature and source boundary

The mechanism does not rely on a conformal theorem.  The retained primary
sources delimit stronger risk claims:

- Romano, Patterson and Candès, *Conformalized Quantile Regression*, NeurIPS
  2019, establishes marginal coverage under exchangeability, not cellwise hard
  safety: https://proceedings.neurips.cc/paper_files/paper/2019/file/5103c3584b063c431bd1268e9b5e76fb-Paper.pdf
- Angelopoulos et al., *Conformal Risk Control*, ICLR 2024, controls expected
  loss under exchangeability, not zero strict-deadline misses:
  https://proceedings.iclr.cc/paper_files/paper/2024/file/f3549ef9b5ff520a7e41ff3cc306ab2b-Paper-Conference.pdf
- Angelopoulos, Barber and Bates, *Online conformal prediction with decaying
  step sizes*, ICML 2024, provides retrospective average coverage behavior,
  not a next-run deadline certificate:
  https://proceedings.mlr.press/v235/angelopoulos24a.html
- Howard et al., *Time-uniform Chernoff bounds via nonnegative
  supermartingales*, 2020, requires a justified conditional process before its
  stopping guarantees apply: https://doi.org/10.1214/18-PS321
- Shojaei, *Conformal Recovery-Deadline Certificates for Runtime Assurance of
  Adapting Controllers*, arXiv:2606.25371v1, separates statistical autonomy
  from a verified backstop and is not used as proof here:
  https://arxiv.org/abs/2606.25371

Bound competition source establishes 9000-second generation/replay phases,
cumulative replay and noncancellable in-flight `RemoteEnv` operations.  It does
not turn the controlled two-second work endpoint into remote safety.

## 18. Taxonomy

- opportunity pattern: **Resource Bottleneck**, secondarily Failure/Risk Gap;
- method paradigm: **Artifact/System**, secondarily Robustification; and
- dominant operation: **replace**.

AHCMS replaces retry-after-saturation with one absorbing transition.  It is not
Bridge Opportunity × Synthesis/Unification and adds no integrated component
stack.

## 19. Self-critique

### Falsifiability

Every valid completed outcome is deterministically mapped.  Zero retry raw,
sub-threshold efficiency, excessive loss, absent tail, any AHCMS overage or a
stronger feasible simple control defeats confirmation.

### Mathematical ownership

The efficiency identity was re-derived from additive prefix work/raw.  Its
positive-domain assumptions and the `W_tail=0` branch are explicit.  All
decision inequalities use integers, and raw-denominator zeros are decisions
rather than accidental exceptions.

### Occam and redundancy

Absorption remains the sole contribution.  Simple controls now face the exact
constrained endpoint.  `rho_tail` and Pareto non-domination are consistency
guards, not extra independent evidence on top of algebraically stronger
predicates.

### Problem alignment

Confirmation would establish that one source-compatible event-aligned stop
preserves controlled portfolio value while materially reducing projected work
under exact resource constraints.  That is useful evidence for competition
allocation, but cannot substitute for the required 9000-second scaling design,
Kaggle commit run or submission-confidence gate.

## 20. Round-10 issue disposition encoded by v4

1. **Endpoint-aligned simple control:** raw-only `rho_simple` is retired.
   Every complete simple control is compared on feasibility, the same
   raw-per-generation-work materiality inequality, and exact raw/work Pareto
   dominance.
2. **Operational overages:** integer nanosecond clock boundaries, selected-path
   and accepted-candidate sets, per-unit formulas, excluded overheads, empty
   replay sum and strict `>2_000_000_000` boundaries are explicit.  The metrics
   are named projected work, never wall-clock or remote safety.
3. **Zero denominators:** `R_retry=0` is deterministic disconfirmation with
   three named sentinels; positive retry raw gates `Delta_E`, `rho_raw` and
   `rho_tail`; raw-only `rho_simple` is retired and has a diagnostic zero
   sentinel; simple efficiency uses a total integer cross product.

## Gate Check

- Falsifiable variables, controls and one primary comparison: **author PASS**.
- Named concept in plain language and formal transition: **author PASS**.
- Existing measured profile and one clean removal: **author PASS**.
- Exact work, overage and numeric domains: **author PASS**.
- Endpoint-aligned Occam rule and denominator totality: **author PASS**.
- Failure modes, fixed bias surface and taxonomy: **author PASS**.
- Anti-stacking: one component/one role/one removal/system result: **author
  PASS**.
- Target/Kaggle bridge: **closed**.
- Independent theory review: **not dispatched; Phase 2 remains closed**.

## Decision

Freeze v4 for deterministic author verification.  Passing that check only
establishes internal specification consistency; it does not clear Phase 2 or
admit Phase 3, attack mutation, Kaggle action or submission.

## Next Steps

1. Run a deterministic v4 author checker covering every metric boundary,
   Pareto/feasibility branch and zero-denominator outcome.
2. Bind exact config, checker and hypothesis identities in a verification log.
3. Open a later sterile round-11 re-review only after the lower verification
   rungs pass.
