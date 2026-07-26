# SCOC-32 Phase-0 evaluation contract

**Version:** scoc32-c3-v1
**Recorded:** 2026-07-23
**Scope:** Phase-0 bridge formalization before any Kaggle mutation.

## Signal tiers

- **Source-compatible control tier:** public notebook-derived mechanism classes only.
  Used only to close control reconstruction and mechanism distinction; not used for target score inference.
- **Target-derived tier:** immutable target-envelope metadata from authorized live or commit artifacts.
  Used only for transferability and confidence bridge before any submission.
- **Submission tier:** full confidence gate with all controls and target evidence active.

## Primary phase-0 metric definitions

Exact competition scoring primitives are:

- full single message raw: `R_full_single(m) = 18m`
- full chain raw: `R_chain_full(m) = 16m + 2`
- compact chain raw (single message compact baseline): `R_chain_compact(m) = 16m + 2` (same raw algebra under exact event model, different control semantics)

Core comparison is exact raw per second:

```
raw_per_sec = exact_raw / measured_wall_seconds
```

Coverage is required as exact complete-event overlap on official scoring predicates:

- coverage for each mechanism must be measured against `SINGLE_FULL`,
- `CHAIN_SCOC` must hold `coverage ≥ 0.95` to be compared on raw/sec.

## Required comparisons (fixed)

The bridge decision uses exactly these mechanisms at fixed URL set and fixed candidate cap:

- `SINGLE_FULL`
- `CHAIN_FULL`
- `CHAIN_COMPACT_EXPLICIT`
- `CHAIN_SCOC`
- `CHAIN_GENERIC`
- `CHAIN_BLOCKED_ANCHOR`
- `COLD_OPERAND_ONLY`

## Bridge equations

- `ratio_raw(m) = (16m + 2) / (18m)`
- incumbent complete-policy win condition:

`T_chain(m) / T_single(m) <= (16m + 2) / (18m * 1.584519189306)`

- at `m=32`, incumbent bridge requires:

`T_chain(32) / T_single(32) <= 0.563174694970`

- source-only 1.25x bridge against `89.455` requires the chain to beat:

`T_chain(32) / T_single(32) <= 0.724145354873`

## Validity checks

- all mechanism semantics must keep identical tool payload and stop semantics unless explicitly in scope (no selector, no compiler, no private-lane invention).
- no chain can be charged success in `SINGLE_FULL`-equivalent syntax if it requires a different template or different candidate domain.
- `COLD_OPERAND_ONLY` and `CHAIN_BLOCKED_ANCHOR` must be in the comparison set; either beating SCOC without a mechanistic distinction is immediate fail for SCOC contribution.
- all comparisons are disallowed if exact per-turn event coverage falls below threshold.

## Failure and retirement policy

- if source-compatible control above `88.188` cannot be reproduced, Phase-0 retirement is immediate;
- if any control collapses coverage or beats SCOC with no distinct boundary, the direction retires in Phase-0;
- if target-envelope capture cannot be pinned to immutable logs and configuration, no transfer claim.

## Submission boundary

- this contract does not authorize submission.
- submission requires the submission-confidence gate from `PROBLEM.md` and an explicitly open authorization record in `state.json`.
