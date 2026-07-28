# Stage A Runner Contract Restore

Date: 2026-07-28T17:18:46Z

## Finding

The repeated post-v16 blank-score / "Submission Format Error" path is not explained by malformed candidate objects or by the four-row CSV schema alone.

Evidence:

- Submission `55046504` (`diagnostic run 16: return_count default=500`) completed with public score `45.000`.
- The same Stage-A single-post candidate family therefore serializes, replays, and fires at `return_count=500`.
- Multiple `return_count=1950` Stage-A runs completed with blank public/private scores in the Kaggle CLI table.
- The latest notebook runner had drifted away from the known-good `81.225` family by adding a subprocess wrapper, multi-path placeholder writes, broad exception catching, and synthetic gateway-owned failure artifacts.

## Root-Cause Inference

There are two distinct blockers:

1. `return_count=1950` is not live-safe for this candidate latency profile until a one-factor count sweep proves otherwise. Treat those blank-score rows as replay/runtime invalidation, not as evidence that candidate serialization is broken.
2. The notebook runner must not catch `serve()` failures or synthesize gateway-owned artifacts. The known-good family writes only `/kaggle/working/submission.csv` as a commit-run placeholder and then directly calls `JEDAttackInferenceServer().serve()`.

## Repair

- Restored the notebook runner to the known-good direct-serve shape.
- Removed subprocess isolation and fallback artifact generation from the notebook.
- Set the default `return_count` back to `500`, the last live-valid count.
- Kept `AICOMP_RETURN_COUNT` override for controlled future sweeps.

## Validation

Local checks passed:

```text
comp/.venv/bin/python -m py_compile experiments/attack.py submission/build_notebook.py
comp/.venv/bin/python submission/build_notebook.py
notebook_contract_ok ai-agent-security-attack.ipynb cells 3 bytes 12807
notebook_contract_ok submission/kaggle_notebook.ipynb cells 3 bytes 12807
notebook_contract_ok submission/kernel/kaggle_notebook.ipynb cells 3 bytes 12807
attack_smoke_ok configured_return_count=7 smoke_count=5
```

## Next Gate

Do not jump back to `1950`.

Use the restored runner and reintroduce candidate count only through one-factor live sweeps, for example:

```text
500 -> 750 -> 1000 -> 1250
```

Advance only when the previous count completes with a visible score.
