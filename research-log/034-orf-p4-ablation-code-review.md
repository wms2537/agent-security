# ORF Phase-4 ablation code review

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Verdict:** SOUND

## Context

This targeted sterile review examined implementation commit `aefbe20` after
predictions were committed at its direct parent `e0b9520`. Dispatch commit
`69fb7e2` changed metadata only. Primary execution was forbidden.

## Verbatim reviewer report

SOUND

Blind assessment

- Line counts: preregistration 95; implementation log 63; ablation runner 715;
  toy suite 150; reviewed core runner 742; bundle helper 605; frozen config 107;
  immutable support 333; baseline table 961 lines (960 data); core summary and
  COMPLETE manifest one canonical-JSON line each.
- Predictions preceded code: `e0b9520` is the direct parent of implementation
  commit `aefbe20`; all five unresolved prediction-ledger rows and mechanisms
  were committed first. `69fb7e2` changes only review-task metadata.
- Exactness/provenance: every frozen input hash matches; runner SHA is
  `568d285a…f933`, tests SHA `a4036d1…362d`; canonical command, arguments,
  working directory, isolated mode, and final attempt identity are exact. The
  final and failed ablation attempts are absent.
- Transaction boundary: binding hashes are checked first, but scientific
  config/table parsing and aggregation begin only after `AttemptBundle.__enter__`
  creates staging and writes the canonical first log line.
- Parser/scorer: exact 35-column schema, ordered identities, three masters × 320
  profiles, canonical integers/fractions, legal cliffs/events, seven scores per
  profile, and exact default-score reproduction enforce 960 rows and 6,720
  scorer comparisons. The scorer matches immutable generation/replay budgets,
  candidate cap, positive-finding retention, `16e+2`, ceiling-to-saturation, and
  final cap algebra.
- Coefficients: the `m={1,2,4}` recovery formulas exactly derive
  `d=(c4−3c2+2c1)/6`, `b=c2−c1−3d`, and `a=c1−b−d`, then reconstruct and verify
  all seven costs.
- OAT isolation: `no_cliff`, `no_curvature`, `no_reset`, `no_novelty`, and
  `unsaturated` each alter only the named event, coefficient, novelty, or
  saturation mechanism; all other costs/events/budgets/caps/policies remain
  unchanged.
- Evaluator fairness: the hash-bound reviewed evaluator and smaller-length tie
  rule are reused identically for adaptive and global policies. The default
  reference is recomputed and checked against exact committed core A/G/regret/
  gain and mean evidence.
- Evidence sufficiency: the design deterministically emits 4,800 full transformed
  profile rows and 15 master records, with exact fractions, action counts,
  A/G/regret, deltas, aggregates, predictions, and word-only log metrics—
  sufficient for independent recomputation.
- Bundle: exact output set, canonical command-owned log, runner/helper/config/
  support/baseline/core-runner/core-COMPLETE/core-summary bindings, COMPLETE-last
  publication, exact hashes, no-replace identity, and self-verification are
  enforced.
- Authorized checks: static compilation PASS for four files; ablation toys 5/5;
  bundle tests 15/15; core toys 4/4; workspace unchanged.
- Leakage/scope: no network, live target, held-out/beacon, external-post, Kaggle,
  or target-derived input exists.

Severity findings: HIGH none; MEDIUM none; LOW none.

T019 execution is permitted once, using only the exact preregistered command and
attempt identity. No Kaggle or held-out action is permitted.

## Gate Check

T025 passes `SOUND`; the final attempt was absent at review closure.

## Problem alignment

The review establishes that any observed attribution is tied to exactly one
named mechanism and remains independently recomputable.

## Decision

Close T025 and permit the one-use public non-target T019 batch.

## Next Steps

Execute the exact command once, verify the complete bundle, and recompute all
4,800 rows before resolving the predictions.
