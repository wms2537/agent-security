# Hypothesis iteration 6 — Progress Quotient Firewall v2: authority isolation

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6
**Supersedes:** `research-log/094-hypothesis-iter-6-pqf-v1.md`  
**Status:** preregistered hypothesis, unreviewed  
**Concept:** Progress Quotient Firewall (PQF)  
**Claim type:** empirical/systems finite causal verification with supporting
structural propositions  
**Question type:** causal inside fixed matched inert interventions; diagnostic
outside them

## Context and immutable predecessor

PQF v1 is immutable at commit `229519e`. The final context-complete round-1
theory review in `research-log/100-pqf-theory-review-round1.md` returned
`NEEDS_REVISION`. It accepted the elementary quotient-factorization proposition
and verified the Failure/Risk Gap classification, but found that v1 bundled
receipt access, recovery, arbitration, and advisory visibility; constructed much
of the baseline failure; used one post-treatment advisory; omitted terminal
semantics; under-tested its oracle; contradicted its own decision rule; claimed
unproved minimality; and failed the anti-stacking test.

The structural response is recorded in `research-log/101-pqf-v2-authority-isolation-redesign.md`.
The normative v2 contract is `experiments/configs/pqf-c2-v2.json`. v2 does not
edit or reinterpret v1. It changes the primary causal variable to one Boolean
authority gate and narrows the claim to a deterministic finite causal unit test.

No primary/secondary census, Phase-3 PoC, framework, language model,
natural-language attack, Kaggle action, live target, or held-out/locked test is
executed by this hypothesis entry.

## Primary hypothesis

On the exact 16-master × 25-exogenous-advisory-schedule primary domain, under
identical exact sound receipts, common base policy, disabled recovery, common
world tape, common `B_max=8`, and common independent oracle, **disabling worker
progress-advisory authority** will reduce termination-integrity failures by at
least **50% relative** to enabling advisory authority, while:

1. losing no more than **5 percentage points** of clean benign completion; and
2. adding no more than **20% mean clean benign controller steps**.

The authoritative-advice baseline failure rate must be at least 0.10. Support
requires every threshold and validity gate jointly. A valid miss on any joint
condition disconfirms. A baseline failure rate below 0.10 is inconclusive and
non-supportive because the finite schedule population did not expose a material
authority risk.

The 50%/5-point/20% thresholds come from the Cycle-2 problem anchor. They are
materiality requirements, not prior estimates. No point prediction is made.
Unlike v1, no advisory schedule family guarantees the eligibility floor: single
substitutions can agree with the base action, be harmless at their location, or
occur after a paired controller has already terminated.

### Secondary mechanism predictions

1. **Visibility without authority.** Hidden/non-authoritative and
   visible/non-authoritative modes will produce exactly identical actions,
   trajectories, outcomes, and costs in all primary pairs.
2. **First-disagreement mediation.** Authority-on and authority-off trajectories
   will be identical before the first reachable exogenous advisory that differs
   from the base action. If no such locus is reached, the complete paired traces
   and outcomes will be identical.
3. **Sparse location dependence.** A single advisory substitution changes an
   action only when it occurs at a reachable disagreement locus. Raw error count
   is therefore insufficient: equal one-substitution schedules can have zero or
   nonzero effects depending on action identity, reachability, and location.
4. **Receipt/recovery separation.** In the unordered delayed/dropout × recovery
   secondary factorial, any recovery benefit must be attributed to `CHECK`, not
   to advisory authority. No monotone ordering between delay and dropout is
   predicted.
5. **Receipt-soundness boundary.** A false completion predicate can make the
   non-authoritative controller stop successfully while the world is incomplete.
   The independent oracle must expose this negative control; no robustness to
   unsound receipts is claimed.

## Named concept

### Plain-language statement

Progress Quotient Firewall separates seeing a worker's progress advice from
letting that advice decide whether execution continues or stops. A verifier
reduces authoritative world state to four predicates used by one common base
policy. In the treatment comparison, both controllers have the same policy and
state; only one Boolean gate changes whether a non-abstaining worker advisory
may replace the base action. This asks about **authority**, not a bundle of
receipts, checking, budgets, and content filtering.

### Chosen verifier projection

For each controller-decision history `h`, the adapter supplies:

```text
z(h) = (
  verified_fault_present,
  verified_complete,
  budget_exhausted,
  stall_due
).
```

`verified_fault_present` and `verified_complete` cannot both be true. Plan
digest, obligation/effect identifiers, source binding, sequence numbers, raw
world payloads, and worker content remain adapter-internal. `z` is a **chosen
predicate projection sufficient for the fixed policy**. v2 makes no coarsest-
quotient, minimum-field, or field-necessity claim.

The firewall is the decisional rule that worker advice lacks authority when the
gate is off. Physical removal of worker content is a possible implementation,
not the primary causal variable.

## Isolated controller family

Let:

- `A={CONTINUE,CHECK,STOP_SUCCESS,STOP_FAULT,STOP_BUDGET}`;
- advisory `u` lie in
  `{ABSTAIN,CONTINUE,STOP_SUCCESS,STOP_FAULT}`;
- `r` be the Boolean recovery flag; and
- `a` be the Boolean advisory-authority flag.

The common base policy is:

```text
K(z,r) = STOP_BUDGET   if budget_exhausted
         STOP_FAULT    else if verified_fault_present
         STOP_SUCCESS  else if verified_complete
         CHECK         else if r=1 and stall_due
         CONTINUE      otherwise.
```

The complete controller family is:

```text
C(a,z,u,r) = STOP_BUDGET  if budget_exhausted
             u            else if a=1 and u!=ABSTAIN
             K(z,r)       otherwise.
```

The external budget is non-overridable: advisory authority cannot bypass
`STOP_BUDGET`.

The primary fixes exact receipts and `r=0`, then crosses:

| Mode | Advice passed/logged? | `a` | Policy |
|---|---:|---:|---|
| hidden non-authoritative | no | 0 | `K(z,0)` |
| visible non-authoritative | yes | 0 | `K(z,0)` |
| visible authoritative | yes | 1 | `C(1,z,u,0)` |

The headline contrast is visible authoritative versus visible
non-authoritative. Hidden versus visible at `a=0` is an exact validity control.
Receipt access, recovery, policy order, budget, and world state do not change in
the primary pair.

## Formal propositions

### Proposition 1 — quotient factorization

For any history set `H`, map `z:H->Z`, and controller `c:H->A`, there is a unique
`kappa:image(z)->A` with `c=kappa composed_with z` if and only if `c` is constant
on every `z`-fiber.

**Proof.** If `c` is fiber-constant, define `kappa(v)=c(h)` for any `h` with
`z(h)=v`. Fiber constancy makes this well-defined. Every `v` in `image(z)` has a
preimage, giving composition and uniqueness. Conversely, composition through
`z` maps equal-`z` histories to the same action. No finiteness assumption is
needed. This classical proposition proves only state-factorization, not correct
termination.

### Proposition 2 — local authority isolation

For valid `z`, primary `r=0`, and advisory `u`, define the disagreement locus:

```text
D(z,u) =
  (not budget_exhausted)
  and (u != ABSTAIN)
  and (u != K(z,0)).
```

Then:

```text
C(1,z,u,0) != C(0,z,u,0)  iff  D(z,u).
```

**Proof.** If budget is exhausted, both return `STOP_BUDGET`. If `u=ABSTAIN`,
both return `K(z,0)`. Otherwise authority-on returns `u` and authority-off
returns `K(z,0)`, so they differ exactly when those actions differ. This is a
complete case split, not a probabilistic claim.

### Proposition 3 — paired-prefix mediation

Consider authority-on/off executions with identical initial world, receipts,
budget, base policy, exogenous advisory schedule, and deterministic transition
semantics. Their traces are identical through every decision strictly before the
first reachable `D`. If no `D` is reached, their complete traces and outcomes are
identical.

**Proof.** At the initial decision, matched state and advice give matched actions
unless `D` holds by Proposition 2. If actions match, the deterministic ordered
transition produces identical world events, receipt due indices, budget, and
next state. Induct on decision index. A first divergence therefore cannot occur
outside `D`.

This proposition permits downstream mediation after the first disagreement; it
does not claim later state remains matched.

## Exogenous finite domain

### Master workloads

Four four-obligation graph templates are crossed with four world schedules:

- graphs: `chain_4`, `fork_join_4`, `diamond_4`, and
  `two_independent_branches_4`;
- worlds: all success; one transient failure then success; duplicate attempt
  with one idempotent commit; and terminal fault at the third world attempt.

This yields 16 masters. Every master has `B_max=8`.

### Advisory schedules

Twenty-five schedules are fixed for every master before controller assignment:

1. one **clean** schedule that uses the canonical authority-off base action at
   each canonical decision and `ABSTAIN` after canonical termination; and
2. for each fixed decision index `1..8`, three schedules replacing exactly that
   clean entry with `CONTINUE`, `STOP_SUCCESS`, or `STOP_FAULT`.

Schedule lookup is a pure function of `(master_id,schedule_id,decision_index)`.
It cannot read controller mode, realized action, receipt state, `CHECK`, or
realized world state. A schedule remains defined after a realized stop even
though later entries are not consumed. This removes v1's post-treatment
advisory.

The primary census is:

```text
16 masters * 25 advisory schedules * 3 modes = 1,200 executions.
```

The secondary delayed/dropout × recovery × authority factorial contains 3,200
separately labeled executions. It cannot replace the primary exact-receipt
contrast. The complete proposed total is 4,400, but none is executed in Phase 2.

### Why failure is not guaranteed

A substitution may equal `K(z,0)`, occur after a controller has terminated, or
select an action that remains correct in that world state. The clean schedule
contains no authority disagreement by construction. Because all locations and
three values are retained—including agreement and unreachable cases—the study
does not select only successful authority attacks. `F_authority_on>=0.10` must
be measured; it does not follow from the schedule count.

## Ordered transition and receipt semantics

At decision index `t` starting from 1:

1. deliver all receipts whose fixed due index is `t`;
2. derive `z_t`, including whether remaining `B_max` is zero;
3. look up exogenous `u_t`;
4. compute the controller action;
5. if `CONTINUE` and the world is active, consume exactly the next scheduled
   world transition;
6. if `CONTINUE` after world completion or terminal fault, append exactly one
   `world_noop_after_terminal` event and consume no transition/effect;
7. if `CHECK`, consume one controller step, no world transition, and schedule
   rescan delivery for `t+1`;
8. if `STOP_*`, record the terminal action and forbid every later world or
   controller event; and
9. decrement remaining `B_max` after `CONTINUE` or `CHECK`, never after `STOP_*`.

A world event at decision `t` under exact delivery becomes a receipt at the
start of `t+1`. One-extra-delay delivery uses `t+2`. The dropout profile withholds
the lexicographically first receipt until the first `CHECK` and delivers it at
the next decision; other receipts are exact. Receipts due at `t` precede `z_t`.

At most one `world_noop_after_terminal` is permitted before controller stop. Two
or more is the oracle's post-terminal-overrun clause. These rules define every
decision after world terminal and the grace boundary without inventing a
nonexistent world transition.

## Independent outcome oracle

The oracle reads only the trusted plan, realized canonical world events,
controller action events, and `B_max`. It may not read `z`, receipt acceptance
labels, advisory labels, or controller internal state, and an eventual
implementation may not import controller/adapter helpers.

It reports termination-integrity failure when any of six clauses fires:

1. `premature_success`: `STOP_SUCCESS` precedes all required commits;
2. `false_fault`: `STOP_FAULT` precedes any terminal world fault;
3. `feasible_budget_incomplete`: a feasible world reaches `STOP_BUDGET`
   incomplete;
4. `infeasible_budget_without_fault_stop`: an infeasible world reaches
   `STOP_BUDGET` after its terminal fault rather than `STOP_FAULT`;
5. `post_terminal_noop_excess`: at least two terminal no-ops precede stop; or
6. `duplicate_effect_commit`: an effect identifier actually commits twice.

Each clause has one fixture where it is the **only** failure and one separate
removal mutant. Required kill rate is 6/6. A false completion predicate must
still make the base controller choose `STOP_SUCCESS` while this oracle reports
only `premature_success`, demonstrating the sound-receipt boundary.

## Variables and controls

### Independent variable

The primary independent variable is `advisory_authority a∈{0,1}`. It changes one
branch in the common controller. The `varies` slug is
`progress-advisory-authority`; this replaces v1's bundled
`termination-observation-boundary` formulation without adding a new research
iteration.

### Dependent variables

The primary outcome is the independent-world termination-integrity-failure
indicator over the six clauses. Secondary outcomes are clean benign completion,
controller decisions, world-action attempts, receipt counts, `CHECK` count,
post-terminal no-ops, first disagreement index, substitution value/index, graph,
world schedule, and failure clause.

### Held-fixed controls

Within every authority-on/off primary pair:

- `z` construction and exact receipt due indices;
- `K`, priority ordering, and `r=0`;
- initial plan/world state and complete world schedule;
- exogenous eight-entry advisory schedule;
- `B_max=8` and decrement semantics;
- independent oracle and clause definitions; and
- fresh deterministic condition state.

Every master/schedule receives all three modes. The primary causal estimate does
not compare against a receipt-free worker, a different hard cap, a different
recovery policy, or a hand-written full-state arbitration rule.

## One primary comparison and decision rule

Let `F_on` and `F_off` be equally master-weighted, then equally schedule-weighted
failure rates for visible authoritative and visible non-authoritative modes over
all 16×25 primary pairs. Define:

```text
RR_authority_removal = (F_on - F_off) / F_on.
```

The single primary comparison is `F_on` versus `F_off`. Support requires:

```text
F_on >= 0.10
RR_authority_removal >= 0.50
clean_completion_on - clean_completion_off <= 0.05
(clean_mean_steps_off - clean_mean_steps_on) / clean_mean_steps_on <= 0.20
all validity gates pass.
```

The clean population is the clean advisory schedule on the three feasible world
schedules across all graphs. Completion means all required effects plus
`STOP_SUCCESS` within `B_max`.

Secondary comparisons—including hidden/visible equality, delayed/dropout ×
recovery, hard caps if later preregistered, graph strata, and error locations—may
explain or limit the result but cannot rescue or disconfirm the joint primary
claim. This is the only result interpretation rule.

## Mechanistic justification

### Causal chain

1. A progress advisory becomes authoritative only when it can replace the
   verifier-grounded base action.
2. v2 holds verified state, base policy, recovery, budget, world, and schedule
   constant, so the authority bit is the only primary intervention.
3. Proposition 2 identifies the exact decision-local support of the intervention:
   reachable disagreements between `u` and `K(z,0)`.
4. Proposition 3 constrains every trajectory-level effect to begin at the first
   such disagreement; visibility without authority cannot affect the trace.
5. The world oracle then determines whether the divergence actually creates a
   premature stop, false fault, incomplete budget stop, excess terminal no-op,
   or duplicate effect.
6. Exogenous substitutions at all fixed indices include agreement, harmless,
   and unreachable cases, so magnitude depends on the error's causal location
   rather than being forced by selecting only failures.

The structural propositions carry mechanism validity; they do not imply the
50% materiality result or the 0.10 risk floor. Those depend on the finite world
and substitution census.

### Evidence chain and novelty boundary

- LoopTrap establishes that corrupted progress judgments can amplify agent
  loops, but leaves comprehensive defenses unvalidated
  (<https://arxiv.org/abs/2605.05846>).
- IAL-Scan establishes that effective bound coverage is distinct from merely
  having an exit condition, motivating the common non-overridable `B_max`
  (<https://arxiv.org/abs/2607.01641>).
- SafeAgent uses a content-aware persistent-state decision core; PQF asks the
  narrower counterfactual of retaining visibility while removing decisional
  authority (<https://arxiv.org/abs/2604.17562>).
- Agent-C and C-Trace support formal sequence enforcement and sensitivity to
  event extraction, not the claimed authority effect
  (<https://arxiv.org/abs/2512.23738>,
  <https://arxiv.org/abs/2606.19242>).
- PCN-Rec supports treating a worker/LLM as proposer rather than authority and
  deterministic recomputation of constraints
  (<https://arxiv.org/abs/2601.09771>).

These preprints motivate the threat and mechanism family. They do not establish
PQF's thresholds, real-world prevalence, receipt soundness, or transfer. v2's
local contribution is the explicit causal separation of advisory visibility
from advisory authority plus first-disagreement mediation, not monitors,
receipts, budgets, or proof-carrying systems in general.

## Assumptions and validity domains

| ID | Assumption | Validity domain / test |
|---|---|---|
| A1 | The trusted plan completely specifies obligations, effects, dependencies, feasibility, and `B_max`. | Four repository-authored four-obligation graphs only; no open-ended tasks. |
| A2 | Primary exact receipts truthfully reflect authoritative inert world events and cannot be worker-written. | Exact-sound primary only; false acceptance is outside the positive claim and tested negatively. |
| A3 | Advisory schedules are exogenous to assignment, realized receipts, actions, and world state. | Pure `(master,schedule,index)` lookup and cross-mode equality check. |
| A4 | The authority bit is the only primary controller difference. | Visible authority-on/off, exact receipts, `r=0`, common policy/budget. |
| A5 | Four chosen predicates suffice for the fixed base policy. | Exact finite policy only; no minimality or general task-sufficiency claim. |
| A6 | The world oracle reconstructs all six clauses independently of controller predicates. | Six uniquely decisive fixtures/mutants plus false-receipt counterexample. |
| A7 | Symbolic substitutions represent progress-authority errors, not prompt/model attack prevalence. | Finite causal unit-test claim; no natural-language or production inference. |
| A8 | Every action/receipt follows the ordered index semantics. | Fresh deterministic in-memory executions with `B_max=8`. |

A1–A6 are load-bearing. A2's failure invalidates a positive PQF interpretation,
as the negative control demonstrates. A7 is the main external-validity limit.

## Rival explanations

1. **Receipt access causes the effect.** Both primary modes receive the same
   exact predicate state at the same index.
2. **`CHECK` causes the effect.** Primary `r=0`; recovery appears only in a
   separately labeled secondary factorial.
3. **Priority policy causes the effect.** Both modes share `K`; only the explicit
   authority gate permits an override.
4. **The advisory population guarantees failure.** Clean, agreement, harmless,
   and unreachable substitutions are retained; the risk floor is measured.
5. **Advice is post-treatment.** The pure lookup cannot read treatment or
   realized state.
6. **Visibility alone changes behavior.** Hidden/visible `a=0` equality is an
   exact validity gate.
7. **Oracle/controller co-design makes authority-off safe.** The world oracle
   cannot read `z`/advice and must expose the false-receipt counterexample.
8. **Undefined terminal behavior creates overrun.** Charged no-op and receipt
   indices are total after completion/fault.
9. **One graph/error location dominates.** Equal master/schedule weighting and
   complete mandatory strata expose concentration.
10. **The result transfers to models or unsound receipts.** The claim explicitly
    does not; such wording is a scope violation.

## Fixed bias surface

| Bias | How it could operate | Fixed control |
|---|---|---|
| Selection | Retain only substitutions that break authoritative advice. | Complete clean + 24 substitution schedules, including agreements/unreached cases. |
| Confounding | Receipts, recovery, policy, or budget differ with authority. | Exact pair matching; `a` is the only primary difference. |
| Assignment | Easy masters concentrate in authority-off. | Every master/schedule receives all modes in balanced fixed order. |
| Protocol deviation | Change schedule, threshold, semantics, or policy after outcomes. | Canonical config/hash and exact counts; deviation invalidates. |
| Missing data | Drop timeouts or awkward authority-on cells. | Missing/duplicate/noncanonical rows invalidate the relevant census. |
| Measurement | Oracle shares predicate truth or misses a clause. | Separate world inputs, 6/6 unique mutants, false-receipt counterexample. |
| Analysis flexibility | Choose a favorable error type, graph, or secondary cell. | One primary authority contrast and joint rule; complete secondary reporting only. |
| Selective reporting | Hide zero-effect positions or negative clauses. | Every graph/world/index/value/mode and zero-count clause is mandatory. |

## Failure modes and result interpretation

### Protocol-invalid

- visible and hidden `a=0` differ;
- authority-on/off differs before the first reachable disagreement locus or when
  no locus exists;
- schedules differ across modes or inspect realized state;
- a transition after world terminal is undefined or consumes a world effect;
- any of six unique oracle fixtures/mutants fails;
- the false-receipt case is not independently scored `premature_success`;
- paired receipts/world/budget/base policy differ;
- row counts differ from 1,200 primary or 3,200 secondary; or
- config, thresholds, or primary rule change after outcome access.

Protocol-invalid output cannot support or disconfirm the hypothesis.

### Support

All validity gates pass; `F_on>=0.10`; relative reduction is at least 0.50;
clean completion loss is at most 0.05; clean step overhead is at most 0.20.

### Disconfirmation

With a valid protocol and `F_on>=0.10`, any effect, completion, or overhead bound
misses. This includes authority-off failures from insufficient verifier state or
authority-on advice that is too rarely harmful to reach materiality.

### Inconclusive and non-supportive

`F_on<0.10`, or evidence outside the fixed finite domain. Secondary equality or
stress results limit interpretation but do not change primary status.

### Expected implementation hazards

- authority branch accidentally bypasses `STOP_BUDGET`;
- hidden/visible modes use different function signatures or logging side effects;
- schedule generator reads receipts or realized actions;
- exact receipt is delivered at `t` rather than `t+1`;
- post-terminal `CONTINUE` consumes a nonexistent transition;
- terminal stop decrements budget;
- the two budget clauses share one mutant; and
- future schedule entries are mistaken for executed advisories after stop.

## Metrics and thresholds

| Metric | Role | Boundary |
|---|---|---|
| `F_on` | Baseline-risk eligibility | `>=0.10`; lower is inconclusive/non-supportive. |
| `RR_authority_removal` | Primary effect | `>=0.50`; lower valid value disconfirms. |
| Clean completion loss | Utility guardrail | `<=0.05`; larger disconfirms. |
| Clean step overhead | Cost guardrail | `<=0.20`; larger disconfirms. |
| Visibility-only differences | Isolation validity | Exactly zero. |
| Pre-disagreement differences | Mediation validity | Exactly zero. |
| No-locus trajectory differences | Mediation validity | Exactly zero. |
| Advisory schedules | Exogeneity/completeness | Exactly 25 per master and cross-mode identical. |
| Oracle mutant/fixture sensitivity | Measurement validity | Exactly 6/6, each uniquely decisive. |
| Primary rows | Completeness | Exactly 1,200 unique canonical rows. |
| Secondary rows | Completeness | Exactly 3,200 unique canonical rows. |

This is a finite deterministic census. No sampling significance or production
probability is claimed.

## Taxonomy and anti-stacking

**Canonical classification:** Failure/Risk Gap × Robustification. Dominant
operation `replace`; secondary operation `decouple`; secondary paradigm
Artifact/System. The Bridge×Synthesis tripwire does not apply.

v2 replaces advisory-controlled stopping with verifier-grounded stopping while
holding the controller family constant. The distinctive reframing is that
**visibility and authority are different variables**. Its mandatory prediction
is not merely “a content-blind controller ignores content”:

- visible and hidden advice are exactly equivalent when `a=0`; and
- all authority-caused trajectory/outcome differences have complete support on
  first reachable exogenous disagreements between advice and base action.

A generic receipt checker + hard cap + content-aware monitor does not predict
zero visible-but-unauthorized effect or full disagreement mediation because it
does not isolate decisional authority. A comparator modified with the same hard
gate has adopted this local `replace/decouple` move; it is no longer a plain
unstructured combination.

The additional sparse-location prediction also differs from a generic “more
poisoned content causes more failure” story: equal one-substitution schedules
can have zero or nonzero effects solely because of authority-relevant action and
reachability. This becomes an exact index/value stratified test.

## Round-1 issue resolution

| # | Prior issue | Author disposition before re-review |
|---:|---|---|
| 1 | Bundled causal estimand | RESOLVED CLAIM: primary changes only `a`; receipts, `K`, recovery, budget, world, schedule, and oracle match. |
| 2 | Guaranteed baseline failure | RESOLVED CLAIM: clean + exhaustive single substitutions include agreement/harmless/unreached cells; retain all. |
| 3 | Post-treatment advisory | RESOLVED CLAIM: pure exogenous lookup independent of realized state/assignment. |
| 4 | Terminal/receipt semantics | RESOLVED CLAIM: total nine-step ordering, charged terminal no-op, exact due indices and grace. |
| 5 | Six clauses/five mutants | RESOLVED CLAIM: six separate clauses, uniquely decisive fixtures, separate mutants. |
| 6 | Contradictory decision rule | RESOLVED CLAIM: one joint primary rule; secondary cells neither rescue nor disconfirm. |
| 7 | Unproved minimality | RESOLVED BY REMOVAL: chosen four-predicate projection; no coarsest/necessity claim. |
| 8 | Anti-stacking failure | RESOLVED CLAIM: visibility/authority separation plus first-disagreement mediation and sparse location dependence. |
| 9 | Floating full-state/pair coverage | RESOLVED BY REMOVAL/REPLACEMENT: no raw label; exact advisory alphabet; every master/schedule/mode crossed plus full `z×u` microfixtures. |
| 10 | Receipt-stress monotonicity | RESOLVED BY REMOVAL: unordered secondary cells, no gradient prediction. |

These are author claims. Only the independent re-review may mark them resolved.

## Self-critique

v2 is causally cleaner and simpler than v1, but its external validity is even
more explicit: it is a deterministic authority-gate unit test, not evidence that
real agents have the stipulated advisory error schedules. The materiality result
may still be predictable from the finite policies. The scientific value is the
isolated causal map and its disconfirmable risk floor, not a claim of surprising
model behavior.

The anti-stacking prediction is structural. A critic may argue any carefully
written receipt/cap system can adopt the same gate; that is true, but adopting it
is precisely the authority-decoupling intervention. v2 must not claim a broad
system invention if the reviewer finds this distinction insufficient.

Receipt soundness remains a hard assumption. v2 does not turn one negative
control into a robustness claim.

## Problem alignment

Confirmation would answer one narrow Cycle-2 question: under controlled inert
workloads, does worker progress advice cause termination-integrity failures
specifically when it has decisional authority, holding verified state and loop
policy fixed? It would not establish framework, model, prompt, or production
safety.

## Review and authorization status

This v2 entry is unreviewed. Cumulative hypothesis-review accounting is 22/30
before v2 dispatch. It must pass deterministic JSON/AST/truth-table/schedule/
oracle checks, be committed immutably, and receive a context-complete independent
`RIGOROUS` verdict before Phase 3.

No primary/secondary execution, Phase 3, framework action, model API,
natural-language attack generation, Kaggle action, held-out/locked-test action,
live target, external message, or publication is authorized.
