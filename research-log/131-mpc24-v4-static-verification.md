# MPC-24 v4 static verification

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** completed

## Context

Round 3 rejected NPG-8's unsupported extrema-as-bounds, incomplete fallback
portfolios, missing objective, absent branch fixtures, indirect evidence binding
and incomplete generation-to-replay scope. V4 replaces that hypothesis with a
monotone 24-to-8-to-1 controller and must pass deterministic checks before one
budgeted reviewer is dispatched.

## Frozen artifacts

| Artifact | Lines | SHA-256 |
|---|---:|---|
| `research-log/130-hypothesis-iter-4-mpc24.md` | 745 | `ac1592714ba28df9b740a5edb6592a0dc2e729a8d6afb5ca2aa5f4f7f48ea9e3` |
| `experiments/configs/mpc24-c3-v1.json` | 308 | `6eb251d101ce4b0db2f6e22380dbbc9c7ce401f285b56ecba71375ccced5466f` |
| `experiments/poc/mpc24_phase2_reference.py` | 417 | `e388fe7eaf8ade9950e7b94600da3c0400376403c4e654bc0d647beffa182008` |

The checker is an author-side specification verifier, not attack or Phase-3
implementation.

## Verification

Exact command:

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_phase2_reference.py --config experiments/configs/mpc24-c3-v1.json
```

Output:

```text
mpc24_phase2_author_check=PASS
source_bindings=6
evidence_bindings=5
mpc24_evidence_audit=PASS
artifact_rows=360
short_frontier_fixed8_wins=9/9
full_frontier_split=24:6/9,8:3/9
heldout_aggregate_ratio=1.507376725838
attribution_fixtures=3
plugin_decision_fixtures=3
state_machine_fixtures=9
occam_failure_fixtures=1
round3_issue_fixtures=6
phase3_profiles=3
phase3_cells=9
plugin_semantics=point_estimate_not_bound
review=not_dispatched
```

Additional deterministic evidence:

- `python -m json.tool experiments/configs/mpc24-c3-v1.json` exited zero and
  emitted `config_json=PASS`.
- in-memory Python compilation emitted `checker_compile=PASS`.
- `git diff --exit-code -- experiments/attack.py` exited zero and emitted
  `attack_implementation_diff=EMPTY`.
- `wc -l` returned hypothesis/config/checker lines `745/308/417`.
- `sha256sum` returned the three hashes in the table above.

## Round-3 defect closure checked at the deterministic rung

1. Plug-in semantics are literally frozen as `point_estimate_not_bound`.
2. Nine state-machine fixtures cover sentinel 24/8/1/drop, first/late
   regression, incomplete sentinel, replay binding and candidate cap.
3. The exact `n_hat_m` and `P_hat_m` objective is executable.
4. Six source and five evidence artifacts match their frozen hashes.
5. Trace content and interaction counts are distinct contracts in the checker.
6. One adverse fixture proves fixed-8 can beat MPC after sentinel overhead.

These are author checks, not an independent rigor verdict.

## Gate Check

- Deterministic verification ladder: **PASS**.
- Hypothesis immutable only after this group is committed and review dispatched.
- Theory review: pending; budget remains `3/12` before dispatch.
- Phase 3, attack implementation and Kaggle mutation remain closed.

## Problem alignment

The state-machine specification tests the only measured heterogeneous
multiplicity boundary while preserving exact resource accounting and exposing
fixed-8 as the simpler solution whenever sentinel overhead erases value.

## Decision

Commit the hypothesis, config, checker and state record explicitly. Only then
dispatch one fresh sterile theory reviewer and charge review round 4.
