# ORF Phase-6 decision archaeology and exemplar move tables

**Date:** 2026-07-19 · **Phase:** 6 · **Scope:** three closest exemplars from the verified five-paper freshness set

## Verification before imitation

The citation database is `research-log/lit/phase6-primary.json`: five opened
primary papers, five `reviewed=yes`, five `reference_verification=verified`,
zero critical field mismatches, and two recorded version/title warnings. Four
records were checked against authoritative arXiv author records; Snell et al.
was additionally checked against the ICLR proceedings record; the SCALE record
was checked field-by-field against Crossref and the AAAI proceedings page.

The required random existence-and-number spot check was selected with:

```text
jq -r '.papers[].title' research-log/lit/phase6-primary.json | shuf -n 2
Learning When to Plan: Efficiently Allocating Test-Time Compute for LLM Agents
Scaling LLM Test-Time Compute Optimally Can be More Effective than Scaling Parameters for Reasoning
```

- **Paglieri et al.**: the arXiv v3 record matches title and nine authors. The
  full PDF reports the 8B dynamic-planning agent at reward 0.387 versus 0.379
  for the 70B zero-shot comparator while using 85% fewer tokens (§5.3), and the
  figure caption states 100 seeds for the zero-shot environments.
- **Snell et al.**: ICLR and arXiv records match the four authors. The abstract
  and introduction report up to fourfold lower compute than best-of-N in the
  selected regimes and a FLOPs-matched comparison with a 14-times-larger model.

No extracted number from an unreviewed or low-confidence entry is used.

## Why these exemplars

The three exemplars occupy increasingly agentic versions of ORF's decision:

| Exemplar | Taxonomy tag | Why it is structurally useful |
|---|---|---|
| Snell et al., 2025 | Puzzle/Contradiction × Empirical Mapping; dominant operation `formalize` | Starts from mixed scaling outcomes, stratifies by a conditioning variable, and converts the heterogeneity into an allocation policy while preserving hard limits. |
| Paglieri et al., 2026 | Resource Bottleneck × Optimization/Search; dominant operation `replace` | Replaces always/never planning with a learned conditional decision and exposes failed instruction/reward-shaping routes rather than sanitizing them. |
| Li et al., 2026 (BAVT) | Failure/Risk Gap × Optimization/Search; dominant operation `replace` | Opens with wasted tool budgets, isolates each control component by ablation, and closes with concrete operating-envelope limitations. |

ORF itself remains Evidence Gap × Empirical Mapping with operation `replace`:
replace a shared fill-length argmax with profile-conditioned argmaxes and measure
the exact finite value of that relaxation. The exemplars are used for rhetorical
decisions, not to imply equivalence of methods, metrics, or evidence strength.

## Decision reconstruction

### Snell et al.

The authors' central decision was to reject one aggregate scaling curve as the
scientific object. Mixed prior results suggested an interaction among prompt
difficulty, model capability, strategy, and budget. They therefore used a
model-specific difficulty statistic, compared allocation strategies within a
fixed compute envelope, and made the per-prompt choice the contribution. The
load-bearing assumption is that difficulty predicts the relevant strategy.
They openly retain limits: difficulty estimation costs compute, the hardest
questions gain little, and specialized revision/verifier training was needed.

### Paglieri et al.

The paper frames fixed planning frequency as the wrong action scope, then asks
whether the decision to plan can be learned inside one agent. SFT priming was
chosen because RL alone tends to refine existing behaviors rather than create a
planning mode. Two abandoned routes—natural-language frequency instructions and
explicit planning penalties—are scientifically important: one collapsed into
fixed patterns, the other suppressed planning. This journey is the closest
exemplar for ORF's necessary admission that oracle value is not learnability.

### Li et al. (BAVT)

BAVT begins with a measured failure surface: trajectory-level controls waste
tool and token budgets on dead ends. The method then maps one component to each
bottleneck: a tree enables alternatives, a residual critic estimates marginal
progress, and remaining budget changes selection. The ablation is decisive:
random tree structure hurts, the critic helps, and budget conditioning adds the
resource-aware control. The authors also state that critic overhead and uniform
single-tool costs limit deployment claims. This is the exemplar for ORF's OAT
results and its need to keep the no-live-transfer boundary close to the result.

## Exemplar Move Table — Introduction and Abstract

| Exemplar | Paragraph | Move | Evidence Type | Opening Function | Closing Function | Notes on why this move worked |
|---|---|---|---|---|---|---|
| Snell | Abstract + Intro ¶1-3 | Turn mixed prior outcomes into a conditional-allocation question | Prior-work contradiction + resource constraint | Ask how extra inference compute should be used for a given hard prompt | Promise a systematic analysis rather than another scaling recipe | The tension is a choice under budget, not generic LLM importance. |
| Snell | Intro ¶4-8 | Define matched alternatives and name the conditioning statistic | Method preview + benchmark choice | Establish best-of-N as the simple control | Promise difficulty-conditioned selection and FLOPs matching | The baseline and conditioning variable appear before headline numbers. |
| Paglieri | Abstract + Intro opening | Contrast always-plan and never-plan policies | Failure cases in long-horizon tasks | Name the concrete cost of planning every action | Pose learning when to plan as the replacement | The binary alternatives make the new decision scope legible immediately. |
| Paglieri | Intro contribution close | Preview two-stage learning and honest outcome boundary | Method/result preview | Explain why priming precedes RL | Close on learned behavior and human steerability | Method order follows an observed learning constraint. |
| BAVT | Abstract + Intro ¶1-4 | Turn budget exhaustion on dead ends into the specific systems bottleneck | Deployment constraint + failure cases | Describe redundant tool calls under finite budgets | Narrow to missing step-level control | The problem is felt as a concrete wasted action, not a field slogan. |
| BAVT | Intro contribution list | Map each proposed component to one bottleneck and one evaluation promise | Design rationale + evaluation contract | Name the tree/critic/budget controller | Promise matched-budget evaluation and a bounded guarantee | A numbered map prevents the components from reading as an arbitrary stack. |

## Exemplar Move Table — Methodology

| Exemplar | Paragraph | Move | Evidence Type | Opening Function | Closing Function | Notes on why this move worked |
|---|---|---|---|---|---|---|
| Snell | §3 problem setup | Formalize the prompt-conditioned choice under a compute budget | Objective/equation | Define available strategies and budget | Identify the unknown selection function | Formalization follows the empirical contradiction, so notation answers a live question. |
| Snell | §3.2 | Separate oracle difficulty from deployable predicted difficulty | Assumption + implementation distinction | State the sufficient-statistic approximation | Admit estimator cost and cross-validation need | The paper does not let an oracle analysis masquerade as deployability. |
| Paglieri | §3 | Decompose one LLM output into decide/plan/act policies | Conceptual equations | Define the state-dependent planning decision | Connect advantage, token cost, and task reward | One unified model avoids inventing a separate router and makes the decision target explicit. |
| Paglieri | §3.1-3.2 | State planning benefit and three costs before optimization | Assumption surface + objective | Ask when planning has positive net value | Explain which costs are explicit versus implicit | The operating assumptions, including zero turn-based latency, are visible before results. |
| BAVT | §3 overview | Introduce components in causal order: alternatives, value, budget | Algorithm design | Define nodes/actions and candidate expansion | Bind selection pressure to remaining budget | Each component has a distinct function and later ablation. |
| BAVT | §3.3-3.4 | Prefer residual progress to absolute self-evaluation | Mechanism + bounded selector | Identify overconfidence as a measurement problem | Derive exploration-to-exploitation behavior | The measurement choice is justified against a named failure mode. |

## Exemplar Move Table — Experimental Setup

| Exemplar | Paragraph | Move | Evidence Type | Opening Function | Closing Function | Notes on why this move worked |
|---|---|---|---|---|---|---|
| Snell | §4 + §3.2 protocol | Match compute and isolate the conditioning choice | Dataset/model/protocol | Define MATH split and PaLM 2 test bed | Explain two-fold selection/evaluation separation | Compute equivalence and selection hygiene are part of setup, not deferred caveats. |
| Paglieri | §4 | Use fixed-frequency/no-plan controls and multiple planning stages | Environments, seeds, controls | Define POGS/Crafter and agent interaction | State SFT/RL configurations that isolate dynamic planning | Controls correspond directly to the paper's binary framing. |
| BAVT | §4.1 | Compare within explicit budget tiers and model families | Benchmarks, budgets, metrics | Define tool-call budgets and QA tasks | Fix exact-match/F1 outcome and baselines | The resource constraint is an experimental variable, not a post-hoc cost report. |

## Exemplar Move Table — Results and Figures

| Exemplar | Paragraph | Move | Evidence Type | Opening Function | Closing Function | Notes on why this move worked |
|---|---|---|---|---|---|---|
| Snell | Fig. 3-4 + §5.3 | Show aggregate reversal by difficulty before policy summary | Stratified curves + matched compute | Compare search strategies at fixed budgets | Convert heterogeneity into the allocation result | The figure supplies the mechanism for the policy, not just a leaderboard bar. |
| Paglieri | Fig. 1 + §5 | Move from zero-shot frequency tradeoff to learned policy | Seed summaries + learning curves | Establish the Goldilocks pattern | Show that SFT+RL learns the conditional behavior | Evidence order distinguishes existence of heterogeneity from learnability. |
| BAVT | Fig. 3-5 + §4.2 | Report the performance-efficiency frontier at every budget | Matched-budget curves | Compare low/mid/high constraints | Highlight one concrete cross-budget contrast | The headline remains embedded in the whole frontier. |
| BAVT | §4.3 ablation | Let a harmful partial system rule out stacking | Component ablation | Show random tree alone degrades | Add critic then budget controller in measured order | A negative component result earns the full design. |

## Exemplar Move Table — Discussion and Limitations

| Exemplar | Paragraph | Move | Evidence Type | Opening Function | Closing Function | Notes on why this move worked |
|---|---|---|---|---|---|---|
| Snell | §5 interpretation + conclusion limits | Explain where additional compute stops substituting for capability | Difficulty-stratified failures | Interpret easy/intermediate gains | Exclude the hardest regime from the broad claim | Boundary cases limit the conclusion at the same granularity as the mechanism. |
| Paglieri | §5.3 + limitations | Preserve failed prompts/reward shaping and autonomous non-completion | Negative implementation evidence + scope | Explain why discarded controls failed | Name model/domain/latency limits | The research journey prevents learned planning from looking inevitable. |
| BAVT | §4.3 + §6 | Tie ablation failures to remaining overhead and cost-model gaps | Ablations + stated limitations | Explain why tree alone is insufficient | Name critic overhead and asymmetric tools as open | Future work follows measured bottlenecks instead of generic expansion. |

## Transfer to the ORF report

The internal report will transfer five moves:

1. Open on the replay-budget decision, not on generic AI security.
2. Separate exact oracle information value from deployable action inference.
3. Put the global exhaustive comparator and fixed-finite estimand before results.
4. Use the homogeneous negative and OAT results to prevent a stacked-success
   narrative.
5. End on the operational gap demonstrated by earlier live disconfirmation,
   not on a generic promise of future work.

No exemplar wording will be copied. Their methods and numbers appear only where
the verified citation database grades the supporting sentence strong or partial.
