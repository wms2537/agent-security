# Cycle-2 decision archaeology — evolving and attacking the orchestration control plane

**Date:** 2026-07-19 · **Phase:** 1 · **Cycle:** 2 · **Scope:** three verified exemplars

## Why these three

The exemplars were chosen for complementary decisions, not surface similarity:

| Exemplar | Taxonomy | Dominant operation | Transferable decision |
|---|---|---|---|
| Lin et al., *Agentic Harness Engineering* | Resource/Engineering Gap × Optimization/Search | `replace` | Replace opaque manual harness edits with explicit components, compressed trajectory evidence, predicted effects, and rollback. |
| Xu et al., *LoopTrap* | Failure/Risk Gap × Empirical Mapping + Optimization/Search | `formalize` then `expose` | Name termination poisoning as a control-flow threat, measure its conditional surface, then show why adaptive search changes the evaluation. |
| Nöther et al., *MaMa* | Failure/Risk Gap × Robustification/Optimization | `replace` | Replace task-only system design with a designer–adversary game and evaluate safety under changed threats. |

Together they trace the exact tension in the candidate project: the harness is
becoming an optimizable artifact, its loop is becoming an attack target, and a
security-aware optimizer already exists. A valid new contribution must therefore
test a relation these works do not: whether security is invariant under declared
function-preserving orchestration rewrites.

## Evidence and limits before imitation

- AHE's arXiv record matches 11 authors. Its abstract reports Terminal-Bench 2
  pass@1 69.7%→77.0% over ten iterations and 12% fewer tokens than the seed on
  SWE-bench-verified. Its stated limitations include benchmark/model dependence,
  prototype status, and incomplete self-modification guardrails.
- LoopTrap's arXiv HTML matches seven authors. The main controlled study uses 10
  strategy families, eight agents, and 60 tasks; static prompts average 2.33×
  step amplification, while its adaptive system averages 3.57× with a 25× peak.
  Main experiments use simulated tool returns, and comprehensive defenses are
  explicitly unvalidated.
- MaMa's arXiv HTML matches three authors and six environments. Its targeted
  attack table reports lower ASR than the least-privilege/tool-filter and
  Guardian-Agent baselines in all four listed environments; the method relies on
  LLM-based adversarial search and safety/quality judges, so it cannot certify an
  undiscovered attack or judge blind spot away.

No operational attack prompt or exploit implementation is copied from the
exemplars. Their numbers are used only to reconstruct scientific choices.

## Decision reconstruction

### Agentic Harness Engineering

**Observed problem.** Harness performance mattered, but the editable surface was
heterogeneous, trajectories were too large for direct inspection, and outcome
changes were hard to attribute.

**Decision.** The authors made three kinds of observability match those three
bottlenecks: components become file-level and revertible; trajectories become a
layered evidence corpus; proposed edits become falsifiable predictions checked
against the next evaluation.

**Why this worked.** It bounded the mutation surface and recorded causal intent.
An autonomous optimizer could change the harness without erasing the reason for
the change or making rollback impossible.

**What it did not solve.** Low self-attribution precision shows that declaring a
prediction does not make it correct. AHE also optimizes benchmark outcomes, not
a fixed external security invariant. Its method is therefore an exemplar for
mutation observability, not proof of safe self-evolution.

### LoopTrap

**Observed problem.** Prompt-injection work focused on outputs and unauthorized
actions, while agent autonomy depended on a progress signal that determines
whether execution continues.

**Decision.** The paper changed the dependent variable from harmful output to
step/token amplification, treated model and task context as conditioning
variables, and compared static with adaptive red-team search in a contained
simulated environment.

**Why this worked.** It made the attacked object—termination judgment—legible as
control flow. Conditional results prevented one universal-prompt story, and the
adaptive study showed that a fixed corpus understates an optimizing adversary.

**What it did not solve.** It leaves defense as future work. Its proposed
independent progress verifier and provenance separation are plausible but not
validated, especially against a defense-aware adversary. The main unified ReAct
harness also leaves multi-agent propagation open.

### MaMa

**Observed problem.** Automated agent-system search optimized task performance,
while compromised constituents could exploit the chosen communication and tool
structure.

**Decision.** The authors turned system design into a Stackelberg-inspired game:
a Meta-Agent proposes agents, tools, and communication; a Meta-Adversary searches
for damaging compromises; the archive carries designs, attacks, safety, and
quality into the next iteration.

**Why this worked.** Safety became part of system search rather than a post-hoc
filter. Transfer tests changed adversary strength, model, objective, and attack
delivery, giving more evidence than an in-distribution win.

**What it did not solve.** LLM adversarial search is not a best-response oracle,
and judge scores are not immutable safety invariants. The method asks which
design wins its game; it does not ask whether two nominally function-preserving
representations of one design preserve security.

## Exemplar move table — Introduction

| Exemplar | Move | Evidence type | Opening function | Closing function | Why it works |
|---|---|---|---|---|---|
| AHE | Turn manual harness craft into three matched observability failures | Engineering bottlenecks + trajectory scale | Establish harness centrality | Promise an autonomous closed loop with falsifiable edits | Each method pillar answers a named failure rather than reading as a stack. |
| LoopTrap | Move prompt injection from output content to termination control | Threat-model contrast + production consequence | Describe the ordinary reason–act–evaluate loop | Name termination poisoning as a new dependent variable | The attacked decision is concrete and different from classic jailbreak output. |
| MaMa | Contrast task-only automated design with compromised-agent risk | Prior system-search success + stronger threat model | Grant the capability gains | Reframe design as a designer–adversary game | It does not reject automated design; it changes the objective under a precise threat. |

## Exemplar move table — Method

| Exemplar | Move | Evidence type | Opening function | Closing function | Why it works |
|---|---|---|---|---|---|
| AHE | Make every editable component explicit and revertible | Representation contract | Bound what the optimizer may change | Enable exact diff and rollback | Auditability is structural, not a prose promise. |
| AHE | Compress trajectories into layered evidence | Observability pipeline | Admit raw traces exceed review capacity | Supply drill-down evidence to the editor | Compression is tied to an explicit consumption constraint. |
| AHE | Pair each edit with predicted consequences | Prospective decision record | Expose causal intent before results | Compare prediction with the next round | Prevents outcome-only hill climbing from masquerading as understanding. |
| LoopTrap | Define step amplification relative to benign execution | Paired metric | Establish a per-task baseline | Quantify control-flow distortion | The ratio isolates prolongation better than final success. |
| LoopTrap | Profile contextual susceptibility before adaptive search | Conditional empirical map | Reject one-size-fits-all attack assumptions | Route later search by observed tendencies | The adaptive method follows measured heterogeneity. |
| MaMa | Formalize designer commitment and adversary response | Game model | Define safety under compromised agents | Motivate alternating design and attack search | The optimizer and threat model share one objective structure. |
| MaMa | Preserve systems and strongest attacks in an archive | Iterative algorithm | Retain prior evidence | Select on safety plus quality | The next design can respond to known failures without forgetting prior utility. |

## Exemplar move table — Experimental setup

| Exemplar | Move | Evidence type | Opening function | Closing function | Why it works |
|---|---|---|---|---|---|
| AHE | Evaluate iterative improvement, frozen transfer, and component ablation | Benchmark rounds + cross-family tests | Measure the evolution path | Separate transferable structure from prompt prose | It tests both the process and the resulting artifact. |
| LoopTrap | Pair benign and injected runs in simulated tool environments | Controlled sandbox protocol | Remove live-service variance and collateral effects | Attribute amplification to the threat condition | Containment improves both safety and causal clarity. |
| LoopTrap | Compare static, routed, reflective, and skill-reuse variants | Baselines + ablations | Define finite attack-search budgets | Attribute adaptive gains | The paper measures which search components matter rather than reporting one endpoint. |
| MaMa | Compare initial systems, task-only search, existing guards, and MaMa | Safety/quality baselines | Establish strong task and security controls | Show whether adversarial feedback adds value | The comparison directly tests the new objective, not just final architecture. |
| MaMa | Change adversary model, strength, objective, and delivery | Transfer tests | Leave the training threat | Probe robustness to threat shift | “Safe” is not inferred from one attacker distribution. |

## Exemplar move table — Results and figures

| Exemplar | Move | Evidence type | Opening function | Closing function | Why it works |
|---|---|---|---|---|---|
| AHE | Plot outcome across all ten iterations | Evolution curve | Show the seed | Preserve non-monotonic edit history | The process remains visible instead of only the winning harness. |
| AHE | Report low prediction precision beside performance gains | Calibration/negative evidence | Test claimed decision observability | Bound causal interpretation | Observability is not confused with accurate self-attribution. |
| LoopTrap | Report task/model interaction before adaptive headline | Stratified heatmaps | Establish heterogeneous vulnerability | Motivate profiling | The mechanism for adaptation appears before its score. |
| LoopTrap | Show convergence and component ablations under one budget | Cumulative ASR + ablations | Compare learning dynamics | Separate profiling, reflection, reuse, and exploration | The adaptive claim survives component removal tests. |
| MaMa | Track safety and quality over design generations | Two-objective curves | Show initial design | Compare with task-only and guard baselines | Makes the alignment tax and improvement path visible together. |
| MaMa | Report changed-threat results after main performance | Transfer tables | Leave the optimization game | State where robustness breaks as compromised agents increase | The claim ends at an observed operating boundary. |

## Exemplar move table — Discussion and limitations

| Exemplar | Move | Evidence type | Opening function | Closing function | Why it works |
|---|---|---|---|---|---|
| AHE | Name model/benchmark fit, attribution weakness, and incomplete self-modification safety | Stated limitations | Bound autonomous-evolution claims | Define the next governance problem | Limitations follow the exact mechanisms used. |
| LoopTrap | Separate threat characterization from unvalidated defense | Explicit scope boundary | Admit the contribution is offensive measurement | Propose independent progress/provenance defenses | The paper does not represent suggestions as results. |
| MaMa | Test stronger adversaries and expose quality tax | Threat-shift results | Challenge the learned design | Show degradation when adversarial control dominates | Robustness is conditional, not absolute. |

## Transfer to the recommended direction

The Orchestration Metamorphic Security Testing direction should transfer six
decisions:

1. From AHE, make every graph component and rewrite an explicit, versioned,
   revertible artifact.
2. From AHE, preregister the expected invariant before observing the paired
   result; do not infer the intended relation after a surprising failure.
3. From LoopTrap, make control-flow outcomes—steps, terminal state, capability
   use, and provenance—first-class, not only final text.
4. From LoopTrap, use paired contained replay and a defense-aware evaluation
   model; do not publish operational attack content.
5. From MaMa, score utility and security together and test outside the exact
   graph/framework condition used to construct the method.
6. Unlike all three, mechanically validate the declared graph equivalence before
   interpreting security non-invariance. Similar benign accuracy is not proof of
   equivalent orchestration semantics.

## What must not be imitated

- Do not turn AHE's three observability pillars into an arbitrary component
  stack; each added mechanism needs an independently testable failure.
- Do not reproduce LoopTrap payloads or mistake adaptive red-team success for an
  authorized live test.
- Do not call LLM-based adversarial search a true best response or an LLM safety
  score an invariant.
- Do not claim a graph rewrite is semantics-preserving because a small benign
  sample happens to tie.

These move tables guide scientific design only. They do not authorize Phase 2,
an attack implementation, a new experiment, or any Kaggle action.
