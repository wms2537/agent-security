# Phase-3 PoC design — HCMS-24

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Run ID:** `poc` · **Status:** frozen before implementation

## Core assumption tested

The smallest credible controlled test of HCMS-24 must exercise both surviving
components end to end:

1. ceiling 24 with exact nested-prefix salvage and permanent downgrade beats
   both calibrated fixed 8 and calibrated exact-24/no-salvage by at least 10%
   aggregate constrained raw; and
2. calibrated replay accounting covers its own candidates with no two-second
   method-cell overage, while a byte-equivalent HCMS method using scalar 1.10
   accounting overruns actual replay in at least one method-cell.

The immutable hypothesis is `research-log/146-hypothesis-iter-7-hcms24.md` at
commit `a8da04e`; the scrutinized `RIGOROUS` review is report 149.

## Minimal probe

Implement exactly the reviewed config `experiments/configs/hcms24-c3-v1.json`:

- three fresh mock profiles × three fresh masters;
- four Williams orders;
- four methods per order;
- 144 primary method repetitions total;
- one delayed-cliff safety fixture stored and aggregated separately;
- two-second controlled generation and replay ledgers;
- fresh generation and replay environments for each endogenous method result.

This is the minimum design that simultaneously preserves the reviewed fresh
mechanism grid, all 12 directed predecessor pairs, both contribution removals,
and an actual replay feasibility test. Expected wall time is several minutes on
CPU. If implementation arithmetic projects beyond 12 minutes, stop before the
scientific run and return `DONE_WITH_CONCERNS`; do not shrink the reviewed grid.

## Prediction frozen before dispatch

The five `hcms24-c3-poc-v1` rows already in `results.tsv` record:

| Metric | Prediction | Direction | Confidence |
|---|---:|---|---|
| HCMS / best simple aggregate | `>=1.10` | beat baseline | medium |
| HCMS actual replay coverage | `1.0` | match | high in controlled domain |
| HCMS actual replay-overage method-cells | `0/36` | match | high in controlled domain |
| scalar HCMS actual replay-overage method-cells | `>=1/36` | adverse removal | medium |
| invalid/timeout/duplicate/generation-overage count | `0` | match | high |

Rationale: the disclosed failed antecedent has matched HCMS ratios `1.4430`
versus fixed 8 and `1.7381` versus no-salvage, calibrated replay coverage
`54/54`, and retrospective scalar overage `7/9` versus calibrated `0/9`. The
fresh 10% floor retains less than one quarter of the smaller antecedent effect
and is a normative complexity penalty, not a confidence bound.

## Confirm, reject and invalid outcomes

- **Confirm:** all five predictions pass, all 144 primary method repetitions
  exist, every method/position count is one per cell, all 12 predecessor pairs
  occur once per profile/master block, all fixtures pass, and COMPLETE binds
  exact artifacts and sources.
- **Safe but insufficient:** valid ratio in `[1.00,1.10)`; reject HCMS complexity
  and prefer the best simple policy.
- **Refute:** valid ratio `<1.00`.
- **Invalidate:** any calibrated replay miss/overage, generation overage,
  timeout, duplicate identity, invalid attribution, missing repetition,
  method-interface drift, safety contamination, or scalar overage count zero.

No retry or threshold/profile change may rescue a scientific outcome.

## Implementation-before-run safeguard

The Phase-3 implementer may create only:

- `experiments/poc/hcms24_phase3_v1.py`;
- focused toy tests under `experiments/poc/` if needed.

It may run static compilation and toy-only tests, but must not create
`experiments/runs/hcms24-c3-poc-v1` or execute the primary/safety batch. A fresh
sterile code review will check, before the first exact invocation:

1. one shared kernel with policy configuration as data;
2. timer boundaries and inclusion of fresh replay construction/reset cost;
3. runtime equality of all non-ledger HCMS/scalar policy fields;
4. exact Williams position/predecessor counts;
5. endogenous scalar candidates and actual replay;
6. mechanical safety-row exclusion from every primary aggregate;
7. per-profile, per-method-cell and aggregate reporting;
8. fresh transaction, command-first log, COMPLETE-last hashes and refusal to
   overwrite an attempt;
9. frozen config/source/hypothesis hashes and no attack/Kaggle action.

Only a `SOUND` code review permits the one scientific command.

## Environment and evaluation-contract routing

Use `comp/.venv/bin/python -I` from repository root, CPU only, with no network.
The existing `experiments/configs/evaluation-contract.md` is ORF-specific; its
immutable-path and no-heldout/no-network/no-Kaggle boundaries still apply, but
its ORF metric is not the HCMS endpoint. The reviewed HCMS config/hypothesis are
the experiment-specific normative metric contract and are additionally
immutable.

Crash budget is three trivial implementation/debug attempts total. A change to
methods, clocks, profiles, masters, orders, scorer, ledger formulas, success
thresholds or aggregation is scientific and requires a superseding hypothesis,
not a debug retry.

## Transferability argument

The PoC can establish that the allocation/state/accounting mechanism works on a
fresh source-authentic mock grid and that calibrated accounting controls
endogenous replay capacity. It cannot establish that target models occupy the
same ceiling/cliff regimes, that their timing tails match, or that controlled
raw maps to leaderboard score. Those phenomena are plausibly model- and
scale-dependent. Therefore a confirmed PoC predicts only that HCMS is ready for
a separately frozen target-confidence bridge; it does not itself justify Kaggle
mutation or submission. A technically valid but target-irrelevant result is a
legal later outcome, not evidence to overclaim.

## Gate

- Phase 2: passed with scrutinized `RIGOROUS` review.
- Phase 3 predictions: frozen before implementer dispatch.
- Scientific execution: blocked pending implementation and sterile code review.
- Phase 4, attack mutation, Kaggle push and submission: closed.
