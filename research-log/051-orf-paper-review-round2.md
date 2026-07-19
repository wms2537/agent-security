# PS-PIR paper review — round 2 (verbatim)

**Paper-review budget after dispatch:** 2/2 (exhausted)  
**Committed target:** `paper/orf-internal-technical-report.md` at `057f854`  
**Orchestrator line-count verification:** `git show 057f854:paper/orf-internal-technical-report.md | wc -l` -> `1184`

---

# NEEDS_REVISION

Verified: `git show 057f854:paper/orf-internal-technical-report.md | wc -l` returned **1184**, and I reviewed the committed file through line 1184 only.

The report is careful, internally coherent, and unusually honest about its limits. Nevertheless, it does not meet a top-tier ML/systems publication bar: its substantive contribution is exact arithmetic for two nested policy classes on designer-engineered deterministic tables. It offers no novel method or theorem, learned selector, observed systems phenomenon, or externally informative evaluation. Addressing that deficit would require a new substantive contribution or new evidence, not further rhetorical revision.

## Claimed-scope verdict

**SUFFICIENT** for its explicitly claimed **internal technical report / deterministic worked-example** scope.

Within that scope, the report supports its narrow conclusion: on the named supplied tables, the perfect-information row-wise policy has the reported exact advantage over the shared-action policy, while the constructed homogeneous tables exercise the equality path. The paper does not misrepresent this as attainable performance, deployment evidence, population inference, or an untouched evaluation. Two non-conclusion-threatening clarifications remain below.

## Prior-issue resolution

| # | Classification | Current-file evidence | Remaining gap |
|---:|---|---|---|
| 1 | RESOLVED | The abstract, construction section, and discussion repeatedly call the crossed tables “designer-specified,” “engineering stress-test choices,” and nonrepresentative of empirical prevalence; see lines 1–3 and 333–361. | Naturally occurring heterogeneity remains unestablished, but the report no longer claims it. |
| 2 | IMPROVED | The abstract, Related Work, and containment subsection explicitly identify the calculation as established VOI plus elementary policy-class containment, not a new regret concept, theorem, or learner. | Substantive novelty remains absent. This is acceptable internally but remains fatal at a top-tier research-publication bar. |
| 3 | RESOLVED | Lines 411–423 and Supplement S2 disclose adaptive public calibration, construction selection, and the complete absence of an untouched tier. Generalization/test claims are withdrawn. | No untouched evidence exists; none is needed for the narrowed claim. The freeze chronology wording still needs the new-issue correction below. |
| 4 | RESOLVED | Lines 391–405 and the “Missing operational evidence” discussion explicitly state that probes never choose an action, no learner or selector-error curve exists, and no fraction of the oracle gap is shown attainable. | A realizable probe-to-action policy remains separate future work and is not claimed here. |
| 5 | RESOLVED | Related Work now covers foundational VOI, contextual bandits, off-policy evaluation, heterogeneous policy learning, adaptive optimization, and recent LLM resource allocation, while distinguishing their assumptions from PS-PIR. | The coverage is sufficient for the narrow report. |
| 6 | RESOLVED | Lines 599–637 provide action counts and stratum accounting; the complete 40-stratum artifact is identified. Historical latency/parser/reserve explanations are consistently labeled diagnostic hypotheses rather than causal findings. | The decomposition remains engineered-table bookkeeping, correctly stated as such. |
| 7 | RESOLVED | The OAT table reports raw \(A\), \(G\), and \(A-G\). Lines 643–690 and the discussion emphasize that transforms move numerator and denominator, interact, and are neither additive nor causal component shares. | None within the descriptive-sensitivity scope. |
| 8 | RESOLVED | Lines 518–521 and the “Descriptive status” section reject population SDs, standardized effects, confidence intervals, tests, and p-values. The 5% line is repeatedly called an uncalibrated numerical cutoff without practical meaning. | The cutoff remains scientifically arbitrary but is no longer given evidentiary force. |
| 9 | RESOLVED | The executed study is renamed PS-PIR. Lines 210–212 and 401–405 reserve ORF-B / Beacon-Held-Out only for an explicitly unexecuted prospective protocol. | None. No beacon or held-out evidence is implied. |
| 10 | IMPROVED | Lines 523–545 and Supplements S3–S5 provide repository-relative commands, environment versions, dependency files, source-revision and manifest machinery, and SHA-256 binding. | Internal reproducibility is well documented. External durability remains absent—no public clone, archive, container, or bit-for-bit lock—and is honestly disclaimed. |
| 11 | RESOLVED | The design-provenance table separates SDK facts, mixed-provenance modeling choices, and engineering choices. Historical forecast misses are documented, while proposed causes are explicitly unsupported hypotheses. | SDK-path and artifact assertions were not independently checked under this report-only review, but the manuscript no longer converts them into causal evidence. |
| 12 | RESOLVED | Lines 224–268 define \(q_z(m)\geq0\), explicitly give the \(q=0\) branch, and evaluate it before the saturation quotient. | None. |

## New issues

1. **Moderate — the Phase-4 freeze chronology is internally overstated.**  
   **Location:** lines 416–420 versus Supplement S2, especially lines 1014–1030.  
   **Issue:** The main text says “labels, actions, predictions, and public config were frozen in `orf-phase4-v1.json`, after which Phase 4 ran.” The detailed chronology instead shows the config/boundaries frozen first, with baseline, core, OAT, second-construction, and prefix predictions frozen sequentially immediately before their corresponding calculations—and after earlier-family results were already known.  
   **Conclusion impact:** No effect on the exact table arithmetic, but it overstates whole-phase prospective locking and weakens the otherwise careful adaptive-history account.  
   **Fix type:** `fixable`. State that config/actions/boundaries were frozen globally, while each family’s predictions were frozen prospectively relative only to that family’s calculation.

2. **Minor — probe residual state is not fully defined in the manuscript.**  
   **Location:** lines 220–280 and 363–368.  
   **Issue:** \(g_z,r_z,p_z,Q_z\) are introduced as what the seven probes “leave,” followed only by qualitative charging rules. The report never explicitly gives their formulas, starting state, probe order, or precise aggregation from \(c_z(m)\) and \(q_z(m)\). Consequently, the claimed homogeneous “unique row-wise maximizer by construction” is not derivable from the written specification alone; it is supported only through referenced code/results.  
   **Conclusion impact:** Does not contradict the reported finite-table comparison, but weakens methodological self-containment and construction-level reproducibility.  
   **Fix type:** `fixable`. Add the residual-state equations and conditions proving uniqueness, or downgrade “by construction” to an observed property of the generated tables.

No new conclusion-threatening mathematical inconsistency was found.

## Dimension checks

| Dimension | Assessment |
|---|---|
| Evidence backing | **Pass at claimed scope; insufficient for top-tier empirical claims.** The reported totals, gaps, means, action counts, and 10,380,000 aggregate gap are mutually arithmetically consistent. Underlying artifacts are referenced but were outside this sterile report-only review. |
| Methodology–results alignment | **Pass.** Results directly instantiate \(G\), \(A\), \(\Delta\), and \(R\); sensitivity outputs are interpreted as deterministic transformations rather than causal ablations. |
| Notation | **Mostly pass.** The former \(q>0/q=0\) contradiction is fixed. The remaining ambiguity is the undefined construction of \(g_z,r_z,p_z,Q_z\). |
| Related-work fairness | **Pass.** The paper gives conceptual ownership to VOI and clearly distinguishes oracle-table arithmetic from contextual learning, partial-feedback evaluation, adaptive optimization, and LLM allocation systems. |
| Design validity / leakage | **Pass only for the deterministic worked example.** Complete counterfactual access and adaptive generator development would invalidate operational or population conclusions, but both are disclosed and those conclusions are expressly rejected. |
| Baseline fairness | **Pass for policy-class arithmetic.** Both comparators receive identical rows, actions, costs, caps, budgets, and scores; only argmax scope differs. The oracle is correctly not presented as an attainable algorithmic baseline. |
| Statistical discipline | **Pass.** The units are finite named tables, dependent prefixes are identified, means are descriptive, and no unjustified sampling inference or uncertainty estimate is used. |
| Story integrity | **Mostly pass.** The narrative consistently narrows the contribution and preserves failures. The whole-phase freeze sentence conflicts with the detailed chronology and should be corrected. |
| Limitations honesty | **Strong pass.** The manuscript repeatedly and specifically disclaims novelty, attainability, transfer, deployment, causal diagnosis, practical utility, untouched evaluation, and external availability. |
| Reproducibility | **Pass internally, not externally.** Environment, commands, paths, manifests, and dependency records are documented. External archive/durability is absent and accurately disclaimed; self-contained probe-state specification remains incomplete. |
