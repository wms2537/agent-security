# Cycle-2 Phase-1 literature map — orchestration as capability and attack surface

**Date:** 2026-07-19 · **Phase:** 1 · **Cycle:** 2 · **Iteration:** 5  
**Scope:** primary-source literature available in July 2026; defensive analysis only

## Boundary and question

This search asks whether the recent progression from prompt engineering to
harness engineering, loop engineering, and graph/orchestration engineering
creates a distinct scientific security problem: **how should an agent runtime
structure, observe, test, and govern a changing graph of models, tools, memory,
verification, retries, and handoffs?**

The review does not execute, reproduce, or optimize any attack. It does not open
a Kaggle surface, held-out set, beacon, private evaluator, or live target. Attack
papers are treated as defensive evidence about failure surfaces. No prompt
payloads or operational attack procedures are retained here.

The source databases are:

- `research-log/lit/arxiv_orchestration_2026.json`: 14 papers and 9 search
  records.
- `research-log/lit/primary_agent_security_2026.json`: 12 papers and 48 search
  records.
- `research-log/lit/primary_jailbreaks_2026.json`: 10 papers and 10 search
  records.

The 67 search records are dated 19–20 July because the work crossed the
UTC/Asia-Kuala-Lumpur date boundary. Each source track stayed below SciAgent's
15-paper-per-searcher ceiling. All 36 retained entries have high relevance; 25
form the core synthesis and 11 are explicitly dismissed from the load-bearing
set below.

## Terminology resolution: Fable 5

The user-mentioned term is exact: **Claude Fable 5** is the model, not the name
of an attack and not a spelling correction. Anthropic's first-party account
describes a reported cybersecurity-safeguard bypass, a deployment interruption,
comparative reproduction, and a targeted classifier update
([incident disclosure](https://www.anthropic.com/news/redeploying-fable-5)).

The evidence must not be collapsed into one claim:

- Anthropic reports that its targeted update blocks the reported technique in
  more than 99% of cases and that it knew of no universal Fable 5 jailbreak at
  the time. This is a provider-authored incident report, not independent raw
  evaluation.
- Anthropic's follow-up draft defines a five-band Cyber Jailbreak Severity scale
  using capability gain, breadth, ease of weaponization, and discoverability;
  zero capability gain makes a bypass informational
  ([framework](https://www.anthropic.com/news/fable-safeguards-jailbreak-framework)).
- A separate single-author arXiv white paper reports worst adaptive attack
  success of 6.1% for Fable 5 and 11.5% for Opus 4.8 over 7,826 intents, with
  model-panel adjudication ([arXiv:2606.18193](https://arxiv.org/abs/2606.18193)).
  This is lower-tier evidence than a peer-reviewed study and does not measure
  marginal capability uplift.

The important scientific lesson is not a vendor-specific jailbreak score. It is
that **bypass frequency, retained capability, marginal capability uplift, ease
of discovery, and operational harm are different variables**. Raw ASR is not a
complete severity measure.

## Verification record

After the source files reached their final sizes, the required random sample was
drawn with these exact commands:

```text
jq -r '.papers[].title' research-log/lit/arxiv_orchestration_2026.json | shuf -n 2
Why Do Multi-Agent LLM Systems Fail?
MASEval: Extending Multi-Agent Evaluation from Models to Systems

jq -r '.papers[].title' research-log/lit/primary_agent_security_2026.json | shuf -n 2
MaMa: A Game-Theoretic Approach for Designing Safe Agentic Systems
Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents

jq -r '.papers[].title' research-log/lit/primary_jailbreaks_2026.json | shuf -n 2
LoopTrap: Termination Poisoning Attacks on LLM Agents
Best-of-N Jailbreaking
```

Checks against primary pages:

- Cemri et al.: arXiv matches title and 13 authors; the abstract reports more
  than 1,600 annotated traces, 14 failure modes, three categories, and Cohen's
  kappa 0.88.
- Emde et al.: ACL Anthology matches the seven authors and July 2026 venue; the
  abstract reports a 3-benchmark × 3-model × 3-framework comparison.
- Nöther et al.: arXiv HTML matches the three authors; the paper evaluates six
  environments. A representative targeted-attack table reports MaMa ASR 0.1700
  versus 0.5646 for least-privilege/tool-filter controls in Travel Planning,
  with the paper's own judge- and threat-model limitations retained.
- Bazinska et al.: arXiv HTML matches the seven authors and reports 194,331
  unique crowdsourced attacks evaluated across 34 LLMs. The paper deliberately
  isolates backbone states rather than full orchestration.
- Xu et al.: arXiv HTML matches the seven authors and reports 10 strategy
  families, eight agents, 60 tasks, mean 3.57× step amplification for LoopTrap,
  and a 25× peak. Only the defensive aggregate and stated limitations are used.
- Hughes et al.: arXiv matches the title/authors and reports 89% ASR on GPT-4o
  and 78% on Claude 3.5 Sonnet at 10,000 augmented samples.

Additional load-bearing checks covered Agentic Harness Engineering, MASS,
Adaptive Test-Time Compute Allocation, AgentDojo, ToolEmu, ASB, ControlValve,
Tool-Guard, both Anthropic disclosures, FlowSteer, and infinite-agent-loop
static analysis. No numerical claim from a low-confidence extraction is used as
a premise for a candidate direction.

## What changed: four layers, not four slogans

| Layer | Engineering object | Capability it adds | Security consequence |
|---|---|---|---|
| Prompt/context | Instructions and per-call information | Better local reasoning and tool selection | Content can blur trusted instruction and untrusted data. |
| Harness | Tools, memory, middleware, permissions, state, evaluation | Reproducible and governable execution around a fixed model | Metadata, memory, and capability bindings become supply-chain and privilege surfaces. |
| Loop | Repeated reason–act–observe–verify–recover–stop control | Adaptation over an unfolding trajectory | Feedback, retries, verification, and termination can be poisoned or amplified. |
| Graph/orchestration | Roles, edges, routing, topology, protocols, and conditional branches | Task-specific division of labour and dynamic resource allocation | The control plane itself can be steered, hijacked, or evolved into an unsafe configuration. |

These are nested. A graph is not a replacement for a harness; it is an explicit
representation of how harness components and agent loops interact. A useful
runtime graph needs more than agent-to-agent message edges. It needs trusted and
untrusted data provenance, capability/permission edges, state transitions,
verification gates, retry and rollback semantics, budgets, and terminal/error
states.

The July 2026 long-horizon survey makes this decomposition unusually explicit.
It formalizes `Agent = policy + harness`, identifies six external harness
components—loops/workflows, context/memory, tools/skills, orchestration,
hooks/middleware, and verification—and frames progress as co-evolution between
that external harness and model optimization
([Dong et al., 2026](https://www.preprints.org/manuscript/202607.1328)). Its 149-page
manuscript was checked through the authors' official GitHub/OpenReview links.
It is only a two-day-old, non-peer-reviewed survey, so its taxonomy is useful
framing rather than empirical proof.

## Orchestration capability evidence

The performance literature establishes that the system, not just the model,
matters:

- GPTSwarm represents prompts and agent connectivity as an optimizable
  computational graph ([ICML 2024](https://arxiv.org/abs/2402.16823)).
- G-Designer learns communication topology and reports strong accuracy with
  major token reduction, demonstrating that topology changes both utility and
  resource use ([ICML 2025](https://arxiv.org/abs/2410.11782)).
- MASS jointly searches prompts and topologies; its results make task-specific
  system design a serious baseline rather than a hand-crafted anecdote
  ([ICLR 2026](https://arxiv.org/abs/2502.02533)).
- The scaling study spans 260 configurations and finds effects from −70.0% to
  +80.8%, warning that adding agents or choosing one topology is not uniformly
  helpful ([Kim et al., 2025](https://arxiv.org/abs/2512.08296)).
- MASEval treats the whole framework configuration as the unit of analysis; one
  reported framework gap is 30.9 points and one trace repeats a clarification
  tool 23 times ([ACL 2026](https://aclanthology.org/2026.acl-demo.34/)).
- Agentic Harness Engineering turns harness components, trajectories, predicted
  edits, outcomes, and rollback into an autonomous evolution loop. Ten rounds
  move Terminal-Bench 2 pass@1 from 69.7% to 77.0%, but self-attribution remains
  low-precision and the prototype's self-modification guardrails are incomplete
  ([Lin et al., 2026](https://arxiv.org/abs/2604.25850)).

The negative literature matters as much as the gains. MAST identifies 14 failure
modes, including repetition, failure to recognize completion, and verification
errors ([Cemri et al., 2025](https://arxiv.org/abs/2503.13657)). Adaptive
test-time allocation reports gains over uniform budgets
([Zhai et al., 2026](https://arxiv.org/abs/2604.14853)), but AgentStop and semantic
early stopping already occupy the generic “predict failure and stop early” idea
([AgentStop](https://arxiv.org/abs/2605.15206),
[semantic stopping](https://arxiv.org/abs/2606.27009)). The long-horizon survey
also explicitly calls for mid-run shortening, rerouting, stopping, and early
path-switching. Therefore a broad adaptive-stopping contribution is already
crowded.

## Recent attacks mapped to the system layer

### 1. Model-policy bypass and attack-compute scaling

Best-of-N shows that repeated black-box sampling turns attack budget into a
first-class variable. Adaptive attacks against eight indirect-prompt-injection
defenses keep success above 50%, demonstrating why a static defense benchmark is
not an adaptive robustness claim
([Zhan et al., 2025](https://arxiv.org/abs/2503.00061)). The Fable disclosures
add a crucial severity distinction, but remain primarily model/safeguard
evidence rather than orchestration evidence.

### 2. Tool metadata, memory, and capability supply chain

AgentPoison reports at least 80% attack success with less than 0.1% poisoned
memory/knowledge content and at most 1% benign impact
([NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/eb113910e9c3f6242541c1652e30dfd6-Abstract-Conference.html)).
MCPTox moves tool-description poisoning to authentic MCP-server metadata, while
Tool-Guard isolates planning evidence and validates calls before execution
([MCPTox](https://arxiv.org/abs/2508.14925),
[Tool-Guard](https://arxiv.org/abs/2606.20922)). These works show that tool
availability is not enough; provenance and pre-action isolation belong in the
harness contract.

### 3. Loop and termination control

LoopTrap defines termination poisoning: untrusted content corrupts progress
assessment and prolongs execution. Its static study averages 2.33× step
amplification; its adaptive red-team system averages 3.57× and explicitly leaves
robust defense unvalidated. The paper proposes independent sandboxed progress
verification and provenance-aware context handling as future work
([Xu et al., 2026](https://arxiv.org/abs/2605.05846)).

Independently, IAL-Scan analyzes 6,549 public agent repositories and confirms 68
infinite-agent-loop findings across 47 projects at 91.9% precision
([Hou et al., 2026](https://arxiv.org/abs/2607.01641)). This is static detection,
not exploitability, prevalence, recall, or a learned runtime defense. Together,
the two papers establish complementary dynamic-adversarial and static-structural
views of the loop surface.

### 4. Planning graph and control-flow manipulation

FlowSteer attacks planning-time workflow formation rather than only message
content, increasing malicious success by up to 55% over naive prompting in its
settings; FlowGuard reduces it by up to 34%
([Li et al., 2026](https://arxiv.org/abs/2605.11514)). Control-flow-hijacking work
reports 83–100% success on undefended coding templates, failures of semantic
defenses under adaptation, and zero success for its permitted-control-flow
ControlValve in the tested templates
([Jha et al., ICLR 2026](https://arxiv.org/abs/2510.17276)).

This is the decisive shift: an attacker can optimize not only text, but **which
agents act, which edge carries authority, how long the loop runs, and what state
is persisted**.

### 5. Automated system design and audit graphs

MaMa already treats safe agent-system design as an adversarial optimization game
and evaluates transfer to altered threats
([Nöther et al., 2026](https://arxiv.org/abs/2602.04431)). Agent-BOM already
represents static capabilities and dynamic semantic states as an attributed
graph for post-hoc security queries
([Li et al., 2026](https://arxiv.org/abs/2605.06812)). These papers make a generic
“optimize a safe graph” or “build a security graph” contribution non-novel.

## Cross-paper synthesis

Three conclusions survive the novelty audit.

1. **The orchestrator is both optimizer and attack target.** Performance work
   makes prompts, topology, routing, and budgets learnable. Security work shows
   the same degrees of freedom can be poisoned. Improving orchestration expands
   the control plane that must be governed.
2. **Trust separation is the missing graph primitive.** Many current graphs
   encode information flow but not why an edge is trusted, which capability it
   confers, what provenance it carries, which invariant guards it, or whether an
   independent component may terminate it.
3. **Evaluation needs relations, not only point scores.** A single ASR, utility,
   or cost number cannot tell whether a supposedly neutral framework/graph
   change silently alters security. MASEval shows framework effects; FlowSteer
   shows planning sensitivity; Agent-BOM supplies a graph vocabulary. A direct
   test of security invariance under controlled orchestration rewrites is not
   represented in the reviewed primary literature.

## Core-set placement and unused-paper sweep

The core synthesis intentionally stops at 25 papers. Every other high-relevance
entry is dismissed explicitly rather than silently dropped.

### Core 25

| Work | Placement |
|---|---|
| GPTSwarm | Foundational graph-as-optimizable-system evidence. |
| G-Designer | Learned topology and efficiency evidence. |
| MASS | Joint prompt/topology search baseline. |
| Why Do Multi-Agent LLM Systems Fail? | Failure taxonomy and completion/verification surface. |
| Towards a Science of Scaling Agent Systems | Negative and task-conditional scaling evidence. |
| MASEval | Whole-system evaluation and framework confounding. |
| Agentic Harness Engineering | Auditable, versioned harness evolution exemplar. |
| Adaptive Test-Time Compute Allocation | Formal budget-allocation neighbor. |
| Towards Long-Horizon Agents | Current field taxonomy and explicit frontier-crowding source. |
| Semantic Early-Stopping | Strongest paired-replay counter-neighbor to generic stopping. |
| AgentDojo | Security–utility benchmark substrate. |
| Agent Security Bench | Broad multi-scenario attack/defense context. |
| AgentPoison | Persistent memory/knowledge poisoning surface. |
| DoomArena | Dynamic threat evaluation and ranking reversal. |
| ControlValve | Explicit permitted-control-flow defense. |
| Tool-Guard | Pre-action validation and isolated planning. |
| MaMa | Closest automated safe-system-design competitor. |
| Agent-BOM | Closest security-audit graph representation. |
| Redeploying Claude Fable 5 | Exact incident identity and provider evidence. |
| Fable safeguards/jailbreak framework | Bypass-versus-capability-uplift distinction. |
| Best-of-N Jailbreaking | Attack-budget scaling. |
| Adaptive Attacks Break Defenses | Adaptive-evaluation requirement. |
| FlowSteer | Planning-time graph steering. |
| When Agents Do Not Stop | Static graph evidence for unbounded loops. |
| LoopTrap | Direct termination-poisoning evidence and open defense gap. |

### Eleven explicitly not load-bearing

| Work | Reason not used as a core premise |
|---|---|
| DyLAN | Useful dynamic-routing history, but MASS/G-Designer and the scaling study provide closer graph comparators. |
| AgentSquare | Modular search is redundant with stronger joint-search/evolution neighbors. |
| AFlow | Important ancestor, but AHE and MaMa more directly cover the new optimization and safety questions. |
| AgentStop | Establishes generic predictive stopping, used only to reject novelty rather than support the chosen gap. |
| InjecAgent | Earlier static indirect-injection benchmark; AgentDojo and ASB supply broader system evaluation. |
| ToolEmu | Establishes generic agent risk in simulation but does not isolate orchestration security. |
| Breaking Agent Backbones | Isolates model-level threat snapshots by design, whereas the target question is the surrounding runtime. |
| MCPTox | Relevant MCP context, but Tool-Guard supplies the more direct defensive mechanism and tradeoff. |
| Fable 5/Opus 4.8 red-team white paper | Quantitative context only; single-author preprint and model-judge dependence make it non-load-bearing. |
| Jailbroken Frontier Models Retain Their Capabilities | Separates capability retention from ASR but is model-side rather than orchestration-side. |
| Action-Graded Severity Scale | Very recent single-author neighbor used to reject a generic beyond-ASR project; not mature enough to anchor graph claims. |

## Candidate directions

Scores are 1–5. The weighted total is 25% novelty, 25% importance, 20%
feasibility, 20% falsifiability, and 10% safe reproducibility.

### A. Orchestration Metamorphic Security Testing — recommended

**Question.** When two runtime graphs are equivalent under a declared benign
operational semantics, are their security outcomes invariant under controlled
graph rewrites?

The method would define a small, executable agent intermediate representation
and a library of validated rewrites, such as alpha-renaming, reordering
independent deterministic gates, identity relays, and bisimulation-preserving
state splits/merges. Each rewrite must preserve declared task inputs, tool
capabilities, and terminal semantics. Paired replay would then test whether
attack resistance, action severity, utility, and cost change beyond stochastic
rerun variance.

This is **Evidence Gap × Empirical Mapping**, dominated by `formalize` and
`decouple`: formalize graph-level metamorphic relations, then decouple security
effects from intended functional changes.

| Dimension | Score | Critique |
|---|---:|---|
| Novelty | 4.5 | Metamorphic testing exists for LLMs, but the reviewed primary set does not test security invariance under validated orchestration-graph rewrites. |
| Importance | 4.3 | Directly tests whether graph engineering creates hidden trust-boundary regressions. |
| Feasibility | 4.0 | Can begin with a restricted IR and public sandbox traces; semantic-equivalence validation is the hard part. |
| Falsifiability | 4.6 | No excess paired security variance, or failure to validate rewrites, rejects the central claim. |
| Safe reproducibility | 4.8 | Can use inert/simulated tools, existing public traces, and non-operational attack labels. |
| **Weighted total** | **4.40** | Best balance of originality, direct graph relevance, and bounded empirical risk. |

**Fatal failure mode:** calling rewrites “equivalent” merely because benign
accuracy is similar. The equivalence contract must be mechanically checked at
the harness level before security differences are interpreted.

### B. Provenance-Decoupled Progress Firewall

**Question.** Can an independent progress controller, denied access to raw
untrusted content and restricted to attested task-state transitions, prevent
termination poisoning without the utility loss of hard step caps?

The controller would see a structured ledger of goals, completed obligations,
tool-result attestations, repeated-state hashes, and budget—not the raw document
or web text consumed by the worker. Its actions would be continue, request an
independent check, escalate, or stop. Evaluation must be adaptive-aware and
matched on task utility and cost.

This is **Failure/Risk Gap × Robustification** with operation `replace`: replace
self-evaluated continuation with an independently grounded gate.

| Dimension | Score | Critique |
|---|---:|---|
| Novelty | 3.6 | LoopTrap explicitly proposes independent progress verification and provenance separation, so novelty lies only in a rigorous architecture and adaptive evaluation. |
| Importance | 4.8 | Direct defense for a measured 2026 control-flow attack. |
| Feasibility | 4.3 | Narrow action space and public simulated settings make a prototype plausible. |
| Falsifiability | 4.7 | Failure under adaptive evaluation or worse security–utility–cost tradeoff than hard caps rejects it. |
| Safe reproducibility | 4.5 | Requires careful handling of attack traces but no live targets or operational payload release. |
| **Weighted total** | **4.35** | Highest immediate defensive value, but a thinner novelty margin. |

**Fatal failure mode:** the supposedly independent controller indirectly sees
the poisoned content through summaries or model-generated progress fields. The
trusted computing base and provenance boundary must be explicit.

### C. Invariant-Preserving Harness Evolution

**Question.** Do task-score-driven harness mutations accumulate security debt
across versions, and can a fixed independent mutation-acceptance gate prevent
regressions without freezing useful evolution?

This would version each graph delta, evaluate task utility and invariant checks,
and accept a mutation only when it is non-dominated under a predeclared safety
contract. Unlike a co-evolving self-judge, the invariant verifier and its test
lineage would remain outside the mutation surface.

This is **Failure/Risk Gap × Robustification/Optimization** with operation
`replace`: replace task-only or jointly judged mutation selection with an
independent invariant-preserving acceptance rule.

| Dimension | Score | Critique |
|---|---:|---|
| Novelty | 3.5 | The long-horizon survey names invariant-preserving evolution, and MaMa already optimizes safety and utility; the longitudinal fixed-verifier distinction must carry the contribution. |
| Importance | 4.7 | Self-evolving harnesses could otherwise institutionalize poisoned skills, permissions, or topology. |
| Feasibility | 3.2 | Requires a credible mutation corpus, stable invariants, and non-toy evolution runs. |
| Falsifiability | 4.1 | No security-debt trend, or no incremental benefit over MaMa/static gates, rejects the direction. |
| Safe reproducibility | 4.4 | Can be sandboxed, but automated mutation increases containment and provenance burden. |
| **Weighted total** | **3.95** | Ambitious and relevant, but currently the highest execution and novelty risk. |

**Fatal failure mode:** presenting AHE plus a static security test suite as a new
method. The contribution must isolate longitudinal drift and a principled
acceptance rule, not stack familiar components.

## Rejected easy directions

- **Generic adaptive stopping:** already crowded by AgentStop, semantic early
  stopping, adaptive compute allocation, the long-horizon survey, and LoopTrap.
- **Generic safe graph optimization:** MaMa directly occupies it.
- **Generic security audit graph:** Agent-BOM directly occupies it.
- **Generic beyond-ASR severity:** Anthropic's CJS framework, Expected Harm, and
  the July 2026 action-graded severity paper already occupy adjacent ground.
- **“Fable 5 jailbreak” as a standalone paper:** the term names a model incident,
  the public evidence is provider-heavy, and reproducing a live bypass is neither
  necessary nor authorized.

## Phase-1 checkpoint recommendation

Advance **Candidate A, Orchestration Metamorphic Security Testing**, to Phase 2
only if the user selects it. Candidate B is the best alternative if immediate
defensive impact is valued over the stronger originality margin. Candidate C
should not advance without first proving that its longitudinal distinction is
not subsumed by MaMa.

No hypothesis, experiment, attack execution, or Kaggle action is authorized by
this map. Phase 1 remains open pending user direction.
