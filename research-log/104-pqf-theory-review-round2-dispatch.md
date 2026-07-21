# PQF theory review round 2 — dispatch record

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6  
**Task:** T040 · **Status:** dispatched  
**Immutable hypothesis commit:** `734b445`  
**Hypothesis path:** `research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md`  
**Committed line count:** 611  
**Hypothesis SHA-256:** `67fcec4d4db275de6a8d7ee6fb54f44aecef0eb088fca7c4e70875e0e9d9b7b7`  
**Config SHA-256:** `63ffb7a4431ee9f955de164476431ca733dc4386533dba6283f988225d006246`  
**Cumulative hypothesis-review budget:** 23/30

## Dispatch rationale

T039 completed the author gate, but SciAgent Phase 2 requires an independent
theory verdict. This is a fresh, sterile, context-complete re-review. The
reviewer receives the immutable v2 entry and normative config, both canonical
SciAgent reference paths that were missing in the first provisional dispatch,
and the exact ten-item issue list from the context-complete v1 verdict.

Every dispatch is charged, so accounting moves from 22 to 23 before the review
begins. The hypothesis is immutable during review.

## Previous-review issue list supplied verbatim

1. **Correct or isolate the causal estimand** — lines 187–196, 264–269, 320–341.
2. **Remove the guaranteed-failure baseline construction or explicitly recast the study as deterministic adversarial unit testing** — lines 239–269, 289–314.
3. **Make advisory assignment exogenous** — lines 223–230, 260–261.
4. **Define all terminal, receipt, and no-next-event transition semantics** — lines 271–280, 462–471.
5. **Add independent validation for all six outcome clauses** — lines 205–214, 422, 483.
6. **Resolve the contradictory support/disconfirmation rules** — lines 42–48, 65–69, 448–453, 508–510.
7. **Withdraw or prove quotient minimality** — lines 330, 365.
8. **Replace the anti-stacking prediction with one a receipt-plus-cap composition does not share** — lines 492–510.
9. **Define the raw full-state label and construct non-vacuous crossed quotient/advisory tests** — lines 57–64, 193–195.
10. **Justify or remove the receipt-stress monotonicity claim** — lines 70–73.

The old line references identify v1 and are retained exactly; the reviewer must
map them to v2 and grade each `RESOLVED / IMPROVED / UNCHANGED / WORSE`, then
check for new defects.

## Exact pre-dispatch verification

```text
$ git show HEAD:research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md | wc -l
611
$ git show HEAD:research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md | sha256sum
67fcec4d4db275de6a8d7ee6fb54f44aecef0eb088fca7c4e70875e0e9d9b7b7  -
$ git show HEAD:experiments/configs/pqf-c2-v2.json | sha256sum
63ffb7a4431ee9f955de164476431ca733dc4386533dba6283f988225d006246  -
```

No primary/secondary experiment, Phase-3 action, framework action, model API,
attack generation, Kaggle action, held-out/locked-test action, live target,
external message or publication is part of this dispatch.
