# Hypothesis — iteration 5, OMST v5 projection-fiber factorization

**Date:** 2026-07-20  
**Phase:** 2 — Hypothesis formation  
**Cycle:** 2  
**Status:** superseding theoretical hypothesis, not yet reviewed  
**Claim type:** theoretical, with a separately falsifiable implementation
correspondence corollary  
**Question type:** causal within the restricted sandbox in `PROBLEM.md`; the
active subclaim is a deterministic structural criterion and makes no empirical
effect or prevalence claim

## Supersession and adverse-result record

This artifact supersedes but does not edit:

- v1: `research-log/056-hypothesis-iter-5-omst.md`;
- v2: `research-log/060-hypothesis-iter-5-omst-v2.md`;
- v3: `research-log/064-hypothesis-iter-5-omst-v3.md`; and
- v4: `research-log/068-hypothesis-iter-5-omst-v4-schema-closure.md`.

The adverse reviews are preserved verbatim in `research-log/058`,
`research-log/062`, `research-log/066`, and `research-log/070`.

v3's empirical metric is recorded `refuted` without execution. v4 correctly
retired that census but replaced it with a co-designed identity: a particular
action mapped key presence into a scalar, and a particular checker mapped that
same scalar into a verdict. Round 4 showed that this was correct but not a
distinguishing scientific prediction, and that its assumption analysis
contained formal errors.

The c2-v5 correction in `research-log/071` concedes those defects and replaces
the constructed identity with a projection-fiber factorization theorem. The
active search dimension remains `schema-security-closure`, kind
`understanding`. PDPF and IPHE remain parked.

## One-sentence hypothesis

A deterministic action can satisfy a full-state security obligation using only
an orchestration node's projected input for every state exactly when the
obligation is constant on every fiber of that projection; consequently, if two
task-identical states project to the same task-only node input but require
different provenance outputs, every deterministic task-projected action fails
on at least one of them.

## Claim boundary

### Claimed

1. A necessary-and-sufficient factorization criterion over total functions.
2. A two-state restricted provenance corollary that quantifies over **every**
   deterministic action on the task projection, not one experiment-authored
   action.
3. A semantic definition of schema-security closure as a functional dependency
   of the obligation on the actual delivered input.
4. A separately falsifiable correspondence proposition for the pinned
   LangGraph 1.2.9 normal PULL-input path.

### Not claimed

- a new theorem in information-flow theory, dependency theory, set theory, or
  category theory;
- an empirical effect, prevalence estimate, security benchmark, or framework
  vulnerability;
- that literal inclusion of `provenance_record` is universally necessary;
- that provenance bytes alone define complete security;
- that randomized, stateful, history-dependent, or externally contextual
  actions are covered unless that information is represented in the actual
  action input/state;
- that a compiled channel list by itself equals the callable's received input;
- that the future correspondence fixture proves the theorem;
- that LangGraph has been downloaded, installed, or run; or
- any Kaggle, locked-test, live-target, attack, model-API, publication, or
  external-message action.

## Research questions

### Primary theorem question

For total `pi:S->Q` with reachable codomain `Q=pi(S)` and total
`tau:S->Y`, is the following equivalence true?

```text
there exists a total deterministic g:Q->Y satisfying
tau(s)=g(pi(s)) for every s in S

if and only if

tau is constant on every fiber of pi.
```

### Restricted provenance question

When two full states share the exact task coordinate but contain different
canonical provenance records, can any deterministic action that receives only
the shared task projection output the correct record-dependent target for both?

### Separate framework-correspondence question

Does pinned LangGraph 1.2.9 actually deliver identical task-only callable-input
mappings and distinct task-plus-provenance mappings for the exact two witness
states, through its normal PULL path?

The proof answers the first two questions. It cannot answer the third.

## Formal objects and concrete meanings

| Symbol | Concrete meaning |
|---|---|
| `S` | declared full-state domain |
| `s,s'` | full states in `S` |
| `pi` | all information actually delivered to the deterministic action, represented as a total function |
| `Q` | reachable action-input set `pi(S)`, not a larger hypothetical codomain |
| `q` | one reachable action input |
| `Y` | exact target-output domain |
| `tau` | full-state security-obligation target, a total function `S->Y` |
| `g` | any total deterministic action `Q->Y` |
| `s ~_pi s'` | observational equivalence at the action input: `pi(s)=pi(s')` |
| `F_q` | projection fiber `{s in S : pi(s)=q}` |
| `closed(pi,tau)` | `tau` has one value on every fiber of `pi` |
| `tau=g∘pi` | for every `s`, the action output on projected input equals the required full-state target |
| `X` | exact task-coordinate domain in the restricted corollary |
| `P` | exact provenance-record domain in the restricted corollary |
| `J(p)` | canonical JSON bytes of provenance record `p` |

No event trace, condition label, hash, sentinel, security verdict, probability,
sample, average, threshold, or effect size appears in the theorem.

## Normative artifact

The machine-readable specification is
`experiments/configs/omst-c2-v5-factorization.json`. The current c2-v5 contract
is `experiments/configs/evaluation-contract-orchestration-c2.md`. This artifact
unpacks them without broadening their claims.

## Definitions

### Reachable projection

`pi:S->Q` is total and `Q` is defined to be exactly `pi(S)`. Hence every
`q in Q` has at least one full-state representative.

For an orchestration node, `pi` includes all information the action can actually
read: delivered schema fields, mapper output, bound defaults/closures/globals,
configuration, store, runtime context, prior local state, or other accessible
coordinates. Calling an accessible coordinate a “side channel” does not make it
disappear from the mathematical input.

### Projection fibers

For each reachable input `q`:

```text
F_q = {s in S : pi(s)=q}.
```

States in one fiber are indistinguishable to a deterministic action whose entire
input is `q`.

### Security closure

`pi` is security-closed for `tau` iff:

```text
for all s,s' in S,
pi(s)=pi(s') implies tau(s)=tau(s').
```

Equivalently, `tau` is constant on each `F_q`. This is a functional dependency:

```text
pi -> tau.
```

It is semantic. It does not mean that a particular field name must literally
appear. A derived coordinate can suffice if it determines the same target; a
listed but unavailable or mapper-dropped field may fail.

### Universal correctness

A deterministic action `g:Q->Y` is universally correct on `S` iff:

```text
for all s in S, g(pi(s))=tau(s).
```

This is exact correctness on the declared state domain, not probabilistic
accuracy or observed success on a sample.

## Factorization theorem

### Statement

For the declared total functions:

```text
exists total deterministic g:Q->Y with tau=g∘pi
iff
closed(pi,tau).
```

### Necessity proof

Assume some total deterministic `g:Q->Y` satisfies `tau=g∘pi`.

Take arbitrary `s,s' in S` with `pi(s)=pi(s')`. Then:

```text
tau(s)
= g(pi(s))             because tau=g∘pi
= g(pi(s'))            because pi(s)=pi(s')
= tau(s')              because tau=g∘pi.
```

Thus every pair in the same projection fiber has the same `tau`; therefore
`closed(pi,tau)`.

Only functionality/determinism and the equality premise are used. No choice of
action implementation, missing-value behavior, or verifier appears.

### Sufficiency proof

Assume `closed(pi,tau)`.

For each `q in Q`, define `g(q)` to be the unique `y in Y` satisfying:

```text
there exists s in S such that pi(s)=q and tau(s)=y.
```

Existence: `q in Q=pi(S)`, so at least one representative `s` exists and
`y=tau(s)` exists because `tau` is total.

Uniqueness: if representatives `s,s'` both map to `q`, closure gives
`tau(s)=tau(s')`. Hence there is exactly one such `y`, so `g` is well-defined
without selecting a privileged representative.

Totality: the definition supplies one `g(q)` for every `q in Q`.

Correctness: for arbitrary `s in S`, let `q=pi(s)`. The unique defining value at
`q` is `tau(s)`, so `g(pi(s))=tau(s)`. Therefore `tau=g∘pi`.

### Biconditional

Necessity and sufficiency prove the factorization criterion.

The c2-v5 domain additionally restricts `S` to finite and nonempty because the
project uses a finite explicit witness. The proof above does not rely on
finiteness after `Q=pi(S)` and totality are established; this is a scope
restriction, not a claimed load-bearing mathematical premise.

## How the theorem can fail outside its domain

### Partial target or projection

If `tau` or `pi` is partial, `tau=g∘pi` may lack a truth value on some states.
Explicit error/bottom semantics are required; c2-v5 does not silently totalize
them.

### Larger codomain than reachable image

If `Q` contains unreachable values, fiber constancy does not define `g` there.
An arbitrary extension could be chosen, but c2-v5 avoids that irrelevant choice
by defining `Q=pi(S)`.

### Randomized or history-dependent action

A randomized or stateful action is not a function `Q->Y` unless randomness and
history are incorporated into the actual input/state. Such systems require a
distributional or transition-system theorem and are outside this claim.

### Incomplete actual input model

If the action reads globals, closure variables, configuration, a store, or
runtime context not represented by `pi`, the chosen `pi` is not its actual input.
The theorem remains true, but the implementation correspondence is false.

## Restricted two-state provenance corollary

### Exact domain

Let `X={x}` contain the one literal task tuple in the v5 JSON. Let
`P={p0,p1}`, where:

```json
p0 = {
  "entity_id": "entity-0",
  "activity_id": "activity-0",
  "agent_id": "agent-0"
}

p1 = {
  "entity_id": "entity-0",
  "activity_id": "activity-0",
  "agent_id": "agent-1"
}
```

Let `S=X×P` and:

```text
tau(x,p)=J(p).
```

The canonical bytes differ because the parsed objects differ at the ASCII
string value of `agent_id`, canonical serialization preserves that value, and
canonical serialization is injective over these two exact parsed values by
direct byte comparison. No cryptographic assumption is involved.

### Task projection impossibility

Define:

```text
pi_task(x,p)=x.
```

Then:

```text
pi_task(x,p0)=x=pi_task(x,p1),
but
tau(x,p0)=J(p0) != J(p1)=tau(x,p1).
```

Therefore `tau` is not constant on this task-projection fiber. By the necessity
direction, no deterministic `g_task:X->Y` can satisfy `tau=g_task∘pi_task` on
both states.

The contradiction can also be seen directly. Universal correctness would
require the single value `g_task(x)` to equal both distinct byte strings
`J(p0)` and `J(p1)`, which is impossible.

Thus:

```text
for every deterministic task-projected action,
at least one of s0 or s1 receives the wrong provenance target.
```

This universal quantifier is the distinguishing prediction absent from v4's
single constructed action.

### Full projection construction

Define:

```text
pi_full(x,p)=(x,p)
g_full(x,p)=J(p).
```

Each full-projection fiber fixes `p`, so `tau` is constant on it, and the
constructive `g_full` satisfies `tau=g_full∘pi_full` on all of `S`.

### Exact necessary-and-sufficient instance result

For this independent-product two-state domain:

```text
task projection: not closed; no universally correct deterministic action exists
full projection: closed; a universally correct deterministic action exists.
```

This does not imply that literal provenance-key inclusion is necessary on every
application state space. If another delivered coordinate determines `J(p)`, the
semantic closure test may pass without the literal key.

## Minimal abstract assumptions

| ID | Premise | Exact regime | Failure consequence |
|---|---|---|---|
| T1 | `S` is finite and nonempty | exact c2-v5 witness/application domain | scope restriction; theorem can generalize, but c2-v5 does not claim/test that extension |
| T2 | `pi` and `tau` are total | every state in declared `S` has one projected input and one required target | partiality needs explicit bottom/error semantics |
| T3 | `Q=pi(S)` | action domain is the reachable image only | larger `Q` needs an arbitrary extension outside observations |
| T4 | `g` ranges over total deterministic functions `Q->Y` | no hidden state, randomness, history, or unmodeled context | different action class; universal impossibility claim does not directly apply |

T1 is not used by either algebraic implication; it bounds the active research
instance. T2-T4 carry the theorem's type and behavior domain. No assumption
contains fiber constancy or the existence of `g`.

## Theorem falsifiability

The theorem is falsified by one concrete countermodel specifying finite
nonempty `S`, total `pi`, total `tau`, reachable `Q`, and deterministic total
actions such that exactly one of these is true:

1. `closed(pi,tau)`; or
2. there exists `g` with `tau=g∘pi`.

The restricted corollary is falsified by showing any of:

- `J(p0)=J(p1)` for the exact literal records;
- `pi_task(s0)!=pi_task(s1)` under its definition;
- a deterministic single-valued `g_task(x)` equal to both distinct targets; or
- `g_full(x,p)=J(p)` fails the stated equality on either exact state.

Framework source mismatch does not falsify the abstract theorem. It rejects the
LangGraph application.

## Pinned LangGraph correspondence proposition

### Official source evidence

The source candidate is LangGraph tag `1.2.9`, object
`95af6a00718588e7b7ce17310e8006d267896a77`.

1. [`StateGraph.add_node` and `CompiledStateGraph.attach_node`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/graph/state.py)
   select the node input schema and bind its compiled channels/mapper.
2. [`PregelNode`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_read.py)
   defines list-valued `channels` as a dictionary input to the bound node and
   identifies `mapper` as an input transformation.
3. The PULL branch of
   [`prepare_single_task`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_algo.py)
   obtains `val` through `_proc_input` and stores it as
   `PregelExecutableTask.input` for the node.

`ChannelRead.do_read` is not treated as the normal PULL-input constructor.

### Correspondence claim

For exact `TaskStateOnly` and `TaskStatePlusProvenance` TypedDict schemas and the
two literal full states:

```text
actual_received_task(s0)=actual_received_task(s1)=x

actual_received_full(s0) != actual_received_full(s1),
and provenance_record is their only value difference.
```

### Mandatory future audit

A future fixture, only after applicable gates, must verify:

| Coordinate | Required evidence |
|---|---|
| Source identity | exact tag/object and authenticated relevant file hashes |
| Compiled channels | exact ordered `proc.channels` for both schemas |
| Availability | every selected witness channel is available before `_proc_input` |
| Mapper | exact mapper identity/hash and input/output bytes |
| Task construction | normal PULL `prepare_single_task -> _proc_input -> PregelExecutableTask.input` path |
| Callable input | canonical mapping recorded at bound-callable entry |
| Pair relation | task inputs identical; full inputs differ only at provenance record |
| Bound environment | code, defaults, closures, globals, config, store, environment, runtime context equal/sealed |
| Capture noninterference | records the argument only; cannot inject input, output, target, event, or verdict |

Compiled channel membership alone is not enough: `_proc_input` can omit
unavailable channels, and the mapper can transform the read values.

Any mismatch rejects correspondence. No adapter substitute, inferred security
verdict, or favorable-case exclusion is permitted.

## Minimal future fixture and stopping rule

After a RIGOROUS theory verdict and separately applicable framework acquisition
gate, at most one two-state, two-schema public non-target fixture may record the
actual callable inputs.

It has no action-generated provenance target and no security checker. Its only
result is whether the two actual input relations above hold. The factorization
theorem supplies the impossibility conclusion if correspondence holds.

One replicate is a source/model correspondence check. If nondeterministic input
construction appears, correspondence fails or the model must change; repeats
cannot become a prevalence study. There is no Phase-4 OMST census.

If correspondence holds, report a narrow schema-closure control. If it fails,
reject the LangGraph application and report why. Either way, OMST stops and the
portfolio can move to PDPF. An adverse theory verdict may close OMST before any
fixture. v3/v4 may not be restored.

## Evidence and novelty boundary

### Information-flow foundations

[Goguen and Meseguer's noninterference framework](https://doi.org/10.1109/SP.1982.10014)
separates a security policy from the system model and asks whether one domain
can affect another's observations.

[Sabelfeld and Myers' information-flow survey](https://www.cs.cornell.edu/andru/papers/jsac/sm-jsac03.pdf)
uses observational equivalence as a core security lens: states equal at an
observable level should not acquire distinguishable observable behavior due to
hidden inputs. c2-v5 applies this established structure to a node's schema
projection and an external obligation target.

### Evaluation motivation only

[ReliabilityBench](https://arxiv.org/abs/2601.06112) and
[ASSURE](https://arxiv.org/abs/2507.05307) motivate checking more than terminal
task success. They do not establish this theorem's novelty and are not used as
theoretical foundations.

### Honest novelty claim

The factorization theorem is classical and elementary. The candidate local
contribution is:

1. define orchestration schema-security closure semantically as
   `pi_C -> tau` rather than literal key inclusion;
2. separate universal impossibility from a co-designed action test; and
3. specify a pinned source-to-callable-input correspondence audit.

If those application choices already appear together in prior work, novelty
fails and the artifact remains only an engineering/theoretical control. No
top-tier novelty claim is made at Phase 2.

## Idea taxonomy

- **Opportunity pattern:** Scope Mismatch.
- **Method paradigm:** Formal Derivation.
- **Dominant operation:** `formalize`.
- **Secondary operation:** `decouple` theorem truth, obligation semantics, and
  runtime correspondence.

This is not Bridge × Synthesis: there is no defense stack or integration of
several methods. It is not Empirical Mapping: no frequency or effect is
estimated.

## Anti-stacking check

The active result has one projection, one obligation, and a universal quantifier
over candidate deterministic actions. It does not assemble components into a
system and call the assembly novel.

A plain composition of one chosen projection, one chosen action, and one chosen
checker can predict that **that action** passes or fails. It does not establish:

```text
if tau varies within a projection fiber,
every deterministic action on that projected input fails somewhere in the fiber.
```

That universal impossibility follows from the fiber structure. Conversely,
testing many actions is unnecessary once the theorem premises hold. This is the
distinguishing prediction v4 lacked.

## Occam's Razor check

The theorem contains only:

- one state domain;
- one projection;
- one obligation target;
- one class of deterministic actions; and
- one equality/fiber criterion.

SHA-256, null sentinels, two duplicate events, P13/P15, an automaton, condition
labels, graph grammars, tapes, inputs, replay gates, and a census are absent.

The two-state provenance instance is the smallest counterexample to fiber
constancy: one state cannot show target variation inside a fiber. The full
projection construction is the simplest sufficiency witness.

## Alternative explanations and scope checks

| Alternative | Could it explain the abstract theorem? | Control/consequence |
|---|---|---|
| Co-designed missing-value branch | No action implementation appears in necessity | v4 mechanism removed |
| Checker assigns expected verdict | No verdict/checker exists | theorem compares functions directly |
| Literal field alias | Can make a schema closed without the named key | semantic dependency definition permits it |
| Global/store/config context | Can distinguish states that task fields cannot | must be included in actual `pi`; otherwise correspondence is false |
| Randomness/history | Can change the action class | outside T4; requires a separate theorem |
| Partial/unavailable channel | Can break assumed projection | direct `_proc_input`/availability/callable-input audit |
| Mapper transformation | Can remove or encode information | mapper output is part of actual `pi` and is audited |
| Capture instrumentation | Can alter delivered input | noninterference/sealed-environment gate; failure rejects fixture |
| Source-version mismatch | Can make the LangGraph path false | exact object/file identity; no adapter substitute |
| Classical theorem | Means mathematical novelty is absent | conceded; contribution limited to application/control |
| Two-state cherry-pick | Could overstate general runtime prevalence | no prevalence claim; pair is an exact counterexample domain |
| Correlated application state | Could let task fields determine provenance | then task projection may be semantically closed; theorem handles this rather than forcing key inclusion |

## Round-4 issue resolution

| Required issue | v5 response | Claimed status before re-review |
|---|---|---|
| Separate/eliminate A3 and A4 | Removed from abstract theorem; accessible context belongs to actual `pi`, implementation sealing moves to correspondence | RESOLVED |
| Concede definition or add prediction beyond plain composition | v4 identity conceded; universal impossibility over every deterministic action derived from nonconstant fibers | RESOLVED |
| Use minimal theorem or justify P13/P15 duplicates | One projection, one target, one action class; events/clauses removed | RESOLVED |
| Repair `E`/`f` type | Both removed; well-typed factorization is `tau=g∘pi` | RESOLVED BY REMOVAL |
| Correct null-record claim | Null restriction/sentinel removed; any canonical `p` is allowed | RESOLVED BY REMOVAL |
| Complete correspondence path | Normal PULL path, availability, mapper, actual callable input and bound environment fixed as mandatory checks | RESOLVED IN SPECIFICATION |
| State projection domain formally | `pi` total and `Q=pi(S)` in definitions/theorem | RESOLVED |

These are author claims. Round-5 review must re-grade all seven and find new
defects.

## Reviewer challenges

The sterile reviewer should:

1. independently prove or refute both factorization directions;
2. check existence, uniqueness, and totality of the sufficiency construction;
3. search for a finite countermodel under T1-T4;
4. determine whether T1 is harmless scope or misleading mathematical padding;
5. verify the two-state task impossibility and full construction;
6. test whether semantic closure correctly handles aliases/derived inputs;
7. judge whether the universal quantifier genuinely resolves anti-stacking;
8. verify that no constructed security verdict or empirical census remains;
9. assess the exact `_proc_input` correspondence requirements; and
10. decide whether the explicitly classical result is substantive enough even
    as an orchestration-security control.

## Phase and authorization gates

Before Phase 3:

1. this artifact must be committed and deterministically checked;
2. the review budget is charged at sterile dispatch;
3. a reviewer must return `RIGOROUS` with an independent proof and strongest
   objection; and
4. any adverse report must be logged verbatim before revision or closure.

Even after RIGOROUS, framework download/install and fixture execution remain
separately gated. No Kaggle action, live target, attack execution, model API,
external message, publication, or locked-test generation/execution is
authorized.

## Expected outcome before review

The factorization theorem and restricted corollary are expected to hold exactly.
Logical confidence is high because the theorem is a standard fiber-constancy
criterion. The meaningful uncertainty is not the algebra; it is whether the
orchestration application and correspondence protocol are sufficiently
substantive and accurately pinned.

If review finds the theorem correct but the application too elementary, OMST
will be retained only as a control and closed. That is a valid scientific
outcome. The project will not add complexity merely to manufacture novelty.
