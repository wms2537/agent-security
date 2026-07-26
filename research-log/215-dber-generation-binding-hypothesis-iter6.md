# DBER — Generation-Binding Hypothesis, Iteration 6

**Date:** 2026-07-26 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 6/6 · **Status:** frozen before theory review

## Context

SCOC-32 was refuted as a distinct mechanism, while its live-era notebook scored
`81.225` with `enable_scoc=False`. Report 208 selected a new orchestration
dimension: admission of already successful probe outputs under separate
generation and replay budgets.

The pre-change profile at `artifacts/dber/run03` produced:

| Controlled regime | Discarded successful probes | Incumbent raw | Oracle salvage raw | Oracle gain | Result |
|---|---:|---:|---:|---:|---|
| generation binding | 26 | 846 | 468 | 55.3191% | supports a narrow premise |
| replay binding | 28 | 72 | 0 | 0% | refutes residual-packing premise |
| candidate binding | 27 | 54 | 0 | 0% | confirms no-op boundary |

The replay-fragment subclaim is retracted. This hypothesis concerns only
generation-binding runs.

## Named concept

### Name

**Dual-Budget Evidence Reuse (DBER).**

### Plain-language statement

The attack currently spends generation time testing candidates, learns that
some are valid, then throws those exact candidates away before constructing its
returned list. DBER keeps those successful probes as optional inventory. It adds
them only if the ordinary controller stops because generation time is binding
while replay time and candidate slots remain. If replay or candidate capacity is
binding, or if the safety calculation does not pass, DBER returns the incumbent
portfolio unchanged.

### Operational definition

For one attack run:

- `C` is the incumbent returned candidate sequence in its original order.
- `P` is the sequence of exact probe candidates whose generation trace contains
  at least one qualifying EXFILTRATION event and whose candidate signature is
  absent from `C`.
- Each `p` in `P` has observed public-generation replay surrogate cost `r(p) > 0`
  and official-SDK raw value `q(p) > 0`.
- `B` is the incumbent replay-safe cap and `R(C)` is the sum of the same measured
  per-candidate costs the incumbent already uses for `C`.
- `K` is the remaining candidate count below the official `2,000` cap.
- `stop(C)` is the controller's exact terminal reason.
- `alpha = 2.0` is the preregistered supplemental-cost stress factor; it is not a
  probability or a tail guarantee.

DBER is eligible only when:

```text
stop(C) = generation
K > 0
R(C) + alpha * min_p_in_P r(p) <= B
```

Eligible probe candidates are traversed by descending `q(p)/r(p)`, then stable
probe order. DBER greedily constructs `S` subject to:

```text
|S| <= K
R(C) + alpha * sum_p_in_S r(p) <= B
```

The returned sequence is `C` followed by `S`. If eligibility fails or `S` is
empty, the returned sequence is exactly `C`.

This is a deterministic bounded packing rule, not a claim of solving the
0/1-knapsack optimum. The factor `alpha` controls a stress envelope in the local
tests; because it is not calibrated to a live latency distribution, it cannot
alone establish a target timeout probability.

## Hypothesis

Under controlled real-SDK regimes in which the unchanged incumbent is
generation-bound and has successful discarded probes, DBER will improve paired
official raw score by at least **10% on average across three preregistered
profiles**, with nonnegative gain in every profile, while:

1. leaving the incumbent prefix byte-equivalent;
2. returning only exact previously successful probe candidates as supplements;
3. satisfying the replay-safe and 2,000-candidate bounds under
   `alpha=2.0`; and
4. returning the exact incumbent sequence in preregistered replay- and
   candidate-binding negative controls.

Mechanistic reason: DBER changes no target interaction and no candidate
semantics. It reclassifies already observed successful probe traces from
measurement-only waste into conditional output inventory when generation has
zero remaining opportunity value but replay/candidate headroom still has
positive capacity.

## Variables

### Independent variable

`probe_output_admission_policy`:

1. `incumbent_discard` — current behavior;
2. `dber_generation_gate` — the rule above; and
3. `bank_all` — admit every successful probe without resource gating, used only
   as a negative control.

### `varies` slug and search kind

```text
varies=probe-output-admission-under-separate-generation-and-replay-budgets
kind=metric
```

This dimension is absent from the prior Cycle-3 metric search. It changes
neither message multiplicity, prefix control, resource-risk stopping, nor
conversation-state representation.

### Dependent variables

Primary:

- paired official-SDK raw-score gain percent of DBER over the incumbent,
  averaged across three preregistered generation-binding profiles.

Secondary:

- per-profile raw gain;
- number and raw value of admitted probes;
- replay-cost stress sum;
- replay-cap overage count;
- candidate-cap overage count;
- incumbent-prefix identity;
- no-op output identity in replay- and candidate-binding controls;
- bank-all overage count;
- runtime and peak memory.

## Pre-specified primary comparison

On three new controlled generation-binding profiles not used in run03, compare
`dber_generation_gate` with `incumbent_discard` using the same deterministic
profile parameters, SDK seed, template bank, probes, route, safe cap, and
candidate construction. Each policy is evaluated on the same successful-probe
inventory and incumbent sequence for an exact paired policy contrast.

Primary success:

```text
mean paired raw gain >= 10%
minimum per-profile paired raw gain >= 0%
replay overages = 0
candidate overages = 0
incumbent-prefix mismatches = 0
supplement provenance mismatches = 0
```

The `10%` threshold is a conservative fraction of the exploratory `55.3191%`
oracle ceiling. The predicted value is `30%` with medium confidence. No sampling
population or p-value claim is made: the three profiles are fixed engineering
units, and the result is an exact conditional contrast over them.

## Controls and invariants

Frozen across policies:

- official SDK scorer, predicates, cell logic, guardrail, fixture set, and seed;
- `experiments/attack.py` incumbent behavior before the DBER admission point;
- eight templates and all message strings;
- probe count, order, route selection, selected structure, and fill construction;
- generation and replay budgets, candidate cap, `replay_safe`, and incumbent
  `cost_inflation`;
- all target interactions and exported traces;
- candidate identity, raw computation, and order of `C`;
- no SCOC activation;
- result exclusions and thresholds.

The implementation may store successful probe candidates and terminal reason
while the incumbent executes. It may not add a probe, change a prompt, re-run a
target interaction, change route selection, or modify scorer/evaluator code.

## Engineering justification

### Measured bottleneck

The pre-change profile is committed at:

- `artifacts/dber/run03/dber-profile.json`
- `artifacts/dber/run03/dber-profile.tsv`
- `artifacts/dber/run03/run.log`

In the generation-binding unit, the unchanged controller returned `846` raw but
discarded 26 exact successful probes worth `468` oracle-salvage raw. Their
observed aggregate cost was `0.938870 s`, while replay headroom was `4.223351 s`.
Even the `alpha=2.0` stress charge yields:

```text
incumbent cost + 2 * probe cost
= 1.716649 + 2 * 0.938870
= 3.594390 s
< 5.940000 s safe cap
```

The negative profile matters equally. In the replay-binding unit, 28 successful
probes existed but none fit the `0.019611 s` residual; bank-all would exceed the
cap by `0.948191 s`. Therefore "valid probes exist" is not sufficient. The
binding-resource and headroom gate is load bearing.

### Source basis

The official competition gateway
`comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py` gives attack
generation and each model/guardrail replay separate `9,000 s` deadlines. The
official limits in `comp/sdk/aicomp_sdk/evaluation/ops.py` cap the returned set
at 2,000 findings and 32 messages per finding. The official scorer in
`comp/sdk/aicomp_sdk/scoring.py` gives each successful unique-domain
EXFILTRATION finding positive raw value. These source facts make a generated,
successful, unique probe a score-bearing candidate if replay capacity remains.

Zou et al., *Security Challenges in AI Agent Deployment: Insights from a Large
Scale Public Competition* (NeurIPS 2025) motivates trajectory-level evaluation
under heterogeneous agent and defense behavior; it does not establish DBER's
resource effect. The July-2026 preprint *Towards Long-Horizon Agents: A Survey*
separates model policy from harness loops, memory, tools, orchestration, and
verification; it supports treating admission as a harness variable, but it is
not peer reviewed and is not load-bearing evidence. The hypothesis rests on the
official SDK and the measured profile, not those adjacent works.

### Per-component mechanism and ablations

DBER is one local replacement with two inseparable checks:

| Element | Measured bottleneck | Role | Required ablation |
|---|---|---|---|
| successful-probe inventory | 26 discarded valid probes, 468 raw ceiling in generation binding | preserve exact already-generated candidates and costs | remove inventory: output and score must equal incumbent |
| generation/headroom admission gate | replay control has 28 valid probes but zero fit; bank-all overflows 0.948191 s | prevent admission when generation is not binding or stressed cost does not fit | replace gate with bank-all: at least one replay-control overage must occur |

The contribution claim, if confirmed, is only the paired end-to-end score gain
under the stated generation-binding constraint with zero control regressions.
It is not "we combined inventory and a gate."

## Mechanistic chain

1. A probe target interaction has already consumed generation time.
2. A successful probe trace proves only that the exact candidate fired in that
   public-generation episode; it does not prove private replay success.
3. Discarding the candidate sets its possible returned raw to zero.
4. When generation is binding, no further fill candidate can be generated, so a
   preserved successful probe can add positive raw without another target call.
5. Replay and candidate capacity remain real costs. The eligibility and packing
   checks must pass under the stress factor before the probe may be appended.
6. If either capacity is binding, the rule returns the incumbent exactly.

The controlled causal claim is limited to this policy intervention on fixed
traces. The live competition claim is predictive: DBER may improve score only
when its runtime eligibility conditions occur and supplemental probes transfer.

## Assumptions and validity domains

1. **Trace validity:** `q(p)>0` is computed from the official SDK trace for the
   exact candidate. Valid only for the public-generation episode; private
   transfer is not assumed.
2. **Cost comparability:** generation episode elapsed time is the incumbent's
   replay-cost surrogate. Valid only under the same model, candidate, tool-hop
   limit, and hardware regime. `alpha=2.0` is a stress test, not a calibrated
   probability bound.
3. **No additional generation:** DBER appends stored candidates without calling
   the target again. Any implementation that replays during generation violates
   the hypothesis.
4. **Stable candidate identity:** stored message tuples reconstruct the exact
   probe candidate. Any serialization mismatch is a hard failure.
5. **Positive raw under replay:** local confirmatory profiles use deterministic
   agents so a previously successful exact probe remains successful. This
   assumption is not projected onto Kaggle; live benefit remains uncertain.
6. **Binding classification:** terminal reasons are recorded from the actual loop
   condition, not inferred afterward from rounded debug values.
7. **Scope:** conclusions apply to resource regimes represented by the fixed
   controlled profiles. They do not establish prevalence across target models.

## Fixed bias surface

1. **Selection:** run03 selected the direction, so confirmatory profiles must be
   new, fully enumerated before implementation results, and all reported.
2. **Confounding:** target calls, traces, base candidates, route, and budgets are
   paired and fixed; the only contrast is output admission. More returned
   candidates are the intended mechanism, not an uncontrolled difference.
3. **Allocation/assignment:** both policies operate on the same profile and
   exact inventory; no profile is assigned to only one policy.
4. **Protocol deviation:** config, predictions, immutable SDK paths, command,
   inputs, and output schema are hash-bound before execution; any mismatch fails
   the unit.
5. **Missing data:** crashes, missing traces, serialization failures, and binding
   mismatches remain ledger rows and cannot be dropped or replaced.
6. **Measurement:** official SDK predicate and scorer implementations compute
   raw; an independent verifier recomputes caps, prefix identity, provenance, and
   raw from artifacts.
7. **Analysis flexibility:** one primary mean, one 10% threshold, three fixed
   units, and exact zero-overage/identity gates are frozen; no post-hoc subgroup
   becomes primary.
8. **Selective reporting:** incumbent, DBER, bank-all, all generation profiles,
   both negative-control families, crashes, and all secondary metrics are
   recorded in `results.tsv`.

## Failure modes and decision boundaries

### Refute

- mean paired generation-profile gain `<10%`;
- any generation profile regresses;
- any replay/candidate overage;
- any incumbent-prefix or supplement-provenance mismatch;
- DBER changes output in a replay- or candidate-binding negative control;
- bank-all does not fail any replay-binding control, eliminating the
  distinguishing resource-gate prediction; or
- implementation requires changing target calls, route, prompts, or evaluator.

### Inconclusive

- a preregistered profile does not enter its declared binding regime because of
  timing drift, provided it remains in the ledger and no replacement is run
  without a new preregistration;
- the controlled result passes but Kaggle runtime never activates DBER; this is
  a no-op live outcome, not mechanism confirmation or refutation.

### Live safety / confidence failure

Even a locally confirmed DBER is not submission-ready unless:

1. source compliance and immutable-evaluator diffs pass;
2. a sterile code review confirms no target-call, route, prompt, prefix, or
   fallback change;
3. replay/candidate bounds pass under `alpha=2.0` and explicit negative controls;
4. both notebook copies rebuild identically from the reviewed attack;
5. the Kaggle commit run completes on the required machine shape; and
6. the pre-submission checklist records that the only positive expectation comes
   from runtime-observed successful probes and generation binding, while no-op is
   possible and private transfer remains uncertain.

A commit run does not supply hidden competition-rerun telemetry. It proves
packaging/mechanics only. A public submission, if later authorized by the
confidence checklist, remains tuning evidence rather than private/final proof.

## Taxonomy and anti-stacking

Classification:

```text
(Resource Bottleneck, Artifact/System, decouple)
```

DBER decouples a probe's measurement role from mandatory discard. It is not
Bridge Opportunity × Synthesis/Unification and does not integrate attack
techniques. The nearest simpler alternative is bank-all. The replay profile
distinguishes them: bank-all overflows while DBER must be a no-op.

Distinguishing predictions not made by a plain combination:

1. gain occurs in generation-binding profiles;
2. exact no-op occurs in replay- and candidate-binding profiles; and
3. bank-all violates at least one replay control.

## Occam and alternatives

- **Return every successful probe:** simpler but refuted by the measured
  `0.948191 s` replay overflow.
- **Reduce probe count:** may save generation time but can change template
  selection and target evidence; it is a different, less identified dimension.
- **Generate more fill:** impossible after generation is binding without changing
  the controller's safety condition.
- **Change message structure:** already searched and does not recover successful
  candidates paid for under the current structure.
- **Optimize a full knapsack:** unnecessary. Deterministic density order with
  hard caps is sufficient for the falsifiable local claim.

## Self-critique

The strongest objection is target prevalence: controlled profiles show that
salvage can matter, not that the live `81.225` runs are generation-bound with
transferable probes. The hypothesis therefore does not claim a Kaggle gain
before a live submission. Its value is that activation is conditioned on
runtime evidence and otherwise preserves the incumbent.

The second objection is the uncalibrated `alpha=2.0`. This is deliberately
described as a stress factor, not a probability bound. It can support controlled
non-overage and a conservative engineering decision, but not the
`PROBLEM.md` replay-tail construct by itself. The live confidence gate remains
responsible for that limitation.

The core claim is falsifiable, changes one dimension, and serves the problem:
confirming it would show that the source-compliant allocation policy can recover
valid score already paid for during generation without weakening replay or
candidate bounds in its stated operating regime.

## Review boundary

This file becomes immutable when the theory review is dispatched. No experiment,
attack edit, Kaggle mutation, or submission has been performed for the frozen
hypothesis.
