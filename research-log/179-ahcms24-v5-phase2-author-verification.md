# AHCMS-24 v5 Phase-2 author verification

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 3 · **Status:** completed

## Context

`research-log/178-hypothesis-iter-8-ahcms24-v5.md` supersedes immutable v4 after sterile round-11 review found a mismatched monotonic-clock construct and an incorrect positive-retry/all-zero-AHCMS-and-simple branch. This entry records lower-rung verification before the final review round is dispatched.

No scientific runner, held-out/Kaggle action, attack mutation, or Phase-3 attempt occurred.

## Immutable candidate identities

```text
1d0e1128b4179b56604a00c60ad7461449f98815eb78ab1f85590da93f752715  experiments/configs/ahcms24-c3-v5.json
b33c612ce930779d56446fd2e82ff3ced6c207385f0d3b0c8b5a36d24d2ecd84  experiments/poc/ahcms24_phase2_reference_v5.py
1877c5023d16addcd029a9a9d9cacbbe34b5213deef9faa8bd9c86f8dc0025bb  research-log/178-hypothesis-iter-8-ahcms24-v5.md
304484543ce7471526408234f13fe83a5277bf756b10b11fcca891e5a47acf7d  experiments/poc/ahcms24_round11_timer_audit.py
b93ad5b7f544eb6bc4e46c217cab3dff5fad0ea65c806388d545e33a13335415  research-log/177-ahcms24-round11-timer-boundary-audit.md
8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d  experiments/attack.py
```

Hypothesis line count: `654`.

## Source/timer audit

Command:

```bash
python -I experiments/poc/ahcms24_round11_timer_audit.py
```

Verified output:

```text
ahcms24_round11_timer_audit=PASS
scientific_runner_executed=false
generation_start=before_generation_environment_checkpoint
generation_end=after_last_interaction_complete_checkpoint_before_exact_prefix_selection
generation_includes=checkpoint_serialization,environment_construction,reset,interactions,in_interval_scheduling
generation_excludes=exact_prefix_extraction,candidate_selection,publication,artifact_fsync
replay_start=before_replay_environment_checkpoint
replay_end=after_last_interaction_complete_checkpoint_before_final_trace_and_scorer
replay_includes=checkpoint_serialization,environment_construction,reset,interactions,in_interval_scheduling
replay_excludes=final_trace_export,predicates,signature,scorer,publication,artifact_fsync
clock_interpretation=captured_elapsed_not_cpu_time_or_remote_deadline_proof
historical_retry_paths=370
historical_retry_elapsed_s=69.00197669875342412
historical_retry_tail_paths=146
historical_retry_tail_elapsed_s=18.36650123470462862
historical_absorbing_elapsed_s=50.63547546404879550
historical_nominal_efficiency_ratio=1.362095216773
historical_half_tail_efficiency_ratio=1.180818355750
historical_half_tail_fraction=0.153517990418
prospective_sensitivity=charge_only_half_retry_tail_elapsed_keep_all_retry_raw
scheduler_bound_scope=bounded_sensitivity_not_arbitrary_or_systematic_noise_guarantee
```

The correction deliberately excludes whole-cell `generation_elapsed_s` from the historical ratio. Both historical sides and future `T_m` now sum only source-audited `path_cost` brackets.

## Deterministic hypothesis/config checker

Command:

```bash
python -I experiments/poc/ahcms24_phase2_reference_v5.py \
  --config experiments/configs/ahcms24-c3-v5.json \
  --hypothesis research-log/178-hypothesis-iter-8-ahcms24-v5.md
```

Verified output:

```text
ahcms24_phase2_author_check_v5=PASS
hypothesis_lines=654
source_bindings=5
evidence_bindings=8
lineage_bindings=4
round11_required_fixes_addressed=2
endpoint=projected_captured_elapsed_at_historical_brackets
in_interval_scheduler_and_controller_elapsed=included
historical_profile_sum=path_cost_s_only
historical_whole_cell_generation_elapsed=excluded
generation_end=before_exact_prefix_and_selection
replay_end=before_final_trace_and_scorer
overage_boundary_ns=2000000000_strict_greater
elapsed_accounting_fixture_cases=15
primary_threshold_cases=10
scheduler_sensitivity_cases=5
scheduler_sensitivity=half_retry_tail_floor_keep_all_retry_raw
scheduler_sensitivity_scope=bounded_not_arbitrary
denominator_totality_cases=6
zero_retry_raw=disconfirm
zero_ahcms_positive_retry=primary_and_retention_disconfirm
zero_ahcms_zero_simple_positive_retry=simple_cross_product_defined
zero_simple_raw_diagnostic=NA_zero_simple_raw
simple_control_fixture_cases=7
simple_control_exhaustive_cases=5184
simple_controls=specified_not_exhaustive
reduced_global_path_cap=unresolved_alternative
raw_prefix_scoring_cases=3
retention_tail_relation=consistency_not_independent_evidence
sampling_manifest=single_draw_no_retry
fresh_units=3_profiles_x_3_masters
method_predecessor=none_matched_trace_projection
official_score_claim=withheld
attack_unchanged=true
phase3_artifacts=absent
review=not_dispatched
```

## Boundary and adversarial cases

The checker executes, rather than merely searches for:

1. positive generation and nonnegative replay duration domains, including Boolean rejection;
2. equality/pass and strict-greater/overage cases at `2_000_000_000 ns`;
3. nominal primary, retention, and tail threshold crossings;
4. floor-half behavior for odd retry-tail nanoseconds;
5. a nominal-pass/sensitivity-fail construction;
6. discounted-tail support pass/fail boundaries;
7. `R_retry=0` deterministic disconfirmation and sentinels;
8. `R_ahcms=0,R_retry>0` primary/retention disconfirmation;
9. `R_ahcms=R_simple=0,R_retry>0`, where the simple cross-product is defined, Pareto remains elapsed-sensitive, and legacy `rho_simple` is `NA_zero_simple_raw`;
10. 5,184 raw/elapsed simple-control combinations including the all-zero-raw Pareto corner;
11. set-aware scorer nonadditivity within and across units; and
12. historical runner, evidence, source, lineage, attack, and absent-Phase-3 identities.

## Static and boundary checks

```text
syntax_and_json_parse=PASS
phase3_artifacts=absent
git diff --check -> empty
attack sha256=8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d
```

## Round-11 author disposition

1. **Elapsed construct/profile alignment — addressed for review.** The endpoint is captured elapsed at the exact historical brackets; in-bracket scheduler/controller time is included. Historical ratio now uses only `path_cost_s`. Replay ends before scorer in both artifacts. A prespecified 50% retry-tail discount is mandatory and its stronger validity limit is explicit.
2. **Positive-retry all-zero AHCMS/simple branch — addressed for review.** Primary and retention disconfirm; simple cross-product stays defined; zero-simple diagnostic uses the sentinel. Dedicated and exhaustive fixtures execute it.
3. **Occam coaching — adopted without claim expansion.** Fixed8/fixed24 are specified controls only; reduced global path cap remains a named unevaluated alternative.

These are author claims pending independent judgment. They do not declare the theory gate passed.

## Gate Check

- Config parses and binds source/evidence/lineage: **PASS**.
- Historical timer AST/source audit: **PASS**.
- Hypothesis/config deterministic contract: **PASS**.
- Numeric/sensitivity/zero-branch fixtures: **PASS**.
- Attack unchanged: **PASS**.
- Phase-3 artifacts absent: **PASS**.
- Hypothesis review budget: unchanged at `11/12`.
- Independent theory verdict: **not dispatched; Phase 2 remains closed**.

## Problem alignment

The repair makes the engineering endpoint reproducible and stressable without translating local elapsed measurements into unsupported Kaggle deadline or score claims.

## Decision

Freeze v5 at its committed identity and open a separate final theory-review task. Do not begin Phase 3 unless the sterile reviewer returns `RIGOROUS` with evidence of scrutiny.

## Next Steps

Commit v5 and this verification record, close T058, and open the final sterile review as the sole next task. Charge review `12/12` only at dispatch in that later task.
