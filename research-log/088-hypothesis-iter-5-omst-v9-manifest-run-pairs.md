# Hypothesis — OMST v9 common-manifest run pairs

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5  
**Status:** complete before independent review; unexecuted  
**Supersedes:** `research-log/084-hypothesis-iter-5-omst-v8-environment-conditional.md`

## Claim in one sentence

The standard projection-fiber factorization theorem and exact two-state
record-reconstruction witness hold unconditionally; independently, for every
authenticated common manifest `M` and role-specific pair of admissible fresh
run objects, the closed LangGraph fixture conditionally delivers equal task
records for the task pair and records differing only at provenance agent ID for
the full pair.

No framework dependency is present, imported, compiled, or invoked now.

## Concept

**Name:** Orchestration Metamorphic Security Testing (OMST), with this artifact
restricted to the **schema-sufficiency control**.

**Plain language:** If a program must reconstruct a target record from only the
fields an orchestration graph gives it, reconstruction is possible exactly when
the omitted distinctions never change the target. A two-state example proves
that task fields alone cannot reconstruct two different provenance records,
whereas task fields plus provenance can. Applying that elementary result to one
specific framework requires a separate correspondence argument. v9 makes that
argument checkable without mixing runs: one immutable manifest authenticates
the common runtime, each execution has its own run object, and task/full pairs
have independent antecedents. A failed optional full control therefore cannot
erase an otherwise valid task-side conclusion.

**Formal contribution:**

1. for total `pi:S->Q=image(pi)` and `tau:S->Y`, a unique
   `g:Q->Y` with `tau=g composed_with pi` exists iff
   `ker(pi) subseteq ker(tau)`;
2. on the exact two-state record witness, every total deterministic task-only
   reconstructor fails on at least one state, while the full projection has a
   unique factor; and
3. two independent universal conditional propositions connect four explicit
   future run objects to one authenticated framework/source manifest.

The first result is classical. The second is a constructed control. The third
is an unexecuted, source-conditional application protocol. None is an empirical
security effect or a framework vulnerability.

## Variables, comparison, and decision rule

### Independent variable

The exact input schema supplied to the capture node:

- `TaskStateOnly`; or
- `TaskStatePlusProvenance`.

### Dependent observation

For a completed admissible run object `R_cell` under manifest `M`:

```text
received(cell,M,R_cell)
```

is the UTF-8 canonical JSON byte string constructed from the sole mapping
supplied to `capture` at callable entry, before `capture` returns any write.

### Controls

- exact literal states `S0,S1`;
- graph topology, capture callable, compile options, and empty runnable config;
- canonicalizer and standard-library JSON file;
- common manifest payload and all authenticated artifacts/dependencies/sources;
- interpreter, isolated child environment, fresh process, and temporary
  directory;
- one graph compile and at most one invoke per run object; and
- exact role launcher and cell/run-ID binding.

### Pre-specified primary comparison

The load-bearing application comparison is the task pair:

```text
C_task(M,R_task_s0,R_task_s1):
received(task_s0,M,R_task_s0)
= received(task_s1,M,R_task_s1).
```

It is assessed only when `P_task(M,R_task_s0,R_task_s1)` is true.

The full pair is an independent optional positive control:

```text
C_full(M,R_full_s0,R_full_s1):
the decoded received mappings differ exactly at
provenance_record.agent_id,
with values agent-0 and agent-1 respectively.
```

It is assessed only when `P_full(M,R_full_s0,R_full_s1)` is true.

### Expected effect and thresholds

There is no population effect size. For an admissible task pair, exact byte
equality is success and any byte inequality is disconfirmation of the task-side
framework application. For an admissible full pair, the exact one-leaf
difference is success; equality, any extra difference, wrong values, or missing
output disconfirms only the full-control application.

A framework/environment guard failure is neither success nor disconfirmation:
it makes the applicable antecedent false and leaves that role unestablished.

## Part I — minimal factorization theorem

### Objects and definitions

Let `S,Y` be arbitrary sets, `pi:S->Q` and `tau:S->Y` total functions, and
define:

```text
Q=image(pi).
```

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

### Theorem

There exists a unique total `g:Q->Y` such that

```text
tau=g composed_with pi
```

if and only if `closed(pi,tau)`.

### Necessity

Assume `tau=g composed_with pi`. For any `s,s'` with `pi(s)=pi(s')`:

```text
tau(s)=g(pi(s))=g(pi(s'))=tau(s').
```

Hence `ker(pi) subseteq ker(tau)`.

### Sufficiency

Assume closure. Define the relation:

```text
G={(q,y) in Q cross Y:
   there exists s in S with pi(s)=q and tau(s)=y}.
```

Every `q in Q=image(pi)` has a representative. Totality of `tau` supplies a
target value. If two states represent the same `q`, closure makes their target
values equal. Thus `G` is the graph of a total function `g:Q->Y`, and for every
`s in S`:

```text
g(pi(s))=tau(s).
```

### Uniqueness

Let `g1,g2` both factor `tau`. For any `q in Q`, the definition
`Q=image(pi)` guarantees some `s` with `pi(s)=q`. Then:

```text
g1(q)=g1(pi(s))=tau(s)=g2(pi(s))=g2(q).
```

Therefore `g1=g2`.

### Boundaries

- If `S=empty`, then `Q=empty`; the unique empty function factors the empty
  `tau`, and closure is vacuous.
- Infinite domains are covered because the construction is pointwise; no
  finiteness or global representative-choice function is assumed.
- Injective `pi` makes closure automatic.
- Constant `pi` on nonempty `S` makes closure equivalent to constant `tau`.
- Partial or multivalued maps are outside this theorem.
- On a separate strict superdomain of `image(pi)`, an extension requires
  `Y` nonempty; off-image values are generally nonunique and become unique only
  when `Y` is a singleton.

## Part II — exact typed witness

Let `P={p0,p1}` be the exact provenance records in the fixture, `B` the set of
canonical JSON byte strings, `J:P->B` the declared canonicalizer, and
`X={x}` the exact singleton of task coordinates.

The canonicalizer is UTF-8 `json.dumps` with `sort_keys=True`, separators
`(',',':')`, `ensure_ascii=True`, `allow_nan=False`, and no trailing newline.
Its domain here is JSON objects and arrays whose leaves are integers, strings,
booleans, or null.

The two target records serialize to:

```text
J(p0)={"activity_id":"activity-0","agent_id":"agent-0","entity_id":"entity-0"}
J(p1)={"activity_id":"activity-0","agent_id":"agent-1","entity_id":"entity-0"}
```

They differ. Define:

```text
S=X cross P
Y=J(P)

tau:X cross P->Y
tau(x,p)=J(p)

pi_task:X cross P->X
pi_task(x,p)=x

pi_full:X cross P->X cross P
pi_full(x,p)=(x,p)

g_full:X cross P->Y
g_full(x,p)=J(p).
```

The sole task fiber contains both witness states while their `tau` values
differ. Therefore:

```text
for every total deterministic g_task:X->Y,
g_task composed_with pi_task differs from tau on at least one state.
```

This excludes every total deterministic task-only reconstructor on the declared
domain, not merely the literal capture action. The full fibers are singletons,
so `g_full` is the unique full factor.

The witness is deliberately constructed. It establishes a record-reconstruction
fact relative to researcher-chosen `tau`; it is not a general provenance policy
or security verdict.

## Part III — common manifest and run objects

### Candidate common manifest M

A candidate manifest `M` is one JSON object with schema
`omst-c2-v9-environment-manifest`. It contains no cell identifier or process.
It binds only state common to every run in either pair:

1. its absolute path and canonical payload SHA-256;
2. fixture, launcher, and normative configuration paths and hashes;
3. interpreter link, resolved target, exact `sys.version`, and executable hash;
4. standard-library JSON path and hash;
5. dependency-lock path and hash;
6. LangGraph and LangChain-core distribution names, exact versions,
   installation roots, import module origins, package roots, and hashes of
   deterministic inventories of every installed distribution file;
7. eight LangGraph and three LangChain-core load-bearing paths and hashes;
8. LangGraph tag `1.2.9` and commit
   `95af6a00718588e7b7ce17310e8006d267896a77`;
9. an independent source-audit report path/hash and an ordered assertion list;
10. exact `sys.path`, meta-path identities, path-hook identities, site-package
    roots, and `.pth` path/hash/executable inventory;
11. absent trace/profile functions, `sitecustomize`, `usercustomize`, and
    executable `.pth` code; and
12. exact empty callbacks, tags, metadata, and configurable mapping.

`manifest_payload_sha256` is SHA-256 of canonical JSON after removing only the
digest field. The manifest's own absolute path is inside that payload. A future
acquired manifest is therefore a new immutable artifact rather than an edit to
`M0`.

### Run object R_cell

For `cell` in:

```text
{task_s0,task_s1,full_s0,full_s1},
```

`R_cell` is one candidate execution record containing:

- exactly one cell and its fixed run ID;
- the payload identity of common manifest `M`;
- the exact role-launcher parent and clean child argv/environment;
- a fresh child process and temporary directory;
- one locally imported framework instance and one compiled graph;
- ordered pre-import authentication, compile, final guard, and optional invoke
  events;
- callable-entry bytes if capture is reached; and
- the sole canonical output record if the run completes.

The binding is literal:

```text
task_s0 <-> R_task_s0
task_s1 <-> R_task_s1
full_s0 <-> R_full_s0
full_s1 <-> R_full_s1.
```

No `R_cell` is part of `M`. No run object is shared between cells.

### Observation function

On completed well-formed run objects, define:

```text
received(cell,M,R_cell)=R_cell.capture_entry_bytes.
```

`P_cell` below entails that this field is defined and that the emitted
`observed_hex` is exactly its hexadecimal encoding. `C_task` and `C_full` are
stated only under role antecedents that include both required `P_cell` facts;
no failed or absent run is silently converted into an observation.

## Part IV — exact current manifest M0

`experiments/configs/omst-c2-v9-M0-unacquired.json` has file SHA-256:

```text
0ee71cc664450cc752e82061d1c0da0a18346e7ce0785f8a712832f8b8b4c40e
```

Its canonical payload SHA-256 is:

```text
846f502e2984ccfba22fedd7b686f8f56d38d351deb48e62dcec46f131301ec1
```

It records:

```text
interpreter link:
/home/soh/agent-security/comp/.venv/bin/python

resolved target:
/home/linuxbrew/.linuxbrew/Cellar/python@3.14/3.14.3_1/bin/python3.14

sys.version:
3.14.3 (main, Feb  3 2026, 15:32:20) [GCC 12.3.0]

interpreter SHA-256:
eca90b668424db6f2105504128f02cac91c2805de9a928abcc272d1444abfde0

stdlib JSON path:
/home/linuxbrew/.linuxbrew/Cellar/python@3.14/3.14.3_1/lib/python3.14/json/__init__.py

stdlib JSON SHA-256:
95022d150a27a2bfd54ac21bfce35812c96b53c420bb7b018dcb573f13e52da0

LangGraph: absent
LangChain-core: absent
dependency lock: absent
source audit: absent
status: unacquired
P_common(M0): false.
```

The clean-child import context has four exact `sys.path` entries, three default
meta-path identities, two default path hooks, one venv site-package root, and no
`.pth` files. The child environment is exactly `HOME=/nonexistent`, `LANG=C`,
`LC_ALL=C`, and `TZ=UTC`.

`verify_common_manifest` first requires `status=acquired`. Thus `M0` would fail
with `manifest_status` before package discovery or framework import. That fact
was checked from code and JSON only; v9 was not executed.

## Part V — closed v9 subject

### Immutable artifact identity

At commit `a0849f6`:

```text
experiments/omst_c2_v9_fixture.py
SHA-256 e9e95741cd306d0aa11456f0977b4e129654653a24a00669fe9aa58e47e20284

experiments/run_omst_c2_v9_fixture.sh
SHA-256 312e104111cd901fddffd921b378b361d72eb082a728f97b3dbe742afa3f4ffd
mode 0755

experiments/configs/omst-c2-v9-manifest-run-pairs.json
SHA-256 a93dcc281c995181c55e9e102030ad4da4c46a6208a10b6dd9af19478388249e
```

The fixture binds:

- exact `S0,S1`, schemas, ordered channel lists, cells, and run IDs;
- one capture callable that serializes before its first write;
- one graph with explicit input schema and START/capture/END edges;
- explicit `None` checkpointer, cache, store, node retry, and node cache;
- the complete common-manifest verifier;
- one final combined post-compile guard function;
- at most one invoke; and
- one five-field canonical output record: `cell`, `manifest_id`,
  `observed_hex`, `run_id`, and `status`.

There is no top-level import of LangGraph or LangChain-core.

### Pre-import authentication

After loading and authenticating the canonical payload, but before the local
framework import, `verify_common_manifest(M)` checks:

1. `status=acquired` and the exact four-variable child environment;
2. fixture, launcher, and config paths/hashes;
3. interpreter link/target/version/hash and stdlib JSON path/hash;
4. present dependency-lock path/hash;
5. exactly two required distributions, their versions, install roots, full
   distribution-tree hashes, module origins, and package roots;
6. the exact set and hashes of eleven load-bearing source files;
7. LangGraph tag/commit, source-audit report path/hash, and the exact six
   verified assertion names;
8. absent trace/profile and site/user customization; and
9. exact import context and no executable `.pth` file.

This pre-import check prevents the fixture from importing an unauthenticated
framework bundle. It is not the claimed final guard: all these checks run again
after compilation.

### Exact final guard order

Inside `run_cell`, the only possible successful order is:

```text
verify_common_manifest(M)
build_graph(schema)
verify_all_guards(M,graph,expected_channels)
graph.invoke(...).
```

`build_graph` contains the local LangGraph import and returns the compiled
graph. The next statement is `verify_all_guards`; the next observation-capable
statement is the sole `graph.invoke`.

`verify_all_guards` first reruns the complete common verifier. It therefore
reauthenticates, after import and compilation:

- artifact and interpreter/stdlib identities;
- distribution versions, origins, roots, and full-tree hashes;
- dependency-lock identity;
- every load-bearing file hash;
- the source-audit report and assertions;
- import context, trace/profile/customization state; and
- exact runnable config.

It then checks:

- exact compiled `proc.channels`;
- `proc.mapper is None`;
- node cache and retry policies are `None`; and
- compiled checkpointer, cache, and store are `None`.

A failed check raises `OMST_RUNTIME_GUARD_FAILED:<label>` before invoke and
before any correspondence observation. This is one final post-compile guard
bundle, not two separated environment/compiled guard phases.

### Role-specific launcher

The authoritative outer argv prefix is:

```text
/usr/bin/env -i
HOME=/nonexistent
PATH=/usr/bin:/bin
LANG=C
LC_ALL=C
TZ=UTC
/bin/bash --noprofile --norc
/home/soh/agent-security/experiments/run_omst_c2_v9_fixture.sh
```

Exactly two actual argv elements follow: a role in `{task,full}` and an
absolute path naming actual manifest `M`.

The script asserts absent `BASH_ENV` and `ENV`, validates the absolute manifest
path, and emits no launcher-owned stdout.

If the role is `task`, it runs only:

```text
task_s0 R_task_s0
task_s1 R_task_s1.
```

If the role is `full`, it runs only:

```text
full_s0 R_full_s0
full_s1 R_full_s1.
```

Each child uses a distinct `/usr/bin/env -i`, the four exact environment
variables, the absolute interpreter link, Python `-I -B`, the absolute fixture,
the actual absolute manifest path, and its exact cell/run-ID pair. Each child
creates one temporary directory and one graph. No graph, checkpoint, channel,
cache, callback manager, input object, or output buffer is shared.

The launcher remains unexecuted.

## Part VI — source bridge

### Authenticated LangGraph basis

The manifest schema requires LangGraph tag `1.2.9`, commit:

```text
95af6a00718588e7b7ce17310e8006d267896a77
```

and installed hashes for:

1. `langgraph/graph/state.py`;
2. `langgraph/pregel/_loop.py`;
3. `langgraph/pregel/_checkpoint.py`;
4. `langgraph/pregel/_io.py`;
5. `langgraph/pregel/_algo.py`;
6. `langgraph/pregel/_retry.py`;
7. `langgraph/pregel/_read.py`; and
8. `langgraph/_internal/_runnable.py`.

The commit-bound paths correspond to:

- [`state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py);
- [`_loop.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py);
- [`_checkpoint.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_checkpoint.py);
- [`_io.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_io.py);
- [`_algo.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_algo.py);
- [`_retry.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_retry.py);
- [`_read.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_read.py); and
- [`_runnable.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/_internal/_runnable.py).

### LangChain-core basis

`M0` has no LangChain-core distribution. A future acquired `M` must bind exact
version, distribution tree, origin, roots, and file hashes for:

1. `langchain_core/runnables/base.py`;
2. `langchain_core/runnables/config.py`; and
3. `langchain_core/callbacks/manager.py`.

The acquired source-audit report must independently verify the precise
callable/config/callback no-pre-capture-mutation assertion. Until that report
and those exact files exist, `P_common(M)` is not discharged. v9 does not call
the absent future source bundle complete.

### L_compile(M)

Authenticated `state.py` registers the exact `TypedDict` state and input
schemas. Ordinary fields use `LastValue`; the capture node's selected channels
derive from the explicit input schema; mapping input has no model-coercion
mapper; the START `PregelNode` and writers are compiled; and retained services
match the explicit `None` inputs. The final guard checks the load-bearing
compiled identities.

### L_start(M)

For this graph, input channels are the single START channel. Authenticated
`_io.map_input` writes:

```text
(START, whole literal input dict),
```

not a tuple per state field. The START task receives that `EphemeralValue`.
Authenticated `state.py` constructs the START writer with `_get_updates`, which
filters the whole mapping into GraphState field writes and emits the capture
branch trigger. `_loop.apply_writes` makes the selected `LastValue` fields
available for the next superstep.

### L_fresh(M)

With no saved checkpoint, authenticated `_loop.py` substitutes
`_checkpoint.empty_checkpoint()`. Its channel values, versions, and seen maps
are empty. `channels_from_checkpoint` constructs fresh channel instances before
L_start. The new process and graph exclude prior loop state.

### L_prepare(M)

Authenticated `_loop.tick` calls `_algo.prepare_next_tasks`.
`prepare_next_tasks` creates a fresh `input_cache`; `_proc_input` reads all
available selected channels, applies a mapper only if non-`None`, and assigns
the resulting mapping to `PregelExecutableTask.input`.

### L_deliver(M)

Authenticated `_retry.run_with_retry` invokes `task.proc` with `task.input`.
Authenticated `_read.PregelNode.node` constructs
`RunnableSeq(bound,writers)`. Authenticated LangGraph
`_internal/_runnable.RunnableSeq` passes its initial input unchanged to the
first bound `RunnableCallable`; only its return reaches writers. The bound
callable is `capture`.

The exact authenticated LangChain-core config/callback implementation must have
no pre-capture mutation authority under the literal empty config. Passive
observation that cannot mutate callable-entry input is irrelevant.

The complete source-conditional trace is:

```text
literal dict
-> START EphemeralValue as one whole dict
-> START task input
-> _get_updates field writes plus capture trigger
-> selected LastValue availability
-> PregelExecutableTask.input
-> PregelNode RunnableSeq(bound,writers)
-> bound RunnableCallable receives unchanged initial input
-> capture(mapping) before any write.
```

These lemmas are per-cell delivery facts. None states a cross-run byte equality
or exact difference.

## Part VII — premises

### P_common(M)

`P_common(M)` is the conjunction of:

**PC1 — canonical manifest identity.** `M` has the required schema, bound
absolute path, valid payload digest, and `status=acquired`.

**PC2 — common artifact/runtime identity.** Fixture, launcher, config,
interpreter, stdlib JSON, child environment, dependency lock, exact package
set, package versions, package roots, module origins, and full distribution-tree
hashes match `M` before import and again after compile.

**PC3 — load-bearing source identity.** The exact eight LangGraph and three
LangChain-core installed source paths/hashes match `M` before import and again
after compile. LangGraph tag/commit metadata match the fixed values.

**PC4 — independent source semantics.** An independent audit of the exact
authenticated source bundle establishes `L_compile`, `L_start`, `L_fresh`,
`L_prepare`, `L_deliver`, and the LangChain-core callback/config
no-pre-capture-mutation assertion. The exact report path/hash and ordered
assertion list match `M` at both runtime checks.

PC4 means the source statements are true for the authenticated bundle; the
report is its immutable evidence. Merely writing `status=passed` in an
unaudited manifest does not satisfy PC4.

**PC5 — import-context exclusion.** Exact `sys.path`, import finders/hooks,
site roots, and `.pth` inventory match `M` before import and after compile;
trace/profile, site/user customization, and executable `.pth` authority are
absent.

**PC6 — literal runnable config.** Callbacks and tags are empty; metadata and
configurable mappings are empty; their runtime value matches `M`.

No PC item contains `C_task`, `C_full`, the equality of literal task fields, or
the difference between literal provenance records. The common antecedent is
therefore not the conclusion in disguise.

### P_cell(M,cell,R_cell)

`P_cell(M,cell,R_cell)` is the conjunction of:

**PR1 — role/cell binding.** `R_cell` names the exact cell and fixed run ID,
uses the manifest payload of `M`, and is spawned only by the matching role
launcher branch.

**PR2 — fresh isolation.** The child has the exact `env -i` state, its own
process and fresh temporary directory, and shares no graph/run objects with any
other cell.

**PR3 — exact local subject.** It loads the authenticated fixture, binds the
literal schema/state/channel triple, imports locally only after common
preauthentication, and compiles exactly one graph.

**PR4 — final atomic guard.** Immediately after compile and before invoke,
`verify_all_guards` returns successfully. That single call reauthenticates all
PC runtime identities and the compiled channels/mapper/policies/services.

**PR5 — single delivery and observation.** Exactly one invoke occurs after the
guard; the source lemmas deliver the selected mapping to `capture`; capture
serializes at callable entry before returning a write; the sole output's
`observed_hex` derives only from those bytes.

A failed guard or missing invoke makes `P_cell` false. It cannot contribute a
sentinel, missing value, or partial output to either conclusion.

### Role-specific antecedents

Define:

```text
P_task(M,R_task_s0,R_task_s1)
iff
P_common(M)
and P_cell(M,task_s0,R_task_s0)
and P_cell(M,task_s1,R_task_s1).
```

Define separately:

```text
P_full(M,R_full_s0,R_full_s1)
iff
P_common(M)
and P_cell(M,full_s0,R_full_s0)
and P_cell(M,full_s1,R_full_s1).
```

There is no free `cell` variable. The task antecedent has no full-cell premise;
the full antecedent has no task-cell premise.

## Part VIII — two conditional propositions

### Task proposition

For every `M,R_task_s0,R_task_s1`:

```text
P_task(M,R_task_s0,R_task_s1)
-> C_task(M,R_task_s0,R_task_s1).
```

### Task derivation

Assume `P_task`. PC2-PC6 give one identical authenticated common bundle for
both task runs, including canonicalizer and source semantics. Each `P_cell`
gives the exact task schema, successful final guard, and source delivery path.
L_compile/L_start/L_fresh expose exactly the five task fields. L_prepare forms
that mapping as `task.input`; L_deliver supplies it unchanged to `capture`.

The five task values in literal `S0` and `S1` are equal. That cross-run literal
equality is not part of any source lemma or guard premise. Deterministic
canonicalization under the same authenticated stdlib JSON therefore gives:

```text
received(task_s0,M,R_task_s0)
=received(task_s1,M,R_task_s1).
```

Hence `C_task`.

### Full proposition

For every `M,R_full_s0,R_full_s1`:

```text
P_full(M,R_full_s0,R_full_s1)
-> C_full(M,R_full_s0,R_full_s1).
```

### Full derivation

Assume `P_full`. The corresponding common and per-cell premises deliver the
six-field full mappings to capture. Literal `S0,S1` agree on the five task
fields and on provenance entity/activity IDs; their provenance agent IDs are
`agent-0` and `agent-1`. Deterministic canonicalization gives two decoded
mappings that differ at exactly that leaf. Hence `C_full`.

The full derivation uses no task-run premise. Its success or failure cannot
alter whether `P_task->C_task` applies.

### Universal form

Combining the separately proved implications:

```text
for every M,R_task_s0,R_task_s1,
P_task(M,R_task_s0,R_task_s1)
-> C_task(M,R_task_s0,R_task_s1)

and independently

for every M,R_full_s0,R_full_s1,
P_full(M,R_full_s0,R_full_s1)
-> C_full(M,R_full_s0,R_full_s1).
```

This does not assert `P_common(M0)`, completion of any run, or an unconditional
framework observation.

## Failure semantics and falsifiers

1. A countermodel to the factorization equivalence falsifies Part I.
2. Equal canonical witness targets or a type error invalidates Part II.
3. An invalid/unacquired manifest makes `P_common(M)` false; no role conclusion
   is established for that manifest.
4. Package/source/lock/import-context drift detected before import aborts before
   framework loading.
5. Drift or compiled-identity mismatch detected in the final guard aborts
   before invoke and makes that `P_cell` false.
6. With `P_task` true, any task byte inequality falsifies the task framework
   application.
7. With `P_full` true, equality, a wrong agent value, or any extra difference
   falsifies only the full-control application.
8. Failure of either full run does not affect the task antecedent.
9. Failure of either task run does not affect the full antecedent.
10. A source audit that cannot establish its six assertions keeps PC4 false;
    an audit label alone is insufficient.
11. None of these outcomes establishes a general security failure, production
    policy, empirical prevalence, or benchmark effect.

## Assumptions and validity domains

### Mathematical assumptions

| Assumption | Role | Validity boundary |
|---|---|---|
| `pi,tau` total | theorem equality domain | Partial/multivalued variants require another theorem. |
| `Q=image(pi)` | canonical unique factor domain | A strict larger domain adds off-image freedom. |
| `J(p0)!=J(p1)` | witness contradiction | If targets collapse, task impossibility disappears. |
| exact product `X cross P` | both provenance alternatives share one task fiber | A correlated domain omitting a state can remove the witness fiber. |

### Application assumptions

| Assumption | Control | Failure consequence |
|---|---|---|
| One common immutable bundle | payload plus double runtime authentication | Role implication remains unapplied. |
| Installed bytes match audited bytes | distribution/source/lock/audit hashes rechecked after compile | Cell aborts before invoke. |
| Source lemmas true | independent exact-bundle audit, PC4 | `P_common` false; no correspondence inference. |
| Selected mapping delivered unchanged | source trace plus mapper/callback/import guards | Applicable correspondence falsified or antecedent false. |
| Fresh run state | exact role launcher, child process, tempdir, no services | `P_cell` false. |
| Canonicalizer deterministic | exact code, primitive-container domain, stdlib hash | Byte conclusion invalid. |
| Output derives only from entry bytes | capture-before-write and output binding | `P_cell` false. |

## Rival explanations and controls

1. **Mapper adds or drops fields.** L_compile plus final `mapper is None` and
   exact channel checks.
2. **START performs per-key input filtering earlier than claimed.** The trace
   explicitly writes one whole dict to START and locates filtering in
   `_get_updates`.
3. **A selected channel is unavailable.** L_start/L_fresh plus independent
   source audit; an execution mismatch falsifies the application.
4. **Checkpoint or input cache is stale.** Fresh process, empty checkpoint,
   fresh channel instances, and fresh `prepare_next_tasks` cache.
5. **Runnable writers see initial input before capture.** `_read` and LangGraph
   RunnableSeq establish bound callable first, writers second.
6. **Callbacks mutate before capture.** Empty config plus exact acquired
   LangChain-core source audit; passive non-mutating observation is allowed.
7. **Import customization mutates globals or inputs.** Exact context before
   import and after compile; no trace/profile/site/user/executable-pth authority.
8. **A package changes between audit and execution.** Package trees, lock,
   source files, and audit report are checked before import and again after
   compile.
9. **One cell passes while its pair does not.** Role antecedent explicitly
   requires both named `P_cell` facts; no free cell variable remains.
10. **Optional full failure erases task evidence.** `P_task` contains no full
    run object or full cell.
11. **Outer shell contamination changes commands/output.** Absolute Bash under
    outer `env -i`, absent BASH_ENV/ENV, absolute child executables.
12. **Capture or output code manufactures equality.** Capture serializes its
    sole entry mapping before any write; output only hex-encodes those bytes.
13. **Canonicalization ambiguity.** Exact options, stdlib file, and
    primitive-leaf JSON-container domain.
14. **Researcher-selected target is mistaken for a security theorem.** Scope is
    record reconstruction relative to `tau`, repeated in claims and nonclaims.
15. **Classical theorem is inflated as novelty.** The factorization result is
    explicitly standard and cannot carry a standalone contribution claim.

## Fixed bias surface

| Bias | Operation here | Control |
|---|---|---|
| Selection | Purpose-built two-state witness could be mistaken for a population | No population or prevalence inference; exact domain stated. |
| Confounding | Environment drift could masquerade as schema behavior | One common `M`; complete double authentication. |
| Assignment | Cells could use mismatched states/schemas | Literal cell/run-ID binding and role-specific launcher. |
| Protocol deviation | Wrong role, extra child, missing final guard, or extra invoke | Exact launcher AST/text, two children per role, exact call order. |
| Missing data | Failed cell could be treated as an observation | Failed/missing run makes `P_cell` false; no sentinel outcome. |
| Measurement | Post-write output could differ from callable entry | Capture serializes at entry before returning any write. |
| Analysis flexibility | Roles could be pooled after failures | Separate fixed implications and exact per-role falsifiers. |
| Selective reporting | Only a favorable pair could be disclosed | Both propositions and all role-specific failure states preregistered. |

## Taxonomy, anti-stacking, and parsimony

### Idea taxonomy

The classification is:

```text
Scope Mismatch x Formal Derivation x formalize
```

with `decouple` secondary. It is not Bridge Opportunity ×
Synthesis/Unification, and its dominant operation is not integrate/unify/merge.

### Anti-stacking

The distinguishing prediction is universal on the declared witness domain:
because one task fiber contains two target values, **every** total deterministic
task-only reconstructor fails on at least one state. Testing one composed
implementation could only reject that implementation. Adding several checkers
would not produce the universal quantifier.

The framework portion is a correspondence control, not a stack of defenses.
Manifest authentication and the final guard are necessary to bind the exact
execution bundle to the already required source-conditional premise; they do
not add a claimed security effect.

### Occam's Razor

The theorem uses `Q=image(pi)` and two states, the smallest nonconstant-fiber
witness. The v9 engineering interface has exactly one common manifest, one run
object per cell, and one antecedent per role pair. It removes the global
four-cell conjunction. The pre-import authentication prevents importing an
unauthenticated bundle; the repeated post-compile authentication closes the
audit-to-invoke drift window and is the single claimed final guard. Neither can
be deleted while retaining both properties.

The full control remains optional and independent. Hash seed is not fixed or
claimed. Locale/timezone are isolated execution hygiene, not mathematical
premises.

## Novelty and scope boundaries

What is claimed:

- a correct application of classical factorization;
- an exact two-state schema-sufficiency witness;
- a closed, falsifiable, role-separated conditional correspondence protocol.

What is not claimed:

- new quotient/factorization mathematics;
- `P_common(M0)`;
- an installed, audited, or executed current framework bundle;
- unconditional LangGraph behavior;
- a general provenance or security policy;
- a framework vulnerability;
- an empirical effect, prevalence, benchmark, or production guarantee;
- a standalone top-tier contribution from this control; or
- a held-out/test result.

## Problem alignment

If the role-specific source-conditional task proposition later survives its
authorized gate, it supplies an independently checkable orchestration control:
one can distinguish a true projection-induced loss of reconstructability from
environment drift or optional-control failure. That directly serves
`PROBLEM.md`'s question about security properties under graph rewrites while
preserving the proxy caveat and narrow synthetic scope.

## Deterministic verification plan before review

Without importing or executing LangGraph:

1. parse fixture AST and launcher Bash syntax;
2. validate normative config, M0, and state JSON;
3. check mode, all artifact hashes, M0 file hash, and M0 canonical payload;
4. prove no top-level framework import exists;
5. statically verify the only run-cell order is common authentication,
   `build_graph`, complete final guard, then invoke;
6. verify task and full launcher branches each name exactly their two cells and
   no opposite-role cell;
7. enumerate the factorization theorem over `|S|=0..4`, three projection
   labels, two target labels, and every reachable-image action;
8. recompute canonical witness target bytes;
9. verify exact source-path counts `8+3`, four cell/run-ID bindings, two
   independent antecedents, and `P_common(M0)=false`;
10. verify every previous reviewed hypothesis and verdict remains unchanged;
11. scan for unresolved placeholders or unauthorized result claims; and
12. dispatch the final sterile reviewer only if all deterministic checks pass.

## Round-8 author disposition

| Round-8 defect | v9 author claim before independent review |
|---|---|
| Ill-scoped one-cell environment/free cell | **AUTHOR-RESOLVED:** common `M`; four explicit `R_cell`; quantified pair antecedents. |
| Missing runtime framework/source/lock reauthentication | **AUTHOR-RESOLVED:** full distribution trees, origins, versions, lock, eleven source hashes, audit report, artifacts and import context checked before import and again after compile. |
| Guard-order mismatch | **AUTHOR-RESOLVED:** local import/compile in `build_graph`; immediately next `verify_all_guards`; immediately next sole invoke. |
| Full control coupled to task | **AUTHOR-RESOLVED:** independent `P_task` and `P_full`, each with only its two cells. |

These are author claims. Only the independent reviewer can mark them resolved.

## Review gate

Return `RIGOROUS` only after:

1. re-deriving the theorem, empty/infinite/larger-domain boundaries, and exact
   witness, while seeking countermodels;
2. checking `M` has no cell/process and every `R_cell` is separately quantified;
3. checking `P_task` and `P_full` contain only their own pair and neither has a
   free variable;
4. checking PC/PR premises do not contain either conclusion;
5. checking full pre-import authentication and the exact single final
   post-compile/pre-invoke reauthentication bundle against the committed code;
6. checking distribution/lock/source/audit/import identities are actually
   included at runtime;
7. checking the START, channel, task preparation, RunnableSeq, callback/config,
   and capture-before-write source chain;
8. confirming `P_common(M0)=false`, absent exact LangChain-core sources, and no
   unconditional framework inference;
9. validating role-specific failure semantics, taxonomy, anti-stacking,
   parsimony, and scope; and
10. identifying the strongest remaining counterexample or testability gap.

A `RIGOROUS` verdict closes Phase 2 only for the unconditional mathematics,
exact witness, and two universal conditional implications. It does not make an
antecedent true or authorize acquisition/execution.

## Authorization boundary

Authorized: this local superseding hypothesis, code-as-text/static checks,
already-scoped source inspection, and one final sterile theory review after the
lower verification rungs pass.

Not authorized: framework download, installation, import, compile, invoke, or
observation; Kaggle; held-out or locked-test action; live targets; operational
attacks or jailbreak reproduction; model APIs; external messages; publication.
