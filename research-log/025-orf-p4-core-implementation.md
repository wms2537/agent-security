# ORF Phase-4 core implementation

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed, explicitly unexecuted

## Context

The exact N=3 global baseline passed. T015 now implements the single clean core
change required for the Phase-4 code-review gate. The core result must remain
unobserved until the code is committed and independently reviewed.

## Content

The implementation will read the committed 960-row baseline score table. For
each master it will recompute the baseline aggregate `G` from column sums and the
core aggregate `A` from the sum of row maxima, with smaller-length tie-breaking.
No profile, score, resource, action, master, or threshold changes. It will also
construct the three frozen homogeneous controls and require exact zero regret and
length-one choices.

The program must use repository-relative paths, exact integer/Fraction arithmetic,
canonical outputs, and word-only stdout metric names compatible with
`grep '^[a-z_]*:'`. Toy unit tests may execute, but neither the core program nor
any calculation over the committed primary tables may run in T015.

## Gate Check

- Static compilation returned `static_compile=PASS`.
- Toy-only execution returned `Ran 4 tests in 0.000s` and `OK`; tests cover
  exact adaptive/global arithmetic, smaller-length ties, score typing, and
  display rendering without reading the primary table.
- `rg` found the committed baseline-table SHA-256 constant and its mandatory
  mismatch failure, plus all word-only primary/control stdout names.
- `test ! -e` verified absence of `run.log`, `core-summary.json`,
  `core-by-master.tsv`, and `homogeneous-by-master.tsv`.
- No primary table was aggregated by the implementation agent and no Phase-4
  master was generated.

## Problem alignment

This keeps the claimed moat test to one auditable action-scope replacement and
prevents implementation complexity from becoming the contribution.

## Decision

Commit the unexecuted implementation for sterile review. Orchestrator inspection
added one pre-review correction: bind the committed baseline table SHA-256
`331e8b5e16b42d8781df68fd49aa9cd83a4d77c8f5ec0ab9de15e09137e59cbf`
rather than merely recording whatever hash is present at execution.

## Next Steps

Dispatch the sterile code reviewer against the committed baseline and unexecuted
core implementation. No held-out, network, or Kaggle action.
