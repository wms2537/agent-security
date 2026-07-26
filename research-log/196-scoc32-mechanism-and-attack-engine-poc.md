# T071 — SCOC-32 mechanism harness run04 and adaptive routing PoC

**Date:** 2026-07-23 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 4/5 · **Status:** completed

## Context

The team needed a completed PoC validation step after the mechanism-harness work
in T070. This run validates reproducibility under the exact command configuration
used for prior artifacts and checks that the new `scoc_chain` route in
`attack.py` stays correct on local mocks before any further Phase-3 PoC or
competition iteration.

## Content

I ran two deterministic checks:

1. Re-run the mechanism harness on the local control set with an explicit
   `PYTHONPATH` mount to ensure the fixture import path is consistent and the
   results can be regenerated.
2. Run `experiments/multi_message_eval.py` to verify routing/debug invariants after
   adding SCOC mode in the real algorithm path.

## Gate check

- `comp/.venv/bin/python -m py_compile experiments/attack.py experiments/multi_message_eval.py experiments/scoc32_mechanism_harness.py`
  - compile check: PASS
- `PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/scoc32_mechanism_harness.py --candidates 12 --seed 42 --lengths 1 4 8 16 24 32 --max-hops 8 --out-dir artifacts/scoc32/run04`
  - command completed and wrote `artifacts/scoc32/run04/scoc32-mechanism-harness.json` + `.tsv`.
  - m=32 coverage: `SINGLE_FULL`, `CHAIN_FULL`, `CHAIN_COMPACT_EXPLICIT`,
    `CHAIN_SCOC`, `CHAIN_GENERIC` each `coverage=1.000`; `CHAIN_BLOCKED_ANCHOR` and
    `COLD_OPERAND_ONLY` each `coverage=0.000`.
  - m=32 raw/s: `CHAIN_FULL 14582.598`, `CHAIN_COMPACT_EXPLICIT 14558.972`,
    `CHAIN_SCOC 13519.899`, `CHAIN_GENERIC 10872.659`.
- `PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/multi_message_eval.py`
  - route sanity and fallback assertions all passed.
  - final print includes: `PASS: adaptive routing, multi raw=390, fallback raw=54`.

## Prediction vs reality

**Prediction (before run):** local SCOC mechanisms should reproduce run03 results
under the same seed and preserve gate-qualifying coverage for non-blocked
mechanisms.

**Reality:** confirmed. Re-run parity held exactly for the run03 gate logic; chain
coverage and raw/sec behavior was stable on m=32 and all listed lengths. Route
debug also confirmed safe handling of positive, fallback, and blocked-context
branches.

## Problem alignment

This PoC validates the core SCOC mechanical assumptions needed before moving to a
competition-facing attempt: the same continuation path can be activated under
explicit control, and the non-viable fallback mechanisms remain excluded by the
coverage gate.

## Decision

T071 is complete and recorded in `results.tsv` as:
`scoc32-mechanism-harness-run04` coverage_gate_m32 with `metric_value=1.0`.
The next step is a controlled, budget-conscious competition-facing candidate
test only after a Phase-3 execution preregistration is attached.

## Next Steps

- Move to SCOC-32 Phase-3 candidate-preregistration and an accountable
  pre-commit local attempt under the exact budget/safety contract.
- Only then run a Kaggle commit/score step when the confidence gate is satisfied.
