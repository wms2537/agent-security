# OMST theory review — round 1

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5
**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

**Status: DONE**

Reviewed [research-log/056-hypothesis-iter-5-omst-v1.md](/home/soh/agent-security/research-log/056-hypothesis-iter-5-omst-v1.md). The file has **492 lines**; both the working-tree file and `git show HEAD:...` report 492.

## 1. Blind assessment

### Justification Correctness: FAIL

The central structural observation is sound: equality of a benign trace view need not imply equality of a security-relevant view. The deterministic paired design, equal decision tapes, exact eligibility check, identity validity gate, and condition-label masking are useful controls.

The primary estimand, however, does not measure what the prose calls a regression rate among secure bases. At lines 132–145,

\[
R=(1-V_{\text{base}})V_{\text{rewrite}}
\]

is averaged over **all** eligible tuples. Therefore the reported rate is:

\[
\frac{\#(\text{eligible, base-safe, rewrite-unsafe})}
{\#(\text{all eligible})},
\]

not the conditional regression rate among eligible base-safe executions. It mixes baseline safety prevalence with rewrite susceptibility. Two rewrite families with identical conditional regression behavior can produce different rates merely because their treatment-specific eligible sets contain different proportions of unsafe bases. The 10-point threshold consequently lacks a stable causal interpretation.

The mechanism-discriminating family comparison is also uncontrolled. Eligibility is rewrite-specific and post-intervention (lines 236–253). Equal eligibility rates within five percentage points do not imply equal composition. Alpha-renaming may exclude one 5% subset while relay insertion excludes a different 5% subset. Comparing family rates without a common eligible/base-safe support set can therefore manufacture the predicted ranking.

The proposed rewrite families are bundled interventions. Relay insertion changes node count, trace length, scheduling, handoff, possible checkpointing, and middleware traversal simultaneously (lines 172–174). State split/merge similarly changes several properties. Thus a higher family rate cannot establish that boundary relocation or metadata loss is the mechanism. Extra execution exposure, canonicalizer behavior, or another bundled change remains sufficient.

There is also a first-principles ambiguity between `B` and some security contracts:

- If `B` contains every actual inert effect and initial capabilities are fixed, capability safety must be invariant under exact `B` equality; a capability regression would instead indicate inconsistent measurement.
- If `B` contains only intended effects while `V` sees additional actual effects, the text must say so explicitly.
- Verification has the same ambiguity because `B` includes completed obligations while `V` checks evidence obligations.

This affects the possible contract-specific signal and hence the pooled 10-point prediction (lines 112–130 and 255–268).

Deterministic predicates are not automatically valid predicates. The single positive control at lines 276–277 is disjunctive: a mutation may pass if either the equivalence checker rejects it or the security evaluator detects it. It therefore cannot establish the sensitivity of each component independently. Condition-label blinding also does not prevent structural family inference from traces.

### Mathematical Depth & Validity Domains: MIXED / FAIL

The appropriate lens is a mapping/fiber argument, and the entry mostly uses it correctly. `B` maps traces into benign-observation classes; OMST searches within one such class for differing security verdicts. Symbols are concretely defined, notation is modest, and the equations are not decorative. They define eligibility, the one-way regression event, and the finite contrast.

The equations nevertheless expose rather than cure the estimand error: the denominator in `Delta_f` does not match the prose’s secure-base regression construct. The entry also never specifies whether `E_f` weights graphs, inputs, tapes, or eligible family-tuples equally. `X_g` appears in the formal definition, yet the “120-graph × three-tape census” does not state the number of inputs or how graphs with different `|X_g|` are weighted.

The exact structural condition should be stated as: security is invariant on each `B`-fiber, equivalently `V` factors through `B`. Calling both `B` and the binary predicate `V` “projections” is imprecise but recoverable. Calling security preservation a “congruence” at lines 181–183 and 432–435 is undefined because no graph-composition algebra or compatibility operation is specified. “Rewrite-invariant” would be accurate.

The listed A1–A9 assumptions each include a regime, which is good. The assumption set itself is incomplete, so the validity-domain requirement is not satisfied overall.

### Logical Soundness: FAIL

The structural argument proves only possibility: `B` equality does not entail `V` equality. It gives no reason to expect a positive frequency, much less at least 10 points. Lines 30–34 acknowledge that neither 10 nor 12 is evidence-derived; thus the effect-size hypothesis is falsifiable but not justified by the supplied mechanism or literature.

The evidence chain is motivational rather than causal evidence. The cited papers support framework sensitivity, harness mutability, security concerns, and the need for stronger metamorphic oracles. None replicates security regression under task-equivalent orchestration rewrites. Most are recent preprints, and *Towards Long-Horizon Agents* is explicitly non-peer-reviewed. The entry correctly limits what these citations prove, but then has no positive evidence for the primary magnitude.

The novelty comparison is also incomplete. The cited systematic survey itself discusses agent action metamorphic relations, end-state equivalence, trajectory/state-aware testing, and security-boundary relations. [ReliabilityBench](https://arxiv.org/abs/2601.06112) already defines action MRs using end-state equivalence rather than text similarity, while [ASSURE](https://arxiv.org/abs/2507.05307) evaluates behavioral consistency and security invariants in an agentic system. Consequently, lines 208–216 and 381–384 do not identify or defeat the strongest nearby prior.

The CrewAI scope logic is sound: a null CrewAI result limits transfer without falsifying the LangGraph-only primary claim. Identity nonzero as a protocol-invalidity condition is also logically appropriate.

### Assumption Completeness: FAIL

Missing load-bearing assumptions include:

- rewrite implementations change only the declared structural factor and faithfully satisfy their preconditions;
- every security-relevant event is observable, canonicalized without loss, and unaffected by instrumentation;
- primary and reference evaluators do not share a common-mode schema or implementation bug;
- graph grammar, rewrite code, `B`, `V`, and thresholds were not tuned using validation outcomes;
- executions do not interfere through process, filesystem, cache, or hidden framework state;
- the 120 graphs and `X_g` are fixed by a deterministic seed/rule before outcome access;
- contract-specific coordinates omitted from `B` are precisely those inspected by `V`;
- base-safety prevalence does not distort the intended estimand—or, preferably, the estimand conditions on base safety;
- family comparisons use common support or otherwise adjust treatment-specific eligibility composition;
- CrewAI execution and evaluator code are sufficiently independent for a transfer claim.

Violation of trace observability, evaluator independence, or rewrite fidelity would invalidate the primary causal attribution entirely.

### Fixed bias surface

The entry formally satisfies the required eight-item surface, one item per category. Its substantive coverage is uneven:

- **Selection:** all generated units are scheduled, but generator tuning and treatment-specific eligibility composition remain.
- **Confounding:** within-pair controls are strong; mechanism-level confounding inside bundled rewrites remains.
- **Assignment:** every graph receives every condition, which is sound; the generation seed and process-isolation contract are not concrete.
- **Protocol deviation:** locks and hashes are promised, but exact commands, versions, budgets, and terminal-state semantics are not specified in this entry.
- **Missing data:** failures invalidate rather than disappear, but “corresponding bundle” versus the entire primary census is ambiguous.
- **Measurement:** exactness and label masking do not establish construct validity, sensitivity, or absence of common-mode error.
- **Analysis flexibility:** the headline contrast is fixed, but tuple weighting and the construction of `E_f`/`I_f` are not.
- **Selective reporting:** mandatory publication of all terminal states and exclusions is strong, conditional on the stated custody process being followed.

### Taxonomy Verification: FAIL

“Empirical Mapping” is plausible for the result, but the claimed local `formalize` classification is not established. The method connects:

1. agent metamorphic/action testing,
2. orchestration-graph transformations,
3. deterministic replay, and
4. security-invariant evaluation.

That looks at least plausibly like **Bridge Opportunity × Synthesis/Unification**, not merely replacement of approximate output similarity. The entry’s purported strongest prior is LLMORPH, but stronger nearby works already use end-state/action equivalence and security invariants. A local extension of ReliabilityBench or ASSURE may achieve most of OMST’s stated goal.

The heightened tripwire is therefore unresolved. The entry must either reclassify and justify why this synthesis is irreducible, or substantively demonstrate what cannot be achieved by locally extending the strongest single prior.

### Anti-Stacking Check: PARTIAL

The entry does state a falsifiable residual prediction: at least 10 points among exact-task-equal eligible pairs, zero identity regression, and a boundary-rewrite-over-alpha ranking. Thus it passes the formal requirement of giving more than “some mutations fail.”

It does not yet establish that this is a prediction a controlled graph-fuzzer plus security checker and functional-equivalence filter would not make. “The plain combination does not require the result” is weaker than showing that it would not predict it. The mechanism-specific ranking could become genuinely distinguishing, but only after common-support comparison and boundary-preservation ablations make the mechanism identifiable.

### Occam’s Razor Check: FAIL

A simpler and more interpretable first hypothesis is:

> Among executions proven base-safe and task-equivalent, one fixed state-boundary rewrite increases security violations relative to an explicit metadata-preserving version of the same rewrite.

That isolates one mechanism, removes arbitrary four-family pooling, and avoids using baseline-unsafety prevalence in the materiality metric. CrewAI transfer and the other rewrite families can follow after the local mechanism survives.

The current design introduces heterogeneous interventions and substantial protocol machinery before establishing that one boundary operation has the predicted effect. Identity, deterministic replay, and oracle validation are necessary controls; omnibus pooling is not.

### Alternative Explanations: INCOMPLETE

A positive result could arise from:

- different base-safety prevalence across eligible sets;
- treatment-specific eligibility composition despite similar eligibility rates;
- increased trace length or execution opportunities;
- canonicalizer or adapter metadata loss;
- predicates treating representational differences as semantic security violations;
- a grammar constructed around the evaluator’s boundary cases;
- actual-versus-intended effect ambiguity in `B`;
- a common bug in primary and reference evaluators;
- extra scheduler, checkpoint, or middleware behavior rather than boundary relocation;
- framework-version-specific defects.

Several are acknowledged, but denominator bias, common-support failure, exposure/trace-length effects, and overlap between `B` and `V` are not adequately controlled.

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. **Repair the primary estimand and weighting** — lines 65–69, 132–150, 221–234, 357–366. Condition the denominator on eligible base-safe executions; state exact graph/input/tape/family weights and the construction of matched identity units.

2. **Resolve the `B`/security-contract overlap** — lines 112–130 and 255–268. Define actual versus intended effects and evidence obligations, then prove for each contract which security coordinates may vary while `B` remains equal. Do not pool logically invariant contract families as if they share the same opportunity for regression.

3. **Make mechanism comparisons causal** — lines 41–55, 168–180, 236–253, 344–355, 364–365. Compare families on common eligible/base-safe support and separate boundary relocation from added steps, checkpointing, middleware traversal, and metadata reconstruction.

4. **Strengthen independent oracle validation** — lines 238–243, 255–279, 330–334, 346–354. Add separate positive and negative controls for the eligibility checker and every security predicate, explicit mutation-adequacy criteria, and a genuinely independent reference implementation.

5. **Correct the evidence and taxonomy argument** — lines 185–219 and 372–384. Compare directly with ReliabilityBench, ASSURE, and other state/action-aware agent MT work; then reclassify or justify why a local extension of the strongest prior is insufficient.

6. **Specify the validation census completely** — lines 16–19, 71–76, 225–234, 281–292, 294–306. Give exact versions/hashes, deterministic generation seed/rule, grammar allocation, every `X_g`, process-isolation rule, execution budget, and whether one failed bundle invalidates the entire primary census.

7. **Add the missing validity assumptions and remove undefined terminology** — lines 160–183, 294–306, 428–457. Add rewrite fidelity, trace completeness, common-mode independence, no validation tuning, no interference, and common-support assumptions; replace or define “congruence.”

The core approach is salvageable, so **FUNDAMENTALLY_FLAWED** is not warranted.

## 2. Actionable coaching

- Redefine the per-family rate as:

  \[
  q_r=
  \frac{\sum 1\{\text{eligible}\}\,1\{\text{base safe}\}\,V_{\text{rewrite}}}
       {\sum 1\{\text{eligible}\}\,1\{\text{base safe}\}},
  \]

  then use an explicitly family-balanced primary average such as `1/4 sum_r q_r`. Keep identity solely as a validity gate.

- For the mechanism ranking, use the intersection of units eligible and base-safe under every compared family. Report both common-support and family-specific conditional rates.

- Create a mechanistic relay ablation:

  1. identity;
  2. extra node with no boundary;
  3. boundary with explicit security-metadata pass-through;
  4. otherwise identical boundary using framework-default reconstruction.

  A default-reconstruction regression that disappears under explicit pass-through is much stronger evidence for the proposed mechanism.

- Build per-contract 2×2 fixtures covering `B` equal/different × `V` equal/different. For capability, provenance, verification, and termination, include known-safe and known-violating traces and require both evaluators to agree independently.

- If `B` records all actual effects, preregister capability regression as impossible and use it as a negative control. If it records only intended effects, rename and define that field unambiguously.

- Drop the unsupported 12-point point estimate unless it is calibrated on a separate development grammar. A normative 10-point decision threshold can stand without pretending to be an evidence-based expected magnitude.

- Compare explicitly against [ReliabilityBench](https://arxiv.org/abs/2601.06112), [ASSURE](https://arxiv.org/abs/2507.05307), and the agent/action-MR work catalogued by the [2026 systematic survey](https://arxiv.org/abs/2605.13898). The novelty claim should identify the exact missing operation in each, not contrast primarily with output-similarity NLP testing.

- Consider a narrower primary hypothesis on one pinned framework, one boundary rewrite, and one contract family. Add the other rewrites and CrewAI only as preregistered replication/generalization stages after that mechanism survives.
