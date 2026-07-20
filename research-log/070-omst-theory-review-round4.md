# OMST theory review — round 4

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

**Status: DONE**

Reviewed file: `research-log/068-hypothesis-iter-5-omst-v4-schema-closure.md`  
Verified line count: **703**

# 1. Blind Assessment

## Overall: NEEDS_REVISION

The intended biconditional is mathematically true after correcting a notation/type error, but it is true by direct expansion of a co-designed action and verifier. Several claims about load-bearing assumptions are false, the anti-stacking comparison uses the wrong baseline, and the stated Occam reduction is not minimal. The result can serve as a narrow regression specification, but it is not yet a rigorous scientific contribution in its present framing.

## Previous-review issue disposition

| Previous issue | Disposition | Assessment |
|---|---|---|
| 1. Empirical contrast definitionally forced | **RESOLVED** | The frequency/effect-size/census claim is explicitly retired at lines 23–26 and 474–476. The remaining fixture is described as a correspondence check, not an empirical estimate. Its expected verdicts are still forced, but the artifact no longer misrepresents them as empirical evidence. |
| 2. `V_prov` not total/executable | **RESOLVED for the active theoretical specification** | P04/P16/P17 and their missing inputs are removed from scope; `R_13_15` now has exact inputs, trace grammar, field constraints, ordering, and a three-valued result at lines 214–279. This establishes a total mathematical relation. No executable implementation exists yet, so executable totality remains a later engineering obligation. |
| 3. Observer outcome-defining | **RESOLVED** | Expected digest construction now uses immutable pre-state bytes offline, lines 256–275 and 404–408. The condition label is decision-inert. |
| 4. Census generator non-byte-complete | **RESOLVED BY REMOVAL** | The generator and census are gone. The future fixture is literal and deterministic. Its correspondence instrumentation is incomplete in a different way, discussed below. |

## Justification Correctness

Let \(u=\texttt{provenance_record}\), \(\delta=H(J(p))\), and \(I_C=1\) iff \(u\in C\).

From exact projection,

\[
u\in\operatorname{dom}(\Pi_C(s)) \iff u\in C.
\]

The declared action therefore produces

\[
D_C =
\begin{cases}
\delta,&u\in C,\\
\texttt{null},&u\notin C.
\end{cases}
\]

Both events carry \(D_C\). On a valid trace, the verifier returns `PRESERVE` iff both event digests equal \(\delta\), hence

\[
R_{13,15}=\texttt{PRESERVE}
\iff (D_C=\delta)\land(D_C=\delta)
\iff D_C=\delta.
\]

Because \(\delta\) is a hexadecimal string and therefore not JSON null,

\[
D_C=\delta\iff u\in C\iff \operatorname{closed}(C).
\]

Thus the intended theorem is correct. Collision resistance is unnecessary.

However, the written formal expression is ill-typed. Lines 101–102 define \(f\) as the action and \(E(q)\) as the trace emitted when \(f\) receives \(q\). Lines 71 and 302–304 instead write \(E(f(\Pi_C(s)))\). Either:

- \(f(q)\) already is the trace, in which case \(E\) should disappear; or
- \(E_f(q)\) denotes execution of \(f\) on \(q\), in which case it should receive \(q\), not \(f(q)\).

The proof silently uses the latter intended semantics. This is repairable but unacceptable in the formal statement.

## Mathematical Depth and Validity Domains

The structural content is a one-bit membership identity. SHA-256, two events, two clause names, an automaton, and condition labels do not contribute mathematical depth. Both obligations inspect copies of the same scalar produced by the same branch, so P13 and P15 are logically duplicate coordinates under A4.

The stated boundary analysis also contains an error. Lines 398–402 claim that a null record makes the expected digest undefined or may cease to distinguish presence from absence. But `null` is explicitly in the domain of \(J\) at lines 119–133. If the key is present with value null, the action computes \(H(J(\texttt{null}))\), a non-null 64-character string; if the key is absent, it emits JSON null. The proof therefore works unchanged for a null record. Non-nullness of \(p\) is unnecessary.

The domain condition \(C\subseteq\operatorname{dom}(s)\), stated only in prose at lines 160–163, should be part of the proposition’s quantified domain or assumptions. Otherwise \(\Pi_C(s)\) is partial while the proposition at lines 299–305 appears universally quantified over \(s,C\).

## Logical Soundness

The central new defect is the claimed independence of A3 and A4.

A4 already says the action obeys the exact rule “if the key is absent, emit null” at lines 169–193 and 283–291. The side-channel countermodel at lines 385–390 instead makes the action emit \(d(p)\) when the key is absent. That countermodel violates A4 as well as A3. It therefore does not establish that A3 is load-bearing while A4 remains true.

Consequences:

- Line 349 incorrectly says A3 is needed for Lemma 2. A4 alone supplies both directions.
- The “remove A3” countermodel does not satisfy the other listed assumptions.
- A3 is at most an implementation-level condition used to justify A4, not an independent premise of the abstract theorem.
- A1 is likewise irrelevant to the abstract proof once \(q=\Pi_C(s)\) is defined; it belongs only in a framework-correspondence corollary.
- A6 is redundant for traces constructed by the exact event-emitting A4 and serialized as \(J(t)\).

The proof itself survives, but the assumption analysis and countermodel discipline do not.

## Assumption Completeness

For the abstract theorem, the assumptions are overcomplete rather than minimal. For framework applicability, they are incomplete operationally:

- LangGraph’s PULL path must have every selected channel available. `_proc_input` omits unavailable channels; membership in `proc.channels` alone does not imply membership in the action input.
- The mapper must be proven identity-like for the exact TypedDict schemas.
- The fixture must establish the action’s received mapping, not merely its compiled channel list.
- A source hash does not by itself establish identical bound globals, defaults, closures, configuration, or runtime context.

The future fixture table at lines 462–473 does not include the “received node-input bytes” audit promised at lines 442–444, nor an explicit sealed-environment check for A3.

Official source inspection does support the candidate correspondence: `add_node` resolves the input schema and `CompiledStateGraph.attach_node` builds `PregelNode.channels` from that schema. But normal node input is then constructed by `prepare_single_task` through `_proc_input`; `ChannelRead.do_read`, cited at lines 438–439, is not the decisive normal PULL-input path. The source chain should name and audit `_proc_input` explicitly. The pinned tag and object are authentic: [LangGraph 1.2.9 release](https://github.com/langchain-ai/langgraph/releases/tag/1.2.9), [commit `95af6a0`](https://github.com/langchain-ai/langgraph/commit/95af6a00718588e7b7ce17310e8006d267896a77).

## Taxonomy Verification

`Scope Mismatch × Formal Derivation`, with dominant operation `formalize`, is accurate. This is not primarily Bridge Opportunity × Synthesis/Unification: there is no substantive integration of distinct methods. The framework projection, action rule, and verifier are one manually specified semantic chain.

The taxonomy passes, but this does not establish novelty.

## Anti-Stacking Check

**Fails the required comparator.**

Lines 601–605 compare the proposal with a terminal-task checker alone. That is a weaker component set, not a plain combination of the same components.

A plain combination of:

1. exact schema projection,
2. the declared “hash-if-present, null-if-absent” action, and
3. the digest-equality verifier

already predicts exactly `full=PRESERVE` and `task=VIOLATE`. The formalization adds no testable prediction that this direct composition does not make. The artifact may still be useful as an explicit regression contract, but its current anti-stacking argument does not support a scientific contribution.

## Occam’s Razor Check

The claimed simplest hypothesis at lines 607–616 is not minimal. The same result follows from one key, one sentinel, one output, and one equality:

\[
u\in C \iff D_C=\delta.
\]

The second event, second identical digest, automaton, condition label, and SHA-256 are unnecessary to the theorem. Two clauses are justified only if they exercise genuinely distinct production paths or can fail independently. Under the declared action they cannot.

## Alternative Explanations

The simpler explanation for the future expected pair is circular construction: the action converts key membership into `digest/null`, and the verifier converts `digest/null` into `PRESERVE/VIOLATE`. This is not label leakage, but it is outcome construction.

Other live alternatives are:

- source/model mismatch in channel availability or mapper behavior;
- fixture instrumentation or action construction, rather than framework projection;
- unverified bound environment despite equal callable source hashes;
- checking compiled channels without checking the actual mapping delivered to the callable.

Condition-label leakage and runtime-observer manufacture are now adequately controlled.

## Severity-ordered revision requirements

1. **Separate or eliminate A3 and A4**; the A3 countermodel at lines 385–390 currently violates A4 and is logically invalid.
2. **Concede that the current theorem is definitional** or supply a prediction unavailable from the plain composition of the same components; lines 593–605 do not pass anti-stacking scrutiny.
3. **Use the genuinely minimal theorem or justify duplicated P13/P15 paths**; lines 178–193, 267–270, and 351–360 currently duplicate one equality.
4. **Repair the type of \(E\) and \(f\)** at lines 71, 101–102, and 302–304.
5. **Correct the null-record boundary claim** at lines 398–402; null is hashable under the declared \(J\).
6. **Make the correspondence path and fixture complete**: audit `_proc_input`, channel availability, mapper behavior, actual received mapping, and the bound environment.
7. **State \(C\subseteq\operatorname{dom}(s)\) formally** rather than leaving the projection’s domain restriction outside A1–A7.

# 2. Actionable Coaching

A stronger formulation would replace the co-designed null branch with an information-flow impossibility result.

Define observational equivalence:

\[
s\sim_C s' \iff \Pi_C(s)=\Pi_C(s').
\]

Any deterministic action that receives only \(\Pi_C(s)\) is constant on each equivalence class of \(\sim_C\). If `provenance_record` is omitted, choose two states equal on \(C\) but with records \(p_0,p_1\) whose concrete digests differ. The action must produce the same output for both states, while the obligation requires two different digests. Therefore no projected-input-only action can satisfy the provenance-dependent obligation for all records when the key is omitted. This establishes necessity structurally, without hard-coding “absent implies null.” Sufficiency can then be a separate constructive lemma for the declared correct action.

This formulation connects directly to noninterference and dependency theory; relevant foundations include Goguen and Meseguer’s *Security Policies and Security Models* and Sabelfeld and Myers’ survey *Language-Based Information-Flow Security*.

Recommended repairs:

- Define either \(T=f(q)\) or \(T=E_f(q)\), not \(E(f(q))\).
- Minimize the abstract assumptions to projection, action transfer, verifier semantics, and serialization domain. Move LangGraph facts into a separate correspondence proposition.
- Permit a null record; require only that \(J(p)\) is defined and that the sentinel used for absence is outside the digest range.
- Provide executable verifier pseudocode or a reference implementation with explicit duplicate-key rejection, exact Python type checks for `seq`, UTF-8 failure handling, and no coercive parsing.
- Replace the `ChannelRead.do_read` correspondence step with the actual `attach_node → PregelNode.channels → prepare_single_task → _proc_input → mapper → callable` path.
- Record the actual canonical input mapping received at callable entry using read-only instrumentation that cannot provide events or expected digests to the verifier.
- If P13 and P15 remain, route them through distinct production paths or state explicitly that the second is a duplicate regression assertion rather than additional theorem structure.
- Treat ReliabilityBench and ASSURE only as evaluation motivation. Their published claims concern metamorphic/reliability testing, not this necessity theorem or its novelty ([ReliabilityBench](https://arxiv.org/abs/2601.06112), [ASSURE](https://arxiv.org/abs/2507.05307)).
- If no prediction beyond direct composition is intended, label the output an engineering regression contract and abandon the top-tier novelty claim.
