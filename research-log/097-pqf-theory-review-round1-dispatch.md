# PQF theory review — round 1 dispatch

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6
**Task:** T038 · **Status:** dispatched

**Artifact:** `research-log/094-hypothesis-iter-6-pqf-v1.md`  
**Immutable hypothesis/config commit:** `229519e`  
**Committed hypothesis line count:** 545  
**Claim type:** empirical/systems with a supporting classical structural
proposition  
**Question type:** causal within fixed matched finite interventions; diagnostic
outside them  
**Budget charged at dispatch:** 21/30

The reviewer dispatch uses the SciAgent theory-reviewer template with only its
round-1 placeholders filled. It contains no previous review, escalation
constraint, author assurances, project learnings, or prior-review history. The
reviewer is directed to read the complete hypothesis from disk and to produce
separate blind-assessment and coaching sections.

## Deterministic pre-dispatch evidence

```text
git show HEAD:research-log/094-hypothesis-iter-6-pqf-v1.md | wc -l
545
```

```text
pqf_hypothesis_v1=PASS lines=545 json=PASS ast=PASS finite_factor_models=16 theorem_counterexamples=0 advisory_invariance_comparisons=64 quotient_mutants_killed=4/4 oracle_mutants_killed=5/5 receipt_soundness_counterexample=PASS co_design_mutant_masked_counterexample=true masters=72 planned_executions=1440 review=unavailable_20_of_20 phase3=not_authorized
```

The stale `review=unavailable_20_of_20` field is an immutable author-check output
recorded before the user extended the budget; it does not control current state.
Current authoritative accounting is 21/30.

## Boundaries

Review only. No experiment, framework acquisition/import/run, model API,
natural-language attack generation, Kaggle action, held-out/locked-test action,
live target, external message, or publication action is authorized.

## Problem alignment

This independent review is the final Phase-2 judgment gate before PQF can enter
a minimal proof-of-concept phase.
