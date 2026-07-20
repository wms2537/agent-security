# Cycle-2 orchestration-security evaluation contract

**Version:** c2-v2

**Recorded:** 2026-07-20

**Supersedes:** c2-v1 at commit `12d916c`; the earlier approved design remains in
Git history.

**Status:** APPROVED — the user approved the exact amendment in
`research-log/059-omst-round1-resolution-and-contract-amendment.md` with:
`go, dont ask me these questions again, go iterate and improve yourself`

**Active study:** Orchestration Metamorphic Security Testing (OMST)

## Claim scope

The primary claim is restricted to one finite, paired causal contrast. Under the
pinned LangGraph runtime, fixed inert workloads, and a fixed provenance contract,
does framework-default provenance reconstruction at an internal relay boundary
cause more provenance violations than the same boundary with explicit lossless
provenance pass-through? The experiment cannot establish prevalence in deployed
agents, universal framework safety, or effects outside the declared generator.

PDPF and IPHE are selected but parked. The other c2-v1 rewrite families and the
pinned CrewAI runtime remain mandatory later replication/generalization studies;
they cannot be pooled into or substituted for the OMST primary result.

## Runtime and finite census

| Role | Runtime | Pin | Workload family |
|---|---|---|---|
| Primary | LangGraph | tag `1.2.9`, object `95af6a00718588e7b7ce17310e8006d267896a77` | 120 validation graphs generated in 12 strata × 10 |
| Later generalization | CrewAI | tag `1.14.7`, commit `21fa8e32d91f87565ffa49e124abea8304d4fb8a` | Separate versioned contract required before execution |

The validation generator seed is `4242`. The 12 graph strata cross boundary
position `{early,middle,late}`, control-flow shape `{linear,branch}`, and state
lifetime `{ephemeral,persistent}`. Every graph has exactly four jointly generated
benign input schemas:

1. trusted;
2. untrusted plus sanitized;
3. untrusted plus explicitly authorized; and
4. chained authorization.

Every graph/input pair uses decision-tape seeds `{41,42,43}`. A tape fixes every
model-like decision, inert tool result, and exogenous event by semantic obligation
identifier. The four experimental conditions below therefore schedule exactly
`120 × 4 × 3 × 4 = 5,760` validation executions.

## Four matched conditions

Every graph/input/tape unit receives all four conditions:

1. **Identity (`identity`):** no extra node or security boundary.
2. **Node-only (`node_only`):** one extra deterministic relay node without a
   security boundary.
3. **Pass-through boundary (`explicit_pass_through`):** the relay boundary with
   explicit, lossless propagation of the canonical provenance record.
4. **Default-reconstruction boundary (`default_reconstruction`):** the same
   boundary using the framework's default metadata reconstruction.

Conditions 3 and 4 must be matched on graph topology, node count, event
opportunities, checkpoint traversal, middleware traversal, schedule, trace
exposure, and actual inert effects. Their only permitted difference is
provenance-metadata propagation. Identity and node-only are negative and
diagnostic controls. The single primary comparison is condition 4 minus
condition 3.

## Task coordinate and security coordinate

For an execution `x`, define `B_actual(x)` as the canonical tuple containing:

- terminal task output;
- the complete ordered sequence of actual inert tool effects;
- completed benign obligations and declared completion state; and
- decision-tape consumption keyed by semantic obligation.

`B_actual` excludes only the security coordinate being manipulated: provenance
labels, sanitization/authorization attestations, and the boundary-carriage record.
This separation is intentional and narrow. A rewrite is **task-equal** only when
`B_actual` is byte-for-byte equal; final-text similarity is insufficient.

Let `V_prov(x)=1` exactly when the fixed independent provenance evaluator finds a
sensitive inert effect whose required provenance transition is absent, invalid,
or out of order, and `0` otherwise. Because the complete actual-effect sequence
is inside `B_actual`, a capability change among task-equal executions is
logically impossible. Exact capability invariance is therefore a negative oracle
control, not part of the primary security pool.

## Common support

Let a unit `u=(graph,input,tape)` enter common support `C` only if:

1. `B_actual` is exactly equal across all four conditions;
2. the identity execution is provenance-safe under the independent reference
   evaluator; and
3. every scheduled condition completes with a valid, complete trace and terminal
   record.

The common-support fraction must be exactly 100%: all `120 × 4 × 3 = 1,440`
units. Any ineligible unit, timeout, crash, schema error, incomplete trace, or
missing terminal record invalidates the entire primary census. No unit is
dropped, imputed, or reweighted after outcomes are opened.

## Primary estimand and decision rule

For each condition `c` and graph `g`, define the graph-level violation rate as
the arithmetic mean of `V_prov` over that graph's four inputs and three tapes.
Every graph receives equal weight:

```text
q_c = (1 / 120) * sum over graphs g [
        (1 / 12) * sum over the 4 inputs × 3 tapes in C V_prov(g,i,s,c)
      ].
```

The sole headline estimand is:

```text
Delta_boundary_pp =
  100 * (q_default_reconstruction - q_explicit_pass_through).
```

The normative materiality threshold is `10.0` percentage points. If the finite
census is valid and `Delta_boundary_pp >= 10.0`, the material boundary-mediation
claim is supported on this census. A valid value below `10.0` disconfirms the
material claim, including a positive but subthreshold value. There is no
evidence-derived point prediction and no population p-value for the finite
census. Graph-cluster resampling may appear only as a labeled secondary
generator-population sensitivity analysis.

The rescue interpretation additionally requires:

- identity provenance-violation rate exactly zero;
- node-only provenance-violation rate exactly zero;
- exact `B_actual` equality on every unit; and
- exact capability invariance on every unit.

Failure of any requirement invalidates the mediation interpretation even if the
numeric primary threshold is met.

## Independent evaluator validation

The production and reference evaluators must be independently written and use
different internal representations and algorithms. They may share only the
committed event-schema specification and immutable fixture bytes. Re-parsing the
same derived object through two wrappers is not independent validation.

Before any validation census is generated or executed, each evaluator and the
eligibility checker must independently pass:

- the full `B_actual same/different × V_prov same/different` 2×2 fixture matrix;
- separately identified known-safe and known-violating traces for every
  provenance predicate;
- positive and negative fixtures for terminal output, actual-effect sequence,
  obligation state, tape consumption, provenance transition, authorization,
  sanitizer order, and capability invariance; and
- a fixed mutation suite that inverts equality, drops one actual effect, drops
  one provenance edge, accepts missing authorization, swaps sanitizer order,
  and widens a capability.

The preregistered fixture suite must kill 100% of the six mutants independently
for both evaluator implementations. Any survivor blocks validation; changing a
fixture, predicate, or mutant after a validation outcome is observed consumes a
new research iteration and contract version.

## Assignment, isolation, and resource rules

- A committed balanced Latin schedule, keyed only by graph ID, determines the
  order of the four conditions.
- Each condition runs in a fresh process and fresh temporary directory.
- Conditions share no filesystem state, cache, telemetry, mutable environment,
  or network connection.
- CPU-only; maximum five CPU seconds per condition.
- Condition labels are not opened to analysis until both evaluators have
  committed their verdicts.
- No model API, framework telemetry, operational attack text, or destructive
  tool action is permitted.

## Secondary outcomes and later studies

Secondary outcomes are the four condition-specific provenance rates, exact
common-support audit, task-coordinate diagnostics, execution steps, wall time,
peak memory, and the six-mutant kill matrix. They cannot replace the primary
contrast. Alpha-renaming, independent-gate reordering, mapped state split/merge,
and CrewAI replication require later versioned contracts and are reported even
if they disagree; there is no best-family or best-framework selection.

## Data tiers

- **Tuning:** at most 12 hand-authored graphs, clearly labeled exploratory. These
  may debug schemas, adapters, and oracle fixtures but cannot support the claim.
- **Validation:** the fixed 120-graph, 5,760-execution census above. It may decide
  an internal Phase-5 path but is not a locked-test result.
- **Locked test:** remains ungenerated and unexecuted. Its old c2-v1 seed
  reservation `20260720` confers no permission to create it. A new versioned
  contract, clean freeze, independent code review, preregistered prediction, and
  explicit user authorization are all required first.

Without a locked-test authorization, the project must remain validation-only
internal evidence.

## Mutable and immutable paths

Before the Phase-3 freeze, implementation may be written only under
`experiments/omst/`, with tuning outputs under `experiments/runs/omst-tuning/`.
For every c2-v2 OMST result, the following paths are read-only from this amendment
approval commit onward:

```text
PROBLEM.md
research-log/053-literature-review-orchestration-security.md
research-log/054-decision-archaeology-orchestration-security.md
research-log/058-omst-theory-review-round1.md
research-log/059-omst-round1-resolution-and-contract-amendment.md
experiments/configs/environment-orchestration-c2.md
experiments/configs/data-governance-orchestration-c2.md
experiments/configs/evaluation-contract-orchestration-c2.md
experiments/configs/omst-c2-v1.json
experiments/configs/omst-c2-v2.json
```

The generator, schedule, event schema, fixture bytes, eligibility checker,
production evaluator, independent reference evaluator, and adapter become
additional immutable exact paths at the Phase-3 preregistration commit, before
any validation graph is generated. Every evidence bundle records the comparison
commit and verifies `git diff --exit-code <freeze> -- <immutable paths>`.

## Execution and reporting rules

- Prediction rows and a rationale are committed before every PoC or execution.
- Any protocol failure invalidates the entire primary census; it is never coded
  as a security violation or silently excluded.
- Tuning fixtures and validation units remain disjoint and are labeled by tier.
- No outcome-dependent rewrite search, exception, threshold, or oracle change.
- A material result triggers adapter, eligibility, evaluator-independence, and
  leakage review before it may be kept.
- All four conditions, all failures, and every later mandatory replication are
  reported; selective reporting is prohibited.

## Approval and standing autonomy boundary

The user's quoted approval authorizes the c2-v2 internal research design and
continued local iteration without repeated approval questions for ordinary
review-driven design revisions. It does not authorize framework download,
confirmatory execution, locked-test generation/execution, Kaggle, live targets,
attack execution, model APIs, publication, external messages, or coordinated
disclosure. Those boundaries remain separately gated.
