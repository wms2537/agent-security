# HCMS-24 Phase-3 PoC implementation checkpoint

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Status:** implemented, unexecuted, awaiting sterile code review

## Files

- `experiments/poc/hcms24_phase3_v1.py` — one config-driven runner and shared
  method-cell kernel;
- `experiments/poc/test_hcms24_phase3_v1.py` — pure/toy checks only.

No existing file was changed by the implementer. The canonical scientific
attempt directory `experiments/runs/hcms24-c3-poc-v1` remains absent.

## Direct main-agent verification

Static source compilation:

```text
static_compile=PASS
```

Toy command:

```bash
comp/.venv/bin/python -I experiments/poc/test_hcms24_phase3_v1.py
```

Output:

```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.004s

OK
```

The initial generic `python -I -m unittest experiments/...` loader command
failed before importing project code because isolated mode does not expose
`experiments` as a package. The canonical direct-script command above passed;
this was a test invocation correction, not a code or scientific attempt.

## Implemented safeguards

- one `run_method_cell` kernel for all policies;
- runtime equality assertion for HCMS/scalar non-ledger fields;
- indexed trace-suffix attribution and exact prefix eligibility;
- cumulative endogenous replay-ledger charging and fresh actual replay;
- actual replay timing begins before fresh construction/reset;
- generation surrogate timing preserves antecedent reset+interaction convention;
- Williams configured and emitted-coordinate balance checks;
- delayed safety namespace and mechanical primary-only aggregation;
- per-candidate, path, method-cell, profile, method and primary artifacts;
- lexical/no-symlink command-first attempt validation;
- exclusive scientific outputs and COMPLETE-last hashes;
- no network, target, attack or Kaggle path.

## Scope and concerns for review

The implementer projects approximately 9–10 minutes on CPU, below the frozen
12-minute stop condition. No scientific timing has been observed.

The sterile review must not infer soundness from toy tests. It must inspect
timer boundaries, SDK/mock dependency binding, exact predicate/scorer identity,
exception preservation, ledger semantics, cell validity, safety exclusion,
output schemas, transaction behavior and whether the one command can produce a
complete auditable bundle without changing the reviewed experiment.

## Gate

- Predictions remain frozen and unpopulated in `results.tsv`.
- Scientific run/debug attempts used: `0/3`.
- Code-review verdict: pending.
- Phase-3 execution, Phase 4, attack mutation and Kaggle action remain closed.
