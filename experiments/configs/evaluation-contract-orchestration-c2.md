# Cycle-2 orchestration-security evaluation contract

**Version:** c2-v1
**Recorded:** 2026-07-20
**Status:** APPROVED — user response `ok` on 2026-07-20
**Active study:** Orchestration Metamorphic Security Testing (OMST)

## Claim scope

The primary claim is restricted to a finite controlled comparison: under pinned
framework versions, fixed inert workloads, fixed abstract security contracts,
and fixed decision tapes, some mechanically eligible task-equivalent rewrites
may produce security regressions that identity rewrites do not. The experiment
cannot establish prevalence in deployed agents or universal framework safety.

PDPF and IPHE are selected but parked. Before either becomes active it receives
its own immutable hypothesis and a versioned study appendix; their provisional
success criteria in `PROBLEM.md` are not pooled with OMST.

## Runtime and benchmark matrix

| Role | Runtime | Pin | Workload family |
|---|---|---|---|
| Primary | LangGraph | tag `1.2.9`, object `95af6a00718588e7b7ce17310e8006d267896a77` | 120 validation base graphs; finite branching/handoff workflows |
| Generalization | CrewAI | tag `1.14.7`, commit `21fa8e32d91f87565ffa49e124abea8304d4fb8a` | 60 validation base graphs; independently adapted flows/crews |

Both runtimes use the same canonical obligation and security-contract model but
separate adapters and execution engines. Each condition uses decision-tape seeds
`{41, 42, 43}`. A tape fixes every model-like decision, inert tool result, and
exogenous event by semantic obligation identifier so graph changes cannot gain an
unmatched inference budget.

## Eligible graph relations

The predeclared rewrite families are alpha-renaming, insertion/removal of an
identity relay, reordering independent deterministic gates, and state split/merge
under an explicit field-partition mapping. A pair enters the security analysis
only if a pre-security eligibility checker establishes exact equality of:

1. accepted input domain and initial capabilities;
2. terminal task output;
3. intended inert tool-effect multiset and order where order is declared relevant;
4. completed obligation set and declared completion state; and
5. decision-tape consumption by semantic obligation identifier.

Eligibility is computed before the security-contract outcome is read. A rewrite
that merely matches aggregate benign accuracy is ineligible, not approximately
equivalent. Exclusion counts and reasons are mandatory outputs.

## Primary estimand and comparison

For eligible base graph `g`, rewrite `r`, framework `f`, and decision-tape seed
`s`, let `V(x)=1` when execution `x` violates at least one fixed security contract
and `0` otherwise. Define the paired regression indicator

```text
R(g,r,f,s) = 1[V(base(g,f,s)) = 0 and V(rewrite(g,r,f,s)) = 1].
```

The finite-census primary metric is

```text
rewrite_regression_rate_pp = 100 * sum R / number_of_eligible_pairs.
```

The **single pre-specified primary comparison** is the LangGraph validation
regression rate for the four eligible OMST rewrite families minus the LangGraph
identity-rewrite regression rate, with the same base graphs and tapes. Identity
must be exactly zero under deterministic tapes; a nonzero identity rate is a
protocol failure, not evidence for OMST.

The Phase-2 hypothesis may pass to PoC only with a theory-reviewed threshold.
The current normative materiality target is an excess of at least 10 percentage
points. A valid rate below that threshold disconfirms the material-effect claim;
positive but subthreshold results remain descriptive. The finite validation set
is reported as a census with exact counts, not a population p-value. A
graph-cluster bootstrap may appear only as secondary generator-population
sensitivity and must resample the entire base graph with all paired conditions.

## Secondary outcomes

- regression rate by rewrite family and security-contract family;
- rewrite-induced improvements, reported separately from regressions;
- exact task-equivalence rejection rate and reason;
- benign obligation completion (must be equal for eligible pairs);
- execution steps, wall time, and peak memory;
- generalization direction and magnitude on the pinned CrewAI runtime;
- stochastic-adapter identity variance, if later authorized, as exploratory only.

## Baselines and fairness

- **Identity rewrite:** exact negative control and primary comparator.
- **Unvalidated final-output match:** negative-method comparator showing why final
  answer equality is not an equivalence proof; it cannot enter the eligible OMST
  denominator.
- **Non-equivalent capability mutation:** positive control for the invariant
  evaluator; never counted as a task-equivalent rewrite.

OMST has no tunable model and receives no post-outcome rewrite search. If any
rewrite, contract, generator parameter, or adapter exception is changed after a
validation outcome is observed, a new research iteration and new config version
are required. Both runtime adapters receive the same implementation/debug budget.

## Data tiers and seeds

- **Tuning:** at most 12 hand-authored base graphs, clearly labeled exploratory;
  may debug schemas, adapters, and eligibility but cannot support the hypothesis.
- **Validation:** the fixed 120/60 generated graph sets and decision seeds
  `{41,42,43}`. These decide Phase-5 iteration paths but are not test results.
- **Locked test:** a separate 120/60 graph set using generator seed `20260720`
  and the same decision seeds. It remains ungenerated and unexecuted until a
  clean implementation freeze, independent code review, preregistered prediction,
  and explicit user authorization. It is run once at conclusion. Without that
  authorization, the project must downgrade to validation-only internal evidence.

The generator's validation seeds and workload counts will be fixed in
`experiments/configs/omst-c2-v1.json`. The locked-test absence is itself checked.

## Mutable and immutable paths

Before the Phase-3 freeze, new implementation may be written only under
`experiments/omst/`, with tuning outputs under `experiments/runs/omst-tuning/`.
The following paths are read-only for every OMST result after this contract is
approved:

```text
PROBLEM.md
research-log/053-literature-review-orchestration-security.md
research-log/054-decision-archaeology-orchestration-security.md
experiments/configs/environment-orchestration-c2.md
experiments/configs/data-governance-orchestration-c2.md
experiments/configs/evaluation-contract-orchestration-c2.md
experiments/configs/omst-c2-v1.json
```

The generator, eligibility checker, security evaluator, and adapters become
additional immutable exact paths at the Phase-3 preregistration commit, before
any validation graph is generated. Every evidence bundle records the comparison
commit and verifies `git diff --exit-code <freeze> -- <immutable paths>`.

## Execution and reporting rules

- CPU-only primary runs; no framework telemetry, model API, or network access.
- At least three fixed decision tapes for every paper-bound condition.
- Prediction rows and rationale are committed before every PoC or experiment.
- Failed or ineligible executions are never silently dropped; each has a terminal
  reason code. Missingness by condition is reported.
- No operational attack strings are stored. Abstract fixtures carry only inert
  labels and fake effects.
- No selective best-framework or best-rewrite headline. LangGraph pooled rewrite
  families are primary; all family and CrewAI outcomes are mandatory secondary
  reports.
- A result exceeding the materiality threshold triggers adapter, eligibility,
  and evaluator leakage review before it can be kept.

## Approval boundary

Approval of this contract authorizes Phase-2 hypothesis formation and local static
or tuning-fixture work. It does **not** authorize framework download, a
confirmatory run, locked-test generation/execution, Kaggle, live attacks, model
APIs, publication, external messages, or coordinated disclosure. Those actions
remain separately gated.
