# Hypothesis iteration 8 v2 — Random-Split Trace PRAC-24

**Date:** 2026-07-22
**Phase:** 2 — Hypothesis Formation
**Cycle:** 3
**Research iteration:** 4/5
**Claim type:** predictive engineering with a finite-population marginal lemma
**Question type:** predictive
**Supersedes:** `research-log/164-hypothesis-iter-8-prac24.md`
**Status:** immutable candidate for independent re-review

## 1. Prediction first

On the first canonical controlled Phase-3 attempt defined by the v2 config:

1. the three profile-specific calibration pairs will all be finite and satisfy
   `q_replay <= 1.25` and `q_generation <= 3.50`;
2. across the nine randomly role-assigned evaluation traces,
   `prac_hcms` aggregate constrained raw will be at least `1.10` times the
   larger valid aggregate of `prac_fixed8` and
   `prac_fixed24_no_salvage`;
3. all 27 PRAC evaluation method-cells will have zero projected generation and
   aggregate-replay overages, and all 36 evaluation method-cells including the
   legacy point diagnostic will be complete and auditable;
4. each of the three claimed PRAC components will pass its exact clean-removal
   predicate; and
5. all `3 profiles * 22 sampled units * 16 paths * 3 prefix arms` potential
   arms, roles, orders, censoring outcomes and policy projections will reconcile
   before `COMPLETE` is published last.

The finite-population lemma predicts separate marginal `19/20` coverage for
one randomly assigned evaluation trace in one controlled profile before
calibration is observed. It does not predict simultaneous coverage, coverage
conditional on a finite or small q, live wall-clock controller safety, target
exchangeability, official score or leaderboard gain.

Confidence is **medium** for finite q below the feasibility ceilings,
**medium** for the 1.10 policy ratio, and **high** for the deterministic
clean-removal conformance predicates. Failure of any numbered condition rejects
the joint controlled claim.

## 2. Round-8 verdict and structural disposition

Round 8 is preserved verbatim in
`research-log/166-prac24-theory-review-round-8.md`. It returned
`NEEDS_REVISION`, while explicitly accepting the rank-19 algebra, cumulative
prefix implication, generation implication, fixture inequalities, profile
reconstruction, taxonomy and fixed bias enumeration.

| Required fix | v2 disposition |
|---|---|
| calibration/evaluation predecessor mismatch makes exchangeability incredible | **structurally replaced:** no method executes during trace capture; calibration and evaluation are a uniform random role split of the same q-independent potential-trace population; methods are later matched projections, so no method predecessor exists |
| compound high-ceiling/salvage component lacks one clean removal | **demoted:** HCMS exact-prefix policy is inherited and receives no PRAC component credit; fixed-8 and fixed-24/no-salvage remain Occam policy comparators, not claimed component ablations |
| aggregate raw ratio does not measure candidate-boundary amortization | **claim withdrawn:** v2 makes no candidate-boundary causal or bottleneck claim; the 1.10 ratio is a prospective policy-selection endpoint only |

The reviewer also coached two boundary clarifications. V2 defines the empty
replay score as zero when every PRAC stream has `K=0`, while any missing arm or
malformed evidence remains infinity. It also states repeatedly that filtering
on finite/sub-ceiling q does not inherit unconditional `19/20` coverage.

## 3. Repair alternatives considered before selection

Scores are `impact * feasibility / complexity`, each input 1--5. A score does
not rescue an option whose evidence premise fails.

| Repair | Likely failure mode | Hardest trap | Evidence check | I | F | C | Score | Decision |
|---|---|---|---|---:|---:|---:|---:|---|
| A. predecessor-stratified live calibration | q-dependent predecessor policies make calibration circular and multiply sparse strata | reproducing every predecessor, position, profile and policy without using the unknown q | round 8 identifies the mismatch; v1 had 12 profile-position q pairs already | 4 | 2 | 4 | 2.00 | reject |
| B. fresh subprocess plus cooldown | thermal/scheduler drift survives process exit, leaving exchangeability assumed | proving the operating system and hardware erased all prior state | no current artifact proves cache or thermal reset | 3 | 3 | 2 | 4.50 | reject |
| C. uniformly role-split matched potential traces | offline projection may not reproduce a live target and capture cost is larger | role-blind capture of every q-independent potential arm with complete censoring | random role assignment directly removes method predecessor and supports a finite-population rank argument | 5 | 4 | 3 | **6.67** | **select** |
| D. drop the probability statement and tune an empirical margin | safe-looking mock result has no declared miss-risk meaning | choosing the margin after the failed run | primary literature and repeated reviews reject observed maxima/arbitrary margins | 1 | 5 | 1 | 5.00 | reject |

V2 selects C because it repairs the theorem's sampling geometry rather than
adding an unverifiable reset ritual or weakening resource risk back into a
point heuristic.

## 4. Frozen artifacts

- normative config: `experiments/configs/prac24-c3-v2.json`, SHA-256
  `ab2a4d871fe6db8cb4d150554260a958956b27ae139069cb07d6f7923195bb42`;
- deterministic author checker:
  `experiments/poc/prac24_phase2_reference_v2.py`, SHA-256
  `66dec6ccfd43af568515e5377eaf02bd816fcbb4768974dfae1f536f7ed69b00`;
- sealed-run diagnostic:
  `experiments/poc/rahcms_resource_diagnostic.py`, SHA-256
  `2b5d748f5550b58ee953afb1643cca0f94f581e9c144b3dabaf28a162667c8ad`;
- literature report: `research-log/162-resource-risk-admission-literature.md`,
  SHA-256
  `d42f11db54aa3a7d718234c69c64e00be39d0ddbb6fd44049a1a55d28a8767cf`;
- diagnosis/selection report:
  `research-log/163-rahcms-diagnosis-and-candidate-selection.md`, SHA-256
  `3e6fc56ca5bda8e682bff2ea41f983c51ef605c271bed3fc8018183ce17c38f1`;
- round-8 report: `research-log/166-prac24-theory-review-round-8.md`,
  SHA-256
  `37f06b237dc62c421d95983a2423d94a11d3b6dded0cd8094f4faf7091de00ab`.

The v2 config binds five authoritative SDK sources, ten evidence artifacts and
four immutable v1 lineage artifacts. The incumbent attack remains SHA-256
`8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d`.
This revision does not alter it.

## 5. Why a potential-trace experiment answers the narrow question

The v1 theory problem was not merely order imbalance. It attempted to learn q
from HCMS trace captures and then compare live sequential methods whose wall
times could depend on different predecessors. Position labels could not make
those two processes exchangeable.

V2 separates two questions:

1. **Policy-value/resource question:** given the same complete table of possible
   prefix-arm outcomes, which deterministic policy returns the most valid raw
   while respecting the risk-adjusted budgets?
2. **Implementation-conformance question:** does the actual controller implement
   each admission and transition correctly on bounded adverse fixtures?

The first is evaluated as matched deterministic projections of held-out trace
tables. No policy is run during capture, so it cannot affect timing, arm
availability or the next method. The second is tested separately and supplies
no efficacy raw. This narrowing loses a live-controller performance claim, but
it identifies the policy comparison without predecessor confounding. Target
execution remains a later bridge.

## 6. Uniform sampling and custody

At the start of the one canonical attempt, before any trace exists, the runner
uses `secrets.randbelow` rejection sampling to create a complete immutable
`SAMPLING.json`:

1. draw 22 unique masters independently for each of three profiles;
2. apply an independent uniform Fisher--Yates permutation to each 22-master
   list; label the first 19 calibration and last 3 evaluation;
3. apply an independent uniform Fisher--Yates permutation to all 66
   profile-master capture units; and
4. independently permute the three prefix-arm execution orders inside every
   unit/path slot.

The full manifest is written and fsynced before capture. No identity, role or
order may be redrawn because of a trace, q, failure or result. A crash consumes
the scientific attempt.

The trace kernel receives profile, master, path slot and arm order but never
the calibration/evaluation role. All q-independent traces are captured in the
interleaved manifest order. Evaluation objects remain only in runner memory;
no evaluation-derived byte is published until all capture ends, calibration
scores are published and q is sealed. The final bundle then publishes every
trace and role for audit.

The validity domain is exact: `secrets.randbelow` must deliver uniform draws,
Fisher--Yates must be implemented without modulo bias, the kernel must remain
role blind, and there must be no outcome-dependent redraw. These are mechanical
Phase-3 review obligations, not assumptions waved into existence.

## 7. One matched potential-trace unit

For one profile/master unit, a fresh spawned child captures 16 path slots. At
each slot it executes fresh requested-prefix arms `m in {24,8,1}` in the
manifest's random arm order. Each arm retains:

- environment construction and reset evidence;
- indexed interaction suffixes for every message;
- exact nested eligible returns among 24/8/1;
- elapsed generation from a return-ready start through a return-ready current
  candidate-list checkpoint;
- actual fresh replay elapsed for every eligible returned prefix; and
- actual scorer output plus identity evidence.

Thus a unit is a q-independent table of potential outcomes. After q is sealed,
a policy walks path slots in order, selects only the arm matching its current
proposal, applies its eligibility/state transition, and either admits or stops.
All policies project the same table. Potential arms not selected by a policy
remain measurement evidence and incur no policy generation/replay charge.

Capture cost is not policy cost. V2 reports capture runtime separately and
never credits unselected arm work against or for a policy. This is an offline
matched policy experiment, not a claim that a live attack can observe
counterfactual arms for free.

## 8. Calibration objects

For trace unit `e` and PRAC policy `u`, let its full no-q eligible candidate
stream have `K_eu` candidates: simulate proposal, eligibility and monotone state
but admit every eligible candidate, so replay no-fit never truncates this
calibration stream. Candidate `i` originates at path slot `p(i)`, has actual
replay cost `a_eui`, and has positive base charge

\[
ell_{eui}=1.25c_{eui}+6.25c_{e,p(i),1}.
\]

Here `c_eui` is the return-ready generation cost of the arm/prefix the policy
would return, and `c_e,p(i),1` is the separately captured one-message arm at
that same path slot. For every policy with `K_eu>0`, define

\[
Z^R_e=\max_u\max_{1\le k\le K_{eu}}
\frac{\sum_{i\le k}a_{eui}}{\sum_{i\le k}ell_{eui}}.
\]

The outer maximum covers `prac_hcms`, `prac_fixed8`, and
`prac_fixed24_no_salvage`; policies with `K=0` contribute no inner maximum. If
every policy has `K=0`, set `Z^R_e=0`. A missing, timed-out, censored or
malformed required arm instead sets `Z^R_e=+infinity`.

For path slot `p` and requested arm `m`, let `g_epm` be its complete
return-ready elapsed time and `b(m)>0` the frozen base duration. Define

\[
Z^G_e=\max_{p\le16,m\in\{1,8,24\}}\frac{g_{epm}}{b(m)}.
\]

Any missing required arm makes `Z^G_e=+infinity`.

Within each profile there are `n=19` calibration units. For
`alpha=0.05`, both multipliers use the independent score's order statistic

\[
r=ceil((n+1)(1-alpha))=ceil(20*0.95)=19.
\]

`q_replay` is rank 19 among the 19 replay scores and `q_generation` is rank 19
among the 19 generation scores. The multipliers are separate; infinity causes
all PRAC policies to abstain and rejects the feasibility prediction.

## 9. Finite-population marginal lemma

Condition on the complete role-blind 22-score potential table for one profile.
The uniform Fisher--Yates role permutation assigns 19 positions to calibration
and three to evaluation. Choose any one of the three symmetric evaluation
slots. Among the 19 calibration scores and that evaluation score, the
evaluation score's rank is uniform over 20 positions under the random role
permutation. Therefore, with conservative ties,

\[
P(Z^R_{eval}\le q_{replay})\ge19/20,
\qquad
P(Z^G_{eval}\le q_{generation})\ge19/20.
\]

For any named PRAC policy, its replay prefix score is no larger than the
all-policy `Z^R`. On the replay event, every prefix admitted by
`q_replay*L(k)<=2` has actual cumulative replay `A(k)<=2`.

On the generation event, every selected arm cost is no larger than its
`q_generation*b(m)` charge. Starting only when this charge fits the observed
remaining budget inductively prevents a projected generation overage for that
trace.

The probability is over the role permutation, not over target models. Separate
replay/generation statements do not yield a joint 0.95 guarantee. Three
evaluation units do not yield simultaneous 0.95 coverage. Most importantly,
after observing that q is finite or below 1.25/3.50, the coverage probability
conditional on that event is not asserted. All held-out projections publish
regardless of q, and q ceilings are engineering feasibility predictions only.

## 10. Inherited policy and exact methods

HCMS exact-prefix behavior is an inherited base, not a new PRAC component:

```text
state <- 24
propose state
return longest exact eligible prefix in 24,8,1
after success: state <- min(state, returned_prefix)
after exact ineligible drop: state <- 1
never increase state
```

V2 makes no causal claim that this policy works through candidate-boundary
amortization. Its prospective 1.10 ratio merely decides whether the inherited
policy is useful enough to retain.

| Method | Policy | Resource behavior |
|---|---|---|
| `prac_hcms` | inherited HCMS | both q multipliers; absorbing no-fit |
| `prac_fixed8` | propose at most 8; exact 8/1 salvage; monotone | same q multipliers; absorbing no-fit |
| `prac_fixed24_no_salvage` | propose 24; exact 24 only | same q multipliers; absorbing no-fit |
| `point_hcms_retry` | inherited HCMS | q values 1, old 0.1 reserve, retry after no-fit |

The legacy point method is a bundled diagnostic and receives no component
attribution.

## 11. Projection kernel

Every method calls the same pure projection function with method configuration
as data:

```text
state <- method.initial_state
candidates <- []
generation_spent <- 0
for path_slot in 1..16:
    proposed <- method.proposal(state)
    arm <- trace[path_slot, proposed]
    charge <- method.generation_charge(proposed)
    if 2-generation_spent < charge: stop
    generation_spent += arm.actual_return_ready_elapsed
    if generation_spent > 2: mark projected generation overage
    returned <- method.salvage(arm.indexed_exact_prefixes)
    if no eligible return: apply ineligible transition; continue
    if method.cumulative_replay_charge(candidates + returned) > 2:
        record drop_ledger_no_fit
        if method.absorbing: stop
        apply removal transition; continue
    append returned and apply success transition
aggregate actual replay from trace for candidates in order
record score, raw, both overages and every decision predecessor
```

The projection must reconstruct from persisted trace rows and agree byte-for-
byte with the in-memory result. Potential-outcome rows cannot be edited or
discarded because a policy did not select them.

## 12. Three claimed components and exact removals

| PRAC component | One role | Measured bottleneck | Clean removal | Exact confirmation predicate |
|---|---|---|---|---|
| complete-trace prefix envelope | supply one all-policy cumulative replay multiplier at the aggregate endpoint | candidate coverage `187/189`, aggregate HCMS replay overage `0/36`, safety prefix ratio `1.102552878986` | change only `q_replay` to 1 | all PRAC held-out aggregate overages 0; on replay-spike fixture full actual <=2 and removal actual >2; `q_replay<=20/19` means not distinguished and joint failure |
| absorbing no-fit | terminate future attempts after first exact replay no-fit | 420 tail paths, 59.767362 seconds, three candidates | change only absorbing stop to retry | saturation fixture full tail paths 0, removal tail paths exactly 3, removal recovered candidates 0 |
| return-ready atomic gate | reserve a complete atomic arm before start | four generation overages; `44/84` zero-interaction paths exceeded 0.1 seconds | change only q-generation gate to old 0.1 reserve | all PRAC held-out generation overages 0; bounded setup full does not start, removal starts/crosses; `q_generation*b24<=0.1` means not distinguished and joint failure |

Each removal changes exactly one field. All conformance fixture raw is excluded
from efficacy. The end-to-end contribution claim is a valid, material
controlled PRAC system result; it is not “we combined conformal calibration,
early stopping and HCMS.”

## 13. Exact conformance fixtures

### Replay spike

After q is sealed, expose ten exact one-message candidates. Each has base
charge 0.2 and bounded actual replay `0.19*q_replay`. Full PRAC admits
`min(10,floor(10/q_replay))`, so actual replay is at most 1.9 seconds. The
q=1 removal admits ten and crosses two seconds iff `q_replay>20/19`. Otherwise
the component is not distinguished and constants remain unchanged.

### Saturation tail

Make the next exact one-message candidate fail sealed replay admission, then
expose exactly three bounded exact paths that also cannot fit and cap. Full
attempts no tail path. The removal attempts three and returns no additional
candidate.

### Bounded long setup

Let `u=q_generation*b(24)`, set return-ready remaining
`r=(u+0.1)/2`, and expose bounded setup `d=r+0.05`. When `u>0.1`, full refuses
because `r<u`; the point removal starts because `r>0.1` and crosses because
`d>r`. Otherwise the component is not distinguished.

### Delayed cliff

The inherited HCMS policy must transition `24 -> 8` and never increase. This is
a correctness fixture and supplies no component or efficacy credit.

## 14. Profiles, metrics and primary comparison

Profiles remain controlled mechanisms rather than target samples:

1. `steady_linear_prac_v2`: compliant, latency 0.0075 seconds;
2. `reset_dominant_prac_v2`: fixed latency 0.043 plus 0.0008 per action; and
3. `immediate_cliff_prac_v2`: exact through message 8, then context-limited,
   latency 0.0015.

The primary comparison is aggregate constrained raw of `prac_hcms` divided by
the larger aggregate of the two valid simple PRAC policies over nine evaluation
traces. A method-cell with an overage, invalid identity or malformed evidence is
invalid, not assigned zero. If either comparator is invalid, the primary policy
comparison is invalid.

Secondary metrics are q values, candidates, exact-prefix counts, per-profile
raw, stopped paths, actual replay, generation time and legacy point behavior.
They cannot replace the primary outcome.

## 15. Failure bands

| Outcome | Decision |
|---|---|
| all validity, q, ratio and three clean-removal gates pass | confirm narrow controlled PRAC hypothesis; eligible only for target-confidence bridge |
| valid q and zero overages but ratio in `[1.00,1.10)` | reject inherited HCMS complexity; prefer strongest simple PRAC policy |
| ratio below 1.00 | refute inherited HCMS policy value |
| q infinity or above a ceiling | reject controlled feasibility; do not clip q or redraw sampling |
| q conditioning used to claim 0.95 | invalidate inference |
| any incomplete trace, role leak, redraw, malformed arm, projected PRAC overage or missing policy cell | invalidate joint result regardless of raw |
| any removal predicate fails or is not distinguished | reject that component and the joint three-component claim |

There is one canonical sampling manifest, one trace capture and one projection.
No seed redraw, q clipping, threshold rewrite, trace replacement, profile
replacement or output-dependent retry is allowed.

## 16. Validity domains

1. **Uniform role assignment:** `secrets.randbelow` and Fisher--Yates must be
   uniform and recorded without modulo bias.
2. **Role blindness:** the capture kernel cannot read split roles; any leak
   invalidates finite-population exchangeability.
3. **No redraw:** a sampling/capture failure consumes the attempt.
4. **Matched support:** all units contain 16 slots and all 24/8/1 arms; no
   policy requests outside that table.
5. **Potential consistency:** policy projection must not affect an arm's stored
   outcome; this is valid for the controlled deterministic profiles only.
6. **Complete-arm timing:** elapsed generation ends at a return-ready checkpoint,
   not the last model interaction.
7. **Censoring:** any missing required arm makes the trace score infinity.
8. **Scorer identity:** `16m+2` is used only with exactly one correctly
   attributed qualifying event per message and all source preconditions.
9. **Projection symmetry:** all methods share one kernel and one trace; only
   named method fields differ.
10. **Marginality:** no conditional, simultaneous or target coverage is inferred.
11. **Offline scope:** potential-trace policy value does not prove live attack
    runtime or allow counterfactual observation in deployment.
12. **Target physics:** in-flight RemoteEnv operations remain uncancellable;
    bounded controlled conformance is not target void-proofness.
13. **Completeness:** all trace, sampling, q, projection, fixture and hash rows
    reconcile before COMPLETE-last.
14. **No official transfer:** confirmation does not imply leaderboard gain.

## 17. Fixed eight-category bias surface

1. **Selection.** Profiles are authored around known steady/reset/cliff
   mechanisms. Masters and split roles are random, but profiles are not a target
   population.
2. **Confounding.** Random role assignment and matched trace projection remove
   method predecessor as a policy confound; capture-time host drift may still
   change the finite table but is independent of role if the kernel is blind.
3. **Assignment.** Uniform recorded Fisher--Yates assigns roles/orders. Any
   modulo-biased or post-outcome assignment invalidates the lemma.
4. **Protocol deviation.** Hash, sampler, trace schema, arm count, q, policy,
   fixture or retry deviation invalidates; it is not repaired in place.
5. **Missing data.** A missing/censored arm makes its complete trace infinity;
   a missing evaluation projection invalidates the bundle.
6. **Measurement.** Mock wall time is noisy and potential outcomes are authored.
   Indexed suffixes, actual replay, return-ready checkpoints and persisted
   reconstruction expose but do not erase this limitation.
7. **Analysis flexibility.** Profiles, sample counts, roles, rank, bases, q
   ceilings, policies, ratio and removal predicates are frozen before output.
8. **Selective reporting.** All sampling roles, potential arms, infinities,
   evaluation projections and fixture failures publish together regardless of q.

## 18. Taxonomy, anti-stacking and alternatives

- opportunity: **Failure/Risk Gap**, secondary Resource Bottleneck;
- method paradigm: **Robustification**, secondary Formal Derivation;
- dominant operation: **replace**.

V2 replaces point resource admission with a complete-trace cumulative-prefix
risk object and replaces retry-after-no-fit with an absorbing transition. The
matched trace corpus is measurement design, not a fourth contribution
component. This is not Bridge Opportunity x Synthesis/Unification.

The three engineering tests are explicit: every claimed component has a
pre-existing numbered bottleneck, exactly one clean removal and an end-to-end
constrained system gate. HCMS is inherited, so its unmeasured candidate-boundary
story cannot inflate component count.

Distinguishing predictions are local: pooled candidate coverage can look high
while a cumulative prefix is unsafe; a retry-only removal consumes three
post-saturation paths without utility; and the fixed reserve starts bounded work
the atomic gate rejects. A vague stack does not entail these exact divergences.

Strong alternatives remain:

- authored profile composition, not HCMS structure, may create the 1.10 ratio;
- the conservative max-over-policies q may make fixed 8 dominate;
- q may exceed feasibility ceilings despite valid marginal calibration;
- potential-arm capture may differ from a live endogenous controller;
- OS randomness or role blinding may be implemented incorrectly;
- deterministic fixtures may show conformance but have low target frequency;
- target models may fail before 8, recover, oscillate or have heavier atomic
  tails than the controlled profiles.

These alternatives bound the claim. None is converted into target confidence
by adding a limitations paragraph.

## 19. Competition bridge remains closed

Phase-3 confirmation would establish only controlled matched-trace policy value
and bounded implementation conformance. Before `experiments/attack.py` changes,
a separate task must bind target scaling from two-second profiles to the source
9000-second phases, an explicit target atomic-tail assumption, incumbent
fallback, and expected benefit over the linked 69.570 result. Before submission,
all seven `PROBLEM.md` confidence gates and Kaggle artifact parity must pass.

Submission authorization exists, but confidence has not been earned.

## 20. Author verification and next gate

Exact command:

```bash
comp/.venv/bin/python -I experiments/poc/prac24_phase2_reference_v2.py \
  --config experiments/configs/prac24-c3-v2.json --hypothesis research-log/167-hypothesis-iter-8-prac24-v2.md
```

Expected output begins `prac24_phase2_author_check_v2=PASS` and includes:

```text
hypothesis_lines=533
round8_issues_addressed=3
sampling_manifest=single_draw_no_retry
split=19_calibration_3_evaluation_per_profile
capture_role_blinded=true
method_predecessor=none_matched_trace_projection
calibration_unit=complete_all_policy_potential_trace
cell_risk_alpha=0.050000
order_statistic_rank=19
empty_replay_score=0.0
censoring=positive_infinity
finite_q_conditioning_claim=forbidden
inherited_hcms_component_credit=false
contribution_components=3
clean_component_removals=3
evaluation_method_cells=36
official_score_claim=withheld
attack_unchanged=true
phase3_artifacts=absent
review=not_dispatched
```

The superseding hypothesis must be committed before re-review. The next sterile
review receives all three round-8 issues for explicit
`RESOLVED/IMPROVED/UNCHANGED/WORSE` disposition plus the complete v2 artifact.

Only a scrutinized `RIGOROUS` verdict opens Phase 3. Until then the v2 runner,
attempt directory, attack mutation, Kaggle commit run and submission remain
prohibited. Writing v2 does not spend a review round; usage remains `8/12`.

## Problem alignment

If confirmed under its narrow scope, PRAC-24 would identify a resource-aware
candidate policy that materially improves controlled score without projected
generation/replay overage, directly serving the competition allocation question
while leaving mandatory target evidence and submission confidence unresolved.
