# AHCMS-24 v3 Phase-2 author verification

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** completed, unreviewed

## Context

Report 170 established that the sealed evidence has zero identifiable complete
`2^3` factorial cells.  Absorption alone has a genuine same-trace removal, so
`research-log/171-hypothesis-iter-8-ahcms24-v3.md` narrows the contribution to
one component and freezes a fresh q-independent matched-trace design.

## Verification

Command:

```text
comp/.venv/bin/python -I experiments/poc/ahcms24_phase2_reference_v3.py --config experiments/configs/ahcms24-c3-v3.json --hypothesis research-log/171-hypothesis-iter-8-ahcms24-v3.md
```

Output:

```text
ahcms24_phase2_author_check_v3=PASS
hypothesis_lines=632
source_bindings=5
evidence_bindings=10
lineage_bindings=3
round9_issues_addressed=4
full_two_cubed_factorial_estimable_cells=0
factorial_nonidentification_disclosed=true
sampling_manifest=single_draw_no_retry
fresh_units=3_profiles_x_3_masters
fisher_yates_demo_digest=25a3bb1e826b590f36d6c8f54c3e093e87544630fb6dc668ada49e809ffd6183
capture_q_independent=true
method_predecessor=none_matched_trace_projection
primary_comparison=absorbing_hcms_vs_retry_hcms
contribution_components=1
clean_component_removals=1
replay_envelope_component_credit=false
atomic_gate_component_credit=false
efficiency_identity_cases=81
strict_maximum_tie_cases=4
finite_population_claim_supports_engineering=false
projected_method_cells=36
official_score_claim=withheld
attack_unchanged=true
phase3_artifacts=absent
review=not_dispatched
```

The checker also re-runs the sealed round-9 audit, verifies every configured
source/evidence/lineage hash, proves the raw/work efficiency identity over 81
positive cases, checks tied and unique-maximum examples, confirms the one-field
primary pair, validates all thresholds and decision bands, and requires the
Phase-3 runner and canonical attempt to remain absent.

## Frozen identities

```text
cca5beccb50bea5d52f7fa9d7fcccf6ba05926cc8e6d4c71435b250414dcf35f  experiments/configs/ahcms24-c3-v3.json
3e6e1345a6e22d916ca68a0856b8830bf1f18c3b81984d4ef6c83bce3983b848  experiments/poc/ahcms24_phase2_reference_v3.py
dbd091908bea27630d57843b3887b656f70a1d080acc5f44a772e2570096db40  research-log/171-hypothesis-iter-8-ahcms24-v3.md
f07dc6ceb2f8401115423cef9262d504dfec81d466cbf7dffd2e13dfd7c09f92  experiments/poc/prac24_round9_factorial_audit.py
5dbad0dbc19956aa4214f3634a7db3a2e254d9e981e77f2cdf566f2589d23ed3  research-log/170-prac24-round9-occam-factorial-audit.md
8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d  experiments/attack.py
```

## Gate Check

- Deterministic author checker: **PASS**.
- Round-9 factorial nonidentification disclosed: **PASS**.
- One measured component and one clean same-trace removal: **PASS**.
- q-dependent component credit removed: **PASS**.
- Tied-rank wording corrected without supporting the engineering claim:
  **PASS**.
- Phase-3 runner/attempt absent: **PASS**.
- Attack and Kaggle state unchanged: **PASS**.
- Independent theory review: **not dispatched**.

## Problem alignment

The revision makes the competition solution smaller and more attributable:
only the event-aligned stop with direct resource evidence survives.

## Decision

The v3 artifact is ready for a later sterile round-10 re-review.  Phase 2
remains closed until a reviewer returns `RIGOROUS` with scrutiny evidence.  This
verification does not spend review budget and admits no Phase-3 or Kaggle work.

## Next Steps

Open exactly one task to obtain a sterile re-review with explicit disposition
of all four round-9 issues.
