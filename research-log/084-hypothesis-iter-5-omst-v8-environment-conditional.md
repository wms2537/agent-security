# Hypothesis — iteration 5, OMST v8 environment-conditional control

**Date:** 2026-07-20  
**Phase:** 2 — hypothesis formation  
**Cycle:** 2  
**Status:** superseding theoretical hypothesis, not yet reviewed  
**Claim type:** unconditional factorization plus an environment-parameterized
conditional engineering implication  
**Scope:** record reconstruction and schema sufficiency relative to `tau`

## Supersession and adverse-result record

This artifact supersedes but does not edit v1-v7. The immediately superseded
v7 artifact is `research-log/080-hypothesis-iter-5-omst-v7-conditional-correspondence.md`
at commit `80e0764`. Round-7 review is preserved verbatim in
`research-log/082-omst-theory-review-round7.md`.

Round 7 accepted the theorem, witness, non-circular conditional logic, literal
metadata, canonicalization, scope, taxonomy, and anti-stacking. It required six
engineering corrections:

1. split pre-cell static identity from within-cell compiled guards;
2. add `PregelNode.node`, LangGraph `RunnableSeq`, bound-callable, and
   LangChain-core callback/config paths;
3. correct the START path from whole-dict write to later `_get_updates`
   filtering;
4. parameterize both antecedent and consequence by one environment `E`;
5. define a genuinely clean outer-shell invocation and remove ineffective
   Python variables under `-I`; and
6. call compiled checks runtime guards, not static assertions.

The c2-v8 amendment in `research-log/083` implements those corrections without
acquiring or executing the absent framework.

## One-sentence hypothesis

The exact target uniquely factors through an input projection exactly when it
is constant on projection fibers; for every candidate environment `E`, if the
complete identity, source, isolation, and per-cell guard bundle `P(E)` holds,
then the pinned task cells deliver equal callable-entry bytes and the full cells
differ exactly at provenance.

## Claim ledger

### Unconditional mathematics

```text
exists unique g:Q=image(pi)->Y with tau=g composed_with pi
iff
ker(pi) subseteq ker(tau).
```

The exact two-state task projection has one fiber with two different canonical
targets, so no total deterministic function on its singleton input can
reconstruct both.

### Conditional framework-control proposition

```text
for every candidate environment E,
P(E) -> C_task(E) and C_full(E).
```

`C_task(E)` is load-bearing for a later framework application. `C_full(E)` is
an optional positive control.

### Current truth status

The recorded local document-check environment is `E0`. LangGraph and
LangChain-core are absent, so `P(E0)=false`. No unconditional LangGraph
correspondence follows or is claimed.

### Nonclaims

- that any `E` satisfying `P(E)` has been acquired;
- a framework run, security verdict, vulnerability, effect, prevalence,
  benchmark, production provenance policy, or general security conclusion;
- a new mathematical theorem or standalone top-tier contribution; or
- any framework download/install/import/run, Kaggle, held-out or locked-test
  action, live target, operational attack, model API, external message, or
  publication.

## Normative artifacts

- contract: `experiments/configs/evaluation-contract-orchestration-c2.md`;
- specification: `experiments/configs/omst-c2-v8-environment-conditional.json`;
- fixture: `experiments/omst_c2_v8_fixture.py`;
- launcher: `experiments/run_omst_c2_v8_fixture.sh`; and
- amendment/source rationale: `research-log/083`.

The fixture and launcher are code-as-text and have not been imported or run.

## Part I — minimal theorem

### Objects and definitions

Let `S,Y` be arbitrary sets, `pi:S->Q` and `tau:S->Y` total functions, and
define `Q=image(pi)`.

For a function `h`:

```text
(u,v) in ker(h) iff h(u)=h(v).
```

Define:

```text
closed(pi,tau) iff ker(pi) subseteq ker(tau).
```

Equivalently, `tau` is constant on every fiber
`F_q={s in S:pi(s)=q}`.

### Necessity

Assume `tau=g composed_with pi`. For `pi(s)=pi(s')`:

```text
tau(s)=g(pi(s))=g(pi(s'))=tau(s').
```

Hence `ker(pi) subseteq ker(tau)`.

### Sufficiency

Assume closure. Define:

```text
G={(q,y) in Q cross Y:
   there exists s in S with pi(s)=q and tau(s)=y}.
```

Every `q in Q=image(pi)` has a representative. Totality of `tau` supplies a
value. Two representatives have the same projection, so closure makes their
target values equal. Thus `G` is the graph of a total function `g:Q->Y`, and
`g(pi(s))=tau(s)` for every `s`.

### Uniqueness

For any two factors `g1,g2` and any `q in Q`, take an existentially guaranteed
`s` with `pi(s)=q`:

```text
g1(q)=g1(pi(s))=tau(s)=g2(pi(s))=g2(q).
```

Therefore `g1=g2`.

### Boundaries

- `S=empty` gives `Q=empty` and the unique empty factor; closure is vacuous.
- Infinite domains are covered because the proof is pointwise.
- Injective `pi` makes closure automatic.
- Constant `pi` on nonempty `S` makes closure equivalent to constant `tau`.
- Partial or multivalued maps are outside the theorem.
- On a separate superdomain of the image, extension requires an element of
  `Y`; off-image values are generally nonunique, except when `Y` is singleton.

This is the standard quotient/kernel factorization result.

## Part II — exact typed witness

Let `P={p0,p1}` be the exact records in the fixture, `B` the set of canonical
JSON byte strings, `J:P->B` the declared canonicalizer, and `X={x}` the exact
task singleton.

The canonicalizer is UTF-8 `json.dumps` with `sort_keys=True`, separators
`(',',':')`, `ensure_ascii=True`, `allow_nan=False`, and no trailing newline.
The domain includes JSON objects and arrays whose leaves are integers, strings,
booleans, or null.

The targets are:

```text
J(p0)={"activity_id":"activity-0","agent_id":"agent-0","entity_id":"entity-0"}
J(p1)={"activity_id":"activity-0","agent_id":"agent-1","entity_id":"entity-0"}
```

They differ. Define:

```text
S=X cross P
Y=J(P)

tau:X cross P->Y                    tau(x,p)=J(p)
pi_task:X cross P->X                pi_task(x,p)=x
pi_full:X cross P->X cross P        pi_full(x,p)=(x,p)
g_full:X cross P->Y                 g_full(x,p)=J(p)
```

The task fiber contains both states with different `tau`, so:

```text
for every total deterministic g_task:X->Y,
g_task composed_with pi_task differs from tau on at least one state.
```

The full fibers are singletons and `g_full` is the unique factor.

The witness is deliberately constructed. It establishes a universal logical
consequence on a record-reconstruction control, not an empirical security
obligation.

## Part III — environments and observations

### Candidate environment E

An environment `E` contains:

- workspace and artifact paths, bytes, modes, and hashes;
- interpreter link, resolved target, version, and hash;
- standard-library JSON path and hash;
- installed LangGraph/LangChain-core distributions, source origins, exact
  versions, licenses, dependency lock, and load-bearing file hashes;
- site/import customization state;
- runnable callback/config semantics;
- outer-shell and Python-child launch environment; and
- one cell identifier and its fresh process/directory state.

Every occurrence of `P`, `received`, `C_task`, and `C_full` below is indexed by
the same `E`. No current/future environment drift is implicit.

### Current E0

```text
interpreter link:
/home/soh/agent-security/comp/.venv/bin/python

resolved target:
/home/linuxbrew/.linuxbrew/Cellar/python@3.14/3.14.3_1/bin/python3.14

version:
CPython 3.14.3 (main, Feb 3 2026, 15:32:20) GCC 12.3.0

interpreter SHA-256:
eca90b668424db6f2105504128f02cac91c2805de9a928abcc272d1444abfde0

stdlib JSON SHA-256:
95022d150a27a2bfd54ac21bfce35812c96b53c420bb7b018dcb573f13e52da0

LangGraph: absent
LangChain-core: absent
P(E0): false
```

### Conditional observations

For a candidate `E` in which a cell completes after all antecedent checks:

```text
received(cell,E)
```

is the UTF-8 canonical byte string constructed from the sole mapping supplied
to `capture` at callable entry, before `capture` returns any write.

Define:

```text
C_task(E):
received(task_s0,E)=received(task_s1,E)

C_full(E):
received(full_s0,E) and received(full_s1,E)
differ exactly at provenance_record.agent_id.
```

## Part IV — closed v8 subject

### Fixture identity

`experiments/omst_c2_v8_fixture.py` has SHA-256:

```text
ebb7bd056db292e61c1e6de6e486bce5dfa048ef3f336fef59ff3c0512ac44f6
```

It binds:

- all four schemas and exact `S0,S1` states;
- ordered task/full channel lists;
- cells `task_s0`, `task_s1`, `full_s0`, `full_s1`;
- empty callbacks, tags, metadata, and configurable mapping;
- one graph, capture node, explicit input schema, START/capture/END edges;
- explicit `None` checkpointer, cache, and store;
- environment and compiled runtime guards;
- one invoke after all guards;
- capture-before-write canonicalization; and
- one canonical result record containing cell, observed bytes as hex, and
  completion status.

### P2a static artifact identity

Before acquisition or execution, `P2a(E)` checks the committed fixture,
launcher, and config hashes; Python AST; JSON and Bash syntax; executable mode;
four cells; schemas; and literal states. This is truly static.

### P2b compiled runtime guards

Inside each future cell, after compilation but before `graph.invoke`, explicit
`require` calls verify:

- fixture, launcher, interpreter, and stdlib JSON paths/hashes against `E`;
- exact compiled `proc.channels`;
- `proc.mapper is None`;
- node cache/retry policies are `None`; and
- compiled checkpointer/cache/store are `None`.

A guard failure raises `OMST_RUNTIME_GUARD_FAILED:<label>` before correspondence
observation. P2b is not a Phase-3 pre-cell fact and no compile-only run is
required. It is an atomic per-cell antecedent evaluated before invoke.

### Authoritative isolated launch

The launcher SHA-256 is:

```text
dfe5f8a00d23e4bb4f1c6d5d6adb8896c2255c015ed4e8fd3997afb01e4d356f
```

Its only authoritative invocation is:

```text
/usr/bin/env -i HOME=/nonexistent PATH=/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC \
/bin/bash --noprofile --norc \
/home/soh/agent-security/experiments/run_omst_c2_v8_fixture.sh
```

Thus the outer Bash starts with a clean environment and absolute executable.
The script asserts empty `BASH_ENV` and `ENV`, emits no launcher-owned output,
and starts each child under a separate `env -i` with only HOME/locale/timezone
and Python `-I -B`.

No fixed hash seed is asserted or needed. `-I` supplies isolated Python mode
and ignores Python environment variables. The ineffective v7
`PYTHONHASHSEED/PYTHONNOUSERSITE` assignments are absent.

Each Python process creates one temporary directory and one graph, so no graph,
checkpoint, channel, input cache, callback manager, input object, or output
buffer is reused across cells.

The launcher remains unexecuted.

## Part V — exact source bridge

### Authenticated LangGraph basis

Every LangGraph path is bound to tag `1.2.9`, commit
`95af6a00718588e7b7ce17310e8006d267896a77`:

1. `libs/langgraph/langgraph/graph/state.py`;
2. `libs/langgraph/langgraph/pregel/_loop.py`;
3. `libs/langgraph/langgraph/pregel/_checkpoint.py`;
4. `libs/langgraph/langgraph/pregel/_io.py`;
5. `libs/langgraph/langgraph/pregel/_algo.py`;
6. `libs/langgraph/langgraph/pregel/_retry.py`;
7. `libs/langgraph/langgraph/pregel/_read.py`; and
8. `libs/langgraph/langgraph/_internal/_runnable.py`.

The source links and exact roles are recorded in the c2-v8 contract and
machine-readable configuration.

### LangChain-core basis at E

No LangChain-core version is installed or guessed at E0. `P1(E)` binds the
exact acquired version, distribution hash, source origin, dependency lock, and
load-bearing hashes. At minimum, P5 audits:

- `langchain_core/runnables/base.py`;
- `langchain_core/runnables/config.py`; and
- `langchain_core/callbacks/manager.py`.

### L_compile(E)

Pinned `state.py` registers exact `TypedDict` state/input schemas and ordinary
fields as `LastValue`. The capture node's selected channels derive from the
explicit input schema. Mapping-type input needs no model-coercion mapper. The
START `PregelNode` and its writers are built at compile. The fixture explicitly
passes absent services and P2b guards them.

### L_start(E)

For this compiled StateGraph, graph input channels are the single START channel.
Pinned `_io.map_input` therefore writes:

```text
(START, whole literal input dict)
```

not one tuple per state field. The START task reads that `EphemeralValue`.
Pinned `state.py` constructs the START writer with `_get_updates`, which filters
the whole input mapping into GraphState field writes; the writer also produces
the branch trigger to capture. `_loop.apply_writes` makes the selected
`LastValue` fields available for the next superstep.

This is the exact corrected path:

```text
literal dict -> START EphemeralValue -> START task input
-> _get_updates field writes + capture trigger -> apply_writes
-> selected LastValue availability.
```

### L_fresh(E)

With no saved checkpoint, pinned `_loop.py` substitutes
`_checkpoint.empty_checkpoint()`. That checkpoint has empty channel values,
versions, and seen maps. `channels_from_checkpoint` constructs fresh channel
instances before L_start. The fresh process eliminates earlier loop objects.

### L_prepare(E)

Pinned `_loop.tick` calls `_algo.prepare_next_tasks`. The latter creates a fresh
`input_cache`; `_proc_input` reads all available channels selected by the
capture `PregelNode`, applies a mapper only if non-`None`, and assigns the
mapping to `PregelExecutableTask.input`.

### L_deliver(E)

Pinned `_retry.run_with_retry` invokes `task.proc.invoke(task.input,config)`.
Pinned `_read.PregelNode.node` constructs the node procedure as
`RunnableSeq(bound,writers)`. Pinned LangGraph `_internal/_runnable.RunnableSeq`
passes its input unchanged to the first step, the bound `RunnableCallable`, and
only then passes the callable's return to writers. The bound callable is
`capture`, so it receives `task.input`.

The exact LangChain-core config/callback path is bound by P1(E) and audited by
P5(E). It must give no pre-capture mutation authority. Passive observation does
not alter callable-entry byte equality and is not excluded merely for being an
observer.

The complete trace is:

```text
literal dict
-> START EphemeralValue
-> START task input
-> _get_updates fields + capture trigger
-> selected LastValue availability
-> PregelExecutableTask.input
-> PregelNode RunnableSeq(bound,writers)
-> bound RunnableCallable receives unchanged input
-> capture(mapping) before any write.
```

## Part VI — P(E)

`P(E)` is the conjunction of eight independently scoped premises.

### P1(E) — environment identity

Interpreter link/target/hash, stdlib JSON path/hash, LangGraph 1.2.9 commit,
exact LangGraph/LangChain-core distributions, dependency lock, licenses, source
origins, and all load-bearing file hashes match the manifest for `E`.

### P2a(E) — static artifact identity

Committed fixture/launcher/config bytes, hashes, syntax, modes, schemas, states,
and four-cell set match `E` before execution.

### P2b(E,cell) — atomic runtime guards

Environment and compiled guards pass inside the cell after compilation and
before invoke. Failure aborts without a correspondence observation.

### P3(E) — authoritative process isolation

The exact outer `env -i` absolute-Bash command and four child `env -i` Python
`-I -B` commands run unchanged; `BASH_ENV/ENV` are absent; launcher stdout is
only the four child records.

### P4(E) — import mutation exclusion

No `sitecustomize`, `usercustomize`, executable `.pth`, import hook, or wrapper
can mutate literal state, application globals, or callable input before capture.

### P5(E) — callback mutation exclusion

Explicit empty callbacks/config plus the exact LangChain-core config/callback
implementation give no pre-capture mutation authority. Passive callbacks that
cannot mutate the argument do not violate P5.

### P6(E) — source lemmas

`L_compile`, `L_start`, `L_fresh`, `L_prepare`, and `L_deliver` are independently
verified against the exact acquired source/dependency bundle. These lemmas are
per-cell path facts and do not contain the cross-cell conclusions.

### P7(E) — cell isolation and observation origin

Each cell is one fresh process/directory, and `observed_hex` is derived only
from the callable-entry mapping.

P2a and P1/P3-P6 are pre-cell gates. P2b is checked atomically inside the cell.
P7 is enforced by the launcher and artifact audit. No ordering cycle remains.

## Derivation of the conditional proposition

Fix an arbitrary `E` and assume `P(E)`.

By L_compile/L_start/L_fresh, each task cell presents exactly the five declared
task `LastValue`s and each full cell those five plus provenance. By L_prepare,
the selected mapping is `PregelExecutableTask.input`. By L_deliver, that mapping
is the unchanged first input to `capture`. P2b guards the compiled identities
before invoke; P3-P5 exclude a mutating pre-capture path; P7 excludes reuse.

The five task values in `S0,S1` are literally equal. Canonicalization is
deterministic under the fixed stdlib JSON identity in `E`. Therefore:

```text
C_task(E).
```

The full mappings add records whose only differing leaf is `agent_id`.
Therefore:

```text
C_full(E).
```

Because `E` was arbitrary:

```text
for every E, P(E) -> C_task(E) and C_full(E).
```

P6 does not contain either conclusion; the last equality/difference step uses
only literal cross-cell fixture values. The implication is not circular.

## Failure semantics

- A theorem countermodel falsifies Part I.
- Equal witness targets or a type mismatch invalidates Part II.
- `P(E)=false` leaves framework correspondence unestablished for `E`.
- P2b failure aborts before observation and cannot count as a `C` result.
- With `P(E)` true, task inequality falsifies `C_task(E)` and rejects the
  task-side framework application.
- With `P(E)` true, full-control failure falsifies optional `C_full(E)` only.
- None of these outcomes is a general security verdict or empirical effect.

## Assumptions, rivals, and controls

### Mathematical premises

| Premise | Role | Failure consequence |
|---|---|---|
| total `pi,tau` | theorem equality domain | Partial/multivalued variant needed. |
| `Q=image(pi)` | canonical unique factor | Larger domain adds off-image freedom. |
| `J(p0)!=J(p1)` | witness contradiction | No two-target impossibility otherwise. |
| exact `X cross P` pairs | witness domain | A correlated real domain may omit the fiber. |

### Engineering rivals

1. Mapper adds/drops fields: L_compile plus P2b.
2. Selected field unavailable: corrected L_start/L_fresh path plus P6.
3. Stale checkpoint/input cache: fresh process, empty checkpoint, fresh
   preparation cache.
4. START filtering mislocated: whole dict then `_get_updates` is explicit.
5. Runnable writer receives input before callable: `_read`/`RunnableSeq` order is
   explicit; bound callable is first.
6. Callback mutates pre-capture state: P5 audits exact config/manager path.
7. Import/site hook mutates state: P4.
8. Environment drift: every claim is indexed by E and guarded by exact hashes.
9. Outer shell contamination: authoritative outer `env -i` and absolute Bash.
10. Capture mutation: canonical string built before first returned write.
11. Canonicalization ambiguity: exact stdlib path/hash and primitive-container
    domain.
12. Researcher target/classical theorem: conceded scope boundaries.

## Bias surface

| Bias | Control |
|---|---|
| Confirmation | Sterile reviewer re-derives theorem and source path and can reject any P item. |
| Selection | Purpose-built two-state witness, no population inference. |
| Measurement | Only pre-write callable-entry bytes, no action verdict. |
| Leakage | Target not passed to capture; fixture equality is literal. |
| Implementation | Exact v8 files, modes, hashes, guards, cells, and source paths. |
| Environment | Explicit E parameter and runtime reauthentication. |
| Analysis flexibility | Pairwise relations and role-specific failures fixed. |
| Novelty/generalization | Classical control scope stated repeatedly. |

## Taxonomy, anti-stacking, and Occam

Taxonomy is `Scope Mismatch × Formal Derivation × formalize`, with `decouple`
secondary. No synthesis claim is made.

Anti-stacking passes narrowly: the nonconstant-fiber proof excludes every total
deterministic function on the declared input, while testing one action excludes
only that action. The claim is bounded to the chosen `X,Y,tau`.

The theorem and witness are minimal. The environment premise bundle is larger
because it connects a concrete dependency/runtime stack, but observer-only
exclusions have been removed: P4/P5 exclude mutation authority, not passive
observation. Hash seed is absent because it is unnecessary. `C_full` remains
optional.

## Deterministic pre-review checks

Without importing or executing LangGraph:

1. parse v8 fixture AST and launcher Bash syntax;
2. validate config/state JSON;
3. verify fixture/launcher/interpreter/stdlib hashes and executable mode;
4. verify authoritative command uses outer `env -i`, absolute Bash, and no
   ineffective Python variables;
5. enumerate the theorem over `|S|=0..4`, three projection labels, two target
   labels, and every reachable-image action;
6. recompute witness target bytes;
7. verify eight P entries, eight LangGraph source paths, three required
   LangChain-core modules, four cells, and `P(E0)=false`;
8. verify all predecessors and reviews unchanged; and
9. scan for unresolved placeholders and prohibited execution/result claims.

## Review gate

Return `RIGOROUS` only after:

1. re-deriving the theorem/witness and searching countermodels;
2. checking the universal environment quantification and non-circularity;
3. independently checking the whole-dict START path and `_get_updates` locus;
4. checking PregelNode/RunnableSeq/bound-callable/callback delivery;
5. checking P2a/P2b timing and abort-before-observation semantics;
6. checking the authoritative clean-shell command and runtime identity guards;
7. confirming `P(E0)=false` and no unconditional framework inference;
8. validating role-specific failures, scope, taxonomy, anti-stacking, and Occam.

A rigorous verdict closes Phase 2 for the theorem and universal implication
only. It does not make `P(E0)` true or authorize acquisition/execution.

## Round-7 disposition

| Requirement | v8 author claim before independent review |
|---|---|
| P2/gate conflict | **AUTHOR-RESOLVED:** P2a pre-cell; P2b atomic after compile/before invoke. |
| Delivery source bridge | **AUTHOR-RESOLVED:** `_read`, LangGraph RunnableSeq, bound callable, conditional LangChain callback/config path. |
| START description | **AUTHOR-RESOLVED:** whole dict to START; `_get_updates` creates fields and trigger. |
| Environment binding | **AUTHOR-RESOLVED:** `forall E,P(E)->C(E)` with runtime identity guards. |
| Shell/`-I` semantics | **AUTHOR-RESOLVED:** outer `env -i` absolute Bash; ineffective variables removed. |
| Terminology | **AUTHOR-RESOLVED:** compiled runtime guards with abort timing. |

These are author claims, not reviewer dispositions.

## Authorization boundary

Authorized: this local revision, code-as-text, static syntax/hash checks,
primary-source inspection, sterile theory review.

Not authorized: framework download/install/import/run; Kaggle; held-out or
locked-test action; live targets; operational attacks; model APIs; external
messages; publication.
