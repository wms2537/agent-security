# Cycle-2 orchestration-security evaluation contract

**Version:** c2-v8

**Recorded:** 2026-07-20

**Supersedes:** c2-v7 at commit `4951313`; all earlier contracts remain in Git.

**Status:** local theory/source/static review only.

## Active claim

For every candidate environment `E`:

```text
P(E) -> C_task(E) and C_full(E).
```

Separately and unconditionally:

```text
exists unique g:Q=image(pi)->Y with tau=g composed_with pi
iff ker(pi) subseteq ker(tau).
```

The exact two-state witness has one task fiber and two different canonical
targets, so every total deterministic task-input function fails on at least one
state. The full projection has the declared unique factor.

The theorem is classical. The witness is a record-reconstruction/schema-
sufficiency control relative to `tau`, not a general security result.

## Current environment E0

`E0` is CPython 3.14.3 with interpreter SHA-256
`eca90b668424db6f2105504128f02cac91c2805de9a928abcc272d1444abfde0`
and stdlib JSON SHA-256
`95022d150a27a2bfd54ac21bfce35812c96b53c420bb7b018dcb573f13e52da0`.

LangGraph and LangChain-core are absent. Therefore `P(E0)=false`, and no
unconditional framework correspondence is claimed.

## Exact static subject

- specification:
  `experiments/configs/omst-c2-v8-environment-conditional.json`;
- fixture: `experiments/omst_c2_v8_fixture.py`, SHA-256
  `ebb7bd056db292e61c1e6de6e486bce5dfa048ef3f336fef59ff3c0512ac44f6`;
- launcher: `experiments/run_omst_c2_v8_fixture.sh`, SHA-256
  `dfe5f8a00d23e4bb4f1c6d5d6adb8896c2255c015ed4e8fd3997afb01e4d356f`.

The fixture binds four cells, exact schemas/states, explicit empty callback
config, graph topology, capture-before-write, environment guards, compiled
runtime guards, one invoke, and canonical output. It remains unexecuted.

## P(E)

`P(E)` contains:

1. exact interpreter, stdlib, LangGraph 1.2.9 commit, LangGraph/LangChain-core
   distributions, dependency lock, source origins, and load-bearing hashes;
2. `P2a`: static artifact identities/syntax/mode/cells match;
3. `P2b(E,cell)`: environment and compiled runtime guards pass within the cell
   after compile and before invoke;
4. authoritative outer clean-shell and four fresh isolated Python-child
   commands execute exactly;
5. no pre-capture mutation through site customization, `.pth`, import hooks,
   wrappers, callbacks, or runnable config;
6. all source lemmas below pass on the acquired exact dependency bundle; and
7. fresh process/directory per cell with output only from callable-entry input.

P2a and P1/P3-P6 are pre-cell acquisition gates. P2b is an atomic within-cell
antecedent; failure aborts before observation. P7 is enforced by the launcher.

## Exact source trace

All LangGraph files below are bound to commit
`95af6a00718588e7b7ce17310e8006d267896a77`:

- [`state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py): schemas, LastValue, START writer, `_get_updates`, selected channels, mapper, services;
- [`_loop.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py): empty checkpoint fallback, channel hydration, input application, ticks;
- [`_checkpoint.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_checkpoint.py): empty checkpoint and fresh channels;
- [`_io.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_io.py): whole input dict to START;
- [`_algo.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_algo.py): fresh input cache, selected reads, `task.input`;
- [`_retry.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_retry.py): `task.proc.invoke(task.input,config)`;
- [`_read.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_read.py): `PregelNode.node` and bound/writer sequence; and
- [`_internal/_runnable.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/_internal/_runnable.py): first-step unchanged input and bound callable.

The exact trace is:

```text
literal dict
-> START EphemeralValue
-> START task input
-> _get_updates field writes + capture trigger
-> apply_writes
-> selected LastValue availability
-> PregelExecutableTask.input
-> PregelNode RunnableSeq(bound,writers)
-> bound RunnableCallable
-> capture(mapping) before write.
```

The acquired LangChain-core version/source and load-bearing
`runnables/base.py`, `runnables/config.py`, and `callbacks/manager.py` hashes are
bound by P1(E) and audited under P5(E).

## Authoritative launch

```text
/usr/bin/env -i HOME=/nonexistent PATH=/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC
/bin/bash --noprofile --norc
/home/soh/agent-security/experiments/run_omst_c2_v8_fixture.sh
```

The launcher asserts empty `BASH_ENV`/`ENV`, emits no own output, and starts four
fresh Python `-I -B` children under their own `env -i`. No fixed hash seed is
claimed or needed.

## Review and phase gates

Phase 2 passes only on a sterile `RIGOROUS` verdict for the theorem/witness and
the universally quantified conditional implication. Such a verdict does not
make `P(E0)` true.

Framework acquisition requires separate authorization. Phase 3 may start only
after a candidate `E` passes P1, P2a, P3-P6. Each cell then evaluates P2b before
invoke; a failed guard aborts. At most four fixed cells may check correspondence.

No OMST Phase-4 security experiment, census, effect, prevalence, benchmark, or
locked test exists.

## Approval boundary

Authorized: local formal correction, code-as-text, static syntax/hash checks,
primary-source research, sterile theory review.

Not authorized: framework download/install/import/run; Kaggle; held-out or
locked-test action; live targets; operational attacks; model APIs; external
messages; publication.
