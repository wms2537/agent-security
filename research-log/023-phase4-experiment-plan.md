# ORF Phase-4 public non-target experiment plan

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed, runs not started

## Context

The Phase-3 PoC confirmed a 49.277489504413% public synthetic conditional-regret
gain on one 40-profile realization. Phase 4 must now test the full 320-profile
mechanics across at least three fixed masters, code-review the implementation
before believing core results, isolate factor contributions, and add one
generalization regime. The future beacon-held-out v9 target remains locked and
unauthorized, so every run below is explicitly public non-target validation.

## Baseline choice and trust

The closest comparison is v9's `PROBE_GLOBAL` policy: retain the identical seven
probes, then select one fill length for every profile in a master. There is no
published number for this bespoke finite table. The trusted reference is the
reviewed exact finite optimizer in `orf_support_calibration.py`, bound to the
actual SDK score identity by the preserved fixtures and the rigorous v9 review.

Baseline tuning parity is exact rather than budgetary: `PROBE_GLOBAL`
exhaustively evaluates all seven legal global lengths and takes their exact
argmax. It has no initialization, training, or unsearched hyperparameter. The
baseline run therefore is also the tuned-baseline run; running a nominal second
copy would add no information and violate the simplicity criterion.

Baseline reproduction has two tolerances. Mechanically, every aggregate score
and selected length must exactly equal an independent recomputation from the
committed 320x7 score table. Predictively, the three-master mean G is expected to
fall in `[7.5m,9.5m]`, centered at 8.5m from calibration v2. A predictive miss
does not excuse a mechanical mismatch.

## Frozen public seed sets

Before any run, three primary preimages and three disjoint generalization
preimages are fixed in `experiments/configs/orf-phase4-v1.json`. Each is hashed
once with SHA-256. No prefix, label, factor, profile, master, or threshold may be
replaced after observing an outcome.

## Sequential runs

| Task | Run | Single change / purpose | N | Estimate |
|---|---|---|---:|---:|
| T014 | `orf-p4-baseline` | Reproduce exact global-fill comparator; save 320x7 tables and a measured per-length/profile preference artifact. Also completes tuned-baseline parity. | 3 masters | <2 min CPU |
| T015 | implementation only | Add the core per-profile action-scope wrapper over the same tables; do not run it. | — | <1 min |
| T016 | sterile code review | Audit baseline+core code for leakage, label/split hygiene, exact metric, immutable inputs, and train/eval separation before core results count. | — | review gate |
| T017 | `orf-p4-core` | Replace one global argmax with per-profile argmaxes; same profiles, probes, score, resources, and seven actions. Include the homogeneous-zero distinguishing prediction. | 3 primary + 3 homogeneous masters | <2 min CPU |
| T018 | checkpoint | Apply the user's advance go only if baseline/core pass; otherwise stop at the failed branch. | — | decision |
| T019 | `orf-p4-ablations` | One-at-a-time removal of cliffs, curvature, reset cost, novelty, and saturation on the same three primary masters; attribute, do not retune. | 3x5 | <3 min CPU |
| T020 | `orf-p4-generalization` | Distinct three-master unsaturated balanced-cliff regime; tests a harder weighting/resource benchmark. | 3 masters | <2 min CPU |
| T021 | `orf-p4-scaling` | Fixed 40/160/320-profile nested scales on the three primary masters; robustness of the materiality direction. | 3x3 | <2 min CPU |
| T022 | summary | Verify every ledger/log/commit, generate comparison artifacts, and close or fail the Phase-4 gate. | — | <2 min |

Runs are sequential because all later code uses the reviewed core engine. No run
may be added without an append-only plan amendment explaining why.

## Predictions reserved for run-time preregistration

The plan freezes the baseline mean prediction (8.5m), core mean gain prediction
(40%), generalization gain prediction (35%), and scaling clear fraction (1.0).
Each task will append its unresolved `results.tsv` row and a run-specific
rationale before dispatch. Ablation values remain unrecorded here because each
has a different estimand; their numeric predictions must be written together,
before the single ablation-batch dispatch, using only already committed evidence.

## Anti-stacking and attribution

The core is one replacement: split-global action scope to per-profile action
scope. The distinguishing prediction is material gain on crossed heterogeneous
profiles but exact equality on homogeneous profiles. The ablation batch does not
add components to the method; it removes generator/score mechanisms one at a
time to determine which aspects explain the observed magnitude.

## Authorization and data discipline

All labels are public deterministic validation signals. The locked test is still
`orf-heldout-v7`; it will not be frozen, generated, or evaluated. No Kaggle,
network, beacon, external posting, or account mutation is authorized. If Phase 5
must conclude without the locked test, the final claim will be downgraded to
public synthetic validation rather than presenting validation as test evidence.

## Gate Check

- Plan JSON parses and fixes N=3 primary/generalization masters, five ablations,
  three scales, exact policies, thresholds, predictions, immutable paths, and
  forbidden actions before execution.
- Each planned run has one state task, estimated compute, and a single scientific
  purpose.
- Baseline trust/tolerance, tuning parity, code-review ordering, distinguishing
  prediction, attribution, Medium-intensity generalization, and robustness are
  all specified.

## Problem alignment

The plan tests whether the proposed online-structure moat has a robust
benchmark-shaped oracle advantage and identifies what produces it, without
substituting public synthetic validation for real model behavior.

## Decision

Execute T014 first. Stop on any mechanical baseline mismatch. Believe no core
result before T016 passes.

## Next Steps

Preregister and run `orf-p4-baseline` only.
