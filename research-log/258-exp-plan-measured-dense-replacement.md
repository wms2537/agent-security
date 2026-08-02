# Phase 4 Experiment Plan — Capped Measured Dense Replacement

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 10 · **Status:** in-progress

## Context

Phase 3 confirmed local mechanics for Capped Measured Dense Replacement in report `257`. The Phase-4 job is to make one controlled change to the active competition kernel: replace the disabled/blind dense branch with the measured-retention branch specified in report `254`, while preserving the v35 validation-fill fallback.

Baseline/floor: v35 public-control validation-fill score `86.670` from submission ref `55158967`.

Failed control: v36 blind four-endpoint dense branch blanked despite clean local schema/source checks, so blind dense emission remains forbidden.

## Plan

### T122 — Local implementation gate

Change: edit `experiments/attack.py` only enough to implement frozen measured dense replacement constants and admission logic:

- `MEASURED_DENSE_REPLACEMENT_ENABLED = True`
- `MEASURED_DENSE_ENDPOINTS = 4`
- `MEASURED_DENSE_MIN_EVENTS = 4`
- `MEASURED_DENSE_MIN_KEPT_TO_USE = 93`
- `MEASURED_DENSE_MAX_KEPT = 96`
- `MEASURED_DENSE_BUDGET_FRAC = 0.20`
- `MEASURED_DENSE_PROBE_REPS = 2`
- `MEASURED_DENSE_MAX_ATTEMPTS = 160`
- `MEASURED_DENSE_SCORE_RATE_GAIN = 1.15`
- `MEASURED_DENSE_PROBE_BASE = 760000`
- `MEASURED_DENSE_FRAME_OFFSET = 50000`

Required local metrics:

- Default local compliant fixture returns dense candidates only after measured firing.
- No-fire fixture returns no dense candidates and falls back to one-url validation-fill candidates.
- Explicit disabled override reproduces the v35 fallback path.
- Serialization has zero empty messages and `max_message_len < 2000`.
- Notebook rebuild embeds the modified attack and preserves direct `JEDAttackInferenceServer().serve()`.

Prediction: `local-measured-dense-impl-gate.poc_gate_pass = 1` with high confidence, because report `257` already confirmed the mechanics against imported attack helpers.

### T123 — Code-review/local confidence gate

Before any Kaggle mutation, review the attack diff and local confidence logs for:

- no blind dense emission;
- threshold constants match report `254`;
- fallback remains active and one-url;
- no submission CSV/header/wrapper regression;
- no use of hidden logs or unavailable Kaggle notebook logs as evidence.

### T124 — Kaggle commit-run artifact gate

Push a kernel version only after T122/T123 pass. Inspect downloaded kernel output for:

- generated `submission.csv` with expected header and non-empty placeholder/output format;
- source marker/hash match;
- no traceback;
- dense/fallback constants embedded as expected.

This is target-owned runtime evidence but not leaderboard evidence.

### T125 — Competition submission gate

Submit the completed kernel version only if T124 passes. Interpret public score using the preregistered bins:

- success: `public_score >= 100.000`;
- partial: `86.670 <= public_score < 100.000`;
- failure: blank/error or `< 86.670`.

## Gate Check

- Plan recorded before implementation: PASS.
- Prediction row recorded before local implementation run: PASS — `results.tsv` contains `local-measured-dense-impl-gate`.

## Problem alignment

This plan targets the measured bottleneck created by blind dense failures while keeping v35 fallback as regression control and preserving confidence-before-submission.

## Decision

Proceed with T122 only. Do not start Kaggle push/submission until the local implementation and review gates pass.
