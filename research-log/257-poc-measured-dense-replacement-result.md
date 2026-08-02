# Capped Measured Dense Replacement PoC Result

**Date:** 2026-08-02 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 10 · **Status:** completed

## Context

Report `254` preregistered Capped Measured Dense Replacement after the blind four-endpoint dense branch blanked remotely in v36. Report `255` accepted the hypothesis as rigorous. Report `256` specified the Phase-3 local PoC criteria before implementation.

The PoC tests only local mechanics: exact dense message construction, candidate-level measured retention, no-fire fallback, capped-unmeasured comparator behavior, score-rate-stop admission logic, and serialization sanity. It does not prove target-model prevalence, replay safety, private transfer, or Kaggle readiness.

## Content

PoC artifacts:

- `experiments/poc/measured_dense_replacement_poc.py`
- `experiments/poc/measured_dense_replacement_notes.md`
- `experiments/poc/measured_dense_replacement_poc.log`

Executed command:

```text
PYTHONPATH=comp/sdk:experiments comp/.venv/bin/python experiments/poc/measured_dense_replacement_poc.py
```

Extracted metrics:

```text
poc_gate_pass: 1
positive_dense_retained: 96
positive_min_events: 4
nofire_dense_retained: 0
nofire_fallback_one_url: 1
unmeasured_comparator_dense_retained: 96
score_rate_stop_changes_admission: 1
max_message_len: 392
empty_messages: 0
runtime_seconds: 4.170895
```

Prediction vs. reality: the preregistered `poc_gate_pass = 1` prediction was confirmed. The positive local fixture retained the frozen cap of 96 dense candidates, every retained dense candidate met the four-event local minimum, the no-fire fixture retained zero dense candidates and exposed the one-url fallback, the capped-unmeasured comparator retained dense candidates without measurement, and the score-rate-stop ablation changed admission as required.

## Gate Check

- PoC support: PASS — `grep "^[a-z_]*:" experiments/poc/measured_dense_replacement_poc.log` returned `poc_gate_pass: 1`.
- Metrics verified from log: PASS — the same grep returned `positive_dense_retained: 96`, `positive_min_events: 4`, `nofire_dense_retained: 0`, `nofire_fallback_one_url: 1`, `unmeasured_comparator_dense_retained: 96`, `score_rate_stop_changes_admission: 1`, `max_message_len: 392`, and `empty_messages: 0`.
- Provenance: PASS — `head -n 1 experiments/poc/measured_dense_replacement_poc.log` returned the exact command `PYTHONPATH=comp/sdk:experiments comp/.venv/bin/python experiments/poc/measured_dense_replacement_poc.py`; `wc -l` returned 11 log lines; `stat` showed the log was written after the script and notes; `py_compile` exited 0.
- User go/no-go: PASS — standing Cycle-3 checkpoint default quotes `go, dont ask me these questions again, go iterate and improve yourself`; the Cycle-3 authorization separately preserves confidence-before-submission.

## Problem alignment

This closes the local mechanics gate for a measured replacement of the refuted blind dense branch while preserving the competition objective and confidence-before-submission rule.

## Decision

Phase 3 is confirmed. Proceed to Phase 4 implementation of the frozen constants in `experiments/attack.py`, with v35 validation-fill fallback retained and no Kaggle submission until the implementation confidence gate passes.

## Next Steps

1. Implement Capped Measured Dense Replacement in the active attack code using the frozen constants from report `254`.
2. Rebuild notebooks and run deterministic/local SDK confidence checks.
3. Only after a clean Kaggle commit-run artifact, decide whether the competition submission confidence gate passes.
