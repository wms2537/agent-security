# Calibrated MPC-24 v5 static verification

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** completed

## Context

V5 narrows the primary claim to controlled Phase-3 validation, calibrates the
replay proxy on a held-out split, makes every online decision observable, binds
the historical generating state and freezes real component ablations.

## Frozen artifacts

| Artifact | Lines | SHA-256 |
|---|---:|---|
| `research-log/136-hypothesis-iter-5-mpc24-calibrated.md` | 640 | `ddd18c6c264e45c029c16e6649c1a86b0a225832168f560a01c624eefed11441` |
| `experiments/configs/mpc24-c3-v2.json` | 221 | `206b358496b5d3585aabb3bd5a2e6a5325198fdf62d71427efd15a55f1419bad` |
| `experiments/poc/mpc24_phase2_reference_v2.py` | 371 | `ef9686662c2856ec809cba22a2e10f44c1e81bf8611f3a85e0bba91930c1bdf3` |

## Deterministic verification

Exact command:

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_phase2_reference_v2.py --config experiments/configs/mpc24-c3-v2.json
```

Output:

```text
mpc24_phase2_author_check_v2=PASS
source_bindings=6
evidence_bindings=6
provenance_dependencies=9
replay_proxy=1.25*c_m+6.25*c_1
holdout_replay_envelope_coverage=54/54
proxy_controller_to_fixed8_ratio=1.443010752688
attribution_fixtures=3
plugin_decision_fixtures=4
only24_eligible_policy=choose1_or_drop
state_machine_fixtures=11
observable_deadline_fixtures=1
phase3_profiles=4
phase3_ablations=5
official_score_claim=withheld
review=not_dispatched
```

Additional checks:

- JSON parsing emitted `config_v2_json=PASS`;
- in-memory compilation of both author checkers emitted
  `python_compile=PASS`;
- `git diff --exit-code -- experiments/attack.py` emitted
  `attack_diff=EMPTY`;
- `git diff --check` returned no output;
- line counts and hashes match the frozen table.

## Gate Check

- Deterministic verification ladder: PASS.
- Round-4 replay/provenance/totality/ablation/claim-scope defects have executable
  author checks.
- Theory review: pending; budget remains `4/12` before dispatch.
- Phase 3, attack implementation and Kaggle mutation remain closed.

## Problem alignment

V5 turns the controller into a fair fixed-8 decision: only a safe, proxy-feasible
and ablation-supported controlled advantage can justify carrying its complexity
toward the competition.

## Decision

Commit v5, config, checker and state. Then dispatch one fresh sterile round-5
reviewer and charge `5/12`.
