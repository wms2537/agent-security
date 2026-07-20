# Cycle-2 orchestration-security evaluation contract

**Version:** c2-v4

**Recorded:** 2026-07-20

**Supersedes:** c2-v3 at commit `bdacc97`; c2-v1 through c2-v3 remain in
Git history.

**Status:** APPROVED UNDER STANDING INTERNAL-ITERATION DEFAULT — the user said
`go, dont ask me these questions again, go iterate and improve yourself` and
later directed continued autonomous improvement. This authorizes the local
review-driven correction below. It does not authorize any action listed under
the approval boundary.

**Active study:** OMST schema-security closure, a deterministic control within
Orchestration Metamorphic Security Testing.

## Adverse theory-gate decision

The c2-v3 empirical materiality claim is retired without execution. Its paired
contrast was definitionally forced by its own premises: the task-only schema
excluded `provenance_record`; side channels were forbidden; the action emitted
`null` when the record was absent; and P13/P15 required the non-null digest. On
every valid pair, the full condition therefore had to preserve P13/P15 and the
task-only condition had to violate them. Averaging that constructed pair over
120 graphs could not provide a valid empirical disconfirmation path.

This is a **theory-gate refutation** of the proposed frequency experiment, not
an experimental null and not evidence that orchestration rewrites are generally
safe or unsafe. No v3 validation or replay execution occurred.

The useful residue is narrower: a deterministic schema-closure proposition and
one future source-authentic regression fixture. The normative machine-readable
specification is `experiments/configs/omst-c2-v4-schema-closure.json`.

## Source-backed implementation boundary

Primary implementation: LangGraph tag `1.2.9`, object
`95af6a00718588e7b7ce17310e8006d267896a77`.

The proposition is connected to these official source surfaces:

- `StateGraph.add_node` selects or infers a node input schema;
- `CompiledStateGraph.attach_node` derives the compiled input channels from
  that schema and binds them to the compiled node;
- `prepare_single_task` obtains node input from the compiled process/channel
  set; and
- `ChannelRead.do_read` reads the selected channels and applies the schema
  mapper.

The source-supported operation is node input-schema projection, not generic
metadata reconstruction and not a framework security guarantee. A future
fixture is valid only if the pinned source and compiled channel audit implement
this exact operation without an adapter-authored projection.

## Deterministic proposition

Let:

- `s` be the immutable full pre-action state;
- `p=s["provenance_record"]` be present and non-null;
- `C` be the compiled input-channel set of the action node;
- `Pi_C(s)` be the exact projection of `s` onto `C`;
- `d(p)=SHA256(canonical_json(p))`;
- `f` be the identical declared action in both conditions; and
- `R_13_15` be the total three-valued predicate defined below.

Schema closure for this obligation is:

```text
closed(C) iff provenance_record is in C.
```

The primary claim is:

```text
Under A1-A7,
closed(C) iff
R_13_15(condition, s_bytes, events(f(Pi_C(s)))) = PRESERVE.
```

This is a necessary-and-sufficient claim over a declared finite semantic model,
not an estimated frequency and not a population claim.

## Conditions and only permitted difference

The future minimal fixture has two conditions:

1. `full`: `TaskStatePlusProvenance`, whose compiled channels are the ordered
   task keys plus `provenance_record`.
2. `task`: `TaskStateOnly`, whose compiled channels are exactly the task keys.

The compiled channel-set symmetric difference must be exactly
`{provenance_record}`. Full pre-state bytes, action source hash, task fields,
inert effect fixture, graph topology, environment, and every non-provenance
output must be identical. Any extra difference is `INVALID`, not evidence for
the proposition.

The action may obtain the record only from its projected input. Configuration,
store, checkpoint side reads, observers, globals, closures, filesystem,
environment, and network are forbidden provenance sources.

## Declared action

The source-identical deterministic action computes:

```text
if provenance_record is present in projected input:
    d_action = SHA256(canonical_json(provenance_record))
else:
    d_action = null
```

It emits exactly:

```text
seq=0, kind=BOUNDARY_EXIT,    record_digest=d_action
seq=1, kind=SENSITIVE_EFFECT, record_digest=d_action, effect_id="effect-0"
```

It also appends the same inert task effect under both conditions. There is no
runtime observer. The expected digest is computed offline from the immutable
pre-action fixture, so instrumentation does not manufacture the result.

## Total P13/P15 predicate

The complete signature is:

```text
R_13_15(condition, pre_state_bytes, ordered_event_bytes)
    -> PRESERVE | VIOLATE | INVALID
```

`condition` must be exactly `full` or `task`. `pre_state_bytes` must be canonical
JSON containing one non-null `provenance_record`. `ordered_event_bytes` must be
a canonical array with exactly the two events above, with array order equal to
integer `seq`, no extra fields, and no extra, duplicate, reordered, or trailing
events. The transition relation is:

```text
START -- BOUNDARY_EXIT(seq=0) --> EXIT_SEEN
EXIT_SEEN -- SENSITIVE_EFFECT(seq=1) --> COMPLETE
all other transitions --> INVALID
```

From the parsed immutable pre-state, the predicate computes
`d_expected=SHA256(canonical_json(provenance_record))` offline.

- P13 holds iff the boundary-exit digest equals `d_expected`.
- P15 holds iff the sensitive-effect digest equals `d_expected`.
- A schema-valid complete trace is `PRESERVE` iff P13 and P15 both hold;
  otherwise it is `VIOLATE`.
- Any context, serialization, field, or transition failure is `INVALID`.

Input class, source label, authorization, operation, and capability are outside
this narrowed P13/P15 proposition; they are neither hidden oracle inputs nor
claimed security properties here.

## Assumptions and validity domains

1. **A1 — exact projection:** the pinned implementation supplies the action
   exactly `Pi_C(s)`. A source or compiled-channel mismatch makes the fixture
   inapplicable.
2. **A2 — non-null obligation:** immutable `s` contains canonical non-null `p`.
   A missing or null record is outside the theorem domain.
3. **A3 — no side channel:** `f` can learn `p` only through its projected input.
   A side channel invalidates necessity.
4. **A4 — declared action:** the identical action follows the digest and event
   rules exactly. A different action invalidates sufficiency.
5. **A5 — offline reference:** the predicate receives immutable pre-state bytes
   and computes its expected digest without runtime observation.
6. **A6 — exact event language:** the trace contains exactly the declared two
   canonical events. Other traces are `INVALID`.
7. **A7 — deterministic representation:** canonicalization and SHA-256 are
   deterministic. The proof compares the same digest construction and does not
   rely on collision resistance.

These assumptions define the claim; premise failures may not be silently
dropped, imputed, or relabeled as security outcomes.

## Derivation

**Sufficiency.** If `closed(C)`, then `p` is in `Pi_C(s)` by A1-A2. By A4,
the action puts `d(p)` in both events. By A5, the predicate independently
computes the same `d(p)`. A6 yields a valid complete trace, so P13 and P15 hold
and the result is `PRESERVE`.

**Necessity.** If the result is `PRESERVE`, both event digests equal the non-null
offline `d(p)`. By A4, the action emits a non-null digest only when `p` is in its
projected input. By A3, no other source can supply `p`. By A1, `p` is in the
projection only when `provenance_record` is in `C`; therefore `closed(C)`.

One countermodel satisfying A1-A7 but falsifying either implication refutes the
proposition. A premise failure shows non-applicability, not confirmation or
disconfirmation. A failure of the future pinned fixture under apparently
satisfied assumptions triggers a correspondence audit; it cannot be averaged
away.

## Minimal regression fixture

Only after a RIGOROUS theory verdict may Phase 3 prepare one public non-target
fixture with the exact pre-state in the v4 JSON. Its checks are:

- source authenticity at the four pinned paths;
- exact compiled channel lists for both schemas;
- symmetric difference exactly `{provenance_record}`;
- identical pre-state bytes and action source hash;
- offline expected digest computed before either action;
- `full` emits that digest twice and returns `PRESERVE`;
- `task` emits `null` twice and returns `VIOLATE`; and
- non-provenance task/effect coordinates remain byte-identical.

This fixture is a regression/correspondence test with one replicate. It cannot
support prevalence, effect-size, robustness, generalization, or population
claims. A large OMST validation census is prohibited under c2-v4 because it
would restate a theorem by repetition.

## Theory-review success and failure metrics

The Phase-2 gate passes only if a sterile reviewer returns `RIGOROUS` after:

- independently re-deriving both implications;
- finding no countermodel under A1-A7;
- confirming that `R_13_15` is total and has no hidden semantic inputs;
- confirming that the observer and census have been removed;
- validating the pinned source-to-model correspondence as a falsifiable premise;
  and
- accepting the deterministic-verification taxonomy and narrow novelty claim.

Any unresolved hidden input, circular oracle, false source correspondence,
countermodel, observer dependence, or reintroduced empirical frequency claim is
`NEEDS_REVISION`. No PoC or implementation begins before `RIGOROUS`.

## Data and execution tiers

- **Phase 2:** specification, proof, static source references, deterministic
  document checks, and sterile theory review only.
- **Phase 3:** one minimal public non-target fixture only after the theory gate.
  Framework acquisition or installation remains separately unauthorized.
- **Phase 4:** no OMST census is justified under this contract.
- **Locked test:** absent, ungenerated, unexecuted, and unauthorized.

## Mutable and immutable paths

Git history preserves c2-v1 through c2-v3. For the c2-v4 theory decision, these
records are immutable once their commits are made:

```text
PROBLEM.md
research-log/053-literature-review-orchestration-security.md
research-log/054-decision-archaeology-orchestration-security.md
research-log/058-omst-theory-review-round1.md
research-log/062-omst-theory-review-round2.md
research-log/063-omst-source-authenticity-and-c2-v3-amendment.md
research-log/064-hypothesis-iter-5-omst-v3.md
research-log/066-omst-theory-review-round3.md
experiments/configs/environment-orchestration-c2.md
experiments/configs/data-governance-orchestration-c2.md
experiments/configs/omst-c2-v1.json
experiments/configs/omst-c2-v2.json
experiments/configs/omst-c2-v3.json
```

The c2-v4 contract, v4 JSON, retirement record, and superseding hypothesis
become immutable at their respective commits. Any later correction requires a
new version and an explicit adverse record; prior artifacts are never edited.

## Approval boundary

The standing default authorizes this local design correction, proof writing,
deterministic checking, and sterile review within the remaining review budget.
It does not authorize framework download or installation, PoC execution,
confirmatory execution, Kaggle, live targets, attack execution, model APIs,
external messages, publication, or locked-test generation/execution.
