# OMST factorization research and c2-v5 amendment

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** c2-v4 constructed identity superseded; c2-v5 projection-fiber
factorization hypothesis activated under the standing internal-iteration default

## Trigger and scientific decision

Round-4 review accepted that c2-v4 had retired the invalid empirical census,
made the narrowed relation total, removed the observer, and removed the
incomplete generator. It independently re-derived the intended biconditional.
It nevertheless found that the result was only a co-designed identity: an
action converted field membership into `digest/null`, and a verifier converted
that same value into `PRESERVE/VIOLATE`.

The review also identified concrete formal defects: an ill-typed `E(f(q))`
expression, a countermodel that violated both A3 and A4, an unnecessary non-null
restriction, duplicated P13/P15 paths, and incomplete LangGraph correspondence
checks.

The right correction is not another event machine. c2-v5 removes the constructed
action/verifier theorem and replaces it with a classical factorization result:

> A deterministic action can satisfy a state-dependent security obligation
> using only a schema projection for every state if and only if the obligation
> is constant on every fiber of that projection.

This yields a stronger, action-independent impossibility statement. If two full
states project to the same node input but require different security outputs,
**every** deterministic action restricted to that input must fail on at least
one of them. A specific `null` branch is no longer assumed.

## Focused primary-source check

The research check used primary or author-hosted sources only. No repository
clone, package download, install, or framework execution occurred.

### Information-flow foundations

[Goguen and Meseguer (1982)](https://doi.org/10.1109/SP.1982.10014) introduced
noninterference as a way to specify when one domain's actions cannot affect what
another observes and emphasized separating security policy from the system
model that must satisfy it.

[Sabelfeld and Myers (2003)](https://www.cs.cornell.edu/andru/papers/jsac/sm-jsac03.pdf)
survey language-based information-flow security and express the core
observational idea: inputs indistinguishable at the observable level should not
produce distinguishable observable behavior. c2-v5 uses the same structural
lens but does not claim a new noninterference theorem. Its local application is
schema projection in an orchestration runtime.

### Pinned LangGraph path correction

The official LangGraph 1.2.9 source confirms the candidate correspondence but
requires a more exact path than c2-v4 stated:

1. [`StateGraph.add_node` and `CompiledStateGraph.attach_node`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/graph/state.py)
   select the node input schema and construct the compiled node's selected
   channels/mapper.
2. [`PregelNode`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_read.py)
   documents that list-valued `channels` are passed as a dictionary to the bound
   callable and that `mapper` transforms that input.
3. The normal PULL path in
   [`prepare_single_task`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_algo.py)
   constructs `val` through `_proc_input` and places it in
   `PregelExecutableTask.input` before invoking the bound node.

`ChannelRead.do_read` is useful for explicit/configured reads but is not the
decisive normal PULL-input construction path. c2-v5 therefore requires direct
audit of `_proc_input`, channel availability, mapper behavior, and the actual
mapping delivered to the callable. A compiled channel list alone is
insufficient.

## Abstract c2-v5 model

Let:

- `S` be a finite nonempty state space;
- `pi:S->Q` be a total projection with `Q=pi(S)`;
- `tau:S->Y` be a total security-obligation target; and
- `g:Q->Y` be any deterministic projected-input action.

Define the projection fiber relation:

```text
s ~_pi s' iff pi(s)=pi(s').
```

Define security closure:

```text
pi is closed for tau iff
for every s,s' in S, pi(s)=pi(s') implies tau(s)=tau(s').
```

The factorization theorem is:

```text
there exists g:Q->Y such that tau = g composed_with pi
iff pi is closed for tau.
```

Necessity follows because a deterministic `g` must return the same value on the
same projected input. Sufficiency follows by defining `g(q)` from any state in
the reachable fiber for `q`; fiber constancy makes the definition independent
of the representative.

## New insight: closure is semantic, not merely key inclusion

c2-v4 defined closure as literal inclusion of `provenance_record`. That is too
syntactic. Another delivered field might deterministically encode the same
obligation target, in which case the record key could be absent while the
projection remains sufficient.

c2-v5 therefore defines a schema as security-closed exactly when the obligation
functionally depends on the delivered projection:

```text
pi_C(s)=pi_C(s') implies tau(s)=tau(s').
```

Literal key inclusion is one way to make this true, not the universal
definition. This distinction also makes side channels conceptually clean: any
runtime context accessible to the action belongs in the actual projection. A
claimed task-only projection that exposes a store/global/closure is simply not
the modeled `pi_C`.

## Restricted provenance corollary

For the exact two-state witness in
`experiments/configs/omst-c2-v5-factorization.json`:

- both states have byte-identical task coordinates;
- their canonical provenance records differ only in `agent_id`;
- `tau(s)` is the canonical provenance-record byte string;
- the task projection maps both states to the same input; and
- the full projection retains the differing record.

Therefore the task projection is not closed for `tau`, so no deterministic
task-projected action can be correct on both states. The full projection is
closed, and `g_full(x,p)=canonical_json(p)` is one constructive correct action.

No hash, absence sentinel, condition label, event automaton, duplicated clause,
or runtime observer is needed.

## c2-v5 artifact changes

### Removed from the active theorem

- the declared `hash-if-present/null-if-absent` action;
- `R_13_15`, P13, P15, event bytes, event ordering, and condition labels;
- the E/f composition notation;
- non-null provenance as an assumption;
- A3/A4 as incorrectly independent abstract premises;
- all empirical effect-size and census language; and
- any mathematical novelty claim for the classical factorization result.

### Added

- exact reachable-image domain `Q=pi(S)`;
- projection-fiber equivalence and semantic security closure;
- the necessary-and-sufficient factorization theorem;
- a universal impossibility corollary over every deterministic
  projected-input-only action;
- explicit recognition that derived coordinates can satisfy an obligation
  without literal key inclusion;
- a two-state witness with distinct exact canonical target bytes; and
- a complete future LangGraph correspondence audit covering `_proc_input`,
  availability, mapper, received input, and bound environment.

## Round-4 requirement disposition

| Round-4 requirement | c2-v5 disposition |
|---|---|
| Separate/eliminate A3 and A4 | **RESOLVED:** removed from abstract theorem; accessible context is part of actual projection, while implementation purity moves to correspondence. |
| Concede definitional result or add distinguishing prediction | **RESOLVED:** v4 identity conceded/superseded; v5 predicts impossibility for every deterministic action on a nonconstant fiber, which one co-designed action does not establish. |
| Minimize theorem or justify duplicate paths | **RESOLVED:** one projection, one obligation, one output; P13/P15 and automaton removed. |
| Repair E/f typing | **RESOLVED BY REMOVAL:** theorem uses the well-typed equation `tau=g composed_with pi`. |
| Correct null boundary | **RESOLVED BY REMOVAL:** null is allowed whenever in the canonical domain; no absence sentinel appears. |
| Complete framework correspondence | **RESOLVED IN SPECIFICATION:** exact PULL path, `_proc_input`, availability, mapper, callable input, and bound environment are mandatory future checks. |
| State projection domain formally | **RESOLVED:** `pi` is total and `Q=pi(S)` in the theorem premises. |

## Taxonomy, novelty, and stopping

The taxonomy remains `Scope Mismatch × Formal Derivation × formalize`, with a
secondary `decouple` operation. The theorem is explicitly classical structure,
not a new mathematical contribution. The candidate local contribution is a
schema-security closure criterion plus a pinned orchestration-runtime
correspondence protocol.

A sterile reviewer must re-derive both theorem directions, test the restricted
corollary, assess whether the universal impossibility passes anti-stacking, and
decide whether the application is substantive enough to retain even as a
control. A RIGOROUS result permits at most one later two-state correspondence
fixture, not a security-effect census. An adverse result may end OMST and advance
the separately parked PDPF direction; it may not resurrect v3 or v4.

## Authorization boundary

The user's standing instruction authorizes this local theory/source correction
and another sterile review within the remaining budget. It does not authorize
framework download/install, fixture execution, Kaggle, live targets,
operational attacks, model APIs, external messages, publication, or locked-test
generation/execution.
