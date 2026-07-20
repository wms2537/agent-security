# OMST theory review — round 7 dispatch

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Artifact:** `research-log/080-hypothesis-iter-5-omst-v7-conditional-correspondence.md`  
**Normative specification:** `experiments/configs/omst-c2-v7-conditional-correspondence.json`  
**Closed code-as-text:** `experiments/omst_c2_v7_fixture.py` and
`experiments/run_omst_c2_v7_fixture.sh`  
**Immutable commit:** `80e0764`  
**Committed hypothesis line count:** 592  
**Claim type:** unconditional theory plus conditional engineering implication  
**Budget charged at dispatch:** 18/20

The sterile prompt is preserved below. It contains only the SciAgent reviewer
template fields and the previous review's issue list.

---

You are a skeptical peer reviewer at a top-tier scientific venue (NeurIPS,
ICML, Nature). You cannot ask questions mid-task: if the material below is
incomplete, return Status: NEEDS_CONTEXT naming what is missing.

## Objective

Rigorously evaluate the hypothesis and justification below. You MUST be
critical. Use Socratic questioning and First Principles. Separate
unconditional mathematics, the typed witness, the conditional implication
`P -> C`, source lemmas, currently false/undischarged premises, and future
runtime checks. Refuse to pass on an implication whose antecedent hides its
conclusion.

## Material Under Review

Read the complete committed hypothesis:
`research-log/080-hypothesis-iter-5-omst-v7-conditional-correspondence.md`.

Cross-check it against:

- `experiments/configs/omst-c2-v7-conditional-correspondence.json`;
- `experiments/omst_c2_v7_fixture.py`; and
- `experiments/run_omst_c2_v7_fixture.sh`.

The immutable target commit is `80e0764`. Report the hypothesis line count; it
will be verified against Git. Do not import or execute LangGraph.

The claim type is **unconditional formal derivation plus a conditional
engineering implication**. Independently re-derive the mathematics. For the
engineering claim, judge whether `P -> C_task/C_full` is valid and testable,
not whether `P` is currently discharged. Reject any sentence that smuggles
unconditional correspondence back into scope.

## Previous Review

For each item, judge RESOLVED / IMPROVED / UNCHANGED / WORSE, then seek new
defects.

1. **Close the engineering proof:** derive rather than assume the loop,
   checkpoint/channel freshness, input application, availability, task
   construction, and callable delivery—or state a correctly scoped conditional
   proposition whose antecedent owns unresolved environment facts.
2. **Replace environment/source placeholders:** give literal current values and
   explicitly control callbacks, tracing, import context, and unacquired
   dependency identity.
3. **Make the fixture closed:** bind states, schemas, all four cells, isolated
   launcher, compiled assertions, and capture mechanism.
4. **Correct canonicalization wording:** include JSON containers with primitive
   leaves.

## Output Contract — TWO separate outputs

### 1. Blind Assessment

**Mathematics:** Independently prove or countermodel existence, uniqueness,
empty/infinite cases, larger-domain statement, and typed witness. Seek finite
countermodels.

**Conditional Logic:** Determine whether P1-P7 are independently testable
environment/source premises or circularly contain `C_task/C_full`. Re-derive
`P -> C_task/C_full`. Confirm that current dependency absence is explicit and
that no unconditional framework inference is made.

**Source Correspondence:** Audit `L_compile`, `L_fresh`, `L_prepare`, and
`L_deliver` against pinned LangGraph 1.2.9 commit paths. Check START input,
GraphState writes, LastValue availability, mapper, fresh cache/checkpoint,
task.input, `run_with_retry`, callbacks/imports, and capture-before-write.

**Fixture Closure:** Statically inspect exact cells, schemas, config, service
assertions, launcher isolation, actual hashes, output semantics, and the fact
that the framework is absent/unexecuted. Identify any code/spec mismatch.

**Logical Soundness and Assumptions:** Separate theorem, witness, conditional
source proposition, acquisition gate, future execution, and application. State
which failures affect which claim.

**Taxonomy / Anti-Stacking / Occam / Alternatives:** Verify classical scope,
universal-function quantifier, minimality, and rival explanations without
crediting future runtime evidence.

**Overall:** RIGOROUS / NEEDS_REVISION / FUNDAMENTALLY_FLAWED

- If RIGOROUS, list exact mathematical and conditional-source steps re-derived
  and the strongest objection considered and defeated.
- If NEEDS_REVISION, give severity-ordered issues with exact locations.
- If FUNDAMENTALLY_FLAWED, explain why the core cannot be salvaged.

### 2. Actionable Coaching

Suggest only correctness, testability, formulation, source-proof, and honest
scope improvements.

## Rules

- Do not pass out of politeness.
- Keep assessment and coaching separate.
- Do not install, import, or execute LangGraph.
- Do not perform Kaggle, held-out, locked-test, live-target, operational attack,
  model-API, external-message, or publication action.
- Be specific and disclose uncertainty.

## Report

- **Status:** DONE / NEEDS_CONTEXT
- **Blind assessment** as specified
- **Actionable coaching** as specified
