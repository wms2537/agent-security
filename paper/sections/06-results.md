# Material finite regret with a homogeneous zero boundary

All three primary masters cleared the registered 5% threshold, while all three
homogeneous masters returned exact equality. These are fixed-finite results over
three pre-specified public masters per condition; profiles, score rows, and
master-by-scale cells are not additional independent units.

## Exhaustive baseline and pre-specified primary

The exhaustive seven-action `PROBE_GLOBAL` comparator attained a mean raw score
of **8,602,550.667** across the three primary masters. Because it evaluates every
legal fill length on the same score tables used by `ADAPTIVE`, it has no
unsearched fill-length choice on those tables. Replacing its single global
argmax with profile-wise argmaxes produced the following registered primary
gains.

| Fixed public master | Adaptive gain over `PROBE_GLOBAL` |
|---|---:|
| P0 | 41.437632336565% |
| P1 | 38.111186959411% |
| P2 | 41.198294770946% |
| **Mean** | **40.249038022308%** |

Across the three paired masters, the measured-master sample s.d. was
**1.855296739857 percentage points**, and the finite observed range was
**38.111186959411--41.437632336565%**. The standardized mean over the measured
master s.d. was **21.694124264676**. This last quantity is descriptive only: it
is neither Cohen's *d* nor an estimate of a population effect. For the primary
fixed census, `test: none; p: not applicable`; the min--max span is not a
confidence interval.

Figure 1 shows the primary masters together with the disjoint changed-public
construction reported below. Each point is one fixed master, the black bars are
descriptive regime means, and no cross-regime pairing is implied.

![Figure 1: Primary and changed-public master gains.](../figures/comparison_chart.svg)

*Figure 1. Profile-conditioned selection clears the materiality threshold in two
public synthetic regimes. Points show three fixed public masters per condition;
black bars show condition means; the dashed line marks 5%. The master labels are
disjoint and are not paired across regimes. Error bars: none. Test: none (finite
pre-specified census); p: not applicable. Source:
`paper/figures/comparison_chart.source.csv`.*

## Exact homogeneous control

The separately derived homogeneous construction returned an
`ADAPTIVE - PROBE_GLOBAL` raw difference of exactly zero for each of its three
masters. Every homogeneous profile and each corresponding global policy selected
fill length one, giving a zero-difference fraction of 3/3 and a length-one
fraction of 3/3.

| Homogeneous outcome | Masters satisfying outcome |
|---|---:|
| Exact adaptive-minus-global raw difference = 0 | 3/3 |
| Profile-wise and global selected length = 1 | 3/3 |

This is an exact finite equality result, not a non-significant population
comparison. No hypothesis test or p-value is attached to it.

## Secondary one-at-a-time contrasts

The five one-at-a-time (OAT) analyses reused the same three primary masters and
compared each transformed condition with that master's core gain. Their paired
mean differences were:

| OAT condition | Mean gain | Paired delta from core |
|---|---:|---:|
| Remove cliff | 7.622073949240% | -32.626964073068 pp |
| Remove curvature | 37.860007927303% | -2.389030095004 pp |
| Remove reset | 18.973588191963% | -21.275449830344 pp |
| Remove novelty bonus | 40.094682770562% | -0.154355251746 pp |
| Remove saturation | 44.355152104598% | +4.106114082290 pp |

Figure 2 shows the three paired master-level deltas and their descriptive means.
The largest observed decreases were under cliff removal and reset removal;
novelty removal changed the mean least, while removing saturation increased it.
These are secondary, paired, descriptive OAT contrasts (`n=3` fixed masters;
`test: none; p: not applicable`). The transforms may interact, so their deltas
are not additive and are not estimates of population-causal effects.

![Figure 2: One-at-a-time deltas from the primary core gain.](../figures/ablation_heatmap.svg)

*Figure 2. Cliff and reset mechanisms have the largest one-at-a-time contribution
pattern in this construction. Colored points are paired deltas for the same three
fixed public masters; black diamonds are their means. Error bars: none. Test:
none (secondary descriptive paired contrasts); p: not applicable. OAT deltas are
nonadditive. Source: `paper/figures/ablation_heatmap.source.csv`.*

## Changed public construction

The disjoint changed public construction returned gains of 36.653863013959%,
37.352060597349%, and 35.175681399541% on its three fixed masters. Its mean was
**36.393868336949%**, with all three masters above the registered 5% threshold.
These labels and construction differ from the primary regime, so no cross-regime
pairing is implied. This is a second public deterministic result, not a held-out
or population-generalization result.

Figure 1 places these values beside the primary construction and the registered
threshold without treating the two regimes as paired.

## Nested profile-set sizes

The same three primary masters were evaluated on strictly nested prefixes of 40,
160, and 320 profiles. Mean gain remained above 5% at each size:

| Profiles per master | P0 | P1 | P2 | Mean gain |
|---:|---:|---:|---:|---:|
| 40 | 52.609341554583% | 45.344531072985% | 48.905042746765% | **48.952971791444%** |
| 160 | 43.389924985133% | 39.592292530738% | 45.400277409186% | **42.794164975019%** |
| 320 | 41.437632336565% | 38.111186959411% | 41.198294770946% | **40.249038022308%** |

All nine master-by-size cells cleared the registered threshold. Because the rows
are nested and the master identities are reused, these are three repeatedly
viewed fixed masters, not nine independent replicates. Figure 3 is therefore a
deterministic robustness view, not a learning curve.

![Figure 3: Gain across nested profile-set sizes.](../figures/scaling_curve.svg)

*Figure 3. Conditional-regret gain persists across nested profile-set sizes.
Colored trajectories reuse the same three fixed public masters; the black
trajectory is their descriptive mean. Error bars: none. Test: none (secondary
descriptive nested robustness); p: not applicable. Source:
`paper/figures/scaling_curve.source.csv`.*

## Registered outcomes and execution resources

All **15/15** registered Phase-4 ledger rows resolved `confirm/keep`: three
baseline metrics, four core/control metrics, five OAT metrics, two changed-public
metrics, and one scale metric. This complete match documents calibration to the
registered local synthetic design; it is not evidence of perfect general
calibration or of correspondence with a live target.

Counting each scientific family once, the Phase-4 batch used **4.456198161 s**
of recorded scientific runtime and reached a maximum reported peak memory of
**0.583507538 GB**. The five OAT rows share one execution and the three scale
summaries share one execution, so repeated ledger resource fields are not summed.
The research cycle used one research iteration, with the active hypothesis at
iteration 4 after nine written ORF revisions and eleven theory-review rounds;
those revisions are not independent hypotheses or experimental units. No locked
test result entered this section.
