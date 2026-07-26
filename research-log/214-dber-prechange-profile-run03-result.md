# T085 — DBER pre-change profile run03 result

**Date:** 2026-07-26 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 6/6 · **Status:** completed, partial support

## Context

Run03 was the third and final profile attempt. Its predictions and unchanged
attack SHA were frozen at commit `1297b0e`.

## Provenance

The first line of `artifacts/dber/run03/run.log` is the exact command:

```text
PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/dber_profile.py --out-dir artifacts/dber/run03
```

Artifact hashes:

```text
run.log            bc7cdc192232f74b2e0a6441a2bb255d008ca85fae24d0ca55c65aea0eb3825a
dber-profile.json  d1bfb7896cd9bdcd89d116746b839b18017c859e221d54422a6fa72de358d60e
dber-profile.tsv   9859132d278cbf9bfb22d3c86f3f5ad0511ad43ccd50f3baaa684e15c2082d36
```

The profile JSON binds unchanged `experiments/attack.py` SHA
`efac97119321c2cafdd1f0df87e756d206a59073ffbd1ebd4f7bf95d52fea883`
and labels the scope controlled real-SDK mock resource regimes only.

## Results

| Regime | Binding | Discarded successful probes | Returned raw | Replay headroom | Oracle salvage raw | Oracle gain | Bank-all overflow |
|---|---|---:|---:|---:|---:|---:|---:|
| generation-limited | generation | 26 | 846 | 4.223351 s | **468** | **55.3191%** | 0 |
| replay-fragmented | replay | 28 | 72 | 0.019611 s | **0** | 0% | 0.948191 s |
| candidate-limited | candidate | 27 | 54 | 5.838983 s | **0** | 0% | 0 |

All three binding labels matched preregistration. The profile used a controlled
agent and selected single-post in all three regimes; it does not establish which
resource binds, or what structure is selected, in the live competition.

## Prediction vs. reality

- **Generation-limited:** predicted at least `18` raw; observed `468`.
  Confirmed strongly. All 26 discarded successful probes fit the replay and
  candidate headroom without another target interaction.
- **Replay-fragmented:** predicted at least `18` raw; observed `0`.
  Disconfirmed. The `0.019611 s` residual was smaller than every discarded
  successful probe. Bank-all would overflow replay by `0.948191 s`.
- **Candidate-limited:** predicted exactly `0`; observed `0`. Confirmed.

The broad pre-profile premise required positive salvage in both the first two
regimes and is therefore **not confirmed**. The narrower generation-binding
premise is supported as exploratory mechanism evidence.

## What the result changes

DBER must not be implemented as generic residual packing or unconditional probe
banking. Its only supported form is:

> When the incumbent stops because generation is binding, and exact replay and
> candidate headroom remain, return already successful probe candidates that
> fit; otherwise return the incumbent list unchanged.

This rule predicts no change in replay- and candidate-limited controls. The
replay-fragment result supplies the distinguishing negative: bank-all is unsafe
even though 28 valid probes exist.

## Limits

1. The result is exploratory and controlled; it cannot confirm target-model
   prevalence or leaderboard gain.
2. All regimes selected single-post, while the live `81.225` controller may
   select multi-message depending on target evidence.
3. Wall-clock rows are not independent seeds. No inferential statistic is made.
4. The `55.3191%` oracle gain is a regime-specific ceiling, not a Kaggle
   forecast.

## Decision

Close T085 as a successful profile with partial support. Open T086 to freeze a
narrow generation-binding hypothesis, explicitly retract the replay-fragment
subclaim, append the fresh `search_log` dimension, and complete the Phase-2
engineering/anti-stacking specification before theory review.

No attack edit, Kaggle mutation, or submission occurred.

## Problem alignment

The profile identifies a measurable orchestration bottleneck that can increase
valid returned score only when resource headroom exists, while furnishing a
negative control that prevents unsafe replay overfill.

## Machine-readable close

```text
t085_dber_profile=PASS attack_sha=efac9711 generation_binding=match generation_discarded=26 generation_salvage_raw=468 generation_gain_percent=55.319148936170 replay_binding=match replay_salvage_raw=0 replay_prediction=disconfirm bank_all_overflow_s=0.948190746795 candidate_binding=match candidate_salvage_raw=0 status=PARTIAL_SUPPORT_GENERATION_ONLY kaggle_mutation=false submission=false next_task=T086
```
