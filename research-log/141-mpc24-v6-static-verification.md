# Counterbalanced MPC-24 v6 static verification

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** completed

## Frozen artifacts

| Artifact | Lines | SHA-256 |
|---|---:|---|
| `research-log/140-hypothesis-iter-6-mpc24-counterbalanced.md` | 540 | `11d184befb428646b77d2af43ac3a44d75dd64a8967bb4905b22b64f668f84ea` |
| `experiments/configs/mpc24-c3-v3.json` | 151 | `af7cdcdc15fdeaaf1000897bf7db6d1fea843e5b91a0db8ebc98ff94c5c77752` |
| `experiments/poc/mpc24_phase2_reference_v3.py` | 157 | `63e5eb65b2b0a1388b35a5c5e76fa6f09bc3931727eebbdad490f03249696e34` |

## Verification

Command:

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_phase2_reference_v3.py --config experiments/configs/mpc24-c3-v3.json
```

Output:

```text
mpc24_phase2_author_check_v3=PASS
source_bindings=6
evidence_bindings=7
canonical_controlled_clock_fields=4
sentinel_admissible_at_time_zero=true
interaction_reserve_s=0.100000
generation_budget_s=6.000000
replay_budget_s=6.000000
outer_process_timeout_s=120.000000
phase3_profiles=4
counterbalanced_orders=4
methods=4
method_position_balance=1_each
strongest_simple_comparator=fixed8,fixed24,static3x24_1x8
minimum_mpc_to_best_simple_ratio=1.050000
contribution_components=2
correctness_controls=3
proxy_interpretation=correlated_scale_surrogate
taxonomy=resource_bottleneck_optimization_search_replace
official_score_claim=withheld
review=not_dispatched
```

Additional evidence:

- JSON parsing: `config_v3_json=PASS`;
- in-memory checker compilation: `python_compile=PASS`;
- attack implementation diff: `attack_diff=EMPTY`;
- `git diff --check`: empty;
- lines and hashes match the table.

## Gate Check

- Deterministic verification: PASS.
- Canonical clock, Latin-square balance, strongest-simple comparator and
  component/control separation are mechanically enforced.
- Theory review: pending; budget `5/12` before dispatch.
- Phase 3, attack implementation and Kaggle mutation remain closed.

## Problem alignment

The repaired protocol makes MPC compete against the best simple density policy
under a feasible, counterbalanced clock rather than winning by an impossible
budget, fixed execution order or weak comparator.

## Decision

Commit v6 and dispatch one sterile round-6 reviewer, charging `6/12`.
