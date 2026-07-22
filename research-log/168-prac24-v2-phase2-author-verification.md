# PRAC-24 v2 Phase-2 author verification

**Date:** 2026-07-22
**Phase:** 2
**Cycle:** 3
**Task:** T052
**Status:** PASS, unreviewed

## Bound candidate

- hypothesis `research-log/167-hypothesis-iter-8-prac24-v2.md`: 533 lines,
  SHA-256 `5f495207251f9b63b64d631d564740ede61c8e0855b49e31381c0b143a2e0aa0`;
- config `experiments/configs/prac24-c3-v2.json`: SHA-256
  `ab2a4d871fe6db8cb4d150554260a958956b27ae139069cb07d6f7923195bb42`;
- checker `experiments/poc/prac24_phase2_reference_v2.py`: SHA-256
  `66dec6ccfd43af568515e5377eaf02bd816fcbb4768974dfae1f536f7ed69b00`.

## Exact command

```bash
comp/.venv/bin/python -I experiments/poc/prac24_phase2_reference_v2.py \
  --config experiments/configs/prac24-c3-v2.json --hypothesis research-log/167-hypothesis-iter-8-prac24-v2.md
```

## Exact output

```text
prac24_phase2_author_check_v2=PASS
hypothesis_lines=533
source_bindings=5
evidence_bindings=10
lineage_bindings=4
round8_issues_addressed=3
sampling_manifest=single_draw_no_retry
split=19_calibration_3_evaluation_per_profile
fisher_yates_demo_digest=96ce8ea1f9ee1ef4c25a290e44a0b30f0bfa9774bdfd2153b728006eb56e1575
capture_role_blinded=true
method_predecessor=none_matched_trace_projection
calibration_unit=complete_all_policy_potential_trace
cell_risk_alpha=0.050000
order_statistic_rank=19
empty_replay_score=0.0
censoring=positive_infinity
finite_q_conditioning_claim=forbidden
inherited_hcms_component_credit=false
contribution_components=3
clean_component_removals=3
replay_fixture_algebra_cases=1899
generation_fixture_algebra_cases=3075
evaluation_method_cells=36
official_score_claim=withheld
attack_unchanged=true
phase3_artifacts=absent
review=not_dispatched
```

## Round-8 issue audit

1. **Exchangeability repair:** calibration/evaluation are now a uniform random
   role split of q-independent complete potential traces. Role is hidden from
   capture, capture order is independently randomized, and every policy is an
   offline projection of the same held-out table. Method predecessor no longer
   exists in the efficacy estimand.
2. **Component contract repair:** HCMS is explicitly inherited and receives no
   contribution credit. The three new PRAC components each have one role, one
   measured antecedent bottleneck, one unique removal and one exact predicate.
3. **Candidate-boundary evidence repair:** the causal amortization claim is
   withdrawn rather than supported by the wrong aggregate ratio. The 1.10
   comparison remains only a prospective policy-retention endpoint.

Additional review coaching is bound: q coverage is never conditioned on finite
or sub-ceiling q, all held-out projections publish regardless of q, and the
empty replay-score convention is zero only when every PRAC stream is empty.

## Residual objections retained for re-review

- The role-split lemma depends on exact uniform `secrets.randbelow`, unbiased
  Fisher--Yates, a role-blind kernel and no outcome-dependent redraw.
- A potential-trace projection does not prove live controller performance or
  target exchangeability; v2 narrows the claim rather than hiding this.
- Authored profile families may still favor HCMS, so the 1.10 comparison is a
  controlled policy decision rather than a target mechanism estimate.
- The actual Phase-3 runner does not exist and must survive implementation and
  sterile code review after, and only after, a rigorous theory verdict.

This author pass is not a theory verdict. Review usage remains `8/12`, and no
Phase-3, attack or Kaggle action was performed.
