# Phase-6 report outline

**Working title:** *Conditional Regret of Global Candidate Length in a Public
Synthetic Agent-Security Model*

**Document class:** paper-shaped internal technical report; no venue submission.

| Position | Section | Story-arc job | Primary source material |
|---:|---|---|---|
| 01 | Abstract | State the exact finite result and operational non-conclusion in 150-300 words. | narrative arc; research-log/042, /044 |
| 02 | Introduction | Make the replay-budget structure decision concrete, position the adaptive-allocation gap, name ORF-B, and list bounded contributions. | PROBLEM.md; state idea DNA; /002, /018, /043-/045 |
| 03 | Related Work | Organize neighbors into prompt-conditioned compute, learned planning, and budget-aware tool search; deny broad novelty. | lit/phase6-primary.json; /043; /045 |
| 04 | Methodology | Define the finite action-scope estimand, exact containment proof, controls, score identity, assumptions, and prediction taxonomy. | /018; /019; config; SDK fixture description |
| 05 | Experimental Setup | Make public Phase-4 generation, masters, baseline, ablations, changed regime, scales, metrics, provenance, compute, and exclusions reproducible. | environment.md; /023-/041; configs and bundle tables |
| 06 | Results | Present baseline/core, homogeneous negative, attribution, changed-regime, and scaling evidence with descriptive fixed-master statistics and Figures 1-3. | /042; /044; comparison.tsv; figures |
| 07 | Discussion | Explain mechanism, preserve historical disconfirmations and nulls, state concrete failure cases, assess novelty, and distinguish proxy progress from the operational problem. | /002; all results.tsv rows; tried_and_failed; /042-/045 |
| 08 | Conclusion | State what is now known, what failed, and the evidence-bound next step without implying authorization. | narrative arc; full journey; /044 |
| 09 | References | List only the five field-verified primary sources actually cited. | lit/phase6-primary.json |
| S1 | Supplementary material | Full 42-row ledger, configs/artifacts, exact proof, reproducibility, data/code availability, and AI-assistance disclosure. | results.tsv; config; run bundles; state; data-governance.md if present |

## Assembly rules

- Markdown is the primary format because Phase 0 selected a working note and the
  user requested a paper/report, not a submission package.
- Main-text figures are numbered by basename: Figure 1 `comparison_chart`,
  Figure 2 `ablation_heatmap`, Figure 3 `scaling_curve`.
- Primary comparison is pre-specified; every ablation/generalization/scale result
  is labeled secondary or descriptive.
- No headline is called held-out. The locked-test absence appears in Abstract,
  Results, Discussion, disclosures, and the final conclusion boundary.
- No population significance language is permitted. `n=3` means fixed masters.
