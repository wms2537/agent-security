# T085 — DBER pre-change profile run03 preregistration

**Date:** 2026-07-26 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 6/6 · **Status:** preregistered, unresolved

**Supersedes only the invalid generation timescales in:** reports 209 and 211

## Context

Run01 could not start, and run02 executed probes but had no verified-fill window.
Both exposed the same unchanged-controller behavior: `slowest` is initialized at
one second and never decreases, so `time_left()` reserves at least `1.3 s` for
the entire run.

## Third and final retry change

Change only the `generation_limited` time budget:

```text
run01 1.30 s -> no interaction
run02 2.00 s -> partial probes, no fill
run03 4.00 s -> preregistered final timescale
```

At four seconds, the invariant reserve plus `0.05 s` margin leaves `2.65 s` for
the frozen probe and fill sequence. The replay-safe cap remains `5.94 s`, so
generation should still bind first.

Every other input is unchanged:

```text
attack_sha256=efac97119321c2cafdd1f0df87e756d206a59073ffbd1ebd4f7bf95d52fea883
probe_reps=5
multi_probe_reps=2
multi_probe_messages=6
multi_fill_messages=24
enable_scoc=false
replay_safe=0.99
```

## Frozen run03 predictions

| Regime | Generation budget | Replay budget | Candidate cap | Predicted binding | Oracle-salvage prediction |
|---|---:|---:|---:|---|---:|
| `generation_limited` | **4.00 s** | 6.00 s | 200 | generation | at least 18 raw |
| `replay_fragmented` | 3.00 s | 0.18 s | 200 | replay | at least 18 raw |
| `candidate_limited` | 3.00 s | 6.00 s | 3 | candidate | exactly 0 raw |

The confirm/disconfirm rules and oracle definitions remain exactly those in
report 209. This is debug attempt 3/3. Another harness execution is forbidden
if run03 fails.

## Command

```text
PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/dber_profile.py --out-dir artifacts/dber/run03
```

## Decision

Predictions are frozen before execution. No attack edit, Kaggle mutation, or
submission is authorized.
