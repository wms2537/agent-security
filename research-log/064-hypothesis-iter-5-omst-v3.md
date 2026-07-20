# Hypothesis iteration 5 — Orchestration Metamorphic Security Testing v3

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** preregistered superseding hypothesis, unreviewed

**Supersedes:** `research-log/060-hypothesis-iter-5-omst-v2.md`, immutable after
round-2 review; v1 remains immutable at `research-log/056`

**Concept:** Schema-Boundary Orchestration Metamorphic Security Testing
(SB-OMST)

**Claim type:** empirical/systems with a deterministic structural subclaim

**Question type:** causal within the fixed paired intervention; diagnostic
outside the pinned runtime, grammar, and abstract provenance policy

## Context and correction history

The round-1 review forced the original pooled rewrite study into a single matched
provenance-boundary rescue. Round 2 accepted the estimand, task/security split,
evidence boundary, taxonomy, assumptions, and anti-stacking logic, but required
an exact security automaton, executable treatment fidelity, byte-deterministic
census generation, and a residual-runtime determinism gate.

The pinned-source check in `research-log/063` then found a more fundamental
naming problem. LangGraph 1.2.9 implements node-input-schema channel projection;
it does not expose a generic “framework-default metadata reconstruction”
operation. This revision therefore studies a real source-backed design choice:
a sensitive action node whose input schema includes only task state versus the
same node whose schema also includes the canonical provenance record.

This is a narrower and potentially elementary claim. The study will not inflate
a source-implied projection fact into a broad framework vulnerability. An
explicit non-redundancy gate below stops the large census if Phase 3 shows the
outcome is a tautological consequence of the treatment and oracle rather than a
scientifically informative runtime behavior.

No framework was cloned, downloaded, installed, or executed while writing this
entry. No experiment, attack, model API, Kaggle action, external message, or
locked-test action occurred. Once review is dispatched, this file is immutable.

## Hypothesis

### Primary finite causal claim

On every protocol-valid common-support unit in the fixed LangGraph c2-v3
validation census, projecting the sensitive-action node onto `TaskStateOnly`
will produce more provenance-policy violations than projecting the identical
node onto `TaskStatePlusProvenance`. The pre-specified material claim is:

```text
Delta_schema_pp =
  100 * (q_task_only_schema_action - q_provenance_visible_action)
  >= 10.0 percentage points.
```

The expected direction is positive. Conditional on the pinned source behaving
exactly as inspected, the compiled-channel audit passing, the action rule in the
fixed config being implemented literally, and all provenance-visible controls
passing, the structural point prediction is **100 percentage points with high
confidence**: `TaskStateOnly` lacks `provenance_record`, so the source-identical
action emits a null provenance digest; `TaskStatePlusProvenance` carries the
record and emits its digest.

That 100-point prediction is not borrowed from prior work and is not a production
prevalence estimate. It is derived from the intervention and the declared
automaton. A result other than 100 on a valid implementation would therefore be
more informative than a match: it would show that our model of compiled state,
trace generation, or policy semantics is wrong.

The decision threshold remains the approved normative 10 points. A valid value
below 10 disconfirms materiality. A positive 10–99.99 value supports the
threshold but disconfirms the exact structural prediction. Protocol failure is
neither support nor disconfirmation.

### Mechanism-rescue prediction

The security difference must disappear when the only changed compiled channel,
`provenance_record`, is restored. Across the paired schema conditions:

- full pre-action graph-state bytes are identical;
- action callable source hashes are identical;
- graph topology, schedule, middleware, checkpointing, tape, and effect fixture
  are identical;
- actual inert effects and all benign task coordinates are identical;
- compiled input-channel symmetric difference is exactly
  `{provenance_record}`; and
- identity and node-only controls remain provenance-safe.

If any other coordinate differs, the result cannot be attributed to schema
projection.

### Non-redundancy stopping rule

Before any 120-graph validation census, Phase 3 must answer:

> After static source verification and one minimal tuning fixture per condition,
> is `V_prov(task_only)=1` and `V_prov(full)=0` a direct definitional consequence
> of the compiled channel sets and action rule, with no context-dependent runtime
> uncertainty left?

If **yes**, the large census is scientifically redundant. Stop OMST after the
minimal deterministic witness, report a source-backed schema-closure result, and
do not claim empirical prevalence or spend validation executions to restate the
construction. This outcome confirms the narrow mechanism but does **not** count
as confirmation of a nontrivial empirical frequency claim.

If **no**, record the specific context-dependent uncertainty—such as channel
availability varying with graph placement or lifetime—and only then may the
predeclared finite census test `Delta_schema_pp`, after all gates pass.

This stopping rule is fixed before implementation results and prevents a large
sample from laundering a tautology into apparent empirical evidence.

## Variables and one primary comparison

### Four conditions

1. `identity`: original sensitive action node receives full graph state.
2. `node_only`: one inert relay is added; the sensitive action still receives
   full graph state.
3. `provenance_visible_action`: the matched separate sensitive-action node has
   exact input schema `TaskStatePlusProvenance`.
4. `task_only_schema_action`: the same action callable has exact input schema
   `TaskStateOnly`.

Conditions 3 and 4 are the primary pair. Conditions 1 and 2 are negative and
diagnostic controls.

### Independent variable

The only permitted primary intervention is the input-schema transfer function
bound to the compiled sensitive-action node:

```text
T_full(s) = projection of full state s onto ordered keys
            [task keys..., provenance_record]

T_task(s) = projection of the same s onto ordered keys
            [task keys...].
```

### Search dimension

The `varies` slug remains `orchestration-rewrite-relation`, `kind: metric`, Cycle
2 iteration 5. v3 supersedes the same active hypothesis and does not append a
duplicate search-log entry. No current-cycle escalation constraint exists.

### Dependent variables

Primary: deterministic binary `V_prov` and the equal-graph contrast
`Delta_schema_pp`.

Secondary/validity: exact compiled channel lists; treatment-fidelity predicates;
full pre-action bytes; `B_actual` component equality; capability equality;
identity/node-only verdicts; production/reference evaluator agreement; clause
fixture coverage; clause-mutant kill; replay equality; terminal status; CPU time;
peak memory; and generator/config hashes.

### Held-fixed controls

Graph/input/tape identity, full pre-action state, source hash of the action
callable, effect fixture, initial capability set, graph nodes and edges, semantic
schedule, branch choices, checkpoint/middleware manifest, framework object,
adapter/instrumentation object, evaluator versions, canonical serialization,
CPU class, process environment, five-second limit, and run order formula are
fixed within every pair.

### Single primary comparison

Only condition 4 minus condition 3 on LangGraph validation units can decide the
material headline. Identity/node-only and all evaluator/treatment/replay checks
gate validity. Other rewrite families, versions, and CrewAI require separate
studies and cannot be pooled into or substituted for this result.

## Named concept

### Plain-language statement

SB-OMST asks whether narrowing a graph node's task-facing schema also removes a
security fact the node needs. It compares the same action under two framework
schema projections, proves that the benign work remains identical, and checks
whether restoring exactly one provenance channel rescues the security verdict.
The method is a controlled schema-closure test, not a claim that task-only
schemas are inherently unsafe or that LangGraph promises to preserve fields a
developer excluded.

### Formal task/security coordinates

For execution `x`, `B_actual(x)` is the tuple of:

1. terminal task output;
2. complete ordered actual inert-effect records;
3. completed benign obligations and completion state; and
4. semantic decision-tape consumption.

It excludes only the canonical provenance record and boundary visibility
events. It does not exclude intended-versus-actual differences: all actual
effects are inside the task coordinate.

`S_prov(x)` is the canonical event subsequence used by `OMST-PROV-1`: source,
sanitization/authorization attestations, node/boundary visibility, sensitive
effect, provenance digests, capability, and completion ordering.

`V_prov(x)=1` exactly when the event trace is schema-valid and at least one of
the 17 normative provenance clauses is false. A malformed event schema,
out-of-range phase, or missing terminal record is protocol invalid and has no
security value.

### Formal finite estimand

Let:

- `G={0,...,119}` be the fixed graph IDs;
- `I={0,1,2,3}` be the input IDs;
- `D={41,42,43}` be decision tapes;
- `K={id,node,full,task}` be conditions;
- `u=(g,i,d)` be a unit;
- `x_u(k)` be its execution in condition `k`;
- `B_u(k)=B_actual(x_u(k))`; and
- `Y_u(k)=V_prov(x_u(k))`.

Common support `C` is the set of units for which:

```text
B_u(id) = B_u(node) = B_u(full) = B_u(task),
Y_u(id) = 0 under the independent reference evaluator,
all four executions are protocol-complete,
the exact treatment-fidelity predicate passes, and
the Phase-3 replay gate has passed for the matching archetype.
```

The contract requires `C=G×I×D`, so `|C|=1,440`. A missing unit invalidates the
entire census; `C` is not a selected favorable subset.

For graph `g` and condition `k`:

```text
q_g(k) = (1/12) * sum over i in I, d in D of Y_(g,i,d)(k)
q_k    = (1/120) * sum over g in G of q_g(k)

Delta_schema_pp = 100 * [q_task - q_full].
```

Every graph receives equal `1/120` weight and every input/tape within a graph
receives equal `1/12` weight. There is no treatment-specific denominator,
identity subtraction, family weighting, imputation, or population p-value.

### Fiber interpretation

`B_actual` maps full traces into task-equivalence fibers. The paired schema
executions occupy the same fiber if their complete benign coordinates are equal.
Provenance security is rewrite-invariant on that fiber only if their `V_prov`
values match. SB-OMST tests whether restoring one schema channel changes the
security coordinate without leaving the task fiber.

## Source-authentic treatment mechanism

### Exact pinned surfaces

The inspected official tag/object fixes four code surfaces:

1. [`StateGraph.add_node`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/graph/state.py)
   selects explicit `input_schema`, infers it from the callable's first typed
   argument, or falls back to the graph state schema.
2. `CompiledStateGraph.attach_node` in the same file computes
   `input_channels=list(builder.schemas[input_schema])` and binds those channels
   to the `PregelNode`.
3. [`prepare_single_task`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_algo.py)
   creates task input through `_proc_input` from the compiled channel set.
4. [`ChannelRead.do_read`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_read.py)
   reads selected channels and applies the schema mapper.

The claim is about this node-schema projection mechanism. It is not a claim that
the framework reconstructs provenance incorrectly.

### Exact schema types

`TaskStateOnly` is an exact `TypedDict` with these ordered keys:

```text
graph_id, input_id, tape_id, subject_id, task_value, scratch,
obligations, effect_id, effect_log, tape_cursor, completion
```

`TaskStatePlusProvenance` contains those exact keys followed by:

```text
provenance_record
```

All field types and serialization rules are normative in
`experiments/configs/omst-c2-v3.json`. No alias, optional fallback, runtime
context, config metadata, global variable, store, or side channel may expose the
record to `TaskStateOnly`.

### Source-identical action rule

Both primary conditions bind the exact same callable bytes. The callable reads
`state.get("provenance_record")`. For boundary conditions it emits
`BOUNDARY_EXIT`, then `SENSITIVE_EFFECT`, with:

```text
record_digest = SHA256(canonical_json(provenance_record)) if present else null.
```

It always performs the same one inert effect and appends the same task effect
record. A read-only pre-task observer logs `BOUNDARY_ENTER` from the full
checkpoint channel map before `_proc_input` projection. That observer may not
write graph state or action input.

### Treatment-fidelity table

| Coordinate | Condition 3 versus 4 rule | Verification |
|---|---|---|
| Full pre-action state bytes | exactly equal, including provenance | canonical byte equality |
| State channel names/values/versions | exactly equal before projection | sorted channel manifest hash |
| Graph node/edge manifest | equal except schema type name | canonical manifest diff |
| Action callable | byte-identical | source/code-object hash |
| Tape and branch decisions | exactly equal | semantic tape ledger equality |
| Middleware/checkpoint policy | exactly equal | manifest equality |
| Resource/process environment | exactly equal | environment manifest |
| Compiled action input channels | symmetric difference exactly `{provenance_record}` | compiled `PregelNode.channels` audit |
| Transfer function | `T_full` versus `T_task` only | source path + channel audit |
| Actual inert effect | exactly equal | `B_actual.effect_log` bytes |
| Post-action non-provenance state | exactly equal | canonical projection equality |

Any failing row invalidates the entire primary census. Assumption language does
not substitute for these observable predicates.

## Exact provenance policy

### Grounding and scope

W3C PROV-DM defines provenance through entities, activities, agents,
derivations, responsibility, and delegation, and recommends validity constraints
on ordering and influence ([W3C PROV-DM](https://www.w3.org/TR/prov-dm/)). NIST
SP 800-162 defines attribute-based authorization using subject, object,
operation, and environment attributes evaluated against policy
([NIST SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final)).

`OMST-PROV-1` is an application-specific specialization, not a claimed
implementation of either standard. These sources ground the constructs; exact
fixtures and independent validators establish only internal construct fidelity.

### Canonical provenance record

Every record has exactly:

```text
subject_id: lowercase SHA-256 identifier
source_label: trusted | untrusted
sanitizers: ordered records {id, scope, decision}
authorizations: parent-before-child records
                {id, parent_id, scope, decision}
```

The record digest is SHA-256 of canonical JSON. Canonical JSON is UTF-8
`json.dumps(sort_keys=true,separators=(',',':'),ensure_ascii=true,
allow_nan=false)` with integers, strings, booleans, and null only, and no trailing
newline.

### Canonical event schema

Every event has exactly eleven fields:

```text
event_id, phase, kind, subject_id, actor_id, record_digest,
attestation_id, parent_id, scope, decision, effect_id
```

All fields are required, unused fields are null, extra fields are forbidden, and
types/enums are fixed in the config. `event_id` is SHA-256 of canonical event
bytes without `event_id`. Semantic phase is fixed:

```text
0 SOURCE
1 SANITIZE or AUTHORIZE
2 NODE_ENTER or BOUNDARY_ENTER
3 NODE_EXIT or BOUNDARY_EXIT
4 SENSITIVE_EFFECT
7 COMPLETE
```

Events are ordered by `(phase,kind,event_id)`. Wall-clock time, task-completion
order, UUIDs, and thread scheduling never enter the security trace.

### Input-specific accepted authorization paths

| Input | Required path before effect |
|---|---|
| trusted | exactly one trusted SOURCE; no sanitizer or authorization required |
| untrusted_sanitized | untrusted SOURCE then exactly one effect-scoped allow SANITIZE |
| untrusted_explicitly_authorized | untrusted SOURCE then exactly one root effect-scoped allow AUTHORIZE |
| chained_authorized | untrusted SOURCE then root allow AUTHORIZE scoped `relay`, then child allow whose parent is root and scope is `effect_id` |

Any deny on the subject/effect path is rejecting. Attestations with the same
kind/parent/scope but different decisions conflict and reject. Missing,
duplicate, reordered, wrong-subject, wrong-effect, or out-of-scope records reject
according to the clauses below.

### Seventeen normative clauses

`V_prov=1` iff a protocol-valid trace violates at least one clause:

1. `P01`: event IDs are unique and equal their hash rule.
2. `P02`: subject and effect identifiers match the unit.
3. `P03`: exactly one phase-0 SOURCE precedes attestations/effect.
4. `P04`: trusted input has trusted source and needs no attestation.
5. `P05`: sanitized input has exactly one valid effect-scoped allow sanitizer.
6. `P06`: explicitly authorized input has exactly one valid root effect-scoped
   allow authorization.
7. `P07`: chained input has the exact root-relay then child-effect allow chain.
8. `P08`: no deny occurs on the active authorization path.
9. `P09`: no conflicting attestations share kind/parent/scope.
10. `P10`: identity/node-only contain no boundary events; node-only has one
    ordered node enter/exit pair.
11. `P11`: schema-boundary conditions have one boundary enter then exit before
    the effect.
12. `P12`: boundary-enter digest equals the full pre-action record digest.
13. `P13`: boundary-exit digest exists and equals boundary-enter digest.
14. `P14`: exactly one sensitive effect occurs after required events.
15. `P15`: effect digest equals the accepted current provenance digest.
16. `P16`: effect operation/id remains inside the unchanged capability set.
17. `P17`: complete occurs after the effect and no security event follows it.

Malformed schema or missing terminal data is protocol invalid before these
clauses are scored.

### Fixtures and clause mutations

For graph 0, tape 41, all four inputs and applicable safe conditions,
`OMST-GEN-1` deterministically produces accepting trace bytes. For each `P01`–
`P17`, the config fixes one exact byte transformation that makes the named clause
false and changes the verdict. It also fixes task-coordinate mutants `B01`
invert-equality and `B02` drop-actual-effect.

The transformations cover duplicate IDs, wrong subject, missing source, invalid
trusted label, missing sanitizer, missing root authorization, broken parent
chain, deny insertion, conflicting attestations, illegal boundary event,
enter/exit reorder, wrong enter digest, null exit digest, duplicate effect, null
effect digest, out-of-capability effect, and post-completion security event.

Every clause receives accepting and rejecting fixtures. All four
`B_actual same/different × V_prov same/different` cells are serialized for every
input. Collateral clause failures are recorded rather than hidden; the named
clause must fail and the overall verdict must flip.

## Independent measurement

The production evaluator is a single-pass explicit state machine over canonical
event bytes. The reference evaluator independently parses fixture bytes into
relational tables keyed by subject/event/attestation and checks set/order
predicates. They share only the normative config/event-schema text and immutable
fixture bytes—not a parser, normalized object, helper, automaton code, or derived
answer table.

Before validation, both implementations must independently:

- pass every accepting/rejecting clause fixture;
- pass all per-input 2×2 construct cells;
- agree on every protocol-invalid fixture;
- kill all 17 clause mutants;
- kill both task-coordinate mutants; and
- agree exactly on every tuning trace after separate parsing.

Required fixture coverage and kill fractions are both 100%. Any disagreement or
survivor blocks validation.

## Byte-deterministic census

### Generator algorithm

The normative generator is `OMST-GEN-1`, seed `4242`. It derives every integer
from the first eight bytes of domain-separated SHA-256:

```text
u64(tag,*ids) = uint64_be(
  SHA256(utf8("OMST-GEN-1|4242|" + tag + "|" + join_decimal(ids,"|")))[0:8]
).
```

Identifiers use the full lowercase SHA-256 digest under the same domain
separation. There is no language-runtime PRNG.

### Graph-ID map and strata

For `graph_id g` in `0..119`:

```text
stratum_id   = g % 12
replicate_id = floor(g / 12)
position     = [early,middle,late][stratum_id % 3]
shape        = [linear,branch][floor(stratum_id/3) % 2]
lifetime     = [ephemeral,persistent][floor(stratum_id/6) % 2].
```

Thus each of 12 strata has exactly ten graph IDs.

### Node and edge grammar

Linear base nodes are `source,stage_a,stage_b,stage_c,complete`.
`sensitive_action` is inserted after `source`, `stage_b`, or `stage_c` for early,
middle, or late position.

Branch base edges are:

```text
source -> stage_a -> fork
fork -> left; fork -> right
left + right -> join -> stage_c -> complete
```

The action is inserted after source, join, or stage_c for early, middle, or late.
Left/right emit domain-separated tokens and join stores their lexicographically
sorted tuple, making merge output order-independent.

The complete task state has the eleven exact task keys listed earlier.
Ephemeral/persistent varies only scratch-channel lifetime; scratch never enters
the provenance policy. The provenance record is a distinct full-state channel.

### Exact inputs, tapes, and order

Input IDs `0..3` map respectively to trusted, sanitized, explicitly authorized,
and chained-authorized templates. Subject, effect, sanitizer, and authorization
IDs are full domain-separated SHA-256 values. The config fixes every template and
the exact substitution rule, so `(graph_id,input_id)` maps to unique canonical
input bytes.

Tapes `{41,42,43}` contain branch choice, three stage tokens, and one inert tool
value, each derived by the `u64` rule from graph/input/tape IDs. The exact tape is
canonical JSON. Every condition consumes the same semantic tape entries.

For graph `g`, condition order indices are:

```text
[(g+j) % 4 for j in 0..3]
```

under the fixed condition-array order. Because 120 is divisible by four, every
condition occupies each order position equally often.

The schedule is exactly `120 × 4 inputs × 3 tapes × 4 conditions = 5,760`
validation executions if the non-redundancy gate permits it.

## Residual-runtime determinism

### Assumption

Under the pinned runtime, semantic tape, canonical schedule, pure node functions,
commutative sorted branch merge, fixed process environment, and fresh isolation,
all scientific coordinates are deterministic. Thread completion, wall clock,
runtime UUIDs, unordered container iteration, and hash randomization are excluded
from those coordinates.

### Replay test

Before validation, all 12 structural archetypes × four inputs × three tapes ×
four conditions run twice in fresh processes: 1,152 tuning-only executions. Each
duplicate pair must be byte-identical on:

1. full pre-action state;
2. compiled action input channels;
3. semantic event trace;
4. `B_actual`;
5. `V_prov`; and
6. terminal state.

Environment fixes include `PYTHONHASHSEED=0`, locale `C`, timezone `UTC`, no
network/telemetry/cache, fresh temporary directory, and CPU-only execution.

Any mismatch blocks the one-run-per-cell validation estimand. This hypothesis
does not silently switch to repeated stochastic estimates. A distributional
redesign would require a new contract and hypothesis.

## Assumptions and validity domains

| ID | Assumption | Validity domain | Consequence outside domain |
|---|---|---|---|
| A1 | `B_actual` contains every benign task output and actual effect | Exact inert tasks and eleven-key task state | Apparent security-only difference may be functional; invalidate |
| A2 | Provenance is security state, not required task output | Four declared input/task contracts only | If task consumes provenance, it must enter `B_actual` and the fiber claim changes |
| A3 | Pinned source paths implement node schema projection as inspected | LangGraph object `95af6a...` and exact API subset | Treatment is inauthentic; stop, no adapter substitute |
| A4 | Primary conditions differ only by the named input-schema projection | Every treatment-fidelity table row passes | Any extra difference invalidates causal attribution |
| A5 | Pre-action observer is read-only and noninterfering | Fixed observer code and trace schema | Observer-induced behavior invalidates evidence |
| A6 | Source-identical callable uses no provenance side channel | No runtime context/config/store/global fallback | Hidden access collapses the treatment contrast |
| A7 | Full-state provenance bytes are identical before projection | Exact pre-action byte equality | Different starting states confound the effect |
| A8 | `OMST-PROV-1` is an adequate implementation of the declared abstract policy | Exact 17 clauses and finite fixtures only | No broader provenance-security conclusion |
| A9 | Independent representations reduce implementation common mode | No shared parser/object/helper/answer table | Agreement may duplicate a bug; invalidate after review |
| A10 | Clause fixtures and mutants adequately test every atomic predicate | Fixed 17+2 mutation set and all 2×2 cells | Surviving or uncovered clause blocks validation |
| A11 | Generator mapping uniquely fixes all validation bytes | `OMST-GEN-1`, config hash, IDs 0..119 | Outcome-tunable census invalidates confirmation |
| A12 | Decision tapes map totally by semantic obligation | Exact tape ledger equality | Different decisions/compute confound pairing |
| A13 | Runtime behavior is deterministic on scientific coordinates | Replay gate passes 100% on 1,152 tuning runs | One-run causal estimand invalid; new design required |
| A14 | Fresh processes eliminate condition interference | Fixed CPU/environment/isolation policy | Hidden state or cache defeats paired attribution |
| A15 | Every validation unit has complete all-condition common support | Exactly 1,440 units and 5,760 executions | One failure invalidates entire census |
| A16 | Graph strata define only a finite workload census | Exact 12 strata and ten replicates | No production or unseen-topology prevalence claim |
| A17 | Ten points is a project materiality threshold | This internal finite decision | Not a field standard or estimated operational risk |
| A18 | The large census adds information beyond a structural witness | Non-redundancy gate says context dependence remains | If false, stop after minimal witness and downgrade claim |

## Fixed bias surface

1. **Selection.** `OMST-GEN-1`, graph IDs, templates, tapes, and order uniquely
   fix every scheduled byte before outcomes. All conditions run on every unit.
   Common support must be 100%; no favorable subset or unsafe-base mixture enters.
2. **Confounding.** Conditions 3/4 share full pre-state, graph, code, tape,
   effect, schedule, checkpoint/middleware, and environment. Exact treatment
   fidelity permits only the provenance input channel to differ. Any other
   difference invalidates rather than adjusts the claim.
3. **Allocation/assignment.** This is complete within-unit assignment. Every
   unit receives all four conditions; cyclic Latin order depends only on graph
   ID and is exactly balanced.
4. **Protocol deviation.** Exact source object, generator/config hash, command,
   environment, terminal semantics, replay gate, and immutable paths are checked.
   A scientific change after outcome access creates a new version/iteration.
5. **Missing data.** Any timeout, crash, malformed event, incomplete terminal
   record, common-support loss, treatment mismatch, or replay mismatch invalidates
   the whole census. No available-case estimate, imputation, or recoding.
6. **Measurement.** Exact event schema, 17-clause automaton, independent
   state-machine/relational implementations, per-clause fixtures, 2×2 cells, and
   100% 19-mutant kill are mandatory. Large `n` cannot rescue oracle failure.
7. **Analysis flexibility.** The graph-equal condition-4-minus-3 estimand,
   10-point threshold, 100-point structural prediction, invalid states, controls,
   and non-redundancy stopping rule are fixed. Secondary tables cannot rescue a
   subthreshold or redundant result.
8. **Selective reporting.** All tuning gate outcomes, all 5,760 scheduled states
   if run, four condition rates, fidelity predicates, evaluator disagreements,
   fixtures, mutants, and later replication are retained. No best-stratum,
   best-family, or best-framework substitution.

## Rival explanations and discriminating checks

| Rival | Why it could mimic the effect | Fixed check | Impact if unresolved |
|---|---|---|---|
| Adapter-authored omission | Custom adapter, not LangGraph, could remove provenance | Pinned source/API path and compiled channel audit; no adapter reconstruction | Stop or rename as adapter result |
| Different starting provenance | Primary conditions may enter with unequal records | Full pre-action canonical bytes and channel-version equality | Invalidate census |
| Different action code | Schema-specific wrappers may differ | One callable/code hash; only schema type differs | Invalidate causality |
| Hidden provenance side channel | Task-only action might read context/store/global | Static/runtime dependency audit and forbidden surfaces | Invalidate treatment |
| Observer interference | Instrumentation may alter state or schedule | Read-only observer tests and state hash before/after observation | Invalidate measurement |
| Generic extra-node exposure | Added node alone may cause violation | Node-only exact-zero control | No schema mediation claim |
| Actual-effect difference | Security finding may be ordinary capability change | Full ordered effect log in `B_actual`; capability exact | Invalidate common support |
| Predicate self-fulfillment | Oracle may simply declare missing field unsafe | Policy grounding, exact clauses, negative/positive fixtures, and explicit triviality limit | Narrow to abstract-policy witness; no broad security claim |
| Common-mode evaluator bug | Independent checkers may share specification error | Different representations, clause mutations, code review | Invalidate or downgrade |
| Generator targeting | Fixed grammar may manufacture favorable cases | Byte-fixed finite-census scope and stratum report | No production prevalence claim |
| Runtime nondeterminism | Branch scheduling or IDs may change trace | 1,152-run duplicate replay gate | Block one-run census |
| Structural tautology | Treatment plus oracle may force result | Phase-3 non-redundancy gate | Stop large census; report deterministic witness only |
| Version specificity | Later releases may behave differently | Exact object claim; separate replication | No universal framework claim |

## Metrics and decision rules

| Outcome | Metric | Support | Disconfirm | Invalid/stop |
|---|---|---|---|---|
| Material schema effect | `Delta_schema_pp` | `>=10.0` on informative valid census | `<10.0` valid census | any gate failure or non-redundancy stop |
| Structural prediction | absolute error from 100 pp | exactly `0.0` pp error | any nonzero error teaches model mismatch | protocol invalid |
| Non-redundancy | context dependence after source+minimal fixture | explicit remaining runtime uncertainty | N/A | no uncertainty: stop census, deterministic witness only |
| Common support | valid units / 1,440 | exactly `1.0` | N/A | below `1.0` |
| Identity | `q_identity` | exactly `0.0` | N/A | nonzero |
| Node-only | `q_node_only` | exactly `0.0` | N/A | nonzero |
| Task equality | four-way `B_actual` equality | exactly `100%` | N/A | any mismatch |
| Treatment fidelity | table rows and channel-set difference | all exact; difference `{provenance_record}` | N/A | any failure |
| Replay | duplicate byte-match fraction | exactly `1.0` | N/A | below `1.0` |
| Oracle coverage | clause fixtures passed | exactly `100%` | N/A | any failure |
| Mutation adequacy | killed fixed 17+2 mutants | exactly `100%` | N/A | any survivor |

A valid value below threshold is disconfirmation, not inconclusive. Protocol
invalid means the question was not tested. Non-redundancy stop means the narrow
mechanism has a deterministic witness but a large empirical rate would add no
scientific signal.

## Evidence chain and novelty boundary

The closest empirical priors remain ReliabilityBench's action/end-state
metamorphic relations over 1,280 episodes and ASSURE's behavioral/security
metamorphic testing of six browser extensions with 531 reported issues
([ReliabilityBench](https://arxiv.org/abs/2601.06112),
[ASSURE](https://arxiv.org/abs/2507.05307)). The 2026 systematic survey and
LLMORPH establish a mature metamorphic-testing field and relation-validity risk
([survey](https://arxiv.org/abs/2605.13898),
[LLMORPH](https://arxiv.org/abs/2603.23611)).

Long-horizon, harness, graph, and security papers motivate the runtime surface
but do not predict the schema effect: *Towards Long-Horizon Agents*, MASEval,
FlowSteer, Agentic Harness Engineering, LoopTrap, Agent-BOM, and MaMa
([survey manuscript](https://www.preprints.org/manuscript/202607.1328),
[MASEval](https://aclanthology.org/2026.acl-demo.34/),
[FlowSteer](https://arxiv.org/abs/2605.11514),
[AHE](https://arxiv.org/abs/2604.25850),
[LoopTrap](https://arxiv.org/abs/2605.05846),
[Agent-BOM](https://arxiv.org/abs/2605.06812),
[MaMa](https://arxiv.org/abs/2602.04431)).

The novelty is not “metamorphic testing plus security,” not discovery that an
omitted field is unavailable, and not a new authorization theory. The narrow
contribution under test is a source-authentic schema-closure relation with exact
task/security fibers, treatment-fidelity predicates, clause-complete oracles,
and a rescue control. If Phase 3 proves that this collapses to a trivial static
fact, novelty is correspondingly downgraded and OMST concludes without a large
experiment.

## Idea taxonomy

- **Opportunity pattern:** Scope Mismatch, secondary Evidence Gap.
- **Method paradigm:** Empirical Mapping with a deterministic verification
  subclaim.
- **Dominant operation:** `decouple`.

The local move separates task-schema sufficiency from security-schema closure at
one source-backed framework boundary. It is not Bridge×Synthesis and does not
integrate defenses. ReliabilityBench or ASSURE would require a new internal
schema treatment, exact channel-fidelity audit, and task/security coordinate
split to estimate this relation.

## Anti-stacking and Occam checks

There is one treatment coordinate and no defense stack. The distinguishing
prediction over a generic graph fuzzer plus checker is the matched rescue under
an exact one-channel compiled difference, with task effects and negative controls
fixed.

Occam's strongest challenge is that one compiled-channel audit and one minimal
fixture may answer the question. The non-redundancy gate accepts that challenge:
if the minimal witness exhausts the uncertainty, the 120-graph census is removed
from the path. The design refuses to equate more executions with more science.

## Predicted failure modes

1. Pinned source differs from inspection; treatment inauthentic, stop.
2. Compiled channels differ by more than provenance; causal claim invalid.
3. Task-only accesses provenance through a side channel; treatment collapsed.
4. Actual effects or task state differ; common support fails.
5. Identity/node-only violate; generic instrumentation/exposure explanation wins.
6. Oracle clause fixture or mutant survives; measurement invalid.
7. Independent evaluators disagree; no security conclusion.
8. Replay differs; one-run estimand invalid.
9. Minimal witness makes effect definitional; large census stops as redundant.
10. Informative valid census returns below 10; materiality refuted.
11. Valid result is 10–99.99; materiality holds but structural model is wrong.
12. Result is fixed to the abstract policy/grammar; no deployment prevalence.

## Self-critique and re-derivation

The causal logic is:

1. Both primary conditions begin with identical full state including provenance.
2. Pinned compilation projects node inputs according to their schema channels.
3. The schemas differ only by `provenance_record`.
4. The source-identical action records the digest it actually receives and
   performs the same inert effect.
5. The declared policy requires the effect's digest to match the pre-boundary
   provenance digest.
6. Therefore full-schema action should pass and task-only action should fail,
   while `B_actual` remains equal.
7. Paired graph/input/tape averaging then yields the finite contrast if, and
   only if, graph context can still change that outcome.

Step 6 exposes the study's central weakness: given the action and policy rules,
the result may be entailed. That is why Phase 3 must test non-redundancy before
the validation census. A deterministic source witness would still establish a
useful schema-closure control, but it would not be an empirical frequency
discovery or a top-venue result.

The second strongest objection is construct self-fulfillment: we define missing
provenance as a violation. The response is a claim downgrade, not rhetoric. The
conclusion can only be “this schema projection violates OMST-PROV-1,” grounded as
an abstract provenance/authorization policy. It cannot become “the framework is
unsafe” or “real agents are exploitable.”

The third objection is that independent code shares a specification. That is
unavoidable for a construct-defined predicate. Separate representations,
fixtures, and mutants reduce implementation errors but cannot prove the policy
is universally correct. The validity domain states that limit.

## Review-resolution matrix

| Review issue | v3 response | Author status |
|---|---|---|
| R1-1 estimand/weighting | exact 1,440-unit support; 1/12 then 1/120 weights | RESOLVED |
| R1-2 task/security overlap | all actual effects in `B_actual`; provenance-only `S_prov` | RESOLVED |
| R1-3 causal mechanism | source-backed one-channel schema projection and fidelity table | RESOLVED |
| R1-4 independent oracle | state-machine versus relational checker, 2×2 fixtures, clause mutations | RESOLVED |
| R1-5 evidence/taxonomy | direct closest-prior comparison; Scope Mismatch × Empirical Mapping × decouple | RESOLVED |
| R1-6 census | exact pin, generator, bytes, IDs, topology, inputs, tapes, order, isolation | RESOLVED |
| R1-7 assumptions/terminology | 18 regimes; defined fiber; no congruence | RESOLVED |
| R2-1 exact `V_prov` | exact 11-field schema, four accepted paths, P01–P17, protocol-invalid split, fixtures/mutations | RESOLVED |
| R2-2 treatment fidelity | exact code paths, schemas, callable rule, pre/boundary/post table, compiled channel predicate | RESOLVED |
| R2-3 deterministic census | OMST-GEN-1 SHA-256 map, exact graph grammar/input/tape/order/serialization | RESOLVED |
| R2-4 runtime randomness | explicit assumption plus 1,152-run byte-replay gate; no silent distributional switch | RESOLVED |

These statuses are author claims. The next independent reviewer must grade the
four round-2 blockers and check whether triviality or observer instrumentation
introduces a new fatal defect.

## Gate Check before theory review

- Falsifiable claim, four conditions, IV/DV, controls, expected direction,
  derived point prediction, and one primary comparison: complete.
- Search dimension: same Cycle-2 iteration-5
  `orchestration-rewrite-relation`, `kind: metric`; no duplicate entry.
- Concept: named, plain-language, and formally defined.
- Empirical/systems justification: pinned mechanism, exact fidelity predicate,
  event schema/automaton, deterministic generator, replay gate, 18 assumptions,
  eight fixed bias items, and 13 rivals.
- Failure/disconfirm/invalid/redundant-stop outcomes: separated.
- Metrics: exact threshold, point calibration, controls, support, fidelity,
  replay, oracle coverage, and mutation adequacy.
- Taxonomy: Scope Mismatch × Empirical Mapping × `decouple`.
- Anti-stacking: one-channel rescue prediction; no component stack.
- Occam: minimal-witness non-redundancy stop prevents redundant large execution.
- Problem alignment: confirmation or a deterministic witness would identify an
  independently checkable schema-closure control for preserving provenance
  across an orchestration rewrite, while an invalid or null result would reject
  that control within the finite proxy.
- Theory review: **PENDING**. No Phase-3 source execution or PoC is permitted
  before RIGOROUS.

## Decision

Commit and deterministically verify v3. Because the ordinary two-review
escalation point has been reached, use the user's standing instruction—`go, dont
ask me these questions again, go iterate and improve yourself`—as the explicit
escalation resolution for one further sterile review within the user-raised
20-round project budget. Charge the round only at dispatch.

## Next Steps

1. Verify config/hypothesis agreement, 17 clauses and mutants, 18 assumptions,
   eight bias items, 11 resolution rows, arithmetic, source paths, no placeholders,
   and immutable predecessor artifacts.
2. Dispatch a sterile review with the four round-2 blockers in the previous-issue
   slot.
3. Proceed to Phase 3 only after RIGOROUS with scrutiny; otherwise record the
   adverse verdict before any further revision.
