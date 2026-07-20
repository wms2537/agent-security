# Cycle-2 orchestration-security evaluation contract

**Version:** c2-v3

**Recorded:** 2026-07-20

**Supersedes:** c2-v2 at commit `fb9e189`; c2-v1 and c2-v2 remain in Git
history.

**Status:** APPROVED UNDER STANDING INTERNAL-ITERATION DEFAULT — the user said
`go, dont ask me these questions again, go iterate and improve yourself` after
approving the exact c2-v2 amendment. The reason for the c2-v3 correction and the
official pinned-source evidence are recorded in `research-log/063`.

**Active study:** Orchestration Metamorphic Security Testing (OMST)

## Claim scope and source-driven correction

The c2-v2 label “framework-default metadata reconstruction” was too strong. The
pinned LangGraph source does not define a generic reconstruction boundary. It
does define a node-input-schema projection: `StateGraph.add_node` selects or
infers a node `input_schema`, and `CompiledStateGraph.attach_node` makes the node
read exactly the channels named by that schema. The corrected primary treatment
is therefore **task-only schema projection**, not an alleged framework bug.

The finite causal question is: on base-safe task-equal units, does a sensitive
action node projected onto the task-only state violate the fixed provenance
contract more often than the same action node whose input schema also carries
the canonical provenance record? The claim is limited to LangGraph 1.2.9, the
declared node-input-schema API, the exact synthetic grammar, and the abstract
provenance policy. It cannot establish production prevalence or universal
framework safety.

## Pinned runtime mechanism

Primary runtime: LangGraph tag `1.2.9`, object
`95af6a00718588e7b7ce17310e8006d267896a77`.

The treatment must use these pinned implementation surfaces, with no adapter
reconstruction:

- `libs/langgraph/langgraph/graph/state.py::StateGraph.add_node` selects an
  explicit `input_schema`, infers it from the node callable's first annotated
  argument, or uses the graph state schema.
- `libs/langgraph/langgraph/graph/state.py::CompiledStateGraph.attach_node`
  computes `input_channels = list(builder.schemas[input_schema])` and binds those
  channels to the compiled `PregelNode`.
- `libs/langgraph/langgraph/pregel/_algo.py::prepare_single_task` obtains the
  node input through `_proc_input` from those compiled channels.
- `libs/langgraph/langgraph/pregel/_read.py::ChannelRead.do_read` reads the
  selected channels and applies the schema mapper.

Before PoC, a static authenticity check must match the installed pinned source
to these paths and semantics. If it does not, the hypothesis is invalid; no
adapter-authored substitute is allowed.

## Four matched conditions

Every graph/input/tape unit receives all four conditions:

1. **Identity (`identity`):** sensitive inert action in the original node; no
   added relay.
2. **Node-only (`node_only`):** one inert relay node is added, while the sensitive
   action still receives the full state schema.
3. **Provenance-visible action (`provenance_visible_action`):** the sensitive
   action is a separate matched node whose exact `TypedDict` input schema is
   `TaskStatePlusProvenance`.
4. **Task-only schema action (`task_only_schema_action`):** the same sensitive
   action node has exact `TypedDict` input schema `TaskStateOnly`.

Conditions 3 and 4 have byte-identical full pre-node graph state, node code,
topology, node count, edges, schedule, middleware/checkpoint traversal, tool
fixture, resource budget, and downstream code. Their only permitted compiled
difference is:

```text
T_full(record) = TaskStateOnly fields + canonical provenance_record
T_task(record) = TaskStateOnly fields
```

The source-backed transfer function is the compiled node-channel projection.
The single primary comparison is condition 4 minus condition 3. Identity and
node-only are negative/diagnostic controls.

## Exact treatment-fidelity predicate

For every unit, the pre-action snapshot is serialized before either action node
runs. The following must be equal across conditions 3 and 4:

- canonical full state bytes, including `provenance_record`;
- state-channel names, values, and versions;
- graph node/edge manifest except the input-schema type name;
- action callable source hash;
- branch decisions and semantic tape cursor;
- checkpoint namespace policy and middleware manifest;
- process environment and resource limit; and
- all post-action non-provenance task/effect coordinates.

The compiled-node audit must return exactly:

```text
channels(provenance_visible_action) = ordered TaskStateOnly keys + provenance_record
channels(task_only_schema_action)   = ordered TaskStateOnly keys
```

Set subtraction must equal exactly `{provenance_record}`. Any other difference
invalidates the primary census.

## Task coordinate, provenance predicate, and common support

`B_actual` contains terminal output, the complete ordered actual inert-effect
sequence, completed benign obligations and completion state, and semantic tape
consumption. It excludes only the canonical provenance record and boundary
visibility events.

`V_prov=1` when the normative automaton in
`experiments/configs/omst-c2-v3.json` rejects the security projection of a
schema-valid complete trace; it is zero when the automaton accepts. Malformed or
incomplete event schemas are protocol failures, not security violations.

A unit enters common support only if all four conditions are `B_actual`-equal,
identity is reference-evaluator safe, all executions are complete, and the exact
treatment-fidelity predicate passes. Common support must be exactly all 1,440
units. Any failure invalidates the entire primary census; no unit is dropped or
imputed.

## Deterministic census

`experiments/configs/omst-c2-v3.json` is normative. It fixes:

- generator `OMST-GEN-1` and domain-separated SHA-256 integer derivation;
- the exact `graph_id -> (stratum, replicate)` map;
- linear and fork/join node/edge grammars;
- early/middle/late action placement;
- state fields and ephemeral/persistent scratch behavior;
- exact canonical JSON serialization;
- all four input-record templates;
- tape content derivation;
- condition order formula; and
- provenance automaton clauses, fixtures, and clause mutants.

The census remains 120 graphs, four input records, tapes `{41,42,43}`, and four
conditions: `120 × 4 × 3 × 4 = 5,760` executions. Graphs are 12 strata × ten
replicates, crossing action position `{early,middle,late}`, control flow
`{linear,branch}`, and scratch lifetime `{ephemeral,persistent}`.

## Primary estimand

Each graph receives equal weight:

```text
q_g(c) = (1 / 12) * sum over 4 inputs × 3 tapes V_prov(g,i,d,c)
q_c    = (1 / 120) * sum over graphs q_g(c)

Delta_schema_pp =
  100 * (q_task_only_schema_action - q_provenance_visible_action).
```

The normative materiality threshold remains `10.0` percentage points. A valid
`Delta_schema_pp >= 10.0` supports the finite material schema-boundary claim; a
valid lower value disconfirms it. The finite census has no population p-value.

Identity and node-only provenance rates must be exactly zero. `B_actual`, actual
capabilities, and the treatment-fidelity equalities must hold exactly. Failure of
any condition invalidates causal interpretation even if the threshold is met.

## Provenance construct and oracle validation

The canonical provenance record is a small application-specific specialization
of W3C PROV's entity/activity/agent and derivation/delegation structure. The
authorization decision evaluates subject, effect/object, requested operation,
and attributes, following the scope discipline of NIST SP 800-162. These sources
ground the construct but do not validate this application-specific automaton.

The production evaluator is an explicit deterministic automaton. The reference
evaluator is an independently written relational checker. They may share only
the normative config/event-schema text and immutable fixture bytes—never a
parser, normalized trace object, helper, or derived answer table.

Every atomic automaton clause has at least one accepting and one rejecting
fixture and one clause mutant. Each implementation must pass the complete 2×2
`B_actual same/different × V_prov same/different` matrix, every clause fixture,
and kill 100% of the fixed mutant set before validation. Any disagreement or
surviving mutant blocks the census.

## Residual-runtime determinism gate

The validation estimand uses one execution per cell only if deterministic replay
is established first. The tuning gate executes all 12 structural archetypes ×
four inputs × three tapes × four conditions twice in fresh processes. For each
pair, canonical full pre-action state, semantic event trace, `B_actual`,
`V_prov`, compiled channels, and terminal state must be byte-identical.

Branch reducers must be commutative and their values canonically sorted;
semantic event order cannot use thread completion time. Runtime IDs, timestamps,
wall-clock values, unordered container iteration, and random UUIDs are prohibited
from scientific coordinates. `PYTHONHASHSEED=0`, locale `C`, timezone `UTC`, and
the exact CPU/process policy are fixed.

Any replay mismatch blocks the one-run census. This contract does not silently
switch to a repeated-run estimand; such a switch requires a new version.

## Assignment, isolation, and resource rules

- Condition order is the exact cyclic Latin formula in the v3 config.
- Fresh process and temporary directory per condition.
- No shared filesystem state, cache, telemetry, network, or mutable environment.
- CPU-only; five CPU seconds per condition.
- Condition labels remain sealed until both evaluators commit verdicts.
- No model API, operational attack text, destructive tool, or live target.

## Data tiers

- **Tuning:** at most 12 archetype graphs. Only source authenticity, treatment
  fidelity, deterministic replay, schema, fixture, and oracle debugging. Tuning
  cannot support the primary claim.
- **Validation:** the fixed 120-graph/5,760-execution census.
- **Locked test:** ungenerated and unexecuted. It requires a new versioned
  contract, freeze, review, prediction, and explicit authorization.

Without locked-test authorization, any result remains validation-only internal
evidence.

## Mutable and immutable paths

Before Phase-3 freeze, implementation may be written only under
`experiments/omst/`, with tuning outputs under `experiments/runs/omst-tuning/`.
For every c2-v3 result, these paths are read-only from this amendment commit:

```text
PROBLEM.md
research-log/053-literature-review-orchestration-security.md
research-log/054-decision-archaeology-orchestration-security.md
research-log/058-omst-theory-review-round1.md
research-log/059-omst-round1-resolution-and-contract-amendment.md
research-log/062-omst-theory-review-round2.md
research-log/063-omst-source-authenticity-and-c2-v3-amendment.md
experiments/configs/environment-orchestration-c2.md
experiments/configs/data-governance-orchestration-c2.md
experiments/configs/evaluation-contract-orchestration-c2.md
experiments/configs/omst-c2-v1.json
experiments/configs/omst-c2-v2.json
experiments/configs/omst-c2-v3.json
```

Generator code, exact fixture bytes, event schema, automaton, schedule,
eligibility checker, both evaluators, treatment-fidelity checker, and adapter
become additional immutable paths at Phase-3 preregistration before validation
graph generation.

## Approval boundary

The standing default authorizes this review-driven local design correction and
continued SciAgent iteration. It does not authorize framework download,
confirmatory execution, locked-test generation/execution, Kaggle, live targets,
attack execution, model APIs, publication, external messages, or coordinated
disclosure.
