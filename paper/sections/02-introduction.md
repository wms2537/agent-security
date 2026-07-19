# Introduction

The audited local SDK couples attack scoring to finite generation and replay
resources. `AttackRunConfig.time_budget_s` is defined as the wall-clock budget
for a full attack run in `comp/sdk/aicomp_sdk/attacks/contracts.py`. The local
gateway sets a 9,000-second generation deadline for each configured model and a
separate 9,000-second deadline for each model–guardrail replay, and it replays
only the candidate prefix bounded by the imported `MAX_REPLAY_FINDINGS`
constant
(`comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py`). The
scorer sums predicate severity weights, adds two raw points for every distinct
score-cell hash, normalizes by the 200,000 raw-score reference, and caps the
normalized attack score at 1,000 (`comp/sdk/aicomp_sdk/scoring.py`). These are
facts about the audited repository, not claims about every benchmark or attack
system. Public-Synthetic Perfect-Information Regret (PS-PIR) adds a deliberately
synthetic decision to this local accounting: whether one fill length must be
shared across all rows of a specified score table or may be selected separately
for each row after all seven action scores are revealed.

Auditing that comparison is useful because it makes the score lost to the
shared-action restriction exactly calculable and exercises the finite
calculation's scorer-accounting and equality code paths. Its conceptual form is
established value of perfect information: information has value through the
decision it changes and
the resulting consequence [1]. In PS-PIR, however, the relevant information is
granted by construction. The row-wise comparator sees the complete
counterfactual score vector before choosing, so a positive difference cannot
show that informative observations exist or are available before an operational
choice. Contextual-bandit, off-policy evaluation, adaptive-optimization, and
heterogeneous-policy work instead makes observable context, partial feedback,
identification assumptions, or sequential observations part of the learning
problem [2]–[5]. Recent LLM systems likewise condition prompt-, subproblem-,
planning-, or step-level resource allocation on estimated or learned signals
[6]–[10]. PS-PIR defines no such signal-to-action mapping: its retained probes
do not choose the fill length.

One earlier live result provides historical motivation for checking structural
and aggregation assumptions, but it is not evidence for PS-PIR. The recorded
multi-post design was forecast at approximately 85 and returned an aggregate of
36.705 (`results.tsv`; `research-log/002-rootcause-and-rebuild.md`). Project
notes proposed latency, reserve allocation, parser behavior, and aggregation
mismatch as possible explanations. The present methods include no timing,
reserve-firing, parsing, or causal-attribution protocol that could identify
those explanations. They therefore remain diagnostic hypotheses. The observed
miss motivated an exact audit of one shared structural choice; it neither
explains the miss nor validates the synthetic table construction.

The evidence tier is correspondingly limited. The generator family, ranges,
weights, and analysis choices were developed adaptively through a public proof
of concept, numeric repair, calibration, and repeated hypothesis review. The
public configuration was then frozen before Phase 4, making that stage a
post-calibration frozen public verification of the selected deterministic
tables, not an untouched test. The 5% line was a preselected internal numerical
cutoff without external utility calibration. No context-to-length learner,
untouched evaluation tier, live target, private target, beacon operation,
held-out freeze or opening, or Kaggle action supplied evidence to the executed
study. **PS-PIR** names that executed public-synthetic calculation;
**ORF-B / Beacon-Held-Out Conditional Regret** is reserved for a prospective
protocol that was not executed.

This internal report contributes only three artifacts:

1. **An exact scorer calculation.** It instantiates the established
   perfect-information comparison on three named designer-specified crossed
   tables, reports the best shared action and every row-wise maximum, and checks
   exact equality on three homogeneous boundary tables. This is an
   implementation of finite-table arithmetic, not a new theorem or regret
   concept.

2. **Direct table diagnostics.** Per-table action histograms show the row-wise
   choices, a complete 40-stratum accounting assigns all 10,380,000 raw points
   of finite regret across 960 engineered rows, and one-at-a-time displays
   report raw perfect-information score \(A\), shared score \(G\), and
   \(A-G\) before their percentage ratios. These diagnostics describe the
   specified tables; they do not identify a causal mechanism or establish
   naturally occurring heterogeneity.

3. **An internally reproducible record.** Repository-relative code, configs,
   score tables, manifests, figures, diagnostic tables, and the complete
   42-row prediction ledger preserve the calculations and their adaptive
   history. The record has no external archive, DOI, or durability guarantee
   and is not a publication package.

Accordingly, PS-PIR is a reproducible scorer worked example rather than a
learned method, empirical population result, or deployable allocation policy.
It establishes no live-transfer or agent-security performance claim. Whether
observations available before a length choice can support a safe selector on an
untouched target remains unanswered and would be separate work.
