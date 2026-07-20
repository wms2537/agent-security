# OMST theory review — round 5

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

**Status: DONE**

Reviewed: `research-log/072-hypothesis-iter-5-omst-v5-factorization.md`  
Verified line count: **628**

# 1. Blind Assessment

## Overall: NEEDS_REVISION

The abstract factorization theorem and the restricted two-state impossibility corollary are correct. I found no finite countermodel under their stated types. However, the artifact is not yet rigorous as a whole because:

1. the separately falsifiable LangGraph proposition names “exact” schemas that are never defined and omits run-state premises needed to make `actual_received_*` a function;
2. T3 is incorrectly presented as theorem-carrying/minimal even though, under T1–T2, a factor can be extended to a larger codomain;
3. the restricted corollary leaves the type of \(J\) and the exact \(Y\) implicit; and
4. the correspondence layer is called a corollary in one place although it is an independent premise requiring source and runtime evidence.

These defects are repairable. The core is not fundamentally flawed, but it is an elementary quotient/factorization lemma whose honest contribution scope is an engineering control.

## Previous-review issue disposition

| # | Disposition | Judgment |
|---|---|---|
| 1. Separate/eliminate A3 and A4 | **RESOLVED** | A3/A4 are gone from the abstract theorem. Accessible context is correctly absorbed into the actual input at lines 143–147, while environment equality is moved to correspondence at lines 445–446. |
| 2. Concede definitional theorem or add an unavailable prediction | **RESOLVED** | v4’s constructed identity is conceded at lines 25–33 and classicality at lines 494–506. The new universal quantifier is actually proved, not merely asserted, although calling it a scientific “prediction” remains inflated. |
| 3. Remove duplicated P13/P15 paths | **RESOLVED** | Events, clauses, verifier, and duplicate equalities are removed. |
| 4. Repair `E`/`f` type | **RESOLVED** | Both symbols are removed; `tau=g∘pi` is well typed. |
| 5. Correct null-record claim | **RESOLVED** | The digest/sentinel boundary is removed. |
| 6. Complete correspondence path and fixture | **IMPROVED** | `_proc_input`, availability, mapper, callable input, and bound environment are now named at lines 432–449. It remains incomplete because the schemas, graph construction, channel types, cache/checkpoint state, and invocation protocol are unspecified. |
| 7. Formalize the projection domain | **RESOLVED** | The previous `C⊆dom(s)` issue disappears under a total `pi:S→Q` with `Q=pi(S)` at lines 138–147 and 194–200. |

## Justification Correctness

### What exactly must be proved?

Let \(S,Q,Y\) be sets, \(\pi:S\to Q\), \(\tau:S\to Y\), and \(Q=\pi(S)\). Define

\[
\operatorname{closed}(\pi,\tau)
\iff
\forall s,s'\in S,\quad
\pi(s)=\pi(s')\Rightarrow\tau(s)=\tau(s').
\]

The claim is

\[
\exists g:Q\to Y,\quad \tau=g\circ\pi
\iff
\operatorname{closed}(\pi,\tau).
\]

### Necessity, independently re-derived

Assume \(\tau=g\circ\pi\). If \(\pi(s)=\pi(s')\), functionality of \(g\) gives

\[
\tau(s)=g(\pi(s))=g(\pi(s'))=\tau(s').
\]

Thus \(\tau\) is constant on every fiber. Lines 202–219 are correct.

### Sufficiency, independently re-derived

Define a relation

\[
G=\{(q,y)\in Q\times Y:
\exists s\in S,\ \pi(s)=q\land\tau(s)=y\}.
\]

For every \(q\in Q=\pi(S)\), a representative exists. Since \(\tau\) is total, at least one corresponding \(y\in Y\) exists. If two values \(y,y'\) arise from representatives \(s,s'\), then \(\pi(s)=\pi(s')=q\), so closure yields \(\tau(s)=\tau(s')\), hence \(y=y'\). Therefore \(G\) is the graph of a total function \(g:Q\to Y\), and for every \(s\),

\[
g(\pi(s))=\tau(s).
\]

Lines 221–241 correctly establish existence, uniqueness of the defining value, totality, and equality.

Moreover, because \(\pi\) is surjective onto \(Q\), the factor \(g\) itself is unique: any two factors agree at every \(q=\pi(s)\). The theorem only claims existence, so omitting this stronger conclusion is not an error, but stating uniqueness would sharpen it.

### Reachable-image and boundary cases

- If \(S=\varnothing\), then \(Q=\varnothing\); closure is vacuous and the unique empty function \(g:\varnothing\to Y\) factors \(\tau\). Nonemptiness is unnecessary.
- Finiteness is unnecessary.
- If \(S\ne\varnothing\), existence of total \(tau:S\to Y\) already entails \(Y\ne\varnothing\).
- If \(\pi\) is injective, closure is automatic.
- If \(\pi\) is constant, closure is exactly constancy of \(\tau\).
- Singleton and empty fibers cause no problem; under \(Q=\pi(S)\), empty fibers do not occur.

### Two-state corollary

For \(S=X\times P\), \(X=\{x\}\), \(P=\{p_0,p_1\}\), and \(\tau(x,p)=J(p)\), the exact canonical byte strings differ at `agent_id`:

```text
{"activity_id":"activity-0","agent_id":"agent-0","entity_id":"entity-0"}
{"activity_id":"activity-0","agent_id":"agent-1","entity_id":"entity-0"}
```

Under \(\pi_{\text{task}}(x,p)=x\), both states map to the same input, while their targets differ. A single-valued \(g_{\text{task}}(x)\) cannot equal both. Under \(pi_{\text{full}}(x,p)=(x,p)\), \(g_{\text{full}}(x,p)=J(p)\) factors \(\tau\).

Lines 310–354 are correct. No cryptographic or global injectivity assumption about canonical JSON is needed.

### Type defect

Lines 115–124 and 282–308 never formally declare a function type for \(J\) or an exact restricted output domain. The corollary should state, for example,

\[
B=\{\text{canonical byte strings}\},\quad
J:P\to B,\quad
Y=J(P)\ \text{or}\ Y=B.
\]

As written, the intended typing is evident from prose and the JSON artifact, but it is not fully unpacked.

## Mathematical Depth and Validity Domains

### Is fiber constancy genuine structure?

Yes, but it is classical and nearly definitional. It is the condition

\[
\ker(\pi)\subseteq\ker(\tau),
\]

equivalently the universal property that \(\tau\) descends to the quotient/image determined by \(\pi\). Projection-fiber notation is not decorative: it exposes the exact obstruction. It does not, however, add mathematical depth beyond elementary function factorization.

### Are T1–T4 accurately characterized?

- **T1, finite and nonempty:** not used. Neither part is needed when \(Q=\pi(S)\). Calling the table “Minimal abstract assumptions” at line 369 is therefore false.
- **T2, total \(\pi,\tau\):** load-bearing for the stated everywhere-defined equality. Partial functions require a restricted domain or explicit bottom/error semantics.
- **T3, \(Q=\pi(S)\):** a useful normalization that makes the factor canonical and unique, but not necessary for existence under T1–T2. If \(Q\supsetneq\pi(S)\), choose \(s_0\in S\), set \(y_0=\tau(s_0)\), define the factor on \(pi(S)\), and assign \(y_0\) to unreachable inputs. Thus lines 260–264 and 375–380 overstate T3’s theorem-carrying role.
- **T4, total deterministic functions:** functionality is load-bearing for necessity. Totality outside the reachable image is only relevant if a larger codomain is retained.

The accurate consequence of dropping T3 is loss of uniqueness/canonicality off the reachable image, not failure of the existence biconditional under the stated nonempty regime.

## Logical Soundness

The artifact now separates three claims substantially better:

1. **Abstract theorem:** proved and correct.
2. **Restricted provenance corollary:** proved and correct once \(J:P\to Y\) is stated.
3. **Pinned LangGraph correspondence:** independent and currently unverified.

That separation is explicit at lines 98–104 and 398–399. However, lines 7–8 call the implementation correspondence a “corollary.” It is not a corollary of the theorem. It is an independent source/runtime proposition; only after establishing it does one obtain a LangGraph application corollary.

The source chain itself is plausible and correctly repaired. Official 1.2.9 source shows that `attach_node` constructs input channels and a mapper from the node input schema, `_proc_input` reads available channels and applies the mapper, and the resulting `val` becomes `PregelExecutableTask.input` ([state.py](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/graph/state.py), [_algo.py](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_algo.py), [_read.py](https://github.com/langchain-ai/langgraph/blob/1.2.9/libs/langgraph/langgraph/pregel/_read.py)). The pinned object `95af6a0…` is the 1.2.9 release commit ([commit](https://github.com/langchain-ai/langgraph/commit/95af6a00718588e7b7ce17310e8006d267896a77)).

What remains missing is a closed formal subject for that source chain:

- `TaskStateOnly` and `TaskStatePlusProvenance` are called “exact” at lines 422–423 but are not defined.
- The enclosing graph state schema, annotations/reducers, node signature, edge topology, input invocation, and checkpointer/cache configuration are absent.
- `_proc_input` can return a cached shallow copy before reading channels; fresh/isolation conditions for `input_cache`, channel objects, checkpoint, and mutations are not specified.
- Lines 464–466 treat one replicate as enough, but one observation cannot establish that `actual_received_*` is a deterministic function. Determinism must come from a source-level argument under fixed run state, not from failure to observe nondeterminism once.

## Assumption Completeness

### Abstract theorem

| Premise | Necessary effect | Violation consequence |
|---|---|---|
| \(\pi:S\to Q\) is a function defined on all \(S\) | Every state has one observation | A partial projection requires restricting the theorem domain or totalizing errors. |
| \(\tau:S\to Y\) is a function defined on all \(S\) | Every state has one exact obligation | Partial or multivalued obligations are not covered. |
| Candidate behavior is a function of the modeled input | Same input forces same output | Hidden state, correlated randomness, history, store, configuration, or globals invalidate the task-only impossibility application unless included in \(\pi\). |
| \(Q=\pi(S)\) | Canonical and unique factor | Not necessary for existence under nonempty \(S\); only unreachable-domain extension becomes nonunique. |
| \(J:P\to Y\) and \(J(p_0)\ne J(p_1)\) | Makes the restricted target typed and nonconstant | Without target separation, the two-state impossibility does not follow. |

### LangGraph application

The application additionally needs:

- literal definitions of both node input `TypedDict`s and the enclosing graph state schema;
- proof that their keys compile to the intended `proc.channels`;
- exact channel types and availability at the PULL step;
- proof of mapper behavior—TypedDict should result in no coercive mapper in this source, but that depends on the exact classes;
- fresh or explicitly controlled input cache, checkpoint, channel state, triggers, and graph invocation;
- equality of all action-readable context within each witness pair;
- entry-time capture before mutation;
- a deterministic source-level model for input construction;
- an independently justified security obligation if “security” rather than “record reconstruction” is claimed.

If task inputs differ, the LangGraph task-impossibility application fails. If only the full-schema positive control fails, the task impossibility can still hold; it is unnecessarily conservative for lines 451–452 to treat every full-control mismatch as invalidating the task-side inference.

## Variables and controls

The intended future fixture is a \(2\times2\) correspondence check:

- varied state coordinate: \(p_0\) versus \(p_1\);
- varied node schema: task-only versus task-plus-provenance;
- controlled: task tuple \(x\), source object, graph construction, channel state, mapper, code, config, store, globals, runtime context, and instrumentation;
- observed variable: mapping at callable entry.

The full schema is a useful positive control for deliverability, but it is not required for the task-side impossibility. No security verdict or causal effect estimate is produced.

## Taxonomy Verification

`Scope Mismatch × Formal Derivation × formalize`, with `decouple` secondary, is accurate. The mismatch is between the full-state obligation and the action-observable quotient. This applies a known structure to a runtime boundary but does not synthesize a defense stack or integrate independent techniques into a new method.

The heightened Bridge × Synthesis tripwire is therefore not triggered. The work’s weakness is elementary/classical scope, not hidden stacking.

## Anti-Stacking Check

**Passes narrowly.**

A test of one selected action establishes at most

\[
\neg\operatorname{correct}(g_0).
\]

The theorem establishes, for the two-state witness,

\[
\forall g:X\to Y,\quad \neg\operatorname{correct}(g).
\]

This stronger quantifier is supported by the same-input/different-target contradiction, and its scope is explicitly limited to deterministic total functions on the modeled input. It is therefore not merely a quantifier change without proof.

However, “distinguishing prediction” at lines 341–342 and 534–536 should be softened to “universal logical consequence.” The target and witness are researcher-chosen precisely to create a nonconstant fiber. This is not independent empirical evidence or a novel scientific prediction.

## Occam’s Razor Check

The theorem’s core is close to minimal, but the assumption presentation is not:

- remove T1 entirely;
- treat \(Q=\pi(S)\) as a definition of the factor domain, not a load-bearing assumption;
- state \(J:P\to Y\);
- optionally strengthen existence to unique existence.

Two states are indeed the smallest witness to nonconstancy within a fiber. The full projection is the simplest sufficiency construction. The second schema in the future fixture should be labeled an optional positive control rather than part of the minimal task-impossibility test.

## Alternative Explanations

- **Aliases or derived fields:** correctly handled semantically. If another delivered coordinate determines \(J(p)\), the projection is closed.
- **Correlated application state:** correctly handled; the artificial product \(X\times P\) guarantees independence only for the exact witness domain.
- **Hidden context:** remains the primary threat to correspondence. Equal callable mapping is insufficient if config, runtime, store, globals, closure state, or invocation history differs.
- **Randomness/history:** outside T4. Merely not observing nondeterminism once does not prove absence.
- **Partial/unavailable channels:** `_proc_input` omits unavailable list-valued channels. The planned audit recognizes this.
- **Mapper behavior:** can drop, encode, or coerce fields. The exact TypedDict definitions are needed before “mapper identity” is meaningful.
- **Input cache/checkpoint state:** newly identified omission; a cached value or nonfresh channel state can explain the observed mapping.
- **Mutable capture:** shallow-copied or subsequently mutated nested mappings can make post-entry logs differ from the true entry argument.
- **Instrumentation:** capture history itself can become accessible state unless fresh and write-only.
- **Source mismatch:** correctly separated from theorem falsity.
- **Classical prior:** the result is a quotient/factorization or functional-dependency criterion, not a new noninterference theorem.
- **Security-target construction:** choosing \(tau(x,p)=J(p)\) proves inability to reconstruct hidden provenance. It does not establish that every real node has this security obligation or that another framework component cannot enforce provenance. The artifact mostly acknowledges this, but “security closure” must always remain explicitly relative to \(tau\).

## Severity-ordered revision requirements

1. **Make the LangGraph proposition executable and closed** at lines 420–466: define both TypedDicts, enclosing state schema, channel annotations, node, graph edges, invocation, checkpointer/cache state, and capture point. Distinguish within-schema pairwise controls from cross-schema differences.
2. **Prove deterministic correspondence rather than infer it from one replicate** at lines 464–466. Include fresh `input_cache`, checkpoint/channel snapshots, mapper purity, and mutation controls.
3. **Correct T3 and minimality claims** at lines 260–264 and 369–380. A larger codomain does not invalidate existence under T1–T2; it only requires a nonunique extension.
4. **Type the restricted instance completely** at lines 282–308: declare \(J:P\to B\), \(Y\), and codomains for \(pi_{\text{task}}\) and \(pi_{\text{full}}\).
5. **Rename the correspondence “proposition” consistently** at lines 7–8 and separate its task-side load-bearing conjunct from the full-schema positive control.
6. **Keep the contribution scope honest:** absent an externally supported provenance obligation, call the instance a record-reconstruction/schema-sufficiency control, not evidence of a general security failure.

# 2. Actionable Coaching

Use the genuinely minimal theorem:

\[
\textbf{Theorem.}\quad
\text{For sets }S,Y,\ \pi:S\to Q=\operatorname{im}\pi,\ \tau:S\to Y,
\]

\[
\exists!\,g:Q\to Y\text{ with }\tau=g\circ\pi
\iff
\ker(\pi)\subseteq\ker(\tau).
\]

No finiteness or nonemptiness premise is needed. If an arbitrary larger action domain \(Q_0\) matters, state a separate extension lemma and distinguish existence from uniqueness off the reachable image.

Type the witness as:

\[
P=\{p_0,p_1\},\quad B=\text{canonical JSON byte strings},\quad
J:P\to B,
\]
\[
X=\{x\},\quad S=X\times P,\quad Y=J(P),
\]
\[
\pi_t:S\to X,\quad \pi_f:S\to X\times P.
\]

For correspondence, split the claim:

- \(C_{\text{task}}\): the two states yield identical complete action-observable inputs under the task schema;
- \(C_{\text{full}}\): the full-schema inputs differ exactly at provenance.

Only \(C_{\text{task}}\) plus target separation is required for impossibility. \(C_{\text{full}}\) is a positive control and constructive deliverability check.

The fixture specification should include literal Python declarations, exact graph construction, fresh-run semantics, checkpoint/channel snapshots, empty/fresh input cache, mapper identity, and canonical entry-time capture. Source inspection should prove the deterministic mapping from those fixed inputs; execution should check correspondence, not infer determinism.

The most direct foundations are:

- quotient-set factorization and kernel inclusion;
- Armstrong-style functional dependencies in database theory;
- Goguen–Meseguer noninterference;
- Sabelfeld–Myers observational equivalence.

The Doob–Dynkin lemma is a useful analogy only if measurable spaces are later introduced; it should not be cited as the present theorem.

Finally, the honest publication scope is narrow: this is a sound classical lemma plus a potentially useful framework regression/control protocol. Without a justified real security policy, broader framework evidence, or a nontrivial new method, it is not a top-tier research contribution.
