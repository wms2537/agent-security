# Hypothesis Iteration 10 v4 — Capped Measured Dense Replacement

**Date:** 2026-08-02 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 10 · **Status:** preregistered

**Supersedes:** `research-log/250-hypothesis-iter-10-measured-density-overlay-v3.md`.

## Revision response

Round-3 review in report 251 resolved the rate artifact, single-post ceiling, dense-minimum interpretability, and comparator existence, but rejected the `24` dense-kept threshold and the taxonomy framing. This revision:

- renames the mechanism to **Capped Measured Dense Replacement**;
- treats v35 fallback as an inherited safety control, not the contribution;
- raises the dense-use threshold to `84` retained dense candidates;
- derives `84` from the success threshold under conservative 3-event dense scoring and 20% fallback displacement;
- narrows the anti-stacking claim to a required evidence package: local comparator distinction plus public score.

## Claim

If the old blind dense branch is replaced by a capped measured dense branch, and that branch retains at least `84` exact four-endpoint candidates with at least `3` observed exfiltration events each, then the first eligible live submission should complete visibly and exceed the pure single-post ceiling.

Primary prediction:

- **Success:** visible public score `>=90.090`.
- **Strong success:** visible public score `>=100.000`.
- **Partial/fallback:** visible public score in `[86.670, 90.090)`.
- **Failure:** blank score or public score `<86.670`.

Scope: one future Kaggle public-score decision plus local ablation evidence. No replay-cost model or cross-model causal claim is asserted.

## Variables and frozen constants

Independent variable:

- Replace the refuted blind dense branch with **Capped Measured Dense Replacement**. The v35 fallback remains as inherited regression control.

`varies` slug:

- `measured-density-validation-fill-admission`

Frozen constants:

```text
MEASURED_DENSE_REPLACEMENT_ENABLED = True
MEASURED_DENSE_ENDPOINTS = 4
MEASURED_DENSE_MIN_EVENTS = 3
MEASURED_DENSE_MIN_KEPT_TO_USE = 84
MEASURED_DENSE_PROBE_REPS = 2
MEASURED_DENSE_MAX_KEPT = 96
MEASURED_DENSE_MAX_ATTEMPTS = 160
MEASURED_DENSE_BUDGET_FRAC = 0.20
MEASURED_DENSE_SCORE_RATE_GAIN = 1.15
MEASURED_DENSE_PROBE_BASE = 760000
MEASURED_DENSE_FRAME_OFFSET = 50000
```

Use rule:

- If the measured branch retains fewer than `84` dense candidates, return zero dense candidates and run inherited v35 fallback.
- If it retains `84-96` dense candidates, return those measured dense candidates first, then inherited v35 fallback with remaining budget.

## Threshold math

Source facts:

- `MAX_REPLAY_FINDINGS = 2_000` at `comp/sdk/aicomp_sdk/evaluation/ops.py:47`.
- single-post public contribution is `(16+2)/200 = 0.090`.
- pure single-post ceiling is `2,000 * 0.090 = 90.000`.
- success is therefore set to `90.090`, one single-post unit above the pure ceiling.

Dense lower-bound contribution:

- `MEASURED_DENSE_MIN_EVENTS = 3`.
- one retained dense candidate has lower-bound public contribution `(16*3+2)/200 = 0.250`.
- the overlay can spend at most `20%` of generation budget before fallback.
- using v35 `86.670` as the fallback floor, a conservative linear displacement model gives fallback remainder `0.8 * 86.670 = 69.336`.
- minimum dense count needed to clear `90.090` under that conservative model:

```text
ceil((90.090 - 69.336) / 0.250) = ceil(20.754 / 0.250) = 84
```

At the cap:

```text
96 * 0.250 + 0.8 * 86.670 = 93.336
96 * 0.330 + 0.8 * 86.670 = 101.016
```

Thus `84` is the smallest useful retained-dense threshold under the declared 3-event lower bound and `20%` fallback-displacement assumption; `96` gives a small ceiling for strong success if four-event behavior transfers.

## Local rate artifact

Report 249 measured deterministic local `CompliantAgent` score-rate ratios for dense4 versus single:

- `3.16x` at mock latency `0.001`;
- `2.05x` at mock latency `0.010`;
- `1.74x` at mock latency `0.020`.

This supports `MEASURED_DENSE_SCORE_RATE_GAIN = 1.15` as a local mechanics gate only. It is not a replay-cost estimate.

## Component evidence and ablations

| Component | Numeric evidence | Role | Ablation/comparator |
|---|---:|---|---|
| Replace blind dense branch | v34 and v36 blind dense variants blanked; v35 validation-fill scored `86.670` | removes the refuted blind dense operation | replacement disabled -> inherited v35 fallback |
| Candidate-level measured retention | v33 dense candidate value `0.130640`; four-event source value `0.330`; 3-event lower bound `0.250` | dense candidates returned only after exact candidate fires `>=3` events | capped unmeasured dense comparator: same caps, no per-candidate retention, local only |
| Minimum dense-use threshold | threshold math above requires `84` retained 3-event dense candidates to clear `90.090` under 20% displacement | prevents interpreting zero/small dense use as density success | positive fixture must retain `>=84`; no-fire fixture must retain zero and fall back |
| Score-rate gate | report 249 local dense/single ratios `1.74x-3.16x` | avoids retaining locally slow dense candidates | score-rate-stop disabled in slow-dense fixture changes admission |

## Taxonomy and anti-stacking

Taxonomy:

- Opportunity pattern: Optimization Bottleneck.
- Method paradigm: Engineering replacement.
- Dominant operation: replace.

The proposed component is not "v35 plus dense" as a novelty claim. The v35 fallback is inherited regression control. The changed component is the replacement of the refuted blind dense branch by a capped measured dense branch.

Anti-stacking evidence package:

1. Local no-fire fixture: measured replacement returns zero dense candidates and falls back; capped unmeasured comparator returns dense candidates despite no firing.
2. Local positive fixture: measured replacement returns only candidates with `>=3` events and uses dense only if `>=84` are retained.
3. Public target: first eligible submission is visible and, for success, `>=90.090`.

The public score alone cannot attribute the mechanism; the hypothesis does not claim it can. The evidence package is what distinguishes the replacement from a plain capped dense stack.

## Threats to validity

- **Selection:** generation-retained dense candidates may fail replay; public score is aggregate only.
- **Confounding:** fallback contribution may dominate; minimum-use threshold and local comparator reduce but do not eliminate ambiguity.
- **Assignment:** Kaggle cells are external; no causal cross-model claim.
- **Protocol deviation:** static checks must forbid global blind dense.
- **Missing data:** target per-candidate logs unavailable; blank remains failure.
- **Measurement:** generation score-rate is a local gate, not replay cost.
- **Analysis flexibility:** constants are frozen in this file.
- **Selective reporting:** v34/v36 blanks remain negative evidence.

## Failure and success interpretation

Failure:

- blank score;
- public score `<86.670`;
- local positive fixture cannot retain `>=84` dense candidates;
- no-fire fixture returns any dense candidate;
- static check finds the old blind dense branch enabled.

Partial:

- `[86.670, 90.090)`.

Success:

- `>=90.090`.

Strong success:

- `>=100.000`.

## Occam-first decision

Single-post micro-tuning is simpler but cannot satisfy `>=90.090` because the source-derived pure single-post ceiling is `90.000`. Full measured-density fill is more complex. Capped Measured Dense Replacement is the smallest first target with threshold math showing a path above the pure ceiling.

## Metrics and ledger row

Primary metric:

- Kaggle public score, success `>=90.090`.

Secondary gates:

- local positive retained dense count `>=84`;
- no-fire fallback zero dense;
- capped-unmeasured local comparator differs from measured replacement;
- static blind-dense absence;
- notebook/server/schema/metadata checks.

Ledger row:

```text
lb-stageb-measured-density-fill public_score 90.090 beat-single-post-ceiling low NA NA NA NA preregistered Capped measured dense replacement; success visible >=90.090, strong success >=100, failure blank or <86.670
```

## Submission confidence gate

No Kaggle submission may occur until:

1. `py_compile experiments/attack.py submission/build_notebook.py` passes.
2. Static grep shows frozen constants and old global `DENSE_ENABLED = False`.
3. Local positive fixture retains `>=84` dense candidates with `>=3` events each.
4. Local no-fire fixture returns zero dense candidates and v35 one-URL fallback candidates.
5. Local capped-unmeasured comparator differs from measured replacement on no-fire.
6. Local score-rate-stop ablation changes admission on a slow-dense fixture.
7. Serialization smoke passes: no empty messages, max length `<2000`.
8. Rebuilt notebooks contain direct serve and placeholder `Id,Score`.
9. Metadata remains `true`, `NvidiaTeslaT4`, `notebook`.
10. Kaggle commit-run output, if pushed, is schema/source clean before competition submit.

## Problem alignment

Confirmation would provide target-owned evidence that replacing the refuted blind dense branch with a small measured dense branch can cross the single-post ceiling without repeating blank-score failure. It would not prove a general replay-cost theory.

## Decision

Proceed to re-review. If rigorous, implement only this frozen replacement and its local ablations.
