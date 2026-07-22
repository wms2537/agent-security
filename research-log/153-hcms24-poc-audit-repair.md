# HCMS-24 Phase-3 PoC audit repair

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Status:** repaired, unexecuted, targeted re-review required

This checkpoint repairs the three HIGH and one MEDIUM blockers in
`research-log/152-hcms24-poc-code-review-round-1.md` without changing the
frozen hypothesis, methods, profiles, clocks, counterbalancing, attack, or
prediction rows.

## Repair disposition

1. **Runtime provenance — repaired.** The transaction now pins 69 SDK/mock
   Python files, verifies the exact 26-file fixture tree (membership and
   bytes), retains the config/source/evidence bindings, and binds the runner
   itself at execution.
2. **Nested and scorer evidence — repaired.** Candidate and path rows now
   retain messages, deterministic hosts, indexed generation/replay suffixes,
   exactness flags, complete traces, predicates, score-cell signatures, and
   findings. Reload validation recomputes attribution and scorer identity from
   the emitted evidence.
3. **Exceptions — repaired.** A shared cell wrapper emits linked diagnostics
   with phase, type, message, timeout status, elapsed time, traceback and
   digest, plus hashes/counts for retained partial candidates and paths.
4. **Transaction integrity — repaired.** Every TSV and JSON output is reloaded
   and reconciled before publication. Final metrics are flushed into
   `run.log`; the log and all ten outputs are then hashed; `COMPLETE.json` is
   exclusively published last. `malformed_artifact_count` is derived instead
   of hard-coded.

The repair deliberately keeps one runner module despite the non-blocking
maintainability review: splitting scientific logic immediately before the
one-shot run would enlarge the reviewed surface without improving the frozen
claim.

## Direct sterile verification

```text
python_compile=PASS
toy_tests=13/13 PASS
git_diff_check=PASS
runner_lines=2049
test_lines=459
runner_sha256=ed82d4a02c8fdf4fda0d40ff0f864595b48cd88765db6df09e7b843f6abb87e3
tests_sha256=3a47189b85ab50832e46d0a2968ba1ccd7069387cfba31e16a9f8faaf1eb2203
canonical_attempt_absent=PASS
scientific_attempts=0/3
```

The added adversarial toys cover binding/tree mutation, independently
recomputable candidate evidence, exception/partial-evidence linkage, complete
bundle reload and aggregate mutation, and late `run.log` mutation after
publication.

## Gate

Scientific execution remains closed until a fresh targeted specification
review returns SOUND. No competition attack, Kaggle push, or Kaggle submission
was performed.
