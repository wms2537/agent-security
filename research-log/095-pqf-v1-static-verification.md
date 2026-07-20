# PQF v1 author-side static verification

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6
**Task:** T037 · **Status:** author checks pass; independent review unavailable

## Scope

This is a deterministic contract/theory check, not the proposed Phase-3 PoC or
the 1,440-execution validation. It parses repository-authored JSON/Python,
exhausts a small Boolean factorization model, checks decision invariance for
finite quotient samples, and exercises contract mutants/counterexamples. It
does not import or execute an agent framework, call a model, generate an attack,
access Kaggle, or create/inspect a locked test.

## Frozen subjects before commit

| Artifact | Lines | SHA-256 |
|---|---:|---|
| `research-log/093-pqf-prior-art-and-oracle-first-design.md` | 189 | recorded by commit object rather than embedded self-hash |
| `research-log/094-hypothesis-iter-6-pqf-v1.md` | 545 | `2c1191a2e3c91bc3113b84e97cde512ab9e1c576201925df4b71c5621f0997f6` |
| `experiments/configs/pqf-c2-v1.json` | 387 | `e6deca7fb0a6696fa7193ab1be813f860ca58cb9481cc7d854b8489e43a675a2` |
| `experiments/pqf_c2_v1_static_verify.py` | 491 | `b77d90a26abe7ed44cb15702250491b5da77a29f45249ef548c052e14b771871` |

The Git commit created after this note is the authoritative immutable binding.

## Verification command

```bash
python -m json.tool experiments/configs/pqf-c2-v1.json >/dev/null
python experiments/pqf_c2_v1_static_verify.py \
  experiments/configs/pqf-c2-v1.json \
  research-log/094-hypothesis-iter-6-pqf-v1.md
git diff --check
```

Exact verifier output:

```text
pqf_hypothesis_v1=PASS lines=545 json=PASS ast=PASS finite_factor_models=16 theorem_counterexamples=0 advisory_invariance_comparisons=64 quotient_mutants_killed=4/4 oracle_mutants_killed=5/5 receipt_soundness_counterexample=PASS co_design_mutant_masked_counterexample=true masters=72 planned_executions=1440 review=unavailable_20_of_20 phase3=not_authorized
```

## What the checks establish

1. The JSON contract parses and binds seven quotient fields, five actions, 72
   masters, 1,440 planned conditions, seven assumptions, nine rivals, all eight
   fixed bias categories, thresholds 0.10/0.50/0.05/0.20, and an explicit 20/20
   review-budget stop.
2. Exhaustion of all 16 Boolean controllers over two two-history quotient fibers
   finds zero counterexamples to “factorization iff fiber constancy.” This is a
   small model of the classical proposition, not a general proof assistant.
3. PQF makes 64 identical-decision comparisons across the finite quotient
   samples and five advisory labels with zero differences.
4. All four forbidden information-channel mutants change a decision and are
   killed: direct advisory, worker-summary digest, unverified completion ID, and
   raw-payload branch.
5. Independent-oracle fixtures expose all five clause-removal mutants:
   premature success, false fault, budget-incomplete, post-terminal overrun, and
   duplicate effect.
6. The false-accept receipt counterexample makes PQF choose `STOP_SUCCESS` while
   the world oracle reports premature success. The invalid co-designed oracle
   masks that failure, so the check distinguishes the representations.
7. The oracle evaluates commits and faults at or before the controller stop. An
   effect/fault scheduled after a stop cannot retroactively make that stop valid.

## Defects found and corrected before this record

The author-side audit made three material corrections rather than preserving a
clean first draft:

1. **Duplicated hard-cap baseline.** The initial worker and hard-cap descriptions
   both used the same ceiling. v1 now gives every controller a common emergency
   ceiling `B_max` and defines a separate earlier `B_cap` only for the hard-cap
   secondary policy. The primary worker/PQF contrast keeps `B_max` matched.
2. **After-stop truth leakage.** The first oracle sketch could treat an effect or
   fault later in the canonical schedule as if it justified an earlier stop. The
   executable oracle fixture now evaluates truth at the stop step and includes
   future-event negative cases.
3. **Unit ambiguity.** Completion loss now has both an executable rate bound
   `0.05` and a display value of five percentage points, preventing an
   implementation from accidentally comparing a rate with the integer `5`.

## Phase-2 author checklist

| Gate item | Author status | Evidence |
|---|---|---|
| Falsifiable claim, variables, controls, one primary comparison | PASS | hypothesis §§ Primary, Variables, Primary comparison |
| Search dimension | PASS PENDING STATE RECORD | `termination-observation-boundary`, kind `metric` |
| Named and formal concept | PASS | exact seven-field quotient and controller map |
| Systems justification and citations | PASS | causal chain, six current primary works, measurement design |
| Failure modes | PASS | invalid/support/disconfirm/inconclusive separated |
| Concrete metrics | PASS | 0.10/0.50/0.05/0.20 plus exact validity gates |
| Taxonomy | PASS | Failure/Risk Gap × Extrapolation/Robustification; replace/decouple |
| Anti-stacking | PASS AUTHOR CLAIM | quotient invariance plus independent utility/cost prediction |
| Problem alignment | PASS | final alignment section |
| Independent theory review | **NOT PASSED** | cumulative budget exhausted 20/20; no dispatch |

## Remaining blockers

- No independent reviewer has tested the controller semantics, oracle
  independence, construct validity, novelty boundary, or whether the finite
  abstract workload is too definitionally favorable.
- Therefore SciAgent Phase 2 remains open/failed even though author checks pass.
- No Phase-3 simulator execution or later phase may begin without a user-granted
  hypothesis-review extension and a `RIGOROUS` verdict with scrutiny evidence.
