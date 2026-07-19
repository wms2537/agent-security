# ORF report revision blueprint — review round 1

**Revision type:** branch-of-origin reconstruction, not local prose repair  
**Trigger:** `research-log/047-orf-paper-review-round1.md`  
**Evidence tier:** deterministic public synthetic tables only  
**Executed-study name:** Public-Synthetic Perfect-Information Regret (PS-PIR)  
**Prospective-only name:** ORF-B / Beacon-Held-Out Conditional Regret  

## Non-negotiable claim boundary

The revised report may claim only that, on three named designer-specified score
tables, allowing a perfect-information row-wise action produces a finite score
gap relative to one exhaustive shared action. It may report exact arithmetic,
action distributions, stratum contributions, and sensitivity calculations for
those tables. It may not call the gap an opportunity beyond those tables, treat
the 5% cutoff as practical materiality, infer learnability, claim an empirical
mechanism, describe the public calculation as untouched confirmation, or imply
that a beacon, held-out tier, Kaggle target, or live system was evaluated.

The correct scientific identity is an internally reproducible scorer worked
example and unit-test artifact. Its conceptual form is established value of
perfect information and policy-class containment. No publication or external
release action is part of this revision.

## Table A — reviewer issue routing to branch of origin

| Issue | Root layer | Required reconstruction | Acceptance test |
|---:|---|---|---|
| 1 | Hypothesis / construction | Replace phenomenon/opportunity framing with designer-specified worked-example framing; add construction-provenance table. | No `opportunity bound`, practical-scale, or external-existence claim. |
| 2 | Novelty | State that the inequality and information-value concept are established; retain only scorer-specific implementation value. | Contributions contain no theorem/concept novelty claim. |
| 3 | Evaluation chronology | Rename Phase 4 as post-calibration frozen public verification and explicitly show no untouched tier. | `confirmatory`, `registered result`, and robustness language removed from scientific interpretation. |
| 4 | Operational estimand | Make perfect counterfactual observability the defining estimand; probes do not choose actions. | Abstract, methods, discussion, and conclusion all deny learner evidence. |
| 5 | Literature model | Add decision-theoretic VOI, contextual bandits/policy evaluation, adaptive optimization, and heterogeneous policy learning. | Ten verified references; closest foundations precede recent LLM neighbors. |
| 6 | Analysis artifacts | Add per-master action histograms and complete stratum regret decomposition; reclassify historical diagnoses as hypotheses. | Tables cover 3 masters, 960 profiles, 40 strata, raw regret 10,380,000. |
| 7 | Mechanism interpretation | Replace attribution language with removal-associated ratio changes; show raw A, G, and A-G. | Six-row core/OAT table present; nonadditivity adjacent. |
| 8 | Statistical model | Remove sample SD and standardized score; report three values/range; rename 5% cutoff. | No inferential/effect-size language for finite census. |
| 9 | Naming | Use PS-PIR for executed calculation; reserve ORF-B for unused prospective protocol. | Title and abstract cannot be misread as held-out evidence. |
| 10 | Reproducibility | Use repo-relative commands; add environment/bootstrap manifest; disclose no external archive. | Clean local bootstrap documented; no machine-specific path. |
| 11 | Motivation/provenance | Cite audited SDK files for scorer/deadline/cap; soften unsupported live causal diagnoses. | Every operational fact has local evidence; causal historical language removed. |
| 12 | Formal notation | Define q >= 0 and branch on q = 0 before saturation. | Zero-yield evaluation order is explicit. |

## Table B — source/exemplar move inventory

| Source | Move to imitate | Constraint on revised prose |
|---|---|---|
| Howard (1966) | Value information through changed decisions, not information alone. | Introduce PS-PIR as a deterministic value-of-perfect-information instance. |
| Langford & Zhang (2007) | Map observable context to actions and analyze regret. | Use as the contrast for the untested context-to-length learner. |
| Dudík et al. (2011) | Evaluate/learn policies under partial feedback and explicit assumptions. | State that a complete counterfactual score table bypasses their central estimation problem. |
| Golovin & Krause (2011) | Separate adaptive policies under observations from fixed policies. | Deny equivalence between PS-PIR's perfect information and operational adaptivity. |
| Athey & Wager (2021) | Learn heterogeneous assignment policies from observed covariates. | Frame the missing selector as policy learning, not as an implementation detail. |
| Snell et al. (2025) | Condition inference allocation on task difficulty and disclose regime dependence. | Position recent adaptive inference as an application neighbor, not conceptual origin. |
| Plan-and-Budget / SCALE | Allocate reasoning resources across subproblems. | Keep quantitative comparisons inside their reported reasoning domains. |
| Paglieri et al. (2026) | Compare learned planning choices with fixed extremes. | Use as evidence of what a deployable learned action policy would need to demonstrate. |
| BAVT (2026) | Tie adaptive tool search to a concrete budget constraint. | Contrast step-level tool-call control with candidate-length scoring tables. |
| SDK scorer/gateway | Define the local score, cap, action cost, deadline, and replay constraints. | Cite exact repository paths; distinguish SDK facts from synthetic choices. |

## Table C — v1 paragraph diagnosis

Paragraph IDs refer to the section source files at committed report `08f300f`.

| V1 unit | Current move | Problem exposed by review | Revision operation |
|---|---|---|---|
| Abstract 1 | Benchmark tension and ORF-B name | Implies operational relevance and held-out evidence. | REWRITE |
| Abstract 2 | 40.249% mean plus sample SD | Treats designed tables like a sample. | REWRITE |
| Abstract 3 | OAT attribution and opportunity language | Overstates nonadditive contrasts and transfer value. | REWRITE |
| Introduction 1 | Deadline/candidate motivation | Facts not tied to auditable SDK locations. | REWRITE |
| Introduction 2 | Live failure causal diagnosis | Timing, reserves, and parsing explanations are not method-backed here. | DELETE/MERGE |
| Introduction 3 | Recent adaptive-allocation gap | Omits foundational policy and VOI literature. | MOVE/REWRITE |
| Introduction 4 | ORF-B estimator | Name and novelty implication are wrong for executed evidence. | REWRITE |
| Introduction 5 | Contributions | Claims an opportunity target and controlled evidence beyond table arithmetic. | REWRITE |
| Related Work 1–2 | Recent LLM adaptive inference | Begins with application neighbors rather than conceptual owners. | MOVE |
| Related Work 3–5 | Five-paper summaries | Too much numeric detail for a narrow internal report. | MERGE |
| Related Work 6 | Bounded novelty close | Still presents exact finite estimand as differentiator. | REWRITE |
| Methodology 1 | Global versus adaptive policies | `adaptive` obscures perfect-information access. | REWRITE |
| Methodology 2 | Containment inequality | Elementary fact is treated as contribution-adjacent. | REWRITE |
| Methodology 3–4 | Score/resource identity | q domain contradiction; SDK and stress-test origins mixed. | REWRITE |
| Methodology 5 | Crossed/homogeneous constructions | Says generator was designed to create phenomenon without limiting inference enough. | REWRITE |
| Methodology 6 | Predictions and taxonomy | Uses materiality and confirmatory framing. | REWRITE |
| Methodology 7 | Assumptions/nonclaims | Correct limits are present but downstream claims exceed them. | MERGE/REWRITE |
| Setup 1 | Fixed master units | Calls labels pre-specified without calibration chronology up front. | REWRITE |
| Setup 2 | Generator constants | Does not disclose that ranges/weights are engineering stress-test choices. | REWRITE |
| Setup 3 | Matched policies | Probes appear operational though oracle ignores them. | REWRITE |
| Setup 4 | OAT/changed/nested studies | `generalization` and `robustness` overstate reused public constructions. | REWRITE |
| Setup 5 | Metrics/statistics | Includes sample SD and standardized mean. | DELETE/REWRITE |
| Setup 6 | Execution/audits | Internal paths and audit claims are not self-contained. | REWRITE |
| Results 1 | Core table and mean | Mean-centered presentation hides named-table nature. | REWRITE |
| Results 2 | Homogeneous control | Treats entailed equality as empirical discriminator. | REWRITE |
| Results 3 | Action-selection behavior omitted | Declared diagnostic missing. | ADD |
| Results 4 | OAT ratio deltas | Raw numerator/comparator/difference missing; causal wording. | REWRITE |
| Results 5 | Changed construction | `generalization` invites transfer interpretation. | REWRITE |
| Results 6 | Scaling | `robustness` invites independent-replication interpretation. | REWRITE |
| Results 7 | Ledger/status | Valuable custody detail dominates main scientific thread. | MOVE |
| Discussion 1 | Primary interpretation | Calls exact table gap a material opportunity. | REWRITE |
| Discussion 2 | Mechanism attribution | Nonadditive transforms cannot support decomposition. | REWRITE |
| Discussion 3 | Historical disconfirmation | Unsupported causal narrative. | REWRITE |
| Discussion 4 | Literature implication | Understates established conceptual prior art. | REWRITE |
| Discussion 5 | Limitations | Strong but repeated across paper. | MERGE |
| Conclusion 1 | Finite result synthesis | Uses confirmed/material/opportunity language. | REWRITE |
| Conclusion 2 | Future target | Blurs worked example and prospective held-out protocol. | REWRITE |
| Supplement S1 | Full ledger | Valuable; statuses retain old labels but are historical records. | KEEP-AS-ARCHIVE |
| Supplement S2 | Chronology | Needs explicit exploration → public freeze → no untouched evaluation. | REWRITE |
| Supplement S3 | Reproducibility | Machine-specific and no bootstrap/lock. | REWRITE |
| Supplement S4 | Custody/governance | Repeated and longer than scientific caveat needs. | MERGE |
| Supplement S5 | Disclosures | Needs revision chronology and review outcome. | REWRITE |

## Table D — target paragraph blueprint

Each row is an obligatory move. Writers may split equations or tables, but may
not omit or broaden a move.

| Target ID | Section | Required move | Evidence anchor | Operation from v1 |
|---|---|---|---|---|
| A1 | Abstract | Name PS-PIR as a deterministic worked example of established perfect-information value. | Howard; C01–C03 | REWRITE |
| A2 | Abstract | Report all three named gains and their range, plus exact homogeneous equality. | core/homogeneous TSV | REWRITE |
| A3 | Abstract | State that 5% was a preselected numerical cutoff without utility calibration. | research-log/018 | REWRITE |
| A4 | Abstract | Deny learner, untouched test, live transfer, beacon, and Kaggle evidence. | state; review issue 4/9 | REWRITE |
| I1 | Introduction | Define the SDK-local shared-length decision and cite scorer/gateway files. | scoring.py; gateway.py; contracts.py | REWRITE |
| I2 | Introduction | Explain why perfect-information value is worth auditing but cannot establish availability of information. | Howard; C04 | REWRITE |
| I3 | Introduction | Reclassify the prior live miss and its proposed causes as historical diagnostic hypotheses. | results.tsv; research-log/002 | REWRITE |
| I4 | Introduction | State executed evidence tier and post-calibration status before contributions. | chronology artifacts | ADD |
| I5 | Introduction | Give three contributions: exact scorer calculation, diagnostics, reproducible record. | generated tables; ledger | REWRITE |
| R1 | Related Work | Establish decision-theoretic information value as conceptual owner. | Howard | ADD/MOVE |
| R2 | Related Work | Contrast observable-context policy learning and partial-feedback evaluation. | Langford; Dudík; Athey-Wager | ADD |
| R3 | Related Work | Contrast partial-observation adaptive optimization with full counterfactual access. | Golovin-Krause | ADD |
| R4 | Related Work | Compress five recent LLM allocation neighbors by allocation granularity and observation. | phase6-primary.json | MERGE |
| R5 | Related Work | Conclude that PS-PIR is a scorer-specific application, not a new regret concept or algorithm. | all ten sources | REWRITE |
| M1 | Methodology | Define table Z, legal M, q >= 0, per-row S, shared G, perfect-information A, Delta, ratio. | config; scorer | REWRITE |
| M2 | Methodology | Branch q=0 before saturation and state H is applied per profile. | checker; scorer | REWRITE |
| M3 | Methodology | Prove only policy-class containment and equality condition. | finite algebra | REWRITE |
| M4 | Methodology | Explain action-distribution/margin dependence without claiming a novel theorem. | score tables | ADD |
| M5 | Methodology | Define crossed/homogeneous tables as designed stress tests and code-path sanity check. | generator; config | REWRITE |
| M6 | Methodology | Present design-provenance table for every constant/range/weight/cutoff. | SDK + project choices | ADD |
| M7 | Methodology | State oracle observability and that retained probes never select an action. | runner; hypothesis | REWRITE |
| E1 | Setup | Separate exploratory calibration, frozen public verification, and absent untouched tier. | logs 007–041 | REWRITE |
| E2 | Setup | Define named deterministic tables and experimental unit without sampling language. | manifests | REWRITE |
| E3 | Setup | Define exhaustive shared comparator and perfect-information row-wise comparator. | core runner | REWRITE |
| E4 | Setup | Define OAT, changed construction, and nested prefixes as sensitivity calculations. | configs; run tables | REWRITE |
| E5 | Setup | Use repo-relative commands and exact environment/bootstrap manifest. | reproducibility README | REWRITE |
| E6 | Setup | Define descriptive outputs: named values/range, action counts, strata, raw A/G/Delta; no test. | generated tables | REWRITE |
| X1 | Results | Report shared action 16 and three named gain values/range before any mean. | core TSV | REWRITE |
| X2 | Results | Report homogeneous zero/length-one as boundary/code-path sanity check. | homogeneous TSV | REWRITE |
| X3 | Results | Report per-master action histograms and interpret only observed dispersion. | action-distributions.tsv | ADD |
| X4 | Results | Report 40-stratum decomposition, zero strata, top-five share, and full-table location. | stratum TSV | ADD |
| X5 | Results | Report core and five OAT raw A/G/Delta plus ratio; use removal-associated language. | oat-raw-summary.tsv | REWRITE |
| X6 | Results | Report changed public construction without `generalization`. | generalization TSV | REWRITE |
| X7 | Results | Report nested-prefix numerical sensitivity without `robustness`. | scaling TSV | REWRITE |
| X8 | Results | State no inferential statistic and no external meaning for 5%. | analysis decision | REWRITE |
| D1 | Discussion | Interpret only exact finite tables and explicitly identify generator selection bias. | design provenance | REWRITE |
| D2 | Discussion | Explain that action dispersion is descriptive evidence of engineered table heterogeneity. | action/stratum tables | REWRITE |
| D3 | Discussion | Treat OAT changes as interacting ratio contrasts, not mechanism shares. | OAT raw table | REWRITE |
| D4 | Discussion | Separate historical miss from current evidence and label diagnoses hypotheses. | results.tsv; log 002 | REWRITE |
| D5 | Discussion | Map missing learner/test/live steps to contextual-policy literature. | foundational refs | REWRITE |
| D6 | Discussion | Consolidate governance: no beacon, held-out, Kaggle, external archive, or submission. | state; permissions | MERGE |
| C1 | Conclusion | State exact contribution as reproducible perfect-information scorer case study. | all result artifacts | REWRITE |
| C2 | Conclusion | State that no agent-security opportunity or deployable gain has been demonstrated. | limitations | REWRITE |
| S1 | Supplement | Preserve full 42-row ledger byte-faithfully and explain historical labels. | results.tsv | KEEP-AS-ARCHIVE |
| S2 | Supplement | Add explicit dated/committed chronology through round-1 review. | git log; logs | REWRITE |
| S3 | Supplement | Map each table/figure/command to repo-relative paths and environment. | repository | REWRITE |
| S4 | Supplement | Include full action and stratum diagnostics or exact source-table references. | generated tables | ADD |
| S5 | Supplement | State internal reproducibility versus absent external archive/durability. | repo state | REWRITE |

## Deep-imitation operation audit

For scientific prose units in Table D, the dominant operation is `REWRITE`;
`ADD` supplies reviewer-required missing moves, while `MERGE` and `MOVE` correct
structure. There are no `KEEP` operations in the scientific narrative. The sole
`KEEP-AS-ARCHIVE` item is the immutable historical ledger, which is evidence
rather than prose. Therefore:

- dominant operation: `REWRITE`;
- scientific-paragraph KEEP fraction: `0%`;
- missing obligatory moves allowed at assembly: `0`;
- unsupported new claims allowed: `0`;
- numerical claims without a local table or verified reference allowed: `0`.

## Writer dispatch contract

Writers receive this blueprint, the verbatim review, the relevant source tables,
and the updated claim map. They must rewrite their section files from the target
moves rather than edit v1 sentence by sentence. Related Work, Methodology, and
Experimental Setup form the first dependency group; Results and Discussion form
the second; Introduction, Abstract, and Conclusion form the third. References
and Supplement are assembled only after all scientific sections stabilize.
