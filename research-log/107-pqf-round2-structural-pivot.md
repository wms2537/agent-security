# PQF round-2 structural pivot: measure before defending

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 7  
**Task:** T041 · **Status:** selected; schema-pilot gate precedes hypothesis

## Decision

Retire the constructed PQF v2 empirical claim and do **not** patch it into a
third synthetic controller census. Select a narrower, observational direction:

> Test whether the termination boundary, its effective authority, and the
> visibility of decision-relevant evidence can be recovered reliably from
> natural public multi-agent traces before proposing an association hypothesis.

The candidate construct is **termination-boundary evidence–authority alignment
(TBEA)**. It is not yet the active confirmatory hypothesis. Iteration 7 is an
understanding iteration whose first output is a label-blind schema pilot. Only a
successful measurement gate permits a later v3 hypothesis and another theory
review.

The full primary-source and data-provenance basis is
`research-log/106-evidence-authority-primary-source-audit.md`.

## Why v2 is retired rather than repaired

The round-2 reviewer proved that the v2 result is substantially fixed by the
author-chosen schedule:

- the three early substitutions already force at least `3/25 = 0.12`
  authority-on failures, above the 0.10 baseline-risk floor;
- the authority-off schedule is copied from the clean controller, fixing clean
  completion loss and clean overhead at zero;
- the same gate stack already predicts the proposed mediation, so the
  anti-stacking test is not distinguishing;
- the decision-9 contract is non-total, and the advertised oracle fixtures are
  not concrete independent validation.

Making those schedules longer, adding more mutants, or repairing the ninth
lookup would improve implementation hygiene but would not restore a
non-predetermined scientific result. PQF v2 therefore ends as a useful negative
design result: an author-controlled finite census cannot validate a claimed
defense when the treatment schedule encodes the effect and guardrails.

## Candidate comparison

| Candidate | Scientific merit now | Decision |
|---|---|---|
| Patch PQF v2 and rerun a larger constructed census | Predetermined outcome and unchanged anti-stacking failure | Reject |
| General evidence–authority theory or graph reference monitor | Duplicates PCAS/FORGE, Fides, NeuroTaint, Temporary Authority, and classical information flow | Reject |
| Formal progress-authority cut theorem | Likely correct but classical, weakly novel, and disconnected from natural termination evidence | Park; do not use as an easy escape |
| Broad MAST “evidence gap” relabeling | MAST already defines information withholding, ignored input, and verification failures | Reject |
| TBEA measurement pilot at the deliberate termination boundary | Non-predetermined and locally distinct if authority/visibility can be recovered reliably | Select conditionally |
| Immediate IPHE activation | Still third in the user-selected portfolio; AHE evidence is relevant but does not cure PDPF measurement uncertainty | Keep parked |

## Latest evidence that changes the scope

The pinned MAST artifact at revision
`5a82e32347f70a701a3c68637de12f8a0be3de3c` contains 1,242 rows, not the
paper's 1,642. The missing 400 rows are the four stated Qwen2.5/CodeLlama
ProgramDev blocks. The human file contains 19 rows rather than 21. The full
artifact has 208 rows labelled FM-3.1, but its `trajectory` is a single
heterogeneous native string and supplies no normalized actor, event, authority,
evidence, or termination-locus field. Ninety composite identities repeat
without an explicit replicate identifier.

Those facts rule out treating MAST as a ready-made EAG benchmark. They do allow
a bounded public-data schema pilot with system-specific parsers, source-span
provenance, and an explicit `indeterminate` outcome.

The closest primary work further narrows novelty:

- MAST owns whole-trace failure modes including premature termination,
  information withholding, ignored input, and verification failures.
- Who&When and AgentRx own generic actor/step failure localization.
- LoopTrap owns termination poisoning and already proposes independent progress
  verification and provenance separation.
- IAL-Scan owns static loop graphs and effective-bound coverage.
- PCAS/FORGE and Fides own causal provenance/reference-monitor and information-
  flow enforcement for privileged actions.
- NeuroTaint owns offline semantic provenance reconstruction.
- Temporary Authority owns freshness, causal priority, binding, and eligibility
  of evidence at a durable-effect commit boundary.

The remaining local question is whether comparable termination-boundary
observability exists in natural traces at all. It is not whether a new firewall
works.

## Pilot construct, deliberately before a hypothesis

For one trace, the pilot attempts to recover only these source-grounded fields:

1. `terminal_transition`: the observable event that changes the run from active
   to terminal;
2. `effective_authority`: the actor or component whose transition makes that
   stop effective, distinct from an actor merely claiming completion;
3. `candidate_evidence`: an earlier source span that could bear on the declared
   terminal predicate;
4. `evidence_origin`: tool, environment, verifier, worker, supervisor, or other
   explicitly visible producer;
5. `visibility_to_authority`: visible, not visible, or indeterminate from the
   trace;
6. `temporal_order`, `target_binding`, `verification_relation`, and
   `dependency_coverage`, each separately coded rather than collapsed; and
7. a final measurement state of `aligned`, `misaligned`, `indeterminate`, or
   `no_observable_deliberate_terminal_transition`.

The pilot must not inspect or export `mast_annotation`. Its purpose is schema
recoverability and coder agreement, not association estimation. Raw trace text
may reveal apparent success or failure, so label blinding is necessary but not
sufficient; the codebook must prohibit exposure coders from deciding whether
the task truly should have terminated.

## Pre-hypothesis gate

Proceed to a confirmatory TBEA hypothesis only if all conditions pass on a
frozen development sample:

1. At least two materially different MAST formats yield an observable deliberate
   terminal transition and effective authority.
2. Each parsed event preserves byte offsets or line spans back to the source;
   unparsed spans remain unparsed.
3. Independent coding distinguishes `misaligned` from `indeterminate` without
   MAST labels, with a predeclared acceptable agreement threshold.
4. Visibility to the effective authority is evidenced by the trace rather than
   inferred from a framework name or role title.
5. Coverage is not supplied almost entirely by one MAS and is not selected using
   FM-3.1.
6. Ambiguous repeated identities are clusterable or excluded by a rule fixed
   before association analysis.
7. The estimated eligible matched sample is large enough for a frozen
   system-and-benchmark-stratified analysis.

If any load-bearing condition fails, close this PDPF empirical branch as
unidentifiable from the authorized public artifacts. Do not convert missing
telemetry into misalignment, relax the gate after seeing labels, or substitute
a formal theorem merely to obtain a positive result.

## Shape of a later hypothesis, if the gate passes

The narrow candidate is an association:

> Among pinned MAST traces with an observable deliberate terminal transition,
> MAST FM-3.1-labelled traces have a higher prevalence of independently coded
> termination-boundary evidence–authority misalignment than system-and-
> benchmark-matched traces with none of FM-1.5, FM-3.1, FM-3.2, or FM-3.3.

This statement remains provisional. A later Phase-2 artifact must independently
freeze sampling, repeated-identity handling, estimand, thresholds, agreement,
coverage, missingness, matching, multiplicity, sensitivity analyses, bias
surface, and failure semantics before review. Modes 3.2 and 3.3 may be secondary
convergent checks only because using them as the primary outcome would be close
to circular.

No causal, defense-efficacy, attack-resistance, deployment-prevalence, model-
family, or production-runtime inference is permitted.

## Taxonomy and anti-stacking

- **Opportunity:** Evidence Gap.
- **Method:** Empirical Mapping.
- **Dominant operation:** `measure`; secondary `differentiate`.
- **Bridge × Synthesis tripwire:** false.

The distinguishing information over the strongest single prior, MAST, is the
explicit temporal relation among terminal transition, effective authority,
evidence source span, and visibility at that boundary. If the pilot cannot
recover those relations independently of MAST's whole-trace labels, the idea
fails anti-stacking and must stop.

## Budget and authorization accounting

- Research iterations: `4/5` after opening this understanding iteration.
- Hypothesis-review rounds: `23/30`; no new round is charged here.
- Phase 3: closed; this is a Phase-2 public-data measurement viability check.
- Kaggle: no action authorized or taken.
- Also absent: framework acquisition/import/execution, model API calls,
  operational attack reproduction, live targets, gated-data access,
  held-out/locked-test action, external messages, or publication.

## Next task

Freeze a label-blind schema-pilot protocol and deterministic extraction contract,
then run only that pilot. A hypothesis and review dispatch are downstream of the
gate, not assumed outcomes.
