# PRAC-24 round-9 Occam and factorial-support audit

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** completed retrospective mechanism selection

## Context

The sterile round-9 review in `research-log/169-prac24-v2-theory-review-round-9.md`
resolved all three round-8 defects but rejected the three-component engineering
claim.  It identified one simpler explanation—absorbing on the first replay
ledger no-fit—and asked for a q-independent matched-trace factorial before the
replay envelope or atomic gate could receive component credit.

This audit asks what the already-sealed HCMS-24 attempt can identify.  The data
were seen before this audit, so the result is explicitly retrospective design
evidence, not a new confirmatory experiment.  The audit never executes the
scientific runner, mutates `experiments/attack.py`, or touches Kaggle.

## Audit question and non-blind expectation

The expected result was recorded from the round-9 review rather than claimed as
a fresh prediction:

1. the absorbing removal should be same-trace identifiable because the sealed
   retry trace contains the paths and outcomes after the first no-fit;
2. the replay-envelope removal should not be same-trace identifiable because
   `hcms_calibrated` and `hcms_scalar` were separate Williams-position
   executions and ledger-dropped paths lack replay potential outcomes; and
3. the atomic-gate removal should not be same-trace identifiable because every
   old method used the same point reserve and unstarted paths have no potential
   outcome.

## Read-only audit

The checker is `experiments/poc/prac24_round9_factorial_audit.py`.  It verifies
the sealed `COMPLETE.json` identity and all eleven artifact hashes before
reading `method_cells.tsv`, `paths.tsv`, and `candidates.tsv`.

Command:

```text
comp/.venv/bin/python -I experiments/poc/prac24_round9_factorial_audit.py
```

Decisive output:

```text
prac24_round9_factorial_audit=PASS
complete_artifacts=11
scientific_runner_executed=false
factorial_factors=replay_envelope,absorbing_no_fit,atomic_gate
full_two_cubed_factorial_estimable_cells=0
absorption_same_trace_estimable=true
absorption_estimable_primary_cells=96
primary_post_no_fit_paths=415
primary_post_no_fit_seconds=59.181928537553
hcms_post_no_fit_paths=146
hcms_post_no_fit_seconds=18.366501234705
primary_later_recovery_candidates=3
primary_later_recovery_raw=54.0
hcms_absorption_raw_loss=18.0
absorbing_hcms_raw=39240.0
hcms_raw_retention=0.999541494727
original_hcms_generation_s=69.903274593176
absorbing_hcms_generation_upper_s=51.536773358472
original_hcms_raw_per_s=561.604591895
absorbing_hcms_raw_per_s_lower=761.398074479
absorbing_efficiency_ratio_lower=1.355754716874
absorbing_hcms_to_best_simple_ratio=1.392971246006
generation_overages_without_absorption=4/144
generation_overages_with_absorption=0/144
hcms_aggregate_replay_overages=0/36
replay_removal_block_pairs=36
replay_removal_same_capture_pairs=0
dropped_paths_without_replay_outcome=426
replay_envelope_same_trace_estimable=false
zero_interaction_paths_gt_point_one=44/84
atomic_gate_same_trace_estimable=false
round9_occam_decision=claim_absorbing_no_fit_only
replay_envelope_status=unclaimed_prospective_guardrail
atomic_gate_status=unclaimed_prospective_guardrail
inference=retrospective_mechanism_selection_only
```

## What is and is not identified

### Absorption is a clean matched-trace removal

The retry trace observes every post-trigger path, so turning absorption on is
exactly a prefix truncation of the same stored trace.  Across the primary grid,
96 cells reached a first ledger no-fit.  Retry then spent 415 paths and
59.181928537553 seconds to recover three candidates worth 54 raw.  In HCMS
alone, absorption removes 146 paths and 18.366501234705 seconds while losing one
18-raw candidate.  It retains `39240/39258 = 0.999541494727` of raw.

Using only recorded path costs, the absorbing HCMS generation-time projection
is an upper bound of 51.536773358472 seconds.  Its raw/second is therefore a
lower bound of 761.398074479 versus 561.604591895 for retry, a conservative
ratio of 1.355754716874.  All four observed generation overages were after the
first no-fit, so the matched truncation removes them; all HCMS aggregate replay
endpoints were already below two seconds.

This is direct bottleneck evidence for one component.  It is not fresh-data
confirmation and it does not establish target prevalence.

### Replay-envelope credit is not identifiable

The 36 calibrated/scalar block pairs are separate captures at different
Williams positions and predecessor states: same-capture pairs are `0/36`.
More importantly, 426 primary ledger-dropped paths have no candidate replay
outcome.  Relaxing the ledger would admit some of those missing potential
outcomes.  Comparing the separately executed scalar method is a useful adverse
diagnostic, but not a one-field projection of a common trace.  A replay
envelope may remain a prospective safety monitor; it receives no contribution
credit here.

### Atomic-gate credit is not identifiable

All old methods used the same `0.1` point reserve.  The `44/84` zero-interaction
paths above that reserve establish reserve underestimation, but every observed
generation overage lies in the tail already removed by absorption.  There is no
stored outcome for an arm the stronger gate would decline to start.  The atomic
gate may remain a prospective conformance monitor; it receives no independent
engineering credit here.

### Why no retrospective `2^3` table is reported

A factorial row requires all factor combinations to be deterministic
projections of one complete potential trace.  The sealed artifact satisfies
that condition only for absorption.  Filling the other cells from separate
executions or q-dependent constructed fixtures would repeat the round-9 defect.
The correct factorial result is therefore `0` estimable complete cells, not a
fabricated eight-row table.

## Candidate critique and selection

Scores are `impact × feasibility / complexity`, each factor 1–5.

| Candidate | Most likely failure mode | Hardest implementation trap | Evidence check | I | F | C | Score | Decision |
|---|---|---|---|---:|---:|---:|---:|---|
| A. Preserve the three-component PRAC claim | conformance fixtures are mistaken for component necessity | silently splicing separate captures into a fake factorial | `0` complete factorial cells; replay/atomic same-trace estimability false | 5 | 1 | 4 | 1.25 | reject: repeats round-9 defect |
| B. Run a retrospective `2^3` factorial anyway | missing potential outcomes are imputed as observations | treating Williams block pairing as common-trace projection | `0/36` replay same-capture pairs and 426 ledger-dropped paths without replay outcomes | 4 | 1 | 5 | 0.80 | reject: not identified |
| C. Absorbing HCMS-24 (AHCMS-24) | fresh traces may contain little futile tail or meaningful recovery after no-fit | keeping the trigger and all controls exactly symmetric | direct same-trace removal; 99.954% raw retention and >=1.3558 efficiency ratio | 4 | 5 | 1 | **20.00** | **select** |

Candidate C is a local `replace` move: replace retry-after-replay-saturation
with one absorbing transition.  The HCMS proposal/salvage policy, point replay
ledger, point pre-path reserve, SDK mechanics, and evidence publication are
inherited controls, not claimed components.

## Decision

Supersede PRAC-24 v2 with a one-component AHCMS-24 hypothesis.  Its prospective
test must capture a complete q-independent retry trace fixed before outcomes,
then project absorption on/off over that same trace.  The primary comparison is
raw per generation second, constrained by at least 99.5% raw retention and
zero full-method overages.  Replay-envelope and atomic-gate calculations may be
reported only as unclaimed safety diagnostics; neither may enter the novelty or
ablation count.

The superseding hypothesis will also remove the ambiguous tied-rank statement.
If it retains the finite-population audit lemma for diagnostics, it will prove
coverage through the probability that the evaluation slot is the unique strict
maximum, so ties can only improve the bound.

## Problem alignment

This audit removes two unsupported components and isolates the only mechanism
with measured competition-relevant resource benefit, serving the requirement
that every added component earn its role before Kaggle action.

## Next Steps

1. Freeze a q-independent complete-trace AHCMS-24 contract and exact removal.
2. Write and author-check the superseding Phase-2 hypothesis.
3. Dispatch no reviewer and perform no Phase-3/Kaggle action until the next
   task.
