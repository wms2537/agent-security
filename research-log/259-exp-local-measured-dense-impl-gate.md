# Local Experiment — Measured Dense Replacement Implementation Gate

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 10 · **Status:** completed

## Context

Report `258` preregistered the local implementation gate before editing active attack code. This run validates that `experiments/attack.py` implements the report `254` frozen measured dense replacement rather than reintroducing the v36 blind dense branch.

## Content

Changed code:

- `experiments/attack.py`
- regenerated notebooks: `ai-agent-security-attack.ipynb`, `submission/kaggle_notebook.ipynb`, `submission/kernel/kaggle_notebook.ipynb`
- local gate script: `experiments/measured_dense_impl_gate/run_check.py`

Executed local gate command:

```text
PYTHONPATH=comp/sdk:experiments comp/.venv/bin/python experiments/measured_dense_impl_gate/run_check.py
```

Extracted metrics:

```text
poc_gate_pass: 1
positive_total_candidates: 120
positive_dense_retained: 96
positive_min_events: 4
positive_first_dense: 1
nofire_total_candidates: 300
nofire_dense_retained: 0
nofire_fallback_one_url: 1
disabled_count: 5
disabled_max_urls: 1
max_message_len: 392
empty_messages: 0
runtime_seconds: 3.684057
```

Prediction vs. reality: the preregistered `poc_gate_pass = 1` prediction was confirmed. The default compliant fixture returned a dense prefix of exactly 96 candidates, the replayed dense messages produced at least four events, the no-fire fixture retained zero dense candidates and fell back to one-url single-post candidates, and the explicit disabled override returned five one-url fallback candidates.

## Gate Check

- Compile: PASS — `comp/.venv/bin/python -m py_compile experiments/attack.py submission/build_notebook.py experiments/measured_dense_impl_gate/run_check.py` exited 0.
- Local metrics: PASS — `grep "^[a-z_]*:" experiments/measured_dense_impl_gate/run.log` returned `poc_gate_pass: 1`, `positive_dense_retained: 96`, `positive_min_events: 4`, `nofire_dense_retained: 0`, `nofire_fallback_one_url: 1`, `disabled_count: 5`, and `disabled_max_urls: 1`.
- Provenance: PASS — `head -n 1 experiments/measured_dense_impl_gate/run.log` returned the exact command; `wc -l` returned 14 log lines; `stat` showed the log was written after source changes.
- Frozen constants/wrapper: PASS — `rg` over `experiments/attack.py` and all three notebooks found `DENSE_ENABLED = False`, `MEASURED_DENSE_REPLACEMENT_ENABLED = True`, `MEASURED_DENSE_MIN_KEPT_TO_USE = 93`, `MEASURED_DENSE_MAX_KEPT = 96`, `MEASURED_DENSE_PROBE_BASE = 760000`, `MEASURED_DENSE_FRAME_OFFSET = 50000`, `Id,Score`, and direct `JEDAttackInferenceServer().serve()`.
- Metadata: PASS — `jq -r '.enable_gpu, .machine_shape, .kernel_type' submission/kernel/kernel-metadata.json` returned `true`, `NvidiaTeslaT4`, `notebook`.
- Blind dense return: PASS — `rg -n "return _emit_dense|_emit_dense\\(" experiments/attack.py` returned only the helper definition, not a return path.

## Problem alignment

This implements the measured replacement for the v36 blind dense failure while preserving a one-url v35 fallback path and preventing another known submission-format/runtime regression.

## Decision

T122 passes locally. Proceed to T123 code-review/local confidence gate before any Kaggle mutation.

## Next Steps

Run a code-review gate on the active attack diff and local evidence. Do not push a Kaggle kernel until that review is closed.
