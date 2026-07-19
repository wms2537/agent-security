# Cycle-1 retrospective — ORF to PS-PIR

**Date:** 2026-07-19 · **Phase:** 6 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed

## Context

Cycle 1 ended with the 1,184-line PS-PIR internal technical report at commit
`057f854`. Sterile paper-review round 2 returned `NEEDS_REVISION` for a top-tier
publication but `SUFFICIENT` for the report's explicit deterministic-worked-
example scope (`research-log/051`). The user then directed: **“ok approve another
2 review budget if you need it. continue iterating and developing new insights.
do approriatev researches about latest advancements in the domain please. it is
july 2026 now.”** This authorizes raising the paper-review limit from 2 to 4;
the new rounds remain unspent until dispatch.

This retrospective mines project learnings, failed approaches, reviewer history,
budgets/gates, and user corrections before the research loop re-enters Phase 1.

## Domain lessons

1. **PS-PIR is a value-of-perfect-information calculation, not a deployable
   policy.** The exact inequality and three named-table magnitudes are sound,
   but a scientifically stronger next contribution must define observations
   available before the action, learn a context-to-length policy, and evaluate
   it without full counterfactual access. Paper reviews 1 and 2 agree that more
   rhetoric cannot substitute for this step.

2. **Engineered crossed tables establish mechanics, not prevalence or practical
   scale.** The public generator deliberately creates action heterogeneity.
   Action histograms and stratum margins explain the table arithmetic, but no
   inference to live targets follows. This limitation recurred from theory
   review through both paper reviews.

3. **Mock-to-live forecast transfer was unreliable.** Equal round-robin scored
   56.76 versus 66 predicted; the multi-post live design scored 36.705 versus
   approximately 85; the later single-post design improved to 69.570 but stayed
   below 84–90. Latency, reserve, parser, and aggregation explanations remain
   diagnostic hypotheses unless measured by a dedicated protocol.

4. **The next estimand needs both decision value and acquisition cost.** A
   selector's value is not the oracle gap alone. It must subtract probe cost,
   selector error, replay-tail risk, and any policy-learning/evaluation error
   under partial feedback. Contextual policy learning, off-policy evaluation,
   and risk-aware resource allocation are therefore closer owners of the next
   question than another synthetic argmax calculation.

5. **Internal reproducibility and external scientific evidence are distinct.**
   Transactional manifests, exact hashes, deterministic tables, and local
   commands make PS-PIR internally auditable. They do not provide an external
   archive, untouched target, learner evaluation, or live-transfer evidence.

## Evidence mined from the cycle

### Learnings

- 28 learning entries exist. The nine earliest are unstructured strings; 19
  later entries use the required `{lesson, apply_when, source, recurrences}`
  schema.
- Promoted recurring lessons include simulator-to-live non-transfer
  (`recurrences=2` before this retrospective), replay-tail calibration
  (`recurrences=3`), and machine-readable protocol underdetermination
  (`recurrences=5`).
- Paper review repeated the finite-estimand/threshold and self-containment
  lessons, so their recurrence counters must be promoted rather than duplicated.

### Tried and failed

- Two approaches are recorded and both are empirical refutations: equal
  round-robin allocation, and the multi-post/reserve/hedge design.
- There are no `implementation_defeated` approaches, so the main failure mode
  was model mismatch rather than inability to execute code.
- One historical entry uses non-schema class
  `refuted-by-real-LB-and-source` instead of the allowed `refuted`; this is a
  state-validation defect. The historical record is retained.

### Reviewer history

- Hypothesis review consumed 11 of 20 authorized rounds. Round 10 still found
  four executable-contract blockers; round 11 accepted their repair as
  `RIGOROUS`.
- Core code review needed three rounds. It caught two HIGH defects before the
  scientific run: stale/partial bundle acceptance and symlink/lexical attempt
  identity. Focused ablation, changed-construction, and scaling reviews then
  passed in one round each.
- Paper review consumed 2 of 2 original rounds. Round 1 found 12 issues rooted
  mainly in claim scope, missing conceptual literature, missing diagnostics,
  statistics, and reproducibility. Round 2 classified ten resolved and two
  improved, accepted the internal-report scope, and found two new clarification
  issues: whole-phase freeze wording and undefined probe residual state.

### Budgets and gate behavior

- End-of-cycle usage before the new user grant: research iterations 1/5,
  hypothesis review 11/20, paper review 2/2.
- The code-review gate caught consequential defects and prevented contaminated
  execution; it earned its cost.
- The Phase-1 freshness gate was too application-neighbor-centric: five recent
  LLM allocation papers passed, but paper review later required VOI, contextual
  bandits, off-policy evaluation, adaptive optimization, and heterogeneous
  policy learning.
- The Phase-5 statistics gate passed sample SD and a standardized master-SD
  quantity despite declaring a fixed finite census; paper review correctly
  removed both.
- The Phase-6 deterministic checks were strong on numbers, citations, ledger
  bytes, and structural rewriting, but did not test claim-level chronology or
  whether every introduced state variable was defined sufficiently for a reader
  to reproduce the construction from prose.
- The locked-test exception worked as intended: the absence of held-out evidence
  stayed explicit and no prohibited action was laundered into a passed gate.

### User correction record

1. “we should develop our own moat instead of relying on others ya” redirected
   the problem from recipe reuse to online system identification.
2. “ok, then lets fix these blockers properly. Remmebr to do the right thing not
   the easy thing” rejected surface closure after theory-review exhaustion and
   led to the executable v9 contract.
3. “No Kaggle action is authorized” was correctly preserved across Phases 3–6.
4. The user questioned writing before Kaggle validation; the response clarified
   that the document was an internal pre-evaluation record, not a transfer claim.
5. The current direction explicitly asks for July-2026 advances and deeper new
   insights, so the next loop must begin with literature rather than manuscript
   polishing.

The recurring correction pattern is **scope and evidence before presentation**:
the user repeatedly preferred a narrower, properly supported artifact over an
easier surface-level success claim.

## Process-defect proposals

These are proposals for the SciAgent skill owner. No skill file is edited here.

| # | Skill file and section | Concrete proposed edit | Cycle evidence |
|---:|---|---|---|
| 1 | `phases/phase-1-literature.md` — search decomposition | Require every literature map to search two tracks before application neighbors: **conceptual owner of the estimand** and **operational owner of the missing step**. Gate on at least one foundational/closest source per load-bearing concept, not only recent papers. | The first five-paper update covered recent LLM allocation but omitted VOI, contextual policy learning/evaluation, and adaptive optimization; paper-review issue 5 forced a branch-of-origin rebuild. |
| 2 | `phases/phase-2-hypothesis.md` — mathematical/method completeness | Add a symbol-table executable-specification check: every state variable in the estimand must have a formula, starting state, update order, and source—or be labeled an imported observed table. Any “by construction” uniqueness/equality claim must be derivable from the written specification or downgraded to an observed table property. | Protocol-under-determination learning recurred five times; paper-review round 2 still found (g_z,r_z,p_z,Q_z) insufficiently defined. |
| 3 | `phases/phase-4-experiments.md` — preregistration chronology | Require a machine-readable `prediction_freeze.tsv` with one row per experiment family: global design/config commit, family prediction commit, code commit, review commit, and first result commit. Gate verifies strict ordering per family and forbids “the phase was frozen” shorthand unless all predictions share one pre-result commit. | Round-2 moderate issue: main text implied whole-phase prediction freeze, while baseline/core/OAT/changed/prefix predictions were frozen sequentially after earlier-family outcomes. |
| 4 | `phases/phase-5-analysis.md` — estimand/statistics declaration | Add a finite-census branch that mechanically forbids sample SD, standardized mean/SD quantities, CIs, p-values, and population language unless a sampling model is explicitly declared. Require threshold provenance: utility-calibrated, theory-bound, or normative/internal. | Phase 5 passed sample SD 1.855 pp and standardized value 21.694 for three named tables; paper-review issue 8 removed both and reclassified 5% as uncalibrated. |
| 5 | `phases/phase-6-paper.md` — claim chronology and scope lint | Before reviewer dispatch, extract every sentence containing `frozen`, `registered`, `confirmed`, `held-out`, `generalization`, `robustness`, or `material`; map it to a dated source event and evidence tier. A sentence without a one-to-one chronology row fails. | Round 1 found post-calibration confirmation overclaim; round 2 still found one freeze sentence inconsistent with the detailed timeline. |
| 6 | `SKILL.md` — ORIENT state validation | Add a deterministic schema audit for `learnings` objects and allowed `failure_class` values. Historical violations are reported, never silently rewritten; new writes fail before commit. | Nine learnings are legacy strings and one failed approach uses `refuted-by-real-LB-and-source`, outside the allowed enum. |
| 7 | `phases/phase-2-hypothesis.md` and `phases/phase-4-experiments.md` — pre-review verification ladder | Add domain-specific adversarial pre-review suites: state-machine predecessor coverage for contracts, actual SDK representation fixtures, and crash/symlink/alias publication tests for evidence bundles. Reviewer judgment comes only after these deterministic suites pass. | Theory round 10 found missing SDK hash representation, undefined scheduler state, external-post idempotency, and absent fixtures; core review rounds 1–2 found crash-atomicity and path-identity HIGHs. |
| 8 | `phases/phase-6-paper.md` — contribution readiness decision | Separate `internal-scope sufficient` from `top-tier publishable` in the paper gate. A top-tier verdict requires at least one of: novel theorem, learned/implemented method with fair baseline, observed phenomenon on an untouched tier, or a validated dataset/benchmark contribution. Rhetorical revisions cannot close a `requires new evidence` gap. | Round-2 reviewer found the report sufficient internally but top-tier-blocked by absent novelty, learner, observed phenomenon, and external evidence. |

## Gate Check

- Required sections `Domain lessons` and `Process-defect proposals`: present.
- Five evidence sources mined: learnings, tried/failed, reviewer history,
  budgets/gates, and correction record.
- Each process proposal names a skill file/section, concrete edit, and cycle
  evidence: 8/8.
- Skill files modified: 0.
- User-authorized paper-review increase recorded: limit 2 -> 4, spent remains 2.
- Kaggle/held-out/beacon/live/private/external-publication action: none.

## Problem alignment

The retrospective redirects the next iteration toward the missing operational
science—observable, replay-safe context-to-action learning—rather than further
optimizing the public synthetic oracle proxy.

## Decision

Close Cycle-1 Phase 6. Re-enter Phase 1 for a July-2026 literature update before
choosing any new active hypothesis. The next work must target a structurally new
dimension (learnable observation-to-action policy, risk-aware acquisition, or a
better evidence design), not another synthetic action-scope magnitude.

## Next Steps

After recording this closeout, read the Phase-1 playbook, increment the research
iteration budget, and search current primary literature through 2026-07-19. No
experiment may run until a new Phase-2 hypothesis, prediction, and review gate
exist.
