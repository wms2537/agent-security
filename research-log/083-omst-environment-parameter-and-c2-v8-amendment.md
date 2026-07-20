# OMST environment parameter and c2-v8 amendment

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** round-7 adverse verdict accepted; c2-v8 activated; no framework
acquisition, import, or execution

## Decision

Round 7 accepted the mathematics, typed witness, non-circularity of the
conditional implication, literal metadata, canonicalization, scope, taxonomy,
and anti-stacking. Its remaining issues were execution-gate mechanics and two
missing/misstated source steps.

c2-v8 resolves them without manufacturing a runtime result:

```text
for every candidate environment E,
P(E) -> C_task(E) and C_full(E).
```

The currently recorded environment is `E0`. `P(E0)=false` because LangGraph and
LangChain-core are absent.

## P2 gate split

v7 incorrectly required compiled graph assertions to pass before the only cell
commands that could execute them. v8 splits this requirement:

- `P2a(E)` is static artifact identity: hashes, syntax, modes, exact cells, and
  literal values are checked before acquisition/execution.
- `P2b(E,cell)` is a set of compiled runtime guards inside each cell. It runs
  after graph construction and before `graph.invoke`. Failure raises
  `OMST_RUNTIME_GUARD_FAILED` and aborts the cell without a correspondence
  observation.

The Phase-3 pre-cell gate requires P1, P2a, and P3-P6. P2b is an atomic
within-cell antecedent. This removes the impossible compile-before-cell order.

## Correct START path

The source trace now states the actual path:

```text
literal dict
-> START EphemeralValue as the whole dict
-> START task input
-> state.py _get_updates per-field writes + capture branch trigger
-> apply_writes
-> selected LastValue fields available
-> capture PULL task.
```

[`_io.map_input`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_io.py)
does not perform per-field GraphState filtering in this compiled graph. It writes
the whole dict to START. The START node assembled in
[`state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py)
uses `_get_updates` and its writers to create the field writes and branch
trigger.

## Complete callable-delivery path

The commit-bound LangGraph source basis now also includes:

- [`_read.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_read.py);
  and
- [`_internal/_runnable.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/_internal/_runnable.py).

The exact delivery trace is:

```text
PregelExecutableTask.proc
-> PregelNode.node
-> RunnableSeq(bound,writers)
-> first bound RunnableCallable receives unchanged task.input
-> capture(mapping)
-> writers consume capture's return.
```

The future exact LangChain-core distribution is not guessed. `P1(E)` must bind
its version, distribution/source hashes, and dependency lock. `P5(E)` requires
audit of its runnable config and callback manager modules, including
`runnables/base.py`, `runnables/config.py`, and `callbacks/manager.py`, before
execution. Only pre-capture mutation authority is load-bearing; passive
observation does not change callable-entry byte equality.

## Closed v8 fixture and environment guards

New immutable code-as-text artifacts are:

- `experiments/omst_c2_v8_fixture.py`, SHA-256
  `ebb7bd056db292e61c1e6de6e486bce5dfa048ef3f336fef59ff3c0512ac44f6`;
- `experiments/run_omst_c2_v8_fixture.sh`, SHA-256
  `dfe5f8a00d23e4bb4f1c6d5d6adb8896c2255c015ed4e8fd3997afb01e4d356f`.

The fixture adds explicit runtime guards for:

- its own and the launcher's recorded hashes;
- interpreter resolved path/hash;
- standard-library JSON path/hash;
- compiled channels and mapper;
- node cache/retry policies; and
- compiled checkpointer/cache/store.

Every guard precedes `graph.invoke`.

## Authoritative shell isolation

The authoritative future launch is now an explicit outer command:

```text
/usr/bin/env -i HOME=/nonexistent PATH=/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC
/bin/bash --noprofile --norc
/home/soh/agent-security/experiments/run_omst_c2_v8_fixture.sh
```

The launcher uses absolute `/bin/bash`, asserts empty `BASH_ENV`/`ENV`, emits no
own output, and starts each Python child under a separate `env -i` with Python
`-I -B`. Ineffective `PYTHONHASHSEED` and `PYTHONNOUSERSITE` assignments are
removed. `-I` provides user-site and Python-environment isolation; fixed hash
seed is neither asserted nor needed for sorted canonical JSON.

## Round-7 disposition

| Requirement | c2-v8 disposition |
|---|---|
| P2/phase-gate conflict | **RESOLVED:** P2a is pre-cell static identity; P2b is an atomic per-cell guard before invoke. |
| Callable-delivery source bridge | **RESOLVED:** `_read.py`, LangGraph `_internal/_runnable.py`, and conditional LangChain-core callback/config modules are explicit. |
| START description | **RESOLVED:** whole dict to START, then `_get_updates` field filtering and trigger. |
| Environment binding | **RESOLVED:** universal `forall E, P(E)->C(E)` plus execution-time path/hash/manifest checks. |
| Shell and `-I` wording | **RESOLVED:** outer clean shell is authoritative; ineffective Python variables removed. |
| Assertion terminology | **RESOLVED:** `compiled_runtime_guards`, with exact failure timing. |

## Scope and authorization

The result remains a classical factorization theorem, typed record-reconstruction
witness, and environment-parameterized conditional control. It is not an
unconditional framework result, vulnerability, security policy, empirical
effect, or standalone top-tier contribution.

The standing instruction authorizes this local code-as-text correction, static
checks, source research, and sterile review only. It does not authorize
framework acquisition/import/execution, Kaggle, held-out or locked-test action,
live targets, operational attacks, model APIs, external messages, or
publication.
