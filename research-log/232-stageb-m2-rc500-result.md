# Stage B exact full-repeat M=2 result

**Date:** 2026-07-31 · **Phase:** 2/4 competition track · **Cycle:** 3 · **Iteration:** 7 · **Status:** completed, disconfirmed

## Context

The fast-bank single-post control returned a public score of `81.000` at
`return_count=900` (ref `55123657`) and a blank score at `return_count=1000`
(ref `55123706`). The next structural hypothesis tested whether two complete
tool-call messages per candidate could amortise candidate-level replay work and
raise score density. The experiment kept the fast-bank selector, direct server
shape, fixed fill, unique destinations, and no generation-side fill
verification. Only candidate message multiplicity changed from one to two.

## Prediction vs. reality

**Pre-run prediction:** with 500 candidates and both messages firing, the source
scorer's `16*M+2` raw model predicted approximately
`500 * 0.09 * 34/18 = 85.000`, above the historical `81.225` incumbent while
remaining below the observed single-post high-side boundary.

**Observed:** the Kaggle API reports:

```text
55134050 ... SubmissionStatus.COMPLETE ... publicScore=, privateScore=
```

The kernel commit output was independently checked before submission: both
notebook copies were rebuilt from the same attack source, `submission.csv` had
the required `Id,Score` header and five placeholder rows, and the notebook used
`JEDAttackInferenceServer().serve()` with `return_count=500` and
`messages_per_candidate=2`. Therefore the result is a remote replay/gateway
failure or invalidation, not a locally reproducible submission-format error.

## Interpretation

The hypothesis is disconfirmed as a competitive first density path at this
count. The result does **not** prove that every multi-event candidate is
invalid: the tested shape creates 1,000 complete user messages, and the hidden
evaluator may reject, time out, or abort on that message volume before exposing
a score. The earlier `rc900` success establishes a useful control boundary for
single-post candidates; the blank v32 run establishes that exact two-message
repetition is not safely transferable at `500x2`.

The shorter completion time of the blank run is compatible with an early hidden
abort: a successful run must complete the full evaluated portfolio, whereas a
gateway or replay failure can terminate on the first failing model/guardrail
path. This is an inference from the status pattern, not episode telemetry.

## Decision

Retire exact full-repeat M=2 at `500x2` as a submission candidate. Do not lower
the count blindly: a lower-count M=2 run would only be useful as a diagnostic
boundary experiment and is unlikely to establish a score above the incumbent.
The next structural candidate, if authorized as a fresh iteration, is a single
user message containing two explicit complete `http.post` calls. It preserves
one replayed user turn per candidate while testing whether event density can
increase without the 2x user-message construction cost. It must first pass
source inspection, local exact-event accounting, and a conservative low-count
remote control before any `>100` count is attempted.

## Gate check

- Remote status command: `comp/.venv/bin/kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v | head -n 12` → ref `55134050` is `SubmissionStatus.COMPLETE` with blank scores.
- Ledger update: `competition/leaderboard_experiments.tsv` row `55134050` → `complete_blank_score_m2_rc500_remote_replay_or_gateway_failure`.
- Local artifact contract: the pre-submit kernel output contained a schema-valid `submission.csv`; no source-format mutation occurred after the validated build.

## Problem alignment

This result directly tests the core question's trade-off between candidate
event density and remote replay validity, and removes one structurally risky
candidate shape from the competition portfolio without confusing a blank
remote result with a local format defect.

## Next steps

Freeze this negative result. Inspect the evaluator's source-level event and
candidate semantics, then preregister one single-message two-call hypothesis
with an explicit prediction and stop condition before implementation or
submission.
