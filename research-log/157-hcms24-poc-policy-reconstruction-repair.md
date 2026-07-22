# HCMS-24 Phase-3 PoC policy-reconstruction repair

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Status:** repaired, unexecuted, fresh re-review required

This fourth implementation repair closes all findings in
`research-log/156-hcms24-poc-code-review-round-3.md` without changing the
frozen HCMS hypothesis, config, profiles, clocks, prediction rows, attack, or
Kaggle state.

## Config-derived method decisions

Every path now retains its full cumulative generation-cost vector. The audit
recompiles the named config policy and independently reconstructs:

- proposal and state before each path;
- exact longest permitted prefix and drop reason;
- calibrated or scalar ledger formula and cumulative charge;
- candidate/path cost, host, message, trace and state correspondence;
- a bijection between every returned path and one logical candidate, including
  generated-but-not-yet-replayed candidates in exception evidence;
- monotone state transitions, path sequencing, generation timing order, legal
  mid-path truncation and legal method termination at cap/deadline;
- replay coverage against the reconstructed charge rather than an emitted
  charge field.

Coherent ledger-field mutation, an omitted returned candidate, state drift and
premature stopping are therefore invalid rather than self-consistent.

## Timeout-safe evidence

Reset and interaction success handling now captures trace/suffix/cost evidence
inside the protected `try` region and checkpoints immediately afterward.
Replay checkpoints distinguish the current candidate, later unreplayed
candidates, completed candidate rows and replay status. A completed row is
followed by an immediate checkpoint, while a timeout in the narrow append
window remains auditable by deduplicating the completed row and current
candidate.

Exception-cell scientific totals use only completed path/candidate evidence;
self-hashed active timing and partial replay elapsed are diagnostic only. An
unreconstructable cell becomes a deterministic invalid sentinel and never
falls back to source metrics.

## Exact audit identity

`primary_summary.json` now records the sorted malformed artifact names as well
as their count. Reload reconstructs the same set, and `main` requires exact
source/reload set equality before publication; equal cardinality with different
members cannot pass.

## Direct sterile verification

```text
python_compile=PASS
toy_tests=15/15 PASS
git_diff_check=PASS
duplicate_literal_keys=0
runner_lines=2915
test_lines=856
runner_sha256=d108710a551033ecd07331670a83d0609c2487d0e914faf7e02f94694d1601b3
tests_sha256=da38bf598ab3caeac19067602304c2d81726db188283dc2b663a6c63c3ad336f
canonical_attempt_absent=PASS
scientific_attempts=0/3
```

The 15 tests now include multiple assertions per real-kernel case: coherent
ledger drift, returned-path omission, config state drift, post-success trace
capture timeout, mutation of untrusted in-flight elapsed time, exact malformed
set equality, and successful complete-cell reconstruction.

## Gate

Scientific execution remains forbidden until a fresh immutable review returns
SOUND. No attack mutation, Kaggle push, or Kaggle submission was performed.
