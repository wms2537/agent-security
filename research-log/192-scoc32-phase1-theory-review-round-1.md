Status: NEEDS_REVISION

File reviewed: `research-log/191-scoc32-phase1-hypothesis-lock.md`

review_integrity=PASS reviewed_lines=84

SHA-256: `7ab83cc53f88b3806cd062ac582506935844d571b0248e2f08d07fdcad56a0a0`

## 1. Blind Assessment

### Justification Correctness

The contribution is falsifiable, but the current formalization is under-specified for a predictive engineering claim. In particular:

1. The central SCOC comparison does not define the full CHAIN_FULL and CHAIN_COMPACT formulas in this artifact, only the SCOC closed form (`R_scoC = 16m + 2`) and a single-template single-full baseline (`R_single = 18m`). That makes the headline claim “`CHAIN_SCOC` must beat `CHAIN_FULL`” non-verifiable inside the file: the comparison set is incomplete for reproduction by a reader.

2. The coverage condition is declared as `cov >= 0.95` (global) and “same chain length,” but there is no explicit formula for exact-event overlap with `SINGLE_FULL` on fixed payload syntax. Without that explicit overlap operator semantics and trace-matching rules, coverage equivalence itself is not testable.

3. `SINGLE_FULL`, `CHAIN_SCOC`, and fixed chain length are framed with symbols (`m`) but missing the valid-regime guard for this project’s branch constraints (e.g., whether `m >= 2`, whether non-delivery turns are excluded, and what counts as an “exact successful anchor”). This is a load-bearing validity-domain gap, not a minor notation issue.

### Mathematical Depth & Validity Domains

The arithmetic itself is minimal but concrete. However, the proof obligations are incomplete:

- The ratio that motivates the transfer boundary is stated (`T_chain/T_single <= 0.563174694970`) without an explicit derivation and without matching variable definition at the file level.
- The lock introduces exact constants (`88.188`, `1.584519189306`) as transfer gates with no unit semantics. They are likely from phase-0, but this file must restate whether these are raw-score thresholds, policy ratio thresholds, or confidence-adjusted quantities.

### Logical Soundness

The hypothesis is structurally coherent as a narrow mechanism. But the strongest local move is weakened by scope incompleteness: the “required falsification pair” omits one frozen comparison control (`CHAIN_GENERIC`) while that mechanism is explicitly in the anti-stacking control set. This weakens anti-stacking validity at the same rigor level as the core claim and should be closed in the frozen map before a pass.

### Assumption Completeness

The hypothesis has partial assumptions (fixed template class, fixed syntax, fixed template class/syntax invariance), but does not enumerate failure-to-meet assumptions and their consequences. Critical missing assumptions include:

- what “same chain length” excludes (retry truncation, malformed turns, or parser-canonicalized wrappers),
- whether all accepted anchors remain semantically equivalent under remote evaluator normalization,
- and whether exact-event coverage is over template class and payload class combined or over payload class only.

Any one of these changing invalidates the stated mechanism attribution.

### Taxonomy Verification

No explicit idea-taxonomy entry appears in this artifact (opportunity pattern / method paradigm / dominant operation). The contract is therefore not self-typed, which is acceptable only if this was frozen earlier and inherited; this file alone cannot be audited for that import. At minimum, it should state its self-classification inline to support anti-stacking and review closure.

### Anti-Stacking Check (Engineering)

The file sets a reasonable mechanism gate, and the frozen control set is good in direction. However, the anti-stacking proof is incomplete on two points:

1. `CHAIN_GENERIC` is part of the frozen admissible control set but is not in the required falsification map.
2. For `CHAIN_COMPACT_EXPLICIT`, the test is defined but the file does not state the ablation parity condition for identical stop semantics and payload shape in the same section, so equal-or-better SCOC performance could still be an implementation artifact.

### Occam's Razor Check

A simpler explanation exists and is not yet explicitly ruled out: parser normalization + payload canonicalization may explain gains from fewer raw fields without requiring destination-operand state continuity. The lock currently attributes all mechanism credit to anchor-conditioned continuation without the strongest available minimal control to separate these effects.

### Alternative Explanations

Two untested alternatives are plausible and would directly mimic some SCOC benefits: (a) static template canonicalization reducing replay token inflation, and (b) anchor-only control flow changing branch choice rather than true destination-operand continuation. Neither is explicitly distinguished with a dedicated falsification condition in this lock.

## Overall: NEEDS_REVISION

Required fixes (ordered by severity):

1. Add explicit CHAIN_FULL and CHAIN_COMPACT_EXPLICIT overlap/baseline definitions in the file so the core comparison is fully reconstructible without external memory.
2. Add the missing `CHAIN_GENERIC` falsification condition with fixed-syntax, fixed-chain-length parity (and fixed stop semantics) or state why it is intentionally non-admissible.
3. Add explicit validity regimes and a per-assumption failure mode list (especially `m`, chain-length definition, stop semantics, and exact-overlap operator), plus direct units for the transfer gate constants.

## 2. Actionable Coaching

- In the machine-readable block, include the exact CHAIN_FULL and CHAIN_COMPACT formulas and a canonical overlap definition for `overlap_exact` (e.g., matching fields, normalization rules, and stop semantics).
- Add a one-line taxonomy classification directly in the lock (`Resource Bottleneck`/`Artifact` + dominant operation), then keep anti-stacking checks aligned to that class.
- Clarify transfer constants (`88.188`, `1.584519189306`) as raw-score ratio or policy-transfer ratio and bind each to the source line where they are inherited.
- Add a direct falsification control for `CHAIN_GENERIC` in Section 4 and a single-paragraph mechanism-separation argument for canonicalization-only artifacts.
