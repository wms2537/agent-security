# OMST pinned-source authenticity check and c2-v3 amendment

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** completed; c2-v3 design correction applied under standing default

## Trigger

Round-2 theory review accepted the v2 estimand, task/security separation,
taxonomy, assumptions, and anti-stacking logic but found four blockers. The most
important was treatment authenticity: v2 named “framework-default metadata
reconstruction” without identifying a real pinned runtime operation.

The user explicitly instructed: `go, dont ask me these questions again, go
iterate and improve yourself`. This record applies that standing default to a
local review-driven design correction. It does not expand the no-Kaggle,
no-live-target, no-external-action, no-model-API, no-framework-download, and
no-locked-test boundary.

## Official pinned-source inspection

The inspection used the official LangGraph repository at tag `1.2.9`; no clone,
package download, install, or execution occurred.

### What the source supports

1. [`StateGraph.add_node`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/graph/state.py)
   accepts an explicit `input_schema`, otherwise infers a schema from the node
   callable's first annotated parameter when present, otherwise uses the graph
   state schema.
2. In the same file,
   `CompiledStateGraph.attach_node` computes the node's input channel list from
   `builder.schemas[input_schema]` and binds those channels to the compiled
   `PregelNode`.
3. [`prepare_single_task`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_algo.py)
   creates task input via `_proc_input` from the compiled process/channel set.
4. [`ChannelRead.do_read`](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_read.py)
   reads the selected channels and applies the schema mapper.

This is an authentic framework projection mechanism: a node with a narrower
schema reads fewer state channels.

### What the source does not support

The inspected source does not define a generic “default metadata reconstruction”
boundary corresponding to the v2 prose. Keeping that name would let an adapter
invent the treatment and then attribute its behavior to LangGraph. That is the
exact easy-but-wrong path the user asked us to avoid.

## Corrective decision

The primary treatment is renamed and narrowed:

```text
v2: framework-default reconstruction vs explicit pass-through
v3: task-only node-input schema vs task-plus-provenance node-input schema
```

Both conditions use the same sensitive-action callable and full pre-node state.
The only compiled channel-set difference is `provenance_record`, verified by an
exact treatment-fidelity predicate. The claim is now about a schema-boundary
design choice on the pinned runtime, not an unspecified framework defect.

This correction may make the mechanism structurally simple. That is acceptable:
the study must report a source-implied or null result honestly and cannot inflate
it into a universal security finding. If Phase 3 shows the mechanism cannot be
exercised exactly through the pinned API, OMST stops or is downgraded; no adapter
substitute is permitted.

## Provenance construct grounding

The v3 automaton uses an application-specific record but anchors its vocabulary
to two authoritative sources:

- [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) treats provenance as records of
  entities, activities, agents, derivations, associations, and delegation, and
  emphasizes validity constraints on ordering and influence.
- [NIST SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final) defines
  authorization as evaluating subject, object, operation, and environment
  attributes against policy and relationships.

Neither source validates this exact automaton. The contract therefore calls it
an abstract application-specific provenance policy and requires clause-level
fixtures, independent implementations, and mutation adequacy.

## Resolution of the four round-2 blockers

| Blocker | c2-v3 response |
|---|---|
| Exact `V_prov` | Normative event schema, canonical record, 17 explicit automaton clauses, protocol-invalid separation, per-clause accepting/rejecting fixtures, and polarity-changing mutants fixed in `omst-c2-v3.json`. |
| Treatment fidelity | Exact pinned API paths, compiled channel-set equality, full pre-action state equality, same callable/graph/tape/checkpoint/middleware, and only `{provenance_record}` symmetric difference. |
| Deterministic census | `OMST-GEN-1`, SHA-256 derivation, graph-ID/stratum map, node/edge grammars, state fields, input templates, tape bytes, canonical JSON, and Latin order formula fixed. |
| Runtime randomness | A 1,152-execution tuning-only duplicate replay gate requires byte equality on all scientific coordinates; failure blocks validation and cannot silently change the estimand. |

## Gate and boundary

This is a material internal contract correction authorized by the recorded
standing default. Git preserves c2-v2. The new contract/config do not authorize
implementation, framework download, PoC, validation, locked-test action, attack
execution, Kaggle, model APIs, publication, or external messages.

## Next Step

Write a new immutable v3 hypothesis that supersedes v2, explicitly acknowledges
the source-driven treatment narrowing and the possibility that the effect is
structurally trivial, deterministically verify it, and dispatch a sterile review
only within the remaining user-authorized review budget.
