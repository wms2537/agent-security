# OMST theory review — round 2

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

**Status:** DONE  
**File reviewed:** `research-log/060-hypothesis-iter-5-omst-v2.md`  
**Verified line count:** 677

## 1. Blind Assessment

### Previous-review issue disposition

| Prior issue | Verdict | Reason |
|---|---|---|
| 1. Primary estimand and weighting | **RESOLVED** | Lines 175–230 define the matched graph/input/tape unit, require all 1,440 units, use fixed 12-within-graph and 120-across-graph weights, and prohibit treatment-specific denominators. |
| 2. `B`/security overlap | **RESOLVED** | Lines 144–173 separate actual task effects from provenance coordinates and restrict the primary study to one provenance contract rather than pooling logically incompatible families. |
| 3. Causal mechanism/common support | **IMPROVED** | The default-versus-pass comparison removes the major topology and boundary-exposure confounds, but treatment fidelity remains asserted rather than operationally checkable. |
| 4. Independent oracle validation | **IMPROVED** | Independent representations, component fixtures, a 2×2 construct matrix, and mutation gates are substantial improvements. The underlying provenance predicate is still too underspecified to know what those implementations must independently implement. |
| 5. Evidence and taxonomy | **RESOLVED** | ReliabilityBench and ASSURE are compared directly, generic metamorphic-testing novelty is disclaimed, and the proposed classification is defensible. |
| 6. Validation census specification | **IMPROVED** | Version, seed, counts, strata, schemas, tapes, isolation, resource limit, and whole-census invalidation are present. The deterministic generator rule and actual fixture contents remain unfixed. |
| 7. Assumptions and terminology | **RESOLVED** | The requested assumptions have explicit regimes and consequences; “congruence” is replaced by a defined fiber/factorization interpretation. Residual runtime nondeterminism is a new omission, discussed below. |

### Justification Correctness

The finite paired estimand is now coherent. Every abstraction is tied to graph/input/tape executions, the weighting is exact, and a valid subthreshold result is correctly classified as disconfirmation. The eight required bias categories are explicitly covered at lines 450–484.

The causal interpretation nevertheless remains underidentified at the implementation boundary. Lines 87–88 and 252–264 say provenance propagation is the only manipulated coordinate, but the entry does not yet define an executable equivalence test proving that statement. Because `B_actual` deliberately excludes provenance, equality of `B_actual` cannot establish that both treatments begin with the same pre-boundary provenance state or diverge only at the boundary transfer operator.

Measurement is also not sufficiently fixed. Lines 156–168 define `V_prov` using a “required ordered provenance transition,” but never specify the accepted transition language for trusted, sanitized, explicitly authorized, and chained-authorized inputs. It is consequently impossible to determine whether identity and node-only executions should satisfy the same predicate, what authorization chains are valid, or how missing, duplicate, reordered, or conflicting attestations are classified.

### Mathematical Depth and Validity Domains

The notation is substantive rather than decorative:

- `B_actual` maps traces into task-equivalence classes.
- A fiber is concretely the set of traces sharing that task coordinate.
- `V_prov` failing to factor through `B_actual` has the stated operational meaning.
- The nested sums encode the actual weighting rule.

The self-rederivation at lines 586–604 reconstructs the argument without relying on notation. There is no mathiness defect.

The assumptions table is unusually good, but A4 and A5 at lines 437–438 currently substitute assumptions for observable fidelity criteria. A13 refers to a “balanced grammar” whose production rules are absent. A9 assumes the correctness of a security predicate that has not yet been stated precisely enough for independent implementation.

### Logical Soundness

The transition from “same boundary machinery” to “metadata carriage is the minimal surviving mechanism” at lines 258–264 is valid only if all of the following are established:

1. identical pre-boundary provenance records;
2. identical boundary invocation and serialization path;
3. a precisely isolated transfer-function difference;
4. identical downstream execution except for the provenance coordinate; and
5. deterministic or distributionally matched runtime behavior.

The current document asserts these conditions but does not preregister how to verify the first three. The acknowledged treatment-authenticity objection at lines 606–612 is therefore not merely a later implementation detail; it is presently a hole in the causal specification.

The statement at lines 188–194 that all unit-level treatment effects are “directly observed” additionally assumes deterministic replay. A fixed semantic decision tape does not necessarily fix thread scheduling, branch completion order, runtime-generated identifiers, hash iteration, or timing-dependent behavior.

### Assumption Completeness

The requested validity assumptions are present. One further load-bearing assumption is missing:

- Under a fixed tape and declared schedule, executions are deterministic with respect to every coordinate entering `B_actual` and `V_prov`, or residual randomness is identically coupled across treatments.

If this is false, one run per cell cannot distinguish treatment effects from runtime variation. Either a determinism/replay gate or a repeated-run potential-outcome estimand is required.

### Taxonomy Verification

**Scope Mismatch × Empirical Mapping × `decouple`** is defensible. The closest work operates at action/end-state or browser-extension scope, whereas this study isolates an internal orchestration boundary. The contribution empirically maps that causal contrast while decoupling task effects from provenance carriage.

“Evidence Gap” would also be a plausible dominant opportunity label, but the selected label is not an attempt to evade the Bridge×Synthesis tripwire. The study is plainly not synthesis/unification.

### Anti-Stacking Check

The hypothesis passes the anti-stacking test. Its distinguishing prediction is not merely that graph mutations sometimes fail. It predicts a matched rescue when only provenance carriage changes and requires exact negative controls. A generic fuzzer-plus-checker does not entail that pattern.

A conventional controlled ablation could make the same prediction, but that is not a stacking defect: the hypothesis has correctly reduced itself to precisely that minimal ablation.

### Occam’s Razor Check

The primary hypothesis is close to minimal. Removing identity and node-only would simplify execution count but weaken causal diagnosis. The fiber language is optional exposition, not added causal machinery.

The simpler verbal hypothesis is “the default relay loses provenance that explicit copying preserves.” The current formal design is an appropriate operationalization of that single mechanism, provided the remaining specifications are fixed.

### Alternative Explanations

The entry handles generic relay exposure, middleware/checkpoint differences, selection, baseline unsafety, adapter bugs, common-mode oracle errors, leakage, version specificity, and generator targeting.

The unresolved alternatives are:

- the adapter creates the observed metadata difference rather than exercising framework-default behavior;
- treatments enter the boundary with different provenance records;
- the shared abstract predicate is wrong despite independent implementations;
- unspecified grammar choices target favorable graphs;
- residual runtime nondeterminism differs across treatment runs.

### Overall

**NEEDS_REVISION**

The core approach is sound and salvageable. The following defects must be fixed before it can receive a rigorous verdict:

1. **Fully specify `V_prov` and its event semantics** — lines 156–168 and 395–428.  
   Define the canonical event schema and an exact state machine, relational predicate, or truth table for every input schema and every condition. Specify source-label requirements, sanitizer/authorization ordering, chained authorization, boundary carriage, duplicates, missing records, conflicts, and sensitive-effect timing. Every atomic clause needs positive and negative fixtures; add mutants for clauses not represented by the current six.

2. **Operationalize treatment fidelity** — lines 82–88, 106–114, 252–264, 437–438, and 606–612.  
   Identify the exact pinned runtime API/source path implementing “default reconstruction,” the explicit carrier path, and the canonical record representation. Require an auditable equality predicate showing identical pre-boundary provenance state, boundary invocation, topology, scheduling, middleware/checkpoint traversal, and downstream non-provenance behavior. The only permitted divergence should be an explicitly named transfer function.

3. **Finish the deterministic census definition** — lines 338–358 and 444–446.  
   Seed plus coarse strata does not uniquely determine 120 graphs. Fix the generator algorithm/version and graph-ID mapping, node-count and edge grammar, branch topology, state fields, boundary placement, obligation/effect placement, provenance chain, exact input fixture bytes, tape contents/generation, and Latin-order formula. Otherwise implementation choices can silently tune the tested census.

4. **Control residual runtime randomness** — lines 108–114, 188–194, and 356–370.  
   Add a validity assumption and test establishing deterministic replay under each tape and schedule, including branch/concurrency behavior. If exact replay cannot be guaranteed, define repeated executions and a paired distributional estimand rather than treating one run per condition as the directly observed unit effect.

## 2. Actionable Coaching

The cleanest v3 would add three compact, normative appendices:

- a treatment-fidelity table naming every pre-boundary, boundary, and post-boundary field and whether it must be equal or may differ;
- a deterministic graph-and-fixture grammar mapping `(seed, graph_id, input_id, tape_id)` to immutable bytes;
- a provenance automaton with accepted and rejected traces for all four input schemas.

Use the tuning tier to test source authenticity and deterministic replay before generating validation graphs. The authenticity check should fail closed: if default behavior cannot be exercised without adapter-authored reconstruction, rename the treatment as an adapter intervention and narrow the claim.

Expand mutation testing from six convenient faults to clause coverage: every independently evaluated predicate clause should have at least one mutation that would make a formerly rejected trace pass or a valid trace fail.

For conceptual grounding, compare the provenance automaton with classic information-flow control, taint propagation, and authorization-chain semantics. This would strengthen construct validity without expanding the empirical claim into a universal security guarantee.
