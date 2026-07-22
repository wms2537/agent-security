# Calibrated MPC-24 theory review round 5 dispatch

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** dispatched

## Context

V5 passed deterministic author verification and is frozen at commit `c7f20ee`.
Per SciAgent accounting, Cycle-3 hypothesis-review usage is charged from `4/12`
to `5/12` at dispatch, regardless of verdict.

## Immutable target

- artifact: `research-log/136-hypothesis-iter-5-mpc24-calibrated.md`;
- commit: `c7f20ee`;
- committed lines: `640`;
- SHA-256:
  `ddd18c6c264e45c029c16e6649c1a86b0a225832168f560a01c624eefed11441`;
- claim type: engineering;
- question type: predictive;
- escalation constraint: none.

## Previous issues supplied for disposition

1. Repair the replay-cost model and re-evaluate actual MPC with the exact online
   proxy; v4's scalar 1.10 contradicted measured pairs and its 1.507 ratio used
   oracle replay cost.
2. Make the controller total and implementation-unique, including the
   24-eligible/8-ineligible edge and observable sequential admission.
3. Supply measured per-component evidence and frozen ablations with exact
   metrics and decision thresholds.
4. Bind measurement provenance completely: generating commit/environment,
   runner/config, SDK, fixtures, guardrail and mock agents.
5. Give the official-score prediction an evidential bridge or narrow it.
6. Operationalize validity/rejection regimes for sentinel-to-fill dependence,
   replay transfer, ledger safety and drift.

The reviewer must label every item `RESOLVED`, `IMPROVED`, `UNCHANGED`, or
`WORSE`, then inspect for new defects.

## Gate Check

- Author checker: PASS in research-log/137.
- Review budget: `5/12` spent at dispatch.
- Phase 3, attack implementation and Kaggle mutation remain closed pending a
  valid `RIGOROUS` verdict.

## Problem alignment

This review decides whether the repaired, controlled hypothesis is sufficiently
total, calibrated and independently testable to justify building the PoC rather
than defaulting immediately to fixed-8.

## Decision

Dispatch one fresh sterile reviewer and record its report verbatim before any
implementation or re-review.
