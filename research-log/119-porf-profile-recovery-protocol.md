# PORF profile recovery protocol — frozen before execution

**Date:** 2026-07-22  
**Phase/task:** Phase 2 / T046 adverse-review resolution  
**Status:** frozen, unrun  
**Config:** `experiments/configs/porf-c3-profile-v2.json`  
**Runner:** `experiments/porf_c3_profile_v2.py`  
**Planned attempt:** `experiments/runs/porf-c3-profile-v2`

## Purpose and evidentiary scope

The unchanged T006 reproduction failed because a one-sample, eight-template
wall-clock race crossed its 1.10 route threshold. This replacement is an
**exploratory engineering profile**, not a confirmation of target-model benefit.
It may seed hypothesis v2 but cannot confirm it.

The protocol separates:

1. exact allocator logic on five deterministic cost/raw profiles; and
2. real-SDK serialization, reset, predicate, score-geometry, and paired
   generation/replay mechanics on controlled mock agents.

It does not claim gpt-oss/Gemma latency, compliance, private-guardrail transfer,
or official-score improvement.

## Frozen policy under test

For each multiplicity `m in {1,4,8,24}`:

- `q_m` is the minimum observed raw candidate value across paired generation and
  replay samples;
- `c^g_m` is the maximum observed generation cost;
- `c^r_m` is the maximum observed replay cost, including fresh replay-environment
  construction;
- an arm is admissible only if every paired sample fires on at least 75% of its
  requested messages; and
- its attainable candidate count is
  `n_m=min(2000,floor(G/c^g_m),floor(R/c^r_m))`.

The selector maximizes `q_m*n_m`; exact ties choose the smaller `m`. This solves
generation time, replay time, and candidate count jointly. It does not optimize
raw/second and then assume the candidate cap is irrelevant.

## Frozen profiles and predictions

Deterministic profiles:

1. linear time-bound -> `m=1`;
2. reset-heavy -> `m=24`;
3. context cliff -> `m=8` and `m=24` inadmissible;
4. candidate-cap binding -> `m=24`; and
5. a counterexample where raw/second selects `m=4` but the joint constrained
   objective selects `m=8`.

SDK profiles use one fixed plain template, five paired samples per arm and phase,
and masters 41, 42, and 43:

- per-turn linear -> select `m=1` on all three masters;
- reset-heavy -> select `m=24` on all three masters; and
- context cliff -> reject `m=24` as inadmissible on all three masters. The exact
  smaller selected arm is recorded but not thresholded.

Primary recovery threshold: all 5 deterministic profiles and all 9 SDK decisions
must pass (`stability_fraction=1.0`). Any other result fails the profile recovery
and hypothesis v2 may not cite it as a stable engineering profile.

## Execution and reporting contract

Exact command:

```bash
comp/.venv/bin/python -I experiments/porf_c3_profile_v2.py \
  --config experiments/configs/porf-c3-profile-v2.json \
  --attempt-dir experiments/runs/porf-c3-profile-v2
```

The attempt path is one-use. The runner records every one of the planned 360 raw
sample rows (`3 profiles * 3 masters * 4 arms * 5 replicates * 2 phases`), all
decisions, paired replay/generation ratios, exact input hashes, runtime, memory and
a self-hashed completion envelope. Failed runs remain evidence and are not erased.

No Kaggle mutation or submission is part of this protocol.
