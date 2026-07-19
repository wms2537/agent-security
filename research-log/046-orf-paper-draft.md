# ORF Phase-6 paper assembly and deterministic verification

**Date:** 2026-07-19  
**Phase/task:** 6 / T031  
**Document class:** paper-shaped internal technical report; no submission  
**Assembled draft:** `paper/orf-internal-technical-report.md`

## Assembly decision

The report follows the registered disconfirmation-led arc: the historical
mock-to-live failure motivates the exact proxy; the 40.249% crossed result and
homogeneous zero are the finite pivot; the missing learner, locked test, replay
tail model, and live/private evidence are the operational resolution. The main
text was assembled only after three ordered section-writer groups. The complete
42-row prediction ledger, including failures and exploratory rows, is embedded
verbatim in the supplement. All generated figures are linked with paths relative
to the assembled report.

The output is Markdown because Phase 0 selected a working note and the user
requested a paper/report, not a submission package. The draft has 629 lines,
9,323 whitespace-delimited words including the full ledger supplement, three
figures, and five references.

## Deterministic consistency checks

| Check | Evidence | Verdict |
|---|---|---|
| Figure inventory | `comparison_chart`, `ablation_heatmap`, and `scaling_curve` each have SVG, PNG, and source CSV; each SVG is referenced exactly once and no generated figure is unreferenced. | PASS |
| Figure contract | SVGs contain editable text. PNG metadata is 118.11 pixels/cm = 300 dpi. Each caption states unit/count, no error bars, `test:none`, `p:not applicable`, and source CSV. Source values match analyzer tables; visual inspection found no clipping or illegible labels. | PASS |
| Abstract/results numbers | Exact checks found every headline and Results-table number in `results.tsv`, run-bundle TSVs, or `research-log/042-analysis-iter-4-tables.md`; primary mean/s.d./range and all OAT, changed-regime, scale, runtime, and memory values match. | PASS |
| Complete ledger | Extraction of the assembled `tsv` fence is byte-identical to `results.tsv` (43 lines including header; 42 data rows). Status census remains keep 26, exploratory 7, crash 6, discard 1, superseded 1, mechanics-only 1. | PASS |
| Citations | The only cited author-year tokens are the five records in `research-log/lit/phase6-primary.json`; every reference is cited and no unverified citation appears. | PASS |
| Reference fields | 5/5 records are `verified`; 0 critical mismatches; 2 checked warnings. The Snell entry uses the final ICLR title rather than the slightly different preprint title. Plan-and-Budget uses current arXiv v3 title and 193.8% E3 value rather than older wording/numbers. | PASS |
| Claim-source gates | 0 metadata-only claims; no mechanism/method/quantitative claim rests on background support. Partial claim C22 is limited to “in this construction and OAT pattern.” C02 and C23-C24 retain contradictory/limiting evidence. | PASS |
| Placeholders | Case-insensitive scan for `TODO`, `PLACEHOLDER`, `[CITATION]`, `lorem`, and `conclusions here` returned no hits in the assembled draft. | PASS |
| Logged experiments | Every quantitative project outcome is present in the ledger or an analyzer table. Calibration crashes, discarded/superseded allocations, and mechanics-only mocks are explicitly excluded from ORF findings rather than silently pooled. | PASS |
| Availability paths | Config, environment, baseline/code/table/summary files, four transactional manifests, master tables, analysis program, figure sources, and analyzer report all exist at the paths stated in the supplement. | PASS |
| Disclosure | Primary versus secondary status, fixed `n=3` masters, no population test, forking paths, AI assistance, compute, repository-only availability, locked-test exception, and no-Kaggle boundary are explicit. | PASS |
| Connective tissue | Cross-source syntheses are labeled as bounded conclusions or our inference. No sentence converts adjacent literature into ORF mechanism evidence; the OAT explanation is construction-bounded; public robustness is not called held-out or population generalization. | PASS |

### Overclaim lint

The required scan for `prove`, `conclusively`, `unprecedented`, `best`,
`superior`, `first`, `novel`, and `paradigm` returned only justified uses:

- `prove`/`proves` occurs only for the finite containment inequality and is
  immediately separated from the empirical 5% magnitude;
- `best legal length` and `best-of-N` are, respectively, the argmax definition
  and a cited comparator name;
- `first` occurs only as a sequence/count term (`first 2,000`, first probe/log,
  first disconfirmation/calibration), never as a priority claim; and
- `novelty` occurs only as the name of the two-point score term or in sentences
  rejecting broad novelty. No manuscript claim uses `conclusively`,
  `unprecedented`, `superior`, or `paradigm`.

Verdict: PASS without wording changes.

## Citation-faithfulness random spot-check

Citation-bearing sentences were numbered in manuscript order:

1. Introduction five-study allocation-family synthesis.
2. Snell difficulty-conditioned strategy and up-to-fourfold compute statement.
3. Plan-and-Budget decomposition and 70%/39%/193.8% statement.
4. SCALE subproblem allocation and 57.50-to-71.25/33–53% statement.
5. Learning When to Plan 0.387-versus-0.379/85% statement.
6. BAVT 0.338-at-five-calls versus 0.334-at-20-calls statement.
7. BAVT critic-overhead and one-tool/uniform-cost limitation.

Logged random command and exact output:

```text
$ seq 1 7 | shuf -n 5
6
1
4
2
5
```

- **6 PASS:** arXiv HTML §4.2 reports OSS-20B average EM 0.338 at five
  tool calls and baseline 0.334 at 20 calls.
- **1 PASS:** the five primary sources respectively describe prompt-difficulty
  compute allocation, subquestion token scheduling, learned dynamic planning,
  subproblem difficulty allocation, and remaining-budget tool search. The
  sentence claims only this technique-family coverage.
- **4 PASS:** the official AAAI record/abstract states subproblem-difficulty
  allocation, AIME25 57.50% to 71.25%, and 33–53% cost reduction.
- **2 PASS:** the ICLR proceedings abstract states prompt-difficulty dependence
  and more than fourfold efficiency relative to best-of-N; the manuscript uses
  the narrower “up to fourfold less” phrasing.
- **5 PASS:** arXiv HTML §5.3 reports the fine-tuned 8B dynamic agent at 0.387,
  the 70B four-step zero-shot baseline at 0.379, and 85% fewer tokens.

No selected sentence failed; no writer-section sweep was triggered. Primary
records checked: ICLR proceedings for Snell; arXiv v3 for Plan-and-Budget and
Learning When to Plan; official AAAI proceedings for SCALE; arXiv HTML for BAVT.

## Review and gate status before dispatch

All deterministic checks required before the Medium-intensity paper reviewer
pass. The draft will be committed before sterile review. Paper-review budget is
still 0/2 in this pre-dispatch record. The empirical locked-test gate item is
**NOT RUN**, not passed: it conflicts with the user's explicit prohibition on
held-out/beacon/freeze/target/evaluation actions. No Kaggle action occurred.

Phase 6 is not yet closed: the sterile paper-review verdict, any routed fixes,
the user draft-review checkpoint, and the post-review retrospective remain.

### Paper-review round 1 dispatch

The committed review target is `paper/orf-internal-technical-report.md` at
commit `08f300f`, with 629 lines. Medium-intensity sterile review round 1 was
charged before dispatch; paper-review budget is now 1/2. The reviewer receives
only the SciAgent paper-reviewer template fields (title and path), with no
project history, assurances, deterministic-check detail, or known pitfalls.
