# PROBLEM.md — Cycle 3: evidence-gated Kaggle competition optimization

**Supersedes:** the Cycle-2 orchestration-security anchor, closed by
`research-log/112-iphe-primary-audit-and-portfolio-closure.md` and the mandatory
retrospective at `research-log/113-cycle2-retrospective.md`. Git history through
commit `8714318` preserves that anchor.

**Status:** Phase-0a problem anchor; the exact method remains under ideation.

**User direction and authorization:**

> now i authosired all kaggle actions, go and play around with it. but with one
> consideration, only submit when you are confident on the solution. we should
> ibnovate , be creative, do the research properly, think properly using the
> sciagent skill

This authorizes Kaggle reads, notebook pulls, pushes, commit runs, output/log
retrieval, leaderboard inspection, and competition submission. It does not make
submission automatic: a submission is permitted only after the confidence gate
below passes on recorded evidence.

## Primary outcome and delivery order

**Primary outcome:** maximize the final competition score and rank with a
source-compliant, replay-safe solution.

**Active track:** competition systems optimization.

**Delivery order:** recover real evaluator evidence → identify a measured
bottleneck → preregister one structural change → locally verify → obtain a
Kaggle commit-run measurement → submit only when the confidence gate passes →
analyze the leaderboard signal. Academic packaging is downstream and cannot
replace competition evidence.

## Core question

Which source-compliant candidate-generation and allocation policy maximizes
expected competition score across the evaluated model/guardrail cells without
voiding the submission through generation or replay timeout?

## Who has this problem and why it matters

The competition rewards findings that survive a remote generation-and-replay
pipeline across heterogeneous models and guardrails. The local optimizer must
trade off finding severity, cross-cell reliability, novelty, returned-candidate
count, and replay cost under a hard time budget. A locally impressive portfolio
that times out, fails parser/tool semantics, or transfers to only one public
mock cell loses.

## Why current approaches fall short

The recorded competition history is strongly miscalibrated:

- equal round-robin scored `56.76` versus `66` predicted;
- the multi-post/reserve/hedge design scored `36.705` versus approximately `85`;
- the simplified single-post rebuild improved to `69.570` but did not establish
  a winning design; and
- the competition rerun log needed for per-model template and latency diagnosis
  was not previously recovered.

Mock mechanics prove that code executes and scores under declared local rules.
They do not identify target-model response rates, private-guardrail transfer,
remote latency tails, or the current leaderboard frontier.

## What success looks like

Phase 0a must recover the current competition state and produce genuinely
distinct candidate directions with reproducible baselines. The selected
direction must then satisfy all of the following before submission:

1. **Source/rule compliance:** exact current competition rules and SDK/source
   constraints are recorded; the candidate passes static compliance checks.
2. **Mechanical correctness:** required output, parser, tool-call, replay, cell
   identity, and scoring invariants pass deterministic tests.
3. **Resource safety:** measured generation and per-finding replay costs support
   an explicit tail-risk bound below the remote deadline, not an arbitrary
   margin.
4. **Structural evidence:** the change targets a measured bottleneck and has a
   prediction that differs from the incumbent; each added component has an
   ablation or is removed.
5. **Regression control:** the incumbent behavior remains available as a
   fallback, and local tests show no loss on already-proven mechanics.
6. **Target-derived evidence:** a Kaggle commit run or other competition-owned
   feedback supports the candidate's assumed behavior. Mock-only improvement is
   insufficient for confidence.
7. **Submission decision:** the expected benefit over the recorded best public
   score `69.570` is positive after uncertainty and timeout risk; the exact
   checklist and decision are committed before submission.

Winning remains the objective. Because the current leaderboard, deadline, daily
submission quota, and scoring surface may have changed, exact rank/score targets
are pending the authorized live-state audit.

## Authorization and non-goals

- All Kaggle competition actions are authorized, subject to official rules and
  the confidence-before-submission condition.
- Do not expose credentials, tokens, cookies, private competition data, or
  other participants' non-public work in logs or commits.
- Do not target systems, accounts, or data outside the competition sandbox.
- Do not perform destructive actions or release an operational payload outside
  the authorized competition artifact.
- Do not claim that a public-leaderboard gain guarantees private/final transfer.
- Do not write a paper as a substitute for an unmeasured competition result.

## Proxy caveat

Local mock score and mechanics are proxies for remote validity and resource
safety. Kaggle public score is a tuning signal and may overfit the public cells;
final/private score and rank are the primary outcome. Improving a mock score by
weakening replay realism, changing evaluator semantics, leaking target details,
or increasing timeout risk is failure.

## Question type

Predictive systems optimization under a fixed competition contract. Causal
claims are limited to controlled local ablations; leaderboard deltas are noisy
external interventions unless the competition exposes a paired evaluation.

## Construct table

| Construct | Operational definition | Observable indicator | Unacceptable proxy |
|---|---|---|---|
| Valid finding | A returned candidate that passes current competition parsing, replay, guardrail and scoring semantics | Remote accepted/scored finding plus exact local mechanics match | Locally emitted JSON or a mock-only positive |
| Portfolio value | Sum of competition scoring contributions across evaluated cells, net of invalidation/timeout risk | Official public/final score; cell telemetry when exposed | Severity sum on one mock cell |
| Cross-cell reliability | Probability a candidate remains valid and effective across the evaluated model/guardrail cells | Per-cell remote outcomes or a preregistered conservative estimator | One model response or public guardrail alone |
| Replay safety | The complete returned set can be replayed within the remote deadline with acceptable void risk | Measured cost distribution and explicit tail bound; completed remote run | Mean latency or observed maximum plus arbitrary margin |
| Structural innovation | A change replacing/decoupling/formalizing a measured bottleneck with a distinguishing prediction | Pre-change profile, preregistered prediction, ablation, and remote signal | Adding more templates or techniques without attribution |
| Submission confidence | All seven success gates above pass on committed evidence before submission | Machine-checkable checklist with PASS and evidence paths | Intuition, mock score alone, or a successful notebook commit |
