# IPHE primary-source audit and Cycle-2 portfolio closure

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 8  
**Task:** T043 · **Status:** novelty NO-GO; public-data NO-GO; Cycle 2 closed at Phase 2

## Outcome

Do **not** activate the proposed Invariant-Preserving Harness Evolution (IPHE)
hypothesis. Two independent entry conditions fail.

1. **Method novelty fails.** Recent primary work already contains external
   release gates, immutable or evolution-inaccessible evaluators, commit-time
   anytime-valid tests, auditable certificates, hard formal constraints plus
   soft utility, longitudinal versioning, and security-specific immutable
   invariants. Combining those elements under a security label is a narrow
   synthesis or application, not a defensible new method.
2. **Public-data identifiability fails.** No audited official artifact exposes
   every accepted and rejected harness candidate together with its exact diff,
   iteration and decision, security measurement, benign-utility measurement,
   and immutable verifier identity. Endpoint harnesses and aggregate paper
   tables cannot identify security-debt accumulation or the effect of a gate.

The only defensible residual gap is an empirical corpus and protocol:

> A precommitted, evolution-inaccessible security-invariant suite evaluated on
> every real candidate—including rejected candidates—across complete
> multi-iteration harness lineages, with candidate-level benign utility and a
> public immutable decision ledger.

That corpus does not currently exist in the audited public artifacts. Creating
it here would require framework/model execution or an author-constructed
candidate history. The former is not authorized; the latter would recreate the
predetermination defect that invalidated PQF. IPHE therefore stops before a
hypothesis, threshold freeze, theory-review dispatch, or Phase-3 experiment.

## Authorization and evidence boundary

This audit used public paper pages, arXiv HTML, repository metadata, Git refs,
and read-only tree/artifact inspection. It did not:

- acquire, import, or execute an agent framework;
- call a model API or generate harness candidates;
- inspect or run a held-out/locked test;
- reproduce an attack or retain an operational payload;
- access gated data;
- take a Kaggle action; or
- send an external message or publish an artifact.

An independent SciAgent evidence verifier separately checked conceptual overlap
and public lineage availability. That was evidence validation, not hypothesis
review, so it consumes no hypothesis-review round.

## Candidate that was audited

The provisional Phase-1 idea asked whether a fixed external security-invariant
acceptance gate could reduce accepted security-regressing harness mutations by
at least 50% relative to task-only selection, while retaining at least 90% of
the comparator's benign-utility gain and allowing exactly zero verifier drift.

Those numerical thresholds were never frozen as a Phase-2 hypothesis. The
audit tests the prerequisites for measuring them, not their truth. They are now
retired because neither a novel method claim nor an identifiable public test is
available.

## Current primary-source matrix

The retained comparison set is capped at 15 sources. All claims below are
paraphrases from the primary paper or author-maintained artifact.

| Primary source | What it already establishes | Consequence for IPHE |
|---|---|---|
| [Towards Long-Horizon Agents: A Survey](https://www.preprints.org/manuscript/202607.1328) | Separates policy from the external harness and identifies harness evolution, verification, and trustworthy long-horizon operation as explicit frontiers. | The broad invariant-preserving-evolution framing is already named; the survey is framing, not empirical proof. |
| [Agentic Harness Engineering](https://arxiv.org/abs/2604.25850) (AHE) | Makes harness components mutable and versioned, keeps evolution infrastructure outside the editable surface, and evaluates predicted improvements/regressions over iterations. | Harness mutation, lineage, rollback, and regression-aware evolution are not new. |
| [AgentDevel](https://arxiv.org/abs/2601.04620) | Externalizes self-improvement into a one-release-candidate-per-iteration pipeline with a flip-centered promotion gate. Its ablation reports 3.1% versus 14.8% P-to-F regressions with versus without the gate, test scores 34.2 versus 35.0, and zero versus four bad releases. | The closest direct prior already demonstrates regression reduction with nearly retained utility under an external release gate. |
| [Self-Evolving Agent Harnesses via Gated Semantic Quality-Diversity](https://arxiv.org/abs/2607.13683) (GSME) | Separates proposal from deterministic measurement/credit, rejects kernel-touching patches, and uses versioned candidates plus activation, validity, significance, and sealed-test gates. | An immutable measurement kernel and gated candidate tree are occupied. |
| [Harness-Aware Self-Evolving](https://arxiv.org/abs/2607.03935) (HASE) | Co-evolves selected harness components and task solutions while keeping the real-world evaluator external and reviewing changes at phase boundaries. | “Mutable harness, external evaluator” is not a novel boundary. |
| [PACE](https://arxiv.org/abs/2606.08106) | Recasts candidate commitment as a paired sequential test and places an anytime-valid acceptance rule at the commit step. | A principled statistical mutation-acceptance gate is directly occupied. |
| [Self-Evolving Agents with Anytime-Valid Certificates](https://arxiv.org/abs/2607.00871) (SEA) | Keeps the base model frozen, versions the surrounding harness, and admits each modification through an anytime-valid gate that emits an auditable certificate against a fixed error budget. | Versioning, per-change gating, auditability, and fixed error budgets are already combined. |
| [SEVerA](https://arxiv.org/abs/2603.25111) | Formulates self-evolving agent synthesis with hard formal output constraints and soft task-utility objectives; the reported evaluation has zero constraint violations. | “Preserve hard invariants while optimizing utility” is already a direct formal objective. |
| [Safety in Self-Evolving LLM Agent Systems](https://arxiv.org/abs/2606.23075) | Defines a module-by-lifecycle threat surface, shows why adversarial effects can persist across evolution, and calls for immutable safety invariants, longitudinal monitoring, and multi-generation audit trails outside optimization. | The security-specific rationale and control principles are already explicit. |
| [Phantom Guardrails](https://arxiv.org/abs/2607.13083) | Uses a deterministic no-failure micro-lab to show that a proposer can invent a failure and that add-only acceptance can preserve the resulting unnecessary guardrail. | A security suite must include negative obligations and counterfactual necessity; suppression-only gates are insufficient. |
| [Rethinking the Evaluation of Harness Evolution for Agents](https://arxiv.org/abs/2607.12227) | Requires matched feedback/inference budgets, compares harness evolution with task-level search baselines, and reports limited held-out generalization. | Any future study needs matched sampling/refinement controls and cannot treat harness evolution's utility premise as given. |
| [Adaptive Auto-Harness](https://arxiv.org/abs/2606.01770) | Extends harness evolution to open-ended task streams and separates evolution loss from adaptation loss. | Longitudinal, stateful evolution is already an explicit systems target. |
| [Meta-Harness](https://arxiv.org/abs/2603.28052) | Optimizes end-to-end model harnesses rather than only prompts and publishes a final optimized harness artifact. | Outer-loop harness search is occupied, although its public artifact does not expose the lineage required here. |
| [MaMa](https://arxiv.org/abs/2602.04431) | Optimizes agent-system design against task utility and adversarial safety objectives through a game-theoretic search. | Generic “safe agent-system optimization” is already occupied; IPHE would need distinctive longitudinal evidence. |
| [TTHE](https://arxiv.org/abs/2607.08124) | Treats a persistent executable harness as the object of test-time evolution and identifies execution-derived proxy reliability as a central challenge. | Candidate acceptance is inseparable from evaluator reliability; a declared invariant alone is not evidence of validity. |

## Direct-overlap judgment

The proposed IPHE components are each anticipated by close work:

| Proposed component | Direct owners in the audited set |
|---|---|
| Harness as the evolving/versioned object | AHE, GSME, SEA, Adaptive Auto-Harness, Meta-Harness, TTHE |
| External release or acceptance pipeline | AgentDevel, PACE, SEA |
| Immutable/evolution-inaccessible evaluator or kernel | GSME, HASE, Safety in Self-Evolving Systems |
| Hard invariant plus soft utility | SEVerA; adjacent safety/utility optimization in MaMa |
| Per-candidate regression protection | AgentDevel, PACE, SEA |
| Auditable lineage/certificate | AHE, GSME, SEA |
| Security persistence across generations | Safety in Self-Evolving Systems |
| Negative obligation/no-op necessity | Phantom Guardrails |
| Matched-compute baseline and held-out skepticism | Rethinking Harness Evolution |

The conjunction is relevant, but relevance is not novelty. Calling the fixed
checks “security invariants” does not distinguish a method from an external
release gate plus a test suite. The broad IPHE claim is therefore a **NO-GO**.

The narrower future contribution changes taxonomy. It would be an **Evidence
Gap × Empirical Mapping** contribution, dominated by `measure` and `decouple`,
whose novelty lies in complete candidate-level evidence and enforced provenance,
not in proposing another gate.

## Public-artifact availability audit

Repository heads were rechecked with read-only `git ls-remote` on 2026-07-22.
The independent verifier enumerated repository trees and release assets at
these exact snapshots. No repository was cloned or executed.

| Source/artifact | Audited snapshot | What is public | Missing load-bearing evidence |
|---|---|---|---|
| [AHE official repository](https://github.com/china-qijizhifeng/agentic-harness-engineering) | `faf44bc4aea57413c520bc5711c6ebf628e0da1e` | 224 committed blobs, source/configuration, documentation, and a final `experiments/evolved_harness`. The README describes locally generated iteration directories and change evaluations. | No committed run/result/history/lineage directory, rejected candidates, candidate-level security outcomes, or release assets. The evolved-harness path appears as a final example, not a complete evolution history. |
| [Rethinking Harness Evolution code](https://github.com/rethinking-harness-evolution/code) | `ffd1ba1c2c3e31099264f630b9ed44aec63a86a7` | 203 committed blobs of code/configuration; documentation describes generated experiment outputs. | No published experiment-results tree, candidate decisions, security measurement, or release asset. |
| [Meta-Harness reference](https://github.com/stanford-iris-lab/meta-harness) | `44b9942127847f7421db70d8c7e48407f09a3c70` | Cleaned framework and reference examples. | No search lineage or rejected-candidate ledger. |
| [Meta-Harness Terminal-Bench artifact](https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact) | `57fefdb2ff84af3fd81b69d67814acbe69bd0743` | Five blobs in one final optimized-harness commit with an aggregate score. | No candidate sequence, rejects, per-candidate utility, or security results. |
| [A-Evolve canonical repository](https://github.com/A-EVO-Lab/a-evolve) | main `c9d4789f2be499589d543aa08e74d05d10d93177`; harness-evolution branch `986d97d43b6313c94c7e72c0b0ab6181ed9edba0`; adaptive-auto-harness branch `17bc9ebb7d4d142af1b109b43ef160031967cc9a` | Code, configuration, seed workspaces, and analysis machinery. | No finished public candidate lineage or rejected-candidate/security ledger; example database is empty. |
| [MaMa official repository](https://github.com/JNoether/MaMa) | `979ecc9751fc8c563a4e9d65ed0f4b65708f6530` | Evaluation code, a safety dataset, and four best-system JSON artifacts. | Best endpoints are not candidate histories; rejected systems and complete decision lineage are absent. |
| AgentDevel | arXiv record/paper | Aggregate accepted/rejected counts, flip outcomes, and gate-ablation tables. | No official repository linked from the paper; no RC blueprints/diffs or rejected RC artifacts. |
| GSME, HASE, PACE, SEA, Phantom Guardrails | arXiv records/papers | Method and aggregate evaluation descriptions. | No attributable official result repository linked from the audited arXiv HTML. This is a bounded “not located in the paper record” statement, not a claim that no repository could exist elsewhere. |
| SEVerA | paper and linked project surface | Formal method and aggregate constraint/utility results. | The public project surface did not provide a complete evolution lineage suitable for this test. |

### Why aggregate tables and endpoints are insufficient

The proposed causal quantity concerns what an acceptance gate prevents over a
sequence of candidate decisions. It cannot be recovered from a final harness or
an aggregate regression percentage because those omit:

- the denominator of all proposed candidates;
- the exact rejected candidates and their counterfactual security/utility
  measurements;
- candidate identity and byte-level diff provenance;
- the temporal order and incumbent against which each candidate was evaluated;
- whether the verifier, its thresholds, or its test lineage changed;
- matched task-only and sampling/refinement baselines at the same feedback and
  inference budget; and
- whether the suite checks both prohibited behavior and unwarranted defensive
  additions.

Without those fields, accepted-candidate trends are conditioned on an unknown
selection process, rejected regressions are invisible, verifier drift cannot be
tested, and apparent security retention can be an endpoint-selection artifact.
No statistical repair can reconstruct the missing candidate history.

## Narrow future protocol and entry prerequisites

A future iteration may revisit this direction only if a real, public lineage
appears or an explicitly authorized study can create one without contaminating
its own test. Minimum prerequisites are:

1. a complete append-only sequence of every candidate, including byte-level
   diff, parent, proposal time, and accepted/rejected/invalid outcome;
2. an externally anchored invariant-suite identifier and content hash fixed
   before the first candidate, with zero mutation-surface access;
3. candidate-level security and benign-utility measurements for both accepted
   and rejected candidates;
4. negative obligations and a deterministic no-op/counterfactual-necessity
   control, not only tests that reward adding restrictions;
5. task-only selection and matched sampling/refinement controls under identical
   feedback, evaluation, and inference budgets;
6. an immutable ledger binding candidate, evaluator, environment, result,
   decision rule, and decision; and
7. a public non-operational security suite whose validity is established
   independently of the evolving proposer.

These requirements are deliberately stronger than “publish the final harness.”
They are what make longitudinal security debt and prevented regressions
identifiable.

## Independent verification and random source check

The independent verifier returned two unambiguous judgments:

- **novelty NO-GO as phrased**; and
- **public-data feasibility NO-GO**, conditional GO only as a new empirical
  benchmark/data contribution with a complete candidate lineage.

After the 15-source set was fixed, the random check was drawn with:

```text
printf '%s\n' AHE AgentDevel GSME HASE PACE SEA SEVerA Safety-Evolving \
  Phantom-Guardrails Rethinking-Harness-Evolution Adaptive-Auto-Harness \
  Meta-Harness MaMa TTHE Long-Horizon-Survey | shuf -n 3
Safety-Evolving
Adaptive-Auto-Harness
Long-Horizon-Survey
```

- ArXiv `2606.23075` freshly matched the title, authors, 22 June 2026 date,
  module-by-lifecycle threat framing, and evolution-persistence premise.
- ArXiv `2606.01770` freshly matched the title, authors, open-ended task-stream
  setting, and evolution-loss/adaptation-loss framing.
- The Preprints page for the long-horizon survey returned HTTP 403 to the fresh
  command-line request. It was therefore not counted as a fresh pass; its
  identity and claims remain backed by the prior official-manuscript check in
  `research-log/053` and the retained high-confidence source record.

One replacement was drawn from the remaining set:

```text
printf '%s\n' AHE AgentDevel GSME HASE PACE SEA SEVerA \
  Phantom-Guardrails Rethinking-Harness-Evolution Meta-Harness MaMa TTHE |
  shuf -n 1
AHE
```

ArXiv `2604.25850` freshly matched the title, 11 authors, observability-driven
evolution method, ten-iteration evaluation, and final performance claim. The
official repository head independently matched
`faf44bc4aea57413c520bc5711c6ebf628e0da1e`.

The head checks also freshly matched the Rethinking, Meta-Harness, A-Evolve, and
MaMa snapshots in the artifact table. These checks establish source identity;
they do not upgrade preprints into peer-reviewed evidence or fill the missing
candidate histories.

## Cycle-2 decision

Cycle 2 ends at Phase 2 as an informative negative portfolio:

- **OMST:** a minimal factorization theorem and witness survived review, but
  the executable framework correspondence was implementation-defeated.
- **PDPF/PQF/TBEA:** the synthetic claim was design-defeated, then the natural
  trace pivot failed its frozen multi-system observability gate.
- **IPHE:** the method claim is occupied and the longitudinal candidate data
  required for a narrower study are unavailable.

No Cycle-2 direction passes into Phase 3. Phases 3–6 are therefore not entered
for this cycle. This is the correct stop condition: another review round cannot
repair absent novelty or absent identifying data.

## Budget and final state

- Research iterations: `5/5`; this audit consumes the final iteration.
- Hypothesis-review rounds: `23/30`; no round is charged because no viable IPHE
  hypothesis was frozen or dispatched. Seven authorized rounds remain unused.
- Paper-review rounds: unchanged at `2/4`.
- Active hypothesis: none.
- No Kaggle, framework/model, attack, gated-data, held-out/locked-test, external
  message, or publication action occurred.
