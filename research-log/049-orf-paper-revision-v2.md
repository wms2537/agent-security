# PS-PIR Phase-6 report revision 2 — deterministic verification

**Date:** 2026-07-19  
**Phase:** 6  
**Task:** T031  
**Document class:** internal technical report / scorer worked example  
**Paper-review budget before dispatch:** 1/2

## Revision outcome

The report was reconstructed from the branch-of-origin blueprint rather than
patched sentence by sentence. The executed calculation is now named
**Public-Synthetic Perfect-Information Regret (PS-PIR)** and framed as a
deterministic application of established value-of-perfect-information and
policy-class containment. `ORF-B / Beacon-Held-Out Conditional Regret` is
identified only as a prospective protocol that was not executed.

The ordered section sources assemble to:

```text
paper/orf-internal-technical-report.md
lines=1184
whitespace_words=9890
bytes=76398
sha256=48ea6a70b31e81717163ccfd551c97efe4ba4f200455c89d4a5bc79a507fb75f
```

The committed source revision used for assembly is
`0b5e9f7eed1338de419d8137b1866624f44c4c26`. The local non-circular integrity
package records 75 code, config, evidence, figure, section, and report files in
`paper/reproducibility/MANIFEST.tsv`; the assembled report is included at the
same hash above. There is no external archive, DOI, container, public clone, or
durability guarantee.

## Round-1 issue resolution audit

| Issue | Revision-2 status | Evidence |
|---:|---|---|
| 1. Engineered phenomenon | RESOLVED by downgrade | Title, Abstract, Methodology, Discussion, and Conclusion restrict magnitude to named designer-specified tables and call the construction a stress test/worked example. |
| 2. Elementary conceptual form | RESOLVED by downgrade | Related Work leads with Howard and explicitly denies a new regret concept, theorem, algorithm, or empirical phenomenon. |
| 3. Post-calibration status | RESOLVED | Introduction, Setup, Discussion, and Supplement use `post-calibration frozen public verification` and show no untouched tier. |
| 4. No learner/probe selector | RESOLVED by downgrade | Oracle access is explicit; probes never select an action; no attainable fraction is claimed. |
| 5. Missing foundational literature | RESOLVED | Five additional field-verified sources cover VOI, contextual bandits/policy evaluation, adaptive optimization, and heterogeneous policy learning. Ten references total; all cited. |
| 6. Missing action/stratum diagnostics | RESOLVED | Three action histograms and full 40-stratum accounting cover 960 rows and raw regret 10,380,000. Historical causal explanations are reclassified as hypotheses. |
| 7. OAT over-attribution | RESOLVED | Core plus five transforms report raw A, G, A-G, and ratios; prose says `removal-associated`, interacting, and nondecompositional. |
| 8. Finite-census/statistical inconsistency | RESOLVED | Sample SD and standardized score are absent; all three values/range are primary; 5% is an uncalibrated numerical cutoff. |
| 9. Held-out method name | RESOLVED | PS-PIR names executed work; ORF-B/Beacon-Held-Out is prospective and unexecuted. |
| 10. External reproducibility | IMPROVED, not claimed resolved | Repo-relative commands, dependency records, source revision, and 75-file manifest exist; absent external archive/container/durability remain disclosed. |
| 11. Unsupported motivation/provenance | RESOLVED at manuscript scope | Gateway/scorer/contracts/ops paths support local SDK facts; latency/reserve/parser/aggregation claims are hypotheses, not causes. |
| 12. q-domain contradiction | RESOLVED | Methodology defines q_z(m)>=0 and evaluates q=0 before saturation; H is per profile. |

No new learner, external data, target evaluation, or publication action was
introduced to simulate resolution of issues 1–4 or 10.

## Deep-imitation and anti-shallow audit

Comparison uses scientific prose paragraphs of at least 30 words in sections
01–08 against committed version 1 at `08f300f`, with whitespace normalization
and `SequenceMatcher >= 0.90` as the near-identical criterion.

```text
near_identical_paragraphs=0/75
near_identical_ratio=0.000000
maximum_allowed=0.35
```

The 51-row rationale matrix has 39 `REWRITE`, 8 `ADD`, 1 `ADD/MOVE`, 2
`MERGE`, and 1 `KEEP-AS-ARCHIVE` operation. `REWRITE` is dominant. Scientific
prose has 0/50 `KEEP` rows; the sole archive operation is the immutable ledger.

Obligatory-move and evidence results:

```text
missing_obligatory_moves=0
unsupported_new_substantive_claims=0
numerical_claims_without_source=0
```

The unsupported-claim audit checked every numeric-bearing main-text line against
the claim map and its primary anchor: SDK constants against local SDK files;
construction constants against the config/generator; results and sensitivities
against committed TSVs; historical values against `results.tsv`; and literature
claims against the two field-verified databases. New narrative claims are either
elementary finite algebra, direct design descriptions, or explicitly labeled
inferences/limitations.

## Deterministic manuscript checks

`python paper/check_revision.py` returned:

```text
revision_check=PASS
near_identical_paragraphs=0/75 ratio=0.000000 threshold=0.35
tables=PASS action_masters=3 profiles=960 strata=40 regret=10380000 oat_rows=6
references=PASS cited=10 field_verified=10 critical_mismatches=0
ledger=PASS byte_identical=true
```

Additional integrity results:

```text
assembly_manifest_determinism=PASS
figure_determinism=PASS
reference_field_integrity=PASS entries=10 critical_mismatches=0
citation_coverage=PASS references=1-10
ledger_integrity=PASS lines=43 data_rows=42 bytes=8119
reviewer_tables_deterministic=PASS
reviewer_table_audit=PASS action_rows=3 profiles=960 strata=40 regret=10380000
```

The scorer/transformation toy suite returned:

```text
Ran 18 tests in 0.003s
OK
```

The assembled image links resolve to the three committed SVG figures. Assembly
rewrites only section-relative figure paths; a second assembly and manifest run
produced identical hashes.

## Evidence-strength decision

The report remains an internal technical report. It does not meet a top-tier
contribution-paper standard because there is no learned selector, untouched
evaluation, live-transfer result, calibrated latency-tail model, external
archive, or novel concept. This is a deliberate evidence-aligned conclusion,
not an unfinished attempt to claim acceptance readiness.

## Authorization boundary

No Kaggle push, API call, notebook run, submission, or leaderboard read was
performed. No beacon was fetched; no held-out set was frozen, opened, derived,
or evaluated; and no live/private target action or external publication/archive
action occurred. Paper-review round 2 has not yet been charged. It may be
dispatched only after this assembled target is committed and the state budget is
updated at dispatch.
