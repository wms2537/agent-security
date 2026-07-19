# Experiment: ORF Phase-4 exact global baseline

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** preregistered, not run

## Context

This is T014 and the first run in the frozen Phase-4 plan. It reproduces the
closest comparator, `PROBE_GLOBAL`, on exactly the three already committed public
non-target masters. The core policy will not be run or evaluated here.

## Design

For each master, generate all 320 primary profiles and exact seven-action score
tables under the v9 default mechanics. Sum each action column across profiles and
choose one global length by exact maximum with smaller-length tie-breaking. Save
the 960 per-profile tables plus aggregate-by-length totals. A common baseline
engine may preserve realized parameters for later preregistered ablations, but
this run must neither calculate nor report the adaptive aggregate.

The baseline implementation must match the immutable calibration reference for
every default profile and score value. An independently readable TSV will permit
the orchestrator to recompute all three global results without rerunning the
generator.

## Prediction and rationale

The predicted primary metric, mean global raw score across three masters, is
**8,500,000**, with medium confidence and a confirmation interval of
`[7,500,000,9,500,000]`. Calibration v2's 64 untouched-at-the-time public
masters had mean G 8,505,123.71875, minimum 7,683,532, maximum 8,968,970, and
all selected length 16. The new labels are distinct, so 8.5m and length 16 are
predictions rather than reused outcomes.

The two exact secondary predictions are global-length-16 fraction `1.0` and
reference-match fraction `1.0`. A score-range miss is a predictive
disconfirmation; any reference mismatch is protocol-invalid and blocks Phase 4.

## Gate Check

Pending execution. The prediction rows, Phase-4 contract, and this rationale are
committed before dispatch.

## Problem alignment

This establishes the strongest exact shared-length comparator before measuring
the proposed profile-conditioned structure advantage.

## Decision

Dispatch one CPU-only baseline implementer after the preregistration commit.

## Next Steps

Verify artifacts, immutable diff, exact recomputation, and provenance. Stop on
any mechanical mismatch. No held-out, network, or Kaggle action.
