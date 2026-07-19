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
