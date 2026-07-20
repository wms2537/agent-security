# Hypothesis iteration 5 — Orchestration Metamorphic Security Testing v1

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5
**Status:** preregistered hypothesis, unreviewed
**Concept:** Orchestration Metamorphic Security Testing (OMST)
**Claim type:** empirical/systems · **Question type:** causal within the controlled
finite interventions; diagnostic outside them

## Context and boundary

Cycle 2 asks which independently checkable controls preserve security properties
when an agent harness, loop, or graph is rewritten or evolves. The user approved
the exact setup contract with `ok`. OMST is the first and sole active hypothesis;
PDPF and IPHE remain parked and cannot borrow evidence from this study.

This entry specifies a local, inert framework experiment. It does not execute an
attack, retain operational prompts, download a framework, contact a model API,
generate or inspect the locked test, access Kaggle, or claim production safety.
Once theory review is dispatched, this file is immutable.

## Hypothesis

### Primary claim

Under the approved protocol, mechanically eligible task-equivalent rewrites of
the pinned LangGraph runtime will cause an **excess rewrite-induced security
regression rate of at least 10 percentage points** over identity rewriting on the
finite 120-graph × three-decision-tape validation census.

The point prediction is **12 percentage points**, with **low confidence**. The
10-point boundary is a user-approved normative materiality threshold, not an
estimate borrowed from prior work; 12 points is a deliberately modest calibration
commitment above it. Existing evidence supports the mechanism and the need for
measurement, not this magnitude.

The claim is supported only if all protocol-validity checks pass, identity
rewriting produces exactly zero regressions, and the excess is at least 10
points. A valid excess below 10 points disconfirms the material-effect claim.
Positive but subthreshold results are descriptive, not “almost confirmed.”

### Secondary, mechanism-discriminating predictions

1. The pooled identity-relay and mapped-state-split/merge families will have a
   higher regression rate than alpha-renaming because they relocate state or a
   security-observable boundary; alpha-renaming should be the lowest-rate family.
2. Exact benign task observations will remain equal in every eligible pair even
   when the security contract differs. If task outputs change, that pair is not
   evidence for the hypothesis.
3. A final-output-only matching baseline will admit more apparent metamorphic
   pairs but a higher eligibility-oracle error rate than OMST's exact observation
   tuple. It may find failures, but cannot attribute them to a task-equivalent
   orchestration rewrite.
4. CrewAI will show the same positive direction, but no minimum magnitude is
   claimed. A zero or negative CrewAI excess limits framework transfer without
   overturning the explicitly LangGraph-scoped primary claim.

## Variables and the one primary comparison

**Independent variable.** Rewrite condition with five fixed levels: identity,
alpha-renaming, identity-relay insertion, reordering of declared-independent
deterministic gates, and mapped state split/merge.

**`varies` slug.** `orchestration-rewrite-relation`.

**Dependent variable.** The primary dependent variable is the paired indicator
that a secure base execution becomes security-contract-violating after an
eligible rewrite. Secondary variables are eligibility/rejection reason, contract
family, benign obligation completion, execution steps, wall time, peak memory,
and rewrite-induced improvements.

**Controls.** The base graph, accepted input domain, initial capabilities,
decision tape, task obligations, inert tool results, security contracts,
framework version, adapter version, evaluator version, hardware class, and
execution budget are held fixed within every pair. Every graph receives every
rewrite family and all three tapes. Condition order uses a preregistered balanced
schedule; no between-graph assignment is used to estimate the primary contrast.

**Single primary comparison.** On LangGraph validation units only:

```text
pooled eligible OMST rewrite regression rate
minus
paired identity-rewrite regression rate.
```

The four non-identity families are pooled exactly as approved. Family-specific
results, all exclusions, and CrewAI are mandatory secondary reports and cannot
replace the headline comparison.

## Named concept

### Plain-language statement

Ordinary regression tests ask whether a rewritten workflow still finishes the
task. OMST asks a narrower but harder question: after proving that a rewrite
preserves a declared finite set of benign task observations, does the rewrite
also preserve the security contract? It treats a graph rewrite as the test input
and the relationship between two executions as the oracle. The point is not that
the graphs are universally equivalent; it is that ordinary task observations
can remain unchanged while provenance, permission, verification, or termination
behavior changes.

### Formal definition with concrete meanings

Let:

- `g` be one generated base orchestration graph;
- `r(g)` be one graph produced by a fixed rewrite family `r`;
- `f` be one pinned framework and adapter;
- `d` be a decision tape fixing every model-like decision, inert tool result, and
  exogenous event by semantic obligation identifier;
- `X_g` be the finite accepted benign input set declared for `g`;
- `B(f,g,d,x)` be the canonical benign observation tuple: terminal task output,
  intended inert tool-effect sequence or multiset according to the task contract,
  completed obligations, completion state, and semantic decision-tape
  consumption for input `x`;
- `V(f,g,d,x)` be 1 when the fixed security-contract evaluator finds at least one
  abstract provenance, permission, verification, or termination violation, and 0
  otherwise.

For this experiment—not outside it—`g` and `r(g)` are **task-equivalent** when
they accept the same `X_g`, begin with identical capabilities, and

```text
B(f,g,d,x) = B(f,r(g),d,x)
```

for every preregistered `d` and every `x` in the finite `X_g`. Equality is exact
canonical equality, not semantic similarity. Eligibility is evaluated before
the security verdict is read.

For an eligible tuple `(g,r,f,d,x)`, define the rewrite-regression indicator

```text
R = (1 - V(f,g,d,x)) * V(f,r(g),d,x).
```

This multiplication has a concrete reading: it equals 1 only when the base is
safe (`V=0`) and the rewrite is unsafe (`V=1`); it is 0 in all other cases. Let
`E_f` be all eligible non-identity LangGraph validation tuples and `I_f` the
matched identity tuples. The primary estimand is

```text
Delta_f = 100 * [sum(R over E_f)/|E_f| - sum(R over I_f)/|I_f|].
```

`Delta_f` is a percentage-point contrast over the exact finite census. It is not
a probability for unobserved production agents. Identity must make the second
term exactly zero. A nonzero identity term means deterministic replay or the
evaluator is broken and invalidates the protocol.

Equivalently, OMST asks whether finite task equivalence under `B` implies the
one-way security refinement “base safe implies rewrite safe.” The hypothesis
says that implication fails at a materially nonzero rate in the tested runtime.

## Why the mechanism is plausible

### Projection rather than universal equivalence

An agent runtime maps a high-level graph plus state and decisions into an event
trace. `B` is a projection of that trace onto declared benign task observations;
`V` is a different projection onto security-relevant relations. Equality after
the first projection does not logically imply equality after the second. The
hypothesis is therefore not “equivalent programs behave differently.” It is that
the commonly observed benign projection can be congruent under a rewrite while
the security projection is not.

The four rewrite families probe different places where this can happen:

- Alpha-renaming should normally leave both projections invariant, providing a
  structure-preserving lower-bound family.
- An identity relay preserves declared task effects but adds a handoff,
  checkpoint, or middleware boundary where provenance or capability metadata may
  be dropped, widened, or reconstructed.
- Reordering declared-independent gates preserves benign effects only within the
  declared commutativity domain, but middleware order can still alter what
  security context is visible at an action.
- State split/merge preserves mapped benign fields while changing granularity,
  persistence, and join behavior for security labels.

If the runtime compiler and adapters preserve both `B` and the security
contracts as congruences, then every eligible `R` is zero and the hypothesis is
cleanly falsified. No theorem guarantees the positive claim.

### Evidence chain and novelty boundary

- *Towards Long-Horizon Agents* models long-horizon agency as a policy coupled
  to a harness and names loops, memory, tools, orchestration, middleware, and
  verification as separate runtime components
  ([preprint](https://www.preprints.org/manuscript/202607.1328)). This supports
  treating the runtime as a scientific object, not the security effect.
- MASEval evaluates the system unit across three benchmarks, models, and
  frameworks, while FlowSteer shows that planning-time graph steering can change
  outcomes ([MASEval](https://aclanthology.org/2026.acl-demo.34/),
  [FlowSteer](https://arxiv.org/abs/2605.11514)). These support framework and
  planning sensitivity but do not establish security invariance.
- Agentic Harness Engineering reports task-performance gains from iterative
  harness changes and also reports incomplete guardrails
  ([AHE](https://arxiv.org/abs/2604.25850)). It motivates versioned runtime
  changes but supplies no rewrite-level security control.
- LoopTrap demonstrates termination poisoning across eight agents and explicitly
  motivates independent progress verification; Agent-BOM supplies a graph
  representation for agent supply-chain security; MaMa optimizes safety and
  utility in agent-system design ([LoopTrap](https://arxiv.org/abs/2605.05846),
  [Agent-BOM](https://arxiv.org/abs/2605.06812),
  [MaMa](https://arxiv.org/abs/2602.04431)). None asks whether a declared
  task-equivalent rewrite preserves security.
- A May-2026 systematic survey covers 93 primary studies on metamorphic testing
  and LLMs, including autonomous agents, while LLMORPH implements 36 relations
  over four NLP tasks and more than 561,000 executions
  ([survey](https://arxiv.org/abs/2605.13898),
  [LLMORPH](https://arxiv.org/abs/2603.23611)). LLMORPH's manually checked
  relation/task false-positive rates range from 0% to 70%, which directly warns
  against calling output similarity an equivalence proof. These works transform
  textual inputs and compare model outputs; they do not validate security
  refinement under orchestration-graph rewrites.

The literature therefore supports an **evidence gap**, not a known positive
effect. The experiment can legitimately return zero.

## Measurement design

### Units and interventions

The primary finite census contains 120 generated LangGraph base graphs. The
generalization census contains 60 CrewAI base graphs. Each graph contains the
preconditions needed to attempt all four non-identity rewrite families. Every
base graph is evaluated under tapes 41, 42, and 43, then paired with every rewrite
under the same tape.

The graph generator is fixed before validation and balances workflow depth,
branching, handoffs, state fields, security-contract family, and order-sensitive
versus order-insensitive benign effects. Workload balance describes the tested
finite set; it is not a claim about production prevalence.

### Eligibility and oracle separation

The eligibility checker receives canonical benign observations but no security
verdict. The security evaluator receives canonical traces with condition labels
replaced by hashes and does not know whether a trace is base, identity, or a
specific rewrite family until all verdicts are committed. Generator, adapters,
eligibility checker, evaluator, and label-opening code become independently
hashed immutable inputs before validation.

Every scheduled execution must end in one terminal status. Framework crashes,
timeouts, schema errors, or incomplete evidence invalidate the corresponding
confirmatory bundle; they are not silently omitted. Eligibility rejection is not
missing data because it defines the relation-specific estimand, but every
rejection reason is counted. For interpretability, a protocol-valid validation
requires at least 95% eligibility in every rewrite family and no more than a
5-percentage-point eligibility-rate spread between families. Falling outside
that envelope invalidates the material pooled claim rather than letting a single
easy family dominate it.

### Security contracts

Security outcomes are deterministic predicates over abstract event traces:

1. **Capability:** no inert effect outside the graph's initial capability set.
2. **Provenance:** no untrusted abstract label reaches a declared sensitive inert
   effect without its fixed sanitization/authorization transition.
3. **Verification:** terminal success requires the independently declared
   evidence obligations.
4. **Termination:** completion or continuation must follow the fixed obligation
   and repeated-state rules.

These constructs have exact machine predicates. They do not use model refusal,
free-text judges, or real exploit payloads.

### Negative and positive controls

- Identity rewriting must yield exact trace equality and zero regressions.
- Alpha-renaming tests whether nominal identifiers leak into behavior.
- Final-output-only matching demonstrates the unacceptable weak proxy but stays
  outside the eligible OMST denominator.
- A predeclared non-equivalent capability mutation must be rejected by the
  task-equivalence checker or detected by the security evaluator, as applicable.
- A small hand-derived fixture set is recomputed by an independent reference
  evaluator before generated validation is permitted.

### Primary and generalization interpretation

The primary result is an exact count and percentage-point contrast. No p-value
is attached to the finite census. A graph-cluster bootstrap may be reported only
as secondary sensitivity to a declared graph-generator population and must
resample whole graphs with all tapes and conditions. It cannot rescue a
subthreshold primary result.

CrewAI uses an independently implemented adapter and runtime. Its result tests
directional transfer, not universal generalization. If its adapter shares core
execution code with LangGraph, it is not an independent generalization and the
claim must be downgraded.

## Assumptions and validity domains

| ID | Assumption | Validity domain | What happens outside it |
|---|---|---|---|
| A1 | Canonical `B` captures every benign observation required by the declared task contract | Finite generated workloads and explicit obligation/effect schemas only | The relation is too weak; a “regression” may be an ordinary functional difference |
| A2 | Decision tapes key decisions by semantic obligation, not incidental node order | Rewrites with a total, mechanically checked semantic-ID mapping | Unmatched compute or different decisions confound the rewrite effect; pair is invalid |
| A3 | Security predicates correctly implement the four abstract contracts | Inert event schema and independently reviewed reference fixtures | Measurement error can manufacture or hide regressions; no conclusion is valid |
| A4 | Framework adapters faithfully expose equivalent canonical events | Pinned versions and adapter-supported graph subset | Adapter artifacts, not framework orchestration, may explain the result |
| A5 | Rewrite preconditions prove only the declared finite task relation | Tested inputs, tapes, and capabilities | No claim of full program equivalence or unseen-input behavior is allowed |
| A6 | Generated graphs cover the boundary mechanisms under study | Balanced grammar defined before validation | A zero may mean absent stressors rather than universal invariance |
| A7 | Deterministic tapes remove inference stochasticity and history dependence | Local inert adapters with network and telemetry disabled | Identity may vary; the primary causal attribution fails |
| A8 | The 10-point threshold represents practical materiality | This project decision only | It is not a field-standard clinical or operational cutoff and cannot be generalized |
| A9 | Pinned LangGraph and CrewAI versions are stable units of intervention | Exact source hashes and lockfile used in the run | Later versions require a new study; “framework X is unsafe” is unsupported |

## Fixed bias surface

1. **Selection.** Graphs are generated from a preregistered balanced grammar and
   every generated unit is scheduled. Relation eligibility is post-intervention
   by construction, so the estimand is explicitly conditional on eligible pairs;
   rejection counts/rates and the 95%/5-point envelope prevent silent favorable
   selection. No claim covers rejected relations.
2. **Confounding.** Base and rewrite share graph, tape, input, capabilities,
   tools, budget, framework, adapter, and hardware. Runtime/framework comparisons
   are secondary and not used as the causal primary contrast. Adapter bugs remain
   a rival explanation addressed by reference fixtures and independent review.
3. **Allocation/assignment.** Every graph receives every condition under the
   same three tapes. A fixed balanced order schedule distributes warm-cache and
   order effects; condition is not assigned according to graph difficulty.
4. **Protocol deviation.** The exact command, environment lock, immutable hashes,
   scheduled unit set, terminal-status ledger, and COMPLETE-last evidence bundle
   are verified before a result can enter `results.tsv`. Any scientific change
   after outcome inspection requires a new iteration.
5. **Missing data.** No failed, timed-out, or malformed scheduled execution is
   imputed or dropped. The primary confirmatory bundle requires every execution
   to reach an allowed terminal status and reports status counts by condition;
   relation-ineligible pairs are reported separately rather than called missing.
6. **Measurement.** Exact task equality and deterministic security predicates
   replace semantic judges. Security evaluation is condition-label-blind until
   commitments are written; identity, non-equivalent, and reference fixtures
   test the evaluator and eligibility oracle. Systematic schema error remains
   fatal regardless of sample size.
7. **Analysis flexibility.** The pooled LangGraph contrast, identity baseline,
   10-point threshold, eligibility envelope, four rewrite families, and mandatory
   secondary tables are fixed here. Bootstrap inference is secondary and cannot
   change the finite-census verdict.
8. **Selective reporting.** All graph × family × tape terminal states, eligibility
   reasons, contract verdicts, and both framework summaries are published in the
   local evidence bundle. PDPF/IPHE results remain separate and no best-family or
   best-framework substitution is allowed.

## Rival explanations and discriminating checks

| Rival explanation | Why it could mimic the claim | Predeclared discriminating check | Conclusion impact if unresolved |
|---|---|---|---|
| Adapter defect | Canonicalization could drop or invent security metadata | Hand-derived fixtures, independent reference evaluator, adapter code review, and exact source hashes | Downgrade from framework result to adapter-artifact report |
| Weak task equivalence | `B` may omit a benign effect that actually changed | Exact obligation/effect schema plus a nested stricter-`B` sensitivity reported secondarily | If primary pairs fail the approved `B`, invalidate; if only stricter sensitivity changes, narrow the relation claim |
| Security-oracle defect | A predicate may simply encode the rewrite family | Condition-label blinding, identity negative, non-equivalent positive, mutation testing of predicates | Any failure invalidates the primary result |
| Generator artifact | Grammar may hard-code the supposed mechanism | Hand-authored fixtures and independent CrewAI adapter; report every grammar factor | Restrict claim to the generated census; no framework-level inference |
| Unequal compute or decisions | Rewrite could receive extra calls or different tape entries | Semantic-ID tape consumption must be exactly equal for eligibility | Pair is ineligible; widespread failure invalidates the pooled design |
| Family-composition artifact | High-rate or high-eligibility family could dominate pooling | All graphs attempt all families; 95% per-family eligibility and 5-point spread gates; mandatory family table | Failing envelope invalidates pooled materiality claim |
| Warm-cache/order effect | Later executions may inherit runtime state | Fresh process per unit plus balanced order and identity check | Nonzero identity or order dependence invalidates causal attribution |
| Version-specific defect | One release may contain a transient bug | Exact version claim plus CrewAI directional report; later versions require reproduction | No universal or current-future framework claim |

## Metrics, thresholds, and decision table

| Outcome | Metric | Confirm/support | Disconfirm | Protocol invalid |
|---|---|---|---|---|
| Primary material effect | `Delta_langgraph` in percentage points | `>=10.0` and all validity checks pass | `<10.0` on a valid census | Identity nonzero, incomplete scheduled set, evaluator/control failure, or eligibility envelope failure |
| Point-prediction calibration | Absolute error from 12 pp | `<=5 pp` is calibrated | `>5 pp` is miscalibrated even if materiality direction holds | Primary protocol invalid |
| Task equivalence | Exact eligible-pair equality | `100%` equality within included pairs | N/A; non-equal pairs are ineligible | Eligibility below 95% in a family or spread above 5 pp |
| Mechanism ranking | relay+split/merge rate versus alpha-renaming | pooled former rate greater | equal or lower | Family eligibility invalid |
| Generalization | `Delta_crewai` | positive direction | zero or negative limits transfer | CrewAI adapter not independent or bundle invalid |
| Identity control | regression rate | exactly `0.0` | N/A | any nonzero value |

There is no scientifically “inconclusive” primary interval. A valid value below
10 is a disconfirmation. “Inconclusive” is reserved for protocol invalidity and
does not consume the hypothesis as a successful test.

## Idea taxonomy

- **Opportunity pattern:** Evidence Gap, with a secondary Failure/Risk Gap.
- **Method paradigm:** Empirical Mapping, supported by Formal Derivation of the
  relation and estimand.
- **Dominant operation:** `formalize`, with `decouple` secondary: formalize a
  graph-level metamorphic relation, then decouple benign task observation from
  security refinement.

This is not Bridge Opportunity × Synthesis/Unification and does not integrate
multiple defenses. It applies one local operation to the strongest nearby
testing assumption: replace approximate output similarity with a mechanically
eligible finite task relation and test one security-refinement implication.

## Anti-stacking and Occam checks

OMST is a reframing/measurement hypothesis, not a bundle of defenses. A plain
combination of graph fuzzing and a security checker predicts that some mutated
graphs will fail. It does **not** require that failures persist after exact task
equivalence, identity control, equal decision tapes, and pre-security eligibility
are enforced. OMST's distinguishing prediction is therefore:

> At least 10 percentage points of secure-base → unsafe-rewrite regressions remain
> among mechanically eligible, exact-task-equal pairs, while identity remains
> exactly zero and state-boundary rewrites outrank alpha-renaming.

If failures disappear after eligibility is enforced, graph fuzzing may still be
useful, but the OMST security-invariance claim is false.

The simplest comparator is identity rewriting, not a larger learned defense. No
LLM, optimizer, judge ensemble, adaptive search, or new security mechanism is
needed to test the claim. Removing the label-blinding or relation-validity
machinery would make the result simpler to compute but unable to distinguish the
main rival explanations.

## Predicted failure modes

1. **True invariance:** the pinned runtimes preserve all four contracts for every
   eligible rewrite; valid `Delta=0`, decisively falsifying materiality.
2. **Relation collapse:** fewer than 95% of pairs are eligible in a family,
   showing the rewrite library does not implement the claimed task relation.
3. **Adapter-induced signal:** regressions vanish under the reference interpreter
   or differ by canonicalizer; the framework claim is unsupported.
4. **Oracle leakage:** the evaluator learns condition from trace formatting;
   label blinding or mutation controls fail, invalidating all security counts.
5. **Weak workload stress:** all generated graphs lack real boundary pressure.
   This cannot turn zero into confirmation; it restricts the negative conclusion
   to the tested grammar.
6. **Single-family dominance:** one family supplies most eligible units or
   regressions. The eligibility envelope and mandatory family report expose it;
   failing the envelope invalidates the pooled headline.
7. **Framework non-independence:** both adapters share execution code, making the
   CrewAI result pseudo-generalization; only the LangGraph result remains.
8. **Normative threshold mismatch:** a reproducible 1–9.99 pp excess may matter in
   another use context, but it still disconfirms this preregistered material claim.

## Self-critique and re-derivation

The load-bearing logic can be reconstructed without equations:

1. A full trace contains more information than the benign task view.
2. Equal benign views therefore do not entail equal security views unless the
   runtime and rewrite preserve the security contracts as an additional
   congruence.
3. The experiment observes both base and rewritten execution under the same
   finite tape, so the paired secure→unsafe indicator is directly observed, not
   imputed as a missing potential outcome.
4. Averaging that binary indicator over all eligible tuples yields the exact
   finite regression rate. Subtracting identity removes only protocol/replay
   regressions; identity is required to be zero, so it cannot statistically
   “adjust away” a broken protocol.
5. The materiality claim follows only if the exact contrast is at least 10
   points. Nothing in the structural argument proves that magnitude.

The hardest objection is that eligibility is defined after the rewrite and can
select a favorable subset. That objection is correct against a claim about all
rewrites. OMST instead defines its construct as the conditional relation on exact
eligible pairs, reports every rejection, requires high balanced eligibility, and
makes no claim about rejected pairs. If the eligibility envelope fails, the
headline is invalid rather than extrapolated.

The next-hardest objection is that deterministic synthetic tapes test framework
plumbing rather than realistic LLM agency. That is also correct as a scope limit.
Determinism is what isolates orchestration causally; a later stochastic-agent
study would be a separate external-validity question. This hypothesis must be
reported as a finite framework-runtime result.

## Gate Check before theory review

- Falsifiable claim, IV/DV, controls, expected effect, and one primary comparison:
  specified above.
- Search dimension: `orchestration-rewrite-relation`, kind `metric`, Cycle 2
  iteration 5; no current-cycle escalation constraint is active.
- Concept: named, plain-language statement and finite formal definition present.
- Empirical/systems justification: causal mechanism, evidence chain, measurement
  design, nine assumptions with validity domains, eight fixed bias items, and
  rival-explanation table present.
- Failure, disconfirm, and protocol-invalid outcomes: separated.
- Metrics: exact primary, calibration, mechanism, generalization, and controls
  with concrete thresholds.
- Taxonomy: Evidence Gap × Empirical Mapping × formalize; no default-template
  tripwire.
- Anti-stacking: exact-task-equal residual-regression prediction distinguishes
  OMST from graph fuzzing plus a checker.
- Problem alignment: confirmation would show that task-preserving orchestration
  changes can materially alter security contracts and supply a checkable control
  for the first part of Cycle 2's core question.
- Theory review: **PENDING**. No experiment is permitted before RIGOROUS.

## Decision

Commit this entry and its targeted two-paper source record, run deterministic
structure checks, then dispatch one sterile empirical/systems theory review. A
NEEDS_REVISION verdict creates a new superseding hypothesis; this file will not
be patched after dispatch.

## Next Steps

1. Append the Cycle-2 search-log entry and freeze this hypothesis in git.
2. Spend one hypothesis-review round at dispatch, not before.
3. Proceed to Phase 3 only if the blind verdict is RIGOROUS with scrutiny.
