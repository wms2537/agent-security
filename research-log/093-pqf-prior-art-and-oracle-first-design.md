# PQF prior art and oracle-first design

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6
**Task:** T037 · **Status:** design evidence before hypothesis freeze

## Question

What is the smallest defensible advance beyond “use an independent progress
verifier,” and how can it be evaluated without making safety true by definition?

This note contains defensive architecture and abstract labels only. It does not
retain or generate jailbreak strings, reproduce LoopTrap strategies, run a model
or framework, access Kaggle, or create/inspect a locked test.

## Targeted primary-source comparison

### LoopTrap — the measured threat and explicit open defense gap

Xu et al. define termination poisoning as corruption of an agent's progress
judgment through untrusted context. Their sandboxed study covers eight agents and
60 tasks; the abstract reports 3.57× mean step amplification and a 25× peak. The
paper motivates independent progress verification and provenance-aware
processing but does not validate a comprehensive defense.

- Primary source: <https://arxiv.org/abs/2605.05846>
- Consequence here: “add an independent progress verifier” is not a novel claim.
  The contribution must specify the information boundary, the verifier's trusted
  inputs, the utility cost, and an evaluation that remains capable of failing.

### IAL-Scan — structural bounds, not content noninterference

Hou et al. model infinite agentic loops with a framework-independent Agent IR and
an Agentic Loop Dependence Graph. A finding requires a feedback path that can
repeatedly reach costly or state-growing operations without effective bound
coverage. They report 68 manually confirmed failures among 74 findings across
6,549 repositories (91.9% precision).

- Primary source: <https://arxiv.org/abs/2607.01641>
- Consequence here: a progress firewall does not replace static bound coverage.
  PQF must be paired with a hard external budget, and its claim is about runtime
  termination decisions under bounded execution, not discovery of code-level
  infinite loops.

### SafeAgent — external governance with a content-aware core

SafeAgent separates runtime execution governance from a context-aware security
decision core over persistent session state. That is a system-level rather than
input/output-only defense, but the decision core deliberately reasons over
context.

- Primary source: <https://arxiv.org/abs/2604.17562>
- Consequence here: PQF makes a different, testable choice. Its continuation
  controller is denied raw context, worker summaries, tool payloads, and hashes
  derived from those bytes. It receives only verifier-owned identifiers and
  counters.

### Agent-C and C-Trace — formal trace enforcement, different properties

Agent-C translates temporal action constraints to logic and intervenes during
tool-call generation. C-Trace evaluates formal compliance predicates over
runtime traces and reports sensitivity to event-extractor noise. These systems
show that sequence-level enforcement and imperfect extraction matter, but their
properties concern action/policy conformance rather than whether more work is
needed.

- Agent-C: <https://arxiv.org/abs/2512.23738>
- C-Trace: <https://arxiv.org/abs/2606.19242>
- Consequence here: PQF must not claim general action safety. Its world oracle
  scores only termination integrity, exact inert effects, and task completion.
  Receipt delay/dropout is a first-class stressor rather than an ignored detail.

### PCN-Rec — worker as proposer, deterministic verifier as authority

PCN-Rec has an LLM propose a structured certificate but deterministically
recomputes constraints from the proposed slate before acceptance. The relevant
principle is proof-carrying interaction: a worker's claim is not itself proof.

- Primary source: <https://arxiv.org/abs/2601.09771>
- Consequence here: a worker may name a candidate transition, but only an
  external receipt adapter may add its identifier to the progress quotient.
  Worker-authored `completed=true`, summaries, and self-signed hashes are never
  controller inputs.

## Synthesis: the local move

The defensible move is not to integrate these systems. It is to **decouple** one
specific control decision from one specific information source:

```text
replace continuation(raw history + worker progress claims)
with continuation(verifier-owned progress quotient only).
```

The quotient contains a trusted plan binding, identifiers of independently
accepted obligation/effect/fault transitions, a verifier-owned stall counter,
and the remaining external budget. It contains no raw task text, observation,
tool result, worker summary, model confidence, embedding, or digest computed from
untrusted content. Hashing untrusted content does not make it trusted and could
retain a high-bandwidth covert signal.

This is **Failure/Risk Gap × Extrapolation/Robustification**, dominated by
`replace` and `decouple`. It is not Bridge × Synthesis.

## Oracle first: prevent a definitional victory

The architecture and outcome oracle use different inputs and representations.

### Controller-side receipt representation

The receipt adapter emits only:

```text
(plan_digest,
 open_obligation_ids,
 verified_completed_obligation_ids,
 verified_effect_ids,
 verified_terminal_fault_ids,
 steps_since_verified_transition,
 remaining_step_budget)
```

The PQF controller maps that quotient to one of `CONTINUE`, `CHECK`,
`STOP_SUCCESS`, `STOP_FAULT`, or `STOP_BUDGET`.

### Outcome-side world representation

The independent oracle reads a canonical world-event tape and the controller's
terminal event. It reconstructs required effects, actual commits, dependency
order, terminal world faults, duplicate effects, and how long execution
continued after the world reached a terminal state. It does **not** read the
controller quotient or receipt-acceptance labels.

The two sides may agree when the receipt adapter is sound and sufficiently
complete. They are not the same function. A false-positive receipt can therefore
make PQF stop successfully while the independent world oracle says an obligation
is incomplete. That finite counterexample is required in the static verifier.

### Co-design falsifier

A deliberately invalid oracle mutant derives `complete` from
`verified_completed_obligation_ids`. It will mask the false-positive-receipt
counterexample. The validation harness must kill this mutant and reject any
outcome implementation that imports or calls controller/receipt code.

### Quotient-leak falsifiers

At least these controller mutants must break paired decision invariance and be
killed:

1. add `worker_progress_advisory` directly;
2. add a hash of the worker summary;
3. let the worker add a `completed` identifier without verifier acceptance; and
4. let a raw tool payload choose `CHECK` versus `CONTINUE`.

## What is structural and what remains empirical

The structural statement is modest and classical: if controller
`c = kappa composed_with q`, histories with the same quotient receive the same
decision. Conversely, a controller constant on every quotient fiber has a
unique factor on `image(q)`. This is an information-flow/factorization property,
not evidence that `q` contains enough truthful progress to finish a task.

The nontrivial systems question is whether the quotient remains sufficient under
independently generated receipt delay, recoverable dropout, retries, fork/join
obligations, terminal faults, and finite budgets. PQF can fail through false
receipts, missing receipts, bad obligation graphs, excessive checks, or a quotient
that omits information necessary for correct stopping. The external oracle makes
all of those failures observable.

## Decision

Proceed to a v1 hypothesis with:

- one primary PQF-versus-worker-self-judgment comparison;
- an exact quotient-invariance validity gate;
- a baseline-risk floor so a trivial zero-risk corpus cannot yield a misleading
  “100% reduction”;
- the existing thresholds: at least 50% relative termination-failure reduction,
  no more than 5 percentage points benign completion loss, and no more than 20%
  step overhead;
- hard-cap and receipt-aware-full-state controllers as secondary baselines;
- independent-oracle clause mutants, quotient-leak mutants, and receipt-soundness
  counterexamples; and
- a claim restricted to a finite inert abstract workload until later evidence
  justifies any framework correspondence.

Theory review cannot be dispatched: the cumulative hypothesis-review budget is
20/20. The hypothesis may be written and statically checked, but Phase 2 cannot
pass and Phase 3 cannot begin without a user-granted review extension.
