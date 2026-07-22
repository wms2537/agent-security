# MPC-24 symmetry and Occam audit result

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** selector refuted; pivot selected

## Frozen execution

Protocol and predictions were committed at `784706c` before the one exact
read-only invocation:

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_symmetry_occam_audit.py
```

Verbatim stdout:

```text
mpc24_symmetry_occam_audit=PASS
antecedent_artifact_status=FAIL
analysis_scope=exploratory_independent_arm_proxy_not_nested_phase3
artifact_rows=360
cells=9
static_primitive_patterns=106
static_period_limit=6
fixed8_aggregate_raw=12090.000000
fixed24_ceiling_aggregate_raw=17446.000000
fixed24_no_salvage_aggregate_raw=10036.000000
mpc_calibrated_aggregate_raw=17446.000000
best_static_pattern=24
best_static_aggregate_raw=17446.000000
mpc_first_state_matches_fixed24_ceiling=9/9
mpc_to_fixed24_ceiling_ratio=1.000000000000
selector_incremental_gain_fraction=0.000000000000
calibrated_mpc_actual_replay_overage_cells=0/9
scalar_mpc_actual_replay_overage_cells=7/9
decision=retire_selector_pivot_to_high_ceiling_salvage
official_target_inference=none
runtime_s=0.099020520
```

Frozen script SHA-256:
`1482abbf1693d9e146177ba547cccccdb5cfff6309e4794f0a558771c2d1c5c2`.

## Prediction ledger

| Metric | Frozen prediction | Result | Signal |
|---|---:|---:|---|
| MPC/fixed24-ceiling first-state match | `9/9` | `9/9` | confirm |
| MPC/fixed24-ceiling aggregate ratio | `<=1.01` | `1.000000000000` | confirm |
| best primitive static pattern | `[24]` | `[24]` | confirm |
| scalar-ledger actual replay overage | `>=1/9` | `7/9` | confirm |
| calibrated-ledger actual replay overage | `0/9` | `0/9` | confirm |

## Interpretation

The v6 selector does not survive the strongest symmetric simple explanation.
Once every method receives the same longest-prefix salvage and permanent
downgrade behavior, always proposing ceiling 24 makes the same initial 24/8
choice as MPC in all nine retained cells and obtains the same aggregate raw.
The selector therefore adds machinery but no measured value in its motivating
artifact.

Two parts do survive:

1. **High ceiling plus monotone salvage.** Removing salvage from fixed 24 lowers
   aggregate raw from `17,446` to `10,036`, a retained-artifact ratio of
   `1.738142686329`. The three natural context-cliff cells are prior measured
   evidence for this component; no purpose-built delayed fixture is needed.
2. **Calibrated replay accounting.** The calibrated controller has zero actual
   replay overage cells, while a full retrospective scalar-ledger controller
   overruns in seven of nine. The future experimental ablation must still run
   as its own end-to-end method because this audit uses independent-arm data.

Fixed 8 is also materially weaker in this retrospective kernel:
`17,446 / 12,090 = 1.443010752688`. This is the same measured direction as the
earlier replay audit, now explained by the simpler high-ceiling salvage policy
rather than a portfolio selector.

## Scope and bias

- The antecedent run is explicitly `FAIL` (`6/9` original decisions passed).
- This is a post-hoc reuse designed to reject or retain a mechanism, not confirm
  a fresh predictive hypothesis.
- Prefixes use independent arm measurements; no nested timing was observed.
- Point-cost admission knows frozen costs and is not an online deadline rule.
- The three profile families and masters are authored and previously inspected.
- No official target, private guardrail, leaderboard, or Kaggle action occurred.

## Decision

Apply the frozen adverse rule: retire MPC-24's multiplicity selector and close
T047 without implementation. Open a new Phase-2 direction, High-Ceiling
Monotone Salvage-24 (HCMS-24), whose only empirical contribution components are:

- ceiling-24 with longest eligible-prefix salvage and permanent downgrade;
- calibrated replay-surrogate accounting.

The superseding hypothesis must use one shared kernel for all methods, exclude
purpose-built safety fixtures from efficacy, run scalar accounting as a true
end-to-end ablation, and make no official-score claim without a separate target
confidence bridge.

## Gate

- Research usage remains `3/5`; execution was the frozen iteration-3 audit.
- Hypothesis-review usage remains `6/12`.
- Phase 2 remains open. HCMS-24 is not yet frozen or reviewed.
- Phase 3, `experiments/attack.py`, Kaggle mutation and submission remain closed.
