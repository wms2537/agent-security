# Phase-6 report outline — revision 2

**Working title:** *Perfect-Information Regret of a Shared Candidate-Length
Constraint on Deterministic Synthetic Score Tables*

**Document class:** internal technical report and scorer worked example; no venue
submission, external release, archive, or held-out evaluation.

| Position | Section | Required argument | Primary evidence |
|---:|---|---|---|
| 01 | Abstract | Identify established perfect-information framing, give three named results/range and equality check, then state the operational non-conclusion. | Howard; core/homogeneous TSV; scope record |
| 02 | Introduction | Ground the SDK-local shared-length decision, classify the historical miss carefully, disclose public calibration, and list three artifact-level contributions. | SDK files; results.tsv; logs 002/018/041 |
| 03 | Related Work | Lead with VOI/contextual policies/adaptive optimization, then compress recent LLM neighbors and deny conceptual novelty. | both Phase-6 literature databases |
| 04 | Methodology | Define PS-PIR, zero-first score arithmetic, containment/equality, stress-test constructions, design provenance, and oracle boundary. | SDK/config/generator; logs 018/019 |
| 05 | Experimental Setup | Separate exploration from public freeze and absent untouched tier; define named tables, comparators, sensitivities, outputs, and local reproduction. | config; logs 023–041; reproducibility guide |
| 06 | Results | Report named core/equality results, action distributions, stratum contributions, raw OAT values, second public construction, and nested sensitivity. | Phase-4 TSVs; reviewer tables; figures |
| 07 | Discussion | Restrict interpretation to designed tables, explain interacting sensitivities, preserve the live miss as history, and specify the missing learner/test steps. | full ledger/tried-and-failed; foundational refs |
| 08 | Conclusion | State the reproducible scorer case study and deny demonstrated opportunity or deployment value. | complete claim map |
| 09 | References | List ten field-verified sources in citation order. | foundational + recent literature JSON |
| S1 | Supplementary material | Preserve the complete ledger, chronology, artifact/reproduction map, full diagnostics, availability limits, and disclosures. | results.tsv; Git/logs; manifests; state |

## Assembly rules

- PS-PIR names the executed public calculation. ORF-B / Beacon-Held-Out names
  only the unexecuted prospective protocol.
- Figures retain their existing basenames, but captions use `worked example`,
  `removal-associated sensitivity`, and `nested numerical sensitivity` language.
- Phase 4 is `post-calibration frozen public verification`, not confirmation.
- The 5% line is a preselected numerical cutoff without external utility
  calibration; `material` is prohibited as an interpretation.
- No sample SD, standardized score, population significance, CI, p-value,
  generalization, or robustness claim is permitted for the named tables.
- The full 42-row ledger is archival evidence and may retain historical labels;
  narrative prose must identify those labels as historical decision records.
- No text may imply a beacon fetch, held-out freeze/open, target evaluation,
  Kaggle action, learner experiment, external archive, or publication action.
