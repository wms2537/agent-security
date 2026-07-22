Status: DONE

File reviewed: `research-log/171-hypothesis-iter-8-ahcms24-v3.md`
Line count: **632** in both the working tree and `HEAD`.

## 1. Blind Assessment

### Previous-review issue disposition

1. **Genuine held-out component ablations — RESOLVED.**
   The unsupported replay-envelope and atomic-gate components are deleted from the contribution. The sole retained component is prospectively toggled over the same nine fresh, q-independent complete traces (`absorb` versus `retry`; lines 36–40, 240–280, 370–390).

2. **Distinct bottlenecks or reduced component claim — RESOLVED.**
   The claim is reduced to absorption alone. Its profile is component-specific: HCMS has 146 post-trigger paths consuming 18.3665 seconds for 18 recovered raw; the broader primary grid has 415 paths and 59.1819 seconds for 54 raw (lines 169–204, 370–388).

3. **Test absorbing-only explanation first — RESOLVED.**
   Absorbing-only is now the hypothesis and primary removal, not one term in a three-component account (lines 29–30, 372–390, 583–587).

4. **Correct tied-rank wording — RESOLVED.**
   Lines 424–439 correctly prove failure through selection of the unique strict maximum. Under ties, failure probability is zero; no unjustified uniform-rank claim remains.

### Justification Correctness

The core algebra is correct. From

\[
W_r=W_a+W_t,\qquad R_r=R_a+R_t,
\]

one obtains

\[
\frac{R_a}{W_a}>\frac{R_r}{W_r}
\iff R_aW_t>R_tW_a
\iff \frac{R_a}{W_a}>\frac{R_t}{W_t},
\]

when the relevant denominators are positive. The text correctly treats the `1.10` margin as an empirical prediction rather than deriving it from this identity.

The historical finite-population bound is also correct: evaluation exceeds calibration maximum only when it receives the unique strict maximum; this occurs with probability `1/(n+1)` if such a maximum exists and zero otherwise.

The measured profile is real and source-bound. I reran the read-only sealed-artifact audit; it verified all eleven hashes and reproduced:

- 415 primary post-no-fit paths / 59.181928537553 seconds / 54 raw;
- 146 HCMS post-no-fit paths / 18.366501234705 seconds / 18 raw;
- `39240/39258 = 0.999541494727` retention;
- retrospective efficiency projection `1.355754716874`;
- zero estimable old `2^3` factorial cells.

The old run was invalid for its original joint claim, but it was complete and sealed. Using it only as retrospective bottleneck profiling—not confirmation—is defensible.

However, three new specification defects prevent a rigorous verdict:

1. **The simple-control Occam test is misaligned with the headline endpoint** — lines 320–325, 332–355, 407–417.
   `rho_simple` compares only raw, while the headline system endpoint is raw per generation-work second. AHCMS can pass `R_ahcms >= 1.10 R_simple` while a simpler fixed method has substantially greater efficiency or dominates under the stated work constraint. Therefore the current predicate does not establish the assertion that it “rejects HCMS complexity.” Compare the complete constrained endpoint against the simple controls, require non-domination on raw and work, or narrow the claim explicitly to an internal HCMS transition improvement.

2. **The zero-overage endpoints are not operationally defined** — lines 126–136, 140–152, 282–329, 332–344.
   The entry never states whether a generation-overage cell is `W_m(u)>2`, captured terminal wall time exceeding two seconds, or a quantity including controller/loop/serialization overhead. This matters because no method executes live during offline projection. Likewise, aggregate replay overage needs an explicit formula specifying which accepted candidates’ actual replay durations are summed and the strict boundary. A core confirmation predicate is therefore not independently reproducible from the entry.

3. **Raw-denominator validity domains are missing** — lines 288–329 and 469–490.
   `Delta_E` divides by `E_retry`; `rho_raw` and `rho_tail` divide by `R_retry`; `rho_simple` divides by the best simple raw. Checking only `W_m>0` does not make these denominators positive. Fresh traces could produce zero raw. The contract must state whether each zero-denominator case is disconfirming or invalid and why.

### Mathematical Depth & Validity Domains

The mathematics is appropriately modest rather than decorative. Symbols are mostly tied to concrete path work, raw credit, and replay charge. The efficiency identity and strict-maximum proof are both unpacked correctly.

The missing denominator domains and undefined overage accounting remain load-bearing boundary failures. In addition, `rho_raw >= 0.995` and `rho_tail <= 0.005` are algebraically equivalent under the stated raw decomposition; retaining both is harmless but redundant.

### Logical Soundness

The matched-trace design is strong: complete potential outcomes are captured before projection, the primary pair is identical before the trigger, and absorption is an exact prefix truncation. It avoids method-order, predecessor, cache, and scheduling contrasts by construction.

The scope is honestly narrow: deterministic controlled mocks, three profiles, nine realized units, and no population, target-model, leaderboard, or hard-deadline inference. Claim verbs do not exceed the project’s predictive question type.

Logical closure still fails at the undefined overage predicates and the raw-only Occam comparison.

### Assumption Completeness

The major attribution assumptions are explicitly stated with appropriate regimes, especially potential consistency only for deterministic mocks and no target transfer.

Missing assumptions or decision rules:

- positivity of all raw quantities used as denominators;
- the exact accounting support of generation and replay overages;
- whether simple-control adequacy is judged by raw, efficiency, or Pareto dominance.

### Taxonomy Verification

The classification is accurate:

- **Resource Bottleneck**, secondarily Failure/Risk Gap;
- **Artifact/System**, secondarily Robustification;
- dominant operation **replace**.

This is a local replacement of retry-after-saturation by absorption. It is not Bridge Opportunity × Synthesis/Unification, so the heightened Bridge×Synthesis tripwire does not apply.

### Anti-Stacking Check

The revised hypothesis passes the engineering anti-stacking structure:

1. One component targets a numerically measured bottleneck.
2. It has a genuine same-trace removal.
3. The claimed contribution is a constrained end-to-end result, not the act of combining components.

The replay envelope and atomic gate receive no component credit. This is no longer stacking.

### Occam’s Razor Check

The principal earlier Occam defect is fixed: absorption alone is now tested first. Fixed8 and fixed24/no-salvage are also included.

The remaining raw-only comparator does not fully test whether those simpler systems explain or outperform the stated efficiency outcome. Thus the Occam check is improved but not complete.

### Alternative Explanations

The entry appropriately anticipates absent saturation, valuable recovery tails, unnecessary HCMS complexity, profile-specific effects, metric mismatch, residual replay risk, and target-scale reversal.

The strongest objection I stress-tested was that the bottleneck profile came from an invalid earlier experiment. That objection does not invalidate the profile itself: the run was complete and hash-sealed, the relevant tail values are directly reconstructible, and the entry expressly treats them as retrospective design evidence only. It would invalidate confirmation, which the entry does not claim.

The literature is non-load-bearing, and its principal boundary statements are faithful: CQR provides marginal coverage under exchangeability, not cellwise hard safety, and the cited recovery-deadline work separates statistical coverage from a verified backstop. [NeurIPS CQR paper](https://proceedings.neurips.cc/paper_files/paper/2019/file/5103c3584b063c431bd1268e9b5e76fb-Paper.pdf), [Shojaei preprint](https://arxiv.org/abs/2606.25371).

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. Align the fixed8/fixed24 Occam comparison with the stated end-to-end efficiency/work objective, or narrow the claim that the comparator rejects HCMS complexity — lines 320–325 and 407–417.
2. Give exact per-unit formulas and accounting boundaries for generation- and aggregate-replay-overage cells — lines 126–136, 282–329, and 332–344.
3. Specify zero-denominator handling for `Delta_E`, `rho_raw`, `rho_tail`, and `rho_simple` — lines 288–329 and 469–490.

## 2. Actionable Coaching

- Define projected resource endpoints explicitly, for example:
  \[
  G_m(u)=\sum_{t\in P_m(u)}d_{u,t},\qquad
  O_G(m)=\sum_u \mathbf{1}[G_m(u)>2],
  \]
  and an analogous actual-replay sum over accepted candidates. If controller or serialization time is excluded, call this a **generation-work overage**, not a wall-clock generation overage.

- Replace `rho_simple` with a comparator that matches the goal. A Pareto rule is clearest: AHCMS must not be dominated by either simple control in raw and generation work, with a preregistered materiality requirement on at least one dimension.

- State exact handling for all-zero raw. For example, `R_retry=0` could be predefined as disconfirmation because no useful retained system exists; a zero simple-control denominator needs a separate deterministic convention.

- Collapse the redundant retention predicates or explicitly note:
  \[
  \rho_{\text{raw}}=1-\rho_{\text{tail}}.
  \]
  Keeping both should be described as a consistency assertion, not two independent pieces of evidence.

- Preserve the existing provenance discipline in the next revision: name the sealed artifact, its invalid-but-complete status, the audit command, and the reconstructed component numbers together.
