# T083 — DBER pre-change profile preregistration

**Date:** 2026-07-26 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 6/6 · **Status:** preregistered, unresolved

## Context

Report 208 selected Dual-Budget Evidence Reuse (DBER) profile-first. SciAgent's
engineering gate requires a measured bottleneck artifact before any component is
built. This task therefore profiles the unchanged controller; it does not edit
`experiments/attack.py`, generate a Kaggle notebook, push a kernel, or submit.

## Profile question

Does the incumbent discard successful probe candidates in a resource regime
where some can fit in the final replay/candidate headroom, or are replay and
candidate capacity already fully binding?

## Frozen input

```text
attack_path=experiments/attack.py
attack_sha256=efac97119321c2cafdd1f0df87e756d206a59073ffbd1ebd4f7bf95d52fea883
controller=8 templates x 5 repetitions + 1 cold start + 2 multi probes
multi_probe_messages=6
multi_fill_messages=24
enable_scoc=false
```

The tracked controller is behaviorally equivalent to the pulled `81.225`
notebook for this profile: SCOC is disabled and the two-repetition multi route
uses the same `1.10` gain threshold. Dormant SCOC/anchor helpers receive no role
or credit.

## Controlled regimes

All regimes use the real public SDK environment and scorer surfaces with a
deterministic `AmortizingAgent` (`0.015 s` fixed reset cost, `0.001 s` per
action). These regimes validate resource accounting and mechanism possibility,
not target-model prevalence.

| Regime | Generation budget | Replay budget | Candidate cap | Predicted binding | Pre-run oracle-salvage prediction |
|---|---:|---:|---:|---|---:|
| `generation_limited` | 1.30 s | 6.00 s | 200 | generation | at least 18 raw |
| `replay_fragmented` | 3.00 s | 0.18 s | 200 | replay | at least 18 raw |
| `candidate_limited` | 3.00 s | 6.00 s | 3 | candidate | exactly 0 raw |

The replay-fragmented prediction is not that replay has abundant headroom. It
predicts discrete residual capacity smaller than the next 24-message fill item
but large enough for at least one already-validated shorter probe.

## Metrics and calculations

- `successful_discarded_probes`: exact successful pre-fill episodes absent from
  the incumbent returned signatures.
- `binding_resource`: candidate if the cap is full; otherwise replay if the next
  selected-structure unit does not fit; otherwise generation.
- `oracle_salvage_raw`: raw of discarded successful probes packed by descending
  raw/replay-second into exact replay and candidate headroom.
- `bank_all_replay_overflow_s`: positive replay-cap violation from admitting all
  discarded probes without resource classification.
- `oracle_gain_percent`: `100 * oracle_salvage_raw / incumbent_returned_raw`.

The oracle is an upper bound and can only seed a hypothesis. It is not a DBER
implementation result and cannot support a Kaggle submission.

## Confirm, disconfirm, and inconclusive outcomes

The bottleneck premise is supported for further hypothesis work only if:

1. at least one regime has `successful_discarded_probes > 0`;
2. both generation-limited and replay-fragmented regimes have
   `oracle_salvage_raw >= 18`;
3. candidate-limited has `oracle_salvage_raw = 0`;
4. replay-fragmented has `bank_all_replay_overflow_s > 0`, distinguishing
   resource-aware DBER from bank-all; and
5. observed binding labels match all three preregistered labels.

Any missing salvage in the first two regimes, positive salvage at a full
candidate cap, or a binding-label mismatch disconfirms this profile design.
Timing within `±20%` that preserves all discrete labels is treated as the same
controlled regime. A timing-boundary flip is inconclusive and requires a new
preregistered regime, not an edited result.

## Prediction rationale

The source executes up to 43 pre-fill candidates but creates the returned list
only afterward. With separate generation and replay budgets, those exact
successful traces are sunk generation work but retain nonzero replay cost.
Generation-limited runs should leave broad replay headroom. A 24-message fill
unit should also leave a discrete replay fragment in the replay-limited control,
while the three-candidate cap should forbid all salvage.

## Command

```text
PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/dber_profile.py --out-dir artifacts/dber/run01
```

## Problem alignment

The profile tests whether the current `81.225` controller leaves source-compliant
score on the table through an orchestration/admission defect, while preserving
the replay deadline and incumbent fallback required by `PROBLEM.md`.

## Decision

Predictions are frozen before execution. Results remain unresolved.
