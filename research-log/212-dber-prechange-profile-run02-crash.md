# T084 — DBER pre-change profile run02 crash

**Date:** 2026-07-26 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 6/6 · **Status:** failed implementation attempt 2/3

## Context

Run02 changed only the generation-limited timescale from `1.30 s` to `2.00 s`
and froze new predictions at commit `002f07d`.

## Execution

The command-first log at `artifacts/dber/run02/run.log` ends:

```text
RuntimeError: generation_limited: 5 returned signatures lack trace rows
```

The attack did execute 17 recorded single probes, but returned the five-item
emergency fallback without executing those candidates. The profile correctly
refused to invent replay costs for returned signatures absent from its trace.

The deterministic cause refines run01's diagnosis: the controller initializes
`slowest=1.0` and updates it with `max(slowest, dt)`, so it remains at least one
second for the whole run. `time_left()` therefore preserves a fixed `1.3 s`
reserve at every phase. After the probe schedule, a two-second generation budget
has insufficient remaining time to enter verified fill.

## Prediction vs. reality

No salvage comparison was computed. The partial probe execution is diagnostic
harness evidence only. All run02 rows remain metric `NA` and become `crash`;
they do not confirm or disconfirm DBER.

## Decision

Open T085 as the third and final allowed profile attempt. Preserve every
controller, replay, candidate, binding, metric, and threshold setting; change
only the generation-limited budget from `2.00 s` to `4.00 s`. This provides
`2.65 s` above the permanent reserve and margin, enough for the frozen probe
schedule plus verified fill in the measured mock regime.

If run03 still fails to produce a valid profile, retire DBER as
implementation-defeated for this iteration. No attack edit or Kaggle action
occurred.

## Problem alignment

Refusing untraced emergency candidates prevents an apparent salvage opportunity
from being manufactured by the profiler itself.
