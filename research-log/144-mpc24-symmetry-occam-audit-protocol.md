# MPC-24 symmetry and Occam audit protocol

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** frozen before execution

## Why this audit owns the round-6 blocker

Round 6 showed that v6 never made the fixed controls share MPC's salvage,
charging and stopping semantics. Once those safety semantics are symmetric, a
simple high-ceiling policy may already reproduce every useful 24/8 choice: it
requests 24, salvages the longest eligible prefix, and permanently lowers its
ceiling. If so, the selector adds no competition value and should be retired.

This read-only audit tests that adverse Occam explanation on the already
retained 360-row source-authentic profile artifact. It does not execute a new
agent, generate a held-out profile, mutate `attack.py`, contact Kaggle, or
confirm a Phase-3/official claim.

## Frozen inputs and disclosure

The input bundle is the failed PORF profile run:

- `experiments/runs/porf-c3-profile-v2/COMPLETE.json`, SHA-256
  `ea7a6d6d53cf7cf3453269e53ce14566943402aa5673022277ea8968f019a1b5`;
- `samples.tsv`, SHA-256
  `61395ac87dca4ace41993325372fd8dc7db6d960efcd502c04934095ed73276d`;
- `summary.json`, SHA-256
  `64c05a59d9006446a7eb35fcabef59368b63b7bc4ad06db252590bd085debf77`;
- generating config SHA-256
  `6d15eb96013f94ae760faa9bfaa22dcdf15419df7bb1b68ec02ec6fc27add0c2`.

The bundle status is `FAIL`, with only `6/9` frozen SDK decisions passing.
This audit uses a post-hoc 24/8 pattern from that disconfirming run solely to
decide whether the new selector survives an adverse simple-policy explanation.

## Shared retrospective kernel

All compared policies use the same mechanics:

1. the controlled generation and replay ledgers are each 4 seconds and the
   candidate cap is 2,000;
2. every request charges the requested arm's generation cost;
3. the returned finding is the longest eligible member of `{24,8,1}` no
   greater than the requested ceiling, using the frozen `coverage>=0.75` rule;
4. every return charges the same calibrated replay surrogate
   `1.25*c_m+6.25*c_1`, one candidate slot and its measured raw;
5. the state becomes `min(old_state, returned_prefix)` and never rises;
6. replicate 0 supplies the first-path point estimate; held-out replicates 3–4
   supply conservative maximum cost and minimum raw for later paths;
7. a candidate is included only if its frozen point costs fit both ledgers.

The last rule is a retrospective point estimate, not an observable online
admission algorithm. Prefix-8 and prefix-1 costs are independent-arm proxies,
not nested measurements. These limitations forbid Phase-3 or target claims.

## Compared policies

- `fixed8`: always proposes ceiling 8;
- `fixed24_ceiling`: always proposes ceiling 24, with the shared permanent
  monotone salvage state;
- `fixed24_no_salvage`: adverse removal that drops a non-eligible 24 request;
- `mpc_calibrated`: v6's one-24-path selector and calibrated ledger;
- `scalar_mpc`: the full selector and capacity calculation under
  `1.10*c_m`, while actual replay costs are accumulated separately;
- every primitive 8/24 static sequence of period 1 through 6, including every
  cyclic phase; ties prefer higher aggregate raw, shorter period, then
  lexicographic order.

This makes the scalar arm a full retrospective controller simulation rather
than applying a different ledger to calibrated-controller traces. A fresh
Phase-3 batch would still be needed for an end-to-end experimental ablation.

## Predictions recorded before execution

| Metric | Prediction | Confidence | Reason |
|---|---:|---|---|
| MPC first state equals fixed24-ceiling first return | `9/9` | high | the six full-coverage cells prefer 24 and the three cliff cells salvage 8 |
| MPC/fixed24-ceiling aggregate ratio | `<=1.01` | high | the selector appears to reproduce the safety ceiling's state, not add a distinct decision |
| best primitive static pattern | `[24]` | medium | any 8 proposal loses raw in the six 24-favoring cells, while shared salvage repairs the three cliffs |
| scalar MPC actual-replay overage cells | `>=1/9` | medium | scalar 1.10 missed 84/90 retained 8/24 replay pairs |
| calibrated MPC actual-replay overage cells | `0/9` | high | the frozen surrogate covered all 54 held-out replay pairs |

## Frozen decision rule

- If first-state match is `9/9` and MPC/fixed24-ceiling is `<=1.01`, retire the
  selector and pivot to a simpler high-ceiling monotone-salvage hypothesis.
- If MPC/fixed24-ceiling is `>=1.05` and at least one first-state choice differs,
  retain the selector for a superseding hypothesis.
- Otherwise declare this direction inconclusive and do not implement it.

Static-pattern and scalar-overage predictions are diagnostics; they cannot
override the selector decision rule.

## Exact execution

After this protocol, script and prediction rows are committed:

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_symmetry_occam_audit.py
```

The script writes no files. Its stdout will be captured verbatim in the result
RECORD, followed by the runtime-populated `results.tsv` rows in a separate
commit.

## Gate

- Research budget is charged from `2/5` to `3/5` at this freeze.
- Hypothesis-review usage remains `6/12`.
- V6 stays immutable and rejected.
- Phase 3, `experiments/attack.py`, Kaggle mutation and submission stay closed.
