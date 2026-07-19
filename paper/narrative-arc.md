# Narrative arc — ORF internal technical report

## Five-sentence spine

**Tension.** In the agent-security benchmark, candidate structure consumes the
same finite generation and replay budgets that determine whether any finding is
scored, yet a single fixed fill length assumes every observed response profile
should spend those budgets in the same way. **Gap.** Recent work shows that
adaptive inference allocation can outperform uniform policies in reasoning and
tool-using agents, but it does not answer how much profile-conditioned candidate
length is worth under this benchmark's exact scorer—and our authorized data do
not reveal whether a live target exposes a learnable signal. **Insight.**
Beacon-Held-Out Conditional Regret (ORF-B) isolates the exact finite score lost
when identical retained probes and resources are forced to share one global
fill length rather than choosing a legal length per profile. **Evidence.** On
three pre-specified public synthetic masters, the profile-conditioned oracle
gained 40.249% over an exhaustive seven-action global comparator, while three
homogeneous masters produced exact zero regret; cliffs and reset overhead
accounted for most of the one-at-a-time magnitude. **Resolution.** The study
establishes a large, auditable public-synthetic oracle information value and its
main boundary conditions, but it does not establish learnability, live-model
heterogeneity, replay-tail safety, private transfer, or Kaggle improvement.

## The research journey

The project began with a live leaderboard failure: a high constructed-mock score
did not transfer because multi-message candidates were latency-bound, ineffective
reserves diluted the dominant mechanism, and one mock cell had been mistaken for
the four-cell aggregate. That disconfirmation redirected the durable-moat question
away from another fixed recipe and toward online system identification: measure
which candidate structure a model can support, then allocate within the replay
budget.

ORF-B is the deliberately narrower scientific step. Its action-scope replacement
compares a per-profile oracle with the strongest matched global policy, not with
an under-tuned default. The finite inequality gives direction but not materiality;
the hypothesis therefore committed to a 5% threshold and a homogeneous equality
control. The design accumulated nine written hypothesis revisions and eleven
theory-review rounds because exact SDK identity, mixture scheduling, numeric
reproducibility, crash-atomic evidence publication, and held-out custody each
exposed blockers. Those engineering constraints are part of the evidential story,
not claimed scientific components.

The public PoC supported the mechanism, after which Phase 4 froze three primary
masters, three disjoint changed-regime masters, five one-at-a-time ablations, and
three nested scales. The core result and homogeneous negative both confirmed.
The changed regime and every scale cell preserved material direction. The most
informative secondary result was attribution: cliff behavior and reset overhead
dominated, novelty was negligible, and saturation suppressed rather than created
the effect. No Phase-4 prediction missed; that local calibration does not repair
the absence of an unopened test tier.

The load-bearing assumption is not the algebra. It is that real target behavior
contains stable, inferable response-profile heterogeneity under a replay-safe
budget. Constructed profiles cannot establish that assumption. The authorized
held-out beacon chain remains unfrozen and unopened, no Kaggle action is allowed,
and the profile-conditioned policy is an oracle rather than a learned controller.
The report must keep this limit adjacent to every broad interpretation.

## Why this approach, not the alternatives

- A copied fixed public recipe cannot be a durable moat and cannot test whether
  the exposed live response curve has information value.
- A mixed nonadaptive portfolio changes allocation and action scope together;
  ORF instead holds probes, actions, scores, and resources fixed and replaces only
  the shared argmax.
- A live or private experiment would answer more of `PROBLEM.md`, but it is not
  authorized. Public deterministic evidence is reported at its true scope.
- A contribution-paper narrative is rejected for now: adaptive allocation is
  crowded prior art, the test tier is unopened, and no learnable selector exists.

## Argument contract

Every section advances one of two linked propositions:

1. **Exact finite proposition:** profile conditioning has material oracle value
   on the frozen public synthetic construction, with a homogeneous zero boundary.
2. **Operational non-conclusion:** this value is not evidence that the live agent
   exposes, reveals, or safely permits exploitation of that information.

The paper succeeds only if a reader can state both propositions after the
abstract and again after the discussion.
