# ORF-B non-target support calibration v2

**Supersedes:** the protocol-invalid run in
`research-log/014-orf-support-calibration.md`  
**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed, exploratory

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

**Support criterion passed; prediction direction confirmed in exploratory data.**
The fixed command completed in 29.43 seconds on CPython 3.14.3. Results were:

| Design | Masters clearing 5% | Minimum gain | Median gain | Maximum gain |
|---|---:|---:|---:|---:|
| equal, `H=200000` | 64/64 | 34.575811113981% | 40.924155277025% | 45.433610480180% |
| balanced cliff presence, `H=200000` | 64/64 | 24.987661930465% | 32.324156091809% | 38.849300841017% |
| no cliff only, `H=200000` | 64/64 | 5.117860088584% | 6.991608265969% | 9.793532503442% |
| cliff only, `H=200000` | 64/64 | 35.101784203438% | 39.796867096003% | 44.613150778688% |
| equal, `H=10^18` | 64/64 | 41.372040363181% | 44.204209608439% | 48.319935695095% |

The no-cliff-only unsaturated sensitivity, not required for passage, cleared on
62/64 masters with a 4.780664512982% minimum and 6.355745532101% median. The
minimum distance of any cliff expression from an integer was
`2.4702028345850861854631560389931149158158007314717302917408272803144660234725560E-8`,
well above `1E-60`.

An independent ledger check returned
`validated_rows=512 unique_design_rows=512 masters=64 all_score_identities=true all_summary_counts=true support=true`.
V1 and v2 output hashes are byte-identical, showing the repaired exact cost
construction did not change a capacity floor, while only v2 conforms to the
preregistered numeric implementation.

Prediction versus reality: all five clearing-fraction predictions and the floor
certificate were conservative and confirmed. Each row is marked `exploratory`,
not `keep`; these outcomes support the plausibility of the future 5% prediction
but cannot confirm it.

Artifact hashes:

- `summary.json`:
  `602d3885232d44a26f22f002f463c314d37308188510e519512bea710e433c05`;
- `masters.tsv`:
  `9d0f5208a18b673713dcec3c80c08c20697bcf06b0d07f5d6470b920e117e235`.

## Decision

Use the v2 distribution as explicitly exploratory support in the superseding ORF
hypothesis. Retain the 5% threshold and target design unchanged. The iteration's
exploratory budget is exhausted at 2/2 (one invalid, one valid); no further
calibration run is permitted.
