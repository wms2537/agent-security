# T084 — DBER pre-change profile run02 preregistration

**Date:** 2026-07-26 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 6/6 · **Status:** preregistered, unresolved

**Supersedes only the invalid run01 timescale in:** `research-log/209-dber-prechange-profile-preregistration.md`

## Context

Run01 never interacted with the controlled target because its `1.30 s`
generation budget could not clear the unchanged controller's initial
`slowest*1.3 = 1.30 s` safety reserve plus margin. Report 210 records that
failure and marks all run01 rows crash/NA.

## Single retry change

The `generation_limited` time budget is scaled from `1.30 s` to `2.00 s`.
This is the only contract change. It exceeds the initial safety sentinel while
remaining smaller than the replay budget and candidate capacity.

Frozen invariants:

```text
attack_sha256=efac97119321c2cafdd1f0df87e756d206a59073ffbd1ebd4f7bf95d52fea883
probe_reps=5
multi_probe_reps=2
multi_probe_messages=6
multi_fill_messages=24
enable_scoc=false
replay_safe=0.99
generation/replay/candidate binding predictions unchanged
oracle-salvage thresholds unchanged: >=18, >=18, ==0 raw
```

## Frozen run02 regimes

| Regime | Generation budget | Replay budget | Candidate cap | Predicted binding | Oracle-salvage prediction |
|---|---:|---:|---:|---|---:|
| `generation_limited` | **2.00 s** | 6.00 s | 200 | generation | at least 18 raw |
| `replay_fragmented` | 3.00 s | 0.18 s | 200 | replay | at least 18 raw |
| `candidate_limited` | 3.00 s | 6.00 s | 3 | candidate | exactly 0 raw |

All metric definitions, confirm/disconfirm rules, limitations, and problem
alignment remain those frozen in report 209. Run02 uses new ledger rows and a
new artifact directory; run01 remains immutable failure evidence.

## Prediction rationale

The two-second scale makes the controller callable but preserves the intended
ordering: generation capacity is far below the `5.94 s` replay-safe cap in the
first regime, the next 24-message unit should not fit the small replay budget in
the second, and the third has no candidate headroom.

## Command

```text
PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/dber_profile.py --out-dir artifacts/dber/run02
```

## Decision

Predictions are frozen before run02. No attack or Kaggle action is authorized by
this retry.
