independent_unit:   one pre-specified fixed public master, paired across policies
n_units:            3 paired masters per reported condition (nested scale cells reuse these same 3 masters)
comparison_family:  1 pre-specified confirmatory baseline comparison; 5 OAT, 1 changed-regime, and 3 scale summaries are secondary descriptive contrasts
correction:         none — single pre-specified primary; no secondary inferential claims or p-value multiplicity family

# ORF Phase-5 analysis — iteration 4

**Date:** 2026-07-19 · **Phase:** 5 · **Cycle:** 1 · **Iteration:** 4 · **Status:** analysis complete; path decision pending

## Scope and analysis set

The paper-bound analysis is the 15 `keep` rows whose `run_id` starts with
`orf-p4-`. Earlier ledger entries measure different targets or mechanics and are
historical context, not commensurate observations. Rows with `status=crash`,
`discard`, or `exploratory` are excluded from every ranking, statistic, and
figure. The `superseded` and `mechanics-only` rows are also excluded, as are the
Phase-3 PoC and support-calibration rows. The PoC may support the chronology but
is not pooled with the three Phase-4 masters.

`results.tsv` contains **42 data rows** (43 lines including the header). Counts by
every observed status are:

| Status | Rows | Included in Phase-4 paper statistics? |
|---|---:|---|
| `keep` | 26 | Only the 15 `orf-p4-*` rows |
| `exploratory` | 7 | No |
| `crash` | 6 | No |
| `discard` | 1 | No |
| `superseded` | 1 | No |
| `mechanics-only` | 1 | No |

The ledger is metric-level. Its 15 Phase-4 rows are not 15 independent units:
the primary unit is one fixed public master, so the relevant `n` is three.
Likewise, 960 profiles, 6,720 action scores, 320 decisions, 15 ablation cells,
and nine nested scale cells are deterministic technical structure, not
independent replications.

## Comprehensive Phase-4 results

The rows below are grouped by estimand. They are not globally ranked because raw
scores, gain percentages, exact fractions, and changed resource regimes are not
interchangeable. The exact exhaustive **PROBE_GLOBAL** policy is the matched
baseline; **Primary core** is the single pre-specified comparison. Runtime and
memory are reported once per executed family and repeated only to keep the table
self-contained.

| Family | Condition | Independent-unit structure | Reported outcome | Mean or exact value | Finite min–max | Delta vs primary core | Runtime (s) | Peak memory (GB) | Ledger |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| **Matched baseline** | **PROBE_GLOBAL, exhaustive 7-action argmax** | 3 fixed primary masters | Global raw score | **8,602,550.666667** | 8,403,762–8,824,632 | Reference | 1.491515685 | 0.023773193 | confirm / keep |
| **Pre-specified primary** | **ADAPTIVE vs PROBE_GLOBAL** | 3 paired primary masters | Adaptive gain (%) | **40.249038022308** | 38.111186959411–41.437632336565 | 0 pp | 0.132034047 | 0.515918732 | confirm / keep |
| OAT attribution | Remove cliff | Same 3 paired primary masters | Adaptive gain (%) | 7.622073949240 | 7.358152493680–7.908360846799 | −32.626964073068 pp | 1.506462713 | 0.548843384 | confirm / keep |
| OAT attribution | Remove curvature | Same 3 paired primary masters | Adaptive gain (%) | 37.860007927303 | 36.085277169782–39.584879778944 | −2.389030095004 pp | 1.506462713 | 0.548843384 | confirm / keep |
| OAT attribution | Remove reset | Same 3 paired primary masters | Adaptive gain (%) | 18.973588191963 | 18.384108984102–19.554006200377 | −21.275449830344 pp | 1.506462713 | 0.548843384 | confirm / keep |
| OAT attribution | Remove novelty bonus | Same 3 paired primary masters | Adaptive gain (%) | 40.094682770562 | 37.932378143820–41.288606188524 | −0.154355251746 pp | 1.506462713 | 0.548843384 | confirm / keep |
| OAT attribution | Remove saturation | Same 3 paired primary masters | Adaptive gain (%) | **44.355152104598** | 42.860593503566–46.447864344166 | +4.106114082290 pp | 1.506462713 | 0.548843384 | confirm / keep |
| Changed public regime | Unsaturated, balanced cliff | 3 disjoint fixed masters; not paired to primary masters | Adaptive gain (%) | 36.393868336949 | 35.175681399541–37.352060597349 | −3.855169685359 pp (descriptive only) | 1.294787546 | 0.558269501 | confirm / keep |
| Nested scale | N=40 profiles | Same 3 primary masters, nested | Adaptive gain (%) | **48.952971791444** | 45.344531072985–52.609341554583 | +8.703933769136 pp | 0.031398170 | 0.583507538 | confirm / keep |
| Nested scale | N=160 profiles | Same 3 primary masters, nested | Adaptive gain (%) | 42.794164975019 | 39.592292530738–45.400277409186 | +2.545126952711 pp | 0.031398170 | 0.583507538 | confirm / keep |
| Nested scale | N=320 profiles | Same 3 primary masters, nested; identical to primary full scale | Adaptive gain (%) | 40.249038022308 | 38.111186959411–41.437632336565 | 0 pp | 0.031398170 | 0.583507538 | confirm / keep |
| Distinguishing negative | Homogeneous profiles | 3 separately derived fixed masters | Adaptive − global raw | **0**; length-one fraction 3/3 | 0–0 | Not a gain comparison | 0.132034047 | 0.515918732 | confirm / keep |

The full Phase-4 batch consumed 4.456198161 reported CPU seconds in aggregate,
with maximum reported peak memory 0.583507538 GB. The scale rows share one
execution, as do the five OAT rows; their repeated resource numbers must not be
summed.

## Pre-specified primary: exact finite-census effect

For each master, the adaptive policy used the same seven actions and score table
as the exact global policy. The only change was action scope:

```text
A = sum_z max_m S_z(m)
G = max_m sum_z S_z(m)
gain = 100(A-G)/G.
```

The three paired master-level gains were 41.437632336565%,
38.111186959411%, and 41.198294770946%. Their mean was
**40.249038022308%**, sample s.d. **1.855296739857 percentage points**, and
finite observed range **38.111186959411–41.437632336565%**. The standardized
mean gain over zero was **21.694124264676 measured master s.d. units**
(`40.249038022308 / 1.855296739857`). This is a descriptive standardization over
the three fixed masters, not a population Cohen's d.

In raw-score units, mean ADAPTIVE score was 12,062,550.666667 (sample s.d.
157,245.982770), mean PROBE_GLOBAL score was 8,602,550.666667 (sample s.d.
211,399.622671), and mean paired improvement was exactly 3,460,000 raw points
(sample s.d. 87,821.654642). The registered estimand averages the three
master-specific percentage gains; the ratio of aggregate means, 40.220629%, is
therefore not substituted for the registered 40.249038% headline.

**Statistical verdict:** material exact finite-census contrast. `test: none
(finite prespecified census); p: not applicable`. No population p-value or
confidence interval is manufactured from three deterministic masters. The
reported min–max is a finite observed range, not an uncertainty interval. With
only n=3, population inference would in any case be weak and would require a
declared sampling population that this experiment does not provide.

## Prediction versus reality

### Complete-ledger audit (distribution only)

The 42-row signal distribution is shown for calibration auditing; excluded
statuses still do not enter a ranking, statistic, or figure.

| Analysis slice | Confirm | Partial | Disconfirm | Null | Total |
|---|---:|---:|---:|---:|---:|
| All ledger rows, all statuses | 31 | 2 | 2 | 7 | 42 |
| Phase-4 `orf-p4-*`, `keep` only | 15 | 0 | 0 | 0 | 15 |

The most informative historical disconfirmation was the superseded
`real-lb-v1-multipost` result (predicted about 85, actual 36.705): a large mock
score did not transfer to the live aggregate because fixed-length multipost
behavior was latency-bound and reserves were ineffective. The discarded
`local-compliant-400-rr` result (predicted 66, actual 56.76) showed that equal
round-robin allocation diluted the dominant high-severity mechanism. These two
rows are not ORF evidence; they diagnose exactly why a constructed simulator
cannot establish live transfer. The seven nulls consist of one timed-out
exploratory Go-Explore attempt and six numeric-crash calibration-v1 rows; none
supplies a scientific effect estimate.

### Phase-4 forecast calibration

| Forecast | Predicted | Actual | Prediction error / disposition |
|---|---:|---:|---|
| Baseline mean global raw | 8,500,000; interval 7,500,000–9,500,000 | 8,602,550.666667 | +102,550.666667; confirm |
| Core mean gain | 40%; interval 30–50% | 40.249038022308% | +0.249038022308 pp; confirm |
| Core all masters ≥5% | 1.0 | 1.0 | exact confirm |
| Homogeneous zero difference | 1.0 fraction | 1.0 fraction | exact confirm |
| Homogeneous length one | 1.0 fraction | 1.0 fraction | exact confirm |
| No-cliff mean gain | 7% | 7.622073949240% | +0.622073949240 pp; confirm |
| No-curvature mean gain | 35% | 37.860007927303% | +2.860007927303 pp; confirm |
| No-reset mean gain | 22% | 18.973588191963% | −3.026411808037 pp; confirm |
| No-novelty mean gain | 40% | 40.094682770562% | +0.094682770562 pp; confirm |
| Unsaturated mean gain | 44% | 44.355152104598% | +0.355152104598 pp; confirm |
| Changed-regime mean gain | 35%; interval 30–45% | 36.393868336949% | +1.393868336949 pp; confirm |
| Changed-regime all masters ≥5% | 1.0 | 1.0 | exact confirm |
| All 3×3 nested scale cells ≥5% | 1.0 | 1.0 | exact confirm |

Scale means were deliberately descriptive and therefore have no post-hoc
numeric “prediction.” All 15 registered Phase-4 ledger metrics resolved
`confirm/keep`. The absence of a Phase-4 miss is evidence of local calibration,
not evidence that the synthetic generator represents a live target population.

## Mechanism, attribution, and distinguishing prediction

The exact inequality `sum(max) >= max(sum)` explains direction: allowing each
profile to choose its best legal action contains the global one-action policy.
Magnitude requires different profiles to prefer different actions. The crossed
primary profiles created that heterogeneity, producing a 40.249% mean gain. The
separately derived homogeneous profiles removed it; every row and global policy
selected length one and adaptive-minus-global was exactly zero for all three
masters. The conjunction—material gain on crossed tables and exact equality on
homogeneous tables—is the distinguishing prediction, and it held.

The OAT evidence identifies cliff behavior as the dominant source: removing it
reduced mean gain by 32.627 pp. Removing reset overhead reduced gain by 21.275
pp. Curvature removal cost 2.389 pp, and deleting the two-point novelty term
cost only 0.154 pp. Removing saturation increased gain by 4.106 pp, indicating
that the cap hides some available action-scope value. These effects are paired
within the same three masters but remain descriptive; they interact and are not
additive. The no-reset result was 3.026 pp below forecast and the no-curvature
result 2.860 pp above forecast, refining the attribution magnitudes without
reversing the pre-specified ordering.

## Robustness, failure cases, and what was not solved

All three primary masters, all three disjoint changed-regime masters, and all
nine nested scale cells exceeded the 5% materiality threshold. Mean gain was
36.394% after simultaneously changing master labels, saturation, and cliff
weighting. It remained 48.953%, 42.794%, and 40.249% at nested N=40, 160, and
320. Because the scale cells reuse masters and rows, this is deterministic
robustness evidence, not a learning curve or nine-replicate sample.

Concrete failure surfaces remain. If profiles share one optimum, conditional
regret is exactly zero, as the homogeneous control demonstrates. With cliffs
removed, the gain shrank to 7.622%, close enough to the 5% threshold that a less
heterogeneous support could erase materiality. Constructed response profiles
validate policy mechanics but do not confirm that a target model exhibits the
same response heterogeneity. ADAPTIVE is an oracle policy; no run shows that an
online learner can infer its action from limited live probes. Replay-deadline
safety would require a calibrated tail/dependence model and explicit void-risk
target. No locked held-out set was opened, and there is no private, live,
latency-safety, causal-population, or Kaggle evidence.

The result therefore solves a **proxy**: it measures exact oracle information
value in a benchmark-shaped, public deterministic finite table. It does not yet
solve `PROBLEM.md`'s operational objective of a replay-safe algorithm that
transfers across live public and private guardrails. The earlier live-LB
disconfirmation makes this boundary empirical rather than ceremonial.

## Baseline and literature position

There is no published numerical baseline for this bespoke deterministic table.
The strongest matched-compute comparator is the exact exhaustive
PROBE_GLOBAL argmax over all seven legal lengths on the same profiles, resource
constraints, scores, and tie rule. It has no training, initialization, or
hyperparameter left unsearched, so the 40.249% contrast is not attributable to
weak baseline tuning.

Conceptually, the analysis concerns the finite value of conditioning a decision
on profile identity rather than enforcing one shared action. A fresh narrow
literature comparison is pending the orchestrator's targeted search and should
be added before paper synthesis. No SOTA number, novelty priority, or external
literature claim is inferred from the local Phase-1 competition recon.

## Figures and source data

**Fig. 1 | Profile-conditioned selection clears the materiality threshold in two public synthetic regimes.** Individual points show three fixed public masters per condition and black bars show condition means; the primary and changed-regime labels are disjoint and no cross-regime pairing is implied. The dashed line is the pre-specified 5% materiality threshold. The zero baseline is retained because gain is a ratio quantity and both zero regret and the 5% threshold are registered reference points. Statistics: n = 3 fixed public masters per condition, error bars show none, test = none (finite prespecified census), p = not applicable. Source data: `paper/figures/comparison_chart.source.csv`.

Single-panel question: Does per-profile selection clear the registered materiality threshold on both the primary and changed public constructions?

**Fig. 2 | Cliff and reset mechanisms dominate the one-at-a-time contribution pattern.** Colored markers show the paired delta from each primary master's core gain, and black diamonds show the three-master means. OAT effects can interact and are not additive. Statistics: n = 3 paired fixed public masters per condition, error bars show none, test = none (secondary descriptive paired contrasts), p = not applicable. Source data: `paper/figures/ablation_heatmap.source.csv`.

Single-panel question: Which named generator or score mechanism most changes the adaptive-versus-global gain when removed alone?

**Fig. 3 | Conditional-regret gain persists across nested profile-set sizes.** Colored trajectories reuse the same three primary masters at N=40, 160, and 320; the black trajectory is their descriptive mean. The nested cells are not independent replicates. Statistics: n = 3 reused fixed public masters per scale, error bars show none, test = none (secondary descriptive nested robustness), p = not applicable. Source data: `paper/figures/scaling_curve.source.csv`.

Single-panel question: Does the material direction persist as each fixed master's profile set expands through strictly nested subsets?

No training curve is produced because no optimization trajectory or per-step
training data exists.

## Evidence-bounded summary

The pre-specified core worked on its exact finite target: per-profile action
selection improved raw score by a mean 3,460,000 points and produced a mean
40.249% gain over the exact exhaustive global policy across three fixed public
masters. The master-level s.d. was 1.855 pp, giving a descriptive standardized
gain of 21.694 measured master s.d. units; all three gains exceeded 5%. This is
an exact finite-census result (`test: none`, `p: not applicable`), not a
population-significance claim.

The mechanism is coherent with the hypothesis. Crossed profiles preferred
different legal lengths, so the sum of profile-wise maxima materially exceeded
the best shared length. When that heterogeneity was removed, all three
homogeneous masters selected length one and had exactly zero regret. OAT
attribution made cliff behavior and reset overhead the largest contributors;
curvature was modest, novelty negligible, and saturation suppressed some
conditional value.

The result was robust inside the public synthetic design: three disjoint
changed-regime masters averaged 36.394%, and every one of nine nested scale
cells cleared 5%. The strongest caution comes from outside this analysis set:
an earlier live-LB disconfirmation showed that high constructed-mock scores can
fail under latency and aggregation. That row is excluded from ORF statistics
but directly limits interpretation.

No published numeric comparator exists for the bespoke table, while the local
PROBE_GLOBAL baseline is already an exact seven-action argmax with matched
compute. A fresh conceptual literature comparison remains pending orchestrator
search. The evidence supports public synthetic oracle information value only;
it does not establish live heterogeneity, learnability, deadline safety,
held-out confirmation, private transfer, or Kaggle improvement, and therefore
does not yet solve the operational problem in `PROBLEM.md`.
