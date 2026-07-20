# PROBLEM.md — Cycle 2: security of agent orchestration

**Supersedes:** the Cycle-1 Kaggle/ORF problem anchor, which closed with the
retrospective at `research-log/052-retrospective.md`. Git history preserves that
anchor through commit `a889275`.

**Direction approval:** the user identified the progression from harness to loop
to graph engineering and then selected the complete research slate verbatim:
`go try all please`. The three directions remain separate studies; selection of
the portfolio does not collapse their evidence or authorize a shared result.

**Core question (one sentence):** Which independently checkable controls preserve
security properties when an agent's harness, execution loop, or orchestration
graph is rewritten or evolves under controlled, inert workloads?

**Who has this problem and why it matters:** Engineers increasingly change the
runtime around an agent—state, retries, handoffs, permissions, verification, and
graph topology—without changing the base model. A task-equivalent rewrite can
therefore cross a trust boundary or alter termination behavior while ordinary
task success remains unchanged. Framework maintainers and teams operating
long-horizon or multi-agent systems need tests that attribute such regressions to
the orchestration layer before deployment.

**Why current approaches fall short:** Current work separately optimizes harnesses
and graphs, evaluates whole systems, blocks individual tool actions, audits supply
chains, or demonstrates loop and planning attacks. It does not yet establish a
controlled security-invariance test for task-equivalent graph rewrites. LoopTrap
suggests independent progress verification but does not validate the proposed
provenance boundary as a defense. MaMa optimizes a system for safety and utility
but does not isolate longitudinal security debt under a fixed external verifier.

**Portfolio order:**

1. **Orchestration Metamorphic Security Testing (OMST):** test whether declared
   task-equivalent graph rewrites preserve security contracts.
2. **Provenance-Decoupled Progress Firewall (PDPF):** replace worker-controlled
   continuation with a controller that sees only attested progress state.
3. **Invariant-Preserving Harness Evolution (IPHE):** replace task-only mutation
   acceptance with a fixed independent safety-contract gate.

SciAgent permits only one active hypothesis. OMST is active first; PDPF and IPHE
remain parked until separate iteration and decision points.

## What success looks like

- OMST supplies mechanically checkable task-equivalence relations and a paired
  measure of rewrite-induced security regressions. A practically material OMST
  result is at least 10 percentage points above the identity-rewrite control on
  the primary finite validation census; exact thresholds remain subject to the
  Phase-2 theory gate.
- PDPF reduces abstract termination-integrity failures by at least 50% relative
  to worker-only continuation while losing no more than 5 percentage points of
  benign task completion and adding no more than 20% execution steps.
- IPHE reduces accepted security-regressing mutations by at least 50% relative
  to task-only mutation selection while retaining at least 90% of the comparator's
  accepted benign utility gain and keeping verifier drift at exactly zero.
- Each result is independently falsifiable. Failure of one direction does not
  become evidence for another, and a synthetic result is never represented as a
  production-agent guarantee.

## Explicit non-goals and authorization boundary

- No Kaggle push, submission, leaderboard read, notebook action, or account
  mutation.
- No live target, real credential, personal data, destructive tool, exploit
  deployment, jailbreak reproduction, attack-prompt optimization, or operational
  payload release.
- No claim that task-equivalent means fully semantically equivalent. OMST
  deliberately holds a declared benign task-observation tuple constant and asks
  whether security-relevant traces still differ.
- No shared multi-hypothesis experiment and no retrospective choice of whichever
  direction yields the most favorable result.
- The locked test tier defined in the evaluation contract is not generated or
  executed without a later explicit user authorization.

**Proxy caveat:** security-contract outcomes on inert, finite framework workloads
are our proxy for orchestration-layer security preservation. Improving those
metrics by weakening the contract, excluding eligible failures, changing the
task-equivalence relation, or tailoring to one framework is failure, not success.

**Question type:** causal within the randomized/paired local interventions defined
by the evaluation contract. Claims outside the tested framework versions,
workload grammars, and abstract security contracts are diagnostic hypotheses only.

## Construct table

| Construct | Operational definition | Observable indicator | Unacceptable proxy |
|---|---|---|---|
| Task-equivalent rewrite | A graph transformation that preserves the predeclared finite benign observation tuple for every eligible input and decision tape in the restricted domain | Exact canonical equality of terminal task output, intended inert tool effects, and declared completion state before security outcomes are inspected | Similar aggregate accuracy, equal final text only, or post-hoc exclusion of mismatches |
| Security preservation | A task-equivalent rewrite does not turn a base execution satisfying the fixed security contract into a rewritten execution violating it | Paired rewrite-induced regression indicator and exact finite-census rate relative to identity rewriting | Model refusal, benign task score, absence of an exception, or a self-judge's safety label |
| Progress integrity | Continue/stop decisions depend only on independently attested obligations and state transitions, not untrusted content or worker-authored summaries | Abstract termination-contract failures, completion rate, and step overhead under matched decision tapes | A hard step cap alone, shorter traces regardless of task completion, or controller access to laundered raw content |
| Evolutionary security debt | Utility-improving harness mutations accepted by the selection rule that newly violate a fixed external security contract | Accepted security-regression rate across a predeclared mutation sequence, with verifier hash unchanged | Final task score, one-version safety, or a verifier that co-evolves with the harness |
| Utility retention | Completion of the same benign obligation set with the same intended inert effects | Exact obligation completion and canonical effect equality; cost recorded separately | Fluency, judge preference, or fewer steps without completing obligations |
| Framework generalization | Direction and materiality replicate under a second independently implemented orchestration runtime | Same preregistered primary/secondary estimands on pinned LangGraph and CrewAI versions | More workloads in one framework or two adapters sharing the same execution engine |
