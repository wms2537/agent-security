# Hypothesis — iteration 5, OMST v4 schema-security closure

**Date:** 2026-07-20  
**Phase:** 2 — Hypothesis formation  
**Cycle:** 2  
**Status:** superseding theoretical hypothesis, not yet reviewed  
**Claim type:** theoretical / deterministic specification verification  
**Question type:** causal within the restricted sandbox in `PROBLEM.md`; this
subclaim establishes a deterministic intervention lemma and makes no empirical
frequency claim

## Supersession and adverse-result discipline

This artifact supersedes, but does not modify:

- v1: `research-log/056-hypothesis-iter-5-omst.md`;
- v2: `research-log/060-hypothesis-iter-5-omst-v2.md`; and
- v3: `research-log/064-hypothesis-iter-5-omst-v3.md`.

Their sterile adverse reviews remain verbatim in `research-log/058`,
`research-log/062`, and `research-log/066`.

Round 3 established that v3's proposed 120-graph frequency contrast was forced
by the intervention and oracle. That metric hypothesis is recorded as
`refuted` before any execution. The c2-v4 correction in `research-log/067`
removes the census rather than attempting to make a tautology look empirical.

The active search entry is now an understanding claim varying
`schema-security-closure`. It is the only active hypothesis. PDPF and IPHE
remain parked.

## One-sentence hypothesis

Under the pinned LangGraph node-input projection correspondence, an immutable
non-null pre-state record, no alternative provenance channel, and the declared
digest-carrying action, inclusion of `provenance_record` in the compiled action
channel set is necessary and sufficient for preserving the narrowed P13/P15
digest obligations under the total predicate `R_13_15`.

## What is and is not claimed

### Claimed

1. A formal biconditional in the semantic model defined below.
2. A falsifiable correspondence premise connecting LangGraph 1.2.9's declared
   input-schema machinery to the model's exact projection `Pi_C`.
3. A minimal regression-control form that a later Phase-3 fixture can check
   after the theory gate and applicable acquisition authorization.

### Not claimed

- that LangGraph promises to preserve fields omitted by an application schema;
- that task-only schemas are generally unsafe;
- that P13/P15 constitute a complete provenance or authorization policy;
- that a production vulnerability, exploit, attack, or prevalence estimate has
  been established;
- that graph topology, long horizons, multi-agent behavior, or runtime
  nondeterminism are being empirically mapped;
- that the previous 17-clause policy is validated;
- that one deterministic fixture generalizes beyond its pinned mechanism; or
- that Phase 3, framework download, an experiment, a locked test, or Kaggle has
  been authorized.

## Research questions

### Primary theoretical question

Does the biconditional

```text
closed(C) <=> R_13_15(k, s_bytes, E(f(Pi_C(s)))) = PRESERVE
```

follow from assumptions A1-A7 for every channel set `C` in the declared model?

### Secondary correspondence question

Does the pinned LangGraph 1.2.9 implementation actually supply the declared
action exactly the selected schema-channel projection, with the full/task
compiled channel symmetric difference exactly `{provenance_record}`?

The primary question is answered by proof or countermodel. The secondary
question is not answered by the proof: it requires later static source
verification and at most one minimal framework-bound regression fixture.

## Concrete meanings of all symbols

| Symbol | Concrete meaning |
|---|---|
| `K` | condition labels `{full,task}`; labels are validated routing metadata and do not determine the security verdict |
| `S` | finite mappings from ASCII state keys to canonical JSON values |
| `s in S` | one immutable full pre-action state mapping |
| `p` | the non-null value `s["provenance_record"]` |
| `C` | the exact compiled input-channel key set of the action node |
| `O` | the singleton security-obligation key set `{provenance_record}` |
| `closed(C)` | `O` is a subset of `C`; because `O` is singleton, exactly `provenance_record in C` |
| `Pi_C(s)` | the mapping containing exactly the keys in `C` and their values in `s`; keys outside `C` are absent |
| `J(x)` | the fixed canonical JSON byte serialization of value `x` |
| `H(b)` | lowercase hexadecimal SHA-256 of byte string `b` |
| `d(p)` | `H(J(p))`, a non-null 64-character lowercase hexadecimal string |
| `f` | the identical deterministic declared action applied to projected node input |
| `E(q)` | the exact ordered two-event sequence emitted when `f` receives projected input `q` |
| `R_13_15` | total three-valued verifier over condition, immutable pre-state bytes, and ordered event bytes |
| `PRESERVE` | both narrowed digest obligations hold on a valid complete trace |
| `VIOLATE` | at least one narrowed digest obligation fails on a valid complete trace |
| `INVALID` | the condition, pre-state, serialization, fields, or transition language is malformed/incomplete |

No probability space, sample, average, effect size, or asymptotic limit appears
in the primary claim.

## Normative representation

The machine-readable source of truth is
`experiments/configs/omst-c2-v4-schema-closure.json`. The prose below unpacks it
and may not broaden it.

### Canonical JSON

`J(x)` is UTF-8 output equivalent to:

```text
json.dumps(
    x,
    sort_keys=true,
    separators=(",", ":"),
    ensure_ascii=true,
    allow_nan=false,
)
```

Only integers, strings, booleans, null, lists, and string-keyed objects are in
domain. There is no trailing newline. Noncanonical, duplicate-key, non-finite,
or out-of-domain input is `INVALID` before a security decision.

### Schema sets

The full schema keys are:

```text
subject_id
task_value
effect_id
effect_log
completion
provenance_record
```

The task schema keys are the same list without `provenance_record`. Ordered
channel equality is an implementation-fidelity check. The theorem itself uses
only membership of `provenance_record`.

### Exact projection

For all `s` and `C` in domain:

```text
Pi_C(s) = { key: s[key] for each key in C }.
```

This definition requires every compiled key in `C` to exist in `s`; otherwise
the input is outside the theorem domain. A key not in `C` is absent. Projection
does not reconstruct it, inject `null`, consult a store, or perform a checkpoint
side read.

## Declared action and emitted events

### Action transfer rule

For projected input `q=Pi_C(s)`, the identical action computes:

```text
if "provenance_record" in q:
    d_action = H(J(q["provenance_record"]))
else:
    d_action = null
```

It emits exactly:

```text
{
  "seq": 0,
  "kind": "BOUNDARY_EXIT",
  "record_digest": d_action
}

{
  "seq": 1,
  "kind": "SENSITIVE_EFFECT",
  "record_digest": d_action,
  "effect_id": "effect-0"
}
```

The action also appends one identical inert effect to task state under both
conditions. The task update is a fidelity coordinate, not an input to P13/P15.

### Provenance-source exclusion

The action may receive the record only as the `provenance_record` member of its
projected input. These sources are forbidden:

- runtime observer or callback;
- configuration or runtime context;
- framework store;
- checkpoint side read;
- global variable or closure capture;
- filesystem, environment, network, cache, or telemetry; and
- schema-specific wrapper or alternate callable.

This exclusion is load-bearing for necessity and is tested as an explicit
premise, not assumed to hold in production systems generally.

## Total verifier `R_13_15`

### Signature and codomain

```text
R_13_15(k, s_bytes, event_bytes)
    -> {PRESERVE, VIOLATE, INVALID}
```

- `k` must be exactly `full` or `task`.
- `s_bytes` must decode and re-encode to exactly the canonical immutable
  pre-state bytes and contain one non-null `provenance_record`.
- `event_bytes` must decode and re-encode to exactly a canonical JSON array of
  two events.

The condition label is decision-inert: it routes fixture audit records but does
not supply a digest, expected verdict, schema set, or clause value. Therefore,
renaming a valid condition cannot change `PRESERVE` versus `VIOLATE`.

### Per-kind field table

| Kind | Exact `seq` | Required fields | Field constraints |
|---|---:|---|---|
| `BOUNDARY_EXIT` | 0 | `seq`, `kind`, `record_digest` | digest is null or exactly 64 lowercase hexadecimal characters |
| `SENSITIVE_EFFECT` | 1 | `seq`, `kind`, `record_digest`, `effect_id` | same digest domain; `effect_id` is a nonempty ASCII string |

Extra fields are forbidden. Array order must equal ascending `seq`. Duplicate,
missing, reordered, negative, noninteger, or trailing sequence entries are
`INVALID`.

### Transition relation

```text
START     -- BOUNDARY_EXIT(seq=0)     --> EXIT_SEEN
EXIT_SEEN -- SENSITIVE_EFFECT(seq=1)  --> COMPLETE
every other state/event pair          --> INVALID
```

The verifier accepts only if the automaton reaches `COMPLETE` with no remaining
events. Hash ordering, wall-clock ordering, thread completion, and event IDs are
absent.

### Offline expectation and decision

After validating `s_bytes`, the verifier computes:

```text
d_expected = H(J(s["provenance_record"]))
```

from the immutable bytes supplied to it. No runtime observer supplies an event
or digest.

- `P13` is true iff `BOUNDARY_EXIT.record_digest == d_expected`.
- `P15` is true iff `SENSITIVE_EFFECT.record_digest == d_expected`.
- return `PRESERVE` iff both are true;
- otherwise return `VIOLATE` after successful schema/transition validation;
- return `INVALID` for every input outside the declared language.

This decision is total over byte strings plus `k`: parsing or domain failures
map to `INVALID`, and every valid complete trace maps to exactly one of
`PRESERVE` or `VIOLATE`.

Input class, source label, authorization chain, operation, and capability set
are intentionally absent. The narrowed claim does not evaluate P04, P16, P17,
or the v3 whole-protocol policy, so those values are not hidden context.

## Assumptions and exact validity domains

| ID | Assumption | Validity domain | What failure means |
|---|---|---|---|
| A1 | The pinned implementation supplies the action exactly `Pi_C(s)` | LangGraph object `95af6a...`, the four named source surfaces, exact `TypedDict` schemas, and audited compiled channels | Source/model correspondence is false; theorem remains abstract and fixture is inapplicable |
| A2 | `s` is immutable across the pair and has one non-null canonical record `p` | Exact literal future fixture; byte equality before projection | Missing/null/different record is outside the theorem domain |
| A3 | The action can learn `p` only through its projected input | Sealed local non-network fixture; forbidden-source audit passes | Nonclosure may still preserve; necessity does not apply |
| A4 | The same deterministic action obeys the exact digest/event rule | One committed callable hash, exact two-event output, no schema wrapper | Closure may fail to preserve; sufficiency does not apply |
| A5 | Expected digest is computed offline from immutable `s_bytes` | Verifier called after fixture bytes are fixed; no runtime hook/callback event | An observer could define or perturb the measured outcome |
| A6 | Event sequence is exactly the two-event language | Canonical bytes and transition validator pass | Trace result is `INVALID`, not a security verdict |
| A7 | `J` and `H` are deterministic and identically specified | Exact canonicalization and SHA-256 implementation vectors | Digest equality is uninterpretable; stop |

Collision resistance is not an assumption. Both sides compute the same function
on the same `p`; the proof uses equality of construction. It also makes no claim
about an adversary finding collisions.

## Proposition

For every `s`, `C`, and valid condition label `k` satisfying A1-A7, define:

```text
q = Pi_C(s)
t = E(f(q))
r = R_13_15(k, J(s), J(t))
```

Then:

```text
closed(C) iff r = PRESERVE.
```

Equivalently, within the valid domain:

```text
not closed(C) iff r = VIOLATE.
```

`INVALID` is excluded from the equivalence only because A2/A6/A7 define valid
inputs. An implementation must report invalidity explicitly rather than omit a
case.

## Derivation from first principles

### Lemma 1 — projection membership

By the definition of `Pi_C`, for any key `x` in domain:

```text
x is present in Pi_C(s) iff x is in C.
```

For `x=provenance_record`, A2 ensures the value in `s` exists and is non-null.
No framework behavior beyond A1 is used in this semantic lemma.

### Lemma 2 — action digest equivalence

By A4 and the action rule:

```text
d_action = d(p) iff provenance_record is present in Pi_C(s).
```

The forward direction uses two facts: `d(p)` is non-null, and the action emits
`null` when the key is absent. The reverse direction uses A2 and exact
projection-value preservation: when present, the projected value equals `p`,
so the identical canonicalization/hash yields `d(p)`.

A3 prevents an unmodeled source from making the forward direction false.

### Lemma 3 — verifier preservation equivalence

By A5-A7, `d_expected=d(p)` and the trace is valid and complete. Both event
digests equal the single `d_action`. Therefore:

```text
R_13_15(...)=PRESERVE iff d_action=d(p).
```

If `d_action=null`, both clauses fail and the valid trace is `VIOLATE`. There is
no condition-dependent branch in the verifier.

### Sufficiency

Assume `closed(C)`. Because the obligation set is singleton,
`provenance_record in C`. Lemma 1 puts `p` in `Pi_C(s)`. Lemma 2 gives
`d_action=d(p)`. Lemma 3 gives `r=PRESERVE`. Thus closure is sufficient.

### Necessity

Assume `r=PRESERVE`. Lemma 3 gives `d_action=d(p)`, which is non-null. Lemma 2
implies `provenance_record` is present in `Pi_C(s)`. Lemma 1 implies
`provenance_record in C`, hence `closed(C)`. Thus closure is necessary.

### Biconditional

The two implications establish
`closed(C) iff r=PRESERVE`. No averaging, independence assumption, causal
effect estimator, statistical test, or runtime replicate is required.

## Countermodel attempts and load-bearing assumptions

These are not dismissed; each shows exactly why an assumption is required.

### Remove A3: side-channel countermodel

Let `provenance_record not in C`, but let `f` read `p` from a global. It emits
`d(p)`, and `R_13_15=PRESERVE` despite nonclosure. Necessity fails. Therefore
A3 is essential and the result cannot be generalized to actions with alternate
context channels.

### Remove A4: wrong-action countermodel

Let `provenance_record in C`, but let `f` always emit `null` or hash a different
object. The schema is closed while the verifier returns `VIOLATE`. Sufficiency
fails. Therefore schema closure alone cannot guarantee arbitrary action logic.

### Remove A2: null/missing-record countermodel

If `p` is absent or null, the offline expected digest is undefined under the
declared domain, or null can cease to distinguish absence from a value. The
theorem does not apply.

### Remove A5: observer-defined outcome

If a runtime observer manufactures `d_expected` or inserts a boundary event,
the trace can reflect instrumentation behavior instead of action projection.
The v3 design had this defect; v4 removes the observer.

### Remove A6: trace-language ambiguity

An extra post-completion event, duplicate effect, or reversed sequence could
require other security clauses. The narrowed verifier returns `INVALID` rather
than pretending P13/P15 form a complete protocol judgment.

### Source correspondence fails

If LangGraph's pinned compiled node supplies values beyond `C`, reconstructs
the record, or does not match the audited schema channels, A1 fails. This does
not falsify the abstract implication, but it falsifies applicability to the
pinned framework. No adapter substitute is allowed.

No countermodel above satisfies all A1-A7. Sterile review must actively search
for one that does.

## Pinned source correspondence

The current evidence is official source inspection, not a local framework run:

1. [`StateGraph.add_node`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/graph/state.py)
   selects an explicit input schema, may infer one from the callable annotation,
   or uses the graph state schema.
2. In the same official file, `CompiledStateGraph.attach_node` derives the input
   channels from `builder.schemas[input_schema]` and binds them to the compiled
   node.
3. [`prepare_single_task`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_algo.py)
   prepares node input from the compiled process/channel set.
4. [`ChannelRead.do_read`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_read.py)
   reads selected channels and applies the schema mapper.

These surfaces motivate A1 but do not prove the future fixture satisfies it.
The Phase-3 correspondence check must audit exact installed source identity,
compiled channel lists, and received node-input bytes. If any differ, the
LangGraph application claim stops.

## Minimal future regression fixture

The exact literal pre-state is fixed in the v4 JSON. It contains five task keys
and this non-null record:

```json
{
  "entity_id": "entity-0",
  "activity_id": "activity-0",
  "agent_id": "agent-0"
}
```

After a RIGOROUS theory verdict and applicable Phase-3 gate, at most one
source-authentic fixture may check:

| Check | Required result |
|---|---|
| Full compiled channels | exact task list plus `provenance_record` |
| Task compiled channels | exact task list only |
| Set symmetric difference | exactly `{provenance_record}` |
| Full pre-state bytes | identical across both conditions |
| Action source hash | identical across both conditions |
| Full emitted digests | two copies of offline `d(p)` |
| Task emitted digests | two `null` values |
| Verifier results | `full=PRESERVE`, `task=VIOLATE` |
| Non-provenance coordinates | byte-identical |

One replicate is sufficient for correspondence because the result is
deterministic and derived. A repeat may diagnose nondeterminism but cannot turn
the control into an empirical sample. A 120-graph census is forbidden.

## Success, disconfirmation, invalidity, and stopping

### Phase-2 theoretical success

A sterile reviewer returns `RIGOROUS` only after independently re-deriving both
implications, validating totality, finding no countermodel under A1-A7, and
accepting the source correspondence as a separate falsifiable premise.

### Theoretical disconfirmation

Any one of these disconfirms the proposition or its claimed derivation:

1. a countermodel satisfying A1-A7 with `closed(C)` and `r!=PRESERVE`;
2. a countermodel satisfying A1-A7 with `not closed(C)` and `r=PRESERVE`;
3. a byte-string input for which the claimed total verifier has no unique output;
4. a hidden semantic input needed by P13/P15; or
5. circular use of the condition/schema label to assign the expected verdict.

### Correspondence disconfirmation

The pinned framework application is rejected if authenticated LangGraph 1.2.9
does not produce the declared channel projection or exact channel difference.
That result cannot be repaired by an adapter.

### Invalidity

A failed premise, malformed trace, altered action, different pre-state, extra
channel difference, or source-identity mismatch is reported explicitly. It is
not averaged, dropped, or called a security violation.

### Stop rule

If review is RIGOROUS, proceed only to the one-fixture Phase-3 correspondence
decision when separately permitted. OMST ends after that result. If review is
adverse, revise the proof only if the issue is substantive and within remaining
budget; do not restore the empirical census. If the theorem is judged merely
definitional with no useful control contribution, report that limitation and
advance to the separately parked PDPF direction rather than inflate OMST.

## Variables and controls

### Independent coordinate

Membership of the singleton security-obligation key
`provenance_record` in compiled channel set `C`.

### Dependent coordinate

The result of `R_13_15`, restricted to valid traces, and the two constituent
equalities P13/P15.

### Held fixed

Full state `s`, non-null record `p`, canonicalization `J`, hash `H`, action `f`,
action source bytes, event grammar, inert task effect, predicate code/spec,
framework object, graph topology, and all non-provenance task coordinates.

The condition label is held as audit metadata and cannot influence the verifier
decision.

## Evidence chain and novelty scope

### Closest framework evidence

The official pinned LangGraph source establishes the candidate projection
mechanism. It does not call schema omission a security bug and does not state
this theorem. The application remains conditional on exact correspondence.

### Closest evaluation priors

[ReliabilityBench](https://arxiv.org/abs/2601.06112) uses metamorphic relations
to evaluate agent reliability, and [ASSURE](https://arxiv.org/abs/2507.05307)
separates behavioral and security dimensions in agent evaluation. They motivate
checking invariants beyond terminal task success. They do not supply this
pinned one-channel projection lemma, its total P13/P15 predicate, or the
source-correspondence stop rule.

The broader Cycle-2 synthesis—including *Towards Long-Horizon Agents*, MASEval,
FlowSteer, LoopTrap, MaMa, AHE, and Agent-BOM—is relevant to the parent problem
but does not turn this deterministic control into a long-horizon result.

### Provenance vocabulary

[W3C PROV-DM](https://www.w3.org/TR/prov-dm/) motivates representing provenance
records around entities, activities, and agents. [NIST SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final)
motivates external policy context. Neither source validates P13/P15; those are
declared application-specific digest obligations.

### Narrow novelty claim

The possible contribution is a reproducible **schema-security closure control**:
state the exact security-obligation key set, prove closure equivalence for a
declared action/oracle, and separately test whether a pinned orchestration
framework implements the assumed projection. The novelty is the disciplined
separation of logical result, implementation correspondence, and empirical
prevalence—not the elementary set-membership proof by itself.

If prior work already gives the same pinned relation, total predicate, and
correspondence control, novelty fails and the result should be reported as a
replication/control.

## Idea taxonomy

- **Opportunity pattern:** Scope Mismatch.
- **Method paradigm:** Formal Derivation, followed only by deterministic
  specification testing for correspondence.
- **Dominant operation:** `formalize`.
- **Secondary operation:** `decouple` the logical obligation from runtime
  instrumentation and from prevalence claims.

This is not Evidence Gap × Empirical Mapping: no empirical map remains. It is
not Bridge × Synthesis: no techniques are integrated into a new stack. The
local move takes one source-backed projection operation and makes its security
closure assumptions explicit.

## Anti-stacking check

There is one mechanism, one obligation key, one action rule, and one verifier.
The claim does not combine multiple defenses or call their composition novel.
Removing any element does not yield a weaker stack; it changes or destroys the
defined implication. The future fixture is a correspondence test, not a
component ensemble.

The distinguishing prediction relative to a plain task-only schema check is:
a schema may be sufficient for the declared task tuple while failing closure
over an independently declared security-obligation key. A terminal-task checker
alone makes no P13/P15 prediction because those digests are excluded from its
coordinate.

## Occam's Razor check

The simplest hypothesis that predicts the outcome is the biconditional above.
That is now the active hypothesis. The v3 graph grammar, four input classes,
three tapes, 17 clauses, replay gate, 120 graphs, and 5,760 executions are
removed because they cannot change the result under A1-A7.

One static proof plus one later source-authentic fixture is sufficient. More
graphs, frameworks, events, provenance clauses, or controls would broaden the
question and require separate hypotheses.

## Alternative explanations and separation checks

| Rival explanation | How it could mimic the result | Separation or consequence |
|---|---|---|
| Oracle assigns verdict from condition label | `task` could be hard-coded to fail | Label is decision-inert; permuting it cannot change digest equalities |
| Runtime observer creates expected digest | Instrumentation could manufacture mismatch | Observer removed; expectation is offline from immutable bytes |
| Different action wrappers | Wrapper, not schema, could change digest | One callable hash and no schema-specific wrapper |
| Adapter-authored projection | Test harness could omit the record itself | Exact pinned compiled-channel and received-input audit; no substitute |
| Different pre-states | Missing record could be a starting-state confound | Canonical pre-state byte equality |
| Extra channel difference | Another omitted field could cause behavior | Symmetric difference must be exactly the singleton key |
| Task effect differs | Result could reflect different benign work | Non-provenance output bytes must match exactly |
| Hash collision/security claim | Digest outcome could be framed cryptographically | Proof needs deterministic equality only; no collision-resistance claim |
| Whole-policy validity | Passing P13/P15 could be mistaken for full security | Result names only P13/P15 and other traces/clauses remain outside scope |
| Repetition as evidence | Many forced pairs could look statistically strong | Census prohibited; one fixture has no population inference |
| Developer error framed as framework bug | Explicitly omitting a field is application design | Claim is closure/correspondence, not a framework vulnerability |
| Source changed or install mismatched | Different runtime may not implement A1 | Exact tag/object/source audit; mismatch rejects applicability |

## Formal-validity threat surface

| Threat | Operation here | Control |
|---|---|---|
| Circular definition | Oracle might use closure or condition to decide | Oracle reads only immutable record and event digests; condition is decision-inert |
| Hidden premise | Action could access record elsewhere | Exhaustive forbidden-source assumption A3 and future audit |
| Partial predicate | Malformed bytes could lack an outcome | Three-valued total codomain with canonical/transition invalidity |
| Symbol overloading | `state`, `schema`, or `preserve` could float | Concrete meaning table and singleton obligation domain |
| Source/model mismatch | Abstract `Pi_C` may not be LangGraph behavior | A1 is a separately falsifiable correspondence premise |
| Construct overreach | Two digest clauses could be called provenance security | Claim and result restricted to P13/P15 |
| Proof by experiment | Expected fixture could substitute for derivation | Both implications written before implementation; review re-derives them |
| Selective applicability | Failed premises could be omitted | Every failure is `INVALID`/inapplicable and stops correspondence claim |

## Round-3 issue resolution

| Required issue | v4 response | Claimed status before re-review |
|---|---|---|
| Empirical contrast is forced and unfalsifiable | Metric outcome recorded `refuted`; frequency claim, effect size, threshold, census, and validation path removed | RESOLVED BY RETIREMENT |
| Predicate lacks complete inputs/order | Active scope narrowed to P13/P15; exact signature, canonical bytes, per-kind fields, integer `seq`, transition relation, and three-valued total output | RESOLVED |
| Observer is underdefined/outcome-defining | Runtime observer removed; expected digest derived offline from immutable pre-state bytes | RESOLVED |
| Generator is not byte-complete | Generator and census removed; one exact literal future fixture only | RESOLVED BY REMOVAL |
| Taxonomy is not empirical mapping | Reclassified as Scope Mismatch × Formal Derivation × `formalize` | RESOLVED |
| Large design violates Occam | One theorem and one correspondence fixture replace the large design | RESOLVED |

These are author claims only. Sterile round-4 review must re-grade every row and
check for new defects.

## Reviewer-specific derivation challenges

The reviewer should not accept the proof by inspection. It should attempt:

1. to construct a model satisfying A1-A7 where closure holds but preservation
   fails;
2. to construct one satisfying A1-A7 where nonclosure preserves;
3. to find a valid byte input with no unique verifier output;
4. to show a required P13/P15 input is hidden outside the signature;
5. to identify circular use of `k`, schema identity, or expected verdict;
6. to test whether any assumption already contains the conclusion;
7. to distinguish theorem truth from LangGraph correspondence;
8. to check whether the contribution is too trivial to justify even a control;
   and
9. to verify that the empirical census is truly absent rather than renamed.

## Phase and authorization gates

Before Phase 3:

1. this exact artifact must be committed and mechanically checked;
2. the hypothesis-review budget is charged at sterile dispatch;
3. the reviewer must return `RIGOROUS` with an independent re-derivation and
   strongest-objection analysis; and
4. any adverse verdict is logged verbatim before another revision.

Even after RIGOROUS, the standing direction does not authorize framework
download/install or fixture execution. Those remain separate applicable gates.
No Kaggle action, operational attack, live target, model API, external message,
publication, or locked-test generation/execution is authorized.

## Expected outcome before review

The proof predicts the biconditional holds exactly in the semantic model. That
prediction has high logical confidence because the action and verifier make the
same record-membership distinction. Confidence in the LangGraph correspondence
is lower until a pinned fixture audits the compiled channels and received input.

If review concludes the result is correct but elementary, the appropriate
scientific outcome is a narrow deterministic control, not an empirical paper
claim. If review finds the assumptions circular or the verifier non-total, the
hypothesis is revised or abandoned. Favorability is not a stopping criterion.
