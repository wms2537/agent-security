# ORF Phase-6 paper revision — round-1 foundation

**Date:** 2026-07-19  
**Phase:** 6  
**Task:** T031  
**Trigger:** paper-review round 1, `NEEDS_REVISION`  
**Scope:** internal technical report; no submission or external release

## Decision

The round-1 review is correct at the claim-model level. The executed calculation
must not be defended as evidence of an agent-security opportunity. It is being
rebuilt as **Public-Synthetic Perfect-Information Regret (PS-PIR)**: a
deterministic scorer worked example on designer-specified tables and an
application of established value-of-information/policy-class containment.

`ORF-B` / `Beacon-Held-Out Conditional Regret` now names only a prospective
protocol that was not executed. No beacon, held-out freeze/open, target,
evaluation, private, live, or Kaggle action was taken in this revision.

## Branch-of-origin issue routing

All twelve reviewer issues were routed before prose revision in
`paper/revision-round1-blueprint.md`:

- construction, novelty, chronology, observability, naming, and statistics were
  routed back to the hypothesis/claim model;
- foundational-literature omission was routed to the literature database and
  Related Work plan;
- omitted action/stratum and raw OAT diagnostics were routed to Phase-5 analysis;
- reproducibility was routed to a local package/bootstrap record;
- unsupported historical causal language was routed to problem-evidence
  classification;
- the zero-yield contradiction was routed to formal notation.

The blueprint contains a v1 paragraph diagnosis, a target paragraph map, and a
writer dispatch contract. The narrative arc, motivation surfaces, 50-row writing
rationale matrix, and 32-claim source map were reconstructed before writer
dispatch. Scientific prose has no planned `KEEP` operation; the only
`KEEP-AS-ARCHIVE` item is the immutable 42-row historical ledger.

## Foundational literature correction

`research-log/lit/phase6-foundational.json` adds five primary, field-verified
conceptual owners:

1. Howard (1966), information value theory;
2. Langford and Zhang (2007), contextual bandits with side information;
3. Dudík, Langford, and Li (2011), doubly robust policy evaluation/learning;
4. Golovin and Krause (2011), adaptive stochastic optimization under partial
   observation;
5. Athey and Wager (2021), heterogeneous policy learning from observational
   data.

The search conclusion is adverse to broad novelty: PS-PIR is a deterministic
scorer-specific application of an established quantity. Observable-context
policy learning and evaluation own the operational step that this oracle table
does not test.

Database verification:

```text
phase6-primary.json: papers=5 verified=5 critical_mismatches=0 warnings=2
phase6-foundational.json: papers=5 verified=5 critical_mismatches=0 warnings=1
```

The single foundational warning records a title variation on the official
Epoch-Greedy proceedings page; the report will use the official landing-page
title. Total planned references are 10.

## Reviewer-requested diagnostics

`experiments/orf-phase5-analysis/generate_reviewer_tables.py` deterministically
generates:

- `paper/tables/action-distributions.tsv`;
- `paper/tables/oat-raw-summary.tsv`;
- `paper/tables/stratum-regret-decomposition.tsv`.

The first extension attempt used the ablation field name
`gain_percent_decimal` for a core row. The core source uses
`adaptive_gain_percent_decimal`; the run failed with `KeyError` before writing a
new table. The script was corrected, then strengthened to recompute the core
ratio from integer raw scores rather than average rounded display values. This
was an analysis-code schema repair, not an experiment rerun or result change.

Final audit:

```text
reviewer_tables=PASS files=3
reviewer_tables_deterministic=PASS
reviewer_table_audit=PASS action_rows=3 profiles=960 strata=40 regret=10380000
```

SHA-256:

```text
485d69de131af5891483db54ca351f10a5a1d4ba7efddddd50472a4ad07c7c12  paper/tables/action-distributions.tsv
0ad5d6aa150a4e0bf3e2611b1bdd01fed1c27aedd118300bd1ec038685007580  paper/tables/oat-raw-summary.tsv
0c2d53046d81dd93ee8f881c686b45d0738614c3d706d8a2baeeb21726b8f005  paper/tables/stratum-regret-decomposition.tsv
```

The action table shows global length 16 for every named master and row-wise
choices across lengths 4, 8, 16, 24, and 32. Across the 40 strata, four have zero
regret (`13`, `28`, `33`, `38`), total raw regret is 10,380,000, and the five
largest stratum shares sum to approximately 47.843%. These are contribution
descriptions of an engineered table, not causal or prevalence estimates.

The raw summary reports core plus all five OAT transforms. Core mean raw
`A/G/(A-G)` is `12,062,550.667 / 8,602,550.667 / 3,460,000.000`; OAT prose must
say only that particular removals produced the largest changes in the displayed
ratio, because both numerator and comparator change and transforms interact.

## SDK provenance correction

Motivating facts are now tied to audited local files:

- `comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py` for the
  9,000-second default, deadline enforcement, replay cap/slicing, and per-model
  generation/replay structure;
- `comp/sdk/aicomp_sdk/scoring.py` for unique-cell scoring and the 200,000
  normalization path;
- `comp/sdk/aicomp_sdk/attacks/contracts.py` for the attack time-budget
  contract.

The synthetic replay budget `B_rep=8100`, crossed ranges
`a in [5,20]/[40,80]`, `b in [0.1,1]/[2,8]`,
`d in {0} or [0.05,0.2]`, `lambda in [0.5,3]`, equal 40-stratum weights, and the
5% cutoff are project stress-test choices. They have no empirical prevalence or
utility calibration. The revised Methodology must display this provenance.

## Reproducibility correction

`paper/reproducibility/README.md` supplies repository-relative verification and
scientific-family commands, canonical inputs/outputs, recorded interpreter and
package versions, and explicit limits. Dependency records are:

- `requirements-core.txt`: `jsonschema==4.26.0`;
- `requirements-figures.txt`: `matplotlib==3.10.9`.

The documented toy-suite command was executed successfully:

```text
Ran 18 tests in 0.003s
OK
```

There is still no public clone, archive, DOI, OS container, or durability
guarantee. The revision will disclose that external reproducibility remains
incomplete instead of claiming publication readiness.

## Gate check

- Verbatim reviewer verdict logged before revision: PASS (`research-log/047`).
- All 12 issues routed to root artifacts: PASS.
- Foundational primary sources field-verified: PASS (5/5; 0 critical mismatch).
- Reviewer-requested tables deterministic and complete: PASS.
- Formal q-domain fix represented in blueprint/claim map: PASS.
- Deep-imitation planning completed before section rewrite: PASS.
- Kaggle/held-out/beacon/live/private action: NONE.

The revision foundation passes. Section rewriting may begin in ordered dependency
groups. Paper-review budget remains `1/2`; no review round is charged until the
fully assembled revision is committed and dispatched.
