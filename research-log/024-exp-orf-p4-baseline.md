# Experiment: ORF Phase-4 exact global baseline

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed, kept

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

- Independent artifact audit returned
  `baseline_artifact_audit=PASS rows=960 score_pairs=6720 masters=[8403762, 8824632, 8579258] mean=8602550.666666666046 all_m=16`; the displayed float is non-authoritative, while the asserted exact mean is `25807652/3` and the logged fixed decimal is `8602550.666666666667`.
- Direct narrow grep extracted every word-only metric. The preregistered secondary
  name `global_length_16_fraction` contains digits and was therefore missed by
  `^[a-z_]*`; the explicit superset extractor `grep -E '^[a-z_][a-z_0-9]*:'`
  recovered `global_length_16_fraction: 1.000000000000` from the original log.
  The one-use validation label was not rerun or the log rewritten merely to
  rename a metric.
- `wc -l` returned 961 score-table lines, 22 aggregate-table lines, and 10 log
  lines. The exact command is the first log line and output mtimes are plausible
  for a 1.491515685-second run.
- `git diff --exit-code a416a72 -- <eight immutable paths>` exited 0 with empty
  output.
- The code never computed or reported the adaptive aggregate.

## Problem alignment

This establishes the strongest exact shared-length comparator before measuring
the proposed profile-conditioned structure advantage.

## Decision

**Keep.** Baseline reproduction and exhaustive tuning parity pass. The three
global scores are 8,403,762; 8,824,632; and 8,579,258, all selecting length 16.
The implementation is a single exact optimizer and passes the simplicity
criterion. The output-name defect is recorded and future stdout metric names
must spell numbers as words.

## Next Steps

Implement but do not run the core per-profile wrapper for the code-review gate.
No held-out, network, or Kaggle action.

## Prediction vs. Reality

The mean prediction was confirmed: actual `8,602,550.666666666667` was
`+102,550.666666666667` above 8.5m and remained inside `[7.5m,9.5m]`. All three
masters selected length 16 and all 6,720 independent/reference score pairs
matched exactly. The result strengthens confidence in baseline mechanics only;
it says nothing yet about the sealed adaptive gain.
