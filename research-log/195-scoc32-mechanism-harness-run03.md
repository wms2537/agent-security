# T070 — SCOC-32 mechanism harness execution and anti-stacking signal check

**Date:** 2026-07-23 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 4/5 · **Status:** done

## Task

Run the SCOC frozen mechanism harness with explicit local-role simulation for all comparison arms:

- `SINGLE_FULL`
- `CHAIN_FULL`
- `CHAIN_COMPACT_EXPLICIT`
- `CHAIN_SCOC`
- `CHAIN_GENERIC`
- `CHAIN_BLOCKED_ANCHOR`
- `COLD_OPERAND_ONLY`

with exact-length candidates and exact-overlap proxy against `SINGLE_FULL`.

## Verification commands

- `comp/.venv/bin/python -m py_compile experiments/mock_agents.py experiments/scoc32_mechanism_harness.py`
- `PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/scoc32_mechanism_harness.py --candidates 12 --seed 42 --lengths 1 4 8 16 24 32 --max-hops 8 --out-dir artifacts/scoc32/run03`
- `python - <<'PY' ...` coverage/raw summary extraction from `artifacts/scoc32/run03/scoc32-mechanism-harness.json`

## Evidence

1. Harness and agent-mode instrumentation compiled successfully; no syntax/runtime import issues remain after the script-level refactor.
2. Harness run completed for all lengths `m ∈ {1,4,8,16,24,32}` with `candidates=12`, `seed=42`, `max_hops=8`.
3. Output artifacts:
   - `artifacts/scoc32/run03/scoc32-mechanism-harness.json`
   - `artifacts/scoc32/run03/scoc32-mechanism-harness.tsv`
4. Gate-relevant findings from the run:
   - `CHAIN_SCOC`: coverage `1.000` for every tested `m` (not filtered).
   - `CHAIN_COMPACT_EXPLICIT`: coverage `1.000` for every tested `m`.
   - `CHAIN_GENERIC`: coverage `1.000` for every tested `m`.
   - `CHAIN_BLOCKED_ANCHOR`: coverage `0.000` for all tested `m`.
   - `COLD_OPERAND_ONLY`: coverage `0.000` for all tested `m`.
5. Anti-stacking implications:
   - `CHAIN_BLOCKED_ANCHOR` and `COLD_OPERAND_ONLY` fail the source-compatibility coverage gate and do not qualify as viable transfer alternatives.
   - `CHAIN_SCOC` remains mechanistically distinct from `CHAIN_COMPACT_EXPLICIT`/`CHAIN_GENERIC` in runtime profile at several lengths, though compact/generic often show higher measured raw-per-second at this local proxy.

## Machine-readable close

```text
t070_scoc32_mechanism_harness=PASS mode=mechanism_compare lengths=1,4,8,16,24,32 candidates=12 out_dir=artifacts/scoc32/run03 blocked_anchor_coverage=0.000 cold_operand_coverage=0.000 scoC_min_coverage=1.000 generic_min_coverage=1.000 compact_min_coverage=1.000 parent=T069
```
