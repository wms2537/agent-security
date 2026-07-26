# T067 — SCOC-32 Phase-1 hypothesis freeze and anti-stacking lock

**Date:** 2026-07-23 · **Phase:** 1 · **Cycle:** 3 · **Iteration:** 5/5 · **Status:** theory-review-ready, anti-stacking locked

**Supersedes:** `research-log/190-scoc32-phase1-decision-archaeology-and-anti-stacking.md`.

**Frozen contracts:** `research-log/189-scoc32-phase0-problem-and-winning-bridge.md` and `experiments/configs/scoc32-c3-phase0-contract.json` (as immutable Phase-0 boundaries).

## 1) Why this freeze is needed

The Phase-1 contract must freeze one narrow claim and reject all equivalent non-boundary gains before implementation or Kaggle action.

- The strongest audited public association remains an unattributed source control at `89.455`.
- To beat the incumbent `69.570`, a complete-policy transfer claim requires either:
  - `m32` raw/sec ratio against the incumbent `T_chain/T_single <= 0.563174694970`, or
  - source-compatible control bridge above `88.188` for a transfer gate.
- `CHAIN_SCOC` is therefore only meaningful if it preserves exact output semantics and beats fixed-length baselines under exact overlap.
- `COLD_OPERAND_ONLY` and `CHAIN_BLOCKED_ANCHOR` are required anti-stack sentinels; each can invalidate contribution credit if they dominate SCOC.
- Taxonomy: `Resource Bottleneck` × `Artifact/System` with core operation `replace` (state-aware continuation replacing full-repeat replay).

## 2) One-sentence primary hypothesis (frozen)

**SCOC-32:** On a fixed template class and fixed payload syntax, replacing repeated full instruction replay with an exact successful anchor plus destination-only operands for later turns (`CHAIN_SCOC`) must beat `CHAIN_FULL` in exact-event coverage-constrained raw/sec at the same chain length, and must not be reducible to a short-message or blocked-anchor artifact.

## 3) Frozen comparison set (anti-stacking locked)

These are the only admissible baseline/control mechanisms for Phase-1:

- `SINGLE_FULL`
- `CHAIN_FULL`
- `CHAIN_COMPACT_EXPLICIT`
- `CHAIN_SCOC`
- `CHAIN_GENERIC`
- `CHAIN_BLOCKED_ANCHOR`
- `COLD_OPERAND_ONLY`

No additional mechanism-level component may be added to the SCOC claim (no selector learning, no harness changes, no new compiler, no private evaluator adaptation) until the Phase-1 and Phase-2 gates close.

### 3.1 Exact chain primitives (reproducible definitions)

- Message length `m` is evaluated on the frozen support set:
  `m ∈ M = {1,4,8,16,24,32}` with integer chain length and fixed candidate cap.
- `SINGLE_FULL`: one full-instruction message with fixed template class, fixed payload normalization, fixed tool path, and fixed stopping condition.
- `CHAIN_FULL`: `m` full-instruction turns using full payload syntax each turn under identical URL set and stop condition.
- `CHAIN_COMPACT_EXPLICIT`: one-shot compact syntax chain where each turn keeps explicit destination semantics; short-message form is in scope only as fixed-length syntax ablation and is counted with `R_compact = 16m + 2`.
- `CHAIN_SCOC`: `CHAIN_FULL` with exact successful anchor conditioning: first turn must be a successful exact anchor, subsequent `m-1` turns may use destination-only operands under the same stop condition.
- `CHAIN_GENERIC`: generic shorthand chain with no explicit anchor-success conditioning and no additional per-turn destination-only state requirement, with raw budget `R_generic = 16m + 2` under the exact-event model.
- `CHAIN_BLOCKED_ANCHOR`: same as `CHAIN_SCOC` except the first anchor path is non-empty and blocked before continuation.
- `COLD_OPERAND_ONLY`: destination-only operand continuation without any prior exact successful anchor (same chain length and tool path as `CHAIN_SCOC`).

## 4) Required falsification map (all arms must be logged)

1. **SCOC-vs-Full contrast:** `CHAIN_SCOC` must exceed `CHAIN_FULL` raw/sec under exact-event coverage versus `SINGLE_FULL`.
2. **Compact-ablation contrast:** `CHAIN_COMPACT_EXPLICIT` must be tested as the one-shot syntax ablation.
   - If it is not worse than SCOC, SCOC loses novelty.
3. **Generic-control contrast:** `CHAIN_GENERIC` must be measured under fixed `m`, identical payload normalization, and identical stop condition.
   - If it dominates SCOC, then SCOC is parsimoniously reclassified as generic syntax compression.
4. **Blocked-anchor contrast:** `CHAIN_BLOCKED_ANCHOR` must be measured.
   - If it beats SCOC with equal/equivalent payload and stop semantics, SCOC loses to blocked-replay behavior.
5. **Cold-operand contrast:** `COLD_OPERAND_ONLY` must remain near-zero coverage.
   - Any nonzero sustained retained raw indicates mechanistic leakage and invalidates contribution credit.

## 5) Frozen success/failure gates

- **Coverage gate (global):** `coverage(arm, SINGLE_FULL) >= 0.95` required before any ratio or win claim.
- **Contribution gate:** SCOC is competitive only if every other admissible control above fails on the frozen comparison map or is mechanically dominated.
- **Mechanism gate:** contribution is only `anchor+destination_operands`; any short-message-only improvement or selector adaptation is out-of-contract.
- **Transfer boundary gate:** source-competent control must be reconstructed at raw-score `>= 88.188` (or complete-policy bridge-to-incumbent ratio at `>=1.584519189306`), otherwise `T067` is retired before Phase-2.

## 6) Formal quantities (frozen)

- Single full raw: `R_single = 18*m`.
- `CHAIN_FULL` raw: `R_full_chain = 18*m`.
- `CHAIN_SCOC` raw: `R_scoC = 16*m + 2`.
- `CHAIN_COMPACT_EXPLICIT` raw: `R_compact = 16*m + 2` under the exact-event model.
- `CHAIN_GENERIC` raw: `R_generic = 16*m + 2` under the exact-event model.
- Candidate ratio at length `m`: `R_scoC/R_single` where `R_single = 18*m`.
- Exact coverage ratio requires the canonical overlap operator:

  `cov(arm) = |O_arm(m) ∩ O_single(m)| / |O_single(m)|`,

  where `O_x(m)` is the exact ordered set of accepted final tool events for mechanism `x`, at chain length `m`, filtered by:
  - exact URL set,
  - normalized payload bytes (canonical JSON key order, literal whitespace stripping for tool arguments),
  - exact chain metadata (`m`, turn index, stop status, and replay index),
  - exact success status.
- Raw/sec comparison for SCOC only when `cov(SCOC) >= 0.95`.

- Invalidity regimes (`VALID` must hold for comparison):
  - `m ∈ M`,
  - fixed template class and payload family are identical across all arms,
  - no selector changes, no harness mutation, no evaluator adaptation,
  - first successful anchor and stop semantics are explicit and identical across arms when applicable,
  - non-delivery/exception turns are excluded from accepted-event numerators and denominators unless they are shared under identical predicates.

## 7) Anti-stacking contract (binding)

This contract forbids mechanism credit from any pair of the above that fails mechanistic separation:

- If `CHAIN_COMPACT_EXPLICIT == CHAIN_SCOC` on fixed `m`, fixed normalized payload, fixed chain domain, fixed stop semantics, and coverage, then only one message-control claim survives and SCOC contribution is zero.
- If `CHAIN_BLOCKED_ANCHOR >= CHAIN_SCOC` on the same frozen comparators, the result is replay-block behavior, not anchor-conditioned continuation.
- If `COLD_OPERAND_ONLY > 0` and survives fixed-coverage checks, the SCOC mechanism is classified as control leakage.
- If `CHAIN_GENERIC >= CHAIN_SCOC` on the same frozen comparators, parser-compression/canonicalization (without anchor-conditioned state transfer) is treated as the primary mechanism and SCOC is retracted.

Canonicalization-only retraction is triggered when:

- `CHAIN_COMPACT_EXPLICIT` and `CHAIN_SCOC` are indistinguishable on `(m, coverage, raw/sec)` and
- payload/signature overlap and endpoint checks are identical under identical `stop` and anchor predicates.

This lock is recorded before any theory-review dispatch as the default anti-stacking disposition.

## 8) Implementation non-goals for Phase-1

- no new harness architecture,
- no evaluator targeting,
- no private telemetry inference,
- no live benchmark generation outside a target-confidence gate.

## 9) Machine-readable close

```text
t067_scoc32_hypothesis_lock=PASS anti_stacking_controls=CHAIN_COMPACT_EXPLICIT|CHAIN_GENERIC|CHAIN_BLOCKED_ANCHOR|COLD_OPERAND_ONLY comparison_set=7 core=anchor-conditioned-destination-operands contract=single-success-then-operands transfer_gate_source_control=88.188 transfer_gate_incumbent=1.584519189306 coverage_gate=0.95 parent=T066 phase=1 next_task=T068 implementation=false kaggle_mutation=false submission=false results_immutable=true attack_immutable=true
```
