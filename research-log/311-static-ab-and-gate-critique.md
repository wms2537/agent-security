# v59 gate critique accepted; static row-isolated A/B built

Date: 2026-08-24 (evening)

## Independent verification of the critique

Reproduced the reviewer's Monte Carlo with my own implementation
(50k trials/condition, lognormal timing noise, null = t2/t1 = 1.889):

| cv | false-activate (3+3 batch) | reviewer | power@1.10x | reviewer |
|---|---|---|---|---|
| 3%  | 0.3%  | 0.3%  | 73.9% | — |
| 5%  | 5.3%  | 5.2%  | 65.3% | — |
| 10% | 20.8% | 20.6% | 57.8% | ~58% |
| 20% | 34.2% | 33.9% | 54.0% | — |

Paired interleaved alternative (5 alternating pairs, median >= 1.08 + >= 4/5
pair wins): false 1.5% @ cv=5%, 9.0% @ cv=10%. Confirms: the shipped v59
gate is statistically fragile and non-interleaved batches confound server-
state drift with structure.

Also conceded: log 310's preregistration had an identifiability conflict
("both-reject => 86-87" overlaps "84-87 => abandon"). A mid-band v59 score
cannot distinguish gate-rejection from false-activation outcomes.

## Updated interpretation bands for pending v59 (ref 55748321)

| Score | Reading |
|---|---|
| >= 92 | Packing materially works even through the noisy gate; still confirm statically before M3/M4 |
| <= 83 | Serious failure or defect; audit before anything else |
| 84-90 | AMBIGUOUS by construction -> decide via static A/B only |

## Static row-isolated A/B harness built (`experiments/static-ab/`)

Deliberately non-adaptive: warm-up + n=8 mean classification (v42 rule) ->
active row returns a DETERMINISTIC BLIND portfolio of 2000 candidates in
index order (arm=m1: one message each, 18 raw when fired; arm=m2: same
message packed twice, 34 raw when both turns post). Inactive row returns the
proven v46/v47 fixed-five. No validation, no gate, no sizing — replay
throughput is exposed directly through partial-score-on-timeout.

Local gates passed: arm shapes, unique domains, packed pairs identical,
determinism across instances, row isolation, and real-SDK scorer end-to-end
(34.0 raw/finding for the m2 portfolio).

Four arms, one submission each (defaults baked into source per build):
A gpt/m1, B gpt/m2, C gemma/m1, D gemma/m2. Row decode: active_row =
2*score - 0.45.

## Acceptance criteria (preregistered)

Per model row: M2 >= 1.05 x M1, then repeat once before deploying. Within
+/-3% => close packing. M2 loses > 3% => close packing. High repeat variance
=> evaluator noise dominates; do not deploy.

## Slot plan (~7 slots to Sep 1 UTC deadline)

1. v59 result lands (no new slot) -> route per bands above.
2. Arms A/B on consecutive slots (gpt row), then C/D (gemma row).
3. Keep v42 as deployed final option throughout (kernel currently at canonical
   v42 config, sha 569c42d3...).

## Ledger taxonomy correction

From now on results.tsv distinguishes INTRA_MESSAGE_MULTIPOST (v36/v38/v44/
v49-gemma/v50 — all closed), INTER_MESSAGE_PACKING (v59 canary + static A/B —
open until the four-arm test resolves), MULTI_PREDICATE (closed: dimong-exact,
v55), FILL_WIDTH (closed), PROMPT_FRAME (closed), BLIND_COUNT (v48, closed as
a lever; reopened here as a measurement instrument).
