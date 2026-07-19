# Related Work

We organize related work by two properties of conditional allocation: the
granularity at which a decision is made and the information available when it is
made. Existing systems condition computation at the prompt, subproblem, or agent
step using estimated difficulty, learned state, or model-generated value. ORF-B
instead conditions a finite candidate-length choice on a fully observed synthetic
response profile and measures an oracle gap. These objectives, domains, and units
are incompatible, so the numbers below characterize results within each cited
study rather than a common ranking.

## Prompt- and subproblem-conditioned compute

Snell et al. study test-time strategy selection at whole-prompt granularity on
mathematical reasoning. They stratify MATH problems by model-specific difficulty,
compare iterative revision and verifier-guided search within fixed inference
budgets, and construct a per-prompt compute-optimal policy. In reported regimes,
that policy nearly matched or exceeded best-of-N while using up to fourfold less
test-time compute; the hardest problems benefited little from additional compute,
and estimating difficulty itself incurred inference cost [Snell et al., 2025].
The study therefore establishes both the value and the boundary of prompt-level
conditioning in its reasoning setting. Its conditioning statistic is an estimate
used to select a strategy; it does not measure candidate length under a security
benchmark scorer.

Plan-and-Budget moves the allocation unit inside a query. It decomposes a
reasoning problem into subquestions, estimates their relative complexity, and
assigns token budgets with an adaptive schedule rather than applying one global
budget. The current report for its reasoning, instruction-following, and
tool-free planning evaluations gives gains of up to 70% in accuracy, a 39% token
reduction, and a 193.8% increase in its E3 efficiency metric [Lin et al., 2026].
Those values describe that paper's own objectives and baselines. The method
depends on a useful complexity ordering and substitutes practical schedules for
parameters that cannot be estimated exactly at deployment.

SCALE likewise allocates at subproblem granularity, selecting System 1 or System
2 processing and a resource level from estimated mathematical difficulty. On
AIME25, its reported comparison raises accuracy from 57.50% to 71.25% while
reducing computation by 33--53% relative to uniform-scaling baselines
[Xiao et al., 2026]. The result reinforces the case against uniform reasoning allocation
in that domain, while leaving its benefits dependent on decomposition and
difficulty classification. Together, these studies show that broad adaptive
allocation across heterogeneous reasoning instances is prior art. They do not,
however, determine the value of replacing one shared candidate-length action
with profile-wise actions under ORF-B's finite score table.

## Learned planning decisions in agents

Paglieri et al. move from estimated task difficulty to a state-dependent planning
decision inside a long-horizon agent. Their unified model learns when to plan
through supervised priming followed by reinforcement learning, with no-planning
and fixed-frequency policies as controls. In the reported Crafter comparison, an
8B dynamic-planning agent attains reward 0.387 versus 0.379 for a 70B zero-shot
baseline while generating 85% fewer tokens [Paglieri et al., 2026]. The paper
also records boundaries that matter for interpreting the result: the agents do
not fully solve Crafter, the evaluation covers two environments, and planning
latency is effectively absent in the turn-based setting.

Their learned live-environment policy answers a different question from ORF-B.
It tests whether an agent can infer when planning has positive net value and act
on that inference. ORF-B measures the information value of an oracle that already
knows each synthetic profile's score table; it neither trains nor evaluates a
selector. Constructed response profiles can validate the mechanics of that
conditional action but cannot confirm that a target model exhibits stable,
observable response heterogeneity. We therefore do not treat the synthetic oracle
gap as evidence that a live agent can learn the corresponding decision.

## Budget-aware tool-agent search

Budget-Aware Value Tree Search (BAVT) is the closest tool-agent neighbor in the
bounded set. It expands alternative tool-use paths, uses a shared LLM critic to
estimate residual step value, prunes low-value paths, and changes selection from
exploration toward exploitation as the remaining tool and token budget shrinks.
Across its multi-hop question-answering evaluation, the reported low-budget
OSS-20B comparison gives average exact match 0.338 with five tool calls, versus
0.334 for parallel sampling with 20 calls [Li et al., 2026]. Its ablation is also
informative: random tree structure alone degrades performance, static step-level
value helps, and remaining-budget conditioning supplies the resource-aware
control.

BAVT performs online, step-level search with a model-generated value signal;
ORF-B evaluates an exact, scorer-specific action-scope relaxation after retaining
the same probes, legal lengths, resources, and score. BAVT's critic adds inference
overhead, and its experiments use one external tool with a uniform discrete cost,
leaving asymmetric tool costs outside the evaluated setting [Li et al., 2026].
Correspondingly, ORF-B's finite resource accounting does not establish replay-
deadline safety. Such a safety claim would require a calibrated latency-tail and
dependence model together with an explicit acceptable void-risk target, neither
of which is measured here.

## Bounded positioning of ORF-B

Our bounded search identified prompt-conditioned reasoning policies,
subproblem-level token schedulers, learned planning gates, and budget-conditioned
tool search. This five-paper set cannot establish exhaustive priority, but it is
sufficient to reject a broad claim that adaptive allocation itself is new. ORF-B's
narrower distinction is an exact SDK-shaped finite conditional-regret measurement:
for identical synthetic profiles, retained probes, legal actions, resources, and
scores, it compares one exhaustive global fill-length argmax with profile-wise
argmaxes and includes a homogeneous equality control. It is not a learned or live
controller, and its public synthetic evidence does not establish target-model
heterogeneity, private transfer, or replay safety. With that scope fixed, the next
section defines the finite estimand and the single action-scope replacement used
to measure it.
