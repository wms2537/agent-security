# AHCMS-24 round-11 timer-boundary audit

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 3 · **Status:** completed

## Context

Sterile theory review round 11 (`research-log/176-ahcms24-v4-theory-review-round-11.md`) found that v4 called `time.monotonic_ns` a work measure, falsely excluded scheduler delay, and did not align its proposed endpoints with the timer brackets that produced the historical profile. This audit repairs the evidentiary premise before v5 is written. It is read-only: it does not execute a scientific runner, construct a Phase-3 attempt, mutate `experiments/attack.py`, contact Kaggle, or create held-out evidence.

## Bound source

- Historical runner: `experiments/poc/hcms24_phase3_v1.py`
- Runner SHA-256: `7b030c67a7f18c4bce77db67f7db757b817aede7cbaf75aa1195a09d42f6b1f6`
- Sealed attempt: `experiments/runs/hcms24-c3-poc-v1`
- `COMPLETE.json` SHA-256: `34e9dc0274e0828f325cb280b2f392a6e867fabf4315c0c962cf3746dc200b07`
- Audit program: `experiments/poc/ahcms24_round11_timer_audit.py`
- Audit-program SHA-256: `304484543ce7471526408234f13fe83a5277bf756b10b11fcca891e5a47acf7d`

The checker parses the pinned runner's AST, extracts the exact `run_method_cell`, `replay_candidate`, and `checkpoint_in_flight` function bodies, and verifies the timer landmarks occur in the order described below. The whole-file hash makes those local ordering checks statements about one immutable source object.

## Historical generation-path bracket

The timer starts at `path_started = time.monotonic()` immediately before the `generation_environment_construction` checkpoint. It ends at `path_cost = max(1e-9, time.monotonic() - path_started)` after the interaction loop and its last `generation_interaction_complete` checkpoint, but before `indexed_exact_flags`, `choose_return_prefix`, path-state transition, candidate assembly, path publication, and artifact persistence.

Therefore the recorded interval includes:

1. the in-flight checkpoint calls and their canonical JSON snapshot serialization when `phase_state` is enabled;
2. fresh generation-environment construction;
3. reset, trace exports, interactions, suffix/cumulative-cost updates, and interaction-complete checkpoints inside the bracket; and
4. garbage collection, preemption, OS scheduling delay, or other host elapsed time that occurs between the two monotonic-clock reads.

It excludes pre-timer host/message construction, exact-prefix extraction, controller selection and transition after the timer, candidate/path assembly, publication checkpoints, and TSV/JSON artifact serialization or fsync. Calling it CPU work, active compute, or scheduler-free time is false. The accurate construct is **captured generation-path elapsed time at the historical bracket**.

## Historical replay bracket

The timer starts at `started = time.monotonic()` before the replay-environment-construction checkpoint and fresh environment construction. It ends at `elapsed = max(1e-9, time.monotonic() - started)` after the interaction loop and its final interaction-complete checkpoint, but before the final trace export, replay-evaluation checkpoint, predicates, signature construction, and `score_attack_raw` call.

Thus it includes in-bracket checkpoint serialization, fresh replay environment construction, reset, trace exports, interactions, suffix updates, and host scheduling/preemption. It excludes the final trace export and every scoring operation after the timer, plus publication and artifact fsync. The accurate construct is **captured accepted-candidate replay elapsed time at the historical bracket**, not scorer-complete replay work.

## Clock representation for v5

The historical runner stored floating-point seconds from `time.monotonic`; v5 will use integer differences from `time.monotonic_ns` while preserving the same start/end landmarks. This changes representation and boundary comparison precision, not the interval being operationalized. Integer sums compare to exactly `2_000_000_000 ns`; equality passes and only strict greater-than is overage.

An elapsed interval cannot identify CPU service time. V5 therefore makes no claim that controller work or scheduler effects are removed. A sum over several independently captured intervals is a **projected captured-elapsed sum**, not actual method wall-clock, target latency, or a remote-deadline certificate.

## Retrospective profile recomputation

The old sealed primary HCMS traces contain:

- 370 retry generation paths;
- retry captured generation-path elapsed, computed only as the sum of those paths' `path_cost_s`: `69.00197669875342412 s`;
- 146 paths after the first replay no-fit;
- retry-tail captured elapsed: `18.36650123470462862 s`;
- absorbing projection captured elapsed: `50.63547546404879550 s`;
- absorbing raw `39,240`; retry raw `39,258`; and
- nominal absorbing/retry raw-per-captured-elapsed ratio: `1.362095216773`.

Both sides of this ratio now use exactly the same quantity proposed for v5: sums of `path_cost_s` intervals. Whole-cell `generation_elapsed_s` is deliberately excluded because it also spans post-timer exact-prefix selection, candidate/path assembly, publication checkpoints, and inter-path controller work. These values therefore establish a path-count-associated elapsed bottleneck at the same timer bracket, not a decomposition of CPU, scheduler, or controller time.

## Bounded scheduler-noise sensitivity

Two conservative recalculations leave all retry raw credited while discounting retry-only elapsed:

1. Deleting the single largest retry-tail interval (`0.17478107300121337 s`) yields an efficiency ratio of `1.358645048025`.
2. Charging only half of every retry-tail interval yields an efficiency ratio of `1.180818355750`; the discounted tail remains `0.153517990418` of the discounted retry total.

V5 will pre-specify the second, stronger perturbation as a confirmation guard on fresh traces: in addition to the nominal rules, replace retry elapsed `T_r=T_a+T_tail` with `T_r^(1/2)=T_a+T_tail/2`, retain all retry raw, and require both the `1.10` efficiency inequality and `0.10` tail-support inequality to pass. This says the result survives a bounded model in which half of every retry-only elapsed interval is measurement inflation.

It does **not** bound arbitrary or systematic host asymmetry. If more than half of retry-tail elapsed is treated as unrelated scheduling/controller inflation, or if the fresh capture violates the randomized/order and completeness contract, the broader efficiency interpretation is unsupported. The prospective fixed-sample result remains a controlled-harness result.

## Verification

Command:

```bash
python -I experiments/poc/ahcms24_round11_timer_audit.py
```

Key output:

```text
ahcms24_round11_timer_audit=PASS
scientific_runner_executed=false
clock_interpretation=captured_elapsed_not_cpu_time_or_remote_deadline_proof
historical_nominal_efficiency_ratio=1.362095216773
historical_delete_largest_tail_efficiency_ratio=1.358645048025
historical_half_tail_efficiency_ratio=1.180818355750
historical_half_tail_fraction=0.153517990418
prospective_sensitivity=charge_only_half_retry_tail_elapsed_keep_all_retry_raw
scheduler_bound_scope=bounded_sensitivity_not_arbitrary_or_systematic_noise_guarantee
```

## Problem alignment

This audit keeps the competition-oriented engineering claim tied to an observable, reproducible elapsed-time endpoint while preventing a controlled monotonic-clock profile from being misreported as target compute or deadline safety.

## Decision

Historical seconds remain admissible as an engineering profile only under these exact source-audited brackets and the narrowed captured-elapsed interpretation. V5 must encode the same brackets, include in-interval scheduling/controller work, add the half-tail sensitivity guard, and retain the remote/Kaggle claim hold.

## Next Steps

Write and deterministically author-check AHCMS-24 v5. Do not dispatch the final theory review until all zero-denominator and endpoint-boundary fixtures pass.
