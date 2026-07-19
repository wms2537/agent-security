# ORF paper review — round 1 (verbatim)

**Paper-review budget after dispatch:** 1/2  
**Committed target:** `paper/orf-internal-technical-report.md` at `08f300f`  
**Orchestrator line-count verification:** `git show 08f300f:paper/orf-internal-technical-report.md | wc -l` → `629`

---

**Status: DONE**

Reviewed file: `paper/orf-internal-technical-report.md`  
Line count: **629**

# Blind assessment

## Overall: NEEDS_REVISION

I would not vote to accept this at NeurIPS/ICML. The exact finite-table calculation appears careful, auditable, and honestly scoped, but the paper does not establish a scientific phenomenon beyond a deliberately heterogeneous synthetic construction, nor does it contribute a learned method. The 40.249% headline is therefore a property of a designer-chosen table and oracle policy class, not evidence about an agent-security system or population.

## Issues ordered by severity

1. **The construction engineers the phenomenon whose magnitude is then reported.**  
   **Location:** Methodology, “Crossed and homogeneous constructions,” especially lines 212–228; “Public masters and profile generator,” lines 256–263; Discussion, lines 449–457.  
   The crossed generator is explicitly “designed to create profile-dependent cost and yield curves,” with uncalibrated bands, cliff frequencies, and equal stratum weights. The homogeneous control fixes the same optimum by construction. Thus positive crossed regret and zero homogeneous regret are not empirical discriminators; only the exact magnitude is computed. The “changed” construction remains in the same hand-designed family and changes several choices simultaneously.  
   **Conclusion impact:** The 40.249% cannot support even the existence or practical scale of an opportunity outside these exact tables. Calling it a “benchmark-shaped opportunity bound” risks giving arbitrary synthetic ranges more scientific meaning than they have.  
   **Fix type:** `downgrade` — position the result as a deterministic worked example or scorer/unit-test artifact. A stronger scientific claim requires new empirically calibrated or untouched external data, not manuscript revision.

2. **There is little conceptual novelty beyond an elementary policy-class containment calculation.**  
   **Location:** Introduction contributions, lines 38–46; Methodology, lines 157–183; Related Work positioning, lines 138–150 and 469–473.  
   \(\sum_z\max_m S_z(m)\geq\max_m\sum_z S_z(m)\) is a standard value-of-perfect-information/policy-class containment fact. The homogeneous equality check is entailed once all row-wise maximizers are fixed to one. This is not “stacking”—the paper cleanly changes one component—but it also does not offer a new algorithm, theorem, identifiable mechanism, or empirically distinguishing prediction.  
   **Conclusion impact:** SDK-faithful computation alone is too narrow for a top-tier contribution paper.  
   **Fix type:** `downgrade` — retain it as an internal technical report, unless a new contribution is added, such as a learnable selector with a regret characterization and external evaluation.

3. **The “registered” result follows extensive adaptive construction and calibration, with no untouched test.**  
   **Location:** Results, lines 428–441; Supplement S2, lines 555–578; S5, lines 612–623.  
   Before Phase 4, the project had a 49.277% PoC, six repaired exploratory calibration conditions that all cleared their thresholds, nine written hypothesis revisions, and eleven theory-review rounds. The Phase-4 predictions then closely match the realized numbers. The authors disclose this well, but “pre-specified” means only before the corresponding calculation, not before selection of the generator family or ranges. The changed construction is also public and non-held-out.  
   **Conclusion impact:** Registration does not give the 40% magnitude confirmatory force; it may be a survivor of adaptive generator and analysis choices. It remains an exact description of the selected table only.  
   **Fix type:** `downgrade` — describe Phase 4 as post-calibration verification. Confirmation or robustness requires a genuinely frozen, untouched tier.

4. **The operationally relevant prediction—whether probes permit action selection—is not tested.**  
   **Location:** Introduction, lines 28 and 34–46; Assumptions, line 246; Matched policies, line 267; Discussion, lines 477–479.  
   `ADAPTIVE` observes every full counterfactual action score. The retained probes do not drive its decision, and the information/computation needed to know all action scores is not an operational resource. No probe-only classifier, contextual baseline, or selector-error curve is evaluated.  
   **Conclusion impact:** The motivating claim that live observations could support model-specific allocation remains wholly untested. The result is only perfect-information value, not evidence that any fraction is attainable.  
   **Fix type:** `downgrade` — keep “perfect-information finite gap” as the sole claim. A learner experiment would be new work.

5. **The novelty review omits the most relevant foundational literatures.**  
   **Location:** Related Work, lines 48–151 and 469–473.  
   The five recent LLM papers are represented fairly and are not strawmanned, but they are not the closest conceptual prior art for max-after-context versus one global action. The paper needs decision-theoretic value of information, contextual decision policy/contextual bandit oracle comparisons, personalization versus uniform policies, and adaptivity-gap work.  
   **Conclusion impact:** The remaining novelty may be substantially narrower than the paper’s “exact finite estimand” framing suggests.  
   **Fix type:** `fixable` — expand prior art and explicitly frame ORF-B as an application of an established quantity.

6. **A declared primary diagnostic is retained but not reported.**  
   **Location:** Metrics, line 277; primary results, lines 308–359.  
   The methods say global selected length and adaptive length counts are retained, but the main results omit them. The artifacts show that global length is 16 for all masters and adaptive choices are spread over 4, 8, 16, 24, and 32. This distribution is the direct evidence for the heterogeneity that produces regret. Historical live results discussed at lines 463–467 have the opposite problem: causal diagnoses are reported without a corresponding experimental methodology.  
   **Conclusion impact:** Readers cannot see whether the 40% is broad across profiles or dominated by a small designed subset, and cannot evaluate the historical causal story.  
   **Fix type:** `fixable` — report the per-master action histograms and stratum-level regret decomposition; either document the historical diagnostic protocol or label those explanations as hypotheses.

7. **The OAT interpretation exceeds what nonadditive ratio contrasts establish.**  
   **Location:** Figure 2 caption, lines 384–388; Discussion, line 451; Conclusion, line 483.  
   “Cliffs and reset overhead account for most of the observed magnitude” sounds decompositional or causal. The transforms interact, and each reported change is a difference between ratios whose \(A\) and \(G\) denominators can both change. The paper itself acknowledges nonadditivity.  
   **Conclusion impact:** The claimed mechanism attribution is stronger than the evidence.  
   **Fix type:** `fixable` — say only “produced the largest removal-associated changes,” and report transformed raw \(A\), \(G\), and \(A-G\), not only percentage-gain deltas.

8. **The statistical presentation is internally inconsistent with the finite-census stance.**  
   **Location:** Abstract, lines 12–16; Metrics, lines 277–279; Results, lines 324–330.  
   The paper calls the three masters a deterministic finite census but reports a **sample** s.d. using the \(n-1\) denominator. For the three named values, finite-population s.d. is about **1.515 pp**, not 1.855 pp. The “standardized mean over measured-master s.d.” of 21.694 has no defined inferential or effect-size interpretation and resembles a signal-to-noise statistic despite repeated caveats. The 5% “materiality” threshold also has no external utility justification.  
   **Conclusion impact:** This can exaggerate the appearance of statistical evidence and gives “material” an unjustified practical meaning.  
   **Fix type:** `fixable` — report the three values and range; remove the standardized quantity. Call 5% a “preselected numerical threshold,” or justify it externally.

9. **The method name implies evidence that explicitly does not exist.**  
   **Location:** Abstract, lines 9–24; S4, lines 604–610.  
   “Beacon-Held-Out Conditional Regret” is used although no beacon was fetched and no held-out tier was frozen or opened.  
   **Conclusion impact:** A reader can reasonably misread the evidence tier from the name before reaching the disclaimers.  
   **Fix type:** `fixable` — rename it to reflect public-synthetic oracle regret, or clearly mark “Beacon-Held-Out” as an unused prospective protocol rather than the executed study.

10. **External reproducibility is not publication-ready despite strong internal reproducibility.**  
    **Location:** Execution, lines 281–299; S3–S4, lines 583–610.  
    Commands, master labels, arithmetic, and local artifacts are unusually detailed. However, the paper explicitly has no archived release, DOI, durability guarantee, or pinned commit, and gives only a partial package/environment description. Absolute local paths are not externally usable.  
    **Conclusion impact:** A competent reader outside this workspace cannot reproduce the experiment from the publication package.  
    **Fix type:** `fixable` — archive a commit, provide a dependency lock/container and clean bootstrap instructions, and replace machine-specific paths.

11. **Several factual motivation and provenance assertions lack manuscript-level support.**  
    **Location:** Introduction paragraph 1, line 28; Introduction paragraph 2, line 30; execution/audit claim, lines 293–295; Discussion, lines 463–467.  
    Unsupported assertions include the exact benchmark deadline/2,000-candidate rules and live observability; the causal claim that longer candidates were latency-bound; reserve firing frequency; Gemma/Harmony parsing harm; and “independent audits” without identifying an audit protocol or artifact in the manuscript. The ledger supports scores but not all causal diagnoses.  
    **Conclusion impact:** These claims motivate the research question and are used to interpret the historical failure; without evidence, readers cannot distinguish diagnosis from plausible post-hoc explanation.  
    **Fix type:** `fixable` — cite the official benchmark/SDK specification and add raw timing/firing/parsing evidence or soften the claims.

12. **One notation contradiction affects zero-yield reproduction.**  
    **Location:** Exact score/resource identity, lines 197–208.  
    The paper defines \(q_z(m)>0\) and immediately specifies behavior when \(q_z(m)=0\).  
    **Conclusion impact:** The intended domain and evaluation order for zero-yield actions are formally ambiguous.  
    **Fix type:** `fixable` — define \(q_z(m)\geq0\), then branch before the saturation expression.

## Dimension-by-dimension assessment

- **Evidence backing:** The finite numerical results are backed by equations, commands, hashes, and local artifacts. Unsupported benchmark and historical causal assertions are listed above.
- **Methodology–results alignment:** Every Phase-4 result family has a described method. The main mismatch is omission of adaptive action counts/global actions; historical causal results lack methods.
- **Notation consistency:** Mostly strong; the \(q_z(m)>0\) versus \(q_z(m)=0\) contradiction should be corrected.
- **Limitations honesty:** Strong. The paper repeatedly and substantively acknowledges oracle observability, synthetic construction, no learner, no locked test, no replay-tail model, and no transfer. It does not hide these behind generic future-work language.
- **Related-work fairness:** The five cited papers are represented cautiously and fairly, but the search is too narrow to evaluate conceptual novelty.
- **Anti-stacking check:** No stacking problem; this is one isolated action-scope change. The failure is lack of conceptual/empirical innovation, not component stacking.
- **Internal contradiction:** Main tensions are finite census versus sample s.d., “Beacon-Held-Out” versus no held-out operation, and confirmatory language after adaptive public calibration.
- **Coherence and flow:** The problem → estimand → exact result → limitations arc is clear. Repeated custody/Kaggle authorization material distracts from the scientific thread.
- **Story integrity:** Stronger than typical. Failed predictions, crashes, repairs, and live disconfirmations are disclosed. The paper is not sanitized, though Phase-4 “registration” must remain explicitly post-calibration.
- **Reproducibility:** Excellent inside the repository; incomplete as a shareable publication artifact.
- **Statistical discipline:** Correctly avoids p-values, CIs, pseudoreplication, and difference-in-significance arguments; discloses the number of revisions. The sample-s.d./standardized-mean presentation is nevertheless inappropriate for its stated census estimand.
- **Design validity and leakage:** This is the main blocker. Public tuning, deliberately heterogeneous construction, arbitrary support weights/ranges, and no untouched test dominate all other bias surfaces. Missing/crashed runs and dependence are disclosed appropriately.
- **Baseline fairness:** `PROBE_GLOBAL` is exact and fairly matched for the stated restricted policy class. It is not under-tuned. The comparison is still an oracle-class contrast, not a deployable baseline comparison.
- **Claims versus evidence breadth:** The abstract and conclusion are commendably narrow. The “material,” “opportunity,” and OAT mechanism language still exceeds what arbitrary public synthetic tables support.

# Actionable coaching

## Title and abstract

- Replace **“Beacon-Held-Out”** and lead with the actual evidence tier, e.g. “Perfect-Information Regret of a Shared Candidate-Length Constraint on Deterministic Synthetic Score Tables.”
- Rewrite “On `n=3` fixed public synthetic masters…” as “Across three named deterministic tables…” and report the three values or range. Remove the standardized mean/s.d. statistic.
- Replace “material” with “above the preselected 5% numerical threshold.”

## Introduction

- After “what exact score is lost…,” state the narrow answer in one sentence: this is an EVPI-style diagnostic on designer-specified tables, not evidence that context is informative or observable.
- Cite the official benchmark specification for the deadline, replay cap, score normalization, and model-observation rules in the opening paragraph.
- The paragraph beginning “The project history makes this concern concrete” should either link to a documented latency/reserve/parser analysis or be shortened to “a prior live result underperformed its forecast; the causes listed below remain diagnostic hypotheses.”

## Related Work

Add foundational references on:

- Howard/Raiffa–Schlaifer value of information and perfect-information decisions;
- contextual policies and contextual bandits, such as Langford & Zhang’s epoch-greedy formulation and Dudík et al.’s off-policy evaluation/learning;
- adaptivity gaps/adaptive optimization, e.g. Golovin & Krause;
- personalization or heterogeneous-treatment policy value versus a uniform action.

Then describe ORF-B as a scorer-specific instantiation, not a new regret concept.

## Methodology

- Add a table explaining the empirical or engineering origin of every range, cliff frequency, stratum weight, budget, and 5% threshold. If none is empirical, label them stress-test choices.
- Prove or characterize how regret depends on the distribution of row-wise optimal actions and margins. That would be more informative than three hash masters.
- Define a realistic observation \(x_z\) derived only from retained probes, and report both oracle regret and achievable policy value \(S_z(\pi(x_z))\).
- Correct \(q_z(m)\geq0\) and state clearly whether \(H\) is applied per profile or to the aggregate.

## Experimental setup

- Separate chronology into “exploratory calibration,” “frozen public verification,” and “untouched evaluation.” The current Phase 4 belongs in the second category.
- Archive and pin the repository, add an environment lock/container, and provide commands relative to repository root.

## Results

- Report the action distributions. The existing artifacts show global length 16 for all three masters, while adaptive choices span lengths 4/8/16/24/32. Include these counts and stratum-level regret contributions.
- Report raw \(A\), \(G\), and \(A-G\) for every OAT condition. Ratio deltas alone obscure whether the numerator, comparator, or both changed.
- Remove: “The standardized mean over the measured master s.d. was 21.694…” It has no defensible interpretation here.
- Call the nested-prefix figure a numerical convergence/sensitivity display, not “robustness,” because it reuses the same generated support.

## Discussion and conclusion

- Replace “cliffs and reset overhead account for most” with “their removal produced the two largest observed changes in percentage regret.”
- Treat the homogeneous result as a code-path/boundary sanity check, not a “necessary” empirical control.
- Move repeated custody, authorization, and Kaggle statements to one short limitations/governance subsection. Preserve the crucial scientific limitations: no learner, no calibrated latency model, no untouched test, and no live-transfer evidence.
- End with the exact defensible contribution: a reproducible case study showing how to compute perfect-information regret for one scorer—not a demonstrated agent-security opportunity.

## Supplement

- Keep the full ledger; it is valuable for story integrity.
- Add timestamps/commit IDs that visibly place PoC, calibration, generator freeze, prediction registration, and evaluation in chronological order.
- Attach the raw evidence for latency, reserve firing, parsing failures, and any claimed independent audit, or reclassify those entries as hypotheses rather than established diagnoses.
