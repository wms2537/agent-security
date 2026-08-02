# Measured Density Local Rate Profile

**Date:** 2026-08-02 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 10 · **Status:** completed

## Context

The v2 theory review required observed elapsed-time/rate numbers for the proposed `1.15x` score-rate stop. This profile is a deterministic local mechanics artifact only; it does not claim target-model timing or replay safety.

## Command

```text
PYTHONPATH=comp/sdk:experiments comp/.venv/bin/python <single-vs-dense CompliantAgent profile>
```

The script used `CompliantAgent`, `build_attack_env`, `_msg`, `_dense_msg(... endpoints=4)`, and `AttackAlgorithm._event_count` over `5` repetitions at three fixed mock latencies.

## Results

| mock latency_s | shape | mean_elapsed_s | mean_events | mean_score | mean_score_per_s |
|---:|---|---:|---:|---:|---:|
| `0.001` | single | `0.019533` | `1.000` | `0.090` | `4.676763` |
| `0.001` | dense4 | `0.022448` | `4.000` | `0.330` | `14.799326` |
| `0.010` | single | `0.039005` | `1.000` | `0.090` | `2.328094` |
| `0.010` | dense4 | `0.069448` | `4.000` | `0.330` | `4.767225` |
| `0.020` | single | `0.057247` | `1.000` | `0.090` | `1.573327` |
| `0.020` | dense4 | `0.120372` | `4.000` | `0.330` | `2.742566` |

The observed dense/single score-rate ratios are approximately:

- `3.16x` at latency `0.001`;
- `2.05x` at latency `0.010`;
- `1.74x` at latency `0.020`.

## Interpretation

This supports `MEASURED_DENSE_SCORE_RATE_GAIN = 1.15` as a local mechanics gate: in a deterministic compliant setting where four posts fire, dense4 comfortably clears the threshold. It does not prove that the target models will clear the threshold or that generation-side elapsed time identifies replay cost.

## Decision

Use these numbers only to justify the local score-rate-stop gate in the revised hypothesis.
