# Conclusion

The executed Public-Synthetic Perfect-Information Regret (PS-PIR) calculation
is a reproducible scorer case study on three named, designer-specified crossed
tables. Relative to the exhaustive shared length 16, the row-wise
perfect-information comparator produced exact gains of **41.437632336565%** on
P0, **38.111186959411%** on P1, and **41.198294770946%** on P2, a finite range
of **38.111186959411--41.437632336565%**. On the three homogeneous tables, both
comparators selected length one and the raw gap was exactly zero; this is the
constructed boundary and code-path sanity check.

The action histograms and stratum accounting describe the heterogeneity built
into the crossed tables. Among the one-at-a-time transformations, cliff and
reset removal produced the two largest removal-associated decreases in the
displayed ratio, but those interacting contrasts do not identify component
shares or mechanisms. Because the table family, coefficient ranges, strata,
weights, and numerical cutoff were engineering choices, none of these exact
magnitudes establishes behavior beyond the specified tables.

PS-PIR contributes no new regret concept, theorem, algorithm, or learner, and
it demonstrates neither an agent-security opportunity nor a deployable gain.
ORF-B / Beacon-Held-Out Conditional Regret names only a prospective protocol
that was not executed; it is not part of the PS-PIR evidence. The unanswered
operational question is: can observations available before the candidate-length
choice, without counterfactual action scores, support a context-to-length policy
that exceeds the best shared length under the same resource and scoring
constraints on an untouched operational target?
