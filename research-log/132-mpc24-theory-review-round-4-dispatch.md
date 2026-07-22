# MPC-24 theory review round 4 dispatch

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** dispatched

## Context

The deterministic verification ladder passed for the superseding MPC-24 v4
hypothesis. Per SciAgent accounting, Cycle-3 hypothesis-review usage is charged
at dispatch time from `3/12` to `4/12`, regardless of verdict.

## Immutable review target

- artifact: `research-log/130-hypothesis-iter-4-mpc24.md`;
- artifact commit: `21c3352`;
- committed line count: `745`;
- committed SHA-256:
  `ac1592714ba28df9b740a5edb6592a0dc2e729a8d6afb5ca2aa5f4f7f48ea9e3`;
- claim type: engineering;
- question type: predictive;
- escalation constraint: none.

The dispatch uses only the sterile `prompts/theory-reviewer.md` template and
the template-authorized previous-issue list. It contains no author framing,
assurances or project learnings.

## Previous issues supplied for disposition

1. Observed extrema from two paths are not conservative future bounds; replace
   the bound language/rule with a validity-supported construction or a
   sequential rule preserving the claimed portfolio dominance.
2. Define and charge every fallback portfolio exactly, including probe/current
   prefixes, prior returns, remaining generation/replay/candidate budgets, fill
   count and value.
3. Specify the provisional joint-cap objective algebraically so conforming
   implementations cannot choose different arms.
4. Add frozen branch profiles for validation rejection, first-fill regression,
   later regression, incomplete paths, replay/candidate binding and fallback.
5. Bind the real engineering evidence directly by path, freeze commit and
   sample/summary hashes.
6. Distinguish `export_trace_dict()` trace differencing from `interact()` event
   counts and state generation-to-public-replay transfer explicitly.

The reviewer must label each `RESOLVED`, `IMPROVED`, `UNCHANGED`, or `WORSE`,
then inspect for newly introduced defects.

## Gate Check

- Deterministic author verification: PASS in research-log/131.
- Review budget: `4/12` spent at dispatch.
- Hypothesis is immutable from commit `21c3352` onward.
- Phase 3, attack implementation and Kaggle mutation remain closed pending a
  valid `RIGOROUS` verdict.

## Problem alignment

An independent hostile review is the last Phase-2 check that the measured
24/8 opportunity is operationally specified and worth testing rather than an
artifact of authored arithmetic or incomplete fallback accounting.

## Decision

Dispatch one fresh reviewer. Record its report verbatim before any further
review, implementation or experiment.
