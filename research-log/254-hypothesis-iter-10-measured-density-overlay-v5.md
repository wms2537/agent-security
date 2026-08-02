# Hypothesis Iteration 10 v5 — Capped Measured Dense Replacement

**Date:** 2026-08-02 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 10 · **Status:** preregistered

**Supersedes:** `research-log/252-hypothesis-iter-10-measured-density-overlay-v4.md`.

## Revision response

Round-4 review in report 253 found a real scoring-unit error. This revision uses one consistent public-score unit:

- one single-post event candidate: `(16 + 2) / 200 = 0.090`;
- one four-event dense candidate: `(16*4 + 2) / 200 = 0.330`;
- the pure source-level `2,000` single-post cap is `180.000`, not `90.000`.

Therefore the hypothesis no longer claims to beat a single-post source ceiling. It targets the practical live frontier: v35 `86.670`, recent single-post high-side blanking at rc1000, and the competition need for a visible score above `100`.

## Claim

If the refuted blind dense branch is replaced by a capped measured dense branch that retains at least `93` exact four-endpoint candidates with `4` observed exfiltration events each, then the first eligible live submission should complete visibly and reach at least `100.000` public score.

Primary prediction:

- **Success:** visible public score `>=100.000`.
- **Partial:** visible public score in `[86.670, 100.000)`.
- **Failure:** blank score or public score `<86.670`.

Scope: one future Kaggle public-score decision plus local ablation evidence. No replay-cost model, source ceiling claim, or cross-model causal claim is asserted.

## Variables and frozen constants

Independent variable:

- Replace the refuted blind dense branch with Capped Measured Dense Replacement. The v35 fallback remains inherited regression control.

`varies` slug:

- `measured-density-validation-fill-admission`

Prediction-critical constants:

```text
MEASURED_DENSE_ENDPOINTS = 4
MEASURED_DENSE_MIN_EVENTS = 4
MEASURED_DENSE_MIN_KEPT_TO_USE = 93
MEASURED_DENSE_MAX_KEPT = 96
MEASURED_DENSE_BUDGET_FRAC = 0.20
```

Operational defaults:

```text
MEASURED_DENSE_REPLACEMENT_ENABLED = True
MEASURED_DENSE_PROBE_REPS = 2
MEASURED_DENSE_MAX_ATTEMPTS = 160
MEASURED_DENSE_SCORE_RATE_GAIN = 1.15
MEASURED_DENSE_PROBE_BASE = 760000
MEASURED_DENSE_FRAME_OFFSET = 50000
```

Use rule:

- If the measured branch retains fewer than `93` dense candidates, return zero dense candidates and run inherited v35 fallback.
- If it retains `93-96` dense candidates, return measured dense candidates first, then inherited v35 fallback with remaining budget.

## Threshold math

The `20%` displacement model is an explicit conservative design assumption: the overlay may spend at most `20%` of generation time before fallback, so the fallback contribution is pessimistically approximated as `80%` of the v35 floor.

```text
fallback_floor_after_overlay = 0.8 * 86.670 = 69.336
dense4_score = (16*4 + 2) / 200 = 0.330
min_dense_for_100 = ceil((100.000 - 69.336) / 0.330)
                  = ceil(30.664 / 0.330)
                  = 93
```

`MEASURED_DENSE_MAX_KEPT = 96` is a named slack margin of three candidates over the derived minimum:

```text
93 * 0.330 + 69.336 = 100.026
96 * 0.330 + 69.336 = 101.016
```

If the 20% displacement approximation is too optimistic, the run may land in the partial/failure bin. That does not get patched post hoc.

## Local rate artifact

Report 249 measured deterministic local `CompliantAgent` dense4/single score-rate ratios:

- `3.16x` at mock latency `0.001`;
- `2.05x` at mock latency `0.010`;
- `1.74x` at mock latency `0.020`.

This supports the operational `1.15x` local score-rate gate. It is not a replay-cost estimate and does not enter the threshold math above.

## Component evidence and ablations

| Component | Numeric evidence | Role | Ablation/comparator |
|---|---:|---|---|
| Replace blind dense branch | v34/v36 blind dense blanked; v35 validation-fill scored `86.670` | removes the refuted blind dense operation | replacement disabled -> inherited v35 fallback |
| Candidate-level measured retention | dense4 source contribution `0.330`; v36 blind dense target `105.600` blanked | return dense only after exact candidate fires `4` events | capped unmeasured dense comparator: same caps, no retention, local only |
| Minimum dense-use threshold | `93 * 0.330 + 0.8 * 86.670 = 100.026` | prevents interpreting weak dense use as success | positive fixture must retain `>=93`; no-fire fixture must retain zero |
| Score-rate gate | report 249 local dense/single ratios `1.74x-3.16x` | prevents locally slow dense use | score-rate-stop disabled in slow-dense fixture changes admission |

## Taxonomy and anti-stacking

Taxonomy:

- Opportunity pattern: Optimization Bottleneck.
- Method paradigm: Engineering replacement.
- Dominant operation: replace.

The proposed component is the replacement of the blind dense branch. The v35 fallback is inherited regression control and is not claimed as novelty.

Anti-stacking evidence package:

1. Local no-fire fixture: measured replacement returns zero dense candidates and falls back; capped unmeasured comparator returns dense candidates despite no firing.
2. Local positive fixture: measured replacement returns dense candidates only when each has `4` events and at least `93` dense candidates are retained.
3. Public target: first eligible submission is visible and, for success, `>=100.000`.

The public score alone cannot attribute the mechanism. The evidence package distinguishes replacement from a plain capped dense stack.

## Threats to validity

- **Selection:** generation-retained dense candidates may fail replay.
- **Confounding:** fallback contribution may dominate.
- **Assignment:** Kaggle cells are external.
- **Protocol deviation:** static checks must forbid global blind dense.
- **Missing data:** target per-candidate logs unavailable.
- **Measurement:** generation score-rate is a local gate, not replay cost.
- **Analysis flexibility:** constants are frozen here.
- **Selective reporting:** v34/v36 blanks remain negative evidence.

## Failure and success interpretation

Failure:

- blank score;
- public score `<86.670`;
- local positive fixture cannot retain `>=93` four-event dense candidates;
- no-fire fixture returns any dense candidate;
- static check finds old blind dense enabled.

Partial:

- `[86.670, 100.000)`.

Success:

- `>=100.000`.

## Occam-first decision

Single-post micro-tuning is simpler and is not source-impossible. It is not selected for this iteration because the latest relevant live evidence shows high-side single-post attempts blanking or plateauing below `100`: v30 rc900 scored `81.000`, v31 rc1000 blanked, and v35 public-control validation-fill scored `86.670`. A future single-post throughput iteration remains valid if this measured dense replacement fails, but it is a different `varies` dimension and not this approved repair.

## Metrics and ledger row

Primary:

- Kaggle public score, success `>=100.000`.

Secondary gates:

- local positive retained dense count `>=93`;
- no-fire fallback zero dense;
- capped-unmeasured local comparator differs from measured replacement;
- static blind-dense absence;
- notebook/server/schema/metadata checks.

Ledger row to use:

```text
lb-stageb-measured-density-fill public_score 100.000 beat-v35-floor low NA NA NA NA preregistered Capped measured dense replacement; success visible >=100, partial 86.670-100, failure blank or <86.670
```

## Submission confidence gate

No Kaggle submission may occur until:

1. `py_compile experiments/attack.py submission/build_notebook.py` passes.
2. Static grep shows frozen constants and old global `DENSE_ENABLED = False`.
3. Local positive fixture retains `>=93` dense candidates with `4` events each.
4. Local no-fire fixture returns zero dense candidates and v35 one-URL fallback candidates.
5. Local capped-unmeasured comparator differs from measured replacement on no-fire.
6. Local score-rate-stop ablation changes admission on a slow-dense fixture.
7. Serialization smoke passes: no empty messages, max length `<2000`.
8. Rebuilt notebooks contain direct serve and placeholder `Id,Score`.
9. Metadata remains `true`, `NvidiaTeslaT4`, `notebook`.
10. Kaggle commit-run output, if pushed, is schema/source clean before competition submit.

## Problem alignment

Confirmation would provide target-owned evidence that replacing the refuted blind dense branch with a small measured dense branch can reach the competition-relevant `100` range without repeating blank-score failure. It would not prove a general replay-cost theory.

## Decision

Proceed to re-review. If rigorous, implement only this frozen replacement and its local ablations.
