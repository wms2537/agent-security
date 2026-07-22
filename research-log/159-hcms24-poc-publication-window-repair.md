# HCMS-24 Phase-3 PoC publication-window repair

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Status:** repaired, unexecuted, final re-review required

This narrow repair closes both blockers in
`research-log/158-hcms24-poc-code-review-round-4.md`.

## Schema correction

`cumulative_costs_json` now belongs exclusively to `PATH_FIELDS`, matching the
row that emits it and the policy reconstruction that consumes it. A nonempty
real-kernel toy path is written through the exact TSV schema, reloaded,
decoded, and independently reconstructed; the test also asserts the field is
absent from `CANDIDATE_FIELDS`.

## Candidate/path publication transaction

Candidate append, decision checkpoint, path append, and published-path
checkpoint now execute inside one guarded region. The in-flight state records
the complete pending path and logical candidate before path publication and
records all generated candidates after publication. If any step times out, a
failure checkpoint preserves the pending records.

Exception-time cell reconstruction is now guarded. If a publication-window
snapshot cannot yet satisfy the returned-path/candidate bijection, the
diagnostic records the reconstruction failure and the cell becomes a
deterministic invalid sentinel. The attempt can therefore continue to its
auditable invalid bundle instead of escaping.

An injected `MethodCellTimeout` exactly at the decision checkpoint verifies:

- no partial candidate/path row is misreported as complete;
- pending path and current candidate survive in the diagnostic;
- timeout and invalid cell flags are retained;
- reconstruction failure is explicit rather than thrown from the wrapper.

## Direct sterile verification

```text
python_compile=PASS
toy_tests=15/15 PASS
nonempty_path_tsv_roundtrip=PASS
candidate_path_publication_timeout=PASS
git_diff_check=PASS
duplicate_literal_keys=0
runner_lines=2955
test_lines=917
runner_sha256=7b030c67a7f18c4bce77db67f7db757b817aede7cbaf75aa1195a09d42f6b1f6
tests_sha256=040ff524960550ed5a7d48d7f8dd8fb1e9f05141a18857c3b3f3f66499b7ad1f
canonical_attempt_absent=PASS
scientific_attempts=0/3
```

The hypothesis, config, methods, clocks, profiles, predictions, attack and
Kaggle state remain unchanged. Scientific execution remains closed until a
fresh immutable review returns SOUND.
