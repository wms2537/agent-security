# ORF-B non-target support calibration

**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** preregistered, not run

## Context

Theory review round 8 accepted the exact conditional-regret identity but found no
substantive support for the low-confidence 5% prediction. This exploratory
calibration is preregistered before execution. It is not the held-out experiment,
cannot confirm the hypothesis, uses no NIST pulse, and performs no Kaggle action.

## Calibration population

Exactly 64 public non-target masters are
`SHA256(ASCII("orf-nontarget-calibration-v1|master|{index:03d}"))` for contiguous
indices 0 through 63. Each master creates the same 40 equal strata and eight
replicates per stratum as ORF-B. Profile streams remain domain-separated by
`primary|stratum={stratum:02d}|replicate={replicate:02d}`. There is no rejection,
replacement, retry, or outcome-dependent generation.

The program uses `comp/.venv/bin/python` (CPython 3.14.3), `random.Random` only to
produce the stable binary-rational `random()` value, and `Decimal` precision 80
with `ROUND_HALF_EVEN` for `ln` and `exp`. Costs become exact `Fraction` values.
Every cliff floor records its distance to the nearer integer. A distance below
`1e-60` fails the preregistered stability certificate; no profile is regenerated.

## Weight and saturation sensitivity

For every master, compute the exact adaptive/global contrast under both
`H=200000` and `H=10^18`, the latter an effectively unsaturated control. Within
each saturation setting compute four fixed weighting regimes:

1. `equal`: all 320 profiles have integer weight 1, matching the hypothesis.
2. `balanced_cliff_presence`: each of 64 no-cliff profiles has weight 4 and each
   of 256 cliff profiles has weight 1, giving the two groups equal total weight.
3. `no_cliff_only`: the 64 no-cliff profiles have weight 1; all others have 0.
4. `cliff_only`: the 256 cliff profiles have weight 1; no-cliff profiles have 0.

For every combination report the fraction of masters clearing 5%, minimum,
median, and maximum gain. All variants are sensitivity analyses; none may replace
the frozen equal-weight target estimand.

## Prediction and rationale

Before the run, I predict that at least 48/64 equal-weight `H=200000` masters will
clear 5%. Confidence is low: the crossed reset, linear, curvature, and cliff bands
are deliberately capable of shifting the preferred length, but the exact regret
magnitude is not bounded and saturation can make heterogeneous profiles share a
near-common optimum.

The predeclared support criterion requires all of the following:

- equal-weight `H=200000`: at least 48/64 clear 5%;
- balanced-cliff, no-cliff-only, cliff-only `H=200000`: each at least 32/64;
- equal-weight `H=10^18`: at least 32/64; and
- minimum cliff-floor distance at least `1e-60`.

Failure of any condition means the ensemble does not support the 5% prediction.
Passage provides exploratory predictive support only; it does not confirm the
single future held-out realization. The held-out threshold, support, target rule,
and decision partition will not be tuned from these outcomes.

## Frozen command and outputs

```text
comp/.venv/bin/python -I experiments/poc/orf_support_calibration.py > experiments/runs/orf-support-calibration-v1/run.log 2>&1
```

The script writes canonical `summary.json` and `masters.tsv` beneath
`experiments/runs/orf-support-calibration-v1/`. The run log's first line is the
executed Python command emitted by the script. The code and all six unresolved
prediction-ledger rows are committed before this command is executed.

## Prediction vs. Reality

Pending. No calibration outcome has been generated or inspected.

## Decision

Run once after this preregistration commit, resolve all six rows, and report the
predeclared support criterion without threshold changes.
