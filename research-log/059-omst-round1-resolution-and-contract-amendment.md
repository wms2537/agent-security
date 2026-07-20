# OMST round-1 resolution and proposed contract amendment

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5
**Status:** approved and applied as c2-v2

## Why the checkpoint was required

The user approved `experiments/configs/evaluation-contract-orchestration-c2.md`
with `ok`. That immutable contract defines a pooled four-rewrite primary
comparison. The round-1 theory reviewer found that this comparison mixes
base-safety prevalence with susceptibility, compares rewrite-specific eligible
sets, and bundles several mechanisms. Fixing those defects changes the primary
estimand and intervention. It therefore requires explicit user approval; it
cannot be disguised as a clarification.

The original hypothesis v1 and adverse review remain unchanged and committed.
Git history preserves c2-v1. The approved successor contract is c2-v2; no second
review round is charged until a superseding hypothesis is written and dispatched.

## Review findings mapped to resolutions

| Required issue | Proposed resolution |
|---|---|
| 1. Estimand and weighting | Condition on base-safe, exact-task-equal common support. Give every graph equal weight, with exactly four inputs and three tapes per graph. Identity becomes a validity gate, not a prevalence-adjustment term. |
| 2. `B`/security overlap | `B_actual` includes all actual inert effects, terminal output, obligations, and tape consumption. Capability differences are therefore impossible among eligible pairs and become a negative control. The primary `V_prov` reads provenance/authorization metadata deliberately omitted from the benign task view. |
| 3. Mechanism causality | Replace the omnibus primary with a matched relay-boundary mediation contrast: same boundary, node count, trace length, checkpoint traversal, and middleware traversal; only explicit metadata pass-through versus framework-default reconstruction differs. |
| 4. Oracle validation | Require separate 2×2 fixtures and positive/negative controls for the eligibility checker and every security predicate, two implementations using different internal representations, and 100% kill of a fixed mutation set before validation. |
| 5. Evidence/taxonomy | Add ReliabilityBench and ASSURE as strongest priors. Classify the contribution as Scope Mismatch × Empirical Mapping × `decouple`: both test action/system relations, but neither isolates internal graph-boundary metadata propagation on common support. |
| 6. Census specification | Pin exact versions already recorded; seed 4242; 120 graphs in 12 strata × 10; four inputs; tapes 41/42/43; fresh process and temporary state per condition; network/telemetry disabled; five-second execution budget; any missing scheduled unit invalidates the entire primary census. |
| 7. Assumptions/terminology | Add rewrite fidelity, complete trace observation, independent representation, no validation tuning, no interference, fixed generation, common support, and runtime-specific scope. Replace undefined “congruence” with “rewrite-invariant on a `B_actual` fiber.” |

## Exact proposed primary study

### Conditions

Each graph/input/tape unit receives four matched conditions:

1. **Identity:** no extra node or boundary.
2. **Node-only control:** an extra deterministic relay node without a security
   boundary.
3. **Pass-through boundary:** the same relay boundary with explicit lossless
   propagation of the canonical provenance record.
4. **Default-reconstruction boundary:** an otherwise byte- and schedule-matched
   boundary using the framework's default metadata reconstruction.

The **single primary comparison** is condition 4 minus condition 3. These two
conditions have the same graph topology, node count, decision-tape consumption,
event opportunities, checkpoint traversal, middleware traversal, and actual
inert effects. The manipulated coordinate is how the boundary propagates
provenance metadata.

Identity and node-only are negative/diagnostic controls. The other approved
rewrite families and CrewAI move to mandatory later replication/generalization;
they cannot replace or pool into the primary result.

### Task view and security view

`B_actual` contains:

- terminal task output;
- the complete sequence of actual inert tool effects;
- completed benign obligations and completion state; and
- decision-tape consumption keyed by semantic obligation.

It excludes only the security metadata being tested: provenance labels,
sanitization/authorization attestations, and their boundary-carriage record.
`V_prov=1` exactly when the same sensitive inert effect lacks the fixed required
provenance transition. Because actual effects are inside `B_actual`, capability
regression among eligible pairs is logically impossible and becomes a negative
oracle control rather than part of the primary pool.

### Common support and weighting

Every graph has exactly four fixed benign inputs, all designed to be base-safe:
trusted, untrusted-plus-sanitized, untrusted-plus-explicitly-authorized, and
chained-authorized. Each runs under tapes 41, 42, and 43.

Let `C` be the intersection of units that:

1. are exactly equal under `B_actual` in all four conditions;
2. are base-safe under the independent provenance reference evaluator; and
3. complete every scheduled condition without protocol failure.

For condition `c`, each graph receives equal weight:

```text
q_c = mean over 120 graphs of
      mean V_prov(c) over that graph's 4 inputs × 3 tapes in C.
```

The primary estimand is:

```text
Delta_boundary = 100 * (q_default_reconstruction - q_explicit_pass_through).
```

The materiality threshold remains the approved normative 10 percentage points.
The unsupported 12-point point prediction is removed. A valid result below 10
points disconfirms material boundary mediation. A valid result at or above 10
supports it. No p-value is attached to the finite census.

The common-support fraction must be 100%. Any missing or ineligible scheduled
unit invalidates the primary census rather than being removed or imputed. This
strict gate is feasible because the grammar constructs all four conditions and
their mappings jointly.

### Exact census

- Runtime: LangGraph 1.2.9, source object
  `95af6a00718588e7b7ce17310e8006d267896a77`.
- Generator seed: 4242.
- Graphs: 120, allocated as 12 declared strata × 10 graphs. The strata cross
  boundary position `{early,middle,late}`, control-flow shape `{linear,branch}`,
  and state lifetime `{ephemeral,persistent}`.
- Inputs: exactly four schemas per graph, fixed above.
- Decision tapes: `{41,42,43}`.
- Scheduled primary executions: `120 × 4 inputs × 3 tapes × 4 conditions = 5,760`.
- Isolation: fresh process and fresh temporary directory per condition; no shared
  filesystem state, cache, telemetry, environment mutation, or network.
- Budget: five CPU seconds per condition. Any timeout, crash, schema error,
  incomplete trace, or missing terminal record invalidates the entire primary
  census.
- Run order: a committed balanced Latin schedule keyed only by graph ID; opening
  the condition labels occurs after both evaluators commit their verdicts.

### Independent validation

The production evaluator and reference evaluator must use different internal
representations and independently written algorithms. They may share only the
published event-schema specification and fixture bytes. Agreement on the same
parsed object is insufficient independence.

Before validation, both implementations must independently pass, for eligibility
and provenance, all four cells of `B_actual same/different × V_prov same/different`,
plus known-safe and known-violating traces. A fixed mutation set separately
inverts equality, drops one actual effect, drops one provenance edge, accepts a
missing authorization, swaps sanitizer order, and widens a capability. The test
suite must kill 100% of these predeclared mutants. Capability invariance among
`B_actual`-equal pairs must be exact.

## Closest-prior correction

[ReliabilityBench](https://arxiv.org/abs/2601.06112) already defines action
metamorphic relations through end-state equivalence and evaluates task
perturbations plus tool/API faults. [ASSURE](https://arxiv.org/abs/2507.05307)
already combines system-level metamorphic execution with behavioral consistency
and security invariants. These invalidate v1's contrast with primarily
input/output NLP testing.

The narrower missing operation is not “metamorphic testing plus security.” It is
a matched **internal orchestration-boundary intervention** that:

1. holds actual task effects and graph exposure fixed;
2. varies only provenance-metadata propagation;
3. conditions on common base-safe task-equal support; and
4. demonstrates mediation by rescue under explicit pass-through.

A local extension of ReliabilityBench would need a new internal graph treatment,
security metadata trace, and causal rescue control; a local extension of ASSURE
would need the same common-support boundary intervention rather than content and
extension-level case generation. Those are the target contribution, not their
existing general metamorphic-testing machinery.

## Revised distinguishing prediction

A graph fuzzer plus functional filter and security checker predicts only that
some rewritten graphs fail. The proposed causal claim predicts a sharper rescue:

> On identical common-support units, framework-default boundary reconstruction
> causes at least 10 percentage points more provenance violations than the same
> boundary with explicit lossless metadata pass-through, while identity,
> node-only, actual effects, and capability invariance remain exact controls.

If both boundary conditions fail equally, the effect is generic added exposure
or evaluator behavior, not provenance-boundary mediation. If explicit
pass-through rescues the effect, the prediction cannot be reduced to “mutations
sometimes fail.”

## Contract changes approved

The approval authorizes these research-design changes only:

- pooled four-family primary → one matched boundary mediation primary;
- all-eligible denominator → common base-safe support with equal graph weight;
- pooled security contracts → provenance primary, capability negative control;
- identity subtraction → explicit pass-through comparator, identity validity;
- 12-point prediction removed; normative 10-point threshold retained;
- other rewrite families/CrewAI become later mandatory replication, not primary;
- exact 5,760-execution validation census and independent-oracle gates fixed.

It does not authorize framework download, confirmatory execution, locked-test
generation/execution, attacks, Kaggle, model
APIs, publication, external messages, or coordinated disclosure.

## User approval and standing default

The user's approval is recorded verbatim:

> go, dont ask me these questions again, go iterate and improve yourself

Operational interpretation: proceed autonomously with rigorous local design,
hypothesis, review, PoC, validation, analysis, and retrospective iterations that
remain inside already authorized research scope; do not repeatedly request
approval for ordinary review-driven design corrections. This standing default
does not relax SciAgent gates and does not authorize Kaggle, live targets,
operational attacks, external messages/publication, model APIs, framework
downloads, or locked-test generation/execution.

## Gate status and next step

Round 1 remains NEEDS_REVISION and budget remains 12/20. The approved c2-v2
contract/config are now fixed. Next: write a new immutable
`059`-successor-numbered hypothesis, run deterministic checks, then dispatch
sterile round 2 and charge 13/20.
