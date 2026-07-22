# PRAC-24 Phase-2 author verification

**Date:** 2026-07-22
**Phase:** 2
**Cycle:** 3
**Task:** T050
**Status:** PASS, unreviewed

## Bound candidate

- hypothesis `research-log/164-hypothesis-iter-8-prac24.md`: 527 lines,
  SHA-256 `2a19b7537711be39cea01ca679821c3a5ab000ae11fa1109fa3987e1bdd53784`;
- config `experiments/configs/prac24-c3-v1.json`: SHA-256
  `a9b31a47ba5e9c665bfb8480c3eab9d5b0e7d616af8b7b2a64bcade13415fe38`;
- checker `experiments/poc/prac24_phase2_reference_v1.py`: SHA-256
  `caf2ceb0801dea86ea17315305215011b203f9b4283f1a5f1650699dc88ccf59`.

## Exact command

```bash
comp/.venv/bin/python -I experiments/poc/prac24_phase2_reference_v1.py \
  --config experiments/configs/prac24-c3-v1.json
```

## Exact output

```text
prac24_phase2_author_check_v1=PASS
source_bindings=5
evidence_bindings=9
precursor_status=invalid_disclosed
diagnosis=retrospective_only
calibration_unit=complete_unbudgeted_hcms_trace_profile_position_stratum
calibration_controller=noncircular_trace_capture
calibration_cells_per_stratum=19
cell_risk_alpha=0.050000
order_statistic_rank=19
censoring=positive_infinity
risk_multipliers=separate_replay_generation
absorbing_no_fit=true
calibration_evaluation_path_cap=16
contribution_components=4
clean_component_removals=4
removal_controls=present
williams_orders=4
directed_predecessor_pairs=12
minimum_primary_ratio=1.100000
maximum_q_replay=1.250000
maximum_q_generation=3.500000
target_remote_cancellation=false
official_score_claim=withheld
attack_unchanged=true
phase3_artifacts=absent
review=not_dispatched
```

## Adversarial author audit

The author pass corrected five issues before freezing this candidate:

1. calibration and evaluation now share an exact 16-path support cap;
2. q calibration is a noncircular wide-time trace capture, not a PRAC run that
   already requires q;
3. an atomic generation unit ends at a return-ready checkpoint rather than at
   the last interaction;
4. four claimed mechanisms have four isolated removals instead of one bundled
   legacy comparator; and
5. q-dependent adverse fixtures have exact formulas and explicit
   nondistinguishability outcomes, so they cannot be tuned after calibration.

Residual load-bearing objections are deliberately not declared resolved:

- profile-position exchangeability is an assumption, not established by fixed
  authored masters;
- the 0.95 statements are marginal per next latent HCMS trace, not conditional,
  simultaneous, control-wide or target-wide;
- controlled bounded fixtures cannot prove safety for uncancellable target
  `RemoteEnv` operations; and
- a valid controlled result has no official-score implication until a separate
  target-confidence bridge passes.

Therefore this is an author-consistent hypothesis candidate, not a rigorous
review verdict and not authorization to implement Phase 3.
