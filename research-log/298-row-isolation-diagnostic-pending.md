# Row-isolation diagnostic — Sub A & Sub B submitted (pending)

Date: 2026-08-17

Goal: decode each model's real per-row finding count to explain the 970 (ours)
vs ~1267 (frontier) gap, and validate the assumed public-score aggregation.

## Method

`ISOLATE_ROW` runs the full v42 fill on ONE row and returns exactly 5 fixed
firing candidates on the other (harmony frame for slow gpt_oss, plain for fast
gemma). run() is invoked once per model; the returned set is replayed vs public +
private guardrails for that model.

- Sub A (v46, ISOLATE_ROW="slow"): gpt_oss active (full fill), gemma = 5 fixed.
- Sub B (v47, ISOLATE_ROW="fast"): gemma active (full fill), gpt_oss = 5 fixed.

## Decode (under assumed publicScore = mean(gpt_oss_public, gemma_public),
##          row_norm = 0.09 * findings; 5 fixed -> 0.45 norm)

- Sub A score `A`  => gpt_oss row norm G = 2*A - 0.45 ; gpt findings = G/0.09
- Sub B score `B`  => gemma  row norm M = 2*B - 0.45 ; gem findings = M/0.09
- Consistency: G + M should ~= 2*87.255 = 174.51 (else aggregation model is wrong)

## What each outcome means

- G + M ~= 174.5 AND one row << other: that row is the bottleneck (under-filled) ->
  spend effort lifting it; confirms aggregation.
- G + M far from 174.5: the assumed aggregation/normalization is WRONG -> the
  whole "970 vs 1267 findings" framing is wrong; re-derive from the two isolated
  scores directly.
- A row near the 180 cap (2000 findings): that row is at the ceiling; only the
  other row has headroom.

## Status

Sub A ref 55579901 PENDING; Sub B v47 submitted PENDING. Active kernel reverted to
v42 (ISOLATE_ROW=None), standing 87.255. Decode + insight update when both score.
