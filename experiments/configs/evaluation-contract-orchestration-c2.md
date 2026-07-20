# Cycle-2 orchestration-security evaluation contract

**Version:** c2-v5

**Recorded:** 2026-07-20

**Supersedes:** c2-v4 at commit `aaf609e`; c2-v1 through c2-v4 remain in Git
history.

**Status:** APPROVED UNDER STANDING INTERNAL-ITERATION DEFAULT — the user
directed autonomous iteration and improvement. This authorizes the local
review-driven formal correction below but none of the external or executable
actions listed at the end.

**Active study:** OMST projection-fiber security closure.

## Adverse-gate decision

c2-v4 correctly retired the invalid empirical frequency claim. Its replacement
biconditional was also mathematically true, but round-4 review showed that it
was a constructed identity: a declared action mapped record presence to
`digest/null`, and a declared checker mapped the same scalar to a verdict.
The theorem added no prediction beyond direct composition and its assumption
analysis contained a type error and an invalid countermodel.

c2-v5 supersedes that constructed result without execution. It does not restore
an event automaton, empirical effect size, graph census, runtime observer, or
security verdict. The normative machine-readable artifact is
`experiments/configs/omst-c2-v5-factorization.json`; the rationale and source
check are in `research-log/071`.

## Abstract model

Let:

- `S` be a finite nonempty set of full states;
- `pi:S->Q` be a total projection, where `Q=pi(S)` is its reachable image;
- `tau:S->Y` be a total security-obligation target; and
- `g:Q->Y` be any total deterministic action that receives only the projected
  input.

The projection-fiber relation is:

```text
s ~_pi s' iff pi(s)=pi(s').
```

The projection is **security-closed for `tau`** iff:

```text
for every s,s' in S,
pi(s)=pi(s') implies tau(s)=tau(s').
```

Equivalently, `tau` functionally depends on `pi` and is constant on every
projection fiber.

## Factorization theorem

The active theoretical hypothesis is:

```text
There exists a total deterministic g:Q->Y such that
tau(s)=g(pi(s)) for every s in S
if and only if
pi is security-closed for tau.
```

### Necessity

Assume `tau=g composed_with pi`. For any `s,s'` with `pi(s)=pi(s')`:

```text
tau(s)  = g(pi(s))
        = g(pi(s'))
        = tau(s').
```

Thus `tau` is constant on each fiber.

### Sufficiency

Assume fiber constancy. For every reachable `q in Q`, choose any state `s_q`
with `pi(s_q)=q` and define:

```text
g(q)=tau(s_q).
```

Because all representatives in the fiber have the same `tau`, `g` is
well-defined. Because `Q` is exactly the reachable image, the definition is
total. For every `s`, `s` and the selected representative for `pi(s)` share a
fiber, hence `g(pi(s))=tau(s)`.

The result is a standard factorization/noninterference structure. No new
mathematical theorem is claimed.

## Schema interpretation

For an orchestration schema with actually delivered coordinate set `C`,
`pi_C(s)` is the exact mapping received by the bound callable after channel
availability and schema mapping. The schema is security-closed only if:

```text
pi_C(s)=pi_C(s') implies tau(s)=tau(s').
```

This semantic definition replaces c2-v4's syntactic key-membership rule.
Literal inclusion of `provenance_record` may be sufficient, but it is not
generally necessary: another delivered coordinate could determine the same
target. Conversely, listing a channel is insufficient if the channel is
unavailable or the mapper drops/transforms it.

Any global, closure, store, configuration, or runtime context that the action
can read is part of the **actual** projection. It cannot be called an unmodeled
side channel while preserving a task-only projection claim.

## Restricted provenance corollary

The exact witness uses:

```text
S = X × P
P = {p0,p1}
tau(x,p) = canonical_json(p)
```

`X` is the singleton task tuple and `p0,p1` are the literal records in the v5
JSON. They differ only in `agent_id`, so their canonical bytes differ.

The two projections are:

```text
pi_task(x,p)=x
pi_full(x,p)=(x,p).
```

For task projection, `(x,p0)` and `(x,p1)` occupy the same fiber but have
different `tau`. The factorization theorem therefore implies:

```text
for every deterministic g_task:X->Y,
g_task cannot equal tau on both witness states.
```

This is the distinguishing universal impossibility prediction. It does not
depend on a particular missing-value branch, sentinel, digest, event trace, or
verifier.

For full projection, every fiber fixes `p`; `tau` is constant on fibers and the
constructive action `g_full(x,p)=canonical_json(p)` is universally correct.

## Assumptions and domains

| ID | Abstract premise | Domain/failure consequence |
|---|---|---|
| T1 | `S` is finite and nonempty | Used to select a representative without additional choice machinery; the finite fixture is the only intended instance |
| T2 | `pi` and `tau` are total on `S` | Partiality requires a different theorem with explicit error semantics |
| T3 | `Q=pi(S)` | Ensures every `q` has a representative and constructed `g` is total on its stated domain |
| T4 | Candidate actions are deterministic total functions `Q->Y` | Randomized, partial, stateful, or externally contextual actions require their randomness/history/context inside the actual input or a different result |

The abstract theorem has no LangGraph, action purity, event, hash, non-null,
instrumentation, or source-code assumption.

## Pinned framework correspondence

The LangGraph application is a separate, unverified corollary. Primary runtime:
tag `1.2.9`, object `95af6a00718588e7b7ce17310e8006d267896a77`.

The future source-to-input audit must follow the normal PULL path:

1. `StateGraph.add_node` input-schema selection;
2. `CompiledStateGraph.attach_node` compiled channel and mapper binding;
3. `PregelNode.channels` and `PregelNode.mapper`;
4. `prepare_single_task` PULL-task construction;
5. `_proc_input` channel-availability filtering, reads, and mapper application;
6. `PregelExecutableTask.input`; and
7. the exact canonical mapping received at bound-callable entry.

`ChannelRead.do_read` is not used as a substitute for the normal PULL-input
path.

The audit must establish:

- authenticated object/file hashes;
- exact `proc.channels` for both schemas;
- availability of every selected witness channel;
- exact mapper identity and output;
- actual received mapping, not merely a compiled list;
- task mapping equality across `s0,s1`;
- full mappings differing only in `provenance_record`;
- equal callable code, defaults, closures, globals, configuration, store,
  environment, and runtime context; and
- capture code that records input but cannot inject state, expected output,
  events, or a verdict.

Any mismatch rejects applicability to LangGraph. No adapter may synthesize the
expected projection.

## Minimal future correspondence fixture

Only after a RIGOROUS theory verdict and applicable Phase-3 acquisition gate may
one public non-target fixture use the exact two states and two schemas in the v5
JSON.

It records only the bound callable's input mapping:

```text
received_task(s0) = received_task(s1) = shared_task

received_full(s0) != received_full(s1),
with provenance_record as the only difference.
```

There is no security verdict, event trace, digest, P13/P15 checker, effect-size
estimate, or population inference. One replicate is a correspondence check;
repetition cannot become empirical evidence for the theorem.

## Theory-review success and failure

The Phase-2 gate passes only if a sterile reviewer returns `RIGOROUS` after:

- independently proving necessity and sufficiency;
- checking that `g` is well-defined and total on reachable `Q`;
- finding no finite countermodel under T1-T4;
- validating the task/full restricted corollary;
- confirming the universal impossibility is not predicted by one specific
  co-designed action test;
- accepting the semantic rather than syntactic closure definition;
- separating abstract theorem truth from LangGraph correspondence; and
- accepting the explicitly classical novelty boundary.

The gate fails on a countermodel, hidden premise, partial projection/target,
ill-typed composition, circular framework premise, overclaimed novelty, or
reintroduced empirical interpretation.

If RIGOROUS, proceed only to the separate correspondence decision when
authorized. If adverse, OMST may be closed as a useful but elementary control
and the portfolio may advance to PDPF; v3/v4 cannot be resurrected.

## Data and execution tiers

- **Phase 2:** proof, primary-source inspection, deterministic document checks,
  and sterile theory review only.
- **Phase 3:** at most one two-state input-correspondence fixture, after all
  applicable gates.
- **Phase 4:** no OMST effect-size, prevalence, robustness, or validation census.
- **Locked test:** absent, ungenerated, unexecuted, and unauthorized.

## Immutable history

Git history preserves c2-v1 through c2-v4, v1 through v4 hypotheses, and all
adverse reviews. Once committed, the c2-v5 contract, JSON, amendment record, and
superseding hypothesis are immutable; another correction requires c2-v6.

## Approval boundary

The standing default authorizes this local formal correction, deterministic
checking, and sterile theory review within the remaining budget. It does not
authorize framework download/install, fixture or experiment execution, Kaggle,
live targets, operational attacks, model APIs, external messages, publication,
or locked-test generation/execution.
