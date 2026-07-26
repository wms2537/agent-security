# T072 — SCOC-32 Phase-3 local red-team paired control comparison

**Date:** 2026-07-23 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 5/5 · **Status:** completed

## Context

After T071 established stable mechanism parity and route sanity, I executed a controlled local SCOC vs non-SCOC red-team comparison in the SDK sandbox to quantify whether enabling SCOC changes structure and throughput under a fixed-cost amortization regime.

## Predefined expectation

I tested two conditions with identical probe/fill envelopes and candidate cap:

- **No-SCOC baseline:** expected local normalized score around 20+ with `multi_message` fill.
- **SCOC-enabled:** expected either improved throughput (structure shift to `scoc_chain`) or parity in score.

## Verification commands

- `comp/.venv/bin/python -m py_compile experiments/attack.py experiments/multi_message_eval.py`
- `cd /home/soh/agent-security && PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python - <<'PY' ...` (paired `evaluate_redteam` + debug dry-run, artifacts in `artifacts/scoc32/run05`)
- `cat artifacts/scoc32/run05/scoc32-local-scoc-pair.tsv`

I used a fixed `AmortizingAgent` target with
`probe_reps=1`, `probe_time_cap_s=5.0`, `gen_margin_s=0.5`, `replay_budget_s=6.0`, `max_candidates=24`, `multi_fill_messages=12`, and `scoc_fill_messages=12`.

## Evidence

Raw summary from `artifacts/scoc32/run05/scoc32-local-scoc-pair.tsv`:

| tag | enable_scoc | findings | normalized | structure | selected_raw_per_s | replay_cost_s |
|---|---|---:|---:|---|---:|---:|
| disable_scoc | False | 24 | 23.280 | multi_message | 1266.895 | 2.1 |
| enable_scoc  | True  | 24 | 23.280 | scoc_chain    | 2.2 |

Detailed debug is in `artifacts/scoc32/run05/scoc32-local-scoc-pair.json`.

## Prediction vs. reality

**Prediction (before run):** enabling SCOC would likely switch routing but should not materially reduce candidate throughput under this fixed mock regime.

**Reality:** both conditions returned 24 findings and identical normalized score (`23.280`), but SCOC enabled changed structure to `scoc_chain` with a slightly higher `unit_cost_s` and slightly higher raw/sec probe estimate than baseline's direct multi-path. There was no closed-form normalized gain despite a structure shift.

## Problem alignment

This is a concrete Phase-3 readiness check for the SCOC lever: whether the route change yields measurable local scoring gain before any remote Kaggle action.

## Decision

T072 is complete and recorded as mechanics-only; the paired local result is **inconclusive on gain** (identical normalized score) and therefore does not yet justify a Kaggle-only SCOC rollout. It supports running a wider controlled matrix (including non-amortizing/legacy-style mock targets and additional seed points) before any confidence-gate submission move.

## Next steps

- Add a second Phase-3 local matrix across two additional target profiles:
  1. zero-overhead deterministic Compliant target with high context limits,
  2. Context-limited target with forced mid-fill breakdown.
- Compare SCOC-only wins versus fallback cost-bounding under identical budgets.
- If SCOC remains non-dominant on normalized score, run a targeted Kaggle dry-measurement only after an additional anti-regression control confirms a true net throughput or reliability benefit.
