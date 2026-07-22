# NPG-8 v3 static verification

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 1 · **Status:** completed — review pending

## Context

Research-log/125 supersedes RCMF v2 with Nested Prefix Gate-8. This note records
the deterministic rung of the verification ladder before any budgeted theory
review.

## Bound artifacts

| Artifact | Lines | SHA-256 |
|---|---:|---|
| `research-log/125-hypothesis-iter-3-npg8.md` | 674 | `0346d0c472bb3d75ca812b44f7180f281c0fdf80a5490a708ee3ed530be54c29` |
| `experiments/configs/npg8-c3-v1.json` | 160 | `b76af5976dbc9fbe65b93cb636559a08de04e9c0943fccd1a6cf847705e32a9c` |
| `experiments/poc/npg8_phase2_reference.py` | 280 | `28503c2046ebb3271af1284b7e47932625086e52082028c5949028f893e9b81d` |

The config binds five scorer/gateway/SDK source files and the exact base attack
bytes at commit `8c44eb4`.

## Deterministic author check

Exact command:

```bash
comp/.venv/bin/python -I experiments/poc/npg8_phase2_reference.py --config experiments/configs/npg8-c3-v1.json
```

Final output:

```text
npg8_phase2_author_check=PASS
source_bindings=5
boundary_algebra_cases=1680
attribution_fixtures=3
concentrated_extra_event_coverage=0.25
policy_value_fixtures=2
boundary_count_dominance_fixtures=2
phase3_design_profiles=3
phase3_npg_to_fixed8_ratio=1.131023918935
phase3_min_oracle_ratio=1.000000000000
phase3_min_screen_saving=0.384615384615
generation_remainder=post_validation
review=not_dispatched
```

The checker independently:

- authenticates source and baseline attack bytes;
- exhaustively verifies the `h>a/8` sign equivalence for 1,680 integer cases;
- rejects aggregate-event substitution with the concentrated-event fixture;
- charges full policy-start versus post-validation generation time;
- charges returned-probe replay cost and fill cost;
- enforces selected-candidate count no greater than the fixed-1 comparator;
- evaluates the exact frozen Phase-3 profiles, arm selection and fixed controls.

## Author-check correction record

The first checker invocation failed
`baseline mismatch: boundary_heavy_activation`. The fixture's expected baseline
was `360`, which omitted the frozen 1.10 replay inflation. The reference
correctly computed 18 rather than 20 candidates, so the config expectation was
corrected to `324` before hypothesis freeze. A later self-audit replaced
`qL * probe_count` with the sum of each probe's own conservative raw and made
the Phase-3 arm selector use the exact post-screen returned-policy value.

These were author-stage specification corrections, not experiments or
post-result hypothesis edits.

## Absence checks

```text
test ! -e experiments/poc/npg8_phase3.py                 -> exit 0
test ! -e experiments/runs/npg8-c3-poc-v1              -> exit 0
rg NPG/npg8 in experiments/attack.py                    -> no match
npg8_attack_implementation_absent=true
```

No NPG attack implementation, Phase-3 run, Kaggle push, commit run or
competition submission exists.

## Gate Check

- Deterministic rung: PASS.
- Execution rung: limited to the author reference/checker; no empirical PoC.
- LLM judgment rung: pending one fresh sterile theory review.
- Hypothesis-review budget remains 2/12 until dispatch.

## Problem alignment

The checker forces the proposed adaptive component to outperform fixed packing
after every declared cost, preventing a mechanically attractive but
competition-negative selector from reaching Kaggle.

## Decision

Freeze the three bound artifacts at the next research commit. Then dispatch a
fresh sterile reviewer with all six round-2 requirements for disposition.
