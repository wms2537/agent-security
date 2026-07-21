# TBEA development bundle and parser freeze

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 7  
**Task:** T042 · **Status:** parser frozen before independent coding

## Label-blind bundle result

After commit `e8a2cfa` froze the source, sample, blinding, codebook, and gates,
the pinned public MAST file was placed under ignored `artifacts/` storage and
passed exact identity checks. The frozen preparer returned:

```text
tbea_pilot bundle=PASS rows=18 systems=3 per_system=6 labels_exposed=false config_sha256=c0600cc77187d6fcfb5279a65ca6cd63a88c3734691ede46ed02328ae5730de5 bundle_sha256=be498bfa16349abe13da23c4b310e019c7ff74673635d18b322a678201d24137 source_sha256=a182daadb8ded015efc889db8bde29e5e4dd478e0dcc5516f6727a1bbc43eaec source_rows=1242
```

The development bundle contains six deterministic composite-identity
representatives each for AG2, AppWorld, and MetaGPT. It contains no MAST label.
The raw trajectory files and source JSON remain ignored and will not be
committed.

The representative populations reported before sampling are AG2 597, AppWorld
30, and MetaGPT 200 clusters. MetaGPT's 200 clusters versus 230 rows confirms
that the predeclared repeated-identity rule is active rather than silently
assuming row independence.

## Format findings used only for parser development

No MAST labels were read. Structural inspection established:

- AG2 serializes adjacent Python-literal message dictionaries on one physical
  line. The parser balances top-level braces with Python tokenization, validates
  each dictionary with `ast.literal_eval`, and retains raw gaps.
- AppWorld uses line headings for tasks, supervisor/service messages, loop
  entry/exit, execution output, and evaluation. The parser creates contiguous
  heading blocks. It records an `explicit_terminal_api` marker only for a literal
  `apis.supervisor.complete_task(...)` call.
- MetaGPT uses timestamped message blocks followed by an explicit logger line.
  The parser records that end line as `implicit_log_end`; it does not promote it
  to a deliberate terminal transition or infer an effective authority.

Markers are retrieval aids, not annotations. An independent coder may reject a
marker as insufficient under the frozen codebook. `boxed_answer` is not a
terminal marker; AG2's `SOLUTION_FOUND` is marked as an explicit token but still
requires an explicit authority judgment.

## Losslessness and provenance

Every parser partitions the exact UTF-8 source bytes into contiguous,
non-overlapping events from byte zero through EOF. Every event records byte and
line spans plus a SHA-256 of the selected source bytes. Verification recomputes
each digest from the label-blind raw text. No parser normalizes, summarizes, or
drops an unrecognized byte.

The normative parser is `experiments/tbea_c2_parse.py`. The independent record
schema is `experiments/configs/tbea-c2-pilot-annotation.schema.json`. The schema
permits event references and fixed categorical/reason codes only; raw trace
quotes and sampled labels are excluded.

## Prediction before coding

The structural inspection suggests a real risk that the gate will fail:

- AppWorld exposes a literal supervisor terminal API in five of the six sampled
  traces.
- AG2 sometimes exposes `SOLUTION_FOUND`, but the effective scheduler path is
  not necessarily present; ordinary boxed answers are completion claims, not
  automatically terminal authority.
- MetaGPT exposes logger end records but no obvious deliberate terminal action
  or component that makes a stop effective.

Therefore the most likely honest result is that only AppWorld is jointly
recoverable, below the required two-system coverage. This prediction is not a
verdict: two independent coders must apply the frozen definitions.

## Independent coding rule

Two sterile coders will receive randomized aliases, the parser bundle, raw
label-blind text, protocol 108, and the fixed annotation schema. Each writes one
immutable record without reading the source JSON, MAST labels, the other coder's
record, this prediction, or any association result. Both records must exist
before agreement is computed or adjudication begins.

## Boundaries

This is still a Phase-2 measurement pilot. No hypothesis has been confirmed, no
Phase-3 experiment or review round is opened, and no Kaggle, framework/model,
attack, gated-data, held-out, external-message, or publication action occurred.
