# OMST minimal theorem and c2-v6 correspondence amendment

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** round-5 adverse verdict accepted; c2-v6 activated under the
standing internal-iteration default; no execution authorized

## Scientific decision

Round 5 independently re-derived the abstract factorization theorem and its
two-state consequence, found no finite countermodel, and judged that the
universal quantifier narrowly passes anti-stacking. It nevertheless returned
`NEEDS_REVISION` because v5 mixed a correct elementary theorem with an open
implementation correspondence and overstated several premises and labels.

c2-v6 keeps the mathematical result but minimizes it. It also turns the
LangGraph correspondence into a closed, independently falsifiable engineering
proposition. The theorem does not depend on that proposition, and the future
runtime check will not be allowed to stand in for the source proof.

## Minimal theorem correction

For sets `S,Y`, a total function `pi:S->Q` where `Q` is **defined** as
`image(pi)`, and a total function `tau:S->Y`:

```text
there exists a unique g:Q->Y with tau=g composed_with pi
iff
ker(pi) is a subset of ker(tau).
```

No finiteness or nonemptiness assumption is used. If `S` is empty, then `Q` is
empty and the unique empty function factors the unique empty `tau`. Defining
`Q=image(pi)` makes the factor canonical and unique; it is not a load-bearing
existence assumption. On a larger separate codomain, a factor can be extended
when an output value exists, but its off-image values are generally nonunique.

## Fully typed witness

Let `P={p0,p1}` be the two exact provenance records in the normative JSON, let
`B` be the set of canonical JSON byte strings, and let `J:P->B` be the declared
canonicalizer. Let `X={x}` be the exact task-tuple singleton, `S=X cross P`, and
`Y=J(P)`.

Define:

```text
tau:X cross P -> Y                 tau(x,p)=J(p)
pi_task:X cross P -> X             pi_task(x,p)=x
pi_full:X cross P -> X cross P     pi_full(x,p)=(x,p)
g_full:X cross P -> Y              g_full(x,p)=J(p)
```

Because `J(p0) != J(p1)`, every total deterministic `g_task:X->Y` differs from
`tau` on at least one witness state. `g_full` is the unique factor through
`pi_full`. This is a universal logical consequence on the declared witness,
not an empirical prediction.

## Closed LangGraph correspondence proposition

The normative artifact now declares literal `TypedDict` classes for:

- `ProvenanceRecord`;
- the five-field `TaskStateOnly` node input;
- `TaskStatePlusProvenance`, which adds exactly `provenance_record`; and
- `GraphState`, which adds a nonrequired string capture field.

It also declares the exact capture callable, `StateGraph(GraphState)`, one
`capture` node with explicit `input_schema`, `START -> capture -> END`, default
`compile()`, exact invocation, canonicalization before the first write, and one
fresh process/graph/temporary directory per cell.

The proposition has two deliberately different roles:

1. `C_task` is load-bearing: callable inputs for `s0,s1` under
   `TaskStateOnly` are byte-identical.
2. `C_full` is an optional positive control: callable inputs under
   `TaskStatePlusProvenance` differ exactly at `provenance_record`.

Failure of `C_task` rejects the LangGraph task-side application. Failure of only
`C_full` rejects the positive control, not the task-side mathematical result.

## Determinism must be proved from source

Official LangGraph 1.2.9 source remains the primary implementation evidence:

- [`StateGraph.add_node` and `CompiledStateGraph.attach_node`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/graph/state.py)
  bind the declared node input schema to compiled channels and any mapper.
- [`PregelNode`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_read.py)
  defines channel selection and input mapping for the bound callable.
- [`prepare_single_task` and `_proc_input`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_algo.py)
  build the PULL task input and assign it to `PregelExecutableTask.input`.

Before any execution, the source-level audit must authenticate tag `1.2.9` at
object `95af6a00718588e7b7ce17310e8006d267896a77`, derive the exact channel lists
and types, prove mapper behavior, prove absent checkpointer/cache/store state,
prove fresh checkpoint/channels/`input_cache`, and show that `_proc_input`
constructs the callable argument from exactly the available selected channels.
It must also rule out configuration, callbacks, globals, closures, mutations,
history, or reused objects as distinguishing coordinates.

Only after that derivation may one execution per fixed cell check that the
runtime snapshot matches the proof. A single replicate is never evidence of
determinism.

No framework repository or package was downloaded, installed, imported, or
executed while preparing this amendment. The literal fixture may be checked as
text or parsed as Python syntax; that is not a framework run.

## Round-5 requirement disposition

| Requirement | c2-v6 disposition |
|---|---|
| Executable, closed proposition | **RESOLVED IN SPECIFICATION:** exact schemas, state, callable, graph, edges, compile, invocation, capture, cells, and run isolation are normative. |
| Source-level determinism | **RESOLVED IN SPECIFICATION:** source proof precedes execution and covers cache/checkpoint/channel/mapper/mutation and hidden-context state. |
| Remove T1 and correct T3 | **RESOLVED:** no finiteness/nonemptiness; `Q=image(pi)` is a definition for canonical uniqueness, with a separate larger-domain extension note. |
| Type `J`, `Y`, and projections | **RESOLVED:** all domains and codomains are explicit. |
| Proposition/control roles | **RESOLVED:** correspondence is independent; `C_task` is load-bearing and `C_full` is optional. |
| Honest scope | **RESOLVED:** the instance is a record-reconstruction/schema-sufficiency control relative to `tau`, not a general security failure. |

## Scope and stopping rule

The retained contribution is an elementary quotient/factorization theorem plus
a pinned engineering correspondence control. It is not a new theorem, a
framework vulnerability, a production provenance policy, an empirical effect,
or a standalone top-tier result. The taxonomy remains `Scope Mismatch × Formal
Derivation × formalize`, with `decouple` secondary.

A sterile theory reviewer must now check the minimal theorem including the
empty-domain boundary, the fully typed witness, the independence and logical
roles of `C_task`/`C_full`, and whether the source/run-state specification is
closed enough to make the future proposition executable. A `RIGOROUS` verdict
closes Phase 2 only; it does not authorize acquisition or execution. An adverse
verdict requires another immutable superseding artifact or retirement.

## Authorization boundary

The user's standing instruction authorizes this local correction and sterile
review within the remaining budget. It does not authorize framework
download/install/run, Kaggle, held-out or locked-test action, live targets,
operational attacks, model APIs, external messages, or publication.
