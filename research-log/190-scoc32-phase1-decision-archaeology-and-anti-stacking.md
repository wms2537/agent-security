# T066 — SCOC-32 phase transition and anti-stacking archaeology

**Date:** 2026-07-23 · **Phase:** 1 · **Cycle:** 3 · **Iteration:** 5 · **Status:** completed
**Hypothesis:** scoc32

## 1) Phase transition summary

`T066` closes Phase-0 into a decision-ready Phase-1 state for SCOC-32.
No implementation, theory-review dispatch, or Kaggle mutation is used in this task.

The governing boundary from `research-log/189` remains active:

- `SINGLE_FULL` is the exact comparison floor.
- `CHAIN_FULL`, `CHAIN_COMPACT_EXPLICIT`, `CHAIN_SCOC`, `CHAIN_GENERIC`,
  `CHAIN_BLOCKED_ANCHOR`, and `COLD_OPERAND_ONLY` are the non-composable boundary
  components for the chain mechanism.
- complete-policy bridge remains `1.584519189306` incumbent ratio or a source-compatible
  control `>88.188` to keep a competition-relevant claim.

## 2) Decision archaeology

### A. Confirmed accepted inputs from Phase-0 and prior evidence

- The **strongest audited public-source association** remains an author/source
  association at `89.455`; score attribution is unavailable.
- the incumbent target artifact is still `69.570` and the live leader is still `110.235`.
- exact scorer algebra (`16m+2` vs `18m`, novelty penalty, EXFIL 16 raw / one-cell 2 raw)
  is retained as a non-negotiable mechanism anchor.
- 2026 literature support for response-conditioned continuation exists (Adaptive
  Adversaries, Prompt Injection as Role Confusion, AgentLAB), but no source reviewed
  artifact demonstrates the full multi-message chain mechanism as both exact and winning.

### B. Non-goals retained from archaeology

1. **No short-message trick-only hypothesis**
   A generic compact wording baseline without anchor semantics is explicitly
   excluded. If `CHAIN_COMPACT_EXPLICIT` or `CHAIN_GENERIC` equals or beats `CHAIN_SCOC`
   under fixed message count and raw/sec accounting, SCOC gets no contribution.

2. **No private-only transfer oracle**
   A hidden private branch has no attributed target mechanism, thus cannot form
   `c89` control in this phase.

3. **No immediate scope stacking**
   SCOC is not combined with selector training, private evaluator adaptation,
   multi-agent orchestration, or a new template compiler before the core
   mechanism survives the boundary checks.

## 3) SCOC-32 anti-stacking map (owned component map)

### 3.1 Core contribution (narrowed)

- **replace** `full instruction repeat` with **response-conditioned operand continuation**
  while preserving full payload/stop semantics.

### 3.2 Borrowed but non-contributing base

- candidate selection mechanism (fixed or pre-chosen in this phase),
- replay ledger mechanics,
- submission workflow,
- existing `CHAIN_COMPACT_EXPLICIT`/cold/anchor-ablation syntax.

### 3.3 Required falsification pair (distinct tests)

- `CHAIN_SCOC` must beat `CHAIN_FULL` at target message lengths on both:
  - exact raw/sec,
  - exact-event coverage versus `SINGLE_FULL`.
- `CHAIN_COMPACT_EXPLICIT` must be tested as a one-syntax ablation.
  - If it matches SCOC with no anchor effect, SCOC receives no novelty credit.
- `CHAIN_BLOCKED_ANCHOR` must be measured.
  - If blocked-anchor survives better than SCOC, the claim is blocked-replay behavior,
    not success-conditioned composition.
- `COLD_OPERAND_ONLY` must remain near-zero baseline.
  - Any positive retained value in this arm is a boundary failure for mechanism credit.

### 3.4 Distinct failure signature expected

If SCOC only improves by token-count reduction while exact-event coverage drops or
the chain collapses under anchor block, the mechanism is reclassified to
`compression+short-hand` and dropped from this direction.

## 4) Required next-step gates for hypothesis entry

Before moving to `T067`, the following must remain true in the next state:

1. no scored transfer claim without a complete-policy `t065` bridge check,
2. no private-replay-only control claim without explicit target evidence,
3. no mechanism credit without the four-arm controlled contrast,
4. no candidate tree changes before anti-stacking holds (`CHAIN_FULL` baseline,
   `CHAIN_COMPACT_EXPLICIT` ablation, `CHAIN_BLOCKED_ANCHOR`, `COLD_OPERAND_ONLY`).

## 5) Phase-1 closeout

- This task is passed as a decision archaeology checkpoint.
- `SCOC-32` remains the only active direction entering the hypothesis-formulation task.
- `T067` is opened as the next Phase-1 technical task:
  freeze the formal hypothesis contract and anti-stacking-locked contribution claim.

## 6) Machine-readable close

```text
t066_scoc32_decision_archaeology=PASS accepted=1.25x_bridge_boundary_only control_unattributed_89=accepted unresolved=source_control_gap parent=T065 next_task=T067 phase=1
```
