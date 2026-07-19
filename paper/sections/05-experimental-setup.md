# Experimental setup

## Evidence chronology

The calculations followed three distinct evidence stages. First, the generator
and analysis choices were developed through adaptive public exploration and
calibration. That stage included a 40-profile proof of concept, repairs to the
public support construction, and repeated hypothesis review. Its outputs
informed the crossed-table family, coefficient ranges, weights, and numerical
cutoffs used later. Second, the labels, actions, predictions, and public config
were frozen in `experiments/configs/orf-phase4-v1.json`, after which Phase 4 ran
a **post-calibration frozen public verification** of those choices. Freezing the
calculation after public calibration prevents outcome-dependent relabeling
within Phase 4, but it does not make the selected construction untouched.
Third, there was no untouched evaluation stage. The locked v7 construction was
neither frozen nor opened, and no live target, beacon, held-out evaluation, or
Kaggle action contributed evidence to PS-PIR.

## Named deterministic tables

The primary calculation uses three designer-specified crossed tables, named by
their ASCII master preimages:

1. `orf-public-phase4-v1|master|000`;
2. `orf-public-phase4-v1|master|001`;
3. `orf-public-phase4-v1|master|002`.

Each name is mapped once by SHA-256 to a deterministic master. Each primary
table has 320 profile rows and seven score columns, one for each legal fill
length in \(\mathcal M=\{1,2,4,8,16,24,32\}\). The 320 rows are the complete
cross of 40 designer-specified strata and eight keyed replicates per stratum.
The strata cross two reset-cost bands, two linear-cost bands, two curvature
settings, and five cliff settings. Equal stratum weights and all coefficient
ranges are engineering stress-test choices; they do not represent estimated
frequencies in a population. Keys include the master, stratum, and replicate,
so every row is recoverable without mutable random state. The reporting unit is
one complete named table; rows, score columns, strata, and nested prefixes are
components or views of those tables, not additional reporting units.

Three homogeneous tables append `|homogeneous` to the corresponding primary
preimages before hashing. Each contains 64 deterministic rows for which the
row-wise optimum is fixed at length one by construction. These tables exercise
the equality and tie-handling code paths; they are not an independently observed
negative condition.

The score cells are exact outputs of the construction described in Methodology.
The primary tables use \(H=200{,}000\), a 9,000-second generation budget, and an
8,100-second synthetic replay allocation. The 9,000-second value and scorer cap
are inherited from the audited SDK; the replay allocation, factor ranges, equal
weights, and 5% line are project choices. The 5% line was fixed before the
Phase-4 calculations solely as an internal numerical cutoff and has no external
utility calibration.

## Matched finite-table comparators

Both comparators receive the identical complete score table and the same seven
legal actions. The exhaustive shared comparator computes the column total for
every \(m\in\mathcal M\) and chooses the maximizing length once for the whole
named table. The perfect-information row-wise comparator chooses the maximizing
length separately in every row and then sums those row maxima. Both choose the
smaller legal length on a tie. Thus the comparison changes only the scope of the
argmax; it does not change profiles, actions, costs, caps, budgets, or scores.
The row-wise comparator is an oracle because it is granted all counterfactual
action scores. Retained probes do not select an action, and no context-to-length
learner is trained or evaluated.

## Sensitivity calculations

Three secondary calculation families describe how the displayed finite-table
ratio changes under specified transformations. They do not provide untouched
transfer evidence.

The one-at-a-time (OAT) family applies five transforms to the same three primary
tables: remove the cliff transform; set curvature to zero; set reset cost to
zero; remove the two-point novelty term; or replace \(H=200{,}000\) with
\(H=10^{18}\). No action set or comparator is retuned. Because a transform can
change both oracle and shared totals and the transforms interact, these are
removal-associated sensitivity calculations rather than component shares.

The changed-construction family uses the three public labels
`orf-public-phase4-generalization-v1|master|000` through `|002`. Despite the
legacy string in those labels and artifact paths, this is a second
designer-specified public construction, not an untouched replication. It uses
\(H=10^{18}\) and weights each no-cliff row four times and each cliff row once,
giving equal aggregate weight to the two groups within each named table.

The nested-prefix family reuses each primary table and includes replicate
indices \(0\) through \(k-1\) in every stratum for \(k\in\{1,4,8\}\), producing
40-, 160-, and 320-row prefixes. These nine master-by-prefix cells are dependent
views of three tables. They are a numerical sensitivity display, not additional
independent evidence or a learning curve.

## Descriptive outputs

For every named primary table, the report retains the exact shared total
\(G\), perfect-information total \(A\), raw gap \(\Delta=A-G\), percentage ratio
\(100\Delta/G\), selected shared length, and the complete row-wise action count
over all seven legal lengths. The primary display reports all three named ratios
and their exact minimum--maximum range. It does not replace those values with a
sampling model.

The stratum accounting reports, for each of the 40 crossed strata, the 24 rows
formed by that stratum across the three named tables, raw regret, share of the
finite total regret, and modal row-wise action. This accounting describes where
the engineered tables contain the finite gap; it is not a causal decomposition.
The OAT display reports raw \(A\), \(G\), and \(\Delta\), alongside the ratio,
for the primary condition and all five transforms. Homogeneous outputs retain
exact action identities and raw equality. Changed-construction and nested-prefix
outputs are reported as named-table or named-prefix values, with arithmetic
aggregates used only as deterministic summaries.

No population standard deviation, standardized score, confidence interval, or
hypothesis test is defined for these finite tables. The analysis declaration is
therefore `test: none; p: not applicable`. Passing the preselected 5% numerical
cutoff is a statement about these exact ratios only.

## Execution and internal reproducibility

All scientific commands are repository-relative and are run from the repository
root. The Phase-4 calculations used Linux x86_64, glibc 2.40, CPython 3.14.3 at
`comp/.venv/bin/python`, and `jsonschema==4.26.0`; they were CPU-only and made no
network calls. Dependency records are pinned in
`paper/reproducibility/requirements-core.txt` and
`paper/reproducibility/requirements-figures.txt`. Exact verification commands,
fresh-attempt rules, canonical inputs and outputs, and the separate figure
environment are listed in `paper/reproducibility/README.md`.

The core and secondary runners bind source, config, upstream evidence, and
outputs by SHA-256 in their `COMPLETE.json` manifests. The reviewer-requested
action, stratum, and raw OAT tables are regenerated with the repository-relative
command:

```bash
comp/.venv/bin/python experiments/orf-phase5-analysis/generate_reviewer_tables.py
```

This constitutes internal reproducibility from the present repository, not an
external availability claim. There is no public clone, externally archived
release, DOI, operating-system container, or durability guarantee.
