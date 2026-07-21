# Evidence–authority graph primary-source audit

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2  
**Status:** bounded primary-source audit complete; conditional measurement pivot only

## Question and authorization boundary

Is a non-predetermined diagnostic hypothesis about evidence/authority alignment
at an agent's termination boundary scientifically viable and still novel against
the strongest 2025–2026 work?

This audit used public papers, public repository pages, dataset cards, and
read-only inspection of one public JSON artifact. It did not reproduce an
attack, retain a payload, run or acquire an agent framework, call a model API,
install a package, access a gated dataset, inspect a held-out target, or take a
Kaggle action.

For this note, **EAG** means an *evidence–authority graph*: an offline diagnostic
record linking (1) a claimed terminal predicate, (2) the actor or component able
to make the stop transition effective, (3) the evidence observable to that
authority, and (4) the evidence's producer, dependency, verification, and
temporal relations. This is a proposed measurement representation, not a claim
that the trace proves the hidden runtime state.

## Decision

**Conditional GO for a narrow measurement/annotation study; NO-GO for the broad
theory or defense claim.**

The defensible question is not whether evidence and authority should be
separated, whether provenance should be tracked, whether termination poisoning
exists, or whether an independent verifier is useful. Those claims are already
occupied. The remaining gap is narrower:

> In natural multi-agent execution traces, can a blinded, reliability-tested
> audit identify the actor/component that makes termination effective, the
> evidence that actor could use, and whether the observed evidence–authority
> relation is aligned, misaligned, or indeterminate at the termination boundary?

The current public data do not answer that question directly. MAST supplies
whole-trace termination-related labels and heterogeneous raw trace strings, but
not normalized actors, events, authority, evidence provenance, or a termination
locus. Who&When supplies generic actor/step failure attribution but no
termination-authority labels. AgentRx is gated and its public card exposes only
annotation fields. The newest commit-time authorization artifact is presently
inaccessible. A study is therefore viable only if it contributes a transparent
cross-system extraction and annotation layer and reports trace insufficiency as
`indeterminate`, rather than treating missing telemetry as a security failure.

This is an **Evidence Gap × Empirical Mapping** move dominated by `measure` and
`differentiate`. It is not a new authorization framework, a graph-engineering
system, an attack paper, or evidence that a proposed defense works.

## Method

The audit preferred paper pages and author-maintained artifacts. The MAST full
and human-labelled JSON files were inspected from their public, pinned Hugging
Face revision through streaming queries; the bytes were not retained locally.
Counts below refer to the artifact as served on 2026-07-22.

The minimum comparison set was MAST/MAST-Data, LoopTrap, IAL-Scan, Agentic
Harness Engineering, PCAS/FORGE, Fides, and AgentRx. Three especially close
neighbors were added because they materially change the novelty judgment:
Temporary Authority, NeuroTaint, and Who&When.

## Primary-source findings

### 1. MAST and the actual MAST-Data artifact

The MAST paper develops 14 whole-trace failure modes in three categories from
150 traces and reports final human inter-annotator agreement of kappa 0.88. Its
termination-adjacent modes are 1.5, unaware of termination conditions; 3.1,
premature termination; 3.2, no or incomplete verification; and 3.3, incorrect
verification. The paper's dataset table enumerates 1,642 traces across seven
systems, four model families, and several benchmarks.

- Paper: <https://arxiv.org/abs/2503.13657>
- NeurIPS 2025 Datasets and Benchmarks record:
  <https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html>
- Official repository:
  <https://github.com/multi-agent-systems-failure-taxonomy/MAST>
- Dataset card: <https://huggingface.co/datasets/mcemri/MAST-Data>
- Audited full artifact, pinned revision:
  <https://huggingface.co/datasets/mcemri/MAST-Data/blob/5a82e32347f70a701a3c68637de12f8a0be3de3c/MAD_full_dataset.json>

#### Artifact identity and paper/artifact mismatch

- Public, ungated Hugging Face dataset; card license is CC-BY-4.0.
- Revision:
  `5a82e32347f70a701a3c68637de12f8a0be3de3c`.
- Full JSON size: 63,463,757 bytes.
- Linked SHA-256:
  `a182daadb8ded015efc889db8bde29e5e4dd478e0dcc5516f6727a1bbc43eaec`.
- The current full artifact has **1,242 records**, not the paper table's 1,642.
  The 400-row difference corresponds to the four 100-row ProgramDev blocks for
  Qwen2.5 and CodeLlama enumerated in the paper but absent from this artifact.
- The artifact consequently exposes only two `llm_name` values, Claude and
  GPT-4o, while the paper analyzes four model families.
- The current human-labelled artifact has **19 records**, not the 21 human
  examples stated in the paper.
- The default Hugging Face dataset build/view fails with
  `DatasetGenerationCastError`: the full and human files have incompatible
  columns. Direct JSON access works, but a default dataset load is not a stable
  analysis interface.

These are material provenance and denominator blockers. A downstream paper must
pin the exact revision, checksum the source, call the population 1,242 rather
than 1,642, and avoid model-family generalizations that the acquired bytes do
not support.

#### Actual schema and termination-label counts

Each full record has:

```text
mas_name, llm_name, benchmark_name, trace_id, trace, mast_annotation
```

`trace` contains `index`, `key`, and `trajectory`; `trajectory` is one large,
system-native string, not a normalized event array. `mast_annotation` contains
14 binary whole-trace labels. It contains no actor, event, reason, evidence,
authority, or per-step field.

Direct counts over the 1,242 records are:

| Label | Meaning | Positive rows |
|---|---|---:|
| 1.5 | unaware of termination conditions | 346 |
| 3.1 | premature termination | 208 |
| 3.2 | no/incomplete verification | 216 |
| 3.3 | incorrect verification | 283 |
| any of the four | union | 743 |
| none of the four | complement | 499 |

The union is not the sum: 516 rows have exactly one of the four labels, 144
have two, and 83 have three. No row has all four.

The core artifact claims can be reproduced without a framework, package, or
local copy. The audit used the following read-only form (long URL wrapped here
only for readability):

```bash
REV=5a82e32347f70a701a3c68637de12f8a0be3de3c
BASE=https://huggingface.co/datasets/mcemri/MAST-Data/resolve/$REV

curl -LfsS "$BASE/MAD_full_dataset.json" |
  jq '{rows:length,
       fm15:(map(.mast_annotation["1.5"])|add),
       fm31:(map(.mast_annotation["3.1"])|add),
       fm32:(map(.mast_annotation["3.2"])|add),
       fm33:(map(.mast_annotation["3.3"])|add)}'

curl -LfsS "$BASE/MAD_human_labelled_dataset.json" | jq 'length'
curl -fsSI "$BASE/MAD_full_dataset.json" |
  rg -i 'x-repo-commit|x-linked-size|x-linked-etag|x-xet-hash'
```

The observed first command result was `1242, 346, 208, 216, 283`; the second
was `19`. The response headers supplied the pinned revision, byte size, linked
SHA-256, and Xet object identity reported above.

The system-level population is heavily imbalanced:

| MAS | Rows | Any of four positive | None of four |
|---|---:|---:|---:|
| AG2 | 597 | 372 | 225 |
| AppWorld | 30 | 10 | 20 |
| ChatDev | 130 | 80 | 50 |
| HyperAgent | 30 | 10 | 20 |
| Magentic | 195 | 111 | 84 |
| MetaGPT | 230 | 150 | 80 |
| OpenManus | 30 | 10 | 20 |

There are only 206 globally unique `trace_id` values. Ninety composite identity
groups `(mas_name, llm_name, benchmark_name, trace_id)` occur twice. The paired
rows have the same `trace.index` and annotations but distinct trajectory strings,
with no run or replicate field that explains the repetition. They must be
treated as ambiguous repeated identities, not silently deduplicated or assumed
independent.

#### What MAST permits and does not permit

The raw strings can be parsed offline without model or framework execution.
Some expose roles and timestamps, but their formats differ by system. MAST can
therefore support *construction* of an actor/event audit corpus through
system-specific deterministic extractors plus manual adjudication. It does not
support actor/event-level EAG analysis out of the box.

It also cannot establish that evidence was truly available, fresh, authentic,
or causally sufficient merely because text appears earlier in the log. The safe
label for absent or ambiguous telemetry is `indeterminate`. Whole-trace MAST
labels 3.2 and 3.3 are too close to an evidence-quality construct to serve as an
independent primary outcome; using them as both target and validation would be
circular. They can be secondary convergent checks only.

### 2. LoopTrap

LoopTrap defines termination poisoning: the same model consumes untrusted
content and self-evaluates progress, allowing that content to distort its
continue/stop judgment. Its controlled evaluation covers eight model/agent
settings and 60 stratified tasks. The reported adaptive mean step amplification
is 3.57x, with a 25x peak. Its defensive discussion already calls for independent
or sandboxed progress verification and provenance-aware separation.

- Primary paper: <https://arxiv.org/abs/2605.05846>

It establishes the threat and locates authority inside self-evaluation in the
studied ReAct-style loop. Its behavioral “authority profile” is a susceptibility
profile, not an authenticated actor/event authority relation. The paper does not
validate a comprehensive separation defense, cover natural multi-agent
termination traces, or release a reusable event-level corpus on its paper page.

**Ruled out:** “independent progress verification” and “separate untrusted
content from termination judgment” are not novel contributions. No attack
strategy or payload is needed for the proposed diagnostic study.

### 3. IAL-Scan / When Agents Do Not Stop

IAL-Scan statically analyzes 6,549 public Python agent repositories. Its Agent
IR contains execution units, controllers, invocations, state updates, bounds,
and exit records. Its Agentic Loop Dependence Graph represents control, calls,
workflow, tool, handoff, message, and feedback edges. A finding requires a
repeatable path to costly or state-growing work without an effective bound that
covers the path. The paper reports 74 alerts and 68 manually confirmed failures
across 47 projects, or 91.9% precision.

- Primary paper: <https://arxiv.org/abs/2607.01641>

This is the strongest graph/control-coverage neighbor. It structurally locates
which controller governs continuation and whether a bound dominates the
feedback path. It does not observe runtime evidence used to justify a particular
termination event, and its source corpus is not an event-trace dataset. The
paper's limitations include framework/language scope, over-approximation, and
poor visibility into custom schedulers, external stopping, and semantic
natural-language checks. No public code/data artifact was linked from the
official paper page at audit time.

**Ruled out:** EAG must not claim graph-level loop discovery, effective-bound
analysis, or source-code authority localization.

### 4. Agentic Harness Engineering

Agentic Harness Engineering keeps the base model fixed while evolving the
harness. Its three observability layers make components revertible, distill raw
rollouts into an evidence corpus, and bind an edit's declared prediction to the
next round's measured outcome. A ten-iteration campaign reports Terminal-Bench 2
pass@1 rising from 69.7% to 77.0%.

- Primary paper: <https://arxiv.org/abs/2604.25850>
- Official MIT repository:
  <https://github.com/china-qijizhifeng/agentic-harness-engineering>

Its decision authority is the evolution loop deciding which harness edit to
retain or revert. It does not formalize termination authority. The public
repository contains the final evolved harness and trace-conversion code, but no
standardized released campaign trace/evidence corpus was visible at audit time.

**Ruled out:** layered observability, edit–prediction–outcome manifests, and
observability-driven harness evolution are prior art. EAG can borrow the audit
discipline, not claim the concept.

### 5. PCAS/FORGE

The paper titled *Formal Policy Enforcement for Real-World Agentic Systems*
describes the policy-compiler architecture and realizes it as FORGE; FORGE is
the prototype, not a separate paper. It represents execution as a causal DAG of
events such as messages, model calls, tool dispatches/results, inter-agent sends,
and external user messages. A reference monitor authorizes policy-relevant
actions from the complete backward slice using Datalog policies and an
observability service. Identity witnesses are verified outside the model, and
sequence numbers are used so the monitor sees the needed predecessor graph
before deciding.

- Primary paper: <https://arxiv.org/abs/2602.16708>

This is the strongest conceptual neighbor for separating provenance-bearing
evidence from decision authority. Its guarantee is conditional on the
environment soundly and completely populating the causal graph. It evaluates
action authorization, including policies requiring external approval or scan
evidence, not whether an agent is justified in ending its reasoning loop. No
public reusable event-graph corpus or official FORGE repository was linked from
the paper page at audit time.

**Ruled out:** causal evidence graphs, external reference monitors, authenticated
identity witnesses, and evidence/authority separation for action authorization
are not novel. A termination study must treat the stop transition as its distinct
boundary and avoid claiming a new general authorization model.

### 6. Fides / agent information-flow control

Fides separates planning from deterministic policy enforcement. Dynamic
information-flow control propagates confidentiality and integrity labels through
messages, model actions, tool calls, and tool results; consequential tool calls
are checked against policies. Its integrity property prevents untrusted data
from controlling trusted actions under the paper's formal assumptions.

- Primary paper: <https://arxiv.org/abs/2505.23643>
- Official MIT repository: <https://github.com/microsoft/fides>

Fides strongly occupies the generic claim that privileged actions should depend
only on appropriately trusted information. Its protected sink is a consequential
tool action, not a termination transition. The repository offers a tutorial and
implementation, not a released natural execution-trace benchmark for offline
actor/event analysis.

**Ruled out:** deterministic taint enforcement and the generic
trusted-input/privileged-action principle are not EAG novelty.

### 7. AgentRx

AgentRx reports 115 failed trajectories across structured API workflows,
incident management, and open web/file tasks. Human annotations identify the
first unrecoverable critical failure step and a grounded failure category. Its
pipeline normalizes raw logs to a Trajectory IR, synthesizes constraints,
produces checker evidence, and uses a judge for localization.

- Primary paper: <https://arxiv.org/abs/2602.02475>
- Official MIT repository: <https://github.com/microsoft/AgentRx>
- Official dataset card: <https://huggingface.co/datasets/microsoft/AgentRx>

The dataset card is CC-BY-4.0 but gated: access requires login, acceptance, and
sharing contact information. It was not accessed. The public card describes
only two splits, `tau_retail` and `magentic_one`, although the paper/repository
describe three domains including Flash. Its listed row fields are annotations:
trajectory ID, summaries, failures with step and failed agent, and root-cause
fields. The card does not list a raw message/event trajectory field.

AgentRx is the closest evidence-backed diagnostic neighbor for actor/step
localization, but it cannot be the authorized substrate here and does not supply
termination evidence/authority labels.

**Ruled out:** generic critical-step, failed-agent, or root-cause localization is
not novel.

### 8. Temporary Authority, NeuroTaint, and Who&When

#### Temporary Authority

The July 11 paper *Temporary Authority, Permanent Effects* defines commit-time
authorization: a durable effect is authorized only if its licensing witness is
fresh, causally prior, bound to the same effect, and eligible at commit. Its
controlled 54-task matrix explicitly records invalidation, witness state,
binding, dependency order, eligibility, and commit attempts. It therefore owns
the broad “evidence remains valid when the agent finishes” territory.

- Primary paper: <https://arxiv.org/abs/2607.10487>
- Advertised artifact:
  <https://anonymous.4open.science/r/temporary-authority-permanent-changes>

The paper advertises machine-readable manifests and trace-review dossiers, but
the artifact's redirected file endpoint returned HTTP 401 during this audit.
Its contents, schema, license, and row-level reuse fitness could not be verified.
The paper protects durable external effects; it contains no termination-specific
analysis. This preserves only the narrow distinction between *authority to stop
reasoning* and *authority to commit a durable effect*.

The 401 observation was a direct unauthenticated header request on 2026-07-22
(2026-07-21 UTC at the server); it is an access-at-audit-time fact, not a claim
that the artifact will remain unavailable.

#### NeuroTaint

NeuroTaint audits traces offline to reconstruct provenance from untrusted sources
to privileged sinks using semantic transformation, causal influence, and
cross-session persistence. It reports TaintBench with 400 scenarios spanning 20
frameworks.

- Primary paper: <https://arxiv.org/abs/2604.23374>

This eliminates any claim that offline semantic provenance reconstruction from
agent traces is itself new. No code or dataset link was exposed on the official
paper page at audit time. EAG would have to use deterministic extraction and
human reliability evidence, and limit itself to the termination boundary.

#### Who&When

Who&When publicly exposes 184 failed multi-agent trajectories: 126
algorithm-generated and 58 hand-crafted. Its fields include `history`,
`mistake_agent`, `mistake_step`, and `mistake_reason`, so generic actor/step
analysis is possible offline without executing a model or framework.

- Primary paper: <https://arxiv.org/abs/2505.00212>
- Official repository:
  <https://github.com/mingyin1/Agents_Failure_Attribution>
- Public dataset: <https://huggingface.co/datasets/Kevin355/Who_and_When>

The repository is MIT, but the dataset card does not display a dataset license;
the code license must not be assumed to license the data. Who&When can validate
actor/step extraction mechanics or supply a non-distributed calibration study,
but it does not annotate a terminal predicate, decision authority, evidence
provenance, or alignment.

## Dataset fitness answer

### Does a public dataset support actor/event analysis without runtime execution?

**Yes for generic failure attribution, no for the proposed termination EAG
measurement without new work.**

| Source | Public access | Useful observed fields | Direct termination EAG support | Main blocker |
|---|---|---|---|---|
| MAST full JSON | ungated; CC-BY-4.0 | heterogeneous raw trajectory string; 14 whole-trace bits | partial substrate only | no normalized events/actors/authority; denominator drift; repeated IDs |
| MAST human JSON | ungated; CC-BY-4.0 | raw trace plus three annotator booleans | no | 19 rows; incompatible schema; typoed round value |
| Who&When | ungated; license unclear | history, failed actor, decisive step, reason | generic actor/step calibration | no termination predicate or authority/provenance |
| AgentRx | gated; CC-BY-4.0 card | card lists failed actor/step/root-cause annotations | unavailable here | gated; public schema omits raw trajectory field; split mismatch |
| Temporary Authority | paper public; artifact endpoint 401 | paper says boundary witnesses and trace dossiers | conceptually close | row-level artifact/schema/license not inspectable |
| LoopTrap | paper public | aggregate attack outcomes | no | no released trace corpus verified |
| IAL-Scan | paper public | source-level graph and bounds | no runtime evidence | no released event corpus verified |
| AHE | public MIT code | final harness and converters | no | no standardized campaign trace corpus verified |
| PCAS/FORGE | paper public | formal causal-event model | no reusable corpus verified | guarantee depends on instrumentation contract |
| Fides | public MIT code | planner/IFC tutorial | no | implementation, not natural trace data |

MAST is the only authorized, termination-labeled primary substrate in this set.
It is large enough for a stratified offline study, but the unit of analysis and
its EAG fields must be newly derived and reliability-tested. Who&When is an
important falsifier of any claim that actor/step attribution is absent from the
literature.

## Narrowest viable hypothesis shape

A hypothesis should be written only after a schema pilot proves that the
termination locus is recoverable across more than one system. The least
predetermined confirmatory form is an association, not a defense result:

> Among MAST traces with an observable deliberate terminal transition, traces
> labelled 3.1 (premature termination) have a higher prevalence of
> independently coded evidence–authority misalignment at that transition than
> system-and-benchmark-matched traces without any of modes 1.5, 3.1, 3.2, or
> 3.3.

This may fail because the association is null, reverses, or becomes
unidentifiable after `indeterminate` cases are retained. It is not guaranteed by
sampling. Mode 3.1 is preferable to 3.2/3.3 as the primary label because the
latter already encode verification failure and would make an evidence-quality
association close to tautological.

A defensible protocol needs all of the following before review:

1. Pin the MAST revision and checksum above; define repeated-identity handling
   before observing the result.
2. Build separate deterministic parsers per MAS, preserving the source span for
   every extracted event; never silently coerce an unparsed span into an event.
3. Freeze an EAG codebook on a development subset, then annotate a disjoint,
   randomized set while blinded to MAST labels.
4. Define the effective termination authority as the component whose transition
   changes the run from active to terminal, not the actor that merely utters a
   completion claim.
5. Record evidence origin, visibility-to-authority, verification relation,
   temporal order, target/task binding, and dependency coverage separately.
   Do not collapse them into a single score before reliability is established.
6. Use at least four outcomes: `aligned`, `misaligned`, `indeterminate`, and
   `no observable deliberate terminal transition`. Missing telemetry must not
   count as misalignment.
7. Report per-system extractor coverage and annotator agreement before pooled
   association. If one system supplies nearly all codeable cases, withdraw the
   cross-system claim.
8. Match or stratify by MAS and benchmark, and account for repeated composite
   identities. Treat model-family comparison as unavailable in the current
   artifact.
9. Use 3.2/3.3 only for convergent validity, Who&When only for generic
   actor/step calibration, and keep both outside the primary estimand.
10. Phrase all results as corpus associations and observability findings. No
    causal, prevalence, runtime-enforcement, attack-resistance, or defense-
    efficacy claim follows from these observational logs.

### Stop conditions

The pivot should be rejected before a confirmatory hypothesis if the pilot
shows any of the following:

- the effective stop authority or terminal transition cannot be recovered with
  acceptable agreement in at least two materially different MAS formats;
- annotators cannot distinguish `misaligned` from `indeterminate` without using
  MAST's target label;
- source strings omit which evidence was visible to the terminating component;
- parser coverage is label-dependent or dominated by one MAS;
- exact repeated-identity semantics cannot be resolved or safely clustered; or
- the usable sample after observability exclusions is too small for a
  pre-specified matched analysis.

## Claims ruled out by this audit

The following must not appear as contribution claims:

- first discovery of termination poisoning or unbounded agent loops;
- first use of independent progress verification;
- first separation of evidence/provenance from action authority;
- first causal/event graph, graph-aware bound coverage, reference monitor, or
  information-flow enforcement for agents;
- first offline semantic provenance audit of agent traces;
- first actor-and-step failure localization benchmark;
- first observability-driven harness evolution or decision manifest;
- proof that a trace-visible evidence item was authentic, complete, or actually
  used by the terminating runtime;
- a causal claim that misalignment produced a MAST failure;
- a deployment prevalence estimate from the MAST sample; or
- evidence that any defense reduces termination failures.

## Bottom line

The latest literature does not leave room for a broad evidence–authority or
progress-firewall novelty claim. It does leave a small, testable empirical gap:
termination-boundary observability and evidence–authority alignment in existing
natural multi-agent traces, with explicit actor/event localization and an
`indeterminate` state for missing telemetry.

MAST provides enough labelled rows to justify a bounded schema pilot, but not a
ready-made EAG dataset. The artifact mismatch, broken default loader, ambiguous
repeated identities, heterogeneous opaque trajectories, and absent authority
fields are not cleanup details; they are the main scientific risks. Proceed only
if the next work product is a blinded measurement protocol with reliability and
coverage gates. Do not proceed by relabeling MAST's verification bits as new
evidence–authority findings.
