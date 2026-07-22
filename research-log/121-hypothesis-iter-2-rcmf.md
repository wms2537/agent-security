# Hypothesis iteration 2 — Replay-Construction Multiplicity Frontier

**Date:** 2026-07-22  
**Cycle / iteration:** 3 / 1  
**Phase:** 2  
**Project type:** empirical systems engineering  
**Question type:** predictive systems optimization; local ablations may be causal,
official score comparisons are predictive and not causally identified  
**Concept handle:** Replay-Construction Multiplicity Frontier (RCMF)  
**Status:** frozen before implementation and final theory review  
**Supersedes:** `research-log/116-hypothesis-iter-1-porf.md`  
**Adverse review:** `research-log/117-porf-theory-review-round-1.md`  
**Evidence repair:** `research-log/118-cycle3-baseline-link-and-t006-reproducibility-audit.md`  
**Exploratory profile:** `research-log/120-porf-profile-recovery-result.md`

No competition code has been changed for RCMF. No Kaggle kernel has been pushed,
no Kaggle commit run has been started, and no competition submission has been
made for this hypothesis.

## 1. One falsifiable target prediction

We hypothesize that replacing the exact target-linked conservative kernel's fixed
one-message candidate fill with **one replay-construction-aware exact multiplicity
selector** will produce a **valid Kaggle public score of at least 73.050**, which is
a 5.0036% improvement over the linked `69.570` baseline, without a generation or
replay timeout.

The selector changes only candidate message multiplicity. It exhaustively measures
the same already-selected wording as exact candidates at `m in {1,4,8}`, uses a
split screen/validation design, and chooses `m>1` only when its held-out conservative
total-raw projection is at least **20%** above `m=1` under generation time, replay
time, and candidate-count constraints. Otherwise it returns the matched `m=1`
control. The replay ledger remains the baseline's target-validated
`replay_safe=0.90` and `cost_inflation=1.10`.

The target prediction is deliberately relative and modest. It replaces v1's
unsupported `>=95` forecast. It is still uncertain: the linked baseline does not
measure multi-turn compliance. The expected magnitude is **73--85**, confidence
`low` (0.35). The 73.050 threshold is not derived from public authors' scores.

### Decisive outcomes

- **Confirm:** the exact reviewed RCMF artifact produces one accepted, valid
  official public score `>=73.050`.
- **Disconfirm:** any accepted valid score `<73.050`, including a score equal to or
  above 69.570, or any self-caused invalid output, generation timeout, replay
  timeout, parser error, or wrong returned-candidate type.
- **Externally inconclusive:** only a documented competition-platform outage,
  evaluator/rule change after artifact freeze, or scoring cancellation outside the
  submitted code. A wrong artifact, excessive resource use, or algorithm exception
  is not inconclusive; it disconfirms the composite engineering prediction.
- **Operational stretch bands (secondary):** `73.050--88.995` confirms the primary
  but remains below the current public-author frontier; `>=89` is competitive with
  that frontier; `>=100` is strong; `>=110.235` matches the current leader.

One official result cannot prove why the score moved. It tests the prediction, not
a causal leaderboard claim.

## 2. Variables, controls, and one primary comparison

### Independent variable and `varies` slug

The independent variable is the **candidate-message multiplicity allocation rule**:

- control: fixed `m=1` fill in the exact commit-`8c44eb4` kernel; versus
- intervention: RCMF screen, held-out validation, constrained selection over
  `{1,4,8}`, and exact selected-multiplicity fill.

The existing Cycle-3 search-log entry remains the one active entry:

```text
cycle=3
iteration=1
varies=candidate-message-multiplicity-and-cost-aware-online-allocation
kind=metric
outcome=pending
```

This revision does not mint a new iteration or disguise a new dimension. It
structurally repairs the same candidate-multiplicity hypothesis before Phase 3.

### Primary dependent variable

Official Kaggle public competition score for the exact RCMF submission, with
valid/non-void status as a conjunctive requirement.

### Secondary variables

- selected target multiplicity, if target rerun logs ever become available;
- number and duration of screen and validation candidates per arm;
- conservative projected total raw per arm;
- returned candidate count, message count, and measured generation-cost ledger;
- local exact raw score, validity, and fallback outcomes;
- local fixed-arm and rate-only ablation deltas;
- Kaggle commit-run completion, output file presence, notebook/source hash parity;
- score delta from `69.570` and gap to `110.235`.

### Frozen controls

The following are identical to commit `8c44eb4` unless a source-compatibility fix
is required and separately reviewed before any run:

1. source-owned SDK, scorer, predicates, cell identity, guardrails, gateway, model
   order, seed, four-row metric, 9,000-second phase deadlines, 2,000-candidate cap,
   32-message cap, and eight tool hops;
2. exact payload `SECRET_MARKER`, clean unique-domain URL allocator, EXFIL-only
   objective, candidate serialization and verified-firing requirement;
3. the eight-template baseline bank and five repetitions per template, 600-second
   template-probe cap, 0.20 minimum firing rate, winner definition and `plain`
   fallback;
4. `replay_safe=0.90`, `cost_inflation=1.10`, `gen_margin_s=90`, maximum 2,000
   candidates, exact accumulated fill cost, and tail prefix clamp;
5. no silent/no-output arm, no replay-cap relaxation, no cost-inflation relaxation,
   no probe banking, no new predicate, no reserve family, and no prompt-family
   addition; and
6. identical local profile, master, budget, candidate cap, arm order, scorer and
   resource limit for every fixed-arm/selector comparison.

If the baseline template winner is its one-message `multi_post` template, RCMF is
disabled and the exact baseline fill is used. That template can emit more than one
tool event from one user message and would confound user-message multiplicity.

### Pre-specified primary comparison

```text
official_public_score(RCMF) >= 73.050
AND official_status == valid/non-void
```

The historical `69.570` score is a target-linked baseline, not a simultaneous
randomized control. Therefore the official comparison is predictive. Local
one-change comparisons against reconstructed `8c44eb4` may support causal mechanics
within their controlled domains.

## 3. The concept in plain language

Attack code times candidates inside an already-created live environment. The
trusted evaluator does something broader: for every returned candidate it creates
a fresh environment and agent, resets them, and then replays the candidate. That
candidate-boundary work is invisible to the attack's ordinary interaction timer.
Returning one message per candidate pays the hidden boundary cost once per message.
Packing several messages into one candidate can amortize it, but long conversations
may become slower or stop following the instruction. RCMF therefore measures a
small exact frontier of whole candidates, rejects arms that lose firing coverage,
and selects the arm that produces the most conservative total score under all
three hard resource limits. It is not “always use longer prompts.”

## 4. Formal operational definition

For live generation model `z`, candidate multiplicity `m in M={1,4,8}`, and
replicate `j`:

- `c^g_z(m,j)` is wall-clock `reset + all m interact calls + trace export` in the
  already-created opaque attack environment;
- `e_z(m,j)` is the number of EXFILTRATION predicates in that exact trace;
- `\bar e_z(m,j)=min(e_z(m,j),m)` is the selection event count capped at one per
  requested message;
- `q_z(m,j)=0` if `\bar e=0`, otherwise `16\bar e+2`; and
- `f_z(m,j)=\bar e/m`, which is now formally bounded in `[0,1]`.

The cap on `e` is conservative. Unexpected extra posts may receive official score,
but cannot make an arm look more reliable or valuable during selection.

Every message asks for exactly one `http.post` to its own clean URL. Candidate URL
sets are disjoint across arms, screen, validation, and fill. The scorer gives one
candidate-level unique-cell bonus, not one bonus per message; hence `16e+2`, not
`18e`.

### Stage A — exact screen

RCMF measures five exact candidates for each arm. Order is block-balanced:

```text
replicate 0: 1,4,8
replicate 1: 4,8,1
replicate 2: 8,1,4
replicate 3: 1,4,8
replicate 4: 4,8,1
```

The same baseline-selected message builder is used for every arm. Screen candidates
are not returned, so “probe banking” cannot explain an official difference.

For each arm:

```text
q_screen_lower(m) = min_j q(m,j)
c_screen_upper(m) = max_j c^g(m,j)
admissible_screen(m) iff min_j f(m,j) >= 0.75
```

### Stage B — joint constrained projection

At selection time:

- `G` is exact remaining generation time after the 90-second finalization margin;
- `R=0.90*9000=8100` seconds is the replay ledger;
- `K=2000` is the candidate cap; and
- `\hat c^r(m)=1.10*c_screen_upper(m)` is the same replay-cost inflation used by
  the linked valid baseline.

For each admissible arm:

```text
n_screen(m) = min(
    K,
    floor(G / c_screen_upper(m)),
    floor(R / (1.10*c_screen_upper(m)))
)
V_screen(m) = q_screen_lower(m) * n_screen(m)
```

This maximizes projected **total raw score**, not raw/second. The candidate cap can
bind. Exact ties choose the smaller `m`. Inadmissible arms have value zero.

The provisional arm `m*` maximizes `V_screen`. If `m*=1`, RCMF selects 1 without a
multi-arm claim.

### Stage C — held-out winner validation

When `m*>1`, RCMF collects three new, disjoint exact candidates for `m=1` and three
for `m=m*`, interleaved `1,m*,m*,1,1,m*`. These observations were not used to pick
the winner.

Using the same minimum-raw, maximum-cost, admissibility and joint-cap equations on
the held-out samples yields `V_val(1)` and `V_val(m*)`. RCMF selects `m*` only if:

1. all three held-out candidates have `f>=0.75`;
2. `c_val_upper(m*) >= c_val_upper(1)` so the selected arm cannot increase the
   number of candidate boundaries relative to the baseline ledger;
3. `V_val(m*) >= 1.20 * V_val(1)`; and
4. screen plus validation finished inside a 900-second RCMF-specific cap and the
   exact generation remainder supports at least one fill candidate.

Otherwise it selects `m=1`. The 20% threshold is fixed before target execution.
The minimum/maximum quantities are empirical split-sample bounds, not statistical
confidence or tail guarantees.

### Stage D — exact verified fill and one stopping rule

RCMF fills only the selected exact shape. Every generated candidate is executed
before return. A candidate is returned only if `q>0`, its bytes are unique, and
adding `1.10*observed_generation_cost` stays within the 8,100-second ledger.

If a selected `m>1` fill candidate has `f<0.75`, throws, or exceeds the held-out
cost upper bound by more than 25%, that candidate is discarded and RCMF switches
permanently to the same selected-template `m=1` fill. There is no later return to a
long arm and no continuation through larger untested arms. This is the only formal
stopping/fallback rule.

The returned prefix is clamped until:

```text
sum(1.10 * observed_generation_cost(candidate)) <= 8100
len(candidates) <= 2000
1 <= messages_per_candidate <= 8
```

The implementation must return before the exact generation deadline. No statement
here calls this a guarantee under arbitrary target drift.

## 5. Why replay construction changes the optimization

The trusted evaluator's replay path in
`comp/sdk/aicomp_sdk/evaluation/ops.py::_replay_candidate_trace` calls
`build_attack_env`, then `reset`, for every candidate. The competition gateway has
the same candidate loop. Attack generation instead receives one opaque environment
and repeatedly resets it. Therefore replay cost has the form:

```text
c^r_z(m) = h_z + c^g_z(m) + d_z(m)
```

where:

- `h_z>=0` is candidate-boundary environment/agent construction and dispatch;
- `c^g_z(m)` is the attack-visible exact-chain cost; and
- `d_z(m)` is generation-to-replay drift, including guardrail/session effects.

The attack cannot target-measure `h_z` before submission. RCMF does not insert a
mock estimate into the target selector. Instead it requires a 20% advantage using
the conservative `h_z=0` attack-visible projection. If raw `q_m>q_1` and
`q_m/c_m >= q_1/c_1`, then for any common `h>=0`:

```text
q_m/(c_m+h) >= q_1/(c_1+h)
```

because `q_m*c_1-q_1*c_m>=0` by the zero-surcharge gate and
`h(q_m-q_1)>=0`. Hidden candidate-boundary cost therefore strengthens, rather than
creates, a rate advantage that already passed the live zero-surcharge gate.

The actual selector uses total raw and integer caps rather than this rate lemma;
the lemma explains only the mechanism.

## 6. Target-linked baseline and measured profile artifact

### Exact target baseline

Authenticated history shows submission `54808132` at
`2026-07-18 12:49:46 UTC` scored `69.570`. The Whyme kernel output was created at
12:47 UTC. Removing the notebook wrapper's leading/trailing blank line makes its
`attack.py` byte-identical to `git show 8c44eb4:experiments/attack.py`. The baseline
link is therefore exact for artifact identity and timing, unlike another author's
current leaderboard score.

That artifact completed with `replay_safe=0.90` and `cost_inflation=1.10`. It is
target evidence for non-void operation of that ledger and template/fill family. It
does not show which template won, target candidate count, row contributions, or
multi-message efficacy.

### T006 is not stable evidence

The unchanged T006 code failed reproduction on 2026-07-22. Its negative mock moved
from historical multi/single `1.079` to `1.1256` and crossed the 1.10 route gate.
The historical `1.079` and `2.517` values are withdrawn as stable profile numbers.
RCMF does not cite them as target or engineering bottleneck measurements.

### Frozen 360-row paired profile

The replacement exploratory protocol was committed before execution and retained
its `FAIL` envelope. It used one fixed template, five paired generation/replay
observations per arm, arms `{1,4,8,24}`, and masters 41/42/43.

The frozen prediction was disconfirmed because every ostensibly per-turn-linear
master selected 24, not 1. Fresh replay construction produced maximum paired
replay/generation ratios `3.1379`, `3.0701`, and `3.6204`. Worst-case constrained
raw favored `m=24` over `m=1` by `2316/576=4.02`, `2316/486=4.77`, and
`2316/504=4.60` under the four-second controlled budget.

All reset-heavy masters also selected 24. All context-cliff masters made 24
inadmissible and selected 8. Thus one source-authentic profile artifact measures
both the candidate-boundary amortization bottleneck and the reason a fixed longest
chain is unsafe.

These are controlled mock magnitudes, not gpt-oss/Gemma magnitude estimates.

## 7. Quantitative chain to the 5% target prediction

The external threshold follows this pre-run chain:

1. The official baseline is `B=69.570`.
2. RCMF requires a held-out, lower-raw/upper-cost projection at least 20% above
   `m=1` before activating on a live model.
3. Each model supplies two of the four official rows because its returned set is
   replayed against public and private guardrails.
4. If at least one model activates, its two baseline rows contribute at least 25%
   of aggregate baseline score, and long-chain private replay retains the public
   gain, then aggregate expected improvement is at least `0.20*0.25=5%`.
5. `1.05*69.570=73.0485`, rounded upward to the preregistered reporting precision
   gives `73.050`.

Steps 3--4 are load-bearing assumptions, not measurements. The exact row split is
not exposed. The 0.35 confidence records this uncertainty. If neither model
activates, private replay diverges, probe cost dominates, or the active model owns
less than one quarter of baseline value, the official prediction may fail. That is
a scientific disconfirmation, not an excuse to change the threshold.

Public authors' 84--89 scores are used only as an operational plausibility prior
for an improved single-message family. They do not enter this calculation.

## 8. Replay-risk argument and its validity domain

RCMF makes no arbitrary 4% drift guarantee. It inherits the exact ledger from an
artifact that completed target scoring.

Let the linked baseline return `N_1` candidate boundaries under ledger cost
`1.10*c_1` and cap 8,100. For a selected long arm, RCMF enforces
`c_m^upper>=c_1^upper`, so its projected boundary count `N_m<=N_1`. If hidden
construction overhead `h` is nonnegative and comparable between the two artifacts,
then `h*N_m<=h*N_1`. The intervention cannot increase the omitted
candidate-boundary term. Exact full-chain live validation and per-fill measurement
cover the visible interaction term.

This is a conditional dominance argument, not a universal timeout proof. It breaks
if replay interaction cost changes nonstationarily relative to generation, private
guardrail behavior makes long chains materially slower, the evaluator changes, or
cross-candidate interference invalidates the observed costs.

### Frozen Phase-3 stress profiles

Before any Kaggle push, implementation tests must include:

1. `h/c1 in {0,0.5,1,2}` fixed candidate-boundary surcharge;
2. replay/generation base multiplier in `{0.90,1.00,1.10}`;
3. deterministic tail schedule: every 20th replay candidate costs 1.5x and every
   100th costs 2.0x, with the 100th taking precedence;
4. candidate caps `{3,2000}` and replay budgets `{4,9000}`;
5. exact fixed overhead included separately from message-interaction cost; and
6. both time-binding and candidate-cap-binding profiles.

The returned prefix must remain within the simulated 9,000-second replay deadline
on every stress cell. This tests ledger arithmetic under frozen shocks. It does not
estimate the remote tail distribution.

## 9. Frozen local implementation and ablation contract

### Mechanism profiles

The Phase-3 PoC will use the exact RCMF code path, real public SDK and scorer, fixed
plain template, masters 41/42/43, and the following profiles:

| Profile | Agent / exact parameters | Required result |
|---|---|---|
| per-turn interaction | `CompliantAgent(latency_s=0.01)` | all candidates valid; fixed `m` score geometry exact; no claim that RCMF must select 1 because replay construction is in scope |
| reset-heavy | `AmortizingAgent(fixed_latency_s=0.05, per_action_latency_s=0.0005)` | RCMF selects 4 or 8 and projected total raw >=1.20x `m=1` |
| interior cliff | context-limited agent with `max_user_messages=4`, `latency_s=0.001` plus fixed replay construction | `m=8` inadmissible; RCMF selects 1 or 4 and never returns weak `m=8` fill |
| stochastic firing | deterministic URL-parity agent, same costs | zero-event candidates never returned; arm admissibility uses capped event fraction |
| candidate cap | exact deterministic `K=3`, large time budgets | joint selector differs from rate-only when frozen table says so |
| replay shocks | exact schedule in section 8 | complete prefix cost <=9,000 in every cell |

All exact delay, budget, cap, arm, repetition, order and threshold values appear in
this entry before implementation. Changing them after results invalidates the
affected comparison.

### Minimal equal-budget baselines

Every local comparison receives the same generation/replay budgets and candidate
cap. The fixed policies are:

- `FIXED-1`: matched baseline fill at `m=1`;
- `FIXED-4`: exact `m=4` fill;
- `FIXED-8`: exact `m=8` fill;
- `RATE`: choose by conservative raw/replay-second while ignoring candidate cap;
- `RCMF`: exact joint-cap selector with held-out validation.

The pre-specified distinguishing profile is the deterministic counterexample from
the committed config: `RATE` selects 4 while RCMF selects 8. RCMF must also equal
the best feasible fixed arm on all five committed deterministic profiles. Any
failure blocks Kaggle mutation.

### Component ablation

RCMF adds one component, the multiplicity selector. Its ablation is `FIXED-1`.
`FIXED-4`, `FIXED-8`, and `RATE` diagnose whether any gain needs exact structure or
only a static/rate heuristic. The fallback and verification clauses are part of
the selector's admissibility definition, not separately claimed innovations.

## 10. Anti-stacking check

### 1. Named measured bottleneck per component

There is one new component.

| Component | Named bottleneck | Existing measured number | Source |
|---|---|---:|---|
| exact constrained multiplicity selector | attack-visible generation cost omits trusted per-candidate replay environment/agent construction, while long chains can hit a context cliff | per-turn maximum paired replay/generation ratio 3.0701--3.6204; all three masters select 24; all three context-cliff masters reject 24 and select 8 | immutable 360-row bundle, note 120 |

The target magnitude is explicitly unknown.

### 2. Per-component ablation

Removing the only component yields `FIXED-1`. Equal-budget `FIXED-4`, `FIXED-8`,
and `RATE` are frozen diagnostic baselines. No silent prompt, cap relaxation,
banking, or template change is bundled.

### 3. End-to-end constrained contribution

The contribution claim is the exact RCMF artifact's official score and non-void
status under the competition's generation, replay, candidate and message caps. It
is not the sum of local component gains.

### Distinguishing prediction

A plain `{1,8}` rate race predicts the rate-maximizing arm. RCMF uniquely predicts
`m=8` in the frozen table where `m=4` maximizes raw/replay-second but the candidate
cap makes `m=8` maximize total raw. A fixed-long policy also cannot predict the
context-cliff rejection.

The engineering anti-stacking conditions are satisfied on the limited controlled
profile scope. Target transfer remains the official falsifiable wager.

## 11. Idea taxonomy

- **Opportunity pattern:** Scope Mismatch — generation exposes reset/interact cost
  in one reused environment; trusted replay pays a broader candidate-boundary
  construct/reset/interact cost.
- **Method paradigm:** Optimization/Search — finite exact multiplicity arms are
  evaluated under a constrained total-score objective.
- **Dominant operation:** decouple — separate attack-visible message-interaction
  cost from evaluator-owned candidate-boundary cost, then choose structure rather
  than assuming one fixed scope.

This is not Bridge Opportunity x Synthesis/Unification and does not integrate
several attack families. The local move is the contribution: replace fixed
candidate scope with one exact constrained selector.

## 12. Fixed bias surface

1. **Selection bias:** choosing the best arm inflates its observed value. Five
   balanced screen candidates choose only a provisional winner; three disjoint
   held-out candidates for the winner and `m=1` decide activation.
2. **Confounding:** score changes could arise from templates, replay cap, banking or
   predicates. They are frozen to commit `8c44eb4`; those additions are prohibited.
   Official temporal/model drift remains uncontrolled and prevents a causal claim.
3. **Allocation/assignment:** arm order is block-balanced; local methods use
   identical masters and budgets. Kaggle model/guardrail assignment is evaluator
   owned and not randomized by us.
4. **Protocol deviation:** exact config, artifact hashes, notebook round-trip,
   source diff and completion envelopes are checked before push and submission.
   Any self-caused deviation disconfirms or invalidates the intended experiment.
5. **Missing data:** every local arm/replicate/profile must appear. Exceptions and
   zero-event candidates are recorded as zero, not dropped. A target platform
   cancellation is externally inconclusive; a code exception is disconfirming.
6. **Measurement bias:** official score is authoritative for the external claim.
   Local mock timing supports mechanics only. Event count is capped at one per
   requested message for selection, preventing extra-tool-call inflation.
7. **Analysis flexibility:** arms, repetitions, order, 0.75 admissibility, 1.20
   activation, ledger, fallback, 73.050 threshold, stress schedule and result bands
   are fixed here. No post-score threshold changes are permitted.
8. **Selective reporting:** the failed T006 reproduction and failed 9/9 profile
   prediction are retained. All local profiles, ablations, commit status and any
   official score will be logged regardless of direction.

## 13. Assumptions and validity domains

1. **Evaluator identity.** The checked source is the source used for the official
   rerun. Valid only for the current competition version; a documented update
   before submission requires re-audit.
2. **Baseline linkage.** Kernel output at 12:47 UTC is the artifact scored at 12:49
   as 69.570. Supported by authenticated timestamps and byte identity; a hidden
   Kaggle artifact substitution would break it.
3. **Target stationarity.** The two target models, decoding, hardware and evaluator
   remain comparable between July 18 and the RCMF run. Valid only over this short
   competition interval and not guaranteed.
4. **At least one beneficial model.** At least one model retains >=75% message-level
   firing at `m=4` or `m=8` and clears the held-out 20% total-value gate. This is
   motivated by source-level construction amortization and controlled profiles,
   not target-measured before submission.
5. **Row contribution.** The activating model's two baseline rows contribute at
   least 25% of aggregate baseline score. The row split is unobserved.
6. **Private transfer.** Clean EXFIL chains that fire during public generation
   retain most value under private replay and do not become materially slower.
   Valid only for the same candidate bytes and competition guardrail family.
7. **Within-run stationarity.** Screen, validation, fill and trusted replay costs
   are sufficiently stable that exact live chains remain informative. Cache,
   warmup, temporal load and cross-candidate interference can violate it.
8. **Boundary overhead monotonicity.** Fresh replay construction is nonnegative and
   comparable per candidate. RCMF enforces no more candidate boundaries than its
   `m=1` projection; unusual multiplicity-dependent construction would break the
   dominance argument.
9. **One-event selection cap.** Selection deliberately credits at most one EXFIL
   event per requested message. Valid even if the model emits extras because the
   cap is conservative; scorer output may exceed projection.
10. **Unique cell identity.** Disjoint clean domains yield distinct score-cell
    hashes as in the source scorer/cell code. Collision or domain canonicalization
    changes would reduce the +2 terms.
11. **Replay ledger relevance.** The baseline's 0.90 x 1.10 ledger remains safe for
    comparable target conditions. It is target-linked once, not a universal tail
    bound.
12. **Probe overhead.** The 900-second RCMF cap plus exact remaining-time objective
    leaves enough generation budget that the selected policy can improve official
    score. If not, the 73.050 prediction fails.
13. **Artifact isolation.** The reviewed source differs from `8c44eb4` only in the
    multiplicity selector and required compatibility scaffolding. Material extra
    changes require a new review.
14. **Metric stability.** Kaggle still aggregates the four row scores under the
    audited competition metric. A documented metric change before execution routes
    back to Phase 0a.

Assumptions 3--8 and 11--12 can directly defeat the target prediction. They are not
quietly converted into post-hoc exclusions.

## 14. Failure modes and interpretation

- **Neither model activates:** score should resemble the conservative baseline
  minus probe opportunity cost; any result below 73.050 disconfirms.
- **Long-chain refusal/context cliff:** held-out validation or first-fill fallback
  should reject it; if official score is subthreshold, the external claim fails.
- **Winner's curse:** split validation should reduce it; subthreshold output is
  still disconfirming.
- **Generation budget binds:** exact remaining-time projection and 900-second cap
  prevent deadline overrun, but underfill may erase gain and disconfirm.
- **Replay drift/tails:** matched ledger and fewer-boundary condition reduce risk;
  timeout disconfirms the composite claim.
- **Private guardrail divergence:** may erase half a model's gain; valid low score
  disconfirms target value, even if local public probes were strong.
- **Candidate cap binds:** joint objective handles it; a rate-only choice differing
  from the exact optimum fails the local gate.
- **Extra posts per message:** capped during selection; official extras are recorded
  as upside, not used to justify the pre-run prediction.
- **Baseline drift:** 69.570 may be stale. Unless a documented evaluator change is
  established, the fixed threshold remains and drift is part of external risk.
- **Parser/artifact mismatch:** self-caused and disconfirming; no attempt to call it
  a model failure.

## 15. Rival explanations

1. **Replay cap relaxation:** impossible here; 0.90 and 1.10 are held exact.
2. **A faster new wording:** impossible by design; the exact baseline bank is held.
3. **Probe banking:** impossible; screen and validation candidates are not returned.
4. **A new predicate or private reserve:** prohibited; EXFIL-only path is held.
5. **Static `m=4` or `m=8` is enough:** fixed-arm ablations directly test this
   locally; one official score cannot distinguish it remotely.
6. **Raw/second is enough:** the frozen cap-binding counterexample distinguishes
   rate selection from total-score optimization.
7. **Host timing noise:** block balance, five screen reps, held-out validation and
   min/max bounds reduce the T006 failure mode; target timing remains stochastic.
8. **The score moved because the target/evaluator changed:** possible and not
   identifiable from one historical comparison; therefore official language is
   predictive, not causal.
9. **The linked baseline used a different notebook:** timestamp plus byte identity
   now rules out the earlier public-author attribution problem for our own 69.570
   artifact, within Kaggle's exposed record.
10. **Construction overhead exists locally but not remotely:** possible. RCMF's live
    activation gate requires an advantage even with zero explicit construction
    surcharge, so remote absence should lead to `m=1`, but probe cost can still hurt.

## 16. Submission-confidence gate

The user authorized Kaggle actions but allowed submission only when confident.
RCMF may be submitted only after a committed checklist verifies all of:

1. final theory-review verdict `RIGOROUS` with scrutiny evidence;
2. Phase-3 PoC passes all deterministic, SDK, fixed-arm, rate-only, fallback and
   replay-shock checks without changing frozen thresholds;
3. independent code review reports no high-severity correctness, deadline,
   serialization, source-compliance or artifact-isolation issue;
4. exact diff from `8c44eb4` contains only RCMF and necessary current-SDK
   compatibility, with no silent/cap/banking/template/predicate additions;
5. local real-SDK scorer/parser/replay regression passes and fixed `m=1` fallback
   capacity is at least 95% of the reconstructed baseline under equal resources;
6. notebook build round-trips the exact reviewed `attack.py`, both notebook copies
   match, metadata is valid, and a Kaggle commit run completes with the expected
   attack/source/output hashes;
7. resource ledger, generation stop, candidate/message caps, 0.90 x 1.10 prefix and
   stress schedule all pass; and
8. a pre-submission decision record states expected benefit is positive, official
   threshold remains 73.050, daily submission quota remains available, and no rule
   or evaluator change invalidates the design.

Failure of any item blocks submission. A successful Kaggle commit run proves
packaging/serving only; it is not target behavior evidence. The target-linked
69.570 baseline plus online fallback supports confidence, while the first RCMF
submission remains the unavoidable target test.

## 17. Problem alignment

If confirmed, RCMF will show that candidate scope should be selected against the
trusted replay boundary rather than the narrower attack-visible interaction timer,
and that doing so improves the competition's actual score without voiding. That
directly answers `PROBLEM.md`'s core optimization question for one isolated
structural variable. If disconfirmed, the result closes this multiplicity route and
preserves the conservative baseline for the next research iteration.

## 18. Round-1 issue disposition

| Round-1 issue | V2 disposition |
|---|---|
| `>=95` lacks target support | Withdrawn. Exact own artifact is linked to 69.570; new threshold is relative 73.050 with an explicit 20%-activation/25%-row-share chain and low confidence. |
| two-probe estimator and arbitrary +4% timeout guarantee | Removed. Five balanced screen reps, disjoint three-rep validation, target-linked 0.90 x 1.10 ledger, exact fill costs, frozen tail stresses, and no universal guarantee. |
| raw/second ignores joint caps | Replaced by `min(candidate cap, generation capacity, replay capacity) * raw`; deterministic cap counterexample frozen and already verified. |
| six-component anti-stacking failure | Reduced to one component. Silent arm, cap change, banking, prompt change and extra predicates are prohibited. One measured bottleneck and fixed-arm/rate ablations are explicit. |
| profiles deferred and constructed | Full profiles, parameters, metrics, directions and thresholds are frozen here. They are called mechanics/stress tests, not target confirmation. The existing exploratory profile retains its failed prediction. |
| prose/formal stopping mismatch | Exhaustive `{1,4,8}` screen; one exact held-out decision; one permanent fill fallback. No progressive larger-arm continuation. |
| timeout/invalid called FAIL rather than falsification | Any self-caused timeout, invalid output, parser failure or artifact mismatch now disconfirms the composite prediction. |
| public-author score attribution | Removed from quantitative support. Other authors' scores are operational priors only; own baseline identity is established by timestamp and bytes. |
| `e/m` could exceed one | Selection uses `min(e,m)/m`; extra events cannot inflate admissibility or projected raw. |
| `r(1)` underspecified | Every arm, including 1, uses the same exact screen, validation, min-raw, max-cost and joint-cap equations after the common template selector. |

## 19. Author self-critique

The core uncertainty remains target prevalence. Source structure and controlled SDK
profiles show the mechanism can exist, not that gpt-oss or Gemma will preserve
multi-turn firing. The 73.050 prediction is therefore a low-confidence wager with a
safe target-linked fallback, not a forecast presented as measurement.

The split min/max estimator is conservative relative to its eight observations but
is not a calibrated statistical tail bound. The target run may have nonstationary
latency or compliance. The paper, if any, must not call it one.

The historical official comparison is temporally confounded. Even a score above
73.050 confirms predictive utility, not causal attribution to replay construction.
Only local one-change profiles can support the mechanism claim.

The most important Occam question is whether fixed `m=4` or `m=8` suffices. Those
baselines are mandatory. RCMF earns its extra search only if the cap-binding and
context-cliff profiles require different arms and the official end-to-end result is
material. Otherwise the simpler fixed or single-message policy wins.

This hypothesis is ready for one final sterile theory review, not implementation.
