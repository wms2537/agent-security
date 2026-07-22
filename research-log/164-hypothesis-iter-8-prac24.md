# Hypothesis iteration 8 — Prefix-Risk Absorbing Controller 24

**Date:** 2026-07-22
**Phase:** 2 — Hypothesis Formation
**Cycle:** 3
**Research iteration:** 4/5
**Claim type:** predictive empirical/systems engineering with a conditional finite-sample lemma
**Question type:** predictive
**Status:** immutable candidate for independent theory review

## 1. Prediction first

On the first fresh controlled Phase-3 bundle defined by the normative config,
and only if calibration is finite and every validity gate passes:

1. `prac_hcms` aggregate constrained raw will be at least `1.10` times the
   larger aggregate of `prac_fixed8` and `prac_fixed24_no_salvage` across the
   36 primary method-cells per method;
2. the sealed profile-position multipliers will satisfy
   `q_replay <= 1.25` and `q_generation <= 3.50`;
3. every `prac_*` primary cell will stay within both two-second controlled
   generation and aggregate-replay budgets, with all 144 primary repetitions,
   order positions, predecessor pairs, identities and evidence complete;
4. the clean replay-envelope removal and the clean atomic-generation-gate
   removal will each fail its preregistered adverse safety fixture, while the
   full controller passes;
5. on the saturation-tail fixture the full controller will attempt zero paths
   after the first replay-ledger no-fit, while the clean retry removal attempts
   at least three and recovers zero candidates; and
6. the delayed-cliff fixture will produce `24 -> 8` and never return upward.

The calibration theorem predicts only marginal `0.95` coverage for one next
exchangeable latent HCMS trace in each exact controlled profile-position
stratum. It does **not** predict simultaneous 0.95 coverage of all evaluation
cells. Zero overages in the finite Phase-3 grid are a stricter empirical gate,
not a consequence obtained by multiplying or misreading marginal guarantees.

Confidence is **medium** for the 1.10 efficacy ratio, **medium** for finite
multipliers below the engineering ceilings, and **high within the injected
bounded fixtures** for clean-removal divergence. No official score,
leaderboard gain, target hard-deadline proof or private-guardrail transfer is
predicted.

## 2. What is superseded and what remains valid

Iteration 7 (`research-log/146-hypothesis-iter-7-hcms24.md`) received a
scrutinized `RIGOROUS` review and therefore legitimately opened one controlled
run. That run is sealed at `experiments/runs/hcms24-c3-poc-v1` and is now an
**invalid, refuting antecedent**, not a positive result:

- its diagnostic HCMS/simple raw ratio was `1.391831525207`;
- frozen candidate-wise replay coverage was `187/189`, not 1.0;
- four primary method-cells crossed the generation budget;
- the safety validity condition failed; and
- the joint HCMS-24 prediction was therefore refuted regardless of raw.

PRAC-24 does not repair, rerun, relabel or average away those failures. It
retains only the HCMS 24/8/1 proposal-and-salvage structure as an inherited
efficacy candidate. It replaces both failed resource decisions and must earn a
new theory review and a new fresh experiment.

## 3. Why the old resource interpretation failed

The read-only diagnostic
`experiments/poc/rahcms_resource_diagnostic.py` binds and reconstructs the
sealed attempt. Its decisive observations are:

```text
hcms_candidate_coverage=187/189
hcms_aggregate_replay_overage_cells=0/36
primary_generation_overage_cells=4/144
post_first_no_fit_paths=420
post_first_no_fit_seconds=59.767362233368
later_recovery_candidates=3
later_recovery_raw=54.0
absorbing_hcms_to_best_simple_ratio=1.392971246006
primary_zero_interaction_paths_gt_point_one=44/84
```

Candidate-specific coverage was the wrong object for the competition endpoint:
the gateway gives one total replay deadline to the ordered returned-candidate
sequence. HCMS had two candidate-level misses but zero aggregate replay
overages in 36 primary cells. Conversely, retry after the first replay-ledger
no-fit spent 420 paths and 59.77 seconds for three one-message recoveries; all
four generation overages occurred in that tail. A fixed 0.1-second reserve was
also below 44 of 84 zero-interaction construction/reset paths.

These are retrospective design facts only. In particular, the absorbing raw
ratio `1.392971246006` is not a fresh effect estimate because the rule was
chosen after inspecting the invalid result.

## 4. Targeted literature result

Report `research-log/162-resource-risk-admission-literature.md` examines five
primary sources and fixes the following boundary:

1. Romano, Patterson and Candès, *Conformalized Quantile Regression* (NeurIPS
   2019), provides one-sided finite-sample **marginal** coverage under
   exchangeability, not conditional or hard real-time safety.
2. Angelopoulos et al., *Conformal Risk Control* (ICLR 2024), controls expected
   bounded monotone loss for exchangeable random loss functions, not zero
   failures in one deployed cell.
3. Angelopoulos, Barber and Bates, *Online conformal prediction with decaying
   step sizes* (ICML 2024), tolerates arbitrary dependence for retrospective
   average coverage; misses may still cluster inside the cell that matters.
4. Howard et al., *Time-uniform Chernoff bounds via nonnegative
   supermartingales* (2020), handles optional stopping only after a conditional
   `sub-psi` process is proved. No such target tail process is presently bound.
5. Shojaei, *Conformal Recovery-Deadline Certificates* (June 2026 preprint),
   gets hard safety from a separate verified backstop, not from its conformal
   quantile. Its statistical deadline is still marginal and exchangeability
   dependent.

The competition source supplies a decisive physical limit: attack code cannot
cancel an in-flight `RemoteEnv` operation. A controlled mock may empirically
validate a bounded return-ready gate; it cannot convert that fact into target
void-proofness. PRAC therefore uses statistical admission for utilization and
keeps the official target-confidence bridge closed.

## 5. Frozen artifacts and provenance

- normative config: `experiments/configs/prac24-c3-v1.json`, SHA-256
  `a9b31a47ba5e9c665bfb8480c3eab9d5b0e7d616af8b7b2a64bcade13415fe38`;
- deterministic author checker:
  `experiments/poc/prac24_phase2_reference_v1.py`, SHA-256
  `caf2ceb0801dea86ea17315305215011b203f9b4283f1a5f1650699dc88ccf59`;
- deterministic sealed-run diagnostic:
  `experiments/poc/rahcms_resource_diagnostic.py`, SHA-256
  `2b5d748f5550b58ee953afb1643cca0f94f581e9c144b3dabaf28a162667c8ad`;
- literature report: `research-log/162-resource-risk-admission-literature.md`,
  SHA-256
  `d42f11db54aa3a7d718234c69c64e00be39d0ddbb6fd44049a1a55d28a8767cf`;
- diagnosis and selection report:
  `research-log/163-rahcms-diagnosis-and-candidate-selection.md`, SHA-256
  `3e6fc56ca5bda8e682bff2ea41f983c51ef605c271bed3fc8018183ce17c38f1`.

The config additionally binds five authoritative SDK sources and nine
antecedent evidence artifacts. The incumbent competition attack remains SHA-256
`8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d`.
This hypothesis does not alter it.

## 6. Formal calibration object

Let profile family be `z`, ordinal execution slot be `o`, calibration master be
`j`, path be `p`, and retained eligible candidate index be `i`. A calibration
cell is one complete 16-path HCMS trace-capture cell in exact stratum `(z,o)`.
It uses the same proposal, exact-prefix salvage and monotone state as HCMS, but
no unknown `q` and no q-dependent replay admission. All retained eligible
candidates are actually replayed under the 120-second outer calibration clock.

For candidate `i`, let `a_i` be actual fresh replay cost and let

\[
\ell_i=1.25c_i+6.25c_{1,i}>0
\]

be the frozen base replay charge. Define

\[
A(k)=\sum_{i\le k}a_i,\qquad
L(k)=\sum_{i\le k}\ell_i,\qquad
Z^{R}=\max_{1\le k\le K}\frac{A(k)}{L(k)}.
\]

For atomic attempted path `p`, let `g_p` be elapsed time from one return-ready
checkpoint through construction, reset, indexed interactions, decision,
retained evidence, path publication and the next return-ready current-candidate
checkpoint. If its proposed prefix is `m_p`, let `b(m_p)` be the frozen positive
base duration from the config and define

\[
Z^{G}=\max_{1\le p\le P}\frac{g_p}{b(m_p)}.
\]

Any missing, timeout, censoring, malformed record or incomplete required cost
sets the affected stratum score to `+infinity`. It is never dropped, imputed or
retried.

For each exact `(z,o)` stratum there are `n=19` complete calibration masters.
For risk `alpha=0.05`, the split-conformal index is

\[
r=\left\lceil(n+1)(1-\alpha)\right\rceil
 =\lceil20\cdot0.95\rceil=19.
\]

`q_replay` and `q_generation` are the respective 19th order statistics. If the
required rank is not finite, the multiplier is infinity and PRAC abstains.
They are separate because replay and generation have different sampling and
physical meanings.

## 7. Conditional lemma and its exact scope

Assume the 19 complete calibration scores and one next latent 16-path HCMS
trace score are exchangeable within one fixed `(profile, position)` stratum,
with ties handled conservatively. Rank symmetry gives

\[
\Pr\{Z_{new}^{R}\le q_{replay}\}\ge0.95,
\qquad
\Pr\{Z_{new}^{G}\le q_{generation}\}\ge0.95.
\]

On the replay event, every prefix `k` with
`q_replay*L(k) <= 2.0` also has `A(k) <= 2.0`. Thus a sequentially selected
terminal prefix is covered without pretending its within-cell candidate rows
are independent.

On the generation event, if the controller starts a path only when remaining
generation time is at least `q_generation*b(m)`, that complete return-ready
atomic path finishes without crossing the controlled deadline. Because both
calibration and evaluation stop before path 17, evaluation observes only a
prefix of the same support on which the maximum was calibrated.

This is a **marginal**, per-next-trace statement over calibration and test. It
is not conditional on the realized calibration set, not simultaneous across 36
cells, not guaranteed for the fixed controls, and not valid under arbitrary
profile/position shift. Separate replay and generation 0.95 statements also do
not imply a joint 0.95 statement. The experiment reports their intersection
empirically and makes no family-wise theorem claim.

## 8. One shared evaluation kernel

All four primary methods must call one kernel for clocks, environment creation,
indexed trace attribution, exact-prefix eligibility, identity allocation,
base charges, q lookup, actual replay, stopping, evidence and artifact schema.
Method configuration is data.

```text
state <- method.initial_state
publish return-ready empty checkpoint
for path_index in 1..16:
    proposed <- method.proposal(state)
    if generation_remaining < method.generation_charge(proposed):
        return current candidates
    execute exactly one complete atomic path to next return-ready checkpoint
    retained <- method.salvage(exact indexed prefixes)
    if no permitted exact prefix:
        apply named monotone ineligible transition
        continue
    if method.replay_charge(candidates + retained) > 2.0:
        publish drop_ledger_no_fit
        if method.absorbing_no_fit: return current candidates
        apply named removal transition and continue
    allocate deterministic unique identities
    append retained candidate
    apply named monotone success transition
replay every returned candidate in order in fresh environments
publish all actual costs, scores, checkpoints, censoring and terminal status
publish COMPLETE last only after reload reconciliation and file hashes
```

For every `prac_*` method,
`generation_charge(m)=q_generation[z,o]*b(m)` and cumulative replay charge is
`q_replay[z,o]*L(k)`. `point_hcms_retry` instead uses both multipliers equal to
one, the old 0.1-second point reserve and retry after ledger no-fit. It is a
legacy bundled removal, not clean evidence for any one component.

## 9. Exact primary policies

| Method | Proposal and state | Salvage | Resource controller |
|---|---|---|---|
| `prac_hcms` | initialize 24; propose state; `state=min(state, returned)` | longest exact 24/8/1 | both q multipliers; absorbing no-fit |
| `prac_fixed8` | initialize 8; propose `min(8,state)` | longest exact 8/1 | same q lookup; absorbing no-fit |
| `prac_fixed24_no_salvage` | always 24; remain 24 after ineligible drop | exact 24 only | same q lookup; absorbing no-fit |
| `point_hcms_retry` | byte-identical HCMS proposal/salvage | longest exact 24/8/1 | q=1, old 0.1 reserve, retry after no-fit |

The calibrated HCMS theorem does not automatically transfer to the controls.
All methods must satisfy observed clocks and evidence gates for their comparison
to be valid. A control overage invalidates the affected constrained comparison;
it cannot be credited as a low score.

## 10. Fresh calibration and evaluation custody

For each of three profile families and each of 19 calibration masters, the
calibration runner executes four independent fresh HCMS trace-capture cells in
fixed ordinal slots `0,1,2,3`. Hence every `(profile, position)` stratum has 19
cells from distinct masters. The trace-capture clock is outer 120 seconds, not
the evaluation two-second claim; its purpose is complete risk measurement.

After a reviewed runner is admitted, calibration identities may be opened
once. The runner writes every score, including infinity, then seals the 12
profile-position pairs of replay/generation multipliers. Evaluation identities
and outputs remain unread until those multipliers and their hashes are fixed.
Calibration is never rerun because a q exceeds the engineering ceiling.

The fresh evaluation masters are `809`, `827`, `853`, disjoint from all 19
calibration masters and prior experiments. Each profile/master block uses four
Williams orders:

```text
prac_hcms, prac_fixed8, point_hcms_retry, prac_fixed24_no_salvage
prac_fixed8, prac_fixed24_no_salvage, prac_hcms, point_hcms_retry
prac_fixed24_no_salvage, point_hcms_retry, prac_fixed8, prac_hcms
point_hcms_retry, prac_hcms, prac_fixed24_no_salvage, prac_fixed8
```

Every method appears once in every position and every one of 12 directed
unequal predecessor pairs appears once. There are
`3 profiles * 3 masters * 4 orders = 36` primary cells per method and 144 total.

## 11. Profiles and scorer identity

The three primary controlled profiles are:

1. `steady_linear_prac_new`: compliant, 0.0075-second latency;
2. `reset_dominant_prac_new`: 0.043-second fixed plus 0.0008 per action; and
3. `immediate_cliff_prac_new`: exact through message 8, then context-limited,
   0.0015-second latency.

A returned prefix is eligible only when every message has exactly one correctly
attributed qualifying host event. Aggregate event counts cannot substitute for
the indexed vector. The raw identity `16*m+2` is used only when its full source
preconditions hold; otherwise actual scorer output is authoritative and the
identity check fails.

## 12. Four components, four clean removals

| Component | Single role | Prior bottleneck | Clean removal and decision |
|---|---|---|---|
| high-ceiling monotone salvage | amortize candidate-boundary cost while retaining exact 8/1 fallbacks | absorbing diagnostic HCMS/simple ratio `1.392971246006` | `prac_fixed8` and `prac_fixed24_no_salvage`; HCMS must be at least 1.10x the stronger valid control |
| complete-cell prefix envelope | convert a dependent replay sequence into one cumulative-prefix risk charge | candidate coverage `187/189` but aggregate HCMS overage `0/36`; safety prefix ratio `1.102552878986` | replay-spike fixture changes only q_replay from sealed q to 1; full stays within replay budget and removal crosses it |
| absorbing no-fit | terminate futile work immediately after replay saturation | 420 paths, 59.77 seconds, three recovered candidates | saturation-tail fixture changes only absorbing stop to retry; full attempts 0 tail paths, removal at least 3 and recovers 0 |
| atomic generation gate | reserve a complete return-ready path before starting | four overages; 44/84 zero-interaction paths exceed 0.1 second | long-setup fixture changes only q-generation gate to old 0.1 reserve; full truncates and removal starts then crosses |

The replay-spike construction is exact. After `q_replay` is sealed it exposes
10 exact one-message candidates. Each has
`c_returned=c_1=0.02666666666666667`, hence base charge
`(1.25+6.25)c_1=0.2`, and bounded actual replay cost `0.19*q_replay`. The full
controller admits `min(10,floor(10/q_replay))`, whose cumulative actual replay
is at most 1.9 seconds. The point removal admits all 10 and crosses two seconds
iff `q_replay>20/19`. If that precondition fails, the replay component is not
distinguished; no fixture constant may change.

The absorbing fixture makes the next exact one-message candidate fail the
sealed cumulative replay admission, then exposes exactly three further bounded
exact paths that also cannot fit. It terminates after the third removal-only
tail path. Full tail paths must be zero; removal tail paths three; both recover
zero returned candidates.

For the long-setup fixture let `u=q_generation*b(24)`. After a return-ready
prelude, controlled remaining time is `r=(u+0.1)/2`, and the next bounded setup
lasts `d=r+0.05`. When `u>0.1`, full PRAC refuses because `r<u`; the point
reserve starts because `r>0.1` and crosses because `d>r`. If `u<=0.1`, the
atomic component is not distinguished; no fixture constant may change.

All safety-fixture raw and candidates live in a separate namespace and are
mechanically excluded from efficacy aggregates.

## 13. Quantitative rationale and failure bands

The 1.10 materiality floor is deliberately far below the retrospective
1.39297 ratio, yet large enough to reject stateful complexity for a negligible
gain. The q ceilings are engineering feasibility gates, not claimed confidence
bounds: a larger finite multiplier may be statistically valid but too
conservative to serve the competition.

| Outcome | Decision |
|---|---|
| all validity gates pass; q ceilings pass; HCMS/simple ratio >=1.10; all four clean removals distinguished | confirm the narrow controlled four-component hypothesis; eligible only for a target-confidence bridge |
| valid and safe but ratio in `[1.00,1.10)` | reject HCMS complexity; prefer strongest simple PRAC policy |
| ratio below 1.00 | refute inherited HCMS efficacy |
| q is infinity or above either ceiling | abstain/reject competition feasibility; do not weaken alpha or tune bases |
| any PRAC generation/replay overage, missing cell, timeout, malformed artifact or identity failure | invalidate the joint result regardless of raw |
| a clean removal does not diverge as predicted | reject that component and the joint four-component claim |
| point legacy comparator happens to pass | report it; it does not rescue or refute a clean component by itself |

There is one calibration and one evaluation execution. No identity replacement,
threshold rewrite, q clipping, profile substitution or output-dependent retry
is permitted.

## 14. Validity domains and hard limits

1. **Source identity:** every config-bound SDK, evidence and incumbent attack
   hash must match.
2. **Exchangeability:** the finite-sample lemma is conditional on complete
   trace exchangeability within exact profile-position strata. Chosen authored
   seeds do not prove that assumption.
3. **Calibration circularity:** calibration uses no q-dependent admission. Any
   q use while generating its own calibration trajectories invalidates it.
4. **Support equality:** both calibration and evaluation stop before path 17.
   A longer evaluation stream is outside the calibrated maximum.
5. **Prefix coupling:** the evaluation HCMS stream before stopping must be a
   prefix of the same proposal/salvage process used by trace capture. Any
   q-dependent mutation before the terminal stop breaks the lemma.
6. **Censoring:** timeout, missingness and malformed cost become infinity. An
   available-case q is forbidden.
7. **Return-ready atomicity:** generation cost includes evidence and the next
   current-list return-ready checkpoint. Measuring interactions alone is
   invalid.
8. **Method symmetry:** all non-named behavior comes from one shared kernel.
9. **Replay endpoint:** actual ordered aggregate replay, not pooled individual
   coverage, decides controlled validity.
10. **Freshness:** evaluation outputs remain unread until calibration q values,
    code and artifact schemas are sealed.
11. **Completeness:** every one of 144 primary cells and every fixture outcome
    must reconcile from retained evidence before COMPLETE-last.
12. **No target hard-safety:** in-flight target RemoteEnv calls are not
    cancellable. Controlled bounded non-overage is not target void-proofness.
13. **No simultaneous theorem:** per-cell marginal coverage is not promoted to
    family-wise coverage; zero observed overages is reported descriptively.
14. **No official-score transfer:** the mock grid does not identify public or
    private leaderboard gain.

## 15. Fixed eight-category bias surface

1. **Selection bias.** PRAC and every threshold are motivated by a failed run.
   Fresh identities prevent literal reuse but authored profiles are not a
   population sample.
2. **Confounding.** Wall time, cache, scheduler and thermal state affect
   capacity. Williams balance handles ordinal position and first-order
   predecessor, not secular or higher-order drift.
3. **Assignment bias.** Calibration/evaluation masters and orders are fixed,
   not randomly drawn. Exact balance improves auditability but weakens
   population inference.
4. **Protocol deviation.** Any hash, path-cap, calibration, order, profile,
   method-interface, q, clock or fixture deviation invalidates the bundle.
5. **Missing data.** Missing, censored and timed-out calibration scores become
   infinity; missing evaluation cells invalidate. No available-case analysis.
6. **Measurement bias.** Wall time is noisy; base costs come from an invalid
   antecedent; source attribution may be wrong. Actual replay, indexed traces,
   return-ready checkpoints and adverse fixtures expose rather than erase it.
7. **Analysis flexibility.** Risks, ranks, bases, ceilings, profiles, methods,
   orders, removals and failure bands are frozen before implementation/output.
8. **Selective reporting.** Calibration scores, infinities, stopped paths,
   fixture failures, all primary cells and invalid status publish together.
   Safety raw cannot be promoted into efficacy.

## 16. Taxonomy, anti-stacking and alternatives

- opportunity: **Failure/Risk Gap**, secondary Resource Bottleneck;
- method paradigm: **Robustification**, secondary Formal Derivation;
- dominant operation: **replace**.

PRAC replaces the failed candidate-level point interpretation with a
complete-cell prefix-risk object and replaces retry-after-no-fit with an
absorbing state. It is not Bridge Opportunity x Synthesis/Unification.

The distinguishing predictions are component-specific: high pooled candidate
coverage may coexist with an unsafe accepted cumulative prefix; the prefix
envelope must separate those cases. A retry removal must consume post-no-fit
work without utility. A point-reserve removal must start a bounded setup the
atomic gate refuses. These are not entailed by merely stacking “conformal,”
“early stop” and “HCMS” labels.

Strong alternative explanations remain:

- base charges may correlate with costs without representing boundary/reset
  mechanics;
- q may be finite only because authored mock tails are light;
- the 19 fixed masters may not be exchangeable with the three evaluation
  masters;
- fixed 8 may retain nearly all useful score and win after q conservatism;
- the apparent HCMS gain may be deliberately encoded by one reset-heavy and one
  cliff profile;
- position balancing may not remove scheduler drift;
- safety fixtures may be construction truths with little target frequency; and
- real guardrails may fail before 8, recover nonmonotonically or have atomic
  latency tails outside controlled support.

The strongest objection is that no controlled mock can establish the target
atomic-cost tail required for a confident official deployment. This hypothesis
accepts that objection. Its purpose is to decide whether PRAC is a valid,
material mechanism worth carrying into a separately frozen target-confidence
bridge—not to bypass that bridge.

## 17. Official competition bridge remains closed

Even a confirmed Phase-3 result cannot mutate `experiments/attack.py` or launch
Kaggle by itself. Before target work, a separate task must specify:

- source-compliant scaling from two-second mocks to the 9000-second generation
  and per-model/guardrail replay phases;
- an explicit, non-void target atomic-tail assumption and evidence for it;
- incumbent fallback and expected benefit over the linked 69.570 submission;
- artifact parity between reviewed local bytes and a Kaggle commit; and
- every confidence gate in `PROBLEM.md`.

Submission remains contingent on confidence, not on authorization alone.

## 18. Author verification and next gate

Exact command:

```bash
comp/.venv/bin/python -I experiments/poc/prac24_phase2_reference_v1.py \
  --config experiments/configs/prac24-c3-v1.json
```

Expected output begins `prac24_phase2_author_check_v1=PASS` and includes:

```text
precursor_status=invalid_disclosed
diagnosis=retrospective_only
calibration_unit=complete_unbudgeted_hcms_trace_profile_position_stratum
calibration_controller=noncircular_trace_capture
calibration_cells_per_stratum=19
cell_risk_alpha=0.050000
order_statistic_rank=19
censoring=positive_infinity
risk_multipliers=separate_replay_generation
absorbing_no_fit=true
calibration_evaluation_path_cap=16
contribution_components=4
clean_component_removals=4
williams_orders=4
directed_predecessor_pairs=12
minimum_primary_ratio=1.100000
maximum_q_replay=1.250000
maximum_q_generation=3.500000
target_remote_cancellation=false
official_score_claim=withheld
attack_unchanged=true
phase3_artifacts=absent
review=not_dispatched
```

This artifact must be committed before review. A fresh sterile reviewer must
receive this full document, the canonical SciAgent mathematical-thinking,
bias-framework and idea-taxonomy references, reports 161--163, and the exact
scope of the marginal lemma.

Only a scrutinized `RIGOROUS` verdict can open Phase 3. Until then the Phase-3
runner, calibration/evaluation attempt directories, competition attack
mutation, Kaggle run and submission remain prohibited. Writing this hypothesis
does not spend a hypothesis-review round; Cycle-3 review usage remains `7/12`
until a later review task actually dispatches.
