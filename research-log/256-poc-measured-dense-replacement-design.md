# PoC Design — Capped Measured Dense Replacement

**Date:** 2026-08-02 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 10 · **Status:** preregistered

## Context

Report 254 passed theory review in report 255. Before changing the active attack code, Phase 3 must verify the frozen mechanics locally.

## Assumption under test

The Capped Measured Dense Replacement mechanics can be implemented so that:

1. a positive local `CompliantAgent` fixture retains at least `93` four-event dense candidates;
2. a no-fire fixture returns zero dense candidates and falls back to v35-style one-URL candidates;
3. a capped-unmeasured comparator differs from measured replacement on no-fire;
4. the score-rate-stop ablation changes admission on a slow-dense fixture;
5. all emitted messages are non-empty and shorter than `2000` characters.

## Prediction

Prediction ledger row:

```text
poc-measured-dense-replacement poc_gate_pass 1 match-baseline high NA NA NA NA preregistered Local PoC must pass positive dense retention >=93, no-fire zero dense fallback, capped-unmeasured comparator difference, and score-rate-stop ablation
```

Predicted primary metric:

- `poc_gate_pass = 1`

Rationale:

The deterministic local `CompliantAgent` already produced four `EXFILTRATION` events for exact dense4 messages in report 249. The no-fire and score-rate-stop cases are local control logic, not model-prevalence claims, so a correct implementation should satisfy them. Failure here would be implementation-defeated, not a target-model disconfirmation.

## Experiment spec

Write `experiments/poc/measured_dense_replacement_poc.py` and run it once.

Required parseable metrics:

```text
poc_gate_pass: 1|0
positive_dense_retained: <int>
positive_min_events: <int>
nofire_dense_retained: <int>
nofire_fallback_one_url: 1|0
unmeasured_comparator_dense_retained: <int>
score_rate_stop_changes_admission: 1|0
max_message_len: <int>
empty_messages: <int>
runtime_seconds: <float>
```

Confirm criteria:

- `poc_gate_pass: 1`;
- `positive_dense_retained >= 93`;
- `positive_min_events >= 4`;
- `nofire_dense_retained == 0`;
- `nofire_fallback_one_url == 1`;
- `unmeasured_comparator_dense_retained > 0`;
- `score_rate_stop_changes_admission == 1`;
- `max_message_len < 2000`;
- `empty_messages == 0`.

Reject criteria:

- any confirm criterion fails.

## Transferability argument

This PoC tests implementation mechanics only: exact candidate construction, event counting, thresholding, fallback, and local ablations. It does not predict target-model dense-event prevalence or hidden replay safety. Passing this PoC permits Phase 4 implementation in the active attack path; it does not authorize Kaggle submission by itself.

## Boundaries

- No Kaggle.
- No network.
- Do not edit `experiments/attack.py` in Phase 3.
- New files under `experiments/poc/` are allowed.

## Problem alignment

This validates the local mechanics needed before testing whether measured dense replacement can reach the competition-relevant `100` range.
