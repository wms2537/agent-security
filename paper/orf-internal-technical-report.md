# Perfect-Information Regret of a Shared Candidate-Length Constraint on Deterministic Synthetic Score Tables

Public-Synthetic Perfect-Information Regret (PS-PIR) is a deterministic scorer worked example that applies the established value-of-perfect-information comparison to a shared candidate-length constraint. On each completely specified score table, an exhaustive comparator selects one fill length for every row, while a perfect-information comparator selects separately after receiving every row's counterfactual scores. The resulting difference is an exact policy-class calculation, not a new regret concept, theorem, or learning method.

On the three named designer-specified crossed tables, the perfect-information gains over the shared comparator were 41.437632%, 38.111187%, and 41.198295%, spanning 38.111187--41.437632%. On three homogeneous tables constructed to have length one as the row-wise optimum, both comparators selected length one and had exactly equal scores, giving zero raw regret. These results describe only the supplied tables and the homogeneous boundary/code-path check. The crossed-table values exceeded a preselected 5% numerical cutoff, but that cutoff has no external utility calibration and does not imply practical importance.

PS-PIR grants full counterfactual observability; retained probes do not select an action. No learner was trained, and no live target, untouched test, beacon, held-out evaluation, Kaggle action, or transfer evaluation supplied evidence. The calculation therefore demonstrates neither an agent-security opportunity nor an attainable or deployable performance gain.

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

# Methodology

## PS-PIR on one fixed finite score table

Public-Synthetic Perfect-Information Regret (PS-PIR) is a deterministic
comparison between two policy classes on one completely specified score table.
It is an instance of established value-of-perfect-information reasoning, not a
new regret definition or an operational routing algorithm. The earlier name
ORF-B / Beacon-Held-Out Conditional Regret denotes only a prospective protocol
that was not executed in this study.

Let \(\mathcal{Z}\) be the finite set of rows in a named synthetic table and let

\[
\mathcal{M}=\{1,2,4,8,16,24,32\}
\]

be the designer-specified candidate fill lengths. For profile \(z\), the common
seven probes leave generation charge \(g_z\), replay charge \(r_z\), retained
candidate count \(p_z\), and raw score \(Q_z\). At fill length \(m\), the exact
candidate cost is \(c_z(m)>0\), the event yield is \(e_z(m)\geq 0\), and the
singleton raw-score increment is \(q_z(m)\geq0\), defined by

\[
q_z(m)=
\begin{cases}
0, & e_z(m)=0,\\
16e_z(m)+2, & e_z(m)>0.
\end{cases}
\]

The positive branch follows the audited scorer: each severity-five predicate
contributes 16 and each distinct score cell contributes 2
(`comp/sdk/aicomp_sdk/scoring.py`). The synthetic trace constructor requires
distinct score-cell hashes within a complete trajectory before using this
shortcut. A zero-yield attempt produces no finding and therefore has
\(q_z(m)=0\).

The zero branch is evaluated *before* any saturation quotient. Specifically,
with generation budget \(B_{\mathrm{gen}}\), synthetic replay budget
\(B_{\mathrm{rep}}\), returned-candidate cap \(C\), and per-profile raw cap
\(H\), define

\[
n_z(m)=0\qquad\text{if }q_z(m)=0.
\]

For \(q_z(m)>0\), first set

\[
h_z(m)=
\begin{cases}
0, & Q_z\geq H,\\
\left\lceil\dfrac{H-Q_z}{q_z(m)}\right\rceil, & Q_z<H,
\end{cases}
\]

and then set

\[
n_z(m)=\max\!\left(0,\min\!\left\{
C-p_z,
\left\lfloor\frac{B_{\mathrm{gen}}-g_z}{c_z(m)}\right\rfloor,
\left\lfloor\frac{B_{\mathrm{rep}}-r_z}{c_z(m)}\right\rfloor,
h_z(m)
\right\}\right).
\]

The corresponding table entry is

\[
S_z(m)=\min\{H,Q_z+n_z(m)q_z(m)\}.
\]

Here \(H\) is applied separately to each profile; it is not an aggregate-table
cap. Probe generation is charged for every attempted probe, while replay and
the candidate count are charged only for positive retained findings. These
rules define the synthetic table and do not model a measured live latency
distribution.

The shared-action comparator (`PROBE_GLOBAL` in the implementation) exhausts
all seven columns but selects one length for every row:

\[
G=\max_{m\in\mathcal{M}}\sum_{z\in\mathcal{Z}}S_z(m).
\]

The row-wise perfect-information comparator (`ADAPTIVE` in the implementation)
selects a column separately after observing every counterfactual entry:

\[
A=\sum_{z\in\mathcal{Z}}\max_{m\in\mathcal{M}}S_z(m).
\]

Ties choose the smaller length. We report the raw gap
\(\Delta=A-G\) and, because \(G>0\) in every reported table, the displayed
ratio

\[
R=100\frac{A-G}{G}.
\]

### Finite policy-class containment

Let \(m_G\) maximize the shared objective. Row by row,
\(\max_m S_z(m)\geq S_z(m_G)\). Summation yields only the elementary
containment result

\[
\Delta=\sum_z\left[\max_m S_z(m)-S_z(m_G)\right]\geq 0.
\]

Equality holds exactly when at least one shared action is row-optimal for every
profile. In one direction, a common row-wise maximizer attains \(A\) inside the
shared class, so \(G=A\). In the other, if \(G=A\), every nonnegative row loss
under \(m_G\) must be zero, so \(m_G\) is row-optimal everywhere. No stronger
theorem, distributional statement, or empirical mechanism is claimed.

For descriptive accounting, define the loss margin of shared action \(m\) on
row \(z\) as

\[
\ell_z(m)=\max_{m'\in\mathcal{M}}S_z(m')-S_z(m)\geq0.
\]

Then the reported gap is the smallest aggregate loss among the seven shared
columns, \(\Delta=\min_m\sum_z\ell_z(m)\). Thus an action histogram alone does
not determine the gap: the result depends both on which lengths maximize which
rows and on the score margins lost when the best shared column is used. This is
a description of finite-table arithmetic, not a novel regret characterization.

## Designer-specified table constructions

The primary crossed construction is an engineering stress test deliberately
made heterogeneous. It does not represent an estimated population of live
profiles. Candidate cost has the form

\[
c_z(m)=a_z+b_zm+d_zm^2.
\]

Forty equally weighted strata cross reset band (`LOW`, `HIGH`), linear-cost band
(`LOW`, `HIGH`), curvature (`NONE`, `HIGH`), and cliff location
\(k\in\{-1,4,8,16,24\}\). Each stratum has eight keyed replicates. Keyed
pseudorandom log-uniform draws use \(a_z\in[5,20]\) or \([40,80]\),
\(b_z\in[0.1,1]\) or \([2,8]\), \(d_z=0\) or
\(d_z\in[0.05,0.2]\), and, when a cliff is present,
\(\lambda_z\in[0.5,3]\). With no cliff or \(m\leq k\),
\(e_z(m)=m\). Above a positive cliff,

\[
e_z(m)=\operatorname{clamp}\!\left(
\left\lfloor m\exp[-\lambda_z(m-k)/k]\right\rfloor,0,m
\right).
\]

The construction therefore supplies the action and margin variation whose exact
consequences PS-PIR tabulates. The ranges, cliff frequency, and equal weights
are design choices; they carry no claim about empirical prevalence.

The homogeneous companion uses 64 keyed profiles with
\(c_z(m)=b_zm\), \(e_z(m)=m\), and \(b_z\in[5,12]\). Under the same finite
resource rules, length one is the unique row-wise maximizer by construction.
The shared and row-wise calculations must consequently agree. This is a
boundary and code-path sanity check, not an empirical discriminator or
additional support for any crossed-table magnitude.

### Design provenance

The following table separates facts read from the audited local SDK from the
choices used to construct PS-PIR. A value derived from an SDK constant can still
be a study choice when it is applied at a different aggregation level.

| Quantity | Value used in PS-PIR | Provenance and interpretation |
|---|---:|---|
| Generation budget \(B_{\mathrm{gen}}\) | 9,000 | SDK fact adopted by the study: the audited gateway sets `DEFAULT_BUDGET_S = 9000.0` for generation and separately for replay (`comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py`). The attack contract defines `time_budget_s` as a full-run wall-clock budget (`comp/sdk/aicomp_sdk/attacks/contracts.py`). |
| Synthetic replay budget \(B_{\mathrm{rep}}\) | 8,100 | Engineering choice in `experiments/poc/orf_support_calibration.py`; a conservative deterministic reserve, not an SDK deadline and not fitted to replay latency. |
| Returned-candidate cap \(C\) | 2,000 | SDK fact adopted by the study: `MAX_REPLAY_FINDINGS = 2_000` in `comp/sdk/aicomp_sdk/evaluation/ops.py`, imported and enforced as a replay slice by the audited gateway. |
| Raw saturation \(H\) | 200,000 per profile | Mixed provenance: the scorer uses `ATTACK_ELITE_RAW = 200000` and caps the corresponding normalized score at 1,000. Applying the equivalent raw saturation separately to every synthetic profile is a PS-PIR modeling choice. |
| Positive singleton score | \(16e+2\) | SDK scoring fact conditional on the constructed finding having \(e\) severity-five predicates and a distinct score cell; zero events produce no finding. |
| Legal/probe lengths | \(\{1,2,4,8,16,24,32\}\) | Engineering discretization fixed in the project config and generator; it is not asserted to be an SDK-mandated action set. |
| Cost form and reset ranges | \(a+bm+dm^2\); \([5,20]\), \([40,80]\) | Designer-specified stress-test choices; no empirical calibration to live reset cost. |
| Linear and curvature ranges | \(b\in[0.1,1]\) or \([2,8]\); \(d=0\) or \([0.05,0.2]\) | Designer-specified stress-test choices; no empirical frequency or latency interpretation. |
| Cliff locations and decay | \(k\in\{-1,4,8,16,24\}\); \(\lambda\in[0.5,3]\) | Designer-specified yield choices; the five cliff cells are equally represented rather than prevalence-weighted. |
| Stratum weights and replicates | 40 strata, equal weight, 8 replicates each | Engineering coverage choice producing 320 rows per named crossed table; not a probability sample. |
| Homogeneous slope range | \(b\in[5,12]\) | Engineering choice selected for the constructed length-one equality path. |
| Numerical cutoff | \(R\geq5\%\) | Preselected internal numerical cutoff fixed before the frozen public calculation, without external utility calibration. Crossing it does not imply practical importance. |

## Oracle information and non-operational scope

PS-PIR grants complete counterfactual access to every \(S_z(m)\) before the
row-wise argmax. The seven retained probes affect \(g_z,r_z,p_z,Q_z\) equally in
both policy classes, but their observations are never used to choose a fill
length. No context-to-action learner, probe-only classifier, selector-error
curve, or partial-feedback estimator is part of the calculation. Accordingly,
\(A\) is a perfect-information comparator on the named table, not evidence that
any fraction of \(\Delta\) is achievable by an agent.

The executed PS-PIR study consists only of deterministic public synthetic
tables. It makes no inference about live response heterogeneity, transfer,
deployable routing, or an untouched evaluation tier. No beacon, held-out
evaluation, private target, live target, or Kaggle action contributes to this
method or its results.

# Experimental setup

## Evidence chronology

The calculations followed three distinct evidence stages. First, the generator
and analysis choices were developed through adaptive public exploration and
calibration. That stage included a 40-profile proof of concept, repairs to the
public support construction, and repeated hypothesis review. Its outputs
informed the crossed-table family, coefficient ranges, weights, and numerical
cutoffs used later. Second, the labels, actions, predictions, and public config
were frozen in `experiments/configs/orf-phase4-v1.json`, after which Phase 4 ran
a **post-calibration frozen public verification** of those choices. Freezing the
calculation after public calibration prevents outcome-dependent relabeling
within Phase 4, but it does not make the selected construction untouched.
Third, there was no untouched evaluation stage. The locked v7 construction was
neither frozen nor opened, and no live target, beacon, held-out evaluation, or
Kaggle action contributed evidence to PS-PIR.

## Named deterministic tables

The primary calculation uses three designer-specified crossed tables, named by
their ASCII master preimages:

1. `orf-public-phase4-v1|master|000`;
2. `orf-public-phase4-v1|master|001`;
3. `orf-public-phase4-v1|master|002`.

Each name is mapped once by SHA-256 to a deterministic master. Each primary
table has 320 profile rows and seven score columns, one for each legal fill
length in \(\mathcal M=\{1,2,4,8,16,24,32\}\). The 320 rows are the complete
cross of 40 designer-specified strata and eight keyed replicates per stratum.
The strata cross two reset-cost bands, two linear-cost bands, two curvature
settings, and five cliff settings. Equal stratum weights and all coefficient
ranges are engineering stress-test choices; they do not represent estimated
frequencies in a population. Keys include the master, stratum, and replicate,
so every row is recoverable without mutable random state. The reporting unit is
one complete named table; rows, score columns, strata, and nested prefixes are
components or views of those tables, not additional reporting units.

Three homogeneous tables append `|homogeneous` to the corresponding primary
preimages before hashing. Each contains 64 deterministic rows for which the
row-wise optimum is fixed at length one by construction. These tables exercise
the equality and tie-handling code paths; they are not an independently observed
negative condition.

The score cells are exact outputs of the construction described in Methodology.
The primary tables use \(H=200{,}000\), a 9,000-second generation budget, and an
8,100-second synthetic replay allocation. The 9,000-second value and scorer cap
are inherited from the audited SDK; the replay allocation, factor ranges, equal
weights, and 5% line are project choices. The 5% line was fixed before the
Phase-4 calculations solely as an internal numerical cutoff and has no external
utility calibration.

## Matched finite-table comparators

Both comparators receive the identical complete score table and the same seven
legal actions. The exhaustive shared comparator computes the column total for
every \(m\in\mathcal M\) and chooses the maximizing length once for the whole
named table. The perfect-information row-wise comparator chooses the maximizing
length separately in every row and then sums those row maxima. Both choose the
smaller legal length on a tie. Thus the comparison changes only the scope of the
argmax; it does not change profiles, actions, costs, caps, budgets, or scores.
The row-wise comparator is an oracle because it is granted all counterfactual
action scores. Retained probes do not select an action, and no context-to-length
learner is trained or evaluated.

## Sensitivity calculations

Three secondary calculation families describe how the displayed finite-table
ratio changes under specified transformations. They do not provide untouched
transfer evidence.

The one-at-a-time (OAT) family applies five transforms to the same three primary
tables: remove the cliff transform; set curvature to zero; set reset cost to
zero; remove the two-point novelty term; or replace \(H=200{,}000\) with
\(H=10^{18}\). No action set or comparator is retuned. Because a transform can
change both oracle and shared totals and the transforms interact, these are
removal-associated sensitivity calculations rather than component shares.

The changed-construction family uses the three public labels
`orf-public-phase4-generalization-v1|master|000` through `|002`. Despite the
legacy string in those labels and artifact paths, this is a second
designer-specified public construction, not an untouched replication. It uses
\(H=10^{18}\) and weights each no-cliff row four times and each cliff row once,
giving equal aggregate weight to the two groups within each named table.

The nested-prefix family reuses each primary table and includes replicate
indices \(0\) through \(k-1\) in every stratum for \(k\in\{1,4,8\}\), producing
40-, 160-, and 320-row prefixes. These nine master-by-prefix cells are dependent
views of three tables. They are a numerical sensitivity display, not additional
independent evidence or a learning curve.

## Descriptive outputs

For every named primary table, the report retains the exact shared total
\(G\), perfect-information total \(A\), raw gap \(\Delta=A-G\), percentage ratio
\(100\Delta/G\), selected shared length, and the complete row-wise action count
over all seven legal lengths. The primary display reports all three named ratios
and their exact minimum--maximum range. It does not replace those values with a
sampling model.

The stratum accounting reports, for each of the 40 crossed strata, the 24 rows
formed by that stratum across the three named tables, raw regret, share of the
finite total regret, and modal row-wise action. This accounting describes where
the engineered tables contain the finite gap; it is not a causal decomposition.
The OAT display reports raw \(A\), \(G\), and \(\Delta\), alongside the ratio,
for the primary condition and all five transforms. Homogeneous outputs retain
exact action identities and raw equality. Changed-construction and nested-prefix
outputs are reported as named-table or named-prefix values, with arithmetic
aggregates used only as deterministic summaries.

No population standard deviation, standardized score, confidence interval, or
hypothesis test is defined for these finite tables. The analysis declaration is
therefore `test: none; p: not applicable`. Passing the preselected 5% numerical
cutoff is a statement about these exact ratios only.

## Execution and internal reproducibility

All scientific commands are repository-relative and are run from the repository
root. The Phase-4 calculations used Linux x86_64, glibc 2.40, CPython 3.14.3 at
`comp/.venv/bin/python`, and `jsonschema==4.26.0`; they were CPU-only and made no
network calls. Dependency records are pinned in
`paper/reproducibility/requirements-core.txt` and
`paper/reproducibility/requirements-figures.txt`. Exact verification commands,
fresh-attempt rules, canonical inputs and outputs, and the separate figure
environment are listed in `paper/reproducibility/README.md`.

The core and secondary runners bind source, config, upstream evidence, and
outputs by SHA-256 in their `COMPLETE.json` manifests. The reviewer-requested
action, stratum, and raw OAT tables are regenerated with the repository-relative
command:

```bash
comp/.venv/bin/python experiments/orf-phase5-analysis/generate_reviewer_tables.py
```

This constitutes internal reproducibility from the present repository, not an
external availability claim. There is no public clone, externally archived
release, DOI, operating-system container, or durability guarantee.

# Results on named deterministic tables

The results below are exact arithmetic on designer-specified score tables. The
shared comparator exhaustively evaluated all seven legal lengths and selected
length **16** on each crossed table. Allowing the perfect-information policy to
select a length separately for every profile produced gains of
**41.437632336565%** on P0, **38.111186959411%** on P1, and
**41.198294770946%** on P2. The finite range across these three named values was
**38.111186959411--41.437632336565%**.

| Crossed table | Perfect-information score, \(A\) | Shared-action score, \(G\) | Raw gap, \(A-G\) | Shared length | Gain, \(100(A-G)/G\) |
|---|---:|---:|---:|---:|---:|
| P0 | 11,886,082 | 8,403,762 | 3,482,320 | 16 | 41.437632336565% |
| P1 | 12,187,804 | 8,824,632 | 3,363,172 | 16 | 38.111186959411% |
| P2 | 12,113,766 | 8,579,258 | 3,534,508 | 16 | 41.198294770946% |

These values describe P0--P2 only. Their arithmetic mean, used below solely to
compact the sensitivity summaries, is 40.249038022308%.

Figure 1 places the primary values beside the second public construction
reported below. The construction labels are not paired, and the two mean bars
do not define a between-construction test.

![Figure 1: Exact gains on two public designer-specified constructions.](figures/comparison_chart.svg)

*Figure 1. Exact percentage gaps for three named tables in the primary public
construction (P0--P2) and three named tables in the changed public construction
(G0--G2). Black bars are descriptive arithmetic means. The dashed 5% line is a
preselected numerical cutoff with no external utility calibration. Error bars
and inferential tests: none. Source:
`paper/figures/comparison_chart.source.csv`.*

## Homogeneous boundary check

The homogeneous construction fixes length one as a row-wise optimum. Both the
shared and perfect-information policies selected length one throughout all
three homogeneous tables, and their scores were exactly equal:

| Homogeneous table | Perfect-information score | Shared-action score | Raw gap | Shared length | All row-wise lengths one |
|---|---:|---:|---:|---:|:---:|
| H0 | 1,277,552 | 1,277,552 | 0 | 1 | yes |
| H1 | 1,198,568 | 1,198,568 | 0 | 1 | yes |
| H2 | 1,230,140 | 1,230,140 | 0 | 1 | yes |

This entailed equality is a boundary and code-path sanity check. It is not an
empirical comparison between populations and does not independently establish
the source of the positive gaps in P0--P2.

## Row-wise action distributions

The perfect-information choices on the crossed tables were dispersed across
lengths 4, 8, 16, 24, and 32. Lengths 1 and 2 were never selected. Each row of
the table below sums to the 320 profiles in that named table.

| Crossed table | Shared length | \(m=1\) | \(m=2\) | \(m=4\) | \(m=8\) | \(m=16\) | \(m=24\) | \(m=32\) | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P0 | 16 | 0 | 0 | 66 | 96 | 72 | 53 | 33 | 320 |
| P1 | 16 | 0 | 0 | 66 | 85 | 83 | 52 | 34 | 320 |
| P2 | 16 | 0 | 0 | 65 | 96 | 69 | 58 | 32 | 320 |

The dispersion is direct description of the engineered profiles. It does not
show that a live observation reveals the listed choices or that these
frequencies occur outside the three tables.

## Stratum contribution accounting

The crossed construction contains 40 factorial strata. Aggregating the three
masters gives 24 profiles per stratum, **960 profiles** in total, and exact
aggregate raw regret of **10,380,000**. Four strata--13, 28, 33, and 38--had
zero raw regret. The five largest raw contributions were:

| Stratum | Raw regret | Share of total raw regret | Modal row-wise length |
|---:|---:|---:|---:|
| 6 | 1,064,390 | 10.254239% | 4 |
| 2 | 1,044,968 | 10.067129% | 8 |
| 1 | 1,016,548 | 9.793333% | 4 |
| 7 | 956,938 | 9.219056% | 8 |
| 0 | 883,284 | 8.509480% | 32 |
| **Top five** | **4,966,128** | **47.843237%** | -- |

The complete 40-row accounting, including reset band, linear band, curvature,
cliff value, profile count, raw regret, share, and modal length, is in
`paper/tables/stratum-regret-decomposition.tsv`. These entries allocate the
observed arithmetic gap across engineered strata; they are not causal component
shares or prevalence estimates.

## One-at-a-time sensitivity calculations

The core row and five one-at-a-time (OAT) transforms are summarized with their
raw quantities below. For each row, \(A\), \(G\), and \(A-G\) are arithmetic
means across P0--P2. The percentage column is the mean of the three exact
master-level ratios, so it need not equal the quotient of the displayed rounded
mean raw values.

| Condition | Mean \(A\) | Mean \(G\) | Mean \(A-G\) | Mean gain | Change from core |
|---|---:|---:|---:|---:|---:|
| Core | 12,062,550.667 | 8,602,550.667 | 3,460,000.000 | 40.249038022308% | -- |
| Remove cliff | 15,937,335.333 | 14,808,566.667 | 1,128,768.667 | 7.622073949240% | -32.626964073068 pp |
| Remove reset | 31,031,426.667 | 26,082,096.000 | 4,949,330.667 | 18.973588191963% | -21.275449830344 pp |
| Remove curvature | 15,676,959.333 | 11,373,606.000 | 4,303,353.333 | 37.860007927303% | -2.389030095004 pp |
| Remove novelty bonus | 11,935,712.000 | 8,521,525.333 | 3,414,186.667 | 40.094682770562% | -0.154355251746 pp |
| Remove saturation | 12,581,486.000 | 8,716,761.333 | 3,864,724.667 | 44.355152104598% | +4.106114082290 pp |

Cliff removal and reset removal produced the two largest removal-associated
decreases in the displayed percentage ratio. Novelty-bonus removal produced the
smallest change, and saturation removal increased the ratio. Every transform
changed both \(A\) and \(G\); the transforms also interact. The differences
therefore cannot be added or read as fractions attributable to separate
mechanisms.

Figure 2 retains the three master-level ratio changes behind the summary. It is
a display of paired calculations on reused tables, not a decomposition.

![Figure 2: Master-level OAT changes from the core percentage ratio.](figures/ablation_heatmap.svg)

*Figure 2. Change from the core percentage ratio under five one-at-a-time
transforms of the same three named crossed tables. Colored points are exact
master-level changes and black diamonds are their arithmetic means. The
transforms change both policies' raw scores and may interact; no additive or
causal interpretation is assigned. Error bars and inferential tests: none.
Source: `paper/figures/ablation_heatmap.source.csv`.*

## Second public construction

A second designer-specified public construction produced gains of
**36.653863013959%**, **37.352060597349%**, and **35.175681399541%** on its
three named tables G0, G1, and G2, respectively. Their descriptive mean was
**36.393868336949%**. All three values were above the preselected 5% numerical
cutoff. The construction changes several engineering choices at once and was
also public, so its values are a second finite calculation rather than evidence
of transfer to another data source.

## Nested-prefix numerical sensitivity

The same P0--P2 profile order was truncated to nested prefixes of 40, 160, and
320 profiles. The resulting exact percentage gaps were:

| Profiles per table | P0 | P1 | P2 | Descriptive mean |
|---:|---:|---:|---:|---:|
| 40 | 52.609341554583% | 45.344531072985% | 48.905042746765% | 48.952971791444% |
| 160 | 43.389924985133% | 39.592292530738% | 45.400277409186% | 42.794164975019% |
| 320 | 41.437632336565% | 38.111186959411% | 41.198294770946% | 40.249038022308% |

All nine displayed cells are above the 5% numerical cutoff, but they reuse the
same three named tables and nested rows. They are not nine independent units. The
change across prefixes is a deterministic numerical-sensitivity result for this
fixed ordering, not evidence about how performance changes with additional
sampled data.

![Figure 3: Exact gaps across nested prefixes of the same tables.](figures/scaling_curve.svg)

*Figure 3. Percentage gaps on nested 40-, 160-, and 320-profile prefixes of
P0--P2. Colored trajectories reuse each named table; the black trajectory is
their descriptive arithmetic mean. No new table is added as prefix length
increases. Error bars and inferential tests: none. Source:
`paper/figures/scaling_curve.source.csv`.*

## Descriptive status of the numbers

No sampling model was specified for the named synthetic tables, and no
inferential statistic is reported. Means are compact arithmetic summaries only;
the primary result is the three values and their range. The 5% line was selected
before these frozen public calculations as an internal numerical cutoff, but it
was not calibrated to deployment utility, cost, or risk. Accordingly, clearing
that line carries no external practical interpretation.

# Discussion

## Scope of the calculation

PS-PIR answers a narrow deterministic question. On the three named crossed
tables, allowing a row-wise perfect-information choice instead of one exhaustive
shared choice produced ratios of 41.437632336565%, 38.111186959411%, and
41.198294770946%; the shared action was length 16 in all three tables. On the
three homogeneous tables, both policy classes selected length one and the raw
gap was exactly zero. These are exact properties of those score tables and a
boundary check of the implementation. They are not estimates of an
agent-security population.

The direction of the comparison follows from policy-class containment, while
the positive magnitude comes from the tables that were supplied. The crossed
generator deliberately varies reset cost, linear cost, curvature, and yield
cliffs over equally weighted strata. Its ranges, factor frequencies, replay
reserve, and weights are engineering stress-test choices rather than measured
features of live response profiles. Moreover, the generator family was
adaptively developed and repaired during public proof-of-concept and calibration
work before the Phase-4 config was frozen. The ensuing calculation is therefore
post-calibration frozen public verification: freezing prevented further
within-stage changes, but it did not remove construction-selection bias or
create an untouched evidence tier.

The second public construction and the nested prefixes do not change that
inference. A mean ratio of 36.393868336949% under a different public weighting
and means of 48.952971791444%, 42.794164975019%, and 40.249038022308% for the
40-, 160-, and 320-row prefixes are further arithmetic descriptions within the
same design program. The prefixes reuse rows from the three primary tables, and
the changed construction remains designer specified. Likewise, the 5% line was
a preselected numerical cutoff without external utility calibration; crossing
it says nothing about practical importance.

## Heterogeneity represented in the engineered tables

The action counts make the source of the finite gap visible without extending
it beyond the construction. Although the best shared action is length 16 for
each table, the row-wise comparator uses lengths 4, 8, 16, 24, and 32. Across
the three tables, the respective per-table count ranges are 65--66, 85--96,
69--83, 52--58, and 32--34; lengths 1 and 2 are unused. This dispersion shows
that the constructed score rows have different maximizing columns. It does not
show that naturally occurring profiles have these frequencies, that the five
actions are distinguishable from retained probes, or that a realizable policy
could select them.

The stratum accounting adds the score margins that an action histogram omits.
Across 960 rows, 36 of the 40 designed strata have positive regret and four
(`13`, `28`, `33`, and `38`) have zero regret. Total raw regret is 10,380,000,
and the five largest stratum shares sum to approximately 47.843%. Thus the gap
is distributed across many cells of this table but is also concentrated in a
few of the largest designed cells. Because strata were crossed and equally
weighted by construction, these shares are bookkeeping over engineered support,
not causal contributions or prevalence estimates.

## Interacting removal contrasts

The one-at-a-time calculations should be read as transformations of the whole
score table, not as a decomposition. In the primary condition, mean raw
perfect-information score (A), shared score (G), and gap (A-G) are
12,062,550.667, 8,602,550.667, and 3,460,000.000. Removing cliffs changes those
three quantities to 15,937,335.333, 14,808,566.667, and 1,128,768.667 and lowers
the displayed ratio from 40.249038022308% to 7.622073949240%. Removing reset
cost instead changes them to 31,031,426.667, 26,082,096.000, and 4,949,330.667,
while the ratio falls to 18.973588191963%. These examples show why a ratio
change cannot be assigned to one component: its numerator and denominator both
move, and the raw gap may increase while the ratio decreases.

Among the five displayed transforms, cliff and reset removal produced the two
largest decreases in the percentage ratio. Curvature removal produced
37.860007927303%, novelty removal produced 40.094682770562%, and removing
saturation produced 44.355152104598%. The transforms interact and were not
combined factorially, so their changes are neither additive shares nor
identified mechanisms. They describe how the selected deterministic tables
respond to five specified edits.

## Historical failures are separate evidence

The project history contains disconfirmations that should not be retrofitted as
support for PS-PIR. A local equal round-robin ensemble was forecast to score 66
but scored 56.76. A subsequent weighted allocation improved that local result,
yet it did not establish transfer. More importantly, an earlier multi-post live
design was forecast at approximately 85 and returned 36.705. Project notes
proposed latency, reserve allocation, parser behavior, and aggregation mismatch
as possible explanations. The PS-PIR methods contain no timing, firing,
parsing, or attribution protocol capable of identifying those causes, so they
remain diagnostic hypotheses rather than findings. A later single-post rebuild
returned 69.570 against a forecast of 84--90, another reminder that local or
synthetic score calculations were not reliable live aggregate predictions.

The public synthetic path was itself adaptive. Six first-pass calibration rows
crashed because of an exact-numeric conversion defect and were rerun only after
the numeric implementation repair; the proof of concept and repaired calibration
outcomes then informed the selected Phase-4 construction. Preserving these failures in
the ledger is essential to interpreting the final tables: the exact arithmetic
is reproducible, but the construction was selected after substantial public
development. Neither the failed live forecasts nor the repaired calibration
establishes why the engineered table has its reported magnitude.

## Missing operational evidence

The difference between PS-PIR and an operational policy is the information and
evaluation problem. PS-PIR grants the row-wise comparator all seven
counterfactual scores before it acts. A deployable study would first need to
define observations available before the length choice and a policy class that
maps those observations to legal actions, as contextual-bandit and heterogeneous
policy-learning work does [2], [4]. It would then need to train or select that
policy without leaking unavailable counterfactuals and evaluate its value under
the relevant feedback and identification assumptions [3]. If the probes were
themselves selected sequentially, the information-acquisition policy and its
structural assumptions would also need to be explicit rather than equated with
full-table access [5].

None of those steps is an implementation detail that can be inferred from the
oracle gap. The retained probes in this study never choose a fill length, no
selector-error curve is measured, and no partial-feedback policy value is
estimated. The study also supplies no calibrated latency-tail model or
whole-run failure-risk guarantee. Consequently, it neither demonstrates an
agent-security opportunity nor establishes that any fraction of the
perfect-information difference is attainable as a replay-safe, deployable gain.

## Governance and availability boundary

For PS-PIR, no beacon was fetched; the prospective ORF-B protocol was not
frozen or opened; and no held-out, live-target, private-target, or Kaggle action
was performed. No external archive, DOI, submission, or public release was
created. The repository supports internal deterministic replay, but it does not
provide an externally durable publication package. Any learner study or target
evaluation would be new work requiring its own prospective design and explicit
authorization. The present evidence ends with a reproducible calculation on
designer-specified public synthetic tables, not a passed external evaluation.

# Conclusion

The executed Public-Synthetic Perfect-Information Regret (PS-PIR) calculation
is a reproducible scorer case study on three named, designer-specified crossed
tables. Relative to the exhaustive shared length 16, the row-wise
perfect-information comparator produced exact gains of **41.437632336565%** on
P0, **38.111186959411%** on P1, and **41.198294770946%** on P2, a finite range
of **38.111186959411--41.437632336565%**. On the three homogeneous tables, both
comparators selected length one and the raw gap was exactly zero; this is the
constructed boundary and code-path sanity check.

The action histograms and stratum accounting describe the heterogeneity built
into the crossed tables. Among the one-at-a-time transformations, cliff and
reset removal produced the two largest removal-associated decreases in the
displayed ratio, but those interacting contrasts do not identify component
shares or mechanisms. Because the table family, coefficient ranges, strata,
weights, and numerical cutoff were engineering choices, none of these exact
magnitudes establishes behavior beyond the specified tables.

PS-PIR contributes no new regret concept, theorem, algorithm, or learner, and
it demonstrates neither an agent-security opportunity nor a deployable gain.
ORF-B / Beacon-Held-Out Conditional Regret names only a prospective protocol
that was not executed; it is not part of the PS-PIR evidence. The unanswered
operational question is: can observations available before the candidate-length
choice, without counterfactual action scores, support a context-to-length policy
that exceeds the best shared length under the same resource and scoring
constraints on an untouched operational target?

# References

[1] Ronald A. Howard. “Information Value Theory.” *IEEE Transactions on
   Systems Science and Cybernetics*, 2(1), 22–26, 1966.
   [doi:10.1109/TSSC.1966.300074](https://doi.org/10.1109/TSSC.1966.300074).

[2] John Langford and Tong Zhang. “The Epoch-Greedy Algorithm for Multi-armed
   Bandits with Side Information.” *Advances in Neural Information Processing
   Systems 20*, 2007.
   [Official proceedings record](https://proceedings.neurips.cc/paper/2007/hash/4b04a686b0ad13dce35fa99fa4161c65-Abstract.html).

[3] Miroslav Dudík, John Langford, and Lihong Li. “Doubly Robust Policy
   Evaluation and Learning.” *International Conference on Machine Learning
   (ICML 2011)*, 2011. arXiv:1103.4601.
   [doi:10.48550/arXiv.1103.4601](https://arxiv.org/abs/1103.4601).

[4] Susan Athey and Stefan Wager. “Policy Learning With Observational Data.”
   *Econometrica*, 89(1), 133–161, 2021.
   [doi:10.3982/ECTA15732](https://onlinelibrary.wiley.com/doi/10.3982/ECTA15732).

[5] Daniel Golovin and Andreas Krause. “Adaptive Submodularity: Theory and
   Applications in Active Learning and Stochastic Optimization.” *Journal of
   Artificial Intelligence Research*, 42, 427–486, 2011.
   [doi:10.1613/jair.3278](https://aaai-21.aaai.org/Library/JAIR/Vol42/jair42-012.php).

[6] Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. “Scaling LLM
   Test-Time Compute Optimally Can be More Effective than Scaling Parameters
   for Reasoning.” *International Conference on Learning Representations
   (ICLR 2025)*, 2025. arXiv:2408.03314.
   [doi:10.48550/arXiv.2408.03314](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b623663fd9b874366f3ce019fdfdd44-Abstract-Conference.html).

[7] Junhong Lin, Xinyue Zeng, Jie Zhu, Song Wang, Julian Shun, Jun Wu, and
   Dawei Zhou. “Plan and Budget: Effective and Efficient Test-Time Scaling on
   Reasoning Large Language Models.” *International Conference on Learning
   Representations (ICLR 2026; accepted, arXiv record)*, 2026.
   arXiv:2505.16122.
   [doi:10.48550/arXiv.2505.16122](https://arxiv.org/abs/2505.16122).

[8] Davide Paglieri, Bartlomiej Cupial, Jonathan Cook, Ulyana Piterbarg, Jens
   Tuyls, Edward Grefenstette, Jakob Nicolaus Foerster, Jack Parker-Holder, and
   Tim Rocktaschel. “Learning When to Plan: Efficiently Allocating Test-Time
   Compute for LLM Agents.” *arXiv preprint*, 2026. arXiv:2509.03581.
   [doi:10.48550/arXiv.2509.03581](https://arxiv.org/abs/2509.03581).

[9] Yang Xiao, Chunpu Xu, Ruifeng Yuan, Jessie Wang, Wenjie Li, and Pengfei Liu.
   “SCALE: Selective Resource Allocation for Overcoming Performance Bottlenecks
   in Mathematical Test-time Scaling.” *Proceedings of the AAAI Conference on
   Artificial Intelligence*, 40(40), 34034–34042, 2026.
   [doi:10.1609/aaai.v40i40.40697](https://doi.org/10.1609/aaai.v40i40.40697).

[10] Yushu Li, Wenlong Deng, Jiajin Li, and Xiaoxiao Li. “Spend Less, Reason
    Better: Budget-Aware Value Tree Search for LLM Agents.” *arXiv preprint*,
    2026. arXiv:2603.12634.
    [doi:10.48550/arXiv.2603.12634](https://arxiv.org/abs/2603.12634).

# Supplementary Material

## S1. Complete historical prediction and outcome ledger

The block below is a byte-for-byte copy of `results.tsv`: one header and all 42
data rows, including failed, exploratory, discarded, superseded, and
mechanics-only records. Its SHA-256 is
`9379de501f0f9bd9330aa146d5df9700816c4ccdc664f899e74a331a6e2f81b1`.
`NA` and `null` retain their recorded meanings and have not been converted to
zero.

This ledger is an immutable history, not revision-2 scientific terminology.
In particular, every occurrence of `confirm` (including descriptions such as
`confirmation interval`), `materiality`, `generalization`, or `robustness` is a
historical signal, metric name, run description, or decision label written
under the earlier protocol. Those words do not upgrade PS-PIR into an untouched
test, practical-utility result, population generalization, or robustness claim.

```tsv
run_id	metric	predicted_value	predicted_direction	confidence	metric_value	signal	memory_gb	runtime_s	status	description
goexplore-det-baseline	normalized	NA	unclear	low	NA	null	0.5	20	exploratory	provided Go-Explore baseline vs deterministic agent; timed out at 20s budget (heavy search)
local-compliant-400-rr	normalized	66	beat-baseline	medium	56.76	disconfirm	0.5	37	discard	equal round-robin ensemble dilutes sev-64 multi-post with sev-4 CD
local-compliant-400	normalized	120	beat-baseline	medium	100.68	partial	0.5	37	keep	weighted alloc, multi-post EXFIL dominant + small diversity hedge (mock upper bound)
local-refuse-exfil-400	normalized	8	match-baseline	high	11.04	confirm	0.5	37	keep	http.post blocked -> selector falls back to CONFUSED_DEPUTY and still fires (robustness path)
local-compliant-400-hardened	normalized	200	beat-baseline	medium	198.60	confirm	0.5	37	keep	multi-post-8 + 22pct second-family reserve; ~2x per-candidate severity, private insurance held
local-refuse-exfil-hardened	normalized	9	match-baseline	high	11.28	confirm	0.5	37	keep	private-guardrail sim (http.post blocked) still scores via CONFUSED_DEPUTY reserve
real-lb-v1-multipost	normalized_lb	~85	beat-baseline	low	36.705	disconfirm	NA	NA	superseded	v1 real LB: mock 198 was ONE compliant cell not the 4-cell mean; multi-post latency-bound + 28pct dead reserves -> bottom of board
real-lb-v2-singlepost	normalized_lb	84-90	beat-prior	medium	69.570	partial	NA	NA	keep	v2 real LB: single-post exfil + per-model raw/s selection + verified fill + void-safe 0.90; +89pct over v1, mid-pack (top ~103.7)
local-replay-cap-parity	findings_ratio	1.210	beat-baseline	high	1.205	confirm	0.5	11	keep	controlled real-SDK run: old 0.90/1.10 accounting returned 39 findings, public 0.99/direct-cost accounting returned 47
local-multi-fixed-overhead-3	normalized	1.950	beat-baseline	high	1.950	confirm	0.5	3	keep	adaptive router selected M8 multi-message under fixed reset overhead; official raw exactly 390=3*(16*8+2)
local-multi-context-fallback-3	normalized	0.270	match-baseline	high	0.270	confirm	0.5	1	keep	M4 probe passed but M8 context-limited candidate failed 75pct gate; router fell back to three single-post findings, exact raw=54
local-multi-default-50	normalized	96.50	beat-baseline	high	96.50	confirm	0.5	20	mechanics-only	production M24 default on compliant/harmony mocks: exact raw=19300=50*(16*24+2); not a real-model score prediction
orf-cal-v1-equal-h200-clear	masters_clearing_5pct_fraction	0.750000000000	beat-baseline	low	NA	null	NA	NA	crash	equal-weight H=200000 non-target calibration; exploratory only
orf-cal-v1-balanced-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	NA	null	NA	NA	crash	balanced cliff-presence H=200000 sensitivity; exploratory only
orf-cal-v1-no-cliff-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	NA	null	NA	NA	crash	no-cliff-only H=200000 sensitivity; exploratory only
orf-cal-v1-cliff-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	NA	null	NA	NA	crash	cliff-only H=200000 sensitivity; exploratory only
orf-cal-v1-equal-unsat-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	NA	null	NA	NA	crash	equal-weight H=10^18 saturation sensitivity; exploratory only
orf-cal-v1-floor-margin	minimum_cliff_floor_distance	0.000000000000000000000000000000000000000000000000000000000001	beat-baseline	low	NA	null	NA	NA	crash	minimum distance from a cliff expression to an integer; no resampling
orf-cal-v2-equal-h200-clear	masters_clearing_5pct_fraction	0.750000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; equal-weight H=200000; exploratory only
orf-cal-v2-balanced-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; balanced cliff-presence H=200000; exploratory only
orf-cal-v2-no-cliff-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; no-cliff-only H=200000; exploratory only
orf-cal-v2-cliff-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; cliff-only H=200000; exploratory only
orf-cal-v2-equal-unsat-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; equal-weight H=10^18; exploratory only
orf-cal-v2-floor-margin	minimum_cliff_floor_distance	0.000000000000000000000000000000000000000000000000000000000001	beat-baseline	low	2.4702028345850861854631560389931149158158007314717302917408272803144660234725560E-8	confirm	NA	29.43	exploratory	retry after v1 numeric crash; no-resampling floor certificate
poc	adaptive_gain_percent	35.0	beat-baseline	low	49.277489504413	confirm	0.053520203	0.679508220	keep	public non-target 40-stratum ORF PoC; support threshold 5%, prediction interval 20-50%
poc	homogeneous_difference_raw	0	match-baseline	high	0	confirm	0.053520203	0.679508220	keep	exact homogeneous negative invariant
poc	sdk_cases_verified	2	match-baseline	high	2	confirm	0.053520203	0.679508220	keep	actual SDK q=16e+2 and 16-hex score-cell fixture checks
orf-p4-baseline	mean_global_score_raw	8500000	unclear	medium	8602550.666666666667	confirm	0.023773193	1.491515685	keep	exact N=3 public non-target PROBE_GLOBAL baseline and tuned parity
orf-p4-baseline	global_length_16_fraction	1.0	match-baseline	high	1.000000000000	confirm	0.023773193	1.491515685	keep	calibration-derived prediction that every master selects m=16
orf-p4-baseline	mechanical_reference_match_fraction	1.0	match-baseline	high	1.000000000000	confirm	0.023773193	1.491515685	keep	exact default tables must match immutable calibration reference
orf-p4-core	mean_adaptive_gain_percent	40.0	beat-baseline	medium	40.249038022308	confirm	0.515918732	0.132034047	keep	public N=3 per-profile-vs-global core; confirmation interval 30-50 percent
orf-p4-core	all_masters_clear_fraction	1.0	beat-baseline	high	1.000000000000	confirm	0.515918732	0.132034047	keep	all three fixed public masters must have adaptive gain at least 5 percent
orf-p4-core	homogeneous_zero_fraction	1.0	match-baseline	high	1.000000000000	confirm	0.515918732	0.132034047	keep	exact zero-regret distinguishing negative across three homogeneous masters
orf-p4-core	homogeneous_length_one_fraction	1.0	match-baseline	high	1.000000000000	confirm	0.515918732	0.132034047	keep	all homogeneous rows and global policies must select fill length one
orf-p4-ablations	no_cliff_mean_gain_percent	7.0	beat-baseline	low	7.622073949240	confirm	0.548843384	1.506462713	keep	one-at-a-time replacement of every event vector by e(m)=m
orf-p4-ablations	no_curvature_mean_gain_percent	35.0	beat-baseline	low	37.860007927303	confirm	0.548843384	1.506462713	keep	one-at-a-time exact d=0 cost transform
orf-p4-ablations	no_reset_mean_gain_percent	22.0	beat-baseline	low	18.973588191963	confirm	0.548843384	1.506462713	keep	one-at-a-time exact a=0 cost transform
orf-p4-ablations	no_novelty_mean_gain_percent	40.0	beat-baseline	medium	40.094682770562	confirm	0.548843384	1.506462713	keep	one-at-a-time replacement of positive raw 16e+2 by 16e
orf-p4-ablations	unsaturated_mean_gain_percent	44.0	beat-baseline	medium	44.355152104598	confirm	0.548843384	1.506462713	keep	one-at-a-time replacement of H=200000 by H=10^18
orf-p4-generalization	mean_generalization_gain_percent	35.0	beat-baseline	medium	36.393868336949	confirm	0.558269501	1.294787546	keep	disjoint public unsaturated balanced-cliff regime; confirm interval 30-45 percent
orf-p4-generalization	all_generalization_masters_clear_fraction	1.0	beat-baseline	high	1.000000000000	confirm	0.558269501	1.294787546	keep	all three weighted generalization masters must gain at least 5 percent
orf-p4-scaling	all_scale_master_cells_clear_fraction	1.0	beat-baseline	high	1.000000000000	confirm	0.583507538	0.031398170	keep	all 3 masters x nested 40/160/320-profile cells must gain at least 5 percent
```

The unchanged status census is 26 `keep`, 7 `exploratory`, 6 `crash`, 1
`discard`, 1 `superseded`, and 1 `mechanics-only`. PS-PIR uses the Phase-4
deterministic score-table artifacts for its worked example; the remaining rows
are preserved to expose calibration, failure, and historical decision paths.

## S2. Chronology and absence of an untouched tier

All times below are local commit times (`+08:00`) on 2026-07-19. A “freeze” in
this table means that a public configuration or prediction was committed before
its corresponding deterministic calculation. It does not mean the generator
family was untouched by earlier exploration.

| Time | Commit | Recorded event | Evidence-tier implication |
|---|---|---|---|
| 15:07:39 | `bba39d7` | Public support calibration v1 preregistered. | Exploratory public calibration. |
| 15:10:17 | `bcf9a5c` | Calibration v1 recorded as numerically invalid. | Six crash rows retained; no effect estimate. |
| 15:11:20 | `47f50a2` | Narrow Decimal/Fraction repair preregistered. | Repair fixed before the retry. |
| 15:13:25 | `a120336` | Calibration v2 recorded. | Public exploratory outcomes informed later magnitude expectations. |
| 16:27:03 | `74d1836` | Prospective ORF-B v9 specification and contract committed. | Protocol design only; no freeze/open or target evaluation. |
| 16:55:17 | `25921b4` | Theory-review round 11 closed `RIGOROUS`. | Theory scrutiny, not empirical held-out evidence. |
| 19:06:56 | `9b0d94a` | Forty-profile public PoC prediction and command frozen. | Post-calibration public check. |
| 19:11:54 | `b126636` | Public PoC recorded at 49.277489504413%. | Used to decide whether to proceed; not pooled with Phase 4. |
| 19:16:39 | `354cc02` | Phase-4 public config, labels, sequence, and boundaries frozen. | Start of post-calibration frozen public verification. |
| 19:17:43 | `a416a72` | Exhaustive shared-policy baseline prediction frozen. | Public prediction before baseline calculation. |
| 19:23:22 | `1b0a7c5` | Baseline score tables and result committed. | Exact shared comparator on the selected tables. |
| 19:31:16 | `9aa3d89` | Core implementation committed unexecuted. | Result remained unavailable before code review. |
| 19:39:47 | `2a4f280` | First core-code review logged a stale/partial-bundle blocker. | Scientific core remained unexecuted. |
| 20:14:48 | `bb896ab` | Transactional evidence-bundle repair committed. | Source-level provenance repair. |
| 20:20:13 | `bfbbdca` | Re-review logged a symlink/lexical-identity blocker. | Scientific core still remained unexecuted. |
| 20:27:28 | `06239e3` | Lexical identity and no-follow repair committed. | Second source-level provenance repair. |
| 20:31:24 | `99ee635` | Third review closed the code gate `SOUND`. | One-use core calculation became eligible. |
| 20:33:19 | `20b73f4` | Three core predictions and equality checks frozen. | Public prediction before the core calculation. |
| 20:35:54 | `02b90ff` | Core and homogeneous results committed. | Three named crossed tables plus a boundary/code-path sanity check. |
| 20:38:46 | `e0b9520` | Five OAT predictions frozen. | Public sensitivity plan before calculation. |
| 21:00:34 | `47fb042` | OAT table committed after focused review. | Removal-associated public sensitivity values. |
| 21:01:41 | `6fc4df8` | Second-construction predictions frozen. | Another designer-specified public calculation. |
| 21:15:26 | `d8ccce6` | Second-construction results committed. | Not an untouched replication or transfer test. |
| 21:16:18 | `a796796` | Nested-prefix prediction frozen. | Reuses the primary tables. |
| 21:26:34 | `eb180fa` | Nested-prefix results committed. | Numerical sensitivity, not independent replication. |
| 21:33:46 | `0fa39de` | Phase-4 batch audit closed. | Public deterministic batch complete. |
| 21:51:51 | `db7e87d` | Phase-5 analysis, figures, and internal-report decision committed. | Locked test explicitly not run. |
| 22:02:40 | `a490f5d` | Version-1 report plan committed. | Writing began after analysis. |
| 22:20:22 | `08f300f` | Version-1 report assembled and deterministically checked. | Internal draft only. |
| 22:20:43 | `b8c0ea0` | Paper-review round 1 dispatched. | Paper-review budget charged 1/2. |
| 22:29:20 | `330703a` | Round-1 `NEEDS_REVISION` verdict logged verbatim. | Twelve issues required branch-of-origin reconstruction. |
| 23:02:23 | `f0af017` | PS-PIR revision-2 foundation and diagnostics committed. | Executed study downgraded to a deterministic worked example. |
| — | — | **Untouched evaluation tier** | **None was created, frozen, opened, or run.** |

The chronology therefore supports custody of each public calculation but gives
the magnitude no untouched-test force. PS-PIR names what was executed. ORF-B /
Beacon-Held-Out Conditional Regret names only the prospective protocol; all its
candidate contracts remained unfrozen and unopened.

## S3. Repository-relative artifact and command map

All paths and commands are relative to the repository root. The clean local
bootstrap, recorded environments, dependency pins, one-use attempt rule, and
full scientific-family commands are documented in
`paper/reproducibility/README.md`.

| Purpose | Canonical inputs or code | Recorded outputs | Verification or regeneration command |
|---|---|---|---|
| Environment | `experiments/configs/environment.md`; `paper/reproducibility/requirements-core.txt`; `requirements-figures.txt` | Recorded CPython/package versions | See `paper/reproducibility/README.md` |
| Shared comparator | `experiments/configs/orf-phase4-v1.json`; `experiments/orf-p4-baseline/run_baseline.py` | `score-tables.tsv`; `aggregate-by-length.tsv`; `baseline-summary.json` | Scientific-family command in the reproducibility guide |
| PS-PIR core and equality check | `experiments/orf-p4-core/run_core.py`; baseline score table | `experiments/runs/orf-p4-core-v1/core-by-master.tsv`; `homogeneous-by-master.tsv`; `COMPLETE.json` | `comp/.venv/bin/python -m unittest experiments/orf-p4-core/test_toy_core.py` |
| OAT sensitivities | `experiments/orf-p4-ablations/run_ablations.py` | `experiments/runs/orf-p4-ablations-v1/ablation-by-master.tsv`; transformed table; `COMPLETE.json` | `comp/.venv/bin/python -m unittest experiments/orf-p4-ablations/test_toy_ablations.py` |
| Second public construction | `experiments/orf-p4-generalization/run_generalization.py` | `experiments/runs/orf-p4-generalization-v1/generalization-by-master.tsv`; score table; `COMPLETE.json` | `comp/.venv/bin/python -m unittest experiments/orf-p4-generalization/test_toy_generalization.py` |
| Nested prefixes | `experiments/orf-p4-scaling/run_scaling.py`; baseline score table | `experiments/runs/orf-p4-scaling-v1/scaling-by-cell.tsv`; `COMPLETE.json` | `comp/.venv/bin/python -m unittest experiments/orf-p4-scaling/test_toy_scaling.py` |
| Reviewer-requested diagnostics | `experiments/orf-phase5-analysis/generate_reviewer_tables.py` | `paper/tables/action-distributions.tsv`; `oat-raw-summary.tsv`; `stratum-regret-decomposition.tsv` | `comp/.venv/bin/python experiments/orf-phase5-analysis/generate_reviewer_tables.py` |
| Figures and source data | `experiments/orf-phase5-analysis/generate_figures.py`; committed experiment tables | `paper/figures/comparison_chart.*`; `ablation_heatmap.*`; `scaling_curve.*` | `python experiments/orf-phase5-analysis/generate_figures.py` |
| Report integrity | Ordered files in `paper/sections/`; committed code/evidence | `paper/orf-internal-technical-report.md`; `paper/reproducibility/SOURCE_REVISION.txt`; `MANIFEST.tsv` | `python paper/assemble_report.py`<br>`python paper/reproducibility/build_manifest.py`<br>`python paper/check_revision.py` |
| Complete audit trail | `results.tsv`; `research-log/020-poc-orf-core.md` through `048-orf-paper-revision-foundation.md` | Ledger, predictions, reviews, analyses, and decisions | `git log --date=iso-strict-local -- research-log results.tsv paper experiments` |

Each transactional `COMPLETE.json` binds the canonical command, attempt
identity, source/input hashes, exact output set, and artifact hashes. The
committed attempt directories are no-overwrite evidence; a scientific-family
rerun must use a new explicit direct-child attempt name as described in the
guide.

## S4. Reviewer-requested diagnostics

The complete diagnostics are machine-readable tables rather than inferential
samples:

- `paper/tables/action-distributions.tsv` has three master rows and 960 profile
  decisions in total. The shared action is length 16 for every master. Row-wise
  choices use lengths 4, 8, 16, 24, and 32; lengths 1 and 2 are unused. Counts
  sum to 320 for each master.
- `paper/tables/stratum-regret-decomposition.tsv` has all 40 crossed strata,
  each aggregating 24 profiles across the three masters: 960 profiles total and
  raw regret 10,380,000. Strata 13, 28, 33, and 38 have zero regret. The five
  largest contributions are strata 6, 2, 1, 7, and 0 and sum to approximately
  47.843237% after displayed-share rounding. This is contribution accounting
  for the engineered tables, not a causal or prevalence decomposition.
- `paper/tables/oat-raw-summary.tsv` reports the core and five transforms as raw
  mean row-wise-oracle score `A`, shared score `G`, difference `A-G`, and the
  displayed percentage ratio. The core row is
  `12,062,550.667 / 8,602,550.667 / 3,460,000.000 / 40.249038022308%`.
  Because transforms can change both `A` and `G` and interact, their values are
  removal-associated sensitivity contrasts, not additive component shares.

The action table, stratum table, and raw OAT table are generated together by
the command listed in S3. Its deterministic audit records three action rows,
960 profiles, 40 strata, and total raw regret 10,380,000.

## S5. Local reproducibility and availability limits

The report is reproducible inside this repository from deterministic integer
and rational tables, committed code, local Git history, completion manifests,
dependency-version records, and the commands in the reproducibility guide. The
Phase-4 scorer calculations used Linux x86-64, glibc 2.40, CPython 3.14.3,
`jsonschema==4.26.0`, CPU only, and no network. Figure generation used CPython
3.11.11 with `matplotlib==3.10.9`.

This is internal reproducibility, not a durable public release. There is no
public clone URL, external archive, DOI, archived operating-system image,
container, bit-for-bit dependency lock, or durability guarantee. The commit IDs
in S2 identify local repository states but are not externally retrievable
without a separately shared repository snapshot. No publication, archive, or
external-release action was taken or authorized.

The data used by PS-PIR are deterministic synthetic tables stored locally. No
personal data, human-subject data, live target data, private evaluation data, or
beacon-derived target data enter the executed calculation.

## S6. Research-process, compute, AI-assistance, and governance disclosure

### Iterations and reviews

The state at revision-2 assembly records cycle 1, active hypothesis iteration
4, and 1 of 5 research-iteration budget units spent. Nine written hypothesis
revisions were preserved. Eleven of 20 authorized hypothesis-review rounds were
dispatched; round 11 returned `RIGOROUS` for the prospective v9 specification.
These are revision and scrutiny counts, not independent hypotheses,
replications, or experimental units.

Paper-review round 1 consumed 1 of the 2 authorized rounds and returned
`NEEDS_REVISION`. Its complete twelve-issue verdict is preserved in
`research-log/047-orf-paper-review-round1.md`. The reconstruction foundation is
`research-log/048-orf-paper-revision-foundation.md`; at the point this supplement
was written, the second paper-review round had not yet been dispatched.

### Full research path

The record is intentionally unsanitized. Equal round-robin allocation was
discarded after underperforming its prediction. A historical multipost/reserve
design was superseded after a 36.705 live aggregate missed its approximately 85
forecast. Latency, reserve, parsing, and aggregation were proposed as possible
explanations in project notes, but PS-PIR did not run a diagnostic protocol that
identifies them as causes. Six calibration-v1 rows crashed because of premature
numeric precision loss; the repair was specified before calibration v2. Two
code reviews then blocked core execution on evidence-bundle and lexical-path
provenance defects, both repaired and re-reviewed before the core calculation.

### Compute

Counting each Phase-4 scientific family once, recorded runtime was exactly
4.456198161 seconds and maximum reported peak memory was 0.583507538 GB. The
five OAT rows share one execution, the scale cells share one execution, and
repeated per-metric runtime fields must not be summed. These are wall-clock and
peak-process measurements on the recorded local environment, not an energy or
hardware-normalized compute estimate. A complete project-wide runtime cannot be
reconstructed exactly from the ledger because historical live rows contain
`NA` and some multi-metric/batched rows repeat one execution's runtime.

### AI assistance and human control

AI agents assisted with literature retrieval and field verification, hypothesis
stress testing, code review, deterministic analysis, figure generation,
manuscript planning and drafting, and manuscript review. The human user selected
the research scope, authorized review budgets and progression through Phase 6,
and set the no-Kaggle and no-held-out boundaries. Agent prose and reviewer
judgments were not used as quantitative evidence without checks against primary
literature or committed machine-readable artifacts.

### Executed versus prospective work

PS-PIR is the executed post-calibration public deterministic calculation. ORF-B
/ Beacon-Held-Out Conditional Regret is prospective and unexecuted. No beacon
was fetched, no held-out freeze or opening occurred, no target/profile set was
derived, and no locked/private score was produced. No new Kaggle push, API call,
notebook run, submission, or leaderboard read was taken after the user's
explicit no-Kaggle boundary or as part of PS-PIR. Earlier historical Kaggle
observations remain visible in S1; they are not PS-PIR evidence. Any future
held-out, live, private, Kaggle, archive, or submission action would require
separate authorization.

The experimental unit in the worked example is one named deterministic master.
Profiles, actions, strata, OAT transforms, and nested-prefix cells are dependent
views, not samples from a declared population. Accordingly, the report supplies
exact values and finite ranges but no sample standard deviation, standardized
effect, confidence interval, population test, or p-value. The preselected 5%
line has no external utility calibration.
