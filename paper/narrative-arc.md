# Narrative arc — PS-PIR internal technical report, revision 2

## Five-sentence spine

**Decision.** The audited scorer exposes a finite action table in which one
candidate fill length can be shared across all response profiles or, under an
oracle, selected separately for each profile. **Conceptual owner.** The
difference is an elementary deterministic instance of value of perfect
information and policy-class containment, not a new regret concept or learned
algorithm. **Worked example.** Public-Synthetic Perfect-Information Regret
(PS-PIR) computes that difference on three named, designer-specified crossed
tables and checks the equality code path on three homogeneous tables. **Result.**
The named crossed-table gains are 41.437632%, 38.111187%, and 41.198295%, whereas
the homogeneous tables have exact zero regret; action and stratum diagnostics
show how the engineered heterogeneity appears in these tables. **Boundary.**
These calculations establish neither informative live observations, a learnable
selector, an untouched-test result, a practical utility threshold, nor a Kaggle
or agent-security performance gain.

## Research journey without hindsight repair

An earlier live aggregate underperformed its public mock forecast. Project notes
proposed latency, reserve, parsing, and aggregation explanations, but the current
study did not run a diagnostic protocol that identifies those causes. Revision 2
therefore retains only the observed miss as historical context and labels the
proposed explanations as diagnostic hypotheses.

The project then narrowed the question to a table-level audit: if every
counterfactual action score were known, how much score would one shared action
lose to row-wise choices on a specified construction? This is a useful scorer
unit test, but it bypasses the operational learning problem. The retained probes
do not choose actions, and no context-to-action policy is trained or evaluated.

The public generator was adaptively repaired and calibrated before Phase 4.
Phase 4 subsequently froze labels and predictions for a public verification
calculation, but there was no untouched evaluation tier. The exact outcomes are
valid descriptions of the selected deterministic tables; their magnitude has no
confirmatory force outside those tables.

Round-1 paper review correctly identified that the original narrative assigned
too much scientific meaning to an engineered construction. Revision 2 therefore
moves the conceptual center to established information-value theory, supplies
the omitted action and stratum diagnostics, exposes the engineering provenance
of every synthetic choice, and treats sensitivity transforms as interacting
descriptive contrasts.

## Argument contract

Every scientific section must preserve all four propositions:

1. For any fixed finite score table, the row-wise perfect-information policy
   weakly contains the best shared action.
2. The reported magnitudes belong only to three named designer-specified tables;
   the homogeneous equality is a boundary/code-path sanity check.
3. The 5% line was a preselected internal numerical cutoff with no externally
   calibrated utility meaning.
4. No learner, live target, beacon, held-out tier, freeze action, Kaggle action,
   or external publication was executed.

## Contribution boundary

The report contributes an auditable scorer-specific worked example, diagnostics,
and a reproducible internal record. It does not contribute a new theorem, regret
definition, adaptive algorithm, empirical population finding, or demonstrated
agent-security opportunity. ORF-B / Beacon-Held-Out Conditional Regret is retained
only as the name of a prospective protocol that was not executed; PS-PIR names
the executed public calculation.

## End state

The final sentence must leave the reader with the right unit of knowledge: these
tables show how to calculate a perfect-information shared-action gap exactly,
while the operational question—whether observable probes support safe action
selection on an untouched target—remains unanswered and would require separate
authorization.
