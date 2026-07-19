# ORF Phase-4 scaling implementation

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** implemented, unexecuted and pending focused review

## Context

T021's prediction and nested selection were committed in research-log/038 before
implementation. A delegated attempt was interrupted after producing no workspace
change. The orchestrator implemented the same deterministic wrapper; no primary
cell was evaluated.

## Content

The 325-line runner SHA-256 is
`6f5fa9a8bb4c61e969b6e0393f57c04cc97db479c7074a76977ed1903bd59bc5`.
It binds the config/baseline/helper/reviewed-core/core evidence, opens the
transaction before table parsing, reuses the reviewed strict baseline parser and
evaluator, selects exact replicate prefixes per stratum, emits nine exact cells,
and requires the full-scale cells to equal committed core evidence.

The 61-line toy suite SHA-256 is
`19f806da99c4cab4c456d951c796d13fb1c41e96b1b4639eeecea31834608609`.

## Gate Check

- Static compilation passes for both files.
- `test_toy_scaling.py`: `Ran 4 tests in 0.001s` / `OK`, covering exact nested
  counts, strict per-stratum replicate prefixes, reviewed evaluator arithmetic,
  and cell-render schema.
- `git diff --check` passes.
- `experiments/runs/orf-p4-scaling-v1` is absent; no primary table was parsed by
  the scientific runner and no scale cell exists.

Local checks pass. T027 will review nesting/full-scale equality/evidence before
execution.

## Problem alignment

The wrapper isolates evidence-set size without changing labels, profile rows,
actions, scoring, or policy logic.

## Decision

Commit unexecuted code/tests and request focused sterile review.

## Next Steps

Run no scientific scaling command before T027 is `SOUND`.
