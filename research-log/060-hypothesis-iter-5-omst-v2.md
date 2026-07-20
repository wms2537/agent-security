# Hypothesis iteration 5 — Orchestration Metamorphic Security Testing v2

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** preregistered superseding hypothesis, unreviewed

**Supersedes:** `research-log/056-hypothesis-iter-5-omst-v1.md`, which remains
immutable after its round-1 review

**Concept:** Orchestration Metamorphic Security Testing (OMST)

**Claim type:** empirical/systems · **Question type:** causal within the fixed,
paired local interventions; diagnostic outside them

## Context and authorization boundary

Cycle 2 asks which independently checkable controls preserve security properties
when an agent harness, loop, or orchestration graph is rewritten. The round-1
review found the original omnibus design salvageable but causally underidentified.
The user approved the exact c2-v2 amendment recorded in `research-log/059`.

This revision narrows the primary study to one provenance-boundary treatment and
one matched rescue. It does not execute an experiment, download a framework,
generate or inspect a locked test, reproduce an attack, contact a model API,
access Kaggle, or claim production safety. Once round-2 theory review is
dispatched, this file is immutable.

## Hypothesis

### Primary causal claim

On the complete, common-support LangGraph c2-v2 validation census, a relay
boundary using **framework-default metadata reconstruction** will cause at least
**10 percentage points more fixed provenance-contract violations** than the same
relay boundary using **explicit lossless canonical-provenance pass-through**.

Formally, the claim is:

```text
Delta_boundary_pp =
  100 * (q_default_reconstruction - q_explicit_pass_through) >= 10.0.
```

The expected direction is positive. There is deliberately **no evidence-derived
point prediction**. Ten percentage points is the previously approved normative
materiality threshold: it specifies what result would be decision-relevant, not
what prior work estimates. A valid result below 10 points disconfirms the
material claim. The hypothesis is therefore a high-risk measurement conjecture,
not an assertion that the literature already demonstrates this magnitude.

The causal interpretation is permitted only when every common-support,
matching, isolation, and oracle-validity gate below passes. A large number from
an invalid census is not partial support.

### Distinguishing rescue prediction

On identical graph/input/tape units, explicit lossless provenance pass-through
will rescue violations caused by default boundary reconstruction while all of
the following remain exact controls:

- identity and node-only provenance-violation rates are zero;
- terminal task output is identical;
- the full actual inert-effect sequence is identical;
- benign obligations and completion state are identical;
- semantic decision-tape consumption is identical; and
- capability invariance is exact.

A generic graph fuzzer plus a functional filter and security checker predicts
that some changed graphs may fail. It does not predict that failure is removed
by changing only the provenance carrier while topology, boundary exposure,
checkpoint traversal, middleware traversal, schedule, and actual effects remain
fixed. That rescue is the mechanism-discriminating prediction.

## Variables and one pre-specified primary comparison

### Independent variable

Every fixed unit receives four within-unit conditions:

1. `identity`: no extra node and no relay boundary;
2. `node_only`: an extra deterministic relay node without a security boundary;
3. `explicit_pass_through`: the relay boundary with explicit lossless carriage
   of the canonical provenance record; and
4. `default_reconstruction`: the same relay boundary using the framework's
   default metadata reconstruction.

The sole manipulated coordinate in conditions 3 versus 4 is provenance-metadata
propagation. Conditions 1 and 2 are negative/diagnostic controls, not alternative
primary comparators.

### Search dimension

The `varies` slug remains `orchestration-rewrite-relation`, with `kind: metric`.
This is a superseding specification of the same Cycle-2 iteration-5 hypothesis,
so it does not create a second search-log entry. No current-cycle escalation
constraint is active.

### Dependent variables

The primary dependent variable is the binary fixed provenance-contract verdict
`V_prov` for each execution. Secondary variables are the four condition-specific
rates, exact common-support status, each component of the benign task coordinate,
capability invariance, execution steps, CPU time, peak memory, terminal-status
code, evaluator agreement, fixture result, and mutant kill result.

### Held-fixed controls

Within a graph/input/tape unit, the graph skeleton, accepted input, initial
capabilities, semantic obligations, inert tools and results, decision tape,
framework and adapter version, event schema, evaluator versions, CPU class,
five-second budget, process-isolation policy, checkpoint traversal, middleware
traversal, trace-exposure opportunities, relay-node count, and schedule are fixed
for conditions 3 and 4. All four conditions are jointly generated before any
security outcome is opened.

### Single primary comparison

Only this comparison decides the headline claim:

```text
equal-graph-weighted provenance-violation rate under default reconstruction
minus
equal-graph-weighted provenance-violation rate under explicit pass-through.
```

Identity, node-only, oracle fixtures, and capability invariance determine
validity and interpretation. Other rewrite families and CrewAI are later
mandatory replication/generalization studies under separate versioned designs;
they cannot replace, pool into, or rescue this primary result.

## Named concept

### Plain-language statement

OMST treats an orchestration rewrite as a controlled intervention rather than as
an arbitrary mutation. Two executions can do exactly the same benign work while
carrying different security metadata across an internal boundary. OMST first
proves equality of the actual work, then asks whether a security verdict changes,
and finally tests the suspected mechanism by restoring only the metadata carrier.
The contribution is not “metamorphic testing plus security”; it is the matched
separation of task effects from provenance propagation at one orchestration
boundary.

### Concrete event coordinates

Every execution yields an immutable canonical event trace. The trace is read
through two declared coordinate maps:

`B_actual(x)` is the benign task coordinate and contains:

1. terminal task output;
2. the complete ordered sequence of **actual**, not intended, inert tool effects;
3. completed benign obligations and declared completion state; and
4. decision-tape consumption keyed by semantic obligation identifier.

`S_prov(x)` is the security coordinate and contains:

1. source provenance labels;
2. sanitization attestations;
3. authorization attestations;
4. boundary-carriage transitions; and
5. their order relative to the sensitive inert effect.

The finite benign tasks do not require provenance metadata as a task output.
Therefore `B_actual` deliberately excludes only `S_prov`; it does not exclude
any output, actual effect, obligation, or decision. The security predicate
`V_prov(x)` equals 1 exactly when a sensitive inert effect lacks the required
ordered provenance transition, and 0 otherwise.

This is a construct choice with a narrow validity domain, not a claim that
provenance is never functionally relevant. If a workload makes provenance part
of its task contract, it is outside this study or must include that field in
`B_actual`, in which case the proposed security difference becomes impossible.

### Formal finite design

Let:

- `G` be the fixed set of 120 generated graphs;
- `I_g` be the four fixed benign inputs for graph `g`;
- `D={41,42,43}` be the fixed decision tapes;
- `K={id,node,pass,default}` be the four conditions;
- `u=(g,i,d)` be one graph/input/tape unit;
- `x_u(k)` be the complete execution of unit `u` under condition `k`;
- `B_u(k)=B_actual(x_u(k))`; and
- `Y_u(k)=V_prov(x_u(k))`.

Because all four potential conditions are executed for every finite unit, no
counterfactual outcome is imputed. The paired unit-level treatment effect is
directly observed as:

```text
tau_u = Y_u(default) - Y_u(pass).
```

Define common support `C` as all units `u` satisfying all three requirements:

```text
B_u(id) = B_u(node) = B_u(pass) = B_u(default),
Y_u(id) = 0 under the independent reference evaluator, and
all four executions have complete protocol-valid terminal records.
```

The contract requires `|C|=120*4*3=1,440`; common support is not a favorable
subset. If one unit is outside `C`, the entire primary census is invalid rather
than estimated on the remainder.

For each condition `k` and graph `g`, define:

```text
q_g(k) = (1 / 12) * sum over i in I_g and d in D of Y_(g,i,d)(k).
```

Every graph then receives exactly equal weight:

```text
q_k = (1 / 120) * sum over g in G of q_g(k).
```

The primary estimand is:

```text
Delta_boundary_pp = 100 * (q_default - q_pass)
                  = 100 * (1 / 120) * sum_g (1 / 12) * sum_(i,d) tau_(g,i,d).
```

There is no family weighting, variable input weighting, treatment-specific
eligibility denominator, or identity subtraction. Identity is a validity gate.
Conditioning on `Y_u(id)=0` is fixed for all four treatments and therefore does
not mix treatment-specific base-safety prevalence into the contrast.

### Fiber and rewrite-invariance interpretation

`B_actual` maps a full trace to a declared benign-task value. Executions with the
same value form a `B_actual` fiber: they are indistinguishable with respect to
the complete task coordinate but may differ in excluded provenance state.

Provenance security is **rewrite-invariant on a `B_actual` fiber** when
`V_prov(x)=V_prov(x')` for the two matched boundary executions in that fiber.
Equivalently, within the tested rewrite pair, `V_prov` factors through
`B_actual`: equal task coordinates imply equal provenance verdicts. The
hypothesis predicts material failure of that factorization under default
reconstruction, with explicit pass-through as the rescue.

No graph-composition algebra is assumed, so this entry does not use the
undefined v1 term “congruence.”

## Why the mechanism is plausible

### First-principles causal chain

1. A runtime boundary must transfer both task state and security metadata.
2. The finite tasks consume task state and actual inert effects, while the fixed
   provenance predicate consumes a distinct authorization/sanitization record.
3. A default reconstruction path may rebuild only declared task-state fields or
   may normalize metadata differently; explicit pass-through carries the
   canonical provenance record losslessly.
4. Conditions 3 and 4 traverse the same relay boundary and execution machinery,
   so added steps, scheduling, checkpointing, and middleware exposure cannot by
   themselves explain a difference between them.
5. If default reconstruction loses or reorders a required provenance transition,
   `B_actual` remains equal while `V_prov` changes.
6. If explicit pass-through removes that difference on the same unit, metadata
   carriage is the minimal surviving mechanism.

This chain establishes a directional mechanism but not its frequency. The 10 pp
threshold is therefore a predeclared materiality decision. The valid finite
census is allowed to return zero and decisively refute the conjecture.

### What must follow if the mechanism is true

If the primary rescue mechanism is correct, the positive effect must be located
only on the provenance coordinate. It must not require more calls, a different
tape, a changed actual effect, a capability widening, or a failing node-only
control. Any such accompanying difference defeats the stated causal explanation.

Conversely, if default and pass-through produce equal provenance verdicts, then
either the pinned runtime already preserves the relevant metadata, the fixed
grammar never creates a stressed transition, or the mechanism is absent in this
scope. None of those outcomes supports the material claim.

## Evidence chain and novelty boundary

The evidence supports the measurement target and the causal risk surface; it
does not supply a prior magnitude.

- *Towards Long-Horizon Agents* separates the policy from harness, loop,
  orchestration, memory, tools, middleware, and verification components. It
  motivates treating the runtime as an intervention surface, but its July-2026
  manuscript is a non-peer-reviewed survey and does not demonstrate this effect
  ([manuscript](https://www.preprints.org/manuscript/202607.1328)).
- MASEval and FlowSteer report system- and graph-level sensitivity, while Agentic
  Harness Engineering reports that harness changes can improve task performance
  despite incomplete guardrails
  ([MASEval](https://aclanthology.org/2026.acl-demo.34/),
  [FlowSteer](https://arxiv.org/abs/2605.11514),
  [AHE](https://arxiv.org/abs/2604.25850)). These motivate orchestration as a
  causal surface but do not validate provenance preservation.
- LoopTrap, Agent-BOM, and MaMa respectively expose termination poisoning,
  graph-level supply-chain structure, and safety/utility optimization in agent
  systems ([LoopTrap](https://arxiv.org/abs/2605.05846),
  [Agent-BOM](https://arxiv.org/abs/2605.06812),
  [MaMa](https://arxiv.org/abs/2602.04431)). They motivate independent controls
  but do not instantiate the matched metadata-carriage intervention.
- The 2026 metamorphic-testing survey covers 93 primary studies and includes
  autonomous-agent settings; LLMORPH implements 36 relations over four NLP tasks
  in 561,267 executions and reports relation/task false-positive rates from 0%
  to 70% in its manual sample
  ([survey](https://arxiv.org/abs/2605.13898),
  [LLMORPH](https://arxiv.org/abs/2603.23611)). These establish both the mature
  method family and the load-bearing need for relation validation.
- ReliabilityBench is the strongest action-level neighbor: it defines action
  metamorphic relations using end-state equivalence and evaluates two models,
  two architectures, four domains, and 1,280 episodes under task perturbations
  and tool/API faults ([ReliabilityBench](https://arxiv.org/abs/2601.06112)). It
  does not intervene on an internal graph boundary or hold boundary exposure
  fixed while changing only provenance carriage.
- ASSURE is the strongest security-invariant neighbor: it performs system-level
  metamorphic testing of six AI browser extensions and reports 531 distinct
  issues using behavioral and security validators
  ([ASSURE](https://arxiv.org/abs/2507.05307)). Its units vary content,
  extension, and model behavior; it does not define the common-support internal
  boundary rescue contrast used here.

The closest priors invalidate any claim that the novelty is generic metamorphic
testing of agents or the addition of a security checker. The narrower gap is a
**scope mismatch**: existing action/end-state and security-invariant relations do
not identify the internal provenance-carriage mechanism. A local extension of
either ReliabilityBench or ASSURE would need to add a graph-internal treatment,
paired all-condition common support, a task/security coordinate separation, and
the explicit pass-through rescue. Those additions are exactly the new empirical
mapping, not evidence that the prior already measured it.

## Complete validation census

### Runtime and generator

- Primary runtime: LangGraph tag `1.2.9`, source object
  `95af6a00718588e7b7ce17310e8006d267896a77`.
- Validation generator seed: `4242`.
- Graphs: exactly 120.
- Allocation: 12 strata × 10 graphs.
- Strata: boundary position `{early,middle,late}` × control-flow shape
  `{linear,branch}` × state lifetime `{ephemeral,persistent}`.
- Every graph jointly instantiates all four conditions before outcomes exist.

### Inputs and decision tapes

Every graph has exactly four fixed input schemas:

1. trusted;
2. untrusted plus sanitized;
3. untrusted plus explicitly authorized; and
4. chained authorization.

Every input runs under tapes `{41,42,43}`. A tape is keyed by semantic obligation
identifier and fixes model-like decisions, inert tool results, and exogenous
events. The primary schedule is therefore:

```text
120 graphs * 4 inputs * 3 tapes * 4 conditions = 5,760 executions.
```

### Assignment and isolation

A committed balanced Latin schedule keyed only by graph ID assigns condition
order. Each condition runs in a fresh process and fresh temporary directory.
There is no shared filesystem state, cache, telemetry, network, mutable
environment, or cross-condition runtime object. The limit is five CPU seconds
per condition on CPU-only hardware.

Condition labels remain sealed until both independent evaluator implementations
have committed their verdicts. Any timeout, crash, schema failure, incomplete
trace, missing terminal record, or common-support failure invalidates the entire
primary census. There is no per-family “corresponding bundle” ambiguity and no
outcome-dependent exclusion.

## Independent measurement and oracle validation

### Separation of implementations

The production evaluator and reference evaluator must be independently written,
use different internal representations, and implement distinct algorithms. They
may share only the committed event-schema specification and immutable fixture
bytes. They may not share a parser, normalized trace object, predicate helper,
canonicalization routine, or derived expected-answer table.

The production eligibility checker compares a stream-derived canonical tuple.
The reference eligibility checker reconstructs the tuple from an independently
indexed event relation. The production provenance evaluator operates as a state
machine; the reference evaluator checks an independently materialized ordered
edge relation. These representation commitments are preregistered before code is
written; equivalent wrappers over one object do not count.

### Full 2×2 construct matrix

Each implementation must independently classify fixtures covering all four
cells below:

| `B_actual` relation | `V_prov` relation | Required example role |
|---|---|---|
| same | same | valid safe and valid violating task-equal pairs |
| same | different | target provenance-regression and rescue pairs |
| different | same | functional mismatch without security change |
| different | different | combined functional and security mismatch |

Separate positive and negative fixtures are required for terminal output,
actual-effect order, obligations, completion state, tape consumption, provenance
edge presence, authorization presence, sanitizer order, boundary-carriage order,
and capability invariance. A disjunctive “one checker caught it” result is a
failure: eligibility and provenance components must each pass their own controls.

### Mutation adequacy

A fixed six-mutant suite is committed before validation:

1. invert task-coordinate equality;
2. drop one actual effect from `B_actual`;
3. drop one provenance edge from `S_prov`;
4. accept a missing authorization;
5. swap sanitizer and authorization order; and
6. widen a capability while claiming invariance.

Both implementations' relevant suites must kill 100% of their applicable
mutants, and the combined validation matrix must kill all six. Any survivor
blocks the validation census. Mutation adequacy tests sensitivity to known
faults; it does not prove the absence of all common-mode specification error,
which remains a stated assumption and limitation.

## Assumptions and validity domains

| ID | Assumption | Validity domain | Consequence outside the domain |
|---|---|---|---|
| A1 | `B_actual` contains every task-relevant output, actual effect, obligation, completion, and decision coordinate | The four finite input schemas and declared inert task contracts | An apparent security change may be an ordinary functional change; invalidate the task-equality claim |
| A2 | Provenance metadata is security-relevant but not itself a required task output | Only workloads whose benign contract does not consume or expose provenance | If provenance is task output, it belongs in `B_actual` and the hypothesized within-fiber difference is impossible |
| A3 | Every security-relevant event is completely observed and canonicalized without instrumentation effects | The pinned event schema and adapter-supported LangGraph subset | Missing or observer-altered events invalidate every security verdict |
| A4 | Conditions 3 and 4 differ only in provenance propagation | Jointly generated matched relay boundaries passing exact structural and schedule checks | Any additional difference confounds the causal mechanism and invalidates the primary comparison |
| A5 | The explicit carrier is lossless and the default path is the runtime's ordinary reconstruction behavior | Pinned LangGraph object and the exact adapter/API surface fixed before validation | Misimplemented treatments become an adapter experiment, not a runtime-boundary test |
| A6 | Semantic decision-tape IDs map totally and uniquely across conditions | Generated graphs whose obligation mapping passes before execution | Different decisions or compute budgets confound the contrast; census invalid |
| A7 | Actual inert effects are faithfully logged in execution order | Local deterministic tools in the declared schema | Capability or effect differences can be hidden; `B_actual` equality is not established |
| A8 | Fresh-process isolation prevents cross-condition interference | CPU-only runs with new temporary state, network and telemetry disabled | Cache, filesystem, or hidden-state carryover defeats paired attribution |
| A9 | Both provenance evaluators implement the declared predicate correctly | Fixed fixtures, independent representations, 100% fixed-mutant kill | Measurement error can create or hide the effect; no primary conclusion |
| A10 | Evaluator independence is sufficient to reduce common-mode implementation error | No shared parser, normalized object, helper, or derived answer table | Agreement may be duplicated error; downgrade or invalidate after code review |
| A11 | Generator, conditions, `B_actual`, `V_prov`, fixtures, mutants, threshold, and analysis are fixed before validation outcomes | Preregistered hashes and immutable paths | Outcome-driven tuning consumes a new iteration; the current confirmation claim is void |
| A12 | All 1,440 units satisfy common support by construction and verification | Jointly generated finite census only | Any failure invalidates the whole primary census; no subset estimate is allowed |
| A13 | The balanced grammar covers the declared boundary positions, control shapes, and state lifetimes | Exactly the 12 strata and 120 graphs | Positive or null results do not generalize to unrepresented graph regimes |
| A14 | Pinned LangGraph `1.2.9` is a stable intervention unit | Exact source object, lockfile, and adapter subset | Later versions and other frameworks require separate replication |
| A15 | Ten percentage points is a useful project materiality boundary | This project's finite validation decision | It is not an estimated prevalence, field standard, or universal risk threshold |

## Fixed bias surface

1. **Selection.** The generator seed, 12 strata, ten graphs per stratum, four
   inputs, and three tapes are fixed before outcomes. Every unit receives every
   condition. Common support must be 100%; no treatment-specific eligible subset
   or favorable base-safety prevalence can enter the estimand.
2. **Confounding.** Conditions 3 and 4 are matched on topology, node count,
   trace opportunities, checkpoint and middleware traversal, decision tape,
   actual effects, resource budget, and isolation. Structural equality audits
   and the node-only control test remaining exposure explanations. An unobserved
   treatment difference invalidates, rather than adjusts, the causal claim.
3. **Allocation/assignment.** This is a complete within-unit design, not a
   between-graph allocation. Every unit executes all four conditions. A balanced
   Latin order keyed only by graph ID distributes order while fresh processes
   eliminate warm-state carryover.
4. **Protocol deviation.** Exact versions, hashes, schema, schedule, command,
   five-second budget, terminal-state semantics, immutable inputs, and COMPLETE
   evidence rules are checked before a result is kept. Any scientific change
   after outcome access creates a new iteration and contract.
5. **Missing data.** A timeout, crash, malformed trace, missing terminal record,
   ineligible task coordinate, or unsafe identity unit invalidates the entire
   5,760-execution census. Nothing is dropped, imputed, recoded as a violation,
   or analyzed on available cases.
6. **Measurement.** Exact task coordinates, an explicit security coordinate,
   two independent representations, the 2×2 construct matrix, component-specific
   controls, sealed condition labels, and 100% six-mutant kill are mandatory.
   Large `n` cannot rescue a failed oracle gate.
7. **Analysis flexibility.** The equal-graph estimand, sole condition-4-minus-3
   comparison, 10 pp threshold, 100% support rule, negative controls, and invalid
   states are fixed here. Secondary stratification or resampling cannot replace
   or rescue a subthreshold primary result.
8. **Selective reporting.** All 5,760 terminal states, four condition rates,
   common-support checks, evaluator disagreements, control outcomes, mutant
   outcomes, and later mandatory replication results are retained and reported.
   There is no best-condition, best-family, or best-framework substitution.

## Rival explanations and discriminating checks

| Rival | How it could mimic the claim | Predeclared check | Conclusion impact if unresolved |
|---|---|---|---|
| Added relay exposure | More events, steps, or nodes could create failures regardless of metadata | Conditions 3/4 have identical relay; node-only separately tests a node without boundary | A node-only signal or mismatch invalidates provenance mediation |
| Checkpoint/middleware difference | Default and pass-through could traverse different plumbing | Exact traversal/event-opportunity equality in structural audit | Any difference invalidates primary causality |
| Actual-effect mismatch | A hidden extra effect could appear security-relevant | Full ordered actual effects are inside `B_actual`; 100% common support required | Any mismatch invalidates census, never counted as security-only |
| Treatment-specific selection | Only favorable default/pass units might remain | All four conditions required on every one of 1,440 units; no subset analysis | Any support loss invalidates entire primary census |
| Baseline-unsafety mixture | Unsafe identity units could distort a joint rate | Independent identity safety required for every unit before labels open | One unsafe identity unit invalidates the census |
| Adapter treatment bug | The adapter may drop metadata rather than the runtime default | Exact pinned API/source audit, treatment fixtures, independent code review | Downgrade to adapter artifact or invalidate runtime claim |
| Common-mode oracle bug | Both evaluators may agree on the same wrong schema | Different representations/algorithms, separate controls, mutation suite, later code review | Unresolved dependence invalidates the primary verdict |
| Structural condition leakage | Evaluator may infer labels from trace form | Labels sealed; reference evaluates ordered relations; all four 2×2 cells include structurally varied fixtures | If predicate depends on condition rather than provenance relation, invalidate measurement |
| Generator targeting | Grammar may overrepresent metadata-sensitive graphs | Exact 12-stratum finite-census claim and mandatory stratum report | Restrict conclusion to census; never infer production prevalence |
| Version-specific behavior | Effect may be a transient pinned-version defect | Exact version language; later CrewAI/other-version replication cannot alter primary | No universal framework conclusion |
| Order or hidden state | Earlier conditions may affect later ones | Fresh process/temp state plus balanced Latin order and no network/telemetry | Any interference invalidates pairing |

## Metrics and decision rules

| Outcome | Metric | Support/required result | Disconfirm | Protocol invalid |
|---|---|---|---|---|
| Primary material effect | `Delta_boundary_pp` | `>=10.0` with every validity gate passing | `<10.0` on a valid census | Any common-support, matching, isolation, evaluator, or control gate fails |
| Expected direction | sign of `Delta_boundary_pp` | positive | zero or negative | Primary protocol invalid |
| Common support | valid units / 1,440 | exactly `1.0` | N/A | anything below `1.0` |
| Identity control | `q_identity` | exactly `0.0` | N/A | any nonzero value |
| Node-only control | `q_node_only` | exactly `0.0` for mediation interpretation | N/A | any nonzero value |
| Task coordinate | componentwise `B_actual` equality | exactly 5,760 condition records in 1,440 equal four-tuples | N/A | any inequality or missing value |
| Capability control | capability equality across conditions | exactly `100%` | N/A | any widening, loss, or disagreement |
| Evaluator agreement | production/reference verdict equality after independent validation | exactly `100%` | N/A | any unexplained disagreement |
| Mutation adequacy | killed fixed mutants / 6 | exactly `1.0` for applicable combined suite | N/A | any surviving mutant |

No scientifically “inconclusive” primary interval exists. A valid subthreshold
value is a disconfirmation. “Protocol invalid” means the causal question was not
successfully tested and cannot be described as support.

## Idea taxonomy

- **Opportunity pattern:** Scope Mismatch, with Failure/Risk Gap secondary.
- **Method paradigm:** Empirical Mapping.
- **Dominant operation:** `decouple`.

The operation decouples actual benign task effects from provenance-metadata
carriage while holding a graph-internal boundary fixed. This is not Bridge
Opportunity × Synthesis/Unification: it neither integrates separate defenses nor
claims to unite testing fields. ReliabilityBench and ASSURE already establish
agent/action relations and security-invariant system testing. OMST locally
changes the unit and treatment they do not cover: an internal boundary's metadata
carrier on complete paired common support.

Calling the study a “local extension” does not eliminate the contribution, but
it correctly narrows it. Extending either closest prior to answer this question
requires the exact new causal intervention, task/security coordinate split,
equal-graph estimand, and rescue control defined here. Generic content
perturbation or system-level invariant checking cannot estimate
`Delta_boundary_pp` without those changes.

## Anti-stacking and Occam checks

OMST adds no defense ensemble, model, optimizer, search loop, or judge stack. It
tests the smallest intervention that distinguishes provenance carriage from the
mere existence of a boundary: same boundary with default reconstruction versus
explicit pass-through. Identity and node-only are necessary falsification
controls; removing them would leave simpler code but a weaker causal claim.

The plain-combination prediction is “some graph mutations fail a security
checker.” The OMST prediction is narrower:

> On the same 1,440 base-safe task-equal units, default reconstruction causes at
> least 10 percentage points more provenance violations than lossless
> pass-through, while identity, node-only, actual effects, and capability remain
> exactly invariant.

If both boundary conditions fail equally, generic added exposure or the oracle
is a better explanation. If neither fails, the pinned runtime is invariant on
this finite fiber. If only default reconstruction fails and pass-through rescues
it, the one-coordinate mechanism survives the controls.

## Predicted failure modes

1. **True preservation:** default reconstruction already carries all required
   provenance, yielding valid `Delta=0` and falsifying materiality.
2. **Weak materiality:** the direction is positive but below 10 pp; the primary
   claim is disconfirmed, even if the cases are diagnostically useful.
3. **Generic boundary failure:** default and pass-through fail equally; boundary
   exposure, not metadata reconstruction, explains the result.
4. **Node exposure:** node-only is nonzero; added execution structure defeats the
   proposed mediation interpretation.
5. **Relation collapse:** any `B_actual` coordinate differs; the joint generator
   failed to create the declared task-equal intervention and the census is void.
6. **Identity unsafety:** even one base execution violates provenance; the
   preregistered common base-safe support does not exist.
7. **Oracle inadequacy:** a component control, 2×2 fixture, evaluator agreement,
   or mutant kill fails; no security rate is interpretable.
8. **Treatment infidelity:** source/code inspection shows default and pass-through
   differ in more than metadata carriage; causal attribution is invalid.
9. **Protocol failure:** any execution is missing, malformed, timed out, or
   cross-contaminated; no available-case estimate is allowed.
10. **Finite-scope artifact:** the effect exists only in one stratum or depends
    on generator structure; the exact census result stands, but any broader
    framework language is prohibited.

## Self-critique and re-derivation

The load-bearing argument can be rebuilt from the design without relying on
notation:

1. The full execution trace is richer than the declared benign task outcome.
2. `B_actual` keeps every actual task effect and excludes only provenance state.
3. Conditions 3 and 4 execute the same boundary and work; only their provenance
   carrier differs.
4. Every unit receives both conditions, so its verdict difference is observed,
   not estimated from unmatched groups.
5. Requiring base safety and exact task equality across all four conditions on
   all units removes baseline prevalence and treatment-specific selection.
6. Averaging the 12 within-graph paired differences and then the 120 graph means
   gives every graph equal weight.
7. A pass-through rescue therefore isolates the provenance-carriage coordinate
   within the declared finite system, subject to fidelity and measurement gates.
8. Nothing in this argument guarantees ten points. That number is the
   preregistered materiality boundary, and the valid experiment may refute it.

The strongest objection is **treatment authenticity**: if “default
reconstruction” is implemented by our adapter rather than exercised through the
pinned runtime's ordinary behavior, the result would be self-authored. This is a
real validity condition, not a limitations-section escape. Phase 3 must first
show from pinned source and non-confirmatory fixtures that both conditions use
the same runtime boundary and that only the explicit carrier differs. Failure
ends or redesigns the hypothesis before validation.

The next strongest objection is **specification common mode**: independent code
can still share a wrong event schema. The 2×2 matrix and mutation suite do not
prove the construct. The claim is therefore restricted to the declared abstract
provenance contract, and later code review must judge whether the schema matches
that contract. It cannot become a universal security guarantee.

The deterministic synthetic setting is also intentionally narrow. It supplies
causal isolation of orchestration behavior, not realism about stochastic LLM
policy behavior or deployed attack prevalence. Those require separate studies.

## Round-1 issue resolution matrix

| Round-1 required issue | Revision location | Claimed status |
|---|---|---|
| 1. Primary estimand and weighting | Formal finite design; common support; equal 12-within-graph then 120-graph mean; no treatment-specific denominator | RESOLVED |
| 2. `B`/security overlap | Concrete event coordinates; all actual effects in `B_actual`; provenance alone in `S_prov`; capability as exact negative control | RESOLVED |
| 3. Causal mechanism/common support | Four matched conditions; condition 4 minus 3 only; 100% all-condition support; topology/exposure/checkpoint/middleware fixed | RESOLVED |
| 4. Independent oracle validation | Different representations/algorithms; per-component controls; 2×2 matrix; fixed six-mutant 100% kill gate | RESOLVED |
| 5. Evidence and taxonomy | Direct ReliabilityBench/ASSURE comparison; Scope Mismatch × Empirical Mapping × `decouple`; local-extension boundary stated | RESOLVED |
| 6. Census specification | Exact pin, seed, 12 strata, 120 graphs, four inputs, three tapes, four conditions, 5,760 runs, isolation/budget/failure scope | RESOLVED |
| 7. Assumptions and terminology | Fifteen assumptions with regimes; “rewrite-invariant on a `B_actual` fiber”; undefined congruence removed | RESOLVED |

These are author claims for round-2 testing, not gate decisions. The independent
reviewer must grade every row RESOLVED / IMPROVED / UNCHANGED / WORSE and check
for new defects.

## Gate Check before theory review

- Falsifiable claim, IV, DV, four conditions, exact controls, expected direction,
  and one condition-4-minus-3 primary comparison: specified.
- Search dimension: Cycle 2 iteration 5,
  `orchestration-rewrite-relation`, `kind: metric`; no duplicate entry and no
  active escalation constraint.
- Concept: named, explained in plain language, and formally defined as paired
  rewrite invariance on a `B_actual` fiber.
- Empirical/systems justification: one-coordinate causal chain, direct prior-work
  boundary, complete measurement design, fifteen assumptions with validity
  domains, all eight fixed bias items, and eleven rival explanations.
- Failure, valid disconfirmation, and protocol invalidity: separated.
- Metrics: exact equal-graph estimand, 10 pp threshold, controls, common support,
  evaluator agreement, and mutation adequacy fixed.
- Taxonomy: Scope Mismatch × Empirical Mapping × `decouple`; not the
  Bridge×Synthesis default.
- Anti-stacking: pass-through rescue under the same boundary distinguishes the
  claim from graph fuzzing plus functional/security filters.
- Problem alignment: confirmation would identify a mechanically checkable
  control—lossless provenance pass-through—that preserves security when one
  orchestration boundary is rewritten, directly answering the first Cycle-2
  causal question within its finite proxy.
- Theory review: **PENDING**. No PoC or experiment is permitted before a valid
  RIGOROUS verdict.

## Decision

Commit and deterministically verify this superseding entry. Then dispatch one
sterile empirical/systems round-2 theory review containing only the required
template fields and the prior issue list. Charge review budget 13/20 at dispatch.

## Next Steps

1. Verify exact census arithmetic, issue rows, bias enumeration, assumptions,
   config agreement, absence of placeholders, and immutable-path status.
2. Dispatch round 2 only after deterministic checks pass.
3. Enter Phase 3 only after a RIGOROUS verdict with scrutiny evidence.
