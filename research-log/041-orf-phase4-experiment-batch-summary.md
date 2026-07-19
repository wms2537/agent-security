# ORF Phase-4 experiment-batch summary

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** gate passed; advance to Phase 5 analysis

## Context

T022 audits the complete public non-target Phase-4 batch frozen in
research-log/023. No new scientific computation, held-out action, network call,
or Kaggle action is part of this closeout.

## Batch result

The exact primary comparison confirmed the candidate-structure policy:

- `PROBE_GLOBAL` exact mean G: 8,602,550.666666666667; all three global actions
  selected length 16 and all 6,720 independent scorer comparisons matched.
- `ADAPTIVE` versus the same table: mean gain 40.249038022308%, inside the
  preregistered `[30,50]` interval; per-master range
  `[38.111186959411%,41.437632336565%]`; all three clear 5%.
- Homogeneous distinguishing negative: 3/3 exact zero regret, global length one,
  and every adaptive row length one.

The attribution batch showed:

| One-at-a-time condition | Mean gain | Delta from primary core |
|---|---:|---:|
| No cliff | 7.622073949240% | -32.626964073068 pp |
| No curvature | 37.860007927303% | -2.389030095004 pp |
| No reset | 18.973588191963% | -21.275449830344 pp |
| No novelty bonus | 40.094682770562% | -0.154355251746 pp |
| Unsaturated | 44.355152104598% | +4.106114082290 pp |

Cliff behavior is the dominant contributor, reset overhead is substantial,
curvature is modest, the two-point novelty term is negligible, and saturation
suppresses some conditional value. OAT effects are not additive.

The disjoint public unsaturated/balanced-cliff regime gained
36.393868336949% (three-master range 35.175681399541–37.352060597349%), inside
its `[30,45]` interval and above 5% for all masters.

The nested-scale check cleared all nine cells. Means were 48.952971791444% at
N=40, 42.794164975019% at N=160, and 40.249038022308% at N=320; the nine-cell
range was 38.111186959411–52.609341554583%. These are nested robustness
descriptions, not independent-sample learning curves.

The machine-readable comparison is
`experiments/orf-phase4-summary/comparison.tsv`.

## Prediction audit

All 15 Phase-4 ledger metrics are resolved `confirm` / `keep`:

- baseline: 3/3;
- primary core and homogeneous controls: 4/4;
- attribution means: 5/5;
- generalization: 2/2;
- scaling: 1/1.

No unresolved Phase-4 row remains. Numeric primary, attribution, and
generalization forecasts were committed before their code/data execution. Scale
means were explicitly descriptive; only the 9/9 clear fraction was predicted.

## Provenance and review audit

- Baseline historical evidence retains exact hashes for its 961-row table,
  22-line aggregate table, summary/profile/notes/log, and immutable-diff proof.
- The initial sterile core review found a HIGH stale/partial-output issue. T023
  replaced reusable writes with exclusive staging, command-owned logging,
  source/input/output hashes, canonical COMPLETE last, fsync, atomic
  no-replace publication, failed siblings, and exact verification.
- Round 2 found a HIGH symlink/lexical-identity bypass. T024 added lexical
  direct-child checks, `lexists/lstat`, `O_NOFOLLOW`, inode/type/content checks,
  and adversarial live/dangling/race tests.
- Round 3 returned `SOUND`, no findings. Bundle tests are 15/15 (including 24
  failure boundaries and five symlink/race cases); core toys are 4/4.
- Ablation, generalization, and scaling runners each received separate focused
  `SOUND` reviews before execution, with no findings at any severity.
- Fresh verification at T022 accepts all four transactional bundles—core,
  ablations, generalization, scaling—as exact `COMPLETE` attempts with current
  binding hashes and exact file sets.
- No failed Phase-4 attempt sibling exists. The run parent contains only those
  four completed batches and the two earlier support-calibration records.
- The eight frozen Phase-4 inputs have an empty diff from plan commit `354cc02`.
- `state.json` and the frozen config parse with duplicate-key rejection; all
  Phase-4 tasks except this closing task were already terminal.

Independent artifact audits recomputed 960 primary rows, 4,800 ablation rows and
33,600 transformed scores, 960 generalization rows and 6,720 scores, and all nine
scaling cells. Total reported scientific runtime was 4.456198161 seconds; maximum
reported peak memory was 0.583507538 GB.

## Interpretation

The public evidence confirms a substantial, robust finite-table oracle advantage
from selecting structure per profile rather than globally. The homogeneous
negative rules out a universal preference for larger actions. Attribution and
the changed regime show the effect is not an artifact of the novelty constant or
one exact saturation cap.

The strongest valid claim stops there. These profiles are purpose-built and
deterministic. No experiment establishes that live target models expose the same
response heterogeneity, that an online learner can infer the per-profile action,
that replay deadlines are safe, or that the advantage transfers to private or
Kaggle evaluation. Because the authorized held-out beacon test remains unfrozen
and unopened, Phase 5 must label the result **public synthetic validation**, not
held-out confirmation.

## Gate Check

- Baseline reproduction/tuning parity: PASS.
- Sterile code review and all blocker repairs: PASS.
- Primary materiality and distinguishing negative: PASS.
- Attribution: PASS and independently auditable.
- Medium-intensity disjoint-regime generalization: PASS.
- Nested robustness/scaling: PASS.
- Prediction ledger, manifests, hashes, immutables, resources, commits, and scope
  boundaries: PASS.

The Phase-4 experiment-batch gate passes.

## Problem alignment

The batch establishes the benchmark-shaped value and mechanism of the proposed
online-structure moat without misrepresenting synthetic oracle value as live
agent performance.

## Decision

Advance to Phase 5 analysis under the user's prior authorization. Preserve the
no-Kaggle and no-held-out/freeze/beacon boundaries.

## Next Steps

Read the SciAgent Phase-5 playbook, synthesize source-backed analysis from the
committed results, and carry only defensible public-synthetic claims into the
Phase-6 paper.
