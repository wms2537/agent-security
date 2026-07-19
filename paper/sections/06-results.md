# Results on named deterministic tables

The results below are exact arithmetic on designer-specified score tables. The
shared comparator exhaustively evaluated all seven legal lengths and selected
length **16** on each crossed table. Allowing the perfect-information policy to
select a length separately for every profile produced gains of
**41.437632336565%** on P0, **38.111186959411%** on P1, and
**41.198294770946%** on P2. The finite range across these three named values was
**38.111186959411--41.437632336565%**.

| Crossed table | Perfect-information score, \(A\) | Shared-action score, \(G\) | Raw gap, \(A-G\) | Shared length | Gain, \(100(A-G)/G\) |
|---|---:|---:|---:|---:|---:|
| P0 | 11,886,082 | 8,403,762 | 3,482,320 | 16 | 41.437632336565% |
| P1 | 12,187,804 | 8,824,632 | 3,363,172 | 16 | 38.111186959411% |
| P2 | 12,113,766 | 8,579,258 | 3,534,508 | 16 | 41.198294770946% |

These values describe P0--P2 only. Their arithmetic mean, used below solely to
compact the sensitivity summaries, is 40.249038022308%.

Figure 1 places the primary values beside the second public construction
reported below. The construction labels are not paired, and the two mean bars
do not define a between-construction test.

![Figure 1: Exact gains on two public designer-specified constructions.](../figures/comparison_chart.svg)

*Figure 1. Exact percentage gaps for three named tables in the primary public
construction (P0--P2) and three named tables in the changed public construction
(G0--G2). Black bars are descriptive arithmetic means. The dashed 5% line is a
preselected numerical cutoff with no external utility calibration. Error bars
and inferential tests: none. Source:
`paper/figures/comparison_chart.source.csv`.*

## Homogeneous boundary check

The homogeneous construction fixes length one as a row-wise optimum. Both the
shared and perfect-information policies selected length one throughout all
three homogeneous tables, and their scores were exactly equal:

| Homogeneous table | Perfect-information score | Shared-action score | Raw gap | Shared length | All row-wise lengths one |
|---|---:|---:|---:|---:|:---:|
| H0 | 1,277,552 | 1,277,552 | 0 | 1 | yes |
| H1 | 1,198,568 | 1,198,568 | 0 | 1 | yes |
| H2 | 1,230,140 | 1,230,140 | 0 | 1 | yes |

This entailed equality is a boundary and code-path sanity check. It is not an
empirical comparison between populations and does not independently establish
the source of the positive gaps in P0--P2.

## Row-wise action distributions

The perfect-information choices on the crossed tables were dispersed across
lengths 4, 8, 16, 24, and 32. Lengths 1 and 2 were never selected. Each row of
the table below sums to the 320 profiles in that named table.

| Crossed table | Shared length | \(m=1\) | \(m=2\) | \(m=4\) | \(m=8\) | \(m=16\) | \(m=24\) | \(m=32\) | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P0 | 16 | 0 | 0 | 66 | 96 | 72 | 53 | 33 | 320 |
| P1 | 16 | 0 | 0 | 66 | 85 | 83 | 52 | 34 | 320 |
| P2 | 16 | 0 | 0 | 65 | 96 | 69 | 58 | 32 | 320 |

The dispersion is direct description of the engineered profiles. It does not
show that a live observation reveals the listed choices or that these
frequencies occur outside the three tables.

## Stratum contribution accounting

The crossed construction contains 40 factorial strata. Aggregating the three
masters gives 24 profiles per stratum, **960 profiles** in total, and exact
aggregate raw regret of **10,380,000**. Four strata--13, 28, 33, and 38--had
zero raw regret. The five largest raw contributions were:

| Stratum | Raw regret | Share of total raw regret | Modal row-wise length |
|---:|---:|---:|---:|
| 6 | 1,064,390 | 10.254239% | 4 |
| 2 | 1,044,968 | 10.067129% | 8 |
| 1 | 1,016,548 | 9.793333% | 4 |
| 7 | 956,938 | 9.219056% | 8 |
| 0 | 883,284 | 8.509480% | 32 |
| **Top five** | **4,966,128** | **47.843237%** | -- |

The complete 40-row accounting, including reset band, linear band, curvature,
cliff value, profile count, raw regret, share, and modal length, is in
`paper/tables/stratum-regret-decomposition.tsv`. These entries allocate the
observed arithmetic gap across engineered strata; they are not causal component
shares or prevalence estimates.

## One-at-a-time sensitivity calculations

The core row and five one-at-a-time (OAT) transforms are summarized with their
raw quantities below. For each row, \(A\), \(G\), and \(A-G\) are arithmetic
means across P0--P2. The percentage column is the mean of the three exact
master-level ratios, so it need not equal the quotient of the displayed rounded
mean raw values.

| Condition | Mean \(A\) | Mean \(G\) | Mean \(A-G\) | Mean gain | Change from core |
|---|---:|---:|---:|---:|---:|
| Core | 12,062,550.667 | 8,602,550.667 | 3,460,000.000 | 40.249038022308% | -- |
| Remove cliff | 15,937,335.333 | 14,808,566.667 | 1,128,768.667 | 7.622073949240% | -32.626964073068 pp |
| Remove reset | 31,031,426.667 | 26,082,096.000 | 4,949,330.667 | 18.973588191963% | -21.275449830344 pp |
| Remove curvature | 15,676,959.333 | 11,373,606.000 | 4,303,353.333 | 37.860007927303% | -2.389030095004 pp |
| Remove novelty bonus | 11,935,712.000 | 8,521,525.333 | 3,414,186.667 | 40.094682770562% | -0.154355251746 pp |
| Remove saturation | 12,581,486.000 | 8,716,761.333 | 3,864,724.667 | 44.355152104598% | +4.106114082290 pp |

Cliff removal and reset removal produced the two largest removal-associated
decreases in the displayed percentage ratio. Novelty-bonus removal produced the
smallest change, and saturation removal increased the ratio. Every transform
changed both \(A\) and \(G\); the transforms also interact. The differences
therefore cannot be added or read as fractions attributable to separate
mechanisms.

Figure 2 retains the three master-level ratio changes behind the summary. It is
a display of paired calculations on reused tables, not a decomposition.

![Figure 2: Master-level OAT changes from the core percentage ratio.](../figures/ablation_heatmap.svg)

*Figure 2. Change from the core percentage ratio under five one-at-a-time
transforms of the same three named crossed tables. Colored points are exact
master-level changes and black diamonds are their arithmetic means. The
transforms change both policies' raw scores and may interact; no additive or
causal interpretation is assigned. Error bars and inferential tests: none.
Source: `paper/figures/ablation_heatmap.source.csv`.*

## Second public construction

A second designer-specified public construction produced gains of
**36.653863013959%**, **37.352060597349%**, and **35.175681399541%** on its
three named tables G0, G1, and G2, respectively. Their descriptive mean was
**36.393868336949%**. All three values were above the preselected 5% numerical
cutoff. The construction changes several engineering choices at once and was
also public, so its values are a second finite calculation rather than evidence
of transfer to another data source.

## Nested-prefix numerical sensitivity

The same P0--P2 profile order was truncated to nested prefixes of 40, 160, and
320 profiles. The resulting exact percentage gaps were:

| Profiles per table | P0 | P1 | P2 | Descriptive mean |
|---:|---:|---:|---:|---:|
| 40 | 52.609341554583% | 45.344531072985% | 48.905042746765% | 48.952971791444% |
| 160 | 43.389924985133% | 39.592292530738% | 45.400277409186% | 42.794164975019% |
| 320 | 41.437632336565% | 38.111186959411% | 41.198294770946% | 40.249038022308% |

All nine displayed cells are above the 5% numerical cutoff, but they reuse the
same three named tables and nested rows. They are not nine independent units. The
change across prefixes is a deterministic numerical-sensitivity result for this
fixed ordering, not evidence about how performance changes with additional
sampled data.

![Figure 3: Exact gaps across nested prefixes of the same tables.](../figures/scaling_curve.svg)

*Figure 3. Percentage gaps on nested 40-, 160-, and 320-profile prefixes of
P0--P2. Colored trajectories reuse each named table; the black trajectory is
their descriptive arithmetic mean. No new table is added as prefix length
increases. Error bars and inferential tests: none. Source:
`paper/figures/scaling_curve.source.csv`.*

## Descriptive status of the numbers

No sampling model was specified for the named synthetic tables, and no
inferential statistic is reported. Means are compact arithmetic summaries only;
the primary result is the three values and their range. The 5% line was selected
before these frozen public calculations as an internal numerical cutoff, but it
was not calibrated to deployment utility, cost, or risk. Accordingly, clearing
that line carries no external practical interpretation.
