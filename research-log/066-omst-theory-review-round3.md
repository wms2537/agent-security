# OMST theory review — round 3

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

- **Status:** DONE
- **Artifact reviewed:** `research-log/064-hypothesis-iter-5-omst-v3.md`
- **Verified line count:** 831

## Blind assessment

### Re-review status

1. **Exact `V_prov`: IMPROVED, not resolved.**  
   The revision adds a canonical schema, four input classes, 17 clauses, and mutations. However, the predicate is still not a total executable relation:

   - The event schema at lines 364–387 has no `source_label`, yet P04 evaluates it.
   - It has no effect `operation` or capability-set representation, yet P16 evaluates both.
   - The input to the claimed “state machine over canonical event bytes” is therefore insufficient; condition, full pre-action record, input class, and initial capability appear to be hidden external inputs.
   - Per-kind required/null field rules are absent.
   - “accepted current provenance digest” in P15 is undefined as an algorithm.
   - Both chained authorizations occupy phase 1, while ordering by `(phase,kind,event_id)` does not guarantee parent-before-child.
   - The P17 mutant is defective: appending an `AUTHORIZE` event at phase 7 still sorts it before `COMPLETE`, so it need not create a post-completion event. A kind/phase mismatch is also not explicitly protocol-invalid.

2. **Treatment fidelity: IMPROVED, not resolved.**  
   The framework paths, schemas, callable, compiled-channel predicate, and matched coordinates are much stronger. The read-only observer at lines 298–311 remains underdefined: no pinned runtime hook, source/call path, invocation-count rule, observer code hash, or proof of noninterference beyond state-write prohibition is given. It also manufactures the pre-projection digest against which the action is judged, making it part of the outcome construction rather than passive instrumentation.

3. **Deterministic census: IMPROVED, not resolved.**  
   The SHA-256 mapping, graph strata, broad topology, input templates, tapes, and Latin order are specified. The description still does not uniquely generate execution bytes. Missing details include exact stage-node transfer functions, reducers/channel implementations, condition-specific graph rewrites, obligation bytes and placement, actor-ID generation, capability bytes, source/attestation/completion event construction, complete effect-record schema, and the exact execution command/environment manifest. Lines 501–545 define a grammar, not yet a complete generator.

4. **Residual runtime randomness: RESOLVED.**  
   Lines 547–575 state a concrete validity regime, exercise branching conditions across all 12 structural archetypes, require duplicate fresh-process execution, compare all scientific coordinates bytewise, and block rather than silently switch estimands. This resolution remains contingent on fully specifying the generator and observer.

### Justification correctness

The one-channel mechanism is causally clear, but the empirical frequency claim is forced by the intervention and oracle:

1. `TaskStateOnly` excludes `provenance_record`.
2. Side channels are forbidden.
3. The identical action emits a null digest when the record is absent.
4. The observer emits the non-null pre-boundary digest.
5. P13 and P15 reject the null digest.
6. The full-schema action receives the record and emits its digest.

Therefore, on every unit satisfying the stated fidelity and validity gates, `Y_task=1` and `Y_full=0`. `Delta_schema_pp=100` is not merely predicted; it is entailed. Any 10–99.99 or sub-10 result must violate the implementation, oracle, or fidelity premises and would be invalid rather than a valid empirical disconfirmation.

The non-redundancy gate correctly prevents a redundant census, but its answer is already logically “yes.” The branch permitting the 5,760-run empirical census has no coherent support under the current premises.

### Mathematical depth and validity domains

The finite estimand and equal weighting are concrete and correctly unpacked. The task-fiber interpretation is meaningful.

However, averaging over graphs adds no mathematical or empirical information once every protocol-valid unit is forced into the same `(Y_full,Y_task)=(0,1)` pair. The `q_g` and `q_k` notation then decorates a deterministic unit-test assertion.

Most assumptions have useful validity domains. A18 is incompatible with the preceding treatment and policy assumptions: context dependence cannot alter the result without causing a fidelity or protocol failure.

### Logical soundness

The deterministic source assertion is logically salvageable. The empirical materiality hypothesis is not presently falsifiable on a valid run. Lines 72–75 and 650–665 describe valid sub-100 outcomes, but the construction admits none.

The stopping rule avoids false empirical inflation, yet it leaves no confirmatory empirical path. The hypothesis should be reclassified before Phase 3 instead of using Phase 3 to discover a consequence already proven by its premises.

### Assumption completeness

The most conclusion-critical assumptions are A3, A4, A5, A6, A7, A8, and A13. Violating any prevents the claimed causal interpretation.

Two missing assumptions are load-bearing:

- The oracle receives an exact, immutable external context sufficient to evaluate source label, accepted provenance, operation, capability, input class, and condition.
- Observer-produced events are semantically equivalent to framework events and do not define the violation they purport to observe.

A5’s validity domain—“fixed observer code and trace schema”—is insufficient. Read-only observation can still alter checkpoint reads, scheduling, callbacks, exceptions, or trace ordering.

### Taxonomy verification

`Scope Mismatch × decouple` fits the local move. `Empirical Mapping` does not fit the current contribution because the result is entailed before empirical mapping begins. The accurate paradigm is deterministic verification or specification testing. Empirical Mapping would become appropriate only if graph/runtime context could legitimately vary the outcome while all validity predicates remained satisfied.

### Anti-stacking check

The one-channel rescue is a genuine minimal ablation and is not a defense stack. However, a plain compiled-channel unit test plus the declared action/oracle makes the same prediction. The rescue distinguishes the schema coordinate but does not establish a nontrivial empirical mechanism.

### Occam’s Razor check

Static source analysis plus one fixture fully answers the stated question. The non-redundancy gate correctly stops the large census, but that makes the current empirical hypothesis conceptually unnecessary. The gate should now be discharged analytically and the claim reclassified.

### Alternative explanations

A positive result can arise entirely from:

- the experiment-authored action emitting null when an intentionally excluded field is absent;
- the experiment-authored observer supplying the comparator digest;
- the policy declaring that exact null/digest mismatch a violation;
- adapter or trace-construction behavior rather than framework security behavior.

The narrow claim “this projection violates OMST-PROV-1” survives these explanations. A claim of nontrivial runtime security behavior does not.

### Overall: NEEDS_REVISION

Blocking issues, ordered by severity:

1. **The empirical contrast is definitionally forced** by lines 58–70, 293–311, and P13/P15 at lines 421–425. The non-redundancy gate’s answer is already “yes,” leaving no valid empirical disconfirmation path.
2. **`V_prov` is not a total executable predicate** at lines 364–457: required policy information is absent from event bytes, ordering is ambiguous, and at least the P17 mutation does not exercise its named clause under the declared sort.
3. **The observer remains an underdefined, potentially outcome-defining instrument** at lines 298–311 and 585–638.
4. **The census generator remains non-byte-complete** at lines 501–545 despite substantial improvement.

## Actionable coaching

Reframe this revision as a deterministic proposition:

> Under the pinned schema-projection implementation, identical pre-state, no provenance side channel, and the declared digest-carrying action, schema closure over `provenance_record` is necessary and sufficient for preserving OMST-PROV-1 clauses P13/P15.

Prove that proposition from the compiled-channel sets, then use one minimal source-authentic fixture as a regression test. Remove the 120-graph materiality estimand unless a context variable can alter the outcome without violating treatment fidelity.

Make the oracle total by defining its complete input tuple, for example:

```text
V_prov(condition, input_class, pre_state, capability_set, ordered_event_bytes)
```

Add a per-event-kind field table and explicit transition relation. Either add `source_label`, `operation`, and capability data to the canonical inputs or state exactly how immutable external context supplies them. Replace hash-based semantic ordering with a sequence index or an explicit happens-before relation, and construct a P17 mutant that truly follows `COMPLETE`.

For the observer, preferably compute the expected pre-projection digest offline from the immutable pre-action snapshot. If runtime observation is indispensable, pin the exact hook/callsite and hash its implementation; verify invocation count, before/after checkpoint versions, schedule, emitted-event independence, and absence of state/config/store mutation.

If an empirical contribution is still desired, study a question not forced by the checker—for example, whether naturally authored or independently generated orchestration schemas remain closed over externally specified security obligations across checkpoint, branch, subgraph, or middleware boundaries. Keep the current one-channel result as the minimal deterministic control rather than the headline empirical finding.
