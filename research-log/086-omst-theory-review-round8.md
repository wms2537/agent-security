# OMST theory review — round 8

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

Status: DONE

Hypothesis line count at immutable commit `629aef6`: **652**.

## 1. Blind Assessment

### Previous-review dispositions

1. **P2a/P2b split — IMPROVED.** Static identity and runtime guards are separated, but the fixture does not implement the claimed single post-compilation guard bundle.
2. **Callable delivery and callback/config sources — RESOLVED for the conditional claim.** The LangGraph path is now complete; exact LangChain-core behavior correctly remains an antecedent for a future acquired environment.
3. **START path — RESOLVED.** Whole-dict delivery to START and later `_get_updates` filtering are correctly distinguished.
4. **Environment parameterization — IMPROVED.** `E` and `P(E0)=false` are explicit, but cell indexing is ill-formed and framework-package identity is not reauthenticated in-cell.
5. **Authoritative shell and `-I` — RESOLVED.**
6. **Runtime-guard terminology and abort semantics — RESOLVED.** Guard failure precedes `graph.invoke`, although the stated post-compilation timing remains inaccurate.

### Mathematics and witness

The factorization theorem is correct:

- If `tau=g∘pi`, equality under `pi` implies equality under `tau`, proving necessity.
- Under `ker(pi)⊆ker(tau)`, define `g(q)` using any representative of `q∈image(pi)`; closure gives well-definedness.
- Every `q` has a representative, so any two factors agree there, proving uniqueness.
- For `S=∅`, `Q=∅` and the unique empty function factors the empty `tau`.
- Infinite domains require no finiteness or global representative-choice function; the graph definition is pointwise.
- On a strict larger codomain, extension requires `Y≠∅`; off-image choices are unique only when `Y` is singleton.

The witness is exact. The task projection has one fiber containing two distinct canonical targets, so every deterministic `g_task:X→J(P)` fails on at least one state. The full projection has singleton fibers and uniquely factors through `g_full(x,p)=J(p)`. This is an unconditional constructed record-reconstruction result, not a conclusion from future executions.

### Universal conditional and circularity

Under the intended interpretation—one common authenticated environment plus successful antecedents for every relevant cell—the source lemmas deliver the selected mapping to `capture`; literal equality of the five task fields yields `C_task`, and the sole provenance difference yields `C_full`. P6 does not itself assert either cross-cell conclusion, so the intended implication is not circular.

The written formulation is nevertheless not rigorous. `E` is defined as containing “one cell identifier and its fresh process/directory state” (`084`, lines 209–219), while `C_task(E)` and `C_full(E)` compare two distinct cells each (lines 247–267). Worse, `P(E)` includes `P2b(E,cell)` with `cell` free rather than quantified over the four cells (lines 449–496; config lines 91–105). Under a literal one-cell reading, P2b can hold for `task_s0` while another cell follows a different compiled path, so `P(E)` does not entail the cross-cell conclusions. The proof silently strengthens P2b/P6 to all relevant cells.

This also obscures role-specific failure: if `P(E)` is repaired as a four-cell conjunction, failure of an optional full-control guard makes global `P(E)` false and prevents establishment of `C_task`, contrary to the claimed optional role of `C_full`.

### Source trace

The pinned tag is authentic: LangGraph `1.2.9` resolves to commit `95af6a0…`. The corrected static trace is supported:

- `state.py` compiles with `input_channels=START`, creates the START `PregelNode`, filters via `_get_updates`, derives node channels from the explicit input schema, and uses ordinary state channels.
- `_io.map_input` writes the entire literal dictionary to the single START channel.
- `_loop.py` supplies an empty checkpoint when no saved checkpoint exists, hydrates channels, and calls task preparation.
- `_checkpoint.py` initializes empty values, versions, and seen maps and constructs channel instances.
- `_algo.py` reads selected available channels into a fresh preparation cache and assigns the result to `PregelExecutableTask.input`.
- `_retry.py` invokes `task.proc` with `task.input`.
- `_read.py` constructs the bound-callable/writer sequence, and LangGraph’s `RunnableSeq` gives its unchanged initial input to the first step before writers.

These facts are visible in the pinned [release and commit](https://github.com/langchain-ai/langgraph/releases/tag/1.2.9), [`state.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/graph/state.py), [`_io.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_io.py), [`_loop.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_loop.py), [`_checkpoint.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_checkpoint.py), [`_algo.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_algo.py), [`_retry.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_retry.py), [`_read.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/pregel/_read.py), and [`_runnable.py`](https://github.com/langchain-ai/langgraph/blob/95af6a00718588e7b7ce17310e8006d267896a77/libs/langgraph/langgraph/_internal/_runnable.py).

No exact LangChain-core distribution exists in E0, so its callback/config behavior cannot currently be source-audited. That does not invalidate the universal conditional if P5/P6 are treated as semantic antecedents, but those sources must be bound before applying it to any candidate environment.

### Static subject audit

The committed fixture and launcher hashes match exactly:

- Fixture: `ebb7bd056db292e61c1e6de6e486bce5dfa048ef3f336fef59ff3c0512ac44f6`
- Launcher: `dfe5f8a00d23e4bb4f1c6d5d6adb8896c2255c015ed4e8fd3997afb01e4d356f`

The fixture AST, JSON, and Bash syntax are valid; the launcher mode is `100755`. Four cells, ordered schemas/channels, exact states, empty config fields, one graph/invocation per child, fresh temporary directories, capture-before-write serialization, and the three-field output record are present.

The authoritative outer command uses `env -i` and absolute Bash; children use separate `env -i` environments and Python `-I -B`. E0’s interpreter target and interpreter/stdlib hashes match, its venv disables system-site packages, and no LangGraph or LangChain-core package directories are present.

A direct code/spec mismatch remains: `run_cell` calls `verify_environment_identity()` before `build_checked()` compiles the graph (`fixture.py`, lines 168–172), while the hypothesis and configuration say all environment and compiled guards run atomically after compilation (`084`, lines 299–312 and 462–465; config lines 43–50). All guards still precede observation, but the asserted ordering and atomicity are false.

The larger environment-binding promise is also not operationally closed. P1 authenticates LangGraph, LangChain-core, the dependency lock, and load-bearing source files only as a pre-cell audit. The in-cell verifier checks fixture, launcher, interpreter, and stdlib JSON, but not installed framework versions, origins, distribution hashes, lock identity, or load-bearing source hashes (`fixture.py`, lines 115–130). A package/source change between P1/P6 audit and import is therefore not detected. This is a testability gap: an omnitemporal semantic reading of P(E) can exclude drift, but the closed procedure cannot establish that the executed bundle is the audited bundle.

### Scope, rivals, taxonomy, and parsimony

The purpose-built scope, nonclaims, failure taxonomy, and separation of theorem, witness, conditional source bridge, and future observation are honest. Mapper, stale-channel, checkpoint, START-filtering, callable-order, callback-mutation, import-mutation, shell-contamination, and capture-order rivals are addressed either statically or as explicit antecedents.

`Scope Mismatch × Formal Derivation × formalize` is reasonable. Anti-stacking passes because the witness excludes every total deterministic function on its declared projected domain, while making no empirical or security generalization. The theorem is minimal. The engineering antecedent is necessarily larger, but the current one-environment/four-cell ambiguity and globally coupled optional control add avoidable complexity.

### Severity-ordered defects

1. **Major — ill-scoped environment and free cell variable.** `E` contains one cell, but the conclusions compare four, and `P2b(E,cell)` is not quantified. Locations: `084` lines 209–222, 247–267, 449–496; config lines 91–105.
2. **Major — execution bundle is not reauthenticated against the audited framework/source manifest.** P1/P6 are pre-cell, while runtime guards omit LangGraph, LangChain-core, dependency-lock, and load-bearing source identities. Locations: `084` lines 451–496; fixture lines 115–130 and 168–172.
3. **Medium — claimed post-compilation atomic guard ordering contradicts the fixture.** Environment guards run before compilation; compiled guards run afterward. Locations: `084` lines 299–312 and 462–465; config lines 43–50; fixture lines 168–172.
4. **Medium — optional full control is coupled to the task consequence through one global antecedent.** A full-cell antecedent failure can make `P(E)` false and block task-side establishment. Locations: `084` lines 57–65, 490–540; config lines 101–113.

**Overall verdict: NEEDS_REVISION.**

The unconditional theorem, exact witness, START/source delivery trace, isolation shell, and honest E0 status are sound. The universal engineering proposition remains salvageable, but its cell/environment quantification and runtime identity protocol are not yet sufficiently defined or dischargeable.

## 2. Actionable Coaching

1. Define a common immutable environment manifest `M` and four run objects `R_cell`, rather than placing one cell identifier inside `E`. Define `received(cell,M,R_cell)` explicitly.
2. Replace free `P2b(E,cell)` with quantified, role-specific antecedents, for example:
   - `P_task(M)=P_common(M) ∧ P_cell(M,task_s0) ∧ P_cell(M,task_s1)`
   - `P_full(M)=P_common(M) ∧ P_cell(M,full_s0) ∧ P_cell(M,full_s1)`
   - then state separate implications for `C_task` and `C_full`.
3. Move `verify_environment_identity()` after compilation and combine it with compiled checks in one immediately pre-invoke guard function.
4. Extend that guard to authenticate the config, installed LangGraph/LangChain-core distributions, exact versions/origins, dependency-lock identity, and every load-bearing source hash used by P5/P6.
5. When a candidate environment is acquired, commit its exact LangChain-core manifest and cite the precise callable/config/callback source assertions. Until then, keep P5/P6 explicitly undischargeable and avoid calling the future source bundle “complete.”
6. Preserve the present theorem, witness, scope, nonclaims, capture-before-write rule, clean-shell invocation, and `P(E0)=false` statement unchanged.
