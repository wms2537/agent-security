# OMST empirical retirement and c2-v4 schema-closure amendment

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** empirical frequency claim refuted at theory gate; deterministic
schema-closure control activated under the standing internal-iteration default

## Decision

The c2-v3 hypothesis proposed a 120-graph, 5,760-execution census of the
violation-rate difference between a task-only action schema and the same action
schema with `provenance_record`. No execution occurred. Round-3 theory review
showed that the contrast had no valid empirical disconfirmation path under its
own premises.

The metric hypothesis is therefore recorded as **refuted** and retired. It will
not be repaired by writing a more elaborate generator or running a larger
sample. That would make a constructed identity look empirical without adding
information.

The narrow, source-backed residue is retained as a new understanding hypothesis:

> Under the pinned schema-projection implementation, immutable non-null
> pre-state, no provenance side channel, and the declared digest-carrying
> action, schema closure over `provenance_record` is necessary and sufficient
> for preserving the narrowed P13/P15 provenance obligations.

The amended normative artifacts are:

- `experiments/configs/evaluation-contract-orchestration-c2.md` (c2-v4); and
- `experiments/configs/omst-c2-v4-schema-closure.json`.

Git history preserves c2-v3 and its immutable hypothesis/review.

## Why the empirical claim is refuted

For every execution that satisfied c2-v3's declared treatment and validity
premises:

1. the task-only schema omitted `provenance_record`;
2. the action had no permitted alternative source for that record;
3. the action emitted `null` when the record was absent;
4. the full schema supplied the record and the action emitted its digest;
5. P13 and P15 required equality to that non-null digest; and
6. premise or fidelity failures were invalid rather than legitimate outcomes.

Consequently, every valid pair was forced to
`(Y_full,Y_task)=(0,1)`. The nominal 100-percentage-point result was a theorem
of the construction. Graph position, branching, scratch lifetime, input class,
and tape could not change it without breaking a premise. The proposed average
over those coordinates was mathematically redundant.

This refutes the proposed **empirical frequency interpretation**. It does not
refute the schema-projection mechanism, establish production prevalence, or
show a framework vulnerability. The correct output is a deterministic control
with explicit validity domains.

## c2-v4 correction

### Removed

- the 120-graph and 5,760-execution materiality census;
- `Delta_schema_pp` and the 10-point success threshold;
- empirical-mapping taxonomy for this active subclaim;
- the 17-clause whole-protocol automaton as the active oracle;
- the underdefined runtime observer;
- graph, input, tape, replay, and large-generator coordinates that cannot alter
  the result under the theorem assumptions; and
- any possibility of treating repeated deterministic witnesses as prevalence.

The v3 automaton and generator remain immutable research history, not active
requirements.

### Added

- one formal necessary-and-sufficient schema-closure proposition;
- assumptions A1-A7 with explicit premise-failure domains;
- exact `Pi_C(s)` projection semantics and closure definition;
- a total three-valued predicate
  `R_13_15(condition,pre_state_bytes,ordered_event_bytes)`;
- per-kind field tables and an integer-sequence transition relation;
- offline expected-digest computation from immutable pre-state bytes;
- separate sufficiency and necessity derivations;
- a countermodel-based falsifier; and
- one future source-authentic regression fixture, permitted only after a
  RIGOROUS theory verdict and applicable Phase-3 gate.

## Round-3 blocker disposition

| Round-3 blocker | c2-v4 disposition |
|---|---|
| Empirical contrast is definitionally forced | **RESOLVED BY RETIREMENT:** the frequency claim, census, effect size, and threshold are removed; the search-log outcome is `refuted`. |
| `V_prov` is not a total executable predicate | **RESOLVED BY NARROWING:** only P13/P15 remain active; all required context is in the exact predicate signature, pre-state bytes, and two canonical sequenced events. Missing/extra/reordered inputs return `INVALID`. |
| Observer is outcome-defining and underpinned | **RESOLVED BY REMOVAL:** expected digest is computed offline from immutable pre-action fixture bytes; no runtime observer exists. |
| Census generator is not byte-complete | **RESOLVED BY REMOVAL:** no census or generator is part of the active claim; one exact literal fixture is specified. |

## Source correspondence and scope

The treatment remains grounded in the official LangGraph 1.2.9 source surfaces
identified in `research-log/063`: input-schema selection in
`StateGraph.add_node`, compiled channel selection in
`CompiledStateGraph.attach_node`, task-input preparation in
`prepare_single_task`, and selected-channel reads in `ChannelRead.do_read`.

That source evidence supports a projection mechanism only. The new theorem also
requires a future compiled-channel correspondence check. If the pinned
implementation does not supply exactly the declared projection, the fixture is
inapplicable and the source-correspondence premise fails. No adapter may be used
to synthesize the expected behavior.

## Falsifiability and stopping rule

The proposition is refuted by one countermodel satisfying A1-A7 in which schema
closure and P13/P15 preservation are not equivalent. The implementation
correspondence is rejected if the future pinned compiled channels or node input
do not match `Pi_C(s)`. A malformed fixture or failed assumption is
`INVALID`/inapplicable and cannot be counted in either direction.

If sterile review returns RIGOROUS, Phase 3 may prepare exactly one minimal
public non-target correspondence fixture under the separate framework-acquisition
boundary. Whether it matches or fails, OMST stops after that deterministic
control. There is no c2-v4 path to a large validation census.

## Taxonomy and contribution claim

The active idea is now:

```text
Scope Mismatch × Formal Derivation × formalize
```

It is a specification/control result: task-facing schema closure does not imply
closure over an external security obligation unless the obligation's field is
included. The contribution is the explicit theorem, total checker semantics,
source-correspondence premise, and regression-control form. It is not an
empirical mapping, benchmark result, production prevalence estimate, general
LangGraph security claim, or defense stack.

## Authorization boundary

The user's standing direction authorizes this rigorous local correction and a
new sterile review within the remaining hypothesis-review budget. It does not
authorize framework download/install, PoC or experiment execution, Kaggle,
live targets, operational attacks, model APIs, external messages, publication,
or locked-test generation/execution.
