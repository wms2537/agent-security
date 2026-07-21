# TBEA schema-pilot result: fail the multi-system measurement gate

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 7  
**Task:** T042 · **Status:** failed gate; empirical PDPF/TBEA branch closed

## Outcome

The frozen label-blind pilot **FAILS**. Termination transition and effective
authority are recoverable in AppWorld, only sparsely in AG2, and not in the
sampled MetaGPT traces. The result therefore does not support a cross-system
termination-boundary evidence–authority hypothesis on the authorized MAST
artifact.

This is a clean negative measurement result, not annotator noise. The two
sterile coders independently agreed exactly on all primary gate fields across
all 18 traces.

## Authenticated inputs

- Frozen protocol commit: `e8a2cfa`
- Frozen parser/agreement commits: `916ec64`, `0831d00`
- Source SHA-256: `a182daadb8ded015efc889db8bde29e5e4dd478e0dcc5516f6727a1bbc43eaec`
- Label-blind bundle SHA-256:
  `be498bfa16349abe13da23c4b310e019c7ff74673635d18b322a678201d24137`
- Parsed manifest SHA-256:
  `8379b954769189443faf2ce7c73a6fab993553c009aab46d06dd518c580e2c4c`
- Coder A SHA-256:
  `c1bc7c152a541e6f11938703f1b72d56b6dc923a70871bced842c2e90c8caf93`
- Coder B SHA-256:
  `18c24923282333504f6ae4f33169783f4ec8c1732acaf3453a97996a87890ab4`

Both coder files validate against the frozen 18-record schema, reference only
existing parser events, use source-grounded actor values, preserve temporal
ordering, and contain no MAST label or raw trajectory excerpt.

## Frozen calculation

The precommitted agreement program returned:

```json
{"both_terminal":7,"checks":{"authority_agreement":true,"relation_alpha":true,"relation_raw_agreement":true,"single_system_share":false,"terminal_event_agreement":true,"two_system_coverage":false,"visibility_alpha":true,"visibility_raw_agreement":true},"coder_a_sha256":"c1bc7c152a541e6f11938703f1b72d56b6dc923a70871bced842c2e90c8caf93","coder_b_sha256":"18c24923282333504f6ae4f33169783f4ec8c1732acaf3453a97996a87890ab4","effective_authority_exact_agreement":1.0,"gate":"FAIL","jointly_recoverable":7,"jointly_recoverable_by_system":{"AG2":2,"AppWorld":5},"maximum_single_system_share":0.7142857142857143,"qualifying_systems":1,"relation_categories":2,"relation_nominal_alpha":1.0,"relation_raw_agreement":1.0,"terminal_event_exact_agreement":1.0,"visibility_categories":2,"visibility_nominal_alpha":1.0,"visibility_raw_agreement":1.0}
```

### Passing gates

- terminal-event exact agreement: `1.00 >= 0.80`;
- effective-authority exact agreement: `1.00 >= 0.80`;
- visibility raw agreement: `1.00 >= 0.75`;
- visibility nominal alpha: `1.00 >= 0.67`, two categories;
- authority–evidence-relation raw agreement: `1.00 >= 0.75`;
- relation nominal alpha: `1.00 >= 0.67`, two categories; and
- source span/digest rate: `1.00`.

### Failing gates

1. **Two-system coverage:** only AppWorld reaches at least four of six jointly
   recoverable traces. Counts are AppWorld `5`, AG2 `2`, MetaGPT `0`; the gate
   requires at least two qualifying systems.
2. **Concentration:** AppWorld supplies `5/7 = 0.7142857` of jointly recoverable
   traces, above the frozen maximum `0.60`.

Either failure is sufficient. Both occur.

## What the perfect primary agreement does and does not mean

Both coders independently classified:

- AG2: two observed deliberate transitions and four with no observable
  deliberate transition;
- AppWorld: five observed and one without an observable deliberate transition;
  and
- MetaGPT: zero observed and six without an observable deliberate transition.

They also agreed that all seven recovered relations supported the observed stop
and that the other eleven had no observable deliberate terminal transition.
This makes the primary negative coverage result unusually clear.

It does **not** establish broad semantic reliability. The coders chose different
candidate-evidence event IDs on five traces, differed on verification relation
on seven, dependency coverage on one, and non-load-bearing reason codes on
eleven. The two-category alpha results mostly separate `supports_stop` from
`no_observable_deliberate_terminal_transition`; this sample contains no coded
misaligned relation. Even without the coverage failures, a mature cross-system
alignment claim would require stronger calibration of these secondary fields.

## Scientific interpretation

The public MAST trajectories are adequate for whole-trace failure labels and
some framework-specific forensic reading. They are not an interchangeable
cross-system event-graph substrate:

- AppWorld exposes a literal supervisor completion API and explicit delivery
  paths.
- Two AG2 traces expose an explicit verifier terminal token, but four ordinary
  boxed-answer traces do not expose an effective terminal transition under the
  frozen rule.
- MetaGPT records reviewer messages and logger endings, not a visible deliberate
  terminal action or the component that makes it effective.

Inferring authority from `Verifier`, `Supervisor`, final-message position, or
framework identity would improve coverage only by replacing observed runtime
authority with a role-title heuristic. That is the exact construct error the
gate was designed to prevent.

The result also explains why a label-level EAG analysis would be misleading:
the systems differ first in telemetry and boundary observability. Pooling them
would confound the proposed mechanism with logging architecture before any MAST
failure label enters the analysis.

## Fixed decision

Close the empirical PDPF/TBEA branch on this authorized artifact. Per protocol:

- do not inspect sampled MAST labels;
- do not calculate an EAG-by-FM-3.1 association;
- do not add systems or traces to hunt for gate passage;
- do not lower the two-system or concentration thresholds;
- do not adjudicate primary fields to manufacture coverage;
- do not treat absent telemetry as misalignment; and
- do not return to the predetermined PQF v2 synthetic census.

The reusable output is a negative design insight: termination evidence–authority
research needs an instrumentation contract that records the terminal transition,
effective authority, evidence delivery, and source provenance at runtime. A
heterogeneous whole-trace corpus cannot reconstruct those facts uniformly after
the event.

## Budget and boundaries

- Research iterations: `4/5`; iteration 7 concludes as a failed understanding
  gate, not an empirical association test.
- Hypothesis-review rounds: `23/30`; none charged for this pilot.
- Phase 3: closed.
- No Kaggle action was authorized or taken.
- No sampled MAST label, framework/model execution, attack reproduction, gated
  data, held-out test, external message, or publication action occurred.

## Next portfolio decision

PDPF has now failed both the synthetic anti-stacking gate and the natural-trace
observability gate. The next principled move is the already user-selected third
study, Invariant-Preserving Harness Evolution, using the final research iteration
first for a current primary-source/data-availability decision—not immediate
implementation or another borrowed threshold.
