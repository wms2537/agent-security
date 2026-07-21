# TBEA label-blind schema-pilot protocol

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 7  
**Task:** T042 · **Status:** frozen before public sample construction

## Purpose

This development pilot asks whether termination-boundary evidence–authority
alignment (TBEA) is measurable from the authorized public MAST artifact. It does
not estimate an association, test a defense, infer causality, or claim that MAST
represents deployed agents.

The protocol is deliberately frozen before deterministic sample construction.
The normative machine-readable contract is
`experiments/configs/tbea-c2-pilot-v1.json`; the only preparation program is
`experiments/tbea_c2_pilot.py`.

## Source identity and attribution

- Dataset: MAST-Data, published with *Why Do Multi-Agent LLM Systems Fail?*
- Authors: Mert Cemri et al.
- Paper: <https://arxiv.org/abs/2503.13657>
- Dataset card: <https://huggingface.co/datasets/mcemri/MAST-Data>
- Revision: `5a82e32347f70a701a3c68637de12f8a0be3de3c`
- File: `MAD_full_dataset.json`
- Size: `63,463,757` bytes
- SHA-256: `a182daadb8ded015efc889db8bde29e5e4dd478e0dcc5516f6727a1bbc43eaec`
- Rows: `1,242`
- Dataset-card license: CC-BY-4.0

The artifact is a public development source, not a held-out tier. Its 1,242 rows
do not match the paper's 1,642-row table, and the omitted model-family blocks
must never be imputed.

## Unit and repeated identities

The pilot's sampling unit is one deterministic representative of a composite
identity cluster:

```text
(mas_name, llm_name, benchmark_name, trace_id, trace.index)
```

The cluster ID is the SHA-256 of the canonical JSON array of those five values.
Within a repeated cluster, the representative is the lexicographically smallest
trajectory SHA-256, then the smaller source ordinal. This rule uses no outcome
label. A future primary analysis, if one is ever approved, must also use one
representative per cluster; an all-row cluster-robust analysis can only be
secondary.

## Development sample

The sample is exactly six representatives from each of:

- `AG2`: role-dialogue format;
- `AppWorld`: supervisor/service-agent workflow; and
- `MetaGPT`: structured `FROM`/`TO`/`ACTION` messages.

These systems were selected for materially different observable formats, not
their MAST labels. For each system, representatives are ranked by:

```text
sha256("TBEA-PILOT-1|2026-07-22|label-blind" + NUL + cluster_id)
```

then by `cluster_id`; the first six are selected. The 18 pilot clusters are
development-only and will be excluded from any later confirmatory sample.

## Blinding firewall

The preparer explicitly whitelists metadata and trace fields and emits no
`mast_annotation`. Annotators may receive only the generated `bundle.json`, raw
trajectory text files, the frozen codebook, and later-frozen parser output.
They may not access the source JSON, row labels, label counts for sampled rows,
each other's records, or an association result.

Raw trajectory content can itself reveal apparent errors. Therefore label
blinding prevents direct target leakage but does not make semantic judgments
independent. Coders must not decide whether the task truly succeeded. They code
only explicit terminal predicates, evidence events, delivery paths, and visible
authority relations.

## Measurement codebook

### Terminal transition

Select an exact parser event only when the trace explicitly shows a deliberate
transition from active execution to a terminal state. A final line merely
because the log ends is insufficient. Timeout, truncation, exception, or missing
tail is not a deliberate stop unless the trace explicitly says the runtime
treated it as such.

### Effective authority

Select the actor or component whose recorded action makes the run terminal.
Distinguish:

- an actor claiming “done”;
- an actor recommending stop;
- a supervisor accepting a result;
- a scheduler/controller emitting the terminal transition; and
- implicit log end with no visible authority.

If the path from utterance to effective transition is not visible, record
`indeterminate`; do not infer authority from a title such as CEO, supervisor, or
verifier.

### Candidate evidence

Select an exact earlier event only when it explicitly bears on the terminal
predicate. Examples of eligible evidence types are a verifier result, tool or
environment outcome, explicit unfinished-obligation record, explicit fault, or
explicit completion confirmation. Mere confidence, fluent prose, framework
reputation, or an annotator's task solution is not evidence.

Record origin, temporal order, target binding, verification relation, and
dependency coverage separately. An item being earlier in the global log does
not prove that the effective authority could see it.

### Visibility

- `visible`: an explicit delivery, shared-state read, quoted receipt, or direct
  same-actor observation connects the evidence to the authority before stop;
- `not_visible`: the trace explicitly confines the evidence to another actor or
  path with no delivery before stop;
- `indeterminate`: telemetry does not establish either relation; or
- `no_candidate_evidence`: no eligible evidence event is found.

### Authority–evidence relation

- `supports_stop`: explicit evidence available at the boundary supports the
  declared terminal predicate;
- `conflicts_visible`: explicit conflicting evidence is visible to the authority
  before it stops;
- `conflicts_stranded`: explicit conflicting evidence exists before stop but an
  observable delivery boundary keeps it from the authority;
- `no_decisive_evidence`: no eligible evidence bears decisively on the predicate;
- `indeterminate`: conflict/support or visibility cannot be established; or
- `no_observable_deliberate_terminal_transition`.

Only `supports_stop` maps to `aligned`. `conflicts_visible` and
`conflicts_stranded` map to `misaligned`. Missing or ambiguous telemetry never
maps to misalignment.

## Parser-development boundary

The preparation program creates lossless raw text and an immutable bundle
manifest. After sample construction, the author may develop deterministic
system-specific segmentation on these 18 development traces only. Every parser
event must retain exact source line/byte spans and a SHA-256 of the selected
source bytes. Parser code and output schema must be committed before independent
coding begins. Parser failures remain failures; no line may be silently dropped
or semantically rewritten.

The future confirmatory corpus, if any, must exclude these 18 clusters and use
the frozen parsers without format-specific changes informed by its MAST labels.

## Independent coding and agreement

Two sterile coders independently receive randomized trace aliases and the same
frozen inputs. They return one record per trace. Adjudication occurs only after
both immutable records exist and is not used to inflate pre-adjudication
agreement.

The gate requires:

- exact terminal-event agreement at least 0.80 where both select a deliberate
  transition;
- exact effective-authority agreement at least 0.80 on those same traces;
- raw visibility agreement at least 0.75;
- raw authority–evidence-relation agreement at least 0.75;
- nominal Krippendorff alpha at least 0.67 for visibility and relation, with at
  least two observed categories; and
- source-span/digest validity exactly 1.00 for every selected event.

If alpha is undefined because the sample has only one category, reliability of
that construct is not demonstrated and the pilot does not authorize a
confirmatory hypothesis.

## Coverage gate

At least two systems must each have at least four of six traces on which both
coders recover a deliberate terminal event and effective authority. No single
system may provide more than 60% of all jointly recoverable traces. This is a
measurement gate, not evidence that three systems are representative.

After a passed annotation gate, a separate script may read MAST labels only to
report label counts among parser-eligible clusters for sample-size feasibility.
It must not compute TBEA-by-label cross-tabs or association estimates before a
confirmatory hypothesis is frozen. If counts cannot support the predeclared
matched analysis, the direction stops.

## Fixed stop interpretation

Any failed load-bearing gate closes the empirical PDPF/TBEA branch on the
authorized artifact. We will not:

- recode indeterminate as misaligned;
- replace exact authority with a role-title heuristic;
- choose new systems after seeing their labels;
- expand the development sample to hunt for agreement;
- turn the pilot into a positive result;
- patch the old synthetic PQF census; or
- substitute a low-novelty formal theorem to avoid a negative decision.

## Commands, before real source access

Static and synthetic checks:

```bash
python -m json.tool experiments/configs/tbea-c2-pilot-v1.json >/dev/null
python -m py_compile experiments/tbea_c2_pilot.py
python -I experiments/tbea_c2_pilot.py self-test
```

Only after this protocol and those artifacts are committed may the exact public
file be placed under the ignored `artifacts/` tree and sampled. Generated raw
trajectory text is not committed.

## Authorization boundary

No Kaggle action is authorized. This pilot also performs no framework
acquisition/import/execution, model call, attack reproduction, gated-data access,
held-out or locked-test action, external message, or publication. Phase 3 stays
closed, and hypothesis-review spending stays at 23/30.
