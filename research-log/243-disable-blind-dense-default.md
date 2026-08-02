# Disable Blind Dense Default

**Date:** 2026-08-02 · **Phase:** 4 · **Cycle:** 3 · **Iteration:** 9 · **Status:** completed

## Context

Report 242 records v36 ref `55177045` completing with a blank public/private score despite clean local and commit-run schema/source gates. The active repository still had `DENSE_ENABLED = True`, so the failed blind dense path remained the default unless explicitly disabled.

## Content

Changed the active attack default:

- `DENSE_ENABLED = False` in `experiments/attack.py`;
- rebuilt all notebook artifacts with `submission/build_notebook.py`;
- kept the explicit `dense_enabled=True` override available for a separately preregistered measured-fill repair experiment;
- did not submit a new Kaggle run.

This restores the active code path to the v35-style public-control validation-fill floor while preserving the dense helpers for controlled future experiments.

## Gate Check

- Rebuild: `comp/.venv/bin/python submission/build_notebook.py` -> `attack.py parses OK`.
- Python/metadata/notebook contract: `comp/.venv/bin/python -m py_compile experiments/attack.py submission/build_notebook.py && jq -r '.enable_gpu, .machine_shape, .kernel_type' submission/kernel/kernel-metadata.json && rg -n "DENSE_ENABLED = False|JEDAttackInferenceServer\(\)\.serve\(\)|Id,Score" ai-agent-security-attack.ipynb submission/kaggle_notebook.ipynb submission/kernel/kaggle_notebook.ipynb` -> `true`, `NvidiaTeslaT4`, `notebook`, and all three notebooks contain the expected markers.
- Ledger shape: `awk -F'\t' ... results.tsv` -> `results.tsv columns 11 ok`; `awk -F'\t' ... competition/leaderboard_experiments.tsv` -> `competition/leaderboard_experiments.tsv columns 10 ok`.
- Default/explicit local smoke: `PYTHONPATH=comp/sdk:experiments comp/.venv/bin/python <AttackAlgorithm smoke>` -> `default_count 5`, `default_max_urls 1`, `default_max_posts 1`, `explicit_dense_count 3`, `explicit_dense_max_urls 4`, `explicit_dense_max_posts 4`.

## Problem alignment

This prevents repeating a refuted hidden-boundary failure and keeps the current repository capable of reproducing the known high-80 floor before any above-ceiling repair.

## Decision

Keep blind dense disabled by default. The next above-100 attempt should not be probe-then-blind-emit; it must be a measured validation-fill density controller or a different preregistered structure with an explicit resource gate.
