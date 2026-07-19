# Claim-to-source map — PS-PIR revision 2

Support grades follow `reference/citation-integrity.md`. Local repository files
are primary evidence for SDK and experiment claims. External conceptual claims
use the field-verified `phase6-foundational.json` and `phase6-primary.json`
databases. The final wording column is binding.

| ID | Claim | Type | Evidence | Grade | Required final wording |
|---|---|---|---|---|---|
| C01 | The audited gateway sets a 9,000-second default budget and bounds candidate/replay slices. | SDK fact | `comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py` | strong | Say audited local gateway, not universal benchmark behavior. |
| C02 | The scorer gives +2 per unique qualifying cell and applies a normalization/cap path with H=200,000. | SDK fact | `comp/sdk/aicomp_sdk/scoring.py` | strong | Cite path; distinguish SDK fact from synthetic generator. |
| C03 | Attack contracts expose a time-budget field whose semantics constrain candidate generation. | SDK fact | `comp/sdk/aicomp_sdk/attacks/contracts.py` | strong | Do not infer an empirical latency distribution. |
| C04 | Perfect-information value is an established decision-theoretic concept. | background | Howard 1966 | strong | PS-PIR is an application, not a new concept. |
| C05 | Contextual-bandit and policy-learning work chooses actions from observable context and evaluates a policy under partial feedback/identification assumptions. | background | Langford-Zhang 2007; Dudík et al. 2011; Athey-Wager 2021 | strong | Contrast with full counterfactual access; do not claim identical setting. |
| C06 | Adaptive-submodular optimization distinguishes adaptive policies conditioned on observations from fixed choices. | background | Golovin-Krause 2011 | strong | Use as conceptual contrast, not claim PS-PIR satisfies submodularity. |
| C07 | Recent LLM work adapts inference, planning, or tool-search allocation by prompt/subproblem/step information. | background | five papers in `phase6-primary.json` | strong | Preserve each paper's task/domain qualifiers. |
| C08 | General adaptive allocation is prior art; PS-PIR has no general novelty claim. | synthesis | C04–C07 | strong | `scorer-specific worked example`. |
| C09 | On any fixed finite table, A=sum row maxima is at least G=max shared-action sum. | formal | log 018 derivation; log 019 review | strong | Only policy-class containment is proved. |
| C10 | Equality holds when a single action is row-optimal everywhere; positive gap requires loss from a shared action on at least one row. | formal | elementary derivation; score tables | strong | No population/mechanism inference. |
| C11 | PS-PIR grants every row's complete counterfactual action scores; retained probes do not choose the action. | method | hypothesis v9; Phase-4 runner | strong | Call it perfect-information/oracle, never deployable adaptive policy. |
| C12 | Legal lengths are {1,2,4,8,16,24,32}; q may be zero and the zero branch precedes saturation. | method | config/checker/generator | strong | Define q>=0 and evaluation order. |
| C13 | The crossed construction deliberately varies reset, linear, curvature, and cliff factors over equally weighted strata. | method | Phase-4 config/generator | strong | `designer-specified stress test`; no empirical prevalence. |
| C14 | The homogeneous construction fixes the row-wise optimum at length one by construction. | method | generator/homogeneous TSV | strong | `boundary/code-path sanity check`, not empirical discriminator. |
| C15 | Every synthetic range, weight, replay reserve, and cutoff is an engineering choice unless directly inherited from SDK code. | provenance | config/log 018 + C01–C03 | strong | Table each origin; do not say empirically calibrated. |
| C16 | The 5% line was selected internally before Phase-4 calculations but has no external utility calibration. | decision record | log 018; review issue 8 | strong | `preselected numerical cutoff`, never `material`. |
| C17 | Phase 4 followed adaptive public exploration/calibration and had no untouched evaluation tier. | chronology | logs 007–041; state | strong | `post-calibration frozen public verification`. |
| C18 | The three named crossed-table gains are 41.437632336565%, 38.111186959411%, and 41.198294770946%; range 38.111186959411–41.437632336565%. | quantitative | `core-by-master.tsv` | strong | Report named values/range; no SD, CI, p, or standardized score. |
| C19 | The shared comparator selects length 16 for each crossed master. | quantitative | core/action TSV | strong | Exact table fact. |
| C20 | Homogeneous tables have zero raw regret and both policies select length one. | quantitative | homogeneous TSV | strong | Sanity-check scope only. |
| C21 | Row-wise selections across the three masters use lengths 4/8/16/24/32 with counts recorded per master; lengths 1/2 are unused. | quantitative | `paper/tables/action-distributions.tsv` | strong | Descriptor of engineered tables only. |
| C22 | The stratum decomposition covers 40 strata, 960 profile rows, total regret 10,380,000; four strata have zero regret and the top five contribute about 47.843%. | quantitative | `paper/tables/stratum-regret-decomposition.tsv` | strong | Contribution accounting, not causal shares. |
| C23 | Core mean raw A/G/Delta are 12,062,550.667/8,602,550.667/3,460,000.000; each OAT row has analogous raw values. | quantitative | `paper/tables/oat-raw-summary.tsv` | strong | Report removal-associated changes and nonadditivity. |
| C24 | Removing cliffs and reset produces the two largest decreases in the displayed percentage ratio; unsaturation increases it. | association | OAT raw summary + ablation TSV | strong | `largest removal-associated changes`; never `account for`. |
| C25 | The second public construction has gains above 5% for its three named masters and mean 36.393868336949%. | quantitative | generalization-by-master TSV | strong | `changed public construction`, not generalization/replication. |
| C26 | Nested prefixes N=40/160/320 yield means 48.952971791444/42.794164975019/40.249038022308% on reused masters. | quantitative | scaling-by-cell TSV | strong | `numerical sensitivity`; not robustness, learning curve, or n=9. |
| C27 | A previous live aggregate scored 36.705 against an approximately 85 forecast. | historical result | results.tsv; log 002 | strong | Historical context outside PS-PIR. |
| C28 | Latency, reserve, parsing, and aggregation explanations for that miss were proposed project hypotheses, not identified causes in PS-PIR. | historical interpretation | log 002; absence of protocol in current methods | strong for classification | Use `hypotheses` or `possible explanations`; no causal conclusion. |
| C29 | No learner, live target, beacon, held-out freeze/open, or Kaggle action was executed for PS-PIR. | scope | state; run artifacts; user authorization | strong | Direct non-claim; not a passed test. |
| C30 | Local code/config/tables/manifests/figures can be replayed from the repository, but no external archive, DOI, or durability guarantee exists. | availability | repository; reproducibility manifest | strong | Internal reproducibility only; no publication-readiness claim. |
| C31 | Scientific Phase-4 runtime totals 4.456198161 s and maximum peak memory is 0.583507538 GB. | compute | logs 041/042; results.tsv | strong | Not hardware-normalized energy. |
| C32 | The report used AI-assisted planning, drafting, analysis, and review under human direction. | disclosure | project record | strong | Internal disclosure; no venue-policy claim. |

## Gate audit

- Metadata-only substantive claims: 0.
- Method, mechanism, and numerical claims backed only by background sources: 0.
- Unsupported causal claims: 0 after C28 downgrade.
- New numerical claims without an identified table: 0.
- Claims of learner value, live transfer, held-out confirmation, beacon use, or
  Kaggle improvement: prohibited by C11, C17, and C29.
