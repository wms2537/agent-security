# TBEA independent coding dispatch and agreement freeze

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 7  
**Task:** T042 · **Status:** two coders dispatched; outcomes unread

## Immutable parsed subject

The committed parser at `916ec64` was run once on the frozen label-blind bundle:

```text
tbea_parser parsed_bundle=PASS rows=18 events=877 source_span_match_rate=1.0 marker_counts={"boxed_answer":15,"explicit_delivery":409,"explicit_terminal_api":5,"explicit_terminal_token":2,"failure_terminal_claim":3,"implicit_log_end":6} parsed_manifest_sha256=8379b954769189443faf2ce7c73a6fab993553c009aab46d06dd518c580e2c4c
```

The marker counts are deterministic lexical facts, not coder judgments. The
parsed manifest, per-trace events, and raw label-blind text live only under the
ignored `artifacts/` tree.

## Dispatch

Two independent agents were assigned randomized aliases and identical frozen
instructions. They may read protocol 108, the annotation schema, parsed events,
and corresponding raw bundle text only. They may not read:

- the source MAST JSON or any `mast_annotation`;
- `state.json`, progress logs, note 109's prediction, or later notes;
- the other coder's record;
- prior outcome counts or association results; or
- web, model, or framework APIs.

Coder A writes only
`experiments/fixtures/tbea-c2-pilot-coder-a.json`; coder B writes only the
corresponding `coder-b.json`. Records contain categorical codes and event IDs,
not raw excerpts. Both artifacts must exist before either is inspected.

## Frozen agreement computation

`experiments/tbea_c2_agreement.py` is frozen before coder outputs are read. It:

1. authenticates the parsed manifest and every parsed file;
2. validates exact schema keys, enums, aliases, event references, ordering, and
   source-grounded authority values;
3. computes exact terminal-event and effective-authority agreement;
4. computes raw agreement and nominal Krippendorff alpha for visibility and the
   authority–evidence relation;
5. counts jointly recoverable traces per system and the maximum system share;
   and
6. applies every numeric gate from protocol 108 without adjudication.

Nominal alpha uses the pooled two-coder category frequencies, observed pairwise
disagreement, and finite-sample expected disagreement. Undefined alpha or fewer
than two observed categories fails the applicable gate. Its synthetic
PASS/FAIL fixtures must both behave correctly before this dispatch record is
committed.

## Interpretation fixed before results

- **PASS:** measurement feasibility only; it permits a later sample-size check
  and hypothesis formulation, not a positive scientific finding.
- **FAIL:** close the empirical PDPF/TBEA branch on the authorized MAST artifact.
  Do not adjudicate to manufacture gate passage, expand the sample, inspect
  labels, or return to the constructed PQF census.

No review round is charged. Phase 3, Kaggle, framework/model execution, attacks,
gated data, held-out tests, external messages, and publication remain closed.
