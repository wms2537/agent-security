# HCMS-24 Phase-3 PoC decision-reconstruction repair

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Status:** repaired, unexecuted, fresh re-review required

This repair closes every final and adverse-axis finding in
`research-log/154-hcms24-poc-code-review-round-2.md`. It changes only the PoC
runner and pure/toy tests; the hypothesis, config, methods, clock, profiles,
predictions, attack and Kaggle state remain unchanged.

## Decision-complete evidence

- Candidate reconstruction now binds exact generation/replay message prefixes
  to trace messages, indexed suffixes, exact flags, predicates, score-cell
  signature, raw score, identity flag and replay coverage.
- Path reconstruction binds deterministic messages/hosts, exact indexed
  suffixes, return/outcome, timing and terminal generation time.
- Cell reconstruction derives counts, dropped paths, generation and replay
  totals/overages, cumulative ledger, replay coverage, score, attribution,
  duplicate signatures, scorer failures, timeout/exception state, validity and
  transition sequence from retained candidate/path/diagnostic evidence.
- The exact configured profile/master/Williams/method grid and one excluded
  safety coordinate are checked. Exception IDs, coordinates, traceback digest,
  partial-row hashes and in-flight snapshots are linked and rederived.
- Recomputed cells drive independent aggregates, safety, Williams balance,
  invalidities, joint conditions and final status after disk reload.

## Invalid but auditable outcomes

Readable semantic discrepancies are collected as a deterministic set of
malformed artifact names. They force `status=invalid` but no longer prevent
stdout, hashed `run.log`, and COMPLETE-last publication. Unreadable schemas or
files still fail closed. An adversarial toy mutates a decision-critical cell,
reconstructs a nonzero malformed set, and verifies the reloaded bundle remains
auditable and invalid.

## Real failure checkpointing

The kernel checkpoints active generation paths, generated-but-unreplayed
candidates, completed candidate rows, and current replay traces before and
after risky reset/interaction calls. An injected failure through the actual
kernel preserves the in-flight replay message and event suffix in the linked
diagnostic. A successful injected kernel cell also exactly equals its
independent reconstruction.

## Direct sterile verification

```text
python_compile=PASS
toy_tests=15/15 PASS
git_diff_check=PASS
runner_lines=2598
test_lines=749
runner_sha256=b7206a89256f84dcfc4c4f9b30798a0cf542c4a6254f67c81aefd28fdd52845f
tests_sha256=8139dfac33e12233b38e220fcc10fe80559ae2ca4a2dc4d958d5006a4baf7d62
canonical_attempt_absent=PASS
scientific_attempts=0/3
```

`ruff` and `mypy` are not installed in the competition environment; this is a
tool-availability note, not a failed check.

## Gate

Scientific execution remains forbidden until a fresh immutable specification
review returns SOUND. No attack mutation, Kaggle push, or Kaggle submission was
performed.
