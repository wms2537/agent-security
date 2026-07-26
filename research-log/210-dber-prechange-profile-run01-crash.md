# T083 — DBER pre-change profile run01 crash

**Date:** 2026-07-26 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 6/6 · **Status:** failed implementation attempt 1/3

## Context

T083 froze three DBER pre-change resource regimes and their prediction-ledger
rows before execution at commit `ddf7178`.

## Execution

The exact first line of `artifacts/dber/run01/run.log` is:

```text
PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/dber_profile.py --out-dir artifacts/dber/run01
```

The run did not enter the first regime. It ended with:

```text
RuntimeError: generation_limited: episodes=0 < prefill=1
```

The attack debug preceding the exception reports zero probes and the five-item
emergency fallback. The cause is deterministic: the production controller
initializes `slowest = 1.0`, and `time_left()` requires
`now + slowest*1.3 < generation_deadline`. The preregistered
`time_budget_s=1.30` with a `0.05 s` margin can never satisfy that condition.

## Prediction vs. reality

No DBER prediction was tested. The harness timescale was invalid before the
first target interaction. All three run01 ledger rows are therefore `crash` with
`metric_value=NA`; they cannot seed or confirm the hypothesis.

## Decision

Mark T083 failed as an implementation attempt, not a scientific refutation.
Open T084 as the first allowed retry. The retry must preserve the attack SHA,
controller configuration, resource-order predictions, metrics, and thresholds,
but scale the time budgets above the incumbent's one-second initial safety
sentinel. It receives new prediction rows and a new artifact directory before
execution.

No attack edit, Kaggle mutation, or submission occurred.

## Problem alignment

Failing closed preserves the competition evidence chain: a harness that never
ran cannot be used to justify a candidate or consume a Kaggle submission.
