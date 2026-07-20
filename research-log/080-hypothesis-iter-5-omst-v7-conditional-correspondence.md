# Hypothesis — iteration 5, OMST v7 conditional correspondence

**Date:** 2026-07-20  
**Phase:** 2 — hypothesis formation  
**Cycle:** 2  
**Status:** superseding theoretical hypothesis, not yet reviewed  
**Claim type:** unconditional formal derivation plus a conditional engineering
correspondence implication  
**Scope:** record reconstruction and schema sufficiency relative to `tau`

## Supersession and adverse-result record

This artifact supersedes but does not edit hypotheses v1-v6. The immediately
superseded artifact is
`research-log/076-hypothesis-iter-5-omst-v6-quotient-control.md` at immutable
commit `35b24a1`. Round-6 review is preserved verbatim in
`research-log/078-omst-theory-review-round6.md`.

Round 6 found the abstract theorem and typed witness rigorous, independently
checked 1,555 finite models including `S=empty`, and accepted the type, role,
scope, taxonomy, anti-stacking, and Occam corrections. Its four remaining
requirements concerned only framework correspondence:

1. derive or correctly condition on the complete loop/input/channel/task path;
2. replace environment/source placeholders and control callbacks/imports;
3. bind the complete four-cell fixture and launcher; and
4. include JSON containers in the canonicalization domain.

The c2-v7 amendment in `research-log/079` accepts the central criticism: the
current environment does not contain LangGraph or LangChain-core, so their
runtime identity cannot be asserted. v7 proves a conditional implication and
does not claim that its antecedent is currently true.

## One-sentence hypothesis

A full-state target factors uniquely through an input projection exactly when
it is constant on every projection fiber; the exact two-state task projection
cannot reconstruct distinct provenance bytes, and an acquired pinned LangGraph
environment realizes that task projection only conditionally on the complete
premise bundle `P`.

## Exact claim ledger

### Unconditional claims

1. For sets `S,Y`, total `pi:S->Q=image(pi)` and total `tau:S->Y`, there exists
   a unique `g:Q->Y` with `tau=g composed_with pi` exactly when
   `ker(pi) subseteq ker(tau)`.
2. For the fully typed exact witness, no total deterministic function on the
   task singleton reconstructs both distinct provenance targets.
3. The exact full projection has the declared unique factor.

### Conditional claims

```text
P -> C_task
P -> C_full.
```

`C_task` is load-bearing for a later pinned-framework application. `C_full` is
an optional positive control.

### Claims expressly absent

- `P` is currently discharged;
- unconditional LangGraph correspondence;
- a framework execution or empirical result;
- a general security failure, framework vulnerability, production provenance
  policy, effect, prevalence, or benchmark claim;
- new mathematical theory or standalone top-tier novelty; and
- any framework acquisition/import/run, Kaggle, held-out or locked-test action,
  live-target test, operational attack, model API, external message, or
  publication.

## Normative artifacts

- contract: `experiments/configs/evaluation-contract-orchestration-c2.md`;
- machine specification:
  `experiments/configs/omst-c2-v7-conditional-correspondence.json`;
- closed fixture: `experiments/omst_c2_v7_fixture.py`;
- isolated launcher: `experiments/run_omst_c2_v7_fixture.sh`; and
- amendment/source record: `research-log/079`.

The fixture and launcher are code-as-text. They have not been imported or run.

## Part I — unconditional mathematics

### Formal objects

Let `S,Y` be arbitrary sets. Let `pi:S->Q` and `tau:S->Y` be total functions,
where `Q` is defined to be `image(pi)`.

For a function `h`, define:

```text
(u,v) in ker(h) iff h(u)=h(v).
```

Define closure relative to the target:

```text
closed(pi,tau) iff ker(pi) subseteq ker(tau).
```

Equivalently, `tau` is constant on each fiber
`F_q={s in S:pi(s)=q}`.

### Theorem

```text
exists unique total g:Q->Y with tau=g composed_with pi
iff
closed(pi,tau).
```

### Necessity

Assume `tau=g composed_with pi`. For arbitrary `s,s'` with
`pi(s)=pi(s')`:

```text
tau(s)=g(pi(s))=g(pi(s'))=tau(s').
```

Therefore `ker(pi) subseteq ker(tau)`.

### Sufficiency

Assume closure. Define the relation:

```text
G={(q,y) in Q cross Y:
   there exists s in S with pi(s)=q and tau(s)=y}.
```

Every `q in Q=image(pi)` has a representative. Totality of `tau` gives one
value. If two representatives give `y,y'`, they are in the same `pi` fiber, so
closure gives `y=y'`. Thus `G` is the graph of a total function `g:Q->Y`, and
its definition gives `g(pi(s))=tau(s)` for every `s`.

No arbitrary representative-selection function or global choice axiom is
needed; unique existence of a value for each `q` directly defines `g`.

### Uniqueness

If `g1,g2` both factor `tau`, then for each `q in Q` there exists `s` with
`pi(s)=q`, and:

```text
g1(q)=g1(pi(s))=tau(s)=g2(pi(s))=g2(q).
```

Hence `g1=g2`.

### Boundaries

- If `S` is empty, then `Q` is empty; the unique empty `g` factors the unique
  empty `tau`, and closure is vacuous.
- The argument is pointwise and does not assume finiteness.
- If `pi` is injective, closure is automatic.
- If `pi` is constant on nonempty `S`, closure is constancy of `tau`.
- Partial or multivalued maps require another formulation.
- If a separate domain `Q0` strictly contains `image(pi)`, the image factor
  remains unique. It extends when `Y` has an element; off-image values are
  generally nonunique, with singleton `Y` as the obvious exception.

This is the standard factorization of a function through the quotient induced
by `ker(pi)`.

## Part II — fully typed witness

Let `P={p0,p1}` be the two exact provenance records in the fixture. Let `B` be
the set of canonical JSON byte strings and `J:P->B` the total canonicalizer.
Let `X={x}` be the exact task singleton.

Canonicalization is UTF-8 `json.dumps` with `sort_keys=True`, separators
`(',',':')`, `ensure_ascii=True`, `allow_nan=False`, and no trailing newline.
Its domain here is JSON objects and arrays whose leaves are integers, strings,
booleans, or null. The witness uses nested objects and one empty array.

The two exact targets are:

```text
J(p0)={"activity_id":"activity-0","agent_id":"agent-0","entity_id":"entity-0"}
J(p1)={"activity_id":"activity-0","agent_id":"agent-1","entity_id":"entity-0"}
```

They are unequal. No global JSON-injectivity premise is used.

Define:

```text
S = X cross P
Y = J(P)

tau:X cross P->Y                    tau(x,p)=J(p)
pi_task:X cross P->X                pi_task(x,p)=x
pi_full:X cross P->X cross P        pi_full(x,p)=(x,p)
g_full:X cross P->Y                 g_full(x,p)=J(p)
```

Both witness states occupy the same `pi_task` fiber and have different `tau`
values. Closure fails, so:

```text
for every total deterministic g_task:X->Y,
g_task composed_with pi_task differs from tau on at least one state.
```

Every `pi_full` fiber is a singleton. Closure holds, and `g_full` is the unique
factor.

The target was researcher-selected to expose one missing coordinate. This is a
universal logical consequence for an exact record-reconstruction control, not
independent empirical evidence or a general security obligation.

## Part III — closed future fixture

### Complete bindings

`experiments/omst_c2_v7_fixture.py` binds:

- `ProvenanceRecord`, `TaskStateOnly`, `TaskStatePlusProvenance`, and
  `GraphState` as literal standard-library `TypedDict`s;
- literal `S0,S1` values;
- exact task and full ordered channel lists;
- all four named cells `task_s0`, `task_s1`, `full_s0`, `full_s1`;
- explicit empty callbacks, tags, metadata, and configurable mappings;
- `StateGraph(GraphState)`, one capture node with explicit input schema,
  `START -> capture -> END`, and explicit `None` checkpointer/cache/store;
- assertions on compiled channels, mapper, cache/retry policies, and compiled
  services;
- one graph invocation on a deep copy;
- callable-entry canonicalization before the first returned write; and
- one canonical diagnostic record containing only cell, observed bytes as hex,
  and completion status.

The fixture SHA-256 is:

```text
e26bca99b0aa9e614308ab0330501d03f78758181f0f4627137da40fb8305d09
```

### Isolated launcher

`experiments/run_omst_c2_v7_fixture.sh` binds four separate commands, one per
cell. Every command uses `/usr/bin/env -i`, the exact interpreter path, Python
`-I -B`, and only:

```text
LANG=C
LC_ALL=C
TZ=UTC
PYTHONHASHSEED=0
PYTHONNOUSERSITE=1
```

The launcher SHA-256 is:

```text
ff9be2b71a41d26cb60b59bb8670cacb8e63e89349efff921cabe52cd12df68c
```

Each process creates its own temporary directory and one graph. No Python
object, graph, checkpoint, channel, cache, callback manager, or capture buffer
is reused across cells.

The launcher remains unexecuted. In the current environment it cannot satisfy
the premise bundle because LangGraph and LangChain-core are absent.

### Literal local document-check environment

```text
interpreter:
/home/soh/agent-security/comp/.venv/bin/python

resolved interpreter:
/home/linuxbrew/.linuxbrew/Cellar/python@3.14/3.14.3_1/bin/python3.14

version:
CPython 3.14.3 (main, Feb 3 2026, 15:32:20) GCC 12.3.0

interpreter SHA-256:
eca90b668424db6f2105504128f02cac91c2805de9a928abcc272d1444abfde0

stdlib json SHA-256:
95022d150a27a2bfd54ac21bfce35812c96b53c420bb7b018dcb573f13e52da0

LangGraph: absent
LangChain-core: absent
```

These are literal values, not instructions to fill values later. The future
framework manifest is absent/unacquired, not represented by a placeholder.

## Part IV — commit-bound source derivation

The source subject is tag `1.2.9`, commit
`95af6a00718588e7b7ce17310e8006d267896a77`. Each cited file URL is bound
directly to that authenticated commit.

### L_compile

[`state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py)
registers `GraphState` and each explicit node input schema. Ordinary
unannotated fields become `LastValue` channels. `attach_node` derives the
capture `PregelNode.channels` from the selected input schema. The exact
`TypedDict` schemas are mapping types, so their mapper is `None` rather than a
model-coercion mapper. The fixture passes `None` for checkpointer, cache, and
store and asserts the compiled result.

Therefore, conditional on exact acquired source/dependencies, compile produces
the exact five task channels or those five plus provenance, with no mapper or
retained service.

### L_fresh

[`_loop.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py)
uses an empty checkpoint when no persisted tuple exists, hydrates channel
instances from it, invokes `_first`, maps graph input, and applies writes.

[`_checkpoint.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_checkpoint.py)
defines that checkpoint with empty channel values, channel versions, and seen
versions and constructs channel instances from the checkpoint/specs.

[`_io.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_io.py)
maps every key in the literal graph input that belongs to the compiled input
channels. The START node then writes the corresponding `GraphState` fields;
`apply_writes` makes those `LastValue` channels available and triggers the
capture node on the next superstep.

Because every selected task/full key is present in `S0,S1`, every selected
channel is available before capture.

### L_prepare

[`_loop.tick`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py)
calls `prepare_next_tasks` after input writes.

[`_algo.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_algo.py)
creates a fresh empty `input_cache` for each `prepare_next_tasks` call.
`_proc_input` reads every available selected channel, uses the channel aliases,
applies the mapper only when non-`None`, and yields the mapping. The PULL branch
assigns it to `PregelExecutableTask.input`.

### L_deliver

[`_retry.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_retry.py)
invokes `task.proc.invoke(task.input, config)` on the synchronous execution
path. The bound callable therefore receives the task mapping. The literal
capture serializes that sole argument before returning any write and has no
closure or mutable application global.

### Symbolic trace

Combining the four lemmas yields:

```text
literal state
-> START input
-> GraphState field writes
-> fresh LastValue values
-> capture PULL task
-> selected input-schema mapping
-> PregelExecutableTask.input
-> task.proc.invoke(task.input, config)
-> capture(mapping) before first write.
```

This is the static source bridge. It is not called a verified property of an
unacquired package environment.

## Part V — exact premise bundle P

`P` is the conjunction of:

### P1 — acquired identity

An authorized local environment is authenticated as LangGraph 1.2.9 at the
pinned commit, with exact installed LangGraph and LangChain-core versions,
source origins, licenses, dependency lock, and relevant file hashes.

### P2 — artifact identity

The fixture and launcher hashes match this hypothesis, and their static
compiled assertions pass without modification.

### P3 — isolated process environment

The exact launcher executes under `env -i` and `-I -B`, so no inherited tracing
variables, `PYTHONPATH`, user-site packages, or callback configuration enter.

### P4 — import-context audit

The acquired environment contains no `sitecustomize`, `usercustomize`,
executable `.pth` entry, import hook, or wrapper that can inspect or mutate the
literal input before capture.

### P5 — callback audit

The explicit `callbacks=[]`, empty tags/metadata/configurable mapping, and
acquired LangChain-core implementation yield no callback handler with authority
to mutate application globals or the input before `capture`.

### P6 — source-lemma audit

An independent audit of the exact acquired source/dependency bundle verifies
`L_compile`, `L_fresh`, `L_prepare`, and `L_deliver` with no alternate normal
path for this fixture.

### P7 — cell isolation

Each cell is one fresh process, and the emitted `observed_hex` is computed only
from the callable-entry mapping.

At present, P1 is false because the packages are absent; therefore the
conjunction `P` is not discharged. The conditional implication remains a
well-formed testable claim.

## Derivation of the conditional consequences

Assume `P`.

By `L_compile`, the task cells select exactly the same five coordinates. By
`L_fresh`, those coordinates are populated from the literal full state and
available before capture. By `L_prepare` and `L_deliver`, exactly that mapping
becomes the capture argument. P3-P5 exclude an additional pre-capture observer
or mutating context, and P7 prevents reuse.

The five selected values are identical in `S0,S1`; deterministic canonical
serialization of equal mappings is equal. Hence:

```text
C_task:
received(task_s0)=received(task_s1).
```

For full cells, the selected coordinates are those five plus
`provenance_record`. The records differ exactly at `agent_id`. Hence:

```text
C_full:
received(full_s0) and received(full_s1)
differ exactly at provenance_record.agent_id.
```

Thus `P -> C_task` and `P -> C_full`.

The future four cell executions may falsify this source derivation or expose a
manifest mismatch. They cannot prove determinism from repetition.

## Logical roles and failure semantics

- Failure of theorem typing or a finite countermodel falsifies Part I.
- Failure of target separation invalidates the witness.
- Failure of any `P` item means framework correspondence is unestablished; it
  does not falsify the abstract theorem.
- With `P` discharged, task-input inequality falsifies `C_task` and rejects the
  pinned task application.
- With `P` discharged, failure of provenance delivery falsifies only optional
  `C_full`.
- A cross-schema mismatch rejects the intended one-coordinate control but does
  not falsify the theorem.

No runtime result is converted into a security verdict, effect, population
claim, or proof of determinism.

## Assumptions and domains

| ID | Premise | Carries | Violation consequence |
|---|---|---|---|
| M1 | `pi,tau` are total functions | theorem | Partial/multivalued cases require a new formulation. |
| M2 | `Q=image(pi)` is the factor domain | uniqueness/canonicality | A larger domain adds unconstrained off-image extension values. |
| W1 | `J:P->B` and `J(p0)!=J(p1)` | witness | The task-side contradiction does not follow without separated targets. |
| W2 | `X cross P` contains both exact pairs | witness | Correlated real-state restrictions may remove the nonconstant fiber. |
| P1-P7 | exact conditional premise bundle | framework implication | Any failure keeps `C_task/C_full` unestablished. |

`P` is not disguised as an assumption of the mathematics. It is the explicit
antecedent of a separate implication.

## Rival explanations and controls

1. **Alias/derived provenance:** excluded only in the artificial witness by
   fixing equal task values; a real alias changes the actual projection.
2. **Mapper coercion:** `L_compile` predicts `None`, the fixture asserts it, and
   P6 audits exact dependency source.
3. **Unavailable channels:** `L_fresh` traces their writes; compiled/runtime
   assertions can falsify it after acquisition.
4. **Cached task input:** `_algo.py` constructs a fresh preparation cache; fresh
   processes independently prevent cross-cell reuse.
5. **Saved checkpoint/history:** explicit `None` checkpointer and fresh process;
   exact loop behavior remains part of P6.
6. **Callbacks/tracing:** `env -i`, `-I`, explicit empty callbacks, and P4-P5
   make this an audited antecedent rather than an assumed absence.
7. **Import hooks/site customization:** explicitly inspected under P4.
8. **Capture mutation:** capture serializes its argument before returning a
   write and receives only primitive-container data.
9. **Canonicalization ambiguity:** exact algorithm and actual stdlib JSON hash
   are fixed; future dependency identity is P1.
10. **Full positive-control failure:** affects `C_full`, not `C_task`.
11. **Researcher-chosen target:** conceded and scope-limiting.
12. **Classical theorem:** conceded; contribution is an engineering control
    protocol, not mathematical novelty.

## Bias surface

| Bias | Mitigation |
|---|---|
| Confirmation | Sterile review must seek theorem countermodels and challenge every source lemma and premise. |
| Selection | Two states are purpose-built and never represented as a population. |
| Measurement | Observable is callable-entry canonical bytes, never an action-authored verdict. |
| Leakage | Expected target is not an input to capture; schema/state equality is literal. |
| Implementation | Actual fixture/launcher files, modes, hashes, cells, and failure conditions are fixed. |
| Environment | Current dependency absence is explicit; acquired identity is P1, not a placeholder. |
| Analysis flexibility | Equality/difference relations and role-specific failures are fixed before any run. |
| Novelty/generalization | Classical and record-reconstruction-only boundaries are explicit. |

## Taxonomy, anti-stacking, and Occam

The taxonomy remains `Scope Mismatch × Formal Derivation × formalize`, with
`decouple` secondary. No distinct techniques are integrated into a new
synthesis.

Anti-stacking passes narrowly for the abstract result: one action test can show
one failure; the nonconstant-fiber proof excludes every total deterministic
function on the declared input. This quantifier is proved, not inferred from a
selected capture action. It says nothing about unmodeled inputs or general
security.

The mathematical subject is minimal: an image-domain factor and a two-state
nonconstant fiber. `C_full` is optional. Locale, timezone, and hash seed are
reproducibility hygiene in the launcher, not logical theorem premises. The
conditional premise bundle contains only identity/isolation facts needed to
connect an acquired implementation to the source trace.

## Deterministic pre-review checks

Without importing LangGraph:

1. parse the fixture with `ast.parse`;
2. check the launcher with `bash -n`;
3. recompute fixture, launcher, interpreter, and stdlib JSON hashes;
4. validate the normative JSON and `state.json`;
5. exhaustively enumerate the factorization theorem for `|S|=0..4`, three
   projection labels, two target labels, and all reachable-image actions;
6. recompute canonical witness bytes;
7. verify four cells, seven `P` items, two conditional claims, and explicit
   absent framework dependencies;
8. verify predecessors/reviews remain unchanged; and
9. scan for placeholders and prohibited execution/result claims.

These are static/document checks, not framework execution.

## Review gate

The sterile reviewer must return `RIGOROUS` only after:

1. independently deriving necessity, sufficiency, uniqueness, and boundary
   cases;
2. validating every witness type and the universal consequence;
3. independently checking the commit-bound source chain for all four lemmas;
4. checking that the actual fixture and launcher are statically closed;
5. confirming that P1-P7 are an explicit antecedent and are not represented as
   currently discharged;
6. checking `P -> C_task/C_full` without using runtime evidence;
7. confirming role-specific failure semantics, taxonomy, anti-stacking, Occam,
   and claim scope; and
8. finding no hidden framework execution, empirical, causal-effect, security,
   or novelty overclaim.

A rigorous verdict closes Phase 2 for the theorem and conditional implication
only. It does not discharge `P`, authorize acquisition, or establish LangGraph
runtime correspondence.

## Round-6 disposition table

| Round-6 requirement | v7 author claim before independent review |
|---|---|
| Complete engineering proof | **AUTHOR-RESOLVED AT CONDITIONAL LEVEL:** `L_compile`, `L_fresh`, `L_prepare`, `L_deliver`; exact environment facts are P antecedents. |
| Literal values and callback/import isolation | **AUTHOR-RESOLVED:** actual local hashes and explicit dependency absence; exact isolation requirements in P3-P5. |
| Closed fixture | **AUTHOR-RESOLVED:** four bound cells, exact launcher, compiled assertions, capture mechanism, and hashes. |
| JSON-container wording | **AUTHOR-RESOLVED:** objects/arrays with primitive leaves, including the empty array. |

These are author claims, not reviewer dispositions.

## Authorization boundary

The standing instruction authorizes this local revision, code-as-text, static
checks, source research, and sterile theory review within the remaining budget.
It does not authorize framework acquisition, installation, import, or
execution; Kaggle; held-out or locked-test action; live targets; operational
attacks; model APIs; external messages; or publication.
