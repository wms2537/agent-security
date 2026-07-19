# ORF-B non-target support calibration v2

**Supersedes:** the protocol-invalid run in
`research-log/014-orf-support-calibration.md`  
**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** preregistered, not run

## Context

Calibration v1 was rejected after its cost polynomial was found to execute under
the default Decimal precision 28 before conversion to `Fraction`. The nominal v1
results remain non-evaluable and are not used here. This is fix attempt 1 and the
second/final exploratory run for iteration 4. It uses no NIST beacon and no Kaggle
action.

## Frozen retry

All scientific choices are unchanged from the preregistration in entry 014:

- the same 64 public masters and keyed 320-profile realizations;
- the same equal, balanced-cliff-presence, no-cliff-only, and cliff-only weights;
- the same `H=200000` and `H=10^18` saturation settings;
- the same six predicted values and low confidence;
- the same all-or-nothing support criterion; and
- no threshold, factor, range, replicate, master, or sensitivity change.

The sole implementation change is numeric. Immediately after precision-80
Decimal parameter generation, create `aF=Fraction(a)`, `bF=Fraction(b)`, and
`dF=Fraction(d)` separately. Then compute every cost as the exact rational
`aF+bF*m+dF*m*m`. No Decimal addition or multiplication occurs in cost
construction, so the process default context cannot round it.

## Prediction and rationale

The v1 outcomes are explicitly ignored. The predictions remain those sealed at
`bba39d7`: equal-weight `H=200000` at least 48/64 clear 5%; balanced-cliff,
no-cliff-only, and cliff-only `H=200000` each at least 32/64; equal-weight
`H=10^18` at least 32/64; and minimum cliff-floor distance at least `1e-60`.
Confidence remains low for exactly the rationale recorded before v1.

The six new ledger rows are a retry ledger, not a reinterpretation of the v1
rows. Passage is exploratory support for a future prediction, never confirmation.
Failure of any check leaves the 5% prediction unsupported. No outcome may tune the
held-out support or threshold.

## Frozen command and outputs

```text
comp/.venv/bin/python -I experiments/poc/orf_support_calibration.py > experiments/runs/orf-support-calibration-v2/run.log 2>&1
```

The output directory is new and fixed. V1 artifacts are never overwritten.

## Prediction vs. Reality

Pending. No v2 output has been generated or inspected.

## Decision

Run once after the fixed code, this entry, and six unresolved retry rows are
committed. Accept or reject the support criterion exactly as preregistered.
