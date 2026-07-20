# Hypothesis — iteration 5, OMST v6 quotient correspondence control

**Date:** 2026-07-20  
**Phase:** 2 — hypothesis formation  
**Cycle:** 2  
**Status:** superseding theoretical hypothesis, not yet reviewed  
**Claim type:** formal derivation plus an independent, falsifiable engineering
correspondence proposition  
**Scope:** record reconstruction and schema sufficiency relative to the declared
target `tau`

## Supersession and adverse-result record

This artifact supersedes but does not edit hypotheses v1-v5:

- `research-log/056-hypothesis-iter-5-omst-v1.md`;
- `research-log/060-hypothesis-iter-5-omst-v2.md`;
- `research-log/064-hypothesis-iter-5-omst-v3.md`;
- `research-log/068-hypothesis-iter-5-omst-v4-schema-closure.md`; and
- `research-log/072-hypothesis-iter-5-omst-v5-factorization.md`.

Their reviews are preserved verbatim in `research-log/058`, `062`, `066`,
`070`, and `074`. In particular, round 5 returned `NEEDS_REVISION` after finding
the abstract theorem and restricted consequence correct. It required six
repairs:

1. a literal executable LangGraph subject;
2. a source-derived deterministic correspondence rather than inference from one
   run;
3. removal of finiteness/nonemptiness and correction of the reachable-image
   role;
4. complete typing of `J`, `Y`, and both projections;
5. consistent separation of the independent correspondence proposition and
   optional full-schema control; and
6. record-reconstruction/schema-sufficiency scope rather than general security.

The c2-v6 amendment in `research-log/075` accepts all six. The normative
machine-readable specification is
`experiments/configs/omst-c2-v6-quotient-control.json`, and the active contract
is `experiments/configs/evaluation-contract-orchestration-c2.md`.

## One-sentence hypothesis

For any total projection, an exact state target is reconstructible by a
deterministic function of the projected input exactly when the target is
constant on the projection fibers; for the pinned two-state provenance witness,
the task-only projection is therefore insufficient, and pinned LangGraph 1.2.9
implements that projection only if the separately stated source correspondence
proposition holds.

## Claims and nonclaims

### Claimed

1. A minimal unique-factorization theorem over arbitrary sets, including the
   empty domain.
2. A fully typed two-state consequence quantifying over every total
   deterministic function of the declared task input.
3. A semantic schema-sufficiency criterion: `ker(pi) subseteq ker(tau)`.
4. A closed source proposition `C_task` for one exact LangGraph fixture.
5. A separate optional positive-control proposition `C_full`.

### Not claimed

- a new theorem in information-flow, dependency, set, quotient, or category
  theory;
- a scientific prediction, causal effect, empirical frequency, prevalence, or
  benchmark result;
- a general security failure, framework vulnerability, production provenance
  requirement, or complete security policy;
- universal necessity of a field literally named `provenance_record`;
- coverage of hidden context not included in the actual input projection;
- that one execution proves determinism;
- that source correspondence has been runtime-confirmed;
- standalone top-tier novelty; or
- any framework download/install/run, Kaggle, held-out or locked-test action,
  live-target test, operational attack, model API, external message, or
  publication.

## Research questions

### Q1 — minimal theorem

For sets `S,Y`, total `pi:S->Q` with `Q=image(pi)`, and total `tau:S->Y`, is

```text
exists unique g:Q->Y such that tau=g composed_with pi
```

equivalent to

```text
for all s,s' in S, pi(s)=pi(s') implies tau(s)=tau(s')?
```

### Q2 — fully typed witness

When the only two full states have the same task tuple but different canonical
provenance bytes, can any total deterministic function of only the task tuple
reconstruct the correct provenance bytes on both?

### Q3 — independent framework proposition

For the literal graph and fixed fresh-run state below, does pinned LangGraph
1.2.9 construct equal callable-entry inputs under `TaskStateOnly` and inputs
differing only at `provenance_record` under `TaskStatePlusProvenance`?

The proof of Q1 answers Q2. It does not logically answer Q3. Q3 requires the
pinned source correspondence derived later in this artifact.

## Formal objects

Let:

```text
S     an arbitrary set of full states
Y     an arbitrary target-output set
pi    a total function S->Q
Q     image(pi), by definition
tau   a total function S->Y
g     a candidate total function Q->Y
```

Define the kernel relation of a function `h` by:

```text
(u,v) in ker(h) iff h(u)=h(v).
```

Define projection closure relative to `tau` by:

```text
closed(pi,tau) iff ker(pi) subseteq ker(tau).
```

Equivalently, `tau` is constant on each fiber
`F_q={s in S:pi(s)=q}`.

No probability, sample, event trace, effect size, threshold, verdict, digest,
missing-value sentinel, action-authored oracle, or framework object appears in
the theorem.

## Minimal unique-factorization theorem

### Statement

For the formal objects above:

```text
exists unique total g:Q->Y with tau=g composed_with pi
iff
closed(pi,tau).
```

### Necessity

Assume `tau=g composed_with pi`. Take arbitrary `s,s' in S` with
`pi(s)=pi(s')`. Then:

```text
tau(s)
= g(pi(s))
= g(pi(s'))
= tau(s').
```

Thus every pair in `ker(pi)` belongs to `ker(tau)`, so
`closed(pi,tau)` holds.

### Sufficiency

Assume `closed(pi,tau)`. Define a relation `G` on `Q cross Y`:

```text
(q,y) in G iff there exists s in S with pi(s)=q and tau(s)=y.
```

For every `q in Q=image(pi)`, a representative `s` exists, and totality of
`tau` supplies a value `y`. If representatives `s,s'` supply `y,y'`, then
`pi(s)=pi(s')=q`; closure gives `tau(s)=tau(s')`, so `y=y'`. Therefore `G` is
the graph of a total function `g:Q->Y`.

For every `s in S`, the definition gives `g(pi(s))=tau(s)`. Hence
`tau=g composed_with pi`.

This construction uses no global choice principle: existence and uniqueness of
the value for each `q` define the function directly.

### Uniqueness

Suppose `g1,g2:Q->Y` both factor `tau`. For arbitrary `q in Q=image(pi)`, choose
the existentially guaranteed `s` with `pi(s)=q`. Then:

```text
g1(q)=g1(pi(s))=tau(s)=g2(pi(s))=g2(q).
```

Thus `g1=g2`.

## Validity domains and boundaries

### Empty domain

If `S` is empty, `Q=image(pi)` is empty. The only `tau` and `g` are empty
functions, closure is vacuous, and unique factorization holds. Nonemptiness is
not assumed.

### Infinite domain

The proof never enumerates `S`, so finiteness is not assumed.

### Injective and constant projections

If `pi` is injective, every fiber has at most one member and closure is
automatic. If `pi` is constant on a nonempty domain, closure is exactly
constancy of `tau`.

### Larger action domain

Let a separate `Q0` strictly contain `image(pi)`. Closure still defines a
unique factor on `image(pi)`. If `Y` has an element, it can be extended to all
of `Q0` by assigning arbitrary values off the image. Such extension values are
not determined by `tau`, so uniqueness generally fails. This does not weaken
the stated theorem because its `Q` is defined as the image.

### Partial, randomized, or stateful behavior

The theorem is about total functions. Partial actions require explicit error
semantics or a restricted domain. A randomized/history-dependent action must
include its seed/history in the modeled input if it is to be represented by a
function on one invocation state. This is a domain boundary, not an implicit
purity assumption.

## Fully typed two-state witness

### Types and values

Let `P={p0,p1}`, where:

```json
{"entity_id":"entity-0","activity_id":"activity-0","agent_id":"agent-0"}
{"entity_id":"entity-0","activity_id":"activity-0","agent_id":"agent-1"}
```

Let `B` be the set of canonical JSON byte strings, and let `J:P->B` serialize
with UTF-8 `json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=True,
allow_nan=False)` and no trailing newline. The exact results are:

```text
J(p0)={"activity_id":"activity-0","agent_id":"agent-0","entity_id":"entity-0"}
J(p1)={"activity_id":"activity-0","agent_id":"agent-1","entity_id":"entity-0"}
```

These byte strings are unequal. No global injectivity claim about JSON is
needed.

Let `X={x}`, where `x` is exactly:

```json
{"subject_id":"subject-0","task_value":"ready","effect_id":"effect-0","effect_log":[],"completion":"pending"}
```

Now define:

```text
S = X cross P
Y = J(P), an exact two-element subset of B

tau:X cross P->Y                    tau(x,p)=J(p)
pi_task:X cross P->X                pi_task(x,p)=x
pi_full:X cross P->X cross P        pi_full(x,p)=(x,p)
g_full:X cross P->Y                 g_full(x,p)=J(p)
```

### Task-side universal consequence

Both witness states occupy the same `pi_task` fiber, but their `tau` values
differ. Closure fails. By the theorem:

```text
for every total deterministic g_task:X->Y,
g_task composed_with pi_task differs from tau on at least one state.
```

This is not the observed failure of one selected action. It excludes every
function on the one declared task input by a same-input/different-target
contradiction.

### Full positive construction

Every `pi_full` fiber is a singleton. Closure holds, and the declared
`g_full(x,p)=J(p)` factors `tau`. This is constructive sufficiency for the exact
record-reconstruction target only.

## Semantic schema sufficiency

For any actual action projection `pi_actual`, record reconstruction relative to
`tau` is possible exactly when `ker(pi_actual) subseteq ker(tau)`.

The criterion concerns delivered information, not field names. Another field
could encode the record and make reconstruction possible. A declared record
field could be unavailable or mapped away. Configuration, store, closure,
global, context, prior state, and history also belong to `pi_actual` whenever
the action can read them.

Therefore the witness does not prove that every system must expose raw
provenance, that reconstruction is a complete security policy, or that the
framework is insecure. It isolates schema sufficiency for one exact `tau`.

## Literal LangGraph subject

The future correspondence subject is the following exact Python program shape.
This text has been parsed for syntax without importing LangGraph.

```python
from __future__ import annotations

import json
from copy import deepcopy
from typing_extensions import NotRequired, TypedDict
from langgraph.graph import END, START, StateGraph


class ProvenanceRecord(TypedDict):
    entity_id: str
    activity_id: str
    agent_id: str


class TaskStateOnly(TypedDict):
    subject_id: str
    task_value: str
    effect_id: str
    effect_log: list[dict[str, object]]
    completion: str


class TaskStatePlusProvenance(TaskStateOnly):
    provenance_record: ProvenanceRecord


class GraphState(TaskStatePlusProvenance):
    received_input: NotRequired[str]


def capture(state: dict[str, object]) -> dict[str, str]:
    received = json.dumps(
        state,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return {"received_input": received}


def build(schema):
    builder = StateGraph(GraphState)
    builder.add_node(
        "capture",
        capture,
        input_schema=schema,
        defer=False,
        retry_policy=None,
        cache_policy=None,
    )
    builder.add_edge(START, "capture")
    builder.add_edge("capture", END)
    return builder.compile()


result = build(schema).invoke(deepcopy(state), config=None)
observed = result["received_input"].encode("utf-8")
```

`state` is exactly `s0` or `s1` from the v6 JSON. `schema` is exactly
`TaskStateOnly` or `TaskStatePlusProvenance`. The four cells execute in this
fixed order only after authorization:

1. `TaskStateOnly,s0`;
2. `TaskStateOnly,s1`;
3. `TaskStatePlusProvenance,s0`; and
4. `TaskStatePlusProvenance,s1`.

Each cell requires a fresh Python process, fresh temporary directory, freshly
constructed graph, one invocation, no network, and no reused graph, channel,
checkpoint, cache, input mapping, or instrumentation object.

## Source-derived correspondence proof

### Pinned source subject

The subject is LangGraph tag `1.2.9`, commit object
`95af6a00718588e7b7ce17310e8006d267896a77`. The relevant official files are:

- `libs/langgraph/langgraph/graph/state.py`;
- `libs/langgraph/langgraph/pregel/_read.py`; and
- `libs/langgraph/langgraph/pregel/_algo.py`.

The derivation is about this source and exact fixture only. Any source/hash or
postcondition mismatch rejects correspondence rather than changing the
theorem.

### D1 — channel construction

`StateGraph(GraphState)` registers the enclosing schema. For unannotated
`TypedDict` fields, `_get_channels` constructs `LastValue` channels. The two
explicit node input schemas are also registered by `add_node`.

The expected node channel keys, in declaration order, are:

```text
TaskStateOnly:
subject_id, task_value, effect_id, effect_log, completion

TaskStatePlusProvenance:
subject_id, task_value, effect_id, effect_log, completion, provenance_record
```

If source inspection yields any other key, type, alias, reducer, or order, the
fixture is rejected.

### D2 — compiled node input

`add_node(..., input_schema=schema)` stores the explicit schema.
`CompiledStateGraph.attach_node` derives `PregelNode.channels` from that schema.
For these `TypedDict` schemas, input is already a mapping; no model-coercion
mapper is required. The admissible postcondition is `proc.mapper is None`.
Any non-`None` mapper rejects this literal correspondence subject rather than
being assumed pure.

### D3 — absent retained services

The literal builder never supplies a checkpointer, cache, store, context schema,
retry, error handler, or cache policy. The admissible compiled postcondition is
that checkpointer, cache, and store are absent and the capture node has no retry
or cache policy. Any retained service rejects the subject.

### D4 — fresh invocation state

Each cell begins in a fresh process, constructs a new graph, and passes a deep
copy of one literal input. Consequently no Python object, compiled graph,
channel instance, checkpoint, or invocation-local input cache is shared across
cells. At task preparation, the checkpoint/channel versions and empty
`input_cache` must be captured and checked before the PULL task. Any prior value
or unavailable selected channel rejects the subject.

### D5 — normal PULL path

On the admissible path, `prepare_single_task` calls `_proc_input` for the
`capture` PULL task. `_proc_input` reads each available selected channel, uses
the compiled aliases, applies no mapper, and returns the task-owned mapping.
`prepare_single_task` stores that value in `PregelExecutableTask.input`; the
bound `capture` callable receives that input.

This is the normal PULL path. An explicit `ChannelRead.do_read` observation or
a compiled channel list is not substituted for callable input.

### D6 — capture and hidden-context control

`capture` has one argument, no closure, no mutation, no store/config/runtime
parameter, and only the fixed `json` module as a global dependency. It
canonicalizes the received mapping before returning its first and only write.
The input states contain only strings, an empty list, and nested string
mappings, so no custom serializer or mutable object hook can distinguish them.

`config=None`, fresh process isolation, disabled network, fixed locale/timezone,
and recorded Python/JSON/environment hashes rule out a declared second input.
Unexpected callbacks, tracing, environment-dependent wrappers, or globals are
rejection conditions. Even if passive instrumentation is present, the recorded
claim is the pre-write callable argument, not timing or trace output.

### D7 — derivation of the propositions

For `TaskStateOnly`, D1-D6 select exactly the five task coordinates. Those five
values are byte-identical in `s0,s1`; canonical serialization of equal mappings
is equal. Therefore:

```text
C_task:
received(TaskStateOnly,s0)=received(TaskStateOnly,s1).
```

For `TaskStatePlusProvenance`, D1-D6 select the same five coordinates plus the
record. The records differ only at `agent_id`; all other selected values are
equal. Therefore:

```text
C_full:
received(TaskStatePlusProvenance,s0)
and received(TaskStatePlusProvenance,s1)
differ exactly at provenance_record.agent_id.
```

This is a source-derived equality under explicit postconditions. The future
four executions may check the derivation but cannot create it. If any
postcondition fails, no result is reported as confirming correspondence.

## Logical roles and failure semantics

`C_task` is load-bearing for applying the two-state impossibility to the pinned
runtime. If it fails, the actual task projection is not the declared `X`, and
the LangGraph application is rejected.

`C_full` is an optional positive control for deliverability and the constructive
full factor. If only `C_full` fails, the task-side application can remain valid;
the positive control is rejected separately.

The cross-schema check requires, for each witness state, that the task input
equals the full input with `provenance_record` removed. Failure rejects the exact
one-coordinate correspondence treatment but does not falsify the abstract
theorem.

No runtime result produces a security verdict, effect estimate, frequency,
population inference, or proof of determinism.

## Assumptions and rejection conditions

| ID | Premise | Role | Failure consequence |
|---|---|---|---|
| A1 | `pi` and `tau` are total functions on `S` | States the theorem's equality domain | Partial/multivalued cases need another theorem. |
| A2 | `Q` is defined as `image(pi)` | Makes the factor canonical and unique | A larger domain needs an extension statement; existence on the image remains. |
| A3 | Candidate behavior is a function of modeled input | Same modeled input has one output | Include randomness/history/context in the input or leave the theorem's domain. |
| A4 | `J:P->B` is exact and `J(p0)!=J(p1)` | Types and separates the witness targets | The two-state consequence does not follow without target separation. |
| A5 | The literal schemas compile to the D1/D2 postconditions | Binds the runtime projection | Reject correspondence if channels or mapper differ. |
| A6 | Each run satisfies D3/D4 isolation | Removes retained distinguishing state | Reject the affected runtime cell. |
| A7 | Normal PULL preparation satisfies D5 | Connects channels to callable input | Reject correspondence if another path constructs the input. |
| A8 | Capture and environment satisfy D6 | Makes the recorded argument stable | Reject runtime correspondence if hidden context or mutation enters. |

A1-A4 carry the theorem/witness. A5-A8 carry only the pinned framework
proposition. No framework assumption is smuggled into the abstract proof.

## Rival explanations and controls

1. **Derived alias:** another task field determines `J(p)`. The artificial
   product witness fixes identical task fields and different targets; a real
   alias would mean the real domain is not this witness.
2. **Mapper transformation:** a mapper drops, adds, or coerces values. The source
   gate requires `mapper is None`; otherwise correspondence is rejected.
3. **Unavailable channel:** `_proc_input` omits an unavailable selected channel.
   Availability is captured before the PULL task; omission rejects the cell.
4. **Input-cache reuse:** cached input explains equality or difference. Fresh
   process/graph and empty-cache snapshot are mandatory.
5. **Checkpoint/history reuse:** prior state distinguishes cells. No
   checkpointer is permitted, and each cell is process-isolated.
6. **Mutable capture:** later state mutation changes the logged object. Capture
   serializes before its first write and stores a string.
7. **Configuration/store/global context:** action sees an unmodeled coordinate.
   The literal callable has no such parameter or closure; source/environment
   inspection rejects unexpected paths.
8. **Instrumentation interference:** observation injects state. The callable's
   own first computation is the capture; no observer node or event machine is
   present.
9. **Canonicalization ambiguity:** serializer differences explain target or
   input difference. Exact Python/stdlib hashes and serializer arguments are
   fixed; only primitive JSON values are used.
10. **Full-control failure:** full schema does not deliver the record. This
    rejects `C_full` only and is not misreported as refuting `C_task`.
11. **Researcher-chosen obligation:** `tau` was selected to expose the missing
    coordinate. Conceded; this is a schema-sufficiency control, not independent
    empirical security evidence.
12. **Classical result:** fiber factorization is known structure. Conceded; the
    local value is the exact runtime correspondence protocol.

## Fixed bias surface

| Bias | Mitigation |
|---|---|
| Confirmation | Sterile reviewer must independently prove or countermodel the theorem and may reject any source postcondition. |
| Selection | The witness is explicitly purpose-built and not represented as a sample. |
| Measurement | Observable is only canonical callable-entry bytes; no action-authored verdict. |
| Leakage | Expected target is not passed to the action; task equality is derived from literal state. |
| Implementation | Exact classes, topology, config, freshness, and rejection conditions are normative. |
| Analysis flexibility | Pairwise equal/different relations and role-specific failures are fixed before execution. |
| Novelty inflation | Classical theorem and engineering-control scope are explicit. |
| Generalization | No prevalence, framework-wide, production, or security-policy inference is allowed. |

## Taxonomy, anti-stacking, and Occam

The taxonomy is `Scope Mismatch × Formal Derivation × formalize`, with
`decouple` secondary. It is not `Bridge × Synthesis`: no independent techniques
are stacked into a new method.

Anti-stacking passes only in the narrow logical sense. Testing one selected
action would show failure of that action. The theorem, plus a nonconstant fiber,
proves failure of every total deterministic function on the declared input.
That stronger quantifier is supported by proof, not by relabeling a test.

Occam's boundary is exact: two states are the smallest nonconstant fiber;
`Q=image(pi)` removes unreachable degrees of freedom; `C_full` is optional; and
no event automaton, verifier, digest, census, or effect threshold remains.

## Distinguishing logical consequences and falsifiers

### Theorem falsifier

Any well-typed model of A1-A2 where closure holds but there is not exactly one
factor, or closure fails but exactly one factor exists, falsifies the theorem.
The empty domain is included.

### Witness falsifier

Any equality `J(p0)=J(p1)`, type mismatch, or task-coordinate difference
invalidates the declared two-state consequence.

### Correspondence falsifiers

- task inputs differ within the task schema;
- compiled task channels contain provenance or omit a task coordinate;
- compiled mapper is non-`None`;
- selected channels are unavailable;
- checkpointer/cache/store/retry or prior state exists;
- `_proc_input` is not the normal callable-input path;
- the captured value is not the pre-write callable argument; or
- environment/config/global/callback state supplies another coordinate.

A source-correspondence falsifier does not falsify the theorem. It rejects its
application to this framework fixture.

## Deterministic pre-review verification plan

Before review, and without importing or running LangGraph:

1. validate the v6 JSON and `state.json`;
2. parse the literal fixture as Python syntax;
3. exhaustively check the theorem for `|S|=0..4`, three projection labels, two
   target labels, and all functions on the reachable image;
4. recompute the exact canonical witness bytes and verify they differ;
5. verify exact schema keys, four cells, two proposition roles, zero census,
   zero security verdicts, and all six review-resolution rows;
6. verify v1-v5 hypotheses and reports remain identical to their committed
   versions; and
7. scan for placeholders and forbidden execution claims.

These are document and finite-model checks. They do not execute the framework
or establish the future runtime observation.

## Review success criteria

The sterile theory reviewer must return `RIGOROUS` only after:

1. independently re-deriving necessity, sufficiency, and uniqueness;
2. checking empty/infinite-domain logic and the larger-codomain extension;
3. verifying all witness function types and the two-state universal
   consequence;
4. actively searching finite countermodels;
5. confirming that `C_task` is independent/load-bearing and `C_full` optional;
6. auditing whether the literal fixture and D1-D7 proof close source/run-state
   determinism without relying on one replicate;
7. stress-testing assumptions, rivals, taxonomy, anti-stacking, and Occam; and
8. accepting the classical novelty and record-reconstruction-only scope.

`RIGOROUS` closes Phase 2. It does not authorize source acquisition, framework
execution, Phase 3, Kaggle, or any external action.

## Round-5 disposition table

| Round-5 requirement | v6 claim before independent review |
|---|---|
| Executable closed subject | **AUTHOR-RESOLVED:** literal schemas, graph, callable, edges, compile, invoke, states, capture, and cell isolation. |
| Deterministic correspondence | **AUTHOR-RESOLVED:** D1-D7 derive equality/difference from pinned source and fixed fresh-run postconditions; runtime is only a check. |
| T1/T3 correction | **AUTHOR-RESOLVED:** no finiteness/nonemptiness; image is a domain definition for canonical uniqueness; larger-domain extension separated. |
| Complete typing | **AUTHOR-RESOLVED:** `J:P->B`, `Y=J(P)`, and every function domain/codomain are explicit. |
| Proposition/control roles | **AUTHOR-RESOLVED:** `C_task` is independent and load-bearing; `C_full` is optional. |
| Honest scope | **AUTHOR-RESOLVED:** record reconstruction/schema sufficiency relative to `tau`; no general security failure. |

These are author claims, not reviewer dispositions.

## Authorization boundary

The standing internal-iteration instruction authorizes writing, deterministic
document checking, and sterile theory review within the remaining budget. It
does not authorize framework download/install/import/run, fixture execution,
Kaggle, held-out or locked-test generation/execution, live targets, operational
attacks, model APIs, external messages, or publication.
