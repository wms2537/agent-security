# Stage B Four-Endpoint Density Implementation

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 9 · **Status:** completed

## Context

Report 239 preregistered a single changed dimension: exact within-message endpoint density. The implementation keeps the v35 validation-fill single-post path as fallback and adds a dense branch only before that fallback.

## Content

The active attack source now:

- defines `DENSE_ENDPOINTS = 4`, `DENSE_TARGET_COUNT = 320`, `DENSE_PROBE_REPS = 2`, and `DENSE_MIN_EVENTS = 4`;
- builds one user message containing four unique `.co` URLs;
- probes both plain and Harmony/channel-shaped exact final messages;
- counts `EXFILTRATION` events from `eval_predicates(trace)` before admission;
- admits dense candidates only if every probe for the chosen arm has four events;
- falls back to the v35 validation-fill `_fill` path if dense probes fail or latency exceeds the conservative budget check.

Source identity:

```text
experiments/attack.py                         a546e769d81984a6063c4ad0fcbf535f576bc8aea2b4c47b3a0e0dd34e2e9f17
ai-agent-security-attack.ipynb                bdcf63d3ef7079d11a379bb5d5276df8f5092d7f863cc811fa3b32de45ed01ca
submission/kaggle_notebook.ipynb              bdcf63d3ef7079d11a379bb5d5276df8f5092d7f863cc811fa3b32de45ed01ca
submission/kernel/kaggle_notebook.ipynb       bdcf63d3ef7079d11a379bb5d5276df8f5092d7f863cc811fa3b32de45ed01ca
submission/kernel/kernel-metadata.json        6d16226f6623c00b598e51b40ce454d386eb67e8dfd0930f94b32349d03d6426
```

## Gate Check

- Compile: `comp/.venv/bin/python -m py_compile experiments/attack.py submission/build_notebook.py` -> exit 0.
- Exact dense mechanics: local SDK CompliantAgent script -> `dense_exact_events 4`, `dense_tool_events 4`, `dense_raw_one 66.0`, `dense_message_len 376`.
- Fallback mechanics: SinglePostOnlyAgent script -> `fallback_count 5`, `fallback_first_urls 1`, `fallback_dense_marker_absent True`.
- Candidate serialization: dense smoke -> `dense_candidates 320`, `dense_messages_per_candidate 1`, `dense_first_url_count 4`, `dense_empty_messages 0`, `dense_max_message_len 380`.
- Notebook rebuild: `comp/.venv/bin/python submission/build_notebook.py` -> `attack.py parses OK`.
- Notebook contract: generated notebook checker -> all three notebooks `contract PASS missing []`.
- Kernel metadata: `jq -r '.enable_gpu, .machine_shape, .kernel_type' submission/kernel/kernel-metadata.json` -> `true`, `NvidiaTeslaT4`, `notebook`.
- Whitespace check: `git diff --check` -> exit 0.

## Problem alignment

The code tests a source-compliant score-density mechanism while preserving the known-good runner and v35 fallback, directly addressing the path from `86.670` toward scores above `100`.

## Decision

Proceed to T118: push the committed notebook to Kaggle, inspect the commit-run artifact, and submit only if the output/source/schema confidence gate remains clean.
