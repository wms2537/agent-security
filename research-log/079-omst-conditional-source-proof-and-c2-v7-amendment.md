# OMST conditional source proof and c2-v7 amendment

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** round-6 adverse verdict accepted; c2-v7 activated; unconditional
framework correspondence withdrawn until acquisition premises are discharged

## Scientific decision

Round 6 found the minimal theorem, all boundary cases, the typed witness,
role separation, scope, taxonomy, and anti-stacking rigorous. It found no
counterexample in 1,555 finite models. The remaining failure was narrower and
important: v6 called the LangGraph proposition source-closed while still
treating channel hydration, input availability, callback isolation, and exact
environment identity as future admissibility conditions.

The correct repair is not to turn absent dependencies into fictional facts.
c2-v7 makes two claim levels explicit:

```text
unconditional: the factorization theorem and typed two-state consequence
conditional:   P implies C_task and C_full for the exact future environment
not claimed:   P is currently discharged, or unconditional LangGraph closure
```

This follows the reviewer's offered `C_task_if_P` formulation. LangGraph and
LangChain-core remain absent from the intended local environment, so no
framework import or run was performed.

## Expanded primary-source path

The source analysis now binds every file directly to authenticated commit
`95af6a00718588e7b7ce17310e8006d267896a77`, rather than claiming unavailable
local hashes.

1. [`state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py)
   registers explicit node input schemas, constructs ordinary `LastValue`
   channels, binds `PregelNode.channels`, uses no coercive mapper for the exact
   `TypedDict` mappings, and accepts explicit `None` services at compile.
2. [`_loop.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py)
   initializes an empty checkpoint when no saved tuple exists, hydrates channel
   instances, maps graph input, applies input writes, prepares tasks, and
   advances writes across the START and capture supersteps.
3. [`_checkpoint.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_checkpoint.py)
   defines `empty_checkpoint` with empty channel values, versions, and seen
   versions, and constructs channels from that checkpoint.
4. [`_io.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_io.py)
   maps every literal input key present in the compiled graph input channels.
5. [`_algo.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_algo.py)
   creates a fresh empty input cache per task-preparation pass, reads each
   available selected channel, applies the mapper only if present, and assigns
   the value to `PregelExecutableTask.input`.
6. [`_retry.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_retry.py)
   calls `task.proc.invoke(task.input, config)` on the synchronous path.

The resulting symbolic trace is:

```text
literal full state
-> START input
-> GraphState field writes
-> fresh LastValue values
-> capture PULL preparation
-> selected input-schema mapping
-> PregelExecutableTask.input
-> task.proc.invoke(task.input, config)
-> capture(mapping) before its first write
```

This supports four source lemmas: `L_compile`, `L_fresh`, `L_prepare`, and
`L_deliver`. It does not discharge dependency identity or ambient-import and
callback isolation for a package environment that does not yet exist. Those
facts are explicitly members of `P`.

## Closed static fixture

c2-v7 adds two complete, unexecuted files:

- `experiments/omst_c2_v7_fixture.py`, SHA-256
  `e26bca99b0aa9e614308ab0330501d03f78758181f0f4627137da40fb8305d09`;
- `experiments/run_omst_c2_v7_fixture.sh`, SHA-256
  `ff9be2b71a41d26cb60b59bb8670cacb8e63e89349efff921cabe52cd12df68c`.

The module binds all four states/schema cells, exact graph construction,
explicit empty callback/config fields, compiled-object assertions, a
capture-before-write callable, temporary directory, and canonical output. The
launcher binds four separate processes under `/usr/bin/env -i` and Python
`-I -B`. It cannot presently execute because the framework dependencies remain
absent and unauthorized.

Static Python parsing and shell syntax checking are allowed document checks;
they do not import LangGraph.

## Literal local metadata

The document-check environment is no longer described with placeholders:

- interpreter: `comp/.venv/bin/python`, CPython 3.14.3;
- interpreter SHA-256:
  `eca90b668424db6f2105504128f02cac91c2805de9a928abcc272d1444abfde0`;
- standard-library JSON SHA-256:
  `95022d150a27a2bfd54ac21bfce35812c96b53c420bb7b018dcb573f13e52da0`;
- LangGraph: absent; and
- LangChain-core: absent.

The future acquired framework manifest has no placeholder value. Its current
status is explicitly **absent/unacquired**, and acquisition remains a separate
gate. Source paths are authenticated by commit URLs until a local manifest is
authorized and constructed.

## Conditional premise bundle P

`P` requires:

1. an acquired local environment authenticated to the pinned release and exact
   LangGraph/LangChain-core manifests;
2. matching committed fixture/launcher hashes and passing static assertions;
3. exact `env -i`, `-I -B` launch with no inherited tracing, `PYTHONPATH`, user
   site, or callback configuration;
4. no `sitecustomize`, `usercustomize`, executable `.pth`, import hook, or
   wrapper capable of pre-capture mutation;
5. `callbacks=[]` producing no callback handler with mutation authority;
6. independent verification of all four source lemmas against the acquired
   bundle; and
7. one fresh process per cell with output derived only from callable-entry
   input.

Therefore:

```text
P -> C_task
P -> C_full
```

Neither consequent is claimed before `P` is discharged. `C_task` remains the
load-bearing later application premise; `C_full` remains optional.

## Round-6 requirement disposition

| Requirement | c2-v7 disposition |
|---|---|
| Complete engineering proof | **RESOLVED AT THE CORRECT CLAIM LEVEL:** four commit-bound source lemmas trace fresh checkpoint, input writes, availability, task input, and delivery; exact environment facts remain named antecedents in `P`, not assumed conclusions. |
| Literal metadata and callback/import isolation | **RESOLVED:** actual local hashes and explicit dependency absence replace placeholders; `env -i`, `-I`, empty callbacks, and import-context checks are exact members of `P`. |
| Genuinely closed fixture | **RESOLVED STATICALLY:** module binds all four cells and assertions; launcher binds four isolated commands; hashes are fixed. Execution remains gated. |
| JSON-container description | **RESOLVED:** objects and arrays with primitive leaves are the exact domain. |

## Scope and phase decision

The retained result is a rigorous classical theorem, a typed minimal witness,
and a testable conditional framework-control protocol. Phase 2 can review the
validity of `P -> C`; it cannot declare `P` discharged. Phase 3 acquisition and
execution remain separate and unauthorized.

The scope remains record reconstruction/schema sufficiency relative to `tau`.
There is no general security result, framework vulnerability, empirical effect,
or top-tier standalone contribution.

## Authorization boundary

The standing instruction authorizes this local amendment, code-as-text, static
checks, and sterile review. It does not authorize framework acquisition,
installation, import, or execution; Kaggle; held-out or locked-test action;
live targets; operational attacks; model APIs; external messages; or
publication.
