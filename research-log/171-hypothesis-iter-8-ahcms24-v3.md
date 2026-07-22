# Hypothesis iteration 8 v3 — Absorbing HCMS-24

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** author-verified, not independently reviewed

**Supersedes:** `research-log/167-hypothesis-iter-8-prac24-v2.md`.

**Frozen contract:** `experiments/configs/ahcms24-c3-v3.json`.

**Review state:** writing and author-checking v3 does not spend a hypothesis
review round.  Review remains `9/12` until a future sterile dispatch.

## 1. Why v2 is superseded

The round-9 reviewer accepted v2's finite-population mathematics, role-blind
matched-trace design, inherited-HCMS demotion, and withdrawal of the
candidate-boundary claim.  It rejected the engineering contribution because
two of three claimed components had only q-dependent conformance fixtures, not
distinct held-out bottlenecks or same-trace ablations.  All four observed
generation overages were inside the futile tail already removed by absorption,
and aggregate HCMS replay overages were `0/36`.  A simpler explanation therefore
fit the evidence: inherited HCMS plus one absorbing no-fit transition.

The read-only audit in report 170 tested whether the sealed trace supports the
requested `2^3` retrospective factorial.  It does not.  Complete estimable
factorial cells are zero: replay-envelope variants were separate live captures,
426 ledger-dropped paths lack replay potential outcomes, and no atomic-gate
removal was captured.  Only absorption is an exact same-trace truncation.

The scientifically valid response is to remove unsupported components, not to
fill missing factorial cells.  V3 claims exactly one new component.

## 2. Hypothesis

### 2.1 One-sentence claim

On nine fresh, q-independent, complete controlled potential traces, replacing
HCMS retry-after-first-replay-no-fit with an absorbing transition will improve
aggregate raw per generation-work second by at least `1.10x` relative to
otherwise identical retry HCMS, while retaining at least `99.5%` of retry raw
and producing zero controlled generation or aggregate-replay overage cells.

This is a predictive fixed-sample systems claim.  It is not a claim about target
models, the Kaggle leaderboard, population-average performance, or hard remote
deadline safety.

### 2.2 Quantified expectation

- primary efficiency-ratio prediction: `1.25` (`beat-baseline`, medium
  confidence), with `1.10` the confirmation threshold;
- absorbing/raw-retention prediction: `0.998` (high confidence), with `0.995`
  the confirmation threshold;
- retry-tail work prediction: at least `0.20` of retry HCMS generation work
  (medium confidence), with `0.10` the confirmation threshold;
- absorbing-HCMS/best-simple raw prediction: `1.20` (medium confidence), with
  `1.10` the confirmation threshold; and
- AHCMS controlled generation and aggregate replay overages: exactly zero
  (medium confidence).

The predictions are informed by a retrospective artifact and are not called
fresh confirmations.  The future traces are not yet sampled or captured.

### 2.3 Primary comparison

The single headline comparison is:

```text
E_ahcms / E_retry >= 1.10
```

where `E_method` is aggregate raw divided by aggregate generation work on the
same nine traces.  This comparison counts only if all retention, tail-support,
trace-completeness, attribution, and controlled-overage constraints below also
pass.  Fixed8 and fixed24/no-salvage are secondary Occam controls.

## 3. Named concept

### 3.1 Name

**Absorbing HCMS-24 (AHCMS-24).**

### 3.2 Plain language

HCMS proposes long candidates and salvages exact shorter prefixes.  Once an
otherwise valid candidate no longer fits the accumulated replay ledger, later
attempts are a timing lottery: they spend generation time while replay capacity
is already saturated.  AHCMS turns that first replay no-fit into an absorbing
state.  It returns the candidates already accumulated and never attempts a
later path in that cell.  Everything else—the 24/8/1 policy, scoring,
candidate identity, point replay ledger, point generation reserve, caps, and
evidence format—stays fixed.

### 3.3 Formal definition

For trace unit `u`, let path slots be `t=1,...,16`.  The inherited HCMS state is
`s_t in {24,8,1}`.  At slot `t`, it selects the stored arm matching `s_t` and
applies the inherited exact-prefix transition.  Let `c_t` be the inherited
positive replay charge when that arm yields an exact eligible candidate, and
let `C_{t-1}` be cumulative accepted charge.

Define the first replay-saturation time

```text
tau_u = min{t : arm t is otherwise exact and eligible,
                 C_(t-1) + c_t > 2.0}.
```

If the set is empty, `tau_u=+infinity`.

- retry HCMS records `drop_ledger_no_fit` at `tau_u` and may continue to later
  slots under the inherited path and generation caps;
- AHCMS records the same drop and terminates immediately at `tau_u`.

Thus AHCMS is a prefix projection of retry HCMS on one stored potential trace.
No q, fitted multiplier, or post-outcome threshold changes either projection.

## 4. Variables and controls

### Independent variable

One binary field only:

```text
after_first_replay_no_fit in {absorb, retry}
```

### Dependent variables

1. aggregate raw per generation-work second;
2. aggregate raw and absorbing/raw-retention ratio;
3. post-first-no-fit path count and generation work;
4. raw recovered after first no-fit;
5. generation-overage cell count;
6. aggregate-replay-overage cell count;
7. AHCMS raw relative to fixed8 and fixed24/no-salvage controls; and
8. invalid, incomplete, timeout, attribution, identity, support and malformed
   evidence counts.

### Controls

AHCMS and retry HCMS share byte-identical:

- complete stored trace unit;
- HCMS proposal and 24/8/1 exact-prefix state transition;
- inherited replay-charge formula `1.25*c_returned + 6.25*c_1`;
- cumulative two-second replay admission endpoint;
- inherited `0.1`-second pre-path point reserve;
- path/candidate caps of 16;
- scorer, SDK cell identity and attribution rules;
- profile, master, arm order and path order;
- generation and replay budgets;
- candidate/raw computation; and
- evidence serialization and invalidity rules.

The only difference is whether control flow terminates after the first
`drop_ledger_no_fit`.

### `varies` and kind

The active search-log entry remains:

```text
varies = complete-cell-resource-risk-admission-and-absorbing-stop
kind   = metric
```

V3 narrows that already-active hypothesis to the one supported dimension;
it does not mint a new research iteration or a second interleaved hypothesis.

## 5. Existing profile artifact

The sealed HCMS attempt is immutable and invalid under its original joint
claim.  It is used only to measure the pre-component bottleneck and choose the
next hypothesis.

The round-9 audit verifies all eleven sealed artifact hashes and recomputes:

```text
absorption_same_trace_estimable=true
absorption_estimable_primary_cells=96
primary_post_no_fit_paths=415
primary_post_no_fit_seconds=59.181928537553
primary_later_recovery_candidates=3
primary_later_recovery_raw=54.0
hcms_post_no_fit_paths=146
hcms_post_no_fit_seconds=18.366501234705
hcms_absorption_raw_loss=18.0
hcms_raw_retention=0.999541494727
absorbing_efficiency_ratio_lower=1.355754716874
generation_overages_without_absorption=4/144
generation_overages_with_absorption=0/144
```

This directly profiles the component's target quantity: work after replay
saturation.  Across the primary grid, the retry tail consumes 59.18 seconds for
three low-value recoveries.  In HCMS alone it consumes 18.37 path-seconds for
one 18-raw candidate.  The same-trace counterfactual retains `39240/39258` raw.

The conservative efficiency projection subtracts only recorded tail path
durations from HCMS generation elapsed.  It does not credit removed loop or
serialization overhead, so `1.355754716874` is a lower bound under that exact
retrospective accounting convention.

These are measured numbers available before AHCMS is built.  They motivate and
size the fresh prediction; they do not confirm it.

## 6. Why the mechanism should work

The replay ledger is monotone: accepted cumulative charge never decreases.
At `tau_u`, the current otherwise-exact candidate fails because adding its
positive charge would cross the replay budget.  Any later candidate also has a
positive charge.  Later timing variation can change which candidate appears,
but cannot restore the already-consumed replay capacity unless it produces a
smaller charge than the rejected candidate.

The sealed trace shows that such recoveries are possible but scarce: three
recoveries after 415 primary paths, worth 54 raw total.  The benefit mechanism
is therefore not “no recovery can happen.”  It is an empirical resource trade:
recovery yield after the saturation signal is too sparse to justify its work
and deadline exposure.

Absorption removes exactly that tail.  On a common potential trace:

```text
W_absorb = sum of path work before and including the first no-fit
W_retry  = W_absorb + W_tail
R_retry  = R_absorb + R_tail
```

with `W_tail>=0` and `R_tail>=0`.  Absorption improves raw per work exactly when

```text
R_absorb/W_absorb > R_tail/W_tail
```

for positive denominators.  The hypothesis predicts this strict inequality by
a material margin on fresh traces.  It does not derive the margin from the
identity; the `1.10` threshold is a preregistered engineering floor informed by
the retrospective `1.3558` projection.

## 7. q-independent matched-trace design

### 7.1 Freeze before capture

One canonical attempt writes and fsyncs `SAMPLING.json` before any trace:

1. draw three unique masters for each of three frozen profiles using uniform
   `secrets.randbelow` rejection sampling;
2. independently Fisher--Yates shuffle all nine profile-master capture units;
3. independently Fisher--Yates shuffle arms `24,8,1` at every path slot; and
4. bind code, config, predictions, thresholds and sampled identities.

No identity, order, trace or failed unit may be redrawn because of an outcome.
A crash consumes the canonical attempt.

### 7.2 Complete potential trace

Each profile-master unit runs in one fresh child process.  The capture kernel
receives no method label.  At every one of 16 path slots it records all three
fresh prefix arms, including construction/reset, indexed interactions, exact
eligible nested returns, return-ready atomic duration, actual replay duration,
scorer output and attribution evidence.

Capture continues through all 16 slots even after a point-ledger no-fit.  The
120-second outer capture bound is separate from the projected two-second
method budget.  Timeout, missing arm, malformed evidence, child failure or
missing eligible replay invalidates the complete unit and joint result; it is
never silently dropped or imputed.

### 7.3 Offline projection

After all capture ends, four methods walk the same stored table:

1. `ahcms_absorbing`;
2. `hcms_retry_removal`;
3. `fixed8_absorbing`; and
4. `fixed24_no_salvage_absorbing`.

Method state selects a stored arm; it cannot change captured outcomes.  There
is no live method order, predecessor, cache, thermal, or scheduling contrast.
The primary pair differs at one transition only.

## 8. Metric definitions

For method `m` and unit `u`, let `P_m(u)` be the selected path prefix before
termination.  For each selected path `t`, let `d_{u,t}` be captured return-ready
atomic path duration.  Let `r_{u,t}` be raw credited by accepted candidates.

```text
W_m = sum_u sum_{t in P_m(u)} d_(u,t)
R_m = sum_u sum_{t in P_m(u)} r_(u,t)
E_m = R_m / W_m
```

`W_m<=0`, non-finite values, or missing rows invalidate the result.

The primary effect is:

```text
Delta_E = E_ahcms / E_retry.
```

The retention constraint is:

```text
rho_raw = R_ahcms / R_retry.
```

Retry-tail support is:

```text
phi_tail = W_retry_tail / W_retry.
```

Tail recovered-raw fraction is:

```text
rho_tail = R_retry_tail / R_retry.
```

The inherited-policy secondary control is:

```text
rho_simple = R_ahcms / max(R_fixed8_absorbing,
                           R_fixed24_no_salvage_absorbing).
```

All ratios are aggregate fixed-sample descriptions over nine units.  There is
no bootstrap, p-value, confidence interval, or population inference.

## 9. Confirmation, disconfirmation and invalidity

### Confirm only if every predicate passes

1. `Delta_E >= 1.10`;
2. `rho_raw >= 0.995`;
3. `phi_tail >= 0.10`;
4. `rho_tail <= 0.005`;
5. `rho_simple >= 1.10`;
6. AHCMS post-first-no-fit paths are exactly zero;
7. AHCMS generation-overage cells are zero;
8. AHCMS aggregate-replay-overage cells are zero;
9. all nine trace units and all 36 method projections are complete; and
10. timeout, duplicate, attribution, identity, support and malformed counts are
    all zero.

### Disconfirm

Complete valid traces disconfirm the hypothesis if any predicate above fails.
In particular:

- no first no-fit on fresh complete traces is disconfirm, not inconclusive;
- a positive but sub-`1.10` efficiency ratio is disconfirm;
- raw retention below `0.995` is disconfirm even if efficiency rises;
- zero overages do not rescue weak efficiency or absent tail support; and
- inherited HCMS failing the `1.10` simple-control ratio rejects its complexity.

### Invalid

Any sampling redraw, missing arm, incomplete trace, timeout, malformed evidence,
attribution failure, out-of-support projection, threshold mutation or
publication mismatch invalidates the joint result.  Invalidity cannot be
relabeled as a disconfirmation or a confirmation.

### Inconclusive

Reserved only for external interruption before a complete canonical fixed
sample exists.  A scientifically completed result has a confirm, disconfirm or
invalid classification.

## 10. Component contract and anti-stacking gate

AHCMS has one contribution component:

| Component | Measured bottleneck | Role | Clean removal | Prospective predicate |
|---|---|---|---|---|
| absorbing no-fit | 415 primary tail paths / 59.1819 s for 54 raw; HCMS 146 paths / 18.3665 s for 18 raw | terminate futile post-saturation work | otherwise identical `hcms_retry_removal` | `Delta_E>=1.10`, `rho_raw>=0.995`, `phi_tail>=0.10`, zero AHCMS overages |

The engineering tests are satisfied on paper:

1. **Measured bottleneck now:** direct same-trace tail work and recovered raw
   exist before implementation.
2. **One ablation:** toggle only absorb versus retry on one complete trace.
3. **System claim:** the claim is constrained end-to-end raw per generation
   work with retention and overage guards, not the existence of a transition.

The replay envelope and calibrated atomic gate from v2 are deleted from the
method, novelty, component count and primary comparison.  q-dependent fixtures
may be software tests but can never count as efficacy or necessity evidence.

This is not a stack.  It is a local replacement of one state transition.

## 11. Distinguishing prediction

A larger fixed reserve or replay multiplier predicts fewer admissions whenever
remaining time or ledger slack is small.  AHCMS instead predicts a structural
break exactly after the first replay-saturation event:

- before the first no-fit, AHCMS and retry HCMS are byte-for-byte identical;
- after the first no-fit, AHCMS performs zero paths regardless of remaining
  generation time; and
- the removed retry tail has low raw yield per work, so aggregate efficiency
  rises while at least `99.5%` raw remains.

A generic combination of margins and caps does not entail this event-aligned
zero-tail prediction.

## 12. Occam controls

The simplest rival is retry HCMS itself: absorption may merely remove useful
recovery.  It is the primary removal.

Fixed8 absorption tests whether the 24-state HCMS base is unnecessary.
Fixed24/no-salvage absorption tests whether exact-prefix salvage is unnecessary.
Neither comparator is claimed as a component ablation.

If AHCMS is not at least `1.10` above the stronger simple control in raw, the
system rejects HCMS complexity even if absorption beats retry in efficiency.

## 13. Corrected finite-population statement

V3 makes no finite-population probability claim for its engineering result.
The v2 statement is nevertheless corrected for the record.

Take fixed values `z_1,...,z_(n+1)` and uniformly assign one index to evaluation,
with the other `n` assigned to calibration.  Failure of

```text
z_eval <= max(z_calibration)
```

requires the evaluation value to be the unique strict maximum of all `n+1`
values.  If a unique strict maximum exists, uniform label assignment selects it
with probability `1/(n+1)`; if the maximum is tied, failure probability is zero
because at least one equal maximum remains in calibration.  Therefore failure
probability is at most `1/(n+1)` and coverage is at least `n/(n+1)`.

The discarded wording “the rank is uniform” was ambiguous under ties.  This
unique-strict-maximum proof is exact.  It is historical clarification only and
does not justify AHCMS, target transfer, conditional coverage, or a q-selected
claim.

## 14. Fixed eight-category bias surface

1. **Selection:** three frozen controlled profiles are purposeful and do not
   represent target prevalence.  Masters are sampled once from a declared
   domain before capture; no outcome-dependent replacement is allowed.
2. **Confounding:** every method is an offline projection of the same complete
   trace.  The primary pair differs only in the post-no-fit transition; no live
   method order or predecessor exists.
3. **Allocation / assignment:** unit and arm capture orders use independently
   recorded Fisher--Yates permutations.  Methods receive all units; there is no
   condition allocation after outcomes.
4. **Deviation from protocol:** code/config/predictions/SAMPLING are bound
   before capture.  A crash or hash mismatch consumes and invalidates the
   attempt; no rescue run is silently substituted.
5. **Missing data:** missing arms, censored required work, timeout, child
   failure and missing replay are retained as invalid complete units, never
   dropped from a favorable denominator.
6. **Measurement:** return-ready path work, exact eligibility, replay elapsed,
   SDK scorer output and candidate identity are retained.  Reload must
   reconstruct every metric from stored rows.
7. **Analysis flexibility:** the primary pair, formulae, aggregation,
   thresholds, invalidity rules and simple controls are frozen here.  No q,
   fitted margin, bootstrap or subgroup selection exists.
8. **Selective reporting:** all nine units, 36 projections, failures, zeros,
   tail rows and invalid artifacts publish.  Every completed outcome is mapped
   to confirm, disconfirm or invalid.

## 15. Assumptions and validity domains

1. **Potential consistency:** a stored arm outcome is unchanged by later
   offline method projection.  This holds only for deterministic mock agents
   keyed by frozen profile/master/path/arm; it is not asserted for a live model.
2. **Complete capture:** all arms and required replays exist for all 16 slots.
   Any absence invalidates the unit rather than invoking extrapolation.
3. **Positive work and charges:** path durations and eligible replay charges
   are positive and finite.  Nonpositive/non-finite values invalidate.
4. **Exact trigger:** `drop_ledger_no_fit` means the arm is otherwise exact and
   eligible but its inherited cumulative point charge crosses two seconds.
5. **Prefix projection:** absorption changes only termination after the trigger;
   it cannot change any pre-trigger state or outcome.
6. **Fixed controlled support:** claims cover only the three named deterministic
   profiles, 16 slots and arms 24/8/1.
7. **No target tail claim:** inherited point charges and the 0.1 reserve are not
   remote safety certificates.  Target attack mutation remains closed.
8. **Fixed-sample interpretation:** nine units establish the realized
   comparison only; they do not estimate a master/profile population effect.

Assumptions 1–5 are load-bearing for component attribution.  Violating any of
them invalidates the matched removal.

## 16. Alternative explanations

1. **No saturation on fresh traces:** if no first no-fit occurs, the component
   has no supported bottleneck and is disconfirmed.
2. **Useful recovery tail:** later candidates may carry enough raw to violate
   retention or tail-yield thresholds.
3. **HCMS base unnecessary:** fixed8 or fixed24 may match AHCMS raw, triggering
   the simple-control rejection.
4. **Profile artifact:** reset/cliff profiles may create the tail; no prevalence
   beyond the fixed controlled set is claimed.
5. **Work metric mismatch:** path work omits target networking/scheduling costs.
   The claim is limited to retained controlled return-ready durations.
6. **Replay risk remains:** absorption can improve generation efficiency while
   inherited point replay accounting remains unsafe elsewhere.  Any AHCMS
   aggregate replay overage rejects the result.
7. **Target scaling reversal:** a two-second mock tail may be negligible under a
   9000-second target phase, or live models may recover after no-fit.  Only a
   later source-compliant target bridge may answer that.

## 17. Failure modes and implementation traps

- Capturing only until absorption would erase the removal's tail.  The kernel
  must capture the full retry trace through slot 16.
- Executing methods live would reintroduce predecessor and host confounds.  All
  methods must be offline projections.
- Replaying only accepted candidates would leave the point-ledger removal
  unsupported.  Every eligible stored arm must receive a replay outcome.
- Treating path cost subtraction as exact wall-clock savings would overclaim.
  The prospective primary metric uses captured selected path work directly.
- Changing the trigger from first otherwise-exact replay no-fit to any failed
  interaction would conflate eligibility and saturation.
- Counting q-dependent stress fixtures as efficacy would repeat round 9.
- Retrying a crashed canonical attempt under a new name would violate the
  single-draw contract.
- Letting a locally clean result mutate `experiments/attack.py` without a
  reviewed target scaling design would violate `PROBLEM.md`.

## 18. Literature and source chain

The component does not rely on a conformal theorem.  The targeted source pass
still bounds what may be claimed:

- Romano, Patterson and Candès, *Conformalized Quantile Regression*, NeurIPS
  2019, provides marginal exchangeable upper-tail coverage, not hard cell
  safety: https://proceedings.neurips.cc/paper_files/paper/2019/file/5103c3584b063c431bd1268e9b5e76fb-Paper.pdf
- Angelopoulos et al., *Conformal Risk Control*, ICLR 2024, controls expected
  loss under exchangeable loss functions, not zero misses in a strict cell:
  https://proceedings.iclr.cc/paper_files/paper/2024/file/f3549ef9b5ff520a7e41ff3cc306ab2b-Paper-Conference.pdf
- Angelopoulos, Barber and Bates, *Online conformal prediction with decaying
  step sizes*, ICML 2024, controls retrospective average coverage under
  dependence, not the next deadline:
  https://proceedings.mlr.press/v235/angelopoulos24a.html
- Howard et al., *Time-uniform Chernoff bounds via nonnegative
  supermartingales*, 2020, requires a proved conditional tail process before
  optional-stopping guarantees apply: https://doi.org/10.1214/18-PS321
- Shojaei, *Conformal Recovery-Deadline Certificates for Runtime Assurance of
  Adapting Controllers*, arXiv:2606.25371v1, separates marginal statistical
  autonomy from a verified backstop.  It is a June-2026 preprint and not used as
  proof here: https://arxiv.org/abs/2606.25371

The competition source provides the operational boundary: the gateway applies
9000-second phases, replay is cumulative across returned candidates, and attack
code cannot cancel an in-flight `RemoteEnv` operation.  Therefore a controlled
AHCMS result cannot become a remote void-proof claim.

## 19. Taxonomy

- opportunity pattern: **Resource Bottleneck**, secondarily Failure/Risk Gap;
- method paradigm: **Artifact/System**, secondarily Robustification; and
- dominant operation: **replace**.

AHCMS replaces retry-after-saturation with one absorbing state.  It is not
Bridge Opportunity × Synthesis/Unification and does not integrate multiple new
techniques.  The local move is the entire hypothesis.

## 20. Self-critique

### Falsifiability

Every complete result has exact numeric thresholds.  A small positive gain,
absent no-fit support, excess raw loss, simple-control parity, or any AHCMS
overage rejects the claim.

### Mathematical ownership

The efficiency identity was re-derived from additive work/raw on a common
trace.  It gives the condition for improvement but not its magnitude; the
`1.10` floor remains an empirical prediction.  The historical finite-population
bound was re-derived through the unique strict maximum, not an ambiguous rank
under ties.

### Simplest explanation

The hypothesis is the simplest explanation identified by round 9: one measured
tail, one state change, one removal.  Replay-envelope and atomic-gate credit is
deleted.

### Problem alignment

If confirmed, AHCMS would show that a source-compatible event-aligned stop can
preserve almost all controlled candidate value while materially reducing work
and deadline exposure.  That directly informs competition allocation, but it
still requires a reviewed 9000-second scaling and Kaggle commit-run bridge.

## 21. Round-9 issue disposition encoded by v3

1. **Genuine held-out component ablation:** prospective AHCMS and retry are
   deterministic projections of the same nine q-independent complete traces.
2. **Distinct bottleneck or reduced claim:** the claim is reduced to absorbing
   no-fit, the only directly measured bottleneck; replay/atomic are unclaimed.
3. **Simpler explanation first:** absorbing-only is the primary hypothesis and
   primary removal.
4. **Tied-rank correction:** the unqualified rank wording is removed and the
   exact unique-strict-maximum argument is recorded without supporting the
   engineering claim.

## Gate Check

- Falsifiable variables, controls and one primary comparison: **author PASS**.
- Named plain-language and formal concept: **author PASS**.
- Engineering profile artifact exists before implementation: **author PASS**.
- One component, one measured bottleneck, one clean removal: **author PASS**.
- Failure modes, metrics and fixed thresholds: **author PASS**.
- Fixed eight-category bias surface: **author PASS**.
- Taxonomy and anti-stacking: **author PASS**.
- Target/Kaggle bridge: **closed**.
- Independent theory review: **not dispatched; Phase 2 remains closed**.

## Decision

Freeze AHCMS-24 v3 for deterministic author verification.  If that passes, the
next task may spend review round 10 on one fresh sterile re-review containing
the four round-9 issues.  No Phase-3 runner, attack mutation, Kaggle action or
submission is admitted by this artifact.

## Next Steps

1. Run the v3 author checker and bind exact hashes/line count.
2. Preserve this hypothesis immutably before any review dispatch.
3. On a later task, dispatch one fresh sterile re-review with explicit
   RESOLVED/IMPROVED/UNCHANGED/WORSE judgments for all round-9 issues.
