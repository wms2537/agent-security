# Cycle-2 orchestration-security evaluation contract

**Version:** c2-v7

**Recorded:** 2026-07-20

**Supersedes:** c2-v6 at commit `0f4b93f`; c2-v1 through c2-v6 remain in Git
history.

**Status:** APPROVED UNDER STANDING INTERNAL-ITERATION DEFAULT — local formal
correction, static code checks, source research, and sterile review only.

**Active study:** OMST record-reconstruction/schema-sufficiency control.

## Round-6 decision

Round 6 found the minimal theorem and typed witness rigorous and found no finite
countermodel. It rejected only the unconditional LangGraph correspondence:
v6's decisive environment/source facts were partly stated as future
postconditions.

c2-v7 removes that overclaim. The active claim structure is:

```text
UNCONDITIONAL:
  unique factorization theorem
  fully typed two-state universal consequence

CONDITIONAL:
  P -> C_task
  P -> C_full

NOT CLAIMED:
  P is currently discharged
  unconditional LangGraph correspondence
```

The normative artifact is
`experiments/configs/omst-c2-v7-conditional-correspondence.json`; the amendment
record is `research-log/079`.

## Minimal theorem

For sets `S,Y`, total `pi:S->Q` where `Q=image(pi)`, and total `tau:S->Y`:

```text
exists unique g:Q->Y with tau=g composed_with pi
iff
ker(pi) subseteq ker(tau).
```

Necessity follows from functionality of `g`. For sufficiency, define `g(q)` as
the common `tau` value on the nonempty fiber over `q`; kernel inclusion makes it
well-defined, and the image domain makes it total and unique.

Empty `S` is allowed and yields the unique empty factor. Finiteness is not
assumed. For a separate strict superset of the image, an extension exists when
an output value exists, but off-image values are generally nonunique.

This is classical quotient/function factorization, not a new theorem.

## Typed witness

```text
P={p0,p1}                         exact fixture records
B                                  canonical JSON byte strings
J:P->B                             exact canonicalizer
X={x}                              exact task singleton
S=X cross P
Y=J(P)

tau:X cross P->Y                   tau(x,p)=J(p)
pi_task:X cross P->X               pi_task(x,p)=x
pi_full:X cross P->X cross P       pi_full(x,p)=(x,p)
g_full:X cross P->Y                g_full(x,p)=J(p)
```

`J(p0)!=J(p1)`. Hence every total deterministic `g_task:X->Y` fails on at
least one witness state. The full projection has singleton fibers and the
declared `g_full` is its unique factor.

Canonicalization covers JSON objects and arrays with primitive leaves. The
fixture uses nested objects and one empty array.

## Conditional correspondence

`C_task` says the exact pinned fixture supplies identical callable-entry bytes
for `task_s0,task_s1`. It is load-bearing for any later framework application.

`C_full` says `full_s0,full_s1` inputs differ only at
`provenance_record.agent_id`. It is an optional positive control.

The active source proposition is only:

```text
P -> C_task
P -> C_full.
```

Neither `C_task` nor `C_full` is asserted unconditionally. If any member of `P`
fails, the framework application remains unestablished; the theorem is
unaffected.

## Closed static fixture

The exact unexecuted subject consists of:

- `experiments/omst_c2_v7_fixture.py`, SHA-256
  `e26bca99b0aa9e614308ab0330501d03f78758181f0f4627137da40fb8305d09`;
- `experiments/run_omst_c2_v7_fixture.sh`, SHA-256
  `ff9be2b71a41d26cb60b59bb8670cacb8e63e89349efff921cabe52cd12df68c`.

The module binds exact schemas, states, graph, node, edges, config, compiled
assertions, capture, and all four named cells. The launcher binds four separate
processes under `/usr/bin/env -i` and Python `-I -B`.

The capture serializes its sole callable argument before returning its first
write. Output is one canonical diagnostic record with no security verdict.

Static Python/shell parsing does not import or run LangGraph.

## Commit-bound source lemmas

All source paths are bound to authenticated LangGraph commit
`95af6a00718588e7b7ce17310e8006d267896a77`.

### L_compile

[`state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py)
registers exact input schemas, ordinary `LastValue` channels, selected
`PregelNode.channels`, `None` mapper for the exact mappings, and absent compiled
services when passed `None`.

### L_fresh

[`_loop.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py),
[`_checkpoint.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_checkpoint.py),
and
[`_io.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_io.py)
give the path from an empty checkpoint through fresh channels, graph input,
START writes, GraphState field writes, and selected-channel availability before
capture.

### L_prepare

[`_algo.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_algo.py)
creates a fresh empty input cache, reads the selected available channels,
applies no mapper, and assigns the result to
`PregelExecutableTask.input`.

### L_deliver

[`_retry.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_retry.py)
invokes `task.proc` with `task.input`; the declared capture receives and
serializes that mapping before a write.

## Premise bundle P

`P` is discharged only if all hold:

1. an authorized acquired environment matches LangGraph 1.2.9 at the pinned
   commit and exact LangGraph/LangChain-core manifests and file hashes;
2. fixture and launcher hashes match, and compiled assertions pass;
3. the exact `env -i`, `-I -B` launcher leaves no inherited tracing,
   `PYTHONPATH`, user site, or callback configuration;
4. the environment has no `sitecustomize`, `usercustomize`, executable `.pth`,
   import hook, or wrapper able to mutate input before capture;
5. explicit `callbacks=[]`, empty tags/metadata/configurable produce no
   mutating callback path;
6. `L_compile`, `L_fresh`, `L_prepare`, and `L_deliver` are independently
   verified against the acquired exact dependency bundle; and
7. each cell is a fresh process and output comes only from callable-entry input.

The current local document-check environment is literally recorded: CPython
3.14.3 interpreter SHA-256
`eca90b668424db6f2105504128f02cac91c2805de9a928abcc272d1444abfde0`
and stdlib JSON SHA-256
`95022d150a27a2bfd54ac21bfce35812c96b53c420bb7b018dcb573f13e52da0`.
LangGraph and LangChain-core are absent. Therefore `P` is not discharged.

## Review gate

Phase 2 passes only if a sterile reviewer returns `RIGOROUS` after:

- independently deriving theorem existence and uniqueness, including empty and
  larger-domain cases;
- validating the complete witness typing and universal consequence;
- confirming the four source lemmas support the conditional implication;
- confirming no environment premise is asserted as currently true;
- checking fixture/launcher closure statically;
- confirming `C_task` load-bearing and `C_full` optional roles;
- accepting the classical novelty and record-reconstruction scope; and
- finding no hidden execution, security, causal-effect, or prevalence claim.

`RIGOROUS` establishes the theorem and validity of `P -> C`; it does not
discharge `P`, authorize acquisition, or establish runtime correspondence.

## Phase and execution tiers

- **Phase 2:** proof, source research, static syntax/document checks, and sterile
  review only.
- **Acquisition gate:** separate authorization before obtaining/installing
  LangGraph or LangChain-core.
- **Phase 3:** only after `P1-P6` pass may four one-use cells check conditional
  correspondence.
- **Phase 4:** no OMST security experiment, census, effect, prevalence, or
  benchmark.
- **Locked test:** absent and unauthorized.

## Scope

The result is a record-reconstruction/schema-sufficiency control relative to
`tau`: classical factorization plus a conditional framework-control protocol.
It is not unconditional LangGraph correspondence, a general security failure,
a framework vulnerability, production policy, empirical result, or standalone
top-tier contribution.

## Immutable history and approval boundary

Git preserves c2-v1 through c2-v6, hypotheses v1-v6, and all adverse reviews.
Once committed, c2-v7 artifacts are immutable; another correction requires
c2-v8.

The standing default authorizes this local correction, code-as-text, static
checks, and sterile review. It does not authorize framework acquisition,
installation, import, or execution; Kaggle; held-out or locked-test action;
live targets; operational attacks; model APIs; external messages; or
publication.
