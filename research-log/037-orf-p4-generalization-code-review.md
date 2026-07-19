# ORF Phase-4 generalization code review

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Verdict:** SOUND

## Context

Focused sterile review examined target `4063a34`; `c7060f1` changed review
metadata only. Fixed masters remained ungenerated.

## Verbatim reviewer report

SOUND

Blind assessment

- Line counts: preregistration 78; implementation log 58; generalization runner
  404; toy suite 84; frozen config 107; immutable support 333; reviewed core 742;
  bundle helper 605.
- Predictions-before-code: `6fc4df8` is the direct parent of `4063a34`; both
  unresolved ledger rows, the 35% prediction, `[30,45]` interval, all-clear
  prediction, labels, regime, command, evidence, and stop rules precede
  implementation. `c7060f1` changes only review metadata.
- Exact bindings: runner SHA `25f88db0…b59f`, toys SHA `10d61b0…eaa`, and all
  helper/config/support/core/core-COMPLETE/core-summary hashes match. Bound
  scientific inputs are unchanged from preregistration.
- Command/attempt: isolated-mode, working-directory, exact `sys.argv`, canonical
  command, lexical final identity, and fresh direct-child bundle constraints are
  enforced. Final and failed generalization attempts are absent.
- Transaction ordering: imports and hash checks have no generation side effects;
  fixed-master hashing, generation, scoring, and aggregation begin only after
  staging creation and canonical first-line log publication.
- Labels: exactly three unique config-matched ASCII preimages use one
  `SHA256(preimage)` derivation. Their domains are disjoint from primary and
  calibration labels; the digest is reused directly for generation and evidence.
- Generator/regime: the hash-bound immutable crossed generator supplies exactly
  320 profiles per master. Legal cliffs are enforced; 64 physical no-cliff and
  256 physical cliff profiles are asserted. Scoring uses immutable support at
  exact `H=10^18`.
- Weighting: no-cliff weight four and cliff weight one yield `64×4=256`,
  `256×1=256`, total effective weight 512 per master. Only weights one/four are
  accepted.
- Estimator fairness: exact row replication is algebraically identical to
  weighted adaptive maxima and weighted global column totals. The hash-bound
  reviewed evaluator and smaller-length tie rule are reused unchanged for both
  policies.
- Evidence sufficiency: 960 physical rows expose identities, strata/replicates,
  cliffs, weights, exact costs, events, scores, and floor margins. Three master
  records expose exact weighted A/G/regret/gain, global action, and weighted
  adaptive counts. These suffice for independent recomputation.
- Aggregates: per-master gains are exact fractions; the three-master mean and
  all-clear fraction are exact, with fixed-decimal rendering only afterward.
  Metrics match the preregistered ledger names and contain no digits.
- Provenance: runner/helper/config/support/reviewed-core/core-COMPLETE/core-summary
  plus every output artifact are bound into COMPLETE-last, no-replace,
  self-verified publication.
- Toy corrections: both recorded failures are confined to toy fixtures—the
  expected digest assertion and a malformed three-column toy table corrected to
  seven columns. The runner does not import the toy module, contains no observed
  fixed-master digest or outcome, and no scientific attempt/output exists. No
  scientific code or decision was changed after observation.
- Authorized checks: static compilation PASS for both files; generalization toys
  5/5; `git diff --check` PASS; workspace unchanged.
- Scope: no held-out/beacon, network, private-transfer, external-post, or Kaggle
  action exists.

Severity findings: HIGH none; MEDIUM none; LOW none.

The one-use T020 run is permitted using only the exact preregistered command and
attempt identity. No held-out or Kaggle action is permitted.

## Gate Check

T026 passes `SOUND`; fixed masters and final attempt were absent at closure.

## Problem alignment

The review establishes a fair, auditable changed-regime test of the same
candidate-structure action scope.

## Decision

Close T026 and permit one exact T020 execution.

## Next Steps

Run the canonical command once, verify all 960 rows and weighted aggregates, and
resolve the prediction ledger.
