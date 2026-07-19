# T005 — replay-safe strong-baseline parity

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 3 · **Status:** completed

## Prediction

Replacing v2's `replay_safe=0.90` plus `cost_inflation=1.10` with the public
baseline's directly measured `replay_safe=0.99` plus `cost_inflation=1.00` should
increase the number of returned firing candidates by:

```text
(0.99 / 1.00) / (0.90 / 1.10) = 1.210×
```

The attack should continue to pass the real SDK replay/scoring pipeline. A mechanics
regression or a materially different controlled capacity ratio would disconfirm the
accounting model.

## Intervention

- Changed only replay sizing defaults to direct measured cost at a 0.99 cap.
- Replaced the invented JSON and one-turn multi-post probes with the current public
  eight-template single-post bank (`plain`, `bare`, `bare_ok`, `call_syntax`, and
  four harmony variants). This removes the v1-refuted one-turn multi-post structure.
- Kept online fire-rate/raw-per-second selection and verified fill unchanged.

## Evidence

```bash
comp/.venv/bin/python -m py_compile \
  experiments/attack.py experiments/local_eval.py experiments/mock_agents.py

comp/.venv/bin/python experiments/local_eval.py 50 120
# compliant: findings=50 raw=900 norm=4.50
# harmony_only: findings=50 raw=900 norm=4.50
# stochastic: findings=50 raw=900 norm=4.50
```

Controlled latency comparison (`CompliantAgent(latency_s=0.002)`, identical 1 s
synthetic replay budget, one probe repetition, real SDK evaluator):

```text
old_budget:             findings=39, raw=702, normalized=3.51
public_baseline_budget: findings=47, raw=846, normalized=4.23
capacity_ratio = 47 / 39 = 1.205×
```

The observed 1.205× is within 0.5% of the predicted 1.210×. Small divergence comes
from discrete candidate count and timing jitter.

## Decision

T005 passes and becomes the single-post control. If latency-linearity transfers to
the real models, the expected score is about `69.57 × 1.205 = 83.84`, consistent
with the audited public 83.88–87.9 band. No real-score claim is made until a Kaggle
rerun. Proceed to T006 because this correction is insufficient to reach 105.635,
let alone 139.14.
