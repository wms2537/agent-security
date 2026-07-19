# ORF evaluation contract

**Version:** public-nontarget-v1  
**Recorded:** 2026-07-19  
**Claim scope:** deterministic public non-target validation of ORF mechanics and
finite-table conditional regret; never evidence of live-model prevalence,
learnability, private transfer, Kaggle performance, or the unexecuted beacon-held-out
v9 claim.

## Data tiers

- **Tuning signal:** the already-spent exploratory calibration rows
  `orf-cal-v1-*` and `orf-cal-v2-*`. They may motivate a prediction but can never
  confirm it.
- **Validation signal:** `orf-poc-v1` and later explicitly preregistered public
  non-target labels. Each label is fixed before execution and may be run once.
- **Test signal:** the beacon-derived `orf-heldout-v7` target. It remains locked,
  uncreated, and unauthorized. No Phase-3 or Phase-4 task may freeze, reveal,
  derive, generate, or evaluate it. Without a separately authorized one-shot test,
  Phase 5 must narrow the conclusion and Phase 6 must not present public validation
  numbers as test results.

## Phase-3 primary metric

For the 40 public PoC profiles fixed in
`experiments/configs/orf-poc-v1.json`, let the immutable support-calibration
functions compute the seven exact integer score values `S_z(m)` for
`m in {1,2,4,8,16,24,32}`. Define

```text
A = sum_z max_m S_z(m)
G = max_m sum_z S_z(m), with smaller m breaking ties
adaptive_gain_percent = 100 * (A-G) / G
```

The primary Phase-3 assumption is supported iff the run is protocol-valid and
`adaptive_gain_percent >= 5`. A valid result below 5 is a disconfirmation, not
an inconclusive result. The prediction-ledger signal is `confirm` when the value
is within the preregistered 20–50% interval, `partial` when it is at least 5% but
outside that interval, and `disconfirm` when it is below 5%.

## Controls and validity checks

- The homogeneous negative uses 64 fixed profiles with `c(m)=b*m`, `e(m)=m`,
  `b in [5,12]`, and must yield adaptive-minus-global raw difference exactly
  zero with both policies choosing `m=1`. Any failure is protocol-invalid.
- The two preserved actual-SDK fixtures must recompute their predicates,
  16-hex score-cell hashes, uniqueness, and `q=16e+2`; exactly two cases must
  pass. Any failure is protocol-invalid.
- Exactly 40 primary profiles, one from every crossed stratum, must be evaluated;
  the sole replicate is index 0. No profile, label, factor, or threshold may be
  replaced after observing an outcome.
- Arithmetic is exact `Fraction` after precision-80 Decimal parameter creation.
  Any cliff-floor distance below `1e-60` is protocol-invalid; there is no
  resampling.

## Immutable read-only paths

The experiment implementer must not modify these paths:

```text
experiments/configs/orf-poc-v1.json
experiments/configs/evaluation-contract.md
experiments/poc/orf_support_calibration.py
experiments/poc/orf_v7_contract_reference.py
experiments/fixtures/orf-heldout-v7-golden-fixtures.json
comp/sdk/aicomp_sdk/core/cells.py
comp/sdk/aicomp_sdk/core/predicates.py
comp/sdk/aicomp_sdk/scoring.py
```

The orchestrator verifies this mechanically over the dispatch commit range.
Mutable code is restricted to new Phase-3 files under `experiments/poc/` and
their local outputs.

## Resource and action boundaries

- CPU only; expected wall time under two minutes; hard design limit five minutes.
- Three trivial PoC debug attempts total. A scientific-choice change is not a
  debug attempt and requires a new preregistration.
- No network, beacon, held-out target, Kaggle, external post, submission, or
  external-account mutation.
