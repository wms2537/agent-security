# AHCMS-24 v4 Phase-2 author verification

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** completed, unreviewed

## Context

Round-10 theory review resolved every earlier structural issue but rejected v3
on three contract defects: a raw-only Occam comparator, undefined resource-work
boundaries, and undefined raw-denominator branches.  Hypothesis 174 and config
v4 repair those issues without changing the one-component AHCMS mechanism or
running fresh traces.

During author self-audit, the raw contract was also tightened to respect the
SDK scorer's nonadditive unique-cell bonus: each method-unit is scored once,
units are aggregated afterward, and retry-tail raw is a marginal difference.

## Verification

Command:

```text
comp/.venv/bin/python -I experiments/poc/ahcms24_phase2_reference_v4.py --config experiments/configs/ahcms24-c3-v4.json --hypothesis research-log/174-hypothesis-iter-8-ahcms24-v4.md
```

Output:

```text
ahcms24_phase2_author_check_v4=PASS
hypothesis_lines=686
source_bindings=5
evidence_bindings=11
lineage_bindings=4
round10_issues_addressed=3
simple_control_endpoint=feasible_efficiency_plus_pareto
legacy_rho_simple_decision_role=retired
generation_overage_boundary_ns=2000000000_strict_greater
aggregate_replay_overage_boundary_ns=2000000000_strict_greater
generation_metric=projected_work_not_wall_clock
replay_metric=accepted_candidate_actual_replay_projected_sum
resource_accounting_fixture_cases=13
denominator_totality_cases=4
zero_retry_raw=disconfirm
zero_simple_raw=positive_over_zero_or_diagnostic_sentinel
simple_control_fixture_cases=6
simple_control_exhaustive_cases=4608
primary_threshold_cases=9
raw_prefix_scoring_cases=3
retention_tail_relation=consistency_not_independent_evidence
full_two_cubed_factorial_estimable_cells=0
sampling_manifest=single_draw_no_retry
fisher_yates_demo_digest=25a3bb1e826b590f36d6c8f54c3e093e87544630fb6dc668ada49e809ffd6183
fresh_units=3_profiles_x_3_masters
method_predecessor=none_matched_trace_projection
contribution_components=1
clean_component_removals=1
official_score_claim=withheld
attack_unchanged=true
phase3_artifacts=absent
review=not_dispatched
```

Additional deterministic checks:

```text
comp/.venv/bin/python -m py_compile experiments/poc/ahcms24_phase2_reference_v4.py
jq empty experiments/configs/ahcms24-c3-v4.json
git diff --check
```

All three commands exit `0`.  `ruff` is unavailable in the pinned environment,
so no ruff result is claimed.

## What the checker establishes

- all bound source, sealed evidence and superseded-lineage identities match;
- the sealed round-9 profile audit still reconstructs the one measured
  absorption bottleneck and zero complete old `2^3` cells;
- generation work includes the triggering path and uses a strict integer
  nanosecond overage boundary;
- aggregate replay work uses only ledger-accepted occurrences, actual captured
  replay durations, an empty-sum rule and the same strict boundary;
- retry-zero-raw, simple-zero-raw and positive-domain branches are total;
- raw-only `rho_simple` has no decision role;
- each feasible simple control faces the same efficiency cross product and
  exact Pareto guard, while infeasible controls remain published;
- 4,608 small-domain cases prove that a feasible simple cannot both dominate
  AHCMS and lose the `1.10` efficiency comparison;
- per-unit scorer fixtures cover new-cell, duplicate-cell, zero-prefix and
  cross-unit nonadditivity boundaries; and
- the Phase-3 runner/attempt remain absent and `experiments/attack.py` remains
  unchanged.

## Frozen identities

```text
8f1a49163fa36c63c72227ae95f1b260112a4219eb455aeff7fe92f531ff5b51  experiments/configs/ahcms24-c3-v4.json
030c8e9928ccdc6b567cba5b6e1fc5dedb4fceb17c3cc647f71e0e5d0f7f119f  experiments/poc/ahcms24_phase2_reference_v4.py
4e66cab8f8e0aa5c155332303cfaa7e2110e3b181e9904c55bc36f87ea55032f  research-log/174-hypothesis-iter-8-ahcms24-v4.md
f07dc6ceb2f8401115423cef9262d504dfec81d466cbf7dffd2e13dfd7c09f92  experiments/poc/prac24_round9_factorial_audit.py
5dbad0dbc19956aa4214f3634a7db3a2e254d9e981e77f2cdf566f2589d23ed3  research-log/170-prac24-round9-occam-factorial-audit.md
ef8c4e56931e9d71089bdf2bd595b939137d59250ce4416a22df7ef018fefa80  research-log/173-ahcms24-v3-theory-review-round-10.md
8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d  experiments/attack.py
```

## Gate Check

- Deterministic author checker: **PASS**.
- Round-10 issue coverage: **3/3 author PASS**.
- Endpoint-aligned constrained Occam rule: **author PASS**.
- Generation/replay formulas and strict boundaries: **author PASS**.
- Denominator and scorer-boundary totality: **author PASS**.
- One measured component and one clean removal: **author PASS**.
- Phase-3 runner/attempt absent: **PASS**.
- Attack and Kaggle state unchanged: **PASS**.
- Independent theory review: **not dispatched**.

## Problem alignment

V4 makes the proposed competition optimization measurable on the exact
resource/value endpoint it claims, so a later controlled result can inform
allocation without being mistaken for remote safety or leaderboard evidence.

## Decision

T056 is author-complete.  Freeze config v4, checker v4 and hypothesis 174 as an
unreviewed unit.  Phase 2 remains closed.  A later task may spend round 11 on a
fresh sterile re-review containing exactly the three round-10 issues; no Phase
3 or Kaggle action is admitted by this verification.

## Next Steps

Open one task for a sterile v4 theory re-review after the frozen identities are
committed.  Do not implement or execute the Phase-3 runner unless that review
returns `RIGOROUS` with scrutiny evidence.
