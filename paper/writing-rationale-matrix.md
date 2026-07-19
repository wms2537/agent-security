# Writing rationale matrix — PS-PIR revision 2

This matrix operationalizes `paper/revision-round1-blueprint.md`. `KEEP` is
prohibited for scientific prose; the historical ledger is the only immutable
archive item.

| ID | Manuscript unit | Function | Evidence anchor | Operation | Completion check |
|---|---|---|---|---|---|
| whole | Controlling structure | Recast an engineered oracle comparison as a deterministic VOI worked example. | Review issues 1–5; narrative arc | REWRITE | No external opportunity or novelty claim. |
| abs-1 | Abstract opening | Name PS-PIR and established perfect-information framing. | Howard; equations | REWRITE | `worked example` or equivalent appears. |
| abs-2 | Abstract result | Report three gains/range and exact equality. | core/homogeneous TSV | REWRITE | No SD or standardized mean. |
| abs-3 | Abstract cutoff | Qualify 5% as internal numerical cutoff. | log 018 | REWRITE | No `material`. |
| abs-4 | Abstract limit | Deny learner/live/untouched/beacon/Kaggle inference. | state | REWRITE | Limit adjacent to result. |
| intro-1 | SDK decision | Ground shared length and resources in audited files. | scoring.py; gateway.py; contracts.py | REWRITE | Paths cited. |
| intro-2 | Conceptual question | Explain value of auditing perfect information without claiming availability. | Howard | REWRITE | Information value separated from observability. |
| intro-3 | Historical miss | Preserve observation, downgrade proposed causes to hypotheses. | results.tsv; log 002 | REWRITE | No causal verb. |
| intro-4 | Evidence tier | State calibration and absence of untouched test. | logs 007–041 | ADD | Before contributions. |
| intro-5 | Contributions | Exact calculation, diagnostics, reproducibility. | tables; manifests | REWRITE | No theorem/algorithm/phenomenon claim. |
| rw-1 | VOI foundation | Identify decision-theoretic owner. | Howard | ADD/MOVE | Opens Related Work. |
| rw-2 | Contextual policies | Explain observable context-to-action learning. | Langford; Dudík; Athey-Wager | ADD | Explicit missing step. |
| rw-3 | Adaptive optimization | Contrast partial observations with full counterfactual table. | Golovin-Krause | ADD | No equivalence claim. |
| rw-4 | Recent neighbors | Compress five LLM allocation papers by axis. | phase6-primary.json | MERGE | Fair domain qualifiers. |
| rw-5 | Novelty close | State scorer-specific application only. | ten-source synthesis | REWRITE | Deny new regret concept. |
| meth-1 | Objects | Define Z, M, q, S, G, A, Delta, ratio. | runner/config | REWRITE | q >= 0. |
| meth-2 | Zero branch | Evaluate q=0 before saturation; H per profile. | scorer/checker | REWRITE | Formal ambiguity removed. |
| meth-3 | Containment | Give finite inequality/equality condition. | algebra | REWRITE | Only statement called proved. |
| meth-4 | Table dependence | Relate gap to row optima/margins descriptively. | score table | ADD | Not a novel theorem. |
| meth-5 | Constructions | Call crossed table a stress test and homogeneous table a sanity check. | generator/config | REWRITE | No empirical discriminator wording. |
| meth-6 | Provenance | Attribute each constant to SDK or engineering choice. | SDK/config/logs | ADD | No unexplained range/weight/cutoff. |
| meth-7 | Oracle | State full counterfactual observability; probes unused for choice. | runner | REWRITE | No attainable fraction implied. |
| setup-1 | Chronology | Separate exploration, public freeze, absent untouched tier. | git/log timeline | REWRITE | Phase 4 called post-calibration verification. |
| setup-2 | Units | Define named deterministic masters, profiles, actions. | manifests | REWRITE | No sample language. |
| setup-3 | Policies | Define exhaustive shared and row-wise perfect-information policies. | core runner | REWRITE | Both use identical tables. |
| setup-4 | Sensitivities | Define OAT, changed construction, nested prefixes. | configs | REWRITE | No generalization/robustness. |
| setup-5 | Reproduction | Give repo-relative bootstrap and commands. | reproducibility README | REWRITE | No absolute home path. |
| setup-6 | Outputs | Define exact values/range/counts/strata/raw scores. | generated tables | REWRITE | test:none; p:n/a. |
| results-1 | Primary | Lead with global m=16 and all three gains/range. | core TSV | REWRITE | Mean is optional/descriptive secondary. |
| results-2 | Equality | Report homogeneous zero and length one as sanity check. | homogeneous TSV | REWRITE | Not independent empirical control. |
| results-3 | Actions | Add per-master action distribution. | action TSV | ADD | Counts sum to 320/master. |
| results-4 | Strata | Add complete decomposition summary and source. | stratum TSV | ADD | 960 profiles; regret 10,380,000. |
| results-5 | OAT | Report raw A/G/Delta and ratio for six rows. | OAT raw TSV | REWRITE | `removal-associated`; nonadditive. |
| results-6 | Changed | Report second public construction. | changed TSV | REWRITE | No transfer implication. |
| results-7 | Prefixes | Report reused nested sensitivity values. | scaling TSV | REWRITE | n remains 3 named masters. |
| results-8 | Statistics | Explain why no inferential statistic is supplied. | design stance | REWRITE | No sample SD/effect size. |
| disc-1 | Scope | Interpret table arithmetic and design selection. | provenance | REWRITE | Magnitude not externalized. |
| disc-2 | Heterogeneity | Interpret action/stratum patterns as engineered-table descriptors. | new diagnostics | REWRITE | Not natural prevalence. |
| disc-3 | OAT | Explain interacting numerator/denominator changes. | OAT raw table | REWRITE | No component share. |
| disc-4 | History | Keep live miss separate; proposed causes remain hypotheses. | results/log 002 | REWRITE | No diagnostic conclusion. |
| disc-5 | Missing science | Map learner/test/live gaps to policy literature. | foundational refs | REWRITE | Concrete requirements, no execution instruction. |
| disc-6 | Governance | Consolidate prohibited/unperformed actions. | state/permissions | MERGE | One short subsection. |
| concl-1 | Contribution | State reproducible scorer case study. | results/artifacts | REWRITE | No concept novelty. |
| concl-2 | Non-conclusion | Deny agent-security opportunity/deployable gain. | limitations | REWRITE | Final sentence preserves gap. |
| refs-1 | References | Include all ten verified sources actually cited. | two literature JSON files | REWRITE | 10/10 cited and field-verified. |
| supp-1 | Ledger | Embed historical 42-row TSV byte-faithfully. | results.tsv | KEEP-AS-ARCHIVE | Bytes identical; old labels identified as historical. |
| supp-2 | Timeline | Add committed exploration/freeze/run/review chronology. | git/logs | REWRITE | Untouched tier visibly absent. |
| supp-3 | Artifact map | List repo-relative code/data/table/figure paths. | repository | REWRITE | Every path exists. |
| supp-4 | Diagnostics | Include or map full action/stratum/OAT tables. | generated tables | ADD | Audit totals present. |
| supp-5 | Reproducibility limit | Distinguish local determinism from absent archive/durability. | repo state | REWRITE | No public-release promise. |
| supp-6 | Disclosure | Update AI/review/iteration and compute disclosures. | state/logs | REWRITE | Counts and limits exact. |

## Matrix audit

- Total rows: 50.
- `REWRITE`: 35; `ADD`: 8; `ADD/MOVE`: 1; `MERGE`: 3;
  `KEEP-AS-ARCHIVE`: 1; controlling/audit rows: 2.
- Dominant scientific-prose operation: `REWRITE`.
- Scientific-prose `KEEP` rows: 0/43 = 0%.
- Every round-1 reviewer issue maps to at least one row.
- Every numerical Results row maps to a committed or newly generated TSV.
