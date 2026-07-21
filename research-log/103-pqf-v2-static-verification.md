# PQF v2 static verification and author audit

**Date:** 2026-07-22  
**Phase:** 2 · **Cycle:** 2 · **Iteration:** 6 · **Task:** T039  
**Artifact under audit:** `research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md`  
**Normative contract:** `experiments/configs/pqf-c2-v2.json`  
**Verifier:** `experiments/pqf_c2_v2_static_verify.py`  
**Status:** deterministic author gate passed; independent theory review pending

## Exact commands

```bash
python -m json.tool experiments/configs/pqf-c2-v2.json >/dev/null
python experiments/pqf_c2_v2_static_verify.py \
  experiments/configs/pqf-c2-v2.json \
  research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md
git diff --check
wc -l \
  research-log/101-pqf-v2-authority-isolation-redesign.md \
  research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md \
  experiments/configs/pqf-c2-v2.json \
  experiments/pqf_c2_v2_static_verify.py
sha256sum \
  research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md \
  experiments/configs/pqf-c2-v2.json \
  experiments/pqf_c2_v2_static_verify.py
```

## Exact output

```text
pqf_hypothesis_v2=PASS lines=611 json=PASS ast=PASS finite_factor_models=16 theorem_counterexamples=0 authority_truth_rows=48 disagreement_rows=12 visibility_differences=0 advisory_schedules=25 exogeneity_comparisons=300 oracle_mutants_killed=6/6 unique_oracle_fixtures=6/6 false_receipt_counterexample=PASS primary_executions=1200 secondary_executions=3200 review=pending phase3=not_authorized
  209 research-log/101-pqf-v2-authority-isolation-redesign.md
  611 research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md
  387 experiments/configs/pqf-c2-v2.json
  468 experiments/pqf_c2_v2_static_verify.py
 1675 total
67fcec4d4db275de6a8d7ee6fb54f44aecef0eb088fca7c4e70875e0e9d9b7b7  research-log/102-hypothesis-iter-6-pqf-v2-authority-isolation.md
63ffb7a4431ee9f955de164476431ca733dc4386533dba6283f988225d006246  experiments/configs/pqf-c2-v2.json
75ec399a7a1d2a750007c10a0507b06cc126b65c73e7169e99026e639fc0d12f  experiments/pqf_c2_v2_static_verify.py
```

`git diff --check` returned no output.

## What the static gate establishes

1. The factorization proposition has no counterexample in all 16 enumerated
   two-history models.
2. The isolated controller theorem holds over all 48 valid `z x u` rows: the
   authority-on/off policies differ in exactly the 12 disagreement rows, and
   hidden versus visible non-authoritative policies never differ.
3. The 25 schedule identifiers are fixed independently of all three modes; all
   300 enumerated outcome-label/mode comparisons use the same lookup result.
4. The independent oracle has six separate clause-removal mutants and six
   fixtures, each uniquely decisive for one clause. The required kill matrix is
   6/6, not the v1 five-mutant proxy.
5. A false accepted completion receipt makes the base controller return
   `STOP_SUCCESS` while the world-only oracle reports `premature_success`, so
   receipt soundness is an explicit boundary rather than a hidden guarantee.
6. Contract counts agree with the prose: 1,200 proposed primary executions and
   3,200 proposed secondary executions. No census was run.

## Adversarial author audit

### Causal isolation

The primary pair changes exactly the Boolean `advisory_authority` branch.
Receipts, projection, base policy, recovery setting, world schedule, budget and
oracle are common. Visibility is controlled by a third mode at authority off.
This closes the bundled-treatment defect as a testable protocol constraint.

### Advice assignment

Advice is indexed only by `(master_id, schedule_id, decision_index)` and is
defined before mode assignment. It is not recomputed from the realized state.
The clean tape is derived from a canonical authority-off trajectory; after any
treated divergence it remains the same predeclared tape. This is exogenous to
the realized treatment path, though purpose-built rather than representative of
model errors.

The 24 substitution identifiers enumerate eight positions crossed with three
values and retain no-op, harmless and unreachable interventions. Some different
identifiers may carry byte-identical tapes when the substituted value equals the
clean value. They remain distinct cells of the fixed index-by-value intervention
domain; v2 does not call them 25 distinct tape contents or infer a natural error
distribution from their equal weighting.

### Non-guaranteed result and triviality boundary

The local controller difference is an algebraic identity, but the joint outcome
claim is not that identity. The independent world oracle, position reachability,
base-policy failures, completion guardrail, overhead guardrail and measured
`F_on>=0.10` floor can each defeat support. The design nevertheless remains a
deterministic causal unit test. It must not be described as evidence about error
prevalence, natural-language attacks, models or production systems.

### Total semantics and measurement independence

The nine-step ordering defines receipt delivery, state derivation, advisory
lookup, action, terminal no-op, check and budget decrement. The oracle reads
trusted plan, world events, action events and the budget only; it cannot consume
controller predicates or advisory labels. Its two budget clauses have different
fixtures and mutants. These properties are assertions for a future
implementation gate, not evidence that such an implementation already exists.

### Decision rule

One joint primary rule governs support. For the removal intervention, completion
loss is `completion_on - completion_off`; clean step overhead is
`(steps_off-steps_on)/steps_on`. A valid materiality-floor miss is explicitly
inconclusive and non-supportive; every other valid threshold miss at or above the
floor disconfirms. Secondary results cannot rescue or disconfirm the primary
claim.

### Remaining live objections for independent review

- The equal-weighted index-by-value intervention population is normative and
  may still be judged too constructed for a meaningful empirical claim.
- The anti-stacking prediction is structural; a comparator that adopts the same
  authority gate has adopted the intervention. A reviewer may still find this
  insufficiently distinctive.
- Exact sound receipts and complete trusted plans are strong assumptions.
- The four-predicate projection is chosen for one policy. No minimality,
  necessity, general sufficiency or transfer claim remains.
- Passing this static verifier cannot validate the proposed execution engine or
  the 4,400 unexecuted outcomes.

## Gate decision

The v2 artifacts are internally consistent enough to freeze for a sterile,
context-complete theory re-review. This is not a `RIGOROUS` verdict and does not
open Phase 3. Hypothesis-review accounting remains 22/30 until dispatch.

No primary/secondary experiment, framework action, model API, attack generation,
Kaggle action, held-out/locked-test action, live target, external message or
publication occurred.
