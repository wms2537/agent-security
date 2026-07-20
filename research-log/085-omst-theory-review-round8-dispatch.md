# OMST theory review — round 8 dispatch

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Artifact:** `research-log/084-hypothesis-iter-5-omst-v8-environment-conditional.md`  
**Normative specification:** `experiments/configs/omst-c2-v8-environment-conditional.json`  
**Closed code-as-text:** `experiments/omst_c2_v8_fixture.py` and
`experiments/run_omst_c2_v8_fixture.sh`  
**Immutable commit:** `629aef6`  
**Committed hypothesis line count:** 652  
**Claim type:** unconditional theory plus universal environment-conditional implication  
**Budget charged at dispatch:** 19/20

The sterile prompt is preserved below. It contains only the SciAgent reviewer
template fields and the previous review's issue list.

---

You are a skeptical peer reviewer at a top-tier scientific venue. You cannot
ask questions mid-task: return `Status: NEEDS_CONTEXT` if required material is
missing.

## Objective

Critically evaluate the immutable hypothesis from First Principles. Separate
the unconditional factorization theorem, exact witness, universal statement
`forall E, P(E)->C(E)`, per-environment source lemmas, within-cell guards, and
future observation. Reject circular antecedents, impossible gate ordering, or
source steps not actually bound.

## Material Under Review

Read completely:

- `research-log/084-hypothesis-iter-5-omst-v8-environment-conditional.md`;
- `experiments/configs/omst-c2-v8-environment-conditional.json`;
- `experiments/omst_c2_v8_fixture.py`; and
- `experiments/run_omst_c2_v8_fixture.sh`.

Target commit: `629aef6`. Report the hypothesis line count. Do not import or
execute LangGraph.

## Previous Review

Judge each as RESOLVED / IMPROVED / UNCHANGED / WORSE and seek new defects.

1. Split `P2a` static artifact identity from `P2b` atomic compiled runtime
   guards so the Phase-3 gate is dischargeable without an unbound compile-only
   execution.
2. Complete callable delivery through `_read.py`, LangGraph
   `_internal/_runnable.py`, and the acquired exact LangChain-core callback/
   runnable config sources.
3. Correct the START path: whole dict to START, then `_get_updates` field writes
   and branch trigger.
4. Parameterize by environment: `forall E, P(E)->C_task(E) and C_full(E)`, with
   runtime identity binding and `P(E0)=false` explicit.
5. Give an authoritative clean outer-shell invocation and correctly describe
   Python `-I`; remove ineffective variables.
6. Rename compiled checks as runtime guards and specify abort-before-observation.

## Output Contract

### 1. Blind Assessment

Independently re-derive/countermodel the theorem and witness, including empty,
infinite, and larger-domain cases.

Audit the universal conditional for circularity and testability. Check P1,
P2a, P2b, P3-P7, ordering, environment equality, and role-specific failure.

Audit the source trace: START whole-dict input, `_get_updates`, LastValue
availability, empty checkpoint/fresh channels/cache, `_proc_input`, task.input,
PregelNode.node, RunnableSeq first-step delivery, bound RunnableCallable,
LangChain-core callback/config premise, and capture-before-write.

Statically audit hashes, modes, cells, runtime-guard timing, authoritative outer
shell, child isolation, output semantics, and explicit absent packages. Do not
use runtime evidence.

Verify assumptions, alternatives, taxonomy, anti-stacking, Occam, and scope.

**Overall:** RIGOROUS / NEEDS_REVISION / FUNDAMENTALLY_FLAWED.

If RIGOROUS, list the exact theorem and source-conditional steps re-derived and
the strongest objection considered and defeated. If adverse, give exact
severity-ordered defects and locations.

### 2. Actionable Coaching

Suggest only correctness, testability, formulation, source-proof, and honest
scope improvements.

## Rules

- Do not pass out of politeness.
- Do not install, import, or execute LangGraph.
- Do not perform Kaggle, held-out, locked-test, live-target, operational attack,
  model-API, external-message, or publication action.
- Keep assessment and coaching separate and disclose uncertainty.

## Report

- **Status:** DONE / NEEDS_CONTEXT
- **Blind assessment**
- **Actionable coaching**
