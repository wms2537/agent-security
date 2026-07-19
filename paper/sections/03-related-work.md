# Related Work

## Value of information

The conceptual owner of Public-Synthetic Perfect-Information Regret (PS-PIR)
is decision-theoretic value of information. Howard values information through
the decisions it changes and the resulting consequences, with perfect
information as the limiting case in which the relevant uncertainty is resolved
before a choice is made [1]. PS-PIR has this established form in a deterministic
finite table: viewed across rows, the shared comparator is restricted to one
candidate length and cannot condition its action on the current row, whereas
the row-wise comparator is granted every counterfactual score for that row
before choosing. The difference between those two values is therefore a
scorer-specific perfect-information calculation. It does not establish that
such information is observable in operation, and the max-before/max-after
comparison is not a new information-value or regret concept.

## Context-conditioned policy learning and evaluation

Contextual policy research addresses the harder step that PS-PIR leaves open:
mapping information available at decision time to an action. Langford and Zhang
study bandits with observable side information, learning a context-to-action
rule while trading off exploration and exploitation and analyzing regret through
the policy class and its learning complexity [2]. Their setting makes the
contextual selector an object to be learned. By contrast, PS-PIR defines no
observable context-to-length rule; it directly supplies the complete score
vector for every legal length on each row.

Dudík et al. study evaluation and optimization of contextual policies from
historical data when only the reward for the logged action is observed [3].
Their doubly robust approach combines reward and logging-policy models, with
explicit assumptions governing what policy value can be identified from partial
feedback. PS-PIR bypasses that central estimation problem because its synthetic
table contains every action's counterfactual score. Consequently, the reported
oracle value is neither an off-policy estimate nor evidence that a policy could
recover the row-wise actions from retained probes.

Athey and Wager provide a related heterogeneous-assignment perspective: they
learn constrained treatment policies from observable individual
characteristics in observational data, using identification conditions and
doubly robust scores to obtain policy-value guarantees [4]. The contrast between
heterogeneous assignments and a uniform assignment resembles the action-class
comparison in PS-PIR, but the evidentiary problems differ. PS-PIR performs exact
arithmetic on designer-specified score tables; it does not estimate treatment
effects, identify policy value from observational data, or learn an assignment
rule. Together, these contextual-policy literatures show that moving from an
oracle table gap to an operational selector would require observations,
identification or feedback assumptions, a specified policy class, and an
evaluation protocol that are absent here.

## Adaptive optimization under partial observation

Golovin and Krause formalize adaptive submodular optimization for sequential
choices under partial observability, where later actions can depend on states
revealed by earlier selections [5]. Their guarantees concern adaptive policies
and greedy optimization under structural assumptions such as adaptive
submodularity. This supplies a useful distinction between observation-conditioned
and fixed policies, but PS-PIR is not an instance of their problem class: it
makes one candidate-length choice per profile after granting the full
counterfactual score row, has no sequential information-acquisition process, and
does not claim adaptive submodularity. The finite PS-PIR difference should thus
not be read as an operational adaptivity gap or as evidence that partial
observations suffice to realize the perfect-information value.

## Recent LLM allocation neighbors

Recent LLM work demonstrates conditional resource allocation at several
granularities, using information that must itself be estimated or learned.
At whole-prompt granularity, Snell et al.'s ICLR study conditions test-time
strategy and compute on model-specific estimates of mathematical-problem
difficulty [6]. At subproblem granularity, the ICLR 2026 Plan-and-Budget paper
decomposes queries and schedules token budgets from estimated relative
complexity across reasoning, instruction-following, and planning tasks [7],
while the peer-reviewed SCALE study selects reasoning modes and resource levels
for mathematical subproblems according to estimated difficulty [9]. These
studies evaluate performance--cost tradeoffs in their own reasoning domains;
they do not evaluate candidate-length actions under the scorer used by PS-PIR.

At agent and step granularity, the Paglieri et al. preprint trains a unified
agent to decide when planning has positive value in long-horizon environments,
comparing its learned decisions with fixed planning patterns [8]. The
Budget-Aware Value Tree Search preprint instead uses model-generated
residual-value estimates and remaining tool/token budget to control step-level
tool-agent search [10]. Their observation and control mechanisms are precisely
what the PS-PIR oracle calculation does not supply: the former learns a planning
gate from task interaction, and the latter performs online budget-conditioned
search using a critic. Their domains, actions, costs, and outcome measures also
differ from the deterministic candidate-length score tables considered here.
Accordingly, their reported quantitative results are not directly comparable
with the PS-PIR percentages.

## Positioning of PS-PIR

The foundational literature establishes value of perfect information,
context-to-action policy learning and evaluation, heterogeneous assignment, and
observation-conditioned optimization [1]–[5]. The recent LLM literature applies
conditional allocation to prompts, subproblems, planning decisions, and tool
search [6]–[10]. Against that background, PS-PIR contributes only a
scorer-specific worked example and reproducible implementation of an established
perfect-information policy-class comparison on named deterministic synthetic
tables. It is not a new regret concept, theorem, adaptive algorithm, learned
selector, or empirical phenomenon. In particular, it provides no evidence that
retained probes reveal the row-wise best length or that any operational policy
can attain a fraction of the computed oracle value.
