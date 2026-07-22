# One-sided resource-risk admission: targeted literature anomaly pass

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** completed targeted pass

## Context and scope

The sealed HCMS-24 PoC retained a `1.391831525207` controlled raw-score ratio but invalidated the joint claim. Two primary replay costs were `1.01984x` and `1.03308x` their candidate-specific charges, while four primary cells admitted fresh construction/reset paths with more than the fixed `0.1 s` reserve and nevertheless crossed the generation deadline. These are not two unrelated threshold defects: both arise from treating random future work as a point cost while claiming one-sided safety.

This bounded anomaly pass asks which published guarantees can replace point-cost admission without post-hoc margin fitting. It examines exactly five primary sources: four peer-reviewed theorem papers and one deadline-specific June-2026 preprint. The search focused on one-sided conditional runtime prediction, conformal/risk control, dependence-aware online calibration, time-uniform concentration, and deadline assurance. Surveys were not used as evidence; Howard et al. is an original master-theorem paper published in a journal named *Probability Surveys*, not a secondary survey.

The application has three unusual properties that every guarantee must be checked against:

1. **Sequential endogeneity:** the controller chooses the next method, prefix and salvage state using prior outcomes; construction/reset mode and remaining time also affect the next cost.
2. **Selective observation:** actual cost is fully observed only for admitted/completed work unless censoring and timeout outcomes are explicitly retained.
3. **Strict total deadline:** one admitted operation can invalidate the cell. An average or marginal coverage statement is not a zero-overage guarantee.

## Source findings

### 1. Conformalized quantile regression (CQR): useful conditional shape, marginal validity

**Source:** Romano, Patterson and Candès, “Conformalized Quantile Regression,” NeurIPS 2019. [Official paper](https://proceedings.neurips.cc/paper_files/paper/2019/file/5103c3584b063c431bd1268e9b5e76fb-Paper.pdf)

The relevant object is a one-sided upper prediction limit for actual cost `Y` conditional on observable pre-admission features `X`. CQR first fits conditional quantiles on a proper training split and then adds an order-statistic correction from a disjoint calibration split. Theorem 2 gives the directly relevant upper-tail statement:

\[
\Pr\{Y_{n+1}\le \widehat q_{\alpha_{hi}}(X_{n+1})+Q_{1-\alpha_{hi}}\}\ge 1-\alpha_{hi}.
\]

The exact load-bearing assumption is exchangeability of all `(X_i,Y_i)`, including the next test pair. The quantile model may be inaccurate and flexible, but it must be fitted without using the calibration/test responses in a way that destroys exchangeability. The guarantee is finite-sample and marginal over the calibration and test draws; it is not conditional coverage for the realized feature vector, the realized calibration set, or a hard subclass. The theorem also allows asymmetric tail control, so an upper-only construction is legitimate and does not need to waste probability mass on the irrelevant lower tail.

**Fit here:** CQR is a good *shape model* for heteroskedastic costs using features known before admission: operation type, method, requested prefix, transition/reset flag, prior-cost summaries and possibly cell identity. It does not automatically fit the deployed stream. HCMS changes which candidates are observed, costs share a cell-level environment, and later candidates are chosen from earlier outcomes; those pairs are not exchangeable merely because the underlying simulator has fixed seeds. Applying ordinary split CQR to admitted candidates and calling the result safe would therefore overclaim. It also supplies probability `1-alpha`, not strict deadline safety.

### 2. Conformal risk control (CRC): exact expected-risk control, but only under exchangeable loss functions

**Source:** Angelopoulos et al., “Conformal Risk Control,” ICLR 2024. [Official paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/f3549ef9b5ff520a7e41ff3cc306ab2b-Paper-Conference.pdf)

CRC can calibrate a conservative admission parameter `lambda` by defining a loss such as `L_i(lambda) = 1{actual_cost_i > charge_i(lambda)}`. Theorem 1 assumes the random loss functions `L_1,...,L_{n+1}` are exchangeable; each `L_i(lambda)` is non-increasing in `lambda`, right-continuous, uniformly bounded by finite `B`, and a maximal `lambda_max` is known whose loss is at most `alpha`. Under those assumptions, its calibrated `lambda_hat` satisfies

\[
\mathbb E[L_{n+1}(\widehat\lambda)]\le \alpha.
\]

The guarantee is unconditional expected risk for the next exchangeable loss, not high-probability safety of a fixed deployed calibration set. The paper's Proposition 4 permits non-exchangeability only by adding an explicit total-variation penalty, `B sum_i TV(Z_i,Z_{n+1})`; this is informative but unusable unless those shifts can actually be bounded. The paper itself states that non-exchangeable extensions require knowledge of the shift.

**Fit here:** the admission threshold is monotone—larger charged time rejects more work—so the loss geometry fits cleanly. The sampling geometry does not. Sequential salvage and remaining-budget decisions change the cost mixture and induce dependence, so the exchangeable-loss assumption needs a new episode-level calibration design or a predeclared group/trajectory unit, not candidate rows pooled after the fact. Even if valid, expected indicator loss controls the frequency of misses and cannot guarantee zero misses in a finite cell. With `K` possible admissions, per-candidate risk `alpha` can imply roughly `K alpha` family-wise risk; a cell-level loss or preallocated alpha budget is required.

### 3. Online conformal prediction with decaying step sizes: arbitrary dependence, retrospective average coverage

**Source:** Angelopoulos, Barber and Bates, “Online conformal prediction with decaying step sizes,” ICML 2024. [PMLR paper and PDF](https://proceedings.mlr.press/v235/angelopoulos24a.html)

This paper removes stochastic assumptions for one specific guarantee. In its adversarial setting, data points may be an arbitrary sequence and score functions `s_t` may be arbitrary maps into `[0,B]`. Theorem 1 assumes only a positive non-increasing step-size sequence `eta_t` and `q_1 in [0,B]`; for every horizon `T`, the absolute error of the *time-average* empirical coverage from `1-alpha` is bounded by

\[
\left|T^{-1}\sum_{t=1}^T 1\{Y_t\in C_t(X_t)\}-(1-\alpha)\right|
\le \frac{B+\eta_1}{\eta_T T}.
\]

For `eta_t proportional to t^{-a}`, `0<a<1`, the bound vanishes as `O(T^{a-1})`. The guarantee is pathwise for arbitrary sequences and therefore survives the dependence/endogeneity that defeats ordinary split conformal. The paper is explicit, however, that this is a retrospective long-run coverage statement. Per-time population coverage and convergence of the threshold to a population quantile require the separate i.i.d. setting, where the score function at time `t` depends only on the past and is independent of current/future data.

**Fit here:** this is a valid *monitor/adaptor* for long-run miss frequency under endogenous streams. It is not an admission certificate for a two-second cell: several misses can cluster early or late while the average bound still holds, and the algorithm can only respond after seeing a miss. Consequently it cannot be the load-bearing safety mechanism for HCMS. It may later update a utility envelope across many independent cells, but treating its arbitrary-sequence average guarantee as pointwise deadline protection would repeat the same category error as the fixed `0.1 s` reserve.

### 4. Time-uniform Chernoff bounds: dependence-compatible only after proving a conditional tail process

**Source:** Howard, Ramdas, McAuliffe and Sekhon, “Time-uniform Chernoff bounds via nonnegative supermartingales,” *Probability Surveys* 17 (2020). [Publisher DOI](https://doi.org/10.1214/18-PS321) · [Author/arXiv version](https://arxiv.org/abs/1808.03204)

The paper's master result can support optional stopping and adaptive sampling, but not for free. Definition 1 requires adapted processes `(S_t,V_t)`, with `V_t` non-negative, and—for every admissible `lambda`—a non-negative supermartingale `L_t(lambda)` satisfying

\[
\exp\{\lambda S_t-\psi(\lambda)V_t\}\le L_t(\lambda),\qquad L_0(\lambda)\le l_0.
\]

Under this `sub-psi` condition, Theorem 1 gives time-uniform line-crossing bounds; for example, for `a,b>0`,

\[
\Pr\{\exists t:S_t\ge a+bV_t\mid\mathcal F_0\}\le l_0e^{-aD(b)}.
\]

The supermartingale formulation permits dependent/adaptive sequences when the increments still satisfy the required conditional moment-generating-function bound given the past. Optional stopping and predictable selection do not invalidate the bound. Conversely, marginal tail fit, empirical residual coverage, or an unconditional MGF is insufficient. If the policy preferentially admits cheap-looking paths, if expensive censored paths disappear, or if construction/reset latency has an unmodeled state-dependent tail, the required conditional supermartingale may fail.

**Fit here:** this is the most principled foundation for an *anytime evidence ledger* across endogenous decisions, provided HCMS can define a filtration, retain censored/timeout observations, and justify bounded or sub-gamma conditional increments after the admission decision. It naturally controls cumulative deviation or a parameter confidence sequence, not the next cost itself. Turning it into a next-operation upper bound still needs a conditional model and a tail assumption. It remains probabilistic; without a deterministic execution cap, a single arbitrarily long environment construction can cross the wall-clock deadline while all prior confidence-sequence statements were valid.

### 5. Conformal recovery-deadline certificates: the relevant architecture is statistical autonomy plus verified safety

**Source:** Shojaei, “Conformal Recovery-Deadline Certificates for Runtime Assurance of Adapting Controllers,” arXiv:2606.25371v1, 24 June 2026. [Author preprint](https://arxiv.org/pdf/2606.25371)

This is the newest and most directly deadline-oriented source, but it is a single-author v1 preprint rather than peer-reviewed evidence, so its theorem statements are useful as an architectural lead and require independent checking before adoption.

Assumption 1 requires calibration recovery times and the next recovery time to be exchangeable, with non-recovery retained as `+infinity`. The split-conformal deadline is the `ceil((1-alpha)(n+1))` order statistic; Theorem 1 gives marginal `Pr(tau_{n+1} <= d_alpha) >= 1-alpha`. It returns `+infinity` rather than fabricate a finite certificate when the sample size or recovery rate is insufficient; a finite `1-alpha` deadline needs at least `ceil(1/alpha)-1` usable calibration episodes. The paper explicitly notes that the guarantee averages over calibration and fault classes, is not conditional on the fixed calibration set or a hard subclass, and is per controller and per fault class. Its weighted-shift theorem additionally needs the exact likelihood ratio `dQ/dP`; the paper concedes that the proposed batch approximation does not inherit the idealized per-point theorem.

The load-bearing result for this project is Proposition 1, not the conformal quantile itself. It proves per-episode safety only because a separately verified backstop detects the critical limit and a safe controller makes the critical set avoidable. The statistical deadline governs autonomy; the verified backstop governs safety even if exchangeability fails.

**Fit here:** the recovery-time estimand is not resource runtime, and the HCMS environment lacks a formally verified real-time controller. Nonetheless, the reliability-asymmetric decomposition transfers exactly: a statistical upper envelope may decide whether useful work is worth attempting, while deadline safety must be enforced by an independent, testable stop/backstop. A probabilistic predictor should be allowed to fail only by rejecting or truncating a candidate, never by consuming the terminal serialization reserve. That separation is more defensible than asking conformal prediction to become a hard real-time proof.

## Guarantee comparison

| Source / mechanism | Exact guarantee object | Load-bearing assumptions | Handles sequential endogenous costs? | Supports strict total-deadline safety? | Decision for HCMS |
|---|---|---|---|---|---|
| CQR (2019) | Finite-sample marginal upper prediction coverage for one next response | Exchangeable feature-response pairs; calibration kept separate from model fit; coverage marginal over calibration/test | **No, not directly.** Policy-dependent selection and within-cell dependence break the rank symmetry | **No.** `1-alpha` is probabilistic and marginal | Use only as a heteroskedastic upper-cost shape model under episode/group-held-out calibration |
| CRC (2024) | Unconditional expected bounded monotone loss `E[L] <= alpha` | Exchangeable random loss functions; monotonicity, right-continuity, finite bound and safe maximal parameter | **No, unless** the calibration unit is redesigned to recover exchangeability or shift is bounded | **No.** Expected miss rate is not family-wise zero miss | Useful for calibrating a cell-level violation loss or alpha-spent policy, not raw candidate rows |
| Online conformal, decaying steps (2024) | Deterministic bound on retrospective time-average coverage error | Arbitrary bounded score sequence; positive step sizes (non-increasing for the simple rate) | **Yes for average coverage.** No stochastic independence is needed | **No.** Misses may cluster and adaptation occurs after failure | Park as a drift monitor; do not use as the pre-start safety gate |
| Howard et al. (2020) | Time-uniform boundary-crossing probability / confidence-sequence machinery | Adapted process plus a proved conditional `sub-psi` supermartingale or equivalent conditional MGF/bounded-increment condition | **Potentially.** Predictable selection is allowed if the conditional tail condition survives it and censoring is retained | **No by itself.** It bounds probability, not physical execution | Candidate foundation for an anytime risk ledger after the conditional cost process is specified and tested |
| Recovery-deadline certificate (2026 preprint) | Marginal conformal deadline; unconditional safety only through verified backstop | Exchangeable episodes for deadline coverage; sound critical monitor and effective safe fallback for hard safety | **Not for candidate costs as written.** Per-controller/class recalibration is required | **Yes only because of the separate verified backstop**, not because of conformal coverage | Adopt the reliability-asymmetric architecture, not its domain-specific theorem as proof |

## Design implication: replace point admission with a reliability-asymmetric gate

No reviewed statistical method justifies the statement “the next endogenous candidate will finish before the remaining wall-clock time.” The correct replacement is therefore not a larger constant and not a more elaborate point predictor. It is one structural change with two deliberately different responsibilities:

1. **Statistical admission envelope (utility):** before starting a path, compute a one-sided upper cost `U_t` for the *entire atomic future-work unit*—environment construction, reset, controller overhead, candidate interaction, accounting and retained-evidence publication. Condition on only pre-admission observables. Freeze a nonzero violation target and calibration unit before fresh evaluation. The first candidate mechanism should be a simple grouped order-statistic/conformalized upper quantile; online PID-style adjustment is deferred because its guarantee is only retrospective average coverage.
2. **Independent deadline backstop (safety):** reserve a separately measured terminal-publication bound `B_terminal`; admit only when `remaining > U_t + B_terminal`; execute admitted work under a cancellable timeout no later than `deadline - B_terminal`; on timeout, retain the censored observation and publish a valid truncated/invalid candidate record. Strict generation safety is supportable only if timeout delivery plus cleanup has a verified bound. If environment construction cannot be interrupted or bounded, the honest action is to stop before constructing it—no statistical method repairs that physical limitation.

The probability accounting must be at the cell/trajectory level. Either calibrate the loss `1{any admitted operation exceeds its envelope}` directly on independent complete episodes, or preregister per-decision risks `alpha_t` with `sum_t alpha_t <= alpha_cell`; otherwise a seemingly small marginal miss rate compounds over many admissions. Method/prefix/reset strata must be declared before calibration, with an abstain/`+infinity` outcome for strata lacking enough evidence. All attempted starts, timeouts and censored costs must remain in the ledger so adaptive selection cannot silently erase the tail.

This architecture makes a sharp next-hypothesis prediction: compared with the fixed `0.1 s` reserve, it should eliminate terminal overages on fresh cells while preserving most of HCMS's raw advantage; compared with a statistical envelope without a hard backstop, it should differ specifically on injected heavy-tail construction/reset paths, where the envelope-only variant may overrun but the backstopped variant must truncate. If the runtime cannot enforce that truncation bound, the hypothesis should be rejected before another scientific run.

## Conclusion

The literature does not support repairing HCMS-24 by multiplying observed maxima or tuning a reserve. CQR/CRC can supply a finite-sample marginal risk envelope under carefully reconstructed exchangeability; online conformal control can monitor average coverage under arbitrary dependence; confidence-sequence machinery can tolerate adaptive selection only after a conditional tail process is proved. None turns random, potentially unbounded work into hard deadline safety. The defensible engineering pivot is reliability-asymmetric admission: statistical calibration buys utilization, while a separately bounded stop-and-publication path enforces the deadline.

No experiment, code/config change, Kaggle action or submission was performed in this pass.
