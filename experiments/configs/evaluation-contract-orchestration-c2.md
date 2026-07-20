# Cycle-2 orchestration-security evaluation contract

**Version:** c2-v6

**Recorded:** 2026-07-20

**Supersedes:** c2-v5 at commit `3176f32`; c2-v1 through c2-v5 remain in Git
history.

**Status:** APPROVED UNDER STANDING INTERNAL-ITERATION DEFAULT — local formal
correction and sterile review are authorized; the external and executable
actions listed at the end are not.

**Active study:** OMST record-reconstruction/schema-sufficiency control.

## Adverse-gate decision

Round 5 accepted the abstract factorization theorem and two-state universal
impossibility, found no finite countermodel, and found the anti-stacking claim
narrowly valid. It rejected v5 as a complete artifact because the LangGraph
correspondence was not executable or deterministic from fixed source/run state,
the theorem retained unnecessary assumptions, the witness was incompletely
typed, the correspondence/control roles were mixed, and “security” scope was
too broad.

c2-v6 corrects those defects without execution. Its normative machine-readable
artifact is `experiments/configs/omst-c2-v6-quotient-control.json`; rationale is
in `research-log/075`.

## Minimal abstract theorem

Let `S,Y` be sets, let `pi:S->Q` be total where `Q` is defined as `image(pi)`,
and let `tau:S->Y` be total. Define:

```text
ker(pi) subseteq ker(tau)
iff
for every s,s' in S, pi(s)=pi(s') implies tau(s)=tau(s').
```

Then:

```text
there exists a unique total g:Q->Y such that tau=g composed_with pi
iff
ker(pi) subseteq ker(tau).
```

### Necessity

If `tau=g composed_with pi` and `pi(s)=pi(s')`, functionality gives
`tau(s)=g(pi(s))=g(pi(s'))=tau(s')`.

### Sufficiency and uniqueness

For `q in Q=image(pi)`, define `g(q)=tau(s)` for any `s` with `pi(s)=q`.
Fiber constancy makes the value well-defined, and the image definition makes
`g` total. It factors `tau`. Any two factors agree at every reachable
`q=pi(s)`, so the factor is unique.

No finiteness or nonemptiness assumption is used. If `S=Q=empty`, the unique
empty `g` factors the unique empty `tau`. `Q=image(pi)` is a domain definition
that makes the factor canonical and unique, not an existence premise. For a
separate larger codomain, a factor may be extended when an output value exists,
but off-image values are not uniquely determined.

The theorem is classical quotient/function-factorization structure. No new
mathematical theorem is claimed.

## Fully typed two-state control

Let:

```text
P = {p0,p1}                         exact records in the v6 JSON
B = the set of canonical JSON byte strings
J:P->B                              exact declared canonicalizer
X = {x}                             exact task-tuple singleton
S = X cross P
Y = J(P)

tau:X cross P->Y                    tau(x,p)=J(p)
pi_task:X cross P->X                pi_task(x,p)=x
pi_full:X cross P->X cross P        pi_full(x,p)=(x,p)
g_full:X cross P->Y                 g_full(x,p)=J(p)
```

The exact canonical target bytes differ only because `agent_id` differs.
Therefore `tau` is not constant on the one `pi_task` fiber, and:

```text
for every total deterministic g_task:X->Y,
g_task composed_with pi_task differs from tau on at least one witness state.
```

`tau` is constant on every singleton `pi_full` fiber, and the declared
`g_full` is its unique factor. This is a universal logical consequence on a
researcher-declared record-reconstruction obligation. It is not an empirical
prediction or evidence of a general security failure.

## Actual-input interpretation

For an orchestration node, `pi` must include everything the action can actually
read: delivered fields, mapper output, config, store, bound defaults, closures,
globals, runtime history, or correlated state. If any of those differ within a
claimed task-only pair, then the real projection is not the declared
`pi_task`.

Closure is semantic. A derived delivered coordinate could determine `tau`
without the literal provenance key; conversely, a listed but unavailable or
mapper-dropped key may not be delivered.

## Independent pinned correspondence propositions

The LangGraph claims are propositions requiring source/run-state evidence, not
corollaries of the abstract theorem.

### C_task — load-bearing

Under the exact fixture and fresh fixed run state, the complete input received
at callable entry for `s0` and `s1` with `TaskStateOnly` is byte-identical.
Failure rejects the task-side LangGraph application.

### C_full — optional positive control

Under the same fixture, callable inputs for `s0` and `s1` with
`TaskStatePlusProvenance` differ exactly at `provenance_record`. Failure rejects
this deliverability/sufficiency control but does not by itself refute `C_task`.

The cross-schema diagnostic checks that the task mapping equals the full
mapping with `provenance_record` removed. Its failure rejects the intended
one-coordinate treatment correspondence.

## Literal future fixture

The v6 JSON is normative for executable text. It fixes:

- exact `TypedDict` definitions for `ProvenanceRecord`, `TaskStateOnly`,
  `TaskStatePlusProvenance`, and enclosing `GraphState`;
- unannotated state fields, whose expected channels must be `LastValue`;
- a pure `capture(state)` callable that canonicalizes its argument before its
  first write;
- `StateGraph(GraphState)`, one node added with explicit `input_schema`, and
  `START -> capture -> END`;
- `builder.compile()` with no explicit checkpointer, cache, or store;
- `invoke(deepcopy(state), config=None)` and UTF-8 capture bytes;
- exact states `s0,s1`; and
- four cells, each in a fresh Python process with a fresh graph and temporary
  directory and no object or `input_cache` reuse.

Network is disabled. Python, standard-library JSON, source, config, and
environment versions/hashes are recorded. No adapter may synthesize either
expected projection.

## Source-level determinism gate

Primary runtime is LangGraph tag `1.2.9`, object
`95af6a00718588e7b7ce17310e8006d267896a77`. Before any fixture execution, a
source audit must establish:

1. authentic source objects and relevant file hashes;
2. exact `LastValue` channel construction from all literal state fields;
3. exact ordered `proc.channels` for each explicit node input schema;
4. `proc.mapper is None` for both schemas, otherwise rejection;
5. compiled checkpointer/cache/store are absent, otherwise rejection;
6. fresh checkpoint/channel state and a fresh empty `input_cache` per invoke;
7. availability of every selected channel before the PULL task;
8. `_proc_input` reads exactly those channels, applies no mapper, and produces
   the task-owned input value;
9. `prepare_single_task` assigns that value to
   `PregelExecutableTask.input`, which the bound callable receives;
10. capture occurs before any write and cannot mutate its argument beforehand;
11. no config, callback, store, global, closure, environment, history, cache,
    retry, or reused object adds a distinguishing coordinate; and
12. `C_task` and `C_full` follow from the fixed source path and run state.

Official source locations are
[`state.py`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/graph/state.py),
[`_read.py`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_read.py),
and
[`_algo.py`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_algo.py).

Execution, if separately authorized after a rigorous theory verdict and source
acquisition gate, may check the derived relations once per fixed cell. One
replicate cannot prove determinism.

## Theory-review gate

Phase 2 passes only if a sterile reviewer returns `RIGOROUS` after:

- independently deriving both theorem directions and factor uniqueness;
- checking empty, singleton, injective, constant, and larger-codomain cases;
- verifying the full typing and exact two-state consequence;
- finding no finite countermodel;
- keeping `C_task` independent and load-bearing and `C_full` optional;
- checking that the exact fixture and source/run-state obligations close the
  future correspondence subject;
- accepting the classical novelty and engineering-control boundary; and
- confirming no empirical or general-security claim has reappeared.

A rigorous verdict closes Phase 2 only. It does not establish `C_task`, execute
the fixture, or authorize Phase 3 acquisition. An adverse verdict requires a
new immutable revision or retirement; v3-v5 cannot be resurrected.

## Data and execution tiers

- **Phase 2:** proof, primary-source inspection, deterministic document/syntax
  checks, and sterile theory review only.
- **Phase 3:** at most one source-derived two-state correspondence check, only
  after applicable acquisition/execution authorization.
- **Phase 4:** no OMST security experiment, census, effect size, prevalence, or
  benchmark claim.
- **Locked test:** absent, ungenerated, unexecuted, and unauthorized.

## Immutable history

Git preserves c2-v1 through c2-v5, hypotheses v1-v5, and every adverse review.
Once committed, the c2-v6 contract, JSON, amendment, and hypothesis are
immutable; another correction requires c2-v7.

## Approval boundary

The standing default authorizes this local formal correction, deterministic
checking, and sterile theory review within the remaining budget. It does not
authorize framework download/install/run, Kaggle, held-out or locked-test
action, live targets, operational attacks, model APIs, external messages, or
publication.
