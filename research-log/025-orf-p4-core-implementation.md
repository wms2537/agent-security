# ORF Phase-4 core implementation

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** dispatched, explicitly unexecuted

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

Pending implementation. Execution is explicitly forbidden until T016 passes.

## Problem alignment

This keeps the claimed moat test to one auditable action-scope replacement and
prevents implementation complexity from becoming the contribution.

## Decision

Dispatch one code implementer with no scientific run authority.

## Next Steps

Commit and deterministically inspect the unexecuted code, then dispatch the
sterile code reviewer. No held-out, network, or Kaggle action.
