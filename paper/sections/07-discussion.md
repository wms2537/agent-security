# Discussion

## Scope of the calculation

PS-PIR answers a narrow deterministic question. On the three named crossed
tables, allowing a row-wise perfect-information choice instead of one exhaustive
shared choice produced ratios of 41.437632336565%, 38.111186959411%, and
41.198294770946%; the shared action was length 16 in all three tables. On the
three homogeneous tables, both policy classes selected length one and the raw
gap was exactly zero. These are exact properties of those score tables and a
boundary check of the implementation. They are not estimates of an
agent-security population.

The direction of the comparison follows from policy-class containment, while
the positive magnitude comes from the tables that were supplied. The crossed
generator deliberately varies reset cost, linear cost, curvature, and yield
cliffs over equally weighted strata. Its ranges, factor frequencies, replay
reserve, and weights are engineering stress-test choices rather than measured
features of live response profiles. Moreover, the generator family was
adaptively developed and repaired during public proof-of-concept and calibration
work before the Phase-4 config was frozen. The ensuing calculation is therefore
post-calibration frozen public verification: freezing prevented further
within-stage changes, but it did not remove construction-selection bias or
create an untouched evidence tier.

The second public construction and the nested prefixes do not change that
inference. A mean ratio of 36.393868336949% under a different public weighting
and means of 48.952971791444%, 42.794164975019%, and 40.249038022308% for the
40-, 160-, and 320-row prefixes are further arithmetic descriptions within the
same design program. The prefixes reuse rows from the three primary tables, and
the changed construction remains designer specified. Likewise, the 5% line was
a preselected numerical cutoff without external utility calibration; crossing
it says nothing about practical importance.

## Heterogeneity represented in the engineered tables

The action counts make the source of the finite gap visible without extending
it beyond the construction. Although the best shared action is length 16 for
each table, the row-wise comparator uses lengths 4, 8, 16, 24, and 32. Across
the three tables, the respective per-table count ranges are 65--66, 85--96,
69--83, 52--58, and 32--34; lengths 1 and 2 are unused. This dispersion shows
that the constructed score rows have different maximizing columns. It does not
show that naturally occurring profiles have these frequencies, that the five
actions are distinguishable from retained probes, or that a realizable policy
could select them.

The stratum accounting adds the score margins that an action histogram omits.
Across 960 rows, 36 of the 40 designed strata have positive regret and four
(`13`, `28`, `33`, and `38`) have zero regret. Total raw regret is 10,380,000,
and the five largest stratum shares sum to approximately 47.843%. Thus the gap
is distributed across many cells of this table but is also concentrated in a
few of the largest designed cells. Because strata were crossed and equally
weighted by construction, these shares are bookkeeping over engineered support,
not causal contributions or prevalence estimates.

## Interacting removal contrasts

The one-at-a-time calculations should be read as transformations of the whole
score table, not as a decomposition. In the primary condition, mean raw
perfect-information score (A), shared score (G), and gap (A-G) are
12,062,550.667, 8,602,550.667, and 3,460,000.000. Removing cliffs changes those
three quantities to 15,937,335.333, 14,808,566.667, and 1,128,768.667 and lowers
the displayed ratio from 40.249038022308% to 7.622073949240%. Removing reset
cost instead changes them to 31,031,426.667, 26,082,096.000, and 4,949,330.667,
while the ratio falls to 18.973588191963%. These examples show why a ratio
change cannot be assigned to one component: its numerator and denominator both
move, and the raw gap may increase while the ratio decreases.

Among the five displayed transforms, cliff and reset removal produced the two
largest decreases in the percentage ratio. Curvature removal produced
37.860007927303%, novelty removal produced 40.094682770562%, and removing
saturation produced 44.355152104598%. The transforms interact and were not
combined factorially, so their changes are neither additive shares nor
identified mechanisms. They describe how the selected deterministic tables
respond to five specified edits.

## Historical failures are separate evidence

The project history contains disconfirmations that should not be retrofitted as
support for PS-PIR. A local equal round-robin ensemble was forecast to score 66
but scored 56.76. A subsequent weighted allocation improved that local result,
yet it did not establish transfer. More importantly, an earlier multi-post live
design was forecast at approximately 85 and returned 36.705. Project notes
proposed latency, reserve allocation, parser behavior, and aggregation mismatch
as possible explanations. The PS-PIR methods contain no timing, firing,
parsing, or attribution protocol capable of identifying those causes, so they
remain diagnostic hypotheses rather than findings. A later single-post rebuild
returned 69.570 against a forecast of 84--90, another reminder that local or
synthetic score calculations were not reliable live aggregate predictions.

The public synthetic path was itself adaptive. Six first-pass calibration rows
crashed because of an exact-numeric conversion defect and were rerun only after
the numeric implementation repair; the proof of concept and repaired calibration
outcomes then informed the selected Phase-4 construction. Preserving these failures in
the ledger is essential to interpreting the final tables: the exact arithmetic
is reproducible, but the construction was selected after substantial public
development. Neither the failed live forecasts nor the repaired calibration
establishes why the engineered table has its reported magnitude.

## Missing operational evidence

The difference between PS-PIR and an operational policy is the information and
evaluation problem. PS-PIR grants the row-wise comparator all seven
counterfactual scores before it acts. A deployable study would first need to
define observations available before the length choice and a policy class that
maps those observations to legal actions, as contextual-bandit and heterogeneous
policy-learning work does [2], [4]. It would then need to train or select that
policy without leaking unavailable counterfactuals and evaluate its value under
the relevant feedback and identification assumptions [3]. If the probes were
themselves selected sequentially, the information-acquisition policy and its
structural assumptions would also need to be explicit rather than equated with
full-table access [5].

None of those steps is an implementation detail that can be inferred from the
oracle gap. The retained probes in this study never choose a fill length, no
selector-error curve is measured, and no partial-feedback policy value is
estimated. The study also supplies no calibrated latency-tail model or
whole-run failure-risk guarantee. Consequently, it neither demonstrates an
agent-security opportunity nor establishes that any fraction of the
perfect-information difference is attainable as a replay-safe, deployable gain.

## Governance and availability boundary

For PS-PIR, no beacon was fetched; the prospective ORF-B protocol was not
frozen or opened; and no held-out, live-target, private-target, or Kaggle action
was performed. No external archive, DOI, submission, or public release was
created. The repository supports internal deterministic replay, but it does not
provide an externally durable publication package. Any learner study or target
evaluation would be new work requiring its own prospective design and explicit
authorization. The present evidence ends with a reproducible calculation on
designer-specified public synthetic tables, not a passed external evaluation.
