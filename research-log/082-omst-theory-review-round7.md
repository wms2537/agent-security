# OMST theory review — round 7

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

Status: DONE

Hypothesis line count at immutable commit `80e0764`: **592**.

## 1. Blind Assessment

### Previous-review dispositions

1. **Close the engineering proof — IMPROVED.** The proposition is now honestly conditional, and P6 owns unresolved source/dependency facts. However, the committed static source bridge still skips load-bearing runnable-delivery steps.
2. **Replace environment/source placeholders — RESOLVED.** Current interpreter, stdlib hashes, and dependency absence are literal; P3–P5 explicitly place tracing, imports, and callbacks in the future antecedent.
3. **Make the fixture closed — IMPROVED.** The four cells, schemas, hashes, graph, capture, and launcher are bound, but the phase gate cannot discharge P2 as written without an additional unbound compile-only execution.
4. **Correct canonicalization wording — RESOLVED.** The domain includes JSON objects and arrays with primitive leaves, including the empty array used by the witness.

### Mathematics

The factorization theorem is correct.

- Necessity: if `tau=g∘pi`, then `pi(s)=pi(s')` implies `tau(s)=g(pi(s))=g(pi(s'))=tau(s')`, so `ker(pi)⊆ker(tau)`.
- Sufficiency: when `tau` is constant on each `pi`-fiber, define `g(q)` as the unique `tau(s)` for any `s` with `pi(s)=q`. Existence of a representative follows from `Q=image(pi)`; fiber constancy gives well-definedness.
- Uniqueness: each `q∈Q` has a representative `s`, so any two factors agree at `q` through `tau(s)`.
- Empty case: `S=Q=∅`; the unique empty map factors the empty `tau`.
- Infinite case: the proof is pointwise and uses no finiteness or choice function.
- Larger domain: on `image(pi)` the factor is unique. Extension to a strict superdomain requires an element of `Y`; off-image values are nonunique unless `Y` is a singleton.
- Finite countermodel search: I independently enumerated all **1,555** pairs of maps for `|S|=0..4`, three projection labels, and two target labels. No countermodel was found.

The typed witness is also correct. `X` is a singleton, `J(p0)≠J(p1)`, and both states lie in the single `pi_task` fiber. Any total deterministic `g_task:X→J(P)` has one output and therefore misses at least one of the two targets. `pi_full` has singleton fibers, and `g_full(x,p)=J(p)` is its unique factor. This proves the universal function quantifier; it is not an inference from four future executions.

### Conditional Logic

P1–P7 do not literally assert `C_task` or `C_full`. P6 assumes independently auditable per-cell source lemmas, not the cross-cell equality/difference conclusions, so the implication is not circular in its intended reading.

Assuming a fixed candidate environment and all source lemmas:

1. Task schemas select the same five fields.
2. Fresh input application populates those fields.
3. Task preparation builds the selected mapping.
4. Runnable delivery passes that mapping to `capture`.
5. The five values are equal between `S0` and `S1`; deterministic canonicalization gives `C_task`.
6. The full mappings add provenance records differing only at `agent_id`; canonicalization gives `C_full`.

Thus the mathematical derivation of `P -> C_task/C_full` is valid under the intended fixed-environment reading. P1 is explicitly false/undischarged in the present environment, and the document makes no unconditional LangGraph inference.

There is, however, a testability defect in the gate. P2 says the compiled assertions “pass,” while the phase gate requires P1–P6 to pass before the four cells run. In the fixture, those assertions occur inside `build()` immediately before `graph.invoke()` ([fixture lines 102–136](/home/soh/agent-security/experiments/omst_c2_v7_fixture.py:102)). The committed artifacts provide no compile-only command by which P2 can be discharged before cell execution. Static inspection can establish that the assertions exist, but not that they pass in the acquired environment.

### Source Correspondence

The pinned tag identity is correct: tag `1.2.9` resolves to `95af6a00718588e7b7ce17310e8006d267896a77`.

The substantive source facts check out:

- `state.py` creates ordinary fields as `LastValue`, derives node channels from the explicit input schema, returns no mapper for a `TypedDict`, and retains the supplied `None` services. [Pinned `state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py)
- `_loop.py` substitutes `empty_checkpoint()`, hydrates fresh channels, applies graph input, and later calls `prepare_next_tasks`. [Pinned `_loop.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py)
- `_checkpoint.py` initializes empty values/versions/seen maps and creates channel instances using `from_checkpoint`. [Pinned `_checkpoint.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_checkpoint.py)
- `_algo.py` creates a fresh `input_cache`, reads all available selected channels, applies a mapper only when present, and puts the result into `PregelExecutableTask.input`. [Pinned `_algo.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_algo.py)
- `_retry.py` calls `task.proc.invoke(task.input, config)`. [Pinned `_retry.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_retry.py)

Two defects remain in the committed justification:

1. At hypothesis lines 326–330, `_io.map_input` is described as mapping each matching state key. For this compiled graph, `input_channels=START`, so it emits `(START, whole_input_dict)`. Per-field filtering occurs later in the START `PregelNode` writer via `_get_updates` in `state.py`. The final availability conclusion is correct, but the stated intermediate source step is false.

2. At lines 348–352, `task.proc.invoke(...)` is treated as sufficient to prove that `capture` receives the mapping. The missing links are load-bearing: `PregelNode.node` constructs a sequence of the bound callable and writers, and `RunnableSeq` invokes its first step with the unchanged task input. Those facts live in uncited `_read.py` and `_internal/_runnable.py`. The latter also exposes the pre-capture callback-manager path that P5 is intended to control. [Pinned `_read.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_read.py), [pinned `_internal/_runnable.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/_internal/_runnable.py)

I independently verified those omitted links, so they support the intended result; the problem is that the claimed closed “static source bridge” does not itself cite or bind them.

### Fixture Closure

Static inspection found:

- Four exact cells and the expected task/full schemas.
- `S0` and `S1` equal on all task fields and different only at `provenance_record.agent_id`.
- Capture serializes its sole argument before returning its only write.
- Exact assertions for channels, mapper, policies, checkpointer, cache, and store.
- One graph invocation and one temporary directory per Python process.
- Canonical output containing only `cell`, `observed_hex`, and `status`.
- Fixture SHA-256 `e26bca99...e5d09` and launcher SHA-256 `ff9be2b7...df68c`, both matching the specification.
- Valid Python AST, valid JSON, valid Bash syntax, and executable launcher mode.

No LangGraph or LangChain-core package was found in the isolated venv, whose `pyvenv.cfg` also disables system-site packages. I did not import or execute LangGraph or the fixture.

Launcher isolation has two formulation defects:

- The Python children run under `env -i`, but the launcher shell itself starts through `#!/usr/bin/env bash` in the inherited environment. Thus statements that the “launcher executes under `env -i`” are stronger than the file guarantees; inherited `PATH` and `BASH_ENV` can affect shell startup or add launcher output before the clean child commands.
- Python `-I` implies `-E`, so `PYTHONHASHSEED=0` and `PYTHONNOUSERSITE=1` are ignored. User-site isolation still follows from `-I`, and hash seed is irrelevant to sorted canonical JSON here, but line 531’s characterization of hash seed as effective reproducibility hygiene is inaccurate.

### Logical Soundness and Assumptions

The roles are otherwise separated correctly:

- Part I is unconditional set theory.
- Part II is an exact artificial witness.
- Part IV is a source-correspondence argument.
- P1–P7 are an acquisition/environment antecedent.
- Future execution checks the conditional application only.
- No runtime outcome is promoted into a security, prevalence, causal, or novelty claim.

Failures are mostly scoped correctly. A theorem countermodel affects Part I; target collapse affects the witness; an undischarged P item leaves only correspondence unestablished; `C_full` failure affects the optional positive control.

The environment should nevertheless be explicitly parameterized. As written, current interpreter and stdlib hashes are documentary facts outside P, while P refers to a future acquired environment. Define `P(E)` and `C(E)`, and require execution-time equality to the recorded interpreter, resolved target, stdlib JSON, fixture, launcher, and package manifests. Otherwise “the current values” and “the future acquired environment” can drift without a formal bridge.

### Taxonomy, Anti-Stacking, Occam, and Alternatives

The classification is accurate: this is classical quotient factorization plus a conditional engineering-control protocol, not new mathematics or a standalone top-tier contribution.

Anti-stacking passes. The nonconstant-fiber argument quantifies over every total deterministic function on the declared input; future actions are only correspondence checks.

Occam passes for the abstract theorem but only partially for P. Observer-only exclusions in P4–P5 are stronger than needed for claims solely about callable-entry bytes; mutation exclusions are load-bearing, observation exclusions are not. The ignored hash-seed variable is also unnecessary.

The strongest rival explanation defeated is that a hidden framework path could deliver provenance despite the task schema: under the fully audited `L_compile/L_fresh/L_prepare/L_deliver` chain, the task mapping is exactly the five selected channels. The remaining objection is not a counterexample to that source behavior; it is that the committed proof and execution gate do not yet bind all steps needed to establish it in the future environment.

### Severity-ordered issues

1. **Major — P2/phase-gate testability conflict.** Hypothesis lines 383–386 and config phase gate line 107 require compiled assertions to pass before the only committed commands that can execute them. Split static artifact identity from runtime compiled guards or provide a closed compile-only probe.
2. **Major — incomplete callable-delivery source bridge.** Hypothesis lines 348–352 and config source lemma `L_deliver` omit `_read.py`, `_internal/_runnable.py`, and the relevant LangChain-core callback-manager sources.
3. **Medium — incorrect START input description.** Hypothesis lines 326–330 and config `L_fresh` attribute per-key filtering to `_io.map_input`; the whole dict is written to START and filtered by the START writer.
4. **Medium — future environment is not explicitly bound to current interpreter/stdlib identity.** Parameterize the proposition by environment and reauthenticate the recorded hashes at execution time.
5. **Low — launcher isolation/flag wording.** The launcher shell is not itself under `env -i`; `-I` ignores both supplied `PYTHON*` variables.
6. **Low — “static assertions” terminology.** These are runtime assertions about a compiled graph, not static assertions.

**Overall verdict: NEEDS_REVISION.**

The mathematical core and intended conditional consequence are sound and salvageable. Revision is required because the execution gate is not currently dischargeable as specified and the claimed closed source bridge omits and misstates load-bearing intermediate steps.

## 2. Actionable Coaching

1. Split P2 into:

   - `P2a`: fixture/launcher/config hashes and syntax match statically.
   - `P2b`: compiled graph assertions pass as atomic preconditions inside each future cell.

   Either remove P2b from the pre-cell phase gate or add a committed, isolated compile-only command.

2. Replace the L_fresh trace with the exact sequence:

   `literal dict -> START EphemeralValue -> START task input -> _get_updates field writes plus branch trigger -> apply_writes -> selected LastValue availability -> capture task`.

3. Add `_read.py` and `_internal/_runnable.py` to the authenticated source basis and trace:

   `PregelExecutableTask.proc -> PregelNode.node -> RunnableSeq(bound, writers) -> bound.invoke(task.input) -> RunnableCallable -> capture(input)`.

   Bind the exact LangChain-core callback-manager files needed for P5.

4. State the theorem as `∀E, P(E) -> C_task(E) ∧ C_full(E)`. Include execution-time checks for the interpreter symlink target, interpreter hash, stdlib JSON hash, artifact hashes, and package/source manifests.

5. Specify an authoritative clean-shell invocation, using an absolute Bash path under an outer `env -i`, or explicitly narrow the isolation claim to the Python children. Account for `BASH_ENV` and launcher-level stdout.

6. Keep `-I` and remove the ineffective `PYTHONHASHSEED` and `PYTHONNOUSERSITE` assignments, or change the Python flags if a fixed hash seed is genuinely required. Do not claim a fixed hash seed while using `-I`.

7. Rename the configuration’s `static_assertions` field to `compiled_runtime_guards` and state that a failed guard aborts the cell before capture.
