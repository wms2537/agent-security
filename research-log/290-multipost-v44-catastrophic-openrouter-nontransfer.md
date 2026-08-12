# v44 multi-post CATASTROPHIC (25.040) — OpenRouter firing did not transfer

Date: 2026-08-12

## Result

v44 (K=8 multi-post both rows, ref 55367233) = **25.040**, vs v42 best 87.255.
Reverted attack.py to the v42 frac-0.98 single-post config.

## Diagnosis

`25.040/87.255 x 1939 = ~556` effective single-post-equivalent findings (single-
post = 1939). Two compounding failures:

1. **Count collapse ~8x.** Replay-safe sizing charges generation elapsed per kept
   candidate; multi-post candidates run ~8 hops -> ~8x elapsed -> ~1/8 the
   returned count (~242).
2. **Real-SDK firing collapse.** OpenRouter showed 8/8 posts per candidate, but
   the real CPU llama.cpp stack fired only ~2.3/8 on average
   (556 ~= 242 x 2.3). The clean OpenRouter tool-API does NOT reproduce
   real-SDK multi-hop tool-calling reliability.

Net: paid 8x cost for ~2.3x value -> catastrophic.

## Lesson (decisive)

The OpenRouter harness faithfully measures: guardrail decisions, predicate/scoring
logic, single-hop compliance, and the EXISTENCE of the multi-post mechanism
(R=16K+2 when posts fire). It does NOT transfer: real-SDK raw-parse firing
reliability across MULTIPLE hops, nor CPU timing. The audit's multi-post lever is
mechanically real but net-negative on this stack as executed, and we have no
faithful offline way to predict real-SDK multi-hop firing -- so further K-tuning
is blind gambling.

## What is NOT invalidated

- Row-isolation diagnostics (decompose aggregate score per model) -- orthogonal,
  still the one disciplined observability move if pushing continues.
- Single-post frac-0.98 remains the best: v42 = 87.255 (standing).

## Scoreboard (post-v35)

v35 86.670 | v36 blank | v37 84.735 | v38 blank | v39 56.475 | v41 62.280 |
v42 87.255 (best) | v43 85.320 | v44 25.040.

Only frac 0.97->0.98 ever beat the floor. Every candidate-shape change (density,
frame, multi-post) regressed.

## State

attack.py = v42 best (frac 0.98 single-post). No further change. Standing 87.255.
