# T065 — SCOC-32 Phase-0 problem and winning-bridge formalization

**Date:** 2026-07-23
**Phase:** 0
**Cycle:** 3
**Iteration:** 5
**Status:** completed
**Hypothesis:** scoc32

## 1) Status at entry

`T065` is the SCOC-32 Phase-0 gate before any implementation, review dispatch, or Kaggle mutation. The objective is to make every Phase-0 contract claim measurable and irreversible:

- rebuild a non-attributed source-compatible control class;
- separate exact raw-cost from token-length intuition;
- define a winner bridge that can actually clear a final-score target; and
- pin fixed failure gates before moving to `P1`.

## 2) Benchmark geometry and hard bridge numbers

From read-only live/public evidence:

- SOTA: `110.235`
- incumbent (`Whyme` accepted artifact): `69.570`
- strongest audited public-source association: `89.455` (score attribution unavailable)

Exact ratios:

- `110.235 / 69.570 - 1 = 1.584519189306`
- `110.235 / 89.455 - 1 = 0.232295567604`
- `89.455 * 1.25 = 111.81875`
- `69.570 * 1.25 = 86.9625`
- `110.235 / 1.25 = 88.188` (minimum qualifying source-compatible control for a direct mechanism-only win claim)

From the exact competition scorer:

- one successful EXFIL event: `16` raw
- one unique score-cell: `2` raw
- one successful finding with `m` messages: `16m + 2` raw
- `m` single-message candidates: `18m` raw

and novelty ratio:

```
ratio_raw(m) = (16m + 2) / (18m)
```

for m ∈ {1,4,8,16,24,32}:

- m4: `0.9166666667`
- m8: `0.9027777778`
- m16: `0.8958333333`
- m24: `0.8935185185`
- m32: `0.8932291667`

Winning complete-policy bridge is strict:

For fixed `m`, SCOC-32 can beat incumbent only if

```
T_chain(m) / T_single(m) < (16m + 2) / (18m * 1.584519189306)
```

At m32:

- `T_chain(32) / T_single(32) ≤ 0.563174694970`

For the same chain vs source-compatible 89.455 control, `1.25x` target requires:

- `T_chain(32) / T_single(32) ≤ 0.713888888889`

For qualifying control `88.188`, `T_chain(32)/T_single(32) ≤ 0.713888888889`.

## 3) Fixed comparison matrix for Phase-0 gates

All comparisons are at fixed `m` and fixed URL set unless explicitly noted:

- `SINGLE_FULL`
  single-message full instruction chain; baseline floor.
- `CHAIN_FULL`
  full-redundant `m`-message chain (old public-style full instruction).
- `CHAIN_COMPACT_EXPLICIT`
  one-message full instruction, one-message compacted explicit destination wording.
- `CHAIN_SCOC`
  anchor success once, then destination-only chain.
- `CHAIN_GENERIC`
  generic shorthand chain with no anchor/explicit state.
- `CHAIN_BLOCKED_ANCHOR`
  chain after non-empty but explicitly blocked anchor path.
- `COLD_OPERAND_ONLY`
  pure cold start with destination-only syntax and no prior success.

Decision rules at fixed `m`:

1. `COLD_OPERAND_ONLY` is fail/anchor-fail test; any retained positive in the bridge is invalid.
2. `CHAIN_SCOC` must strictly dominate `CHAIN_FULL` raw/sec by `≥1.25x`.
3. `CHAIN_SCOC` must clear `coverage_threshold ≥ 0.95` against `SINGLE_FULL`.
4. `CHAIN_COMPACT_EXPLICIT` must be tested as an ablative baseline:
   - if coverage is near equal and `CHAIN_SCOC` fails raw/sec, no composition claim survives.
5. If `CHAIN_BLOCKED_ANCHOR` clears and `CHAIN_SCOC` does not, the mechanism explanation is a blocked anchor artifact, not chain amortization.
6. If any mechanism requires changing template grammar or selector logic, that component is outside this task and remains a charged fixed-cost arm.

## 4) Source-control reconstruction protocol

Public notebooks are source-compatible controls, not scored evidence. SCOC-32 Phase-0 uses:

- `SINGLE_FULL` as a source-compatible control family (`control_scoc32_v0`) with explicit note: no score attribution.
- one deterministic non-attributed reconstruction:
  - fixed template family,
  - same URL set,
  - same scoring call site,
  - same candidate cap and hop cap,
  - no target run data used.

Control can only be used in bridge math; if we fail to bind a source-compatible control above `88.188`, this direction retires at Phase-0.

## 5) Target-derived evidentiary boundary

No target prevalence claim is accepted from public source or local source proxies. The Phase-0 gate requires one live target-relevance evidence bundle before any claimed score transfer:

- pinned model binaries (GGUF/weights or equivalent reproducible hashes),
- fixed harness config,
- generator/replay split evidence,
- one complete run envelope with explicit `generation_cost_sec`, `replay_cost_sec`, and `void_rate`.

No live score is treated as evidence of winning unless both:

- bridge is still above the threshold above, and
- reproducible target-envelope fields are within this contract.

## 6) Hard retirement rules

Do not proceed past Phase-0 if:

- chain raw/sec advantage collapses under `COLD_OPERAND_ONLY` with equal-length controls,
- `CHAIN_SCOC` fails `COLD_OPERAND_ONLY` rejection plus `coverage ≥ 0.95`,
- anchor blocking control (`CHAIN_BLOCKED_ANCHOR`) dominates `CHAIN_SCOC`,
- source-compatible control is above `88.188` and not reproducible,
- `T_chain(32)` is not within bridge inequality above,
- target envelope is not captured with immutable, parseable traces.

`CHAIN_FULL` and `CHAIN_COMPACT_EXPLICIT` are required negative controls; if either beats SCOC under this contract without a distinct mechanistic profile, this project retires SCOC in Phase-0.

## 7) Phase transition

`T065` pass criteria are:

- honest unscored control reconstruction in source-compatible form;
- fixed comparison matrix and coverage/target definitions;
- exact bridge thresholds and retirement checks written before any implementation;
- target evidence boundary recorded with immutable inputs.

Transition is to `T066` (`P1`) only if all above checks are `PASS`.

## 8) Machine-readable close

```text
t065_scoc32_phase0_bridge=PASS c89_control=unqualified_source_control incumbent_bridge=1.584519189306 m32_max_time_ratio_inc=0.563174694970 phase_next=1 next_task=T066 implementation=false kaggle_mutation=false submission=false
```
