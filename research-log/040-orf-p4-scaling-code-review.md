# ORF Phase-4 scaling code review

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Verdict:** SOUND

## Context

Focused sterile review examined target `73b1d3d`; `a64d32b` changed metadata
only. The primary table was not parsed or aggregated.

## Verbatim reviewer report

SOUND

Blind assessment

- Line counts: preregistration 67; implementation log 48; scaling runner 325;
  toy suite 61; reviewed core 742; bundle helper 605; frozen config 107;
  baseline table 961 lines; core summary and COMPLETE one canonical-JSON line
  each.
- Predictions-before-code: `a796796` is the direct parent of implementation
  commit `73b1d3d`; the exact scales, subset rule, nine-cell all-clear prediction,
  threshold, command, evidence, and stop rules were committed first. `a64d32b`
  changes only review metadata.
- Exact bindings: runner SHA `6f5fa9a…9bc5`, toys SHA `19f806da…609`, and all
  config/baseline/core/helper/core-evidence hashes match.
- Command/attempt: repository root, isolated mode, exact `sys.argv`, canonical
  command, and lexical final attempt identity are enforced. Final and failed
  scaling attempts are absent.
- Transaction ordering: only source/input hash checks and side-effect-free module
  loading precede bundle entry; baseline parsing and every scientific computation
  occur after staging creation and canonical log publication.
- Parser/evaluator: the hash-bound reviewed strict parser enforces the exact
  960-row schema, row order, master/profile/stratum/replicate identities,
  digests, widths, and seven nonnegative score columns. The hash-bound reviewed
  evaluator supplies exact A/G/regret/gain and smaller-length ties.
- Selection: `profile_index % 8 < k` selects exactly replicate prefix `0..k−1`
  in each of all 40 strata for `k={1,4,8}`, yielding N={40,160,320}. The sets are
  strictly nested, and `k=8` selects every baseline row exactly once.
- Nine cells: three fixed masters are evaluated at each of three scales,
  producing exactly nine records with exact A/G/regret/gain, global action,
  adaptive action counts, digest, scale, and profile count.
- Full-scale equality: the `k=8` records reuse the identical bound table, strict
  parser, and reviewed evaluator as the core. The runner additionally checks
  master identity, A, G, regret, and exact gain against all three committed core
  records; deterministic ties and action counts therefore derive identically as
  well.
- Aggregate: all-clear is the exact fraction of nine gains satisfying `gain ≥ 5`;
  by-scale means are exact Fractions over three masters. Metric names satisfy the
  canonical extractor.
- Evidence sufficiency: the nine-cell TSV plus canonical summary, exact bound
  baseline, committed selection function, and reviewed parser/evaluator are
  sufficient for independent row selection and recomputation.
- Provenance: runner/helper/config/baseline/reviewed-core/core-COMPLETE/core-
  summary and every output artifact are bound into COMPLETE-last, no-replace,
  self-verified publication.
- Authorized checks: static compilation PASS for both files; scaling toys 4/4;
  `git diff --check` PASS; workspace unchanged. The primary baseline table was
  not parsed or aggregated during review.
- Scope: no generation, live target, held-out/beacon, network, private-transfer,
  or Kaggle action exists.

Severity findings: HIGH none; MEDIUM none; LOW none.

The one-use T021 execution is permitted using only the exact preregistered
command and attempt identity. No held-out or Kaggle action is permitted.

## Gate Check

T027 passes `SOUND`; final/failed scaling attempts were absent at closure.

## Problem alignment

The review establishes an exact evidence-size-only comparison with full-scale
identity to the reviewed core.

## Decision

Close T027 and permit one exact T021 execution.

## Next Steps

Run once, verify the manifest, independently subset/recompute all nine cells,
then close or fail Phase 4.
