# OMST theory review — round 6

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

Status: DONE

Committed hypothesis line count at `35b24a1`: **675**

No files were edited. LangGraph was neither installed, imported, nor executed.

# 1. Blind Assessment

## Overall verdict: NEEDS_REVISION

The abstract theorem and typed witness are rigorous. The independent engineering correspondence proposition is plausible and likely repairable, but v6 does not yet prove it as a closed proposition. Several decisive source/run-state facts are stated as admissible postconditions or future snapshot requirements rather than derived from the pinned source and literal fixture.

I found no mathematical counterexample. I checked 1,555 finite models with \(|S|=0\ldots4\), three projection labels, two target labels, and all functions on the reachable image; none violated the theorem.

## Previous-review dispositions

| Round-5 issue | Disposition | Reason |
|---|---|---|
| 1. Executable and closed LangGraph proposition | **IMPROVED** | Literal schemas, state, node, edges, compile/invoke shape, roles, and capture are now present. It is not fully closed: `schema` and `state` remain externally supplied, the process harness and internal snapshot mechanism are absent, and key run-state facts are still postconditions. |
| 2. Deterministic correspondence from source/run state | **IMPROVED** | The source chain is substantially better and correctly identifies `_proc_input`. Fresh `input_cache` is statically supported. Fresh checkpoint/channel construction, input application, selected-channel availability, callback isolation, and final task-to-callable delivery are asserted or deferred rather than fully proved in the artifact. |
| 3. Remove T1 and correct T3 | **RESOLVED** | Finiteness and nonemptiness are gone; `Q=image(pi)` is correctly used for canonical uniqueness, and the larger-codomain extension is separated. |
| 4. Fully type the witness | **RESOLVED** | `J:P→B`, `Y=J(P)`, `tau`, `pi_task`, `pi_full`, and `g_full` are consistently typed. |
| 5. Separate logical roles | **RESOLVED** | `C_task` is independent and load-bearing; `C_full` is optional. Cross-schema failure has its own role. |
| 6. Keep scope honest | **RESOLVED** | Claims remain restricted to record reconstruction/schema sufficiency relative to `tau`; no general security, causal-effect, prevalence, or vulnerability claim reappears. |

## Justification Correctness

**Necessity.** If `tau=g∘pi`, then `pi(s)=pi(s')` implies
`g(pi(s))=g(pi(s'))`, hence `tau(s)=tau(s')`. Therefore
`ker(pi)⊆ker(tau)`.

**Sufficiency.** Under closure, define `g(q)` as the common `tau`-value of the
fiber over `q`. Since `Q=image(pi)`, every `q` has a representative. Closure
makes the value independent of representative, so `g` is total and
`g(pi(s))=tau(s)`. No enumeration or global choice is required.

**Uniqueness.** For each `q∈Q=image(pi)`, choose a representative `s`.
Any two factors satisfy
`g1(q)=g1(pi(s))=tau(s)=g2(pi(s))=g2(q)`.

**Boundary cases.**

- If `S=∅`, then `Q=∅`; the unique empty function factors the unique empty `tau`, and closure is vacuous.
- The proof is pointwise and remains valid for infinite `S`.
- Totality is correctly load-bearing. Partial or multivalued behavior requires a different formulation.
- For a strict larger codomain `Q0`, the image factor remains unique. An extension exists if `Y` is nonempty, but off-image values are generally nonunique. The qualifier “generally” correctly permits the singleton-`Y` exception.

**Typed witness.** The canonical record bytes recompute exactly and differ only at `agent_id`. The task coordinates in `s0,s1` are identical. Thus the task projection contains one fiber with two distinct `tau` values, excluding every total deterministic `g_task:X→Y`, not merely the selected capture action. `pi_full` is bijective onto `X×P`, and the declared `g_full` is its unique factor.

The mathematical portion is rigorous.

## Engineering Correspondence

### What the pinned source supports

The tag and commit are authentic: [LangGraph 1.2.9 release](https://github.com/langchain-ai/langgraph/releases/tag/1.2.9) and [commit `95af6a0`](https://github.com/langchain-ai/langgraph/commit/95af6a00718588e7b7ce17310e8006d267896a77).

Static source inspection supports several important steps:

- [`state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py) registers explicit input schemas, derives their channel lists, uses `LastValue` for ordinary fields, and gives `TypedDict` inputs a `None` mapper. Its compile defaults pass through absent checkpointer, cache, and store values.
- [`_algo.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_algo.py) creates a fresh empty `input_cache` inside each `prepare_next_tasks` call. `_proc_input` reads available selected channels, applies the mapper only when non-`None`, and the resulting `val` becomes `PregelExecutableTask.input`.
- [`_retry.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_retry.py) shows the execution step invoking `task.proc` with `task.input`.
- The literal Python block parses without importing LangGraph, and its JSON values match the normative specification.

These facts make both `C_task` and `C_full` credible.

### Why the proposition is not closed yet

1. **The cited proof path is incomplete.** Lines 393–398 name only `state.py`, `_read.py`, and `_algo.py`. Those files do not alone prove fresh checkpoint construction, channel hydration, graph-input application, field availability before the PULL task, or the final execution call.

   Those steps require at least [`_loop.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py), [`_checkpoint.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_checkpoint.py), [`_io.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_io.py), and `_retry.py`. The source appears capable of supplying the missing proof, but the artifact does not give it.

2. **Decisive facts are deferred.** At lines 425–446, channels, mapper, retained services, checkpoint versions, availability, and empty-cache state are called “expected” or “admissible” postconditions that “must be captured and checked.” Lines 450–454 then assume the “admissible path.” A5–A8 at lines 525–528 restate these decisive steps as premises. Consequently D7 proves:

   ```text
   if D1-D6's postconditions hold, then C_task and C_full follow
   ```

   It does not yet prove that the literal fixture necessarily satisfies those postconditions.

3. **Input availability is not derived.** `_proc_input` silently omits unavailable list channels. Therefore exact availability is load-bearing. The artifact does not trace the literal input through `map_input`, START-node writes, `apply_writes`, channel versions, and channel hydration to prove that all five or six selected channels are available before capture.

4. **Hidden callback/instrumentation context remains conditional.** Lines 467–471 say unexpected callbacks, tracing, wrappers, or globals cause rejection. Rejection semantics do not establish their absence. `config=None` is not itself a proof that no ambient callback/tracing configuration is created. A graph-level callback sees the full initial input and arbitrary callback code could mutate global or mutable state before capture. This need not occur in ordinary LangGraph, but the complete-observable-input proposition must exclude it by an exact isolated launch/configuration or a static proof.

5. **The environment is not literally pinned.** The normative JSON contains:

   ```text
   "python": "exact version/hash from environment manifest"
   "stdlib_json": "exact file hash recorded"
   ```

   These are instructions, not actual versions/hashes. The available environment note records CPython 3.14.3 but no interpreter hash or stdlib JSON hash. Relevant LangGraph/dependency file hashes are likewise obligations rather than supplied values. Thus the claim at lines 467–468 that hashes are recorded is presently false.

6. **The “literal executable” is still a program shape.** Lines 357–373 leave `schema` and `state` unbound, while lines 385–387 prescribe fresh-process behavior outside the program. There is no exact launcher or static instrumentation showing the required pre-PULL snapshots. This is testability incompleteness, not evidence that the expected relation is false.

Accordingly, neither `C_task` nor `C_full` is falsified, but neither is established as the claimed closed source/run-state proposition. `C_task` cannot yet carry the LangGraph application. `C_full` remains correctly optional.

## Logical Soundness

The abstract theorem, witness, source correspondence, future runtime check, and application scope are explicitly separated. The theorem contains no framework premise and is not circular.

The engineering derivation is conditionally sound but overstated. A7 assumes that normal PULL preparation satisfies D5, including the key connection from channels to callable input; A6 and A8 assume the isolation and hidden-context properties needed for equality. Using those premises to derive `C_task` is valid, but calling the resulting proposition source-closed before deriving the premises is not.

The document correctly states that one replicate cannot prove determinism and that a correspondence failure rejects only the framework application. No causal or security conclusion is smuggled in.

## Assumption Completeness

A1, A4, and the image-domain definition are sufficient for the theorem and witness. A3 is properly an application/modeling premise rather than a theorem premise.

Missing or incompletely discharged engineering premises include:

- the complete pinned dependency/source path governing loop initialization and callable execution;
- exact top-level handling of `checkpointer=None`;
- fresh empty checkpoint and channel instantiation;
- graph-input-to-channel writes and selected-channel availability;
- exact runner delivery of `PregelExecutableTask.input`;
- absence of ambient callbacks, tracing, import hooks, `sitecustomize`, or mutable global preparation;
- actual Python, stdlib JSON, dependency, and source hashes; and
- an exact isolated process command.

Violation of channel/mapper/availability/task-delivery premises invalidates both correspondence propositions. A hidden context that distinguishes task cells invalidates `C_task`. Failure of provenance delivery invalidates `C_full` only. None affects the abstract theorem.

`PYTHONHASHSEED`, locale, timezone, temporary-directory freshness, and network isolation are not load-bearing for canonical equality over these primitive values once the actual callable argument and serializer are fixed. They may remain reproducibility controls, but the claim that Occam’s boundary is “exact” is too strong.

## Taxonomy Verification

`Scope Mismatch × Formal Derivation × formalize`, with `decouple` secondary, is acceptable. The work applies a classical factorization criterion and separately proves an implementation correspondence; it does not synthesize multiple techniques into a new method.

The heightened `Bridge × Synthesis` tripwire is not triggered under the current contribution claim. It would be triggered if the theorem-plus-source protocol were promoted as a novel integrated method. The explicit classical-novelty disclaimer prevents that inflation.

## Anti-Stacking Check

The abstract anti-stacking claim passes. A nonconstant fiber proves impossibility for every total deterministic function on the declared task input, not just the selected capture action.

The quantifier remains restricted to `X`, `Y`, and the researcher-selected `tau`. It does not cover actions with hidden inputs or establish a general provenance/security obligation. The artifact states that limitation honestly.

The corresponding LangGraph claim remains contingent on completing `C_task`.

## Occam’s Razor Check

The theorem and two-state witness are minimal. `Q=image(pi)` removes off-image degrees of freedom, and two states are the smallest counterexample to fiber constancy. `C_full` is correctly optional.

The engineering layer retains some unnecessary controls and duplicates source-derivable checks. In particular, source already constructs a fresh empty `input_cache` inside `prepare_next_tasks`; runtime identity capture is useful as a diagnostic but not a proof premise. Locale, timezone, and hash seed should be labeled reproducibility controls rather than logical necessities.

## Alternative Explanations

- **Aliases:** defeated within the artificial product witness.
- **Randomness/history/partiality:** correctly outside the abstract total-function claim unless included in modeled input.
- **Mapper behavior:** static source supports `mapper=None` for these `TypedDict` schemas.
- **Input-cache reuse:** source supports a fresh per-`prepare_next_tasks` cache.
- **Checkpoint/channel reuse:** protocol intent is clear, but the artifact does not prove the loop/checkpoint path.
- **Unavailable channels:** remains deferred and is load-bearing.
- **Capture mutation:** the literal callable serializes before its first write and does not mutate its argument.
- **Callbacks/instrumentation:** not fully excluded by `config=None` and prose rejection conditions.
- **Source mismatch:** tag/commit identity is authentic, but exact relevant file/dependency hashes are not recorded.
- **Canonicalization:** record bytes recompute correctly. A minor normative inconsistency remains: the canonicalization description says only integers/strings/booleans/null are used, while the fixture also contains objects and an empty array. It should say that all leaves are primitive JSON values.
- **Researcher-chosen obligation and classical prior:** both are explicitly conceded and appropriately limit novelty and scope.

## Severity-ordered required revisions

1. **Close the engineering proof** at hypothesis lines 393–497 and A5–A8, deriving rather than assuming checkpoint/channel freshness, input application, channel availability, task construction, and callable delivery.
2. **Replace environment/source placeholders with literal values** for the normative JSON environment and lines 467–470; explicitly control callbacks/tracing/import context.
3. **Make the fixture genuinely closed** by binding `state` and `schema`, specifying the isolated launch configuration, and defining the required static/runtime capture mechanism.
4. **Correct the minor canonicalization description** to include JSON containers with primitive leaves.

# 2. Actionable Coaching

1. Split the correspondence into explicit lemmas:

   ```text
   L_compile(schema):
     exact proc.channels, mapper=None, no node cache/retry

   L_fresh(state):
     empty checkpoint -> fresh channels -> input writes -> all selected channels available

   L_prepare:
     fresh input_cache -> _proc_input -> task.input

   L_deliver:
     run_with_retry invokes task.proc with task.input;
     capture receives that mapping before any write
   ```

   Derive `C_task` and `C_full` only after proving all four.

2. Expand the pinned source set to include `state.py`, `_loop.py`, `_checkpoint.py`, `_io.py`, `_algo.py`, `_retry.py`, and any LangChain-core runnable code needed to prove callback/config injection behavior. Record exact blob hashes or bind each file directly to the authenticated commit.

3. Trace one fresh invocation symbolically:

   ```text
   literal state
   -> START input
   -> GraphState channel writes
   -> fresh LastValue instances
   -> branch trigger
   -> selected channels available
   -> _proc_input mapping
   -> PregelExecutableTask.input
   -> task.proc.invoke(task.input, config)
   -> capture(state)
   ```

   This supplies the missing deterministic bridge without relying on a replicate.

4. Replace “admissible postcondition” wording with either:

   - a proved consequence of the literal source and fixture; or
   - an explicit conditional proposition named `C_task_if_P`.

   Do not call the unconditional framework proposition established while its load-bearing premises remain future gates.

5. Pin the process environment literally: exact interpreter executable/hash, stdlib JSON hash, LangGraph and LangChain-core hashes, isolated invocation flags, cleared tracing variables, and `callbacks=[]` or equivalent. State how `sitecustomize`, import hooks, and ambient runnable context are excluded.

6. Provide a complete static fixture module or deterministic generator that binds all four cells. Instrumentation should observe `PregelExecutableTask.input` without modifying it and should assert absence of callbacks/services before the node runs.

7. Keep runtime execution in its proper role: a single execution per cell may falsify the static derivation or detect a source/environment mismatch, but it cannot establish determinism.

8. Simplify the proof surface. Retain locale/timezone/hash-seed controls only as reproducibility hygiene; remove them from the logical dependency chain. Keep `C_full` and the cross-schema diagnostic explicitly optional.

9. Frame the foundational result as the standard factorization of a function through the quotient by `ker(pi)`. Appropriate context includes quotient-set universal properties, Goguen–Meseguer noninterference, and Sabelfeld–Myers information-flow foundations. The contribution should remain the exact framework correspondence/control construction, not mathematical novelty.

A repaired version could plausibly receive **RIGOROUS**: the core mathematics is correct, the literal values align, and the pinned source appears to contain the missing engineering steps.
