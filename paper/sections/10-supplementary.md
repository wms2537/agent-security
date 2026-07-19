# Supplementary Material

## S1. Complete historical prediction and outcome ledger

The block below is a byte-for-byte copy of `results.tsv`: one header and all 42
data rows, including failed, exploratory, discarded, superseded, and
mechanics-only records. Its SHA-256 is
`9379de501f0f9bd9330aa146d5df9700816c4ccdc664f899e74a331a6e2f81b1`.
`NA` and `null` retain their recorded meanings and have not been converted to
zero.

This ledger is an immutable history, not revision-2 scientific terminology.
In particular, every occurrence of `confirm` (including descriptions such as
`confirmation interval`), `materiality`, `generalization`, or `robustness` is a
historical signal, metric name, run description, or decision label written
under the earlier protocol. Those words do not upgrade PS-PIR into an untouched
test, practical-utility result, population generalization, or robustness claim.

```tsv
run_id	metric	predicted_value	predicted_direction	confidence	metric_value	signal	memory_gb	runtime_s	status	description
goexplore-det-baseline	normalized	NA	unclear	low	NA	null	0.5	20	exploratory	provided Go-Explore baseline vs deterministic agent; timed out at 20s budget (heavy search)
local-compliant-400-rr	normalized	66	beat-baseline	medium	56.76	disconfirm	0.5	37	discard	equal round-robin ensemble dilutes sev-64 multi-post with sev-4 CD
local-compliant-400	normalized	120	beat-baseline	medium	100.68	partial	0.5	37	keep	weighted alloc, multi-post EXFIL dominant + small diversity hedge (mock upper bound)
local-refuse-exfil-400	normalized	8	match-baseline	high	11.04	confirm	0.5	37	keep	http.post blocked -> selector falls back to CONFUSED_DEPUTY and still fires (robustness path)
local-compliant-400-hardened	normalized	200	beat-baseline	medium	198.60	confirm	0.5	37	keep	multi-post-8 + 22pct second-family reserve; ~2x per-candidate severity, private insurance held
local-refuse-exfil-hardened	normalized	9	match-baseline	high	11.28	confirm	0.5	37	keep	private-guardrail sim (http.post blocked) still scores via CONFUSED_DEPUTY reserve
real-lb-v1-multipost	normalized_lb	~85	beat-baseline	low	36.705	disconfirm	NA	NA	superseded	v1 real LB: mock 198 was ONE compliant cell not the 4-cell mean; multi-post latency-bound + 28pct dead reserves -> bottom of board
real-lb-v2-singlepost	normalized_lb	84-90	beat-prior	medium	69.570	partial	NA	NA	keep	v2 real LB: single-post exfil + per-model raw/s selection + verified fill + void-safe 0.90; +89pct over v1, mid-pack (top ~103.7)
local-replay-cap-parity	findings_ratio	1.210	beat-baseline	high	1.205	confirm	0.5	11	keep	controlled real-SDK run: old 0.90/1.10 accounting returned 39 findings, public 0.99/direct-cost accounting returned 47
local-multi-fixed-overhead-3	normalized	1.950	beat-baseline	high	1.950	confirm	0.5	3	keep	adaptive router selected M8 multi-message under fixed reset overhead; official raw exactly 390=3*(16*8+2)
local-multi-context-fallback-3	normalized	0.270	match-baseline	high	0.270	confirm	0.5	1	keep	M4 probe passed but M8 context-limited candidate failed 75pct gate; router fell back to three single-post findings, exact raw=54
local-multi-default-50	normalized	96.50	beat-baseline	high	96.50	confirm	0.5	20	mechanics-only	production M24 default on compliant/harmony mocks: exact raw=19300=50*(16*24+2); not a real-model score prediction
orf-cal-v1-equal-h200-clear	masters_clearing_5pct_fraction	0.750000000000	beat-baseline	low	NA	null	NA	NA	crash	equal-weight H=200000 non-target calibration; exploratory only
orf-cal-v1-balanced-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	NA	null	NA	NA	crash	balanced cliff-presence H=200000 sensitivity; exploratory only
orf-cal-v1-no-cliff-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	NA	null	NA	NA	crash	no-cliff-only H=200000 sensitivity; exploratory only
orf-cal-v1-cliff-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	NA	null	NA	NA	crash	cliff-only H=200000 sensitivity; exploratory only
orf-cal-v1-equal-unsat-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	NA	null	NA	NA	crash	equal-weight H=10^18 saturation sensitivity; exploratory only
orf-cal-v1-floor-margin	minimum_cliff_floor_distance	0.000000000000000000000000000000000000000000000000000000000001	beat-baseline	low	NA	null	NA	NA	crash	minimum distance from a cliff expression to an integer; no resampling
orf-cal-v2-equal-h200-clear	masters_clearing_5pct_fraction	0.750000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; equal-weight H=200000; exploratory only
orf-cal-v2-balanced-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; balanced cliff-presence H=200000; exploratory only
orf-cal-v2-no-cliff-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; no-cliff-only H=200000; exploratory only
orf-cal-v2-cliff-h200-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; cliff-only H=200000; exploratory only
orf-cal-v2-equal-unsat-clear	masters_clearing_5pct_fraction	0.500000000000	beat-baseline	low	1.000000000000	confirm	NA	29.43	exploratory	retry after v1 numeric crash; equal-weight H=10^18; exploratory only
orf-cal-v2-floor-margin	minimum_cliff_floor_distance	0.000000000000000000000000000000000000000000000000000000000001	beat-baseline	low	2.4702028345850861854631560389931149158158007314717302917408272803144660234725560E-8	confirm	NA	29.43	exploratory	retry after v1 numeric crash; no-resampling floor certificate
poc	adaptive_gain_percent	35.0	beat-baseline	low	49.277489504413	confirm	0.053520203	0.679508220	keep	public non-target 40-stratum ORF PoC; support threshold 5%, prediction interval 20-50%
poc	homogeneous_difference_raw	0	match-baseline	high	0	confirm	0.053520203	0.679508220	keep	exact homogeneous negative invariant
poc	sdk_cases_verified	2	match-baseline	high	2	confirm	0.053520203	0.679508220	keep	actual SDK q=16e+2 and 16-hex score-cell fixture checks
orf-p4-baseline	mean_global_score_raw	8500000	unclear	medium	8602550.666666666667	confirm	0.023773193	1.491515685	keep	exact N=3 public non-target PROBE_GLOBAL baseline and tuned parity
orf-p4-baseline	global_length_16_fraction	1.0	match-baseline	high	1.000000000000	confirm	0.023773193	1.491515685	keep	calibration-derived prediction that every master selects m=16
orf-p4-baseline	mechanical_reference_match_fraction	1.0	match-baseline	high	1.000000000000	confirm	0.023773193	1.491515685	keep	exact default tables must match immutable calibration reference
orf-p4-core	mean_adaptive_gain_percent	40.0	beat-baseline	medium	40.249038022308	confirm	0.515918732	0.132034047	keep	public N=3 per-profile-vs-global core; confirmation interval 30-50 percent
orf-p4-core	all_masters_clear_fraction	1.0	beat-baseline	high	1.000000000000	confirm	0.515918732	0.132034047	keep	all three fixed public masters must have adaptive gain at least 5 percent
orf-p4-core	homogeneous_zero_fraction	1.0	match-baseline	high	1.000000000000	confirm	0.515918732	0.132034047	keep	exact zero-regret distinguishing negative across three homogeneous masters
orf-p4-core	homogeneous_length_one_fraction	1.0	match-baseline	high	1.000000000000	confirm	0.515918732	0.132034047	keep	all homogeneous rows and global policies must select fill length one
orf-p4-ablations	no_cliff_mean_gain_percent	7.0	beat-baseline	low	7.622073949240	confirm	0.548843384	1.506462713	keep	one-at-a-time replacement of every event vector by e(m)=m
orf-p4-ablations	no_curvature_mean_gain_percent	35.0	beat-baseline	low	37.860007927303	confirm	0.548843384	1.506462713	keep	one-at-a-time exact d=0 cost transform
orf-p4-ablations	no_reset_mean_gain_percent	22.0	beat-baseline	low	18.973588191963	confirm	0.548843384	1.506462713	keep	one-at-a-time exact a=0 cost transform
orf-p4-ablations	no_novelty_mean_gain_percent	40.0	beat-baseline	medium	40.094682770562	confirm	0.548843384	1.506462713	keep	one-at-a-time replacement of positive raw 16e+2 by 16e
orf-p4-ablations	unsaturated_mean_gain_percent	44.0	beat-baseline	medium	44.355152104598	confirm	0.548843384	1.506462713	keep	one-at-a-time replacement of H=200000 by H=10^18
orf-p4-generalization	mean_generalization_gain_percent	35.0	beat-baseline	medium	36.393868336949	confirm	0.558269501	1.294787546	keep	disjoint public unsaturated balanced-cliff regime; confirm interval 30-45 percent
orf-p4-generalization	all_generalization_masters_clear_fraction	1.0	beat-baseline	high	1.000000000000	confirm	0.558269501	1.294787546	keep	all three weighted generalization masters must gain at least 5 percent
orf-p4-scaling	all_scale_master_cells_clear_fraction	1.0	beat-baseline	high	1.000000000000	confirm	0.583507538	0.031398170	keep	all 3 masters x nested 40/160/320-profile cells must gain at least 5 percent
```

The unchanged status census is 26 `keep`, 7 `exploratory`, 6 `crash`, 1
`discard`, 1 `superseded`, and 1 `mechanics-only`. PS-PIR uses the Phase-4
deterministic score-table artifacts for its worked example; the remaining rows
are preserved to expose calibration, failure, and historical decision paths.

## S2. Chronology and absence of an untouched tier

All times below are local commit times (`+08:00`) on 2026-07-19. A “freeze” in
this table means that a public configuration or prediction was committed before
its corresponding deterministic calculation. It does not mean the generator
family was untouched by earlier exploration.

| Time | Commit | Recorded event | Evidence-tier implication |
|---|---|---|---|
| 15:07:39 | `bba39d7` | Public support calibration v1 preregistered. | Exploratory public calibration. |
| 15:10:17 | `bcf9a5c` | Calibration v1 recorded as numerically invalid. | Six crash rows retained; no effect estimate. |
| 15:11:20 | `47f50a2` | Narrow Decimal/Fraction repair preregistered. | Repair fixed before the retry. |
| 15:13:25 | `a120336` | Calibration v2 recorded. | Public exploratory outcomes informed later magnitude expectations. |
| 16:27:03 | `74d1836` | Prospective ORF-B v9 specification and contract committed. | Protocol design only; no freeze/open or target evaluation. |
| 16:55:17 | `25921b4` | Theory-review round 11 closed `RIGOROUS`. | Theory scrutiny, not empirical held-out evidence. |
| 19:06:56 | `9b0d94a` | Forty-profile public PoC prediction and command frozen. | Post-calibration public check. |
| 19:11:54 | `b126636` | Public PoC recorded at 49.277489504413%. | Used to decide whether to proceed; not pooled with Phase 4. |
| 19:16:39 | `354cc02` | Phase-4 public config, labels, sequence, and boundaries frozen. | Start of post-calibration frozen public verification. |
| 19:17:43 | `a416a72` | Exhaustive shared-policy baseline prediction frozen. | Public prediction before baseline calculation. |
| 19:23:22 | `1b0a7c5` | Baseline score tables and result committed. | Exact shared comparator on the selected tables. |
| 19:31:16 | `9aa3d89` | Core implementation committed unexecuted. | Result remained unavailable before code review. |
| 19:39:47 | `2a4f280` | First core-code review logged a stale/partial-bundle blocker. | Scientific core remained unexecuted. |
| 20:14:48 | `bb896ab` | Transactional evidence-bundle repair committed. | Source-level provenance repair. |
| 20:20:13 | `bfbbdca` | Re-review logged a symlink/lexical-identity blocker. | Scientific core still remained unexecuted. |
| 20:27:28 | `06239e3` | Lexical identity and no-follow repair committed. | Second source-level provenance repair. |
| 20:31:24 | `99ee635` | Third review closed the code gate `SOUND`. | One-use core calculation became eligible. |
| 20:33:19 | `20b73f4` | Three core predictions and equality checks frozen. | Public prediction before the core calculation. |
| 20:35:54 | `02b90ff` | Core and homogeneous results committed. | Three named crossed tables plus a boundary/code-path sanity check. |
| 20:38:46 | `e0b9520` | Five OAT predictions frozen. | Public sensitivity plan before calculation. |
| 21:00:34 | `47fb042` | OAT table committed after focused review. | Removal-associated public sensitivity values. |
| 21:01:41 | `6fc4df8` | Second-construction predictions frozen. | Another designer-specified public calculation. |
| 21:15:26 | `d8ccce6` | Second-construction results committed. | Not an untouched replication or transfer test. |
| 21:16:18 | `a796796` | Nested-prefix prediction frozen. | Reuses the primary tables. |
| 21:26:34 | `eb180fa` | Nested-prefix results committed. | Numerical sensitivity, not independent replication. |
| 21:33:46 | `0fa39de` | Phase-4 batch audit closed. | Public deterministic batch complete. |
| 21:51:51 | `db7e87d` | Phase-5 analysis, figures, and internal-report decision committed. | Locked test explicitly not run. |
| 22:02:40 | `a490f5d` | Version-1 report plan committed. | Writing began after analysis. |
| 22:20:22 | `08f300f` | Version-1 report assembled and deterministically checked. | Internal draft only. |
| 22:20:43 | `b8c0ea0` | Paper-review round 1 dispatched. | Paper-review budget charged 1/2. |
| 22:29:20 | `330703a` | Round-1 `NEEDS_REVISION` verdict logged verbatim. | Twelve issues required branch-of-origin reconstruction. |
| 23:02:23 | `f0af017` | PS-PIR revision-2 foundation and diagnostics committed. | Executed study downgraded to a deterministic worked example. |
| — | — | **Untouched evaluation tier** | **None was created, frozen, opened, or run.** |

The chronology therefore supports custody of each public calculation but gives
the magnitude no untouched-test force. PS-PIR names what was executed. ORF-B /
Beacon-Held-Out Conditional Regret names only the prospective protocol; all its
candidate contracts remained unfrozen and unopened.

## S3. Repository-relative artifact and command map

All paths and commands are relative to the repository root. The clean local
bootstrap, recorded environments, dependency pins, one-use attempt rule, and
full scientific-family commands are documented in
`paper/reproducibility/README.md`.

| Purpose | Canonical inputs or code | Recorded outputs | Verification or regeneration command |
|---|---|---|---|
| Environment | `experiments/configs/environment.md`; `paper/reproducibility/requirements-core.txt`; `requirements-figures.txt` | Recorded CPython/package versions | See `paper/reproducibility/README.md` |
| Shared comparator | `experiments/configs/orf-phase4-v1.json`; `experiments/orf-p4-baseline/run_baseline.py` | `score-tables.tsv`; `aggregate-by-length.tsv`; `baseline-summary.json` | Scientific-family command in the reproducibility guide |
| PS-PIR core and equality check | `experiments/orf-p4-core/run_core.py`; baseline score table | `experiments/runs/orf-p4-core-v1/core-by-master.tsv`; `homogeneous-by-master.tsv`; `COMPLETE.json` | `comp/.venv/bin/python -m unittest experiments/orf-p4-core/test_toy_core.py` |
| OAT sensitivities | `experiments/orf-p4-ablations/run_ablations.py` | `experiments/runs/orf-p4-ablations-v1/ablation-by-master.tsv`; transformed table; `COMPLETE.json` | `comp/.venv/bin/python -m unittest experiments/orf-p4-ablations/test_toy_ablations.py` |
| Second public construction | `experiments/orf-p4-generalization/run_generalization.py` | `experiments/runs/orf-p4-generalization-v1/generalization-by-master.tsv`; score table; `COMPLETE.json` | `comp/.venv/bin/python -m unittest experiments/orf-p4-generalization/test_toy_generalization.py` |
| Nested prefixes | `experiments/orf-p4-scaling/run_scaling.py`; baseline score table | `experiments/runs/orf-p4-scaling-v1/scaling-by-cell.tsv`; `COMPLETE.json` | `comp/.venv/bin/python -m unittest experiments/orf-p4-scaling/test_toy_scaling.py` |
| Reviewer-requested diagnostics | `experiments/orf-phase5-analysis/generate_reviewer_tables.py` | `paper/tables/action-distributions.tsv`; `oat-raw-summary.tsv`; `stratum-regret-decomposition.tsv` | `comp/.venv/bin/python experiments/orf-phase5-analysis/generate_reviewer_tables.py` |
| Figures and source data | `experiments/orf-phase5-analysis/generate_figures.py`; committed experiment tables | `paper/figures/comparison_chart.*`; `ablation_heatmap.*`; `scaling_curve.*` | `python experiments/orf-phase5-analysis/generate_figures.py` |
| Report integrity | Ordered files in `paper/sections/`; committed code/evidence | `paper/orf-internal-technical-report.md`; `paper/reproducibility/SOURCE_REVISION.txt`; `MANIFEST.tsv` | `python paper/assemble_report.py`<br>`python paper/reproducibility/build_manifest.py`<br>`python paper/check_revision.py` |
| Complete audit trail | `results.tsv`; `research-log/020-poc-orf-core.md` through `048-orf-paper-revision-foundation.md` | Ledger, predictions, reviews, analyses, and decisions | `git log --date=iso-strict-local -- research-log results.tsv paper experiments` |

Each transactional `COMPLETE.json` binds the canonical command, attempt
identity, source/input hashes, exact output set, and artifact hashes. The
committed attempt directories are no-overwrite evidence; a scientific-family
rerun must use a new explicit direct-child attempt name as described in the
guide.

## S4. Reviewer-requested diagnostics

The complete diagnostics are machine-readable tables rather than inferential
samples:

- `paper/tables/action-distributions.tsv` has three master rows and 960 profile
  decisions in total. The shared action is length 16 for every master. Row-wise
  choices use lengths 4, 8, 16, 24, and 32; lengths 1 and 2 are unused. Counts
  sum to 320 for each master.
- `paper/tables/stratum-regret-decomposition.tsv` has all 40 crossed strata,
  each aggregating 24 profiles across the three masters: 960 profiles total and
  raw regret 10,380,000. Strata 13, 28, 33, and 38 have zero regret. The five
  largest contributions are strata 6, 2, 1, 7, and 0 and sum to approximately
  47.843237% after displayed-share rounding. This is contribution accounting
  for the engineered tables, not a causal or prevalence decomposition.
- `paper/tables/oat-raw-summary.tsv` reports the core and five transforms as raw
  mean row-wise-oracle score `A`, shared score `G`, difference `A-G`, and the
  displayed percentage ratio. The core row is
  `12,062,550.667 / 8,602,550.667 / 3,460,000.000 / 40.249038022308%`.
  Because transforms can change both `A` and `G` and interact, their values are
  removal-associated sensitivity contrasts, not additive component shares.

The action table, stratum table, and raw OAT table are generated together by
the command listed in S3. Its deterministic audit records three action rows,
960 profiles, 40 strata, and total raw regret 10,380,000.

## S5. Local reproducibility and availability limits

The report is reproducible inside this repository from deterministic integer
and rational tables, committed code, local Git history, completion manifests,
dependency-version records, and the commands in the reproducibility guide. The
Phase-4 scorer calculations used Linux x86-64, glibc 2.40, CPython 3.14.3,
`jsonschema==4.26.0`, CPU only, and no network. Figure generation used CPython
3.11.11 with `matplotlib==3.10.9`.

This is internal reproducibility, not a durable public release. There is no
public clone URL, external archive, DOI, archived operating-system image,
container, bit-for-bit dependency lock, or durability guarantee. The commit IDs
in S2 identify local repository states but are not externally retrievable
without a separately shared repository snapshot. No publication, archive, or
external-release action was taken or authorized.

The data used by PS-PIR are deterministic synthetic tables stored locally. No
personal data, human-subject data, live target data, private evaluation data, or
beacon-derived target data enter the executed calculation.

## S6. Research-process, compute, AI-assistance, and governance disclosure

### Iterations and reviews

The state at revision-2 assembly records cycle 1, active hypothesis iteration
4, and 1 of 5 research-iteration budget units spent. Nine written hypothesis
revisions were preserved. Eleven of 20 authorized hypothesis-review rounds were
dispatched; round 11 returned `RIGOROUS` for the prospective v9 specification.
These are revision and scrutiny counts, not independent hypotheses,
replications, or experimental units.

Paper-review round 1 consumed 1 of the 2 authorized rounds and returned
`NEEDS_REVISION`. Its complete twelve-issue verdict is preserved in
`research-log/047-orf-paper-review-round1.md`. The reconstruction foundation is
`research-log/048-orf-paper-revision-foundation.md`; at the point this supplement
was written, the second paper-review round had not yet been dispatched.

### Full research path

The record is intentionally unsanitized. Equal round-robin allocation was
discarded after underperforming its prediction. A historical multipost/reserve
design was superseded after a 36.705 live aggregate missed its approximately 85
forecast. Latency, reserve, parsing, and aggregation were proposed as possible
explanations in project notes, but PS-PIR did not run a diagnostic protocol that
identifies them as causes. Six calibration-v1 rows crashed because of premature
numeric precision loss; the repair was specified before calibration v2. Two
code reviews then blocked core execution on evidence-bundle and lexical-path
provenance defects, both repaired and re-reviewed before the core calculation.

### Compute

Counting each Phase-4 scientific family once, recorded runtime was exactly
4.456198161 seconds and maximum reported peak memory was 0.583507538 GB. The
five OAT rows share one execution, the scale cells share one execution, and
repeated per-metric runtime fields must not be summed. These are wall-clock and
peak-process measurements on the recorded local environment, not an energy or
hardware-normalized compute estimate. A complete project-wide runtime cannot be
reconstructed exactly from the ledger because historical live rows contain
`NA` and some multi-metric/batched rows repeat one execution's runtime.

### AI assistance and human control

AI agents assisted with literature retrieval and field verification, hypothesis
stress testing, code review, deterministic analysis, figure generation,
manuscript planning and drafting, and manuscript review. The human user selected
the research scope, authorized review budgets and progression through Phase 6,
and set the no-Kaggle and no-held-out boundaries. Agent prose and reviewer
judgments were not used as quantitative evidence without checks against primary
literature or committed machine-readable artifacts.

### Executed versus prospective work

PS-PIR is the executed post-calibration public deterministic calculation. ORF-B
/ Beacon-Held-Out Conditional Regret is prospective and unexecuted. No beacon
was fetched, no held-out freeze or opening occurred, no target/profile set was
derived, and no locked/private score was produced. No new Kaggle push, API call,
notebook run, submission, or leaderboard read was taken after the user's
explicit no-Kaggle boundary or as part of PS-PIR. Earlier historical Kaggle
observations remain visible in S1; they are not PS-PIR evidence. Any future
held-out, live, private, Kaggle, archive, or submission action would require
separate authorization.

The experimental unit in the worked example is one named deterministic master.
Profiles, actions, strata, OAT transforms, and nested-prefix cells are dependent
views, not samples from a declared population. Accordingly, the report supplies
exact values and finite ranges but no sample standard deviation, standardized
effect, confidence interval, population test, or p-value. The preselected 5%
line has no external utility calibration.
