# ORF Phase-5 analysis gate and path decision

**Date:** 2026-07-19 · **Phase:** 5 · **Cycle:** 1 · **Iteration:** 4  
**Decision:** conclude the authorized public-synthetic study as an internal
technical report; advance to Phase 6 only to assemble and review that report

## Analyzer verification

The mandatory independent analyzer wrote
`research-log/042-analysis-iter-4-tables.md`, the reproducible plotting program
`experiments/orf-phase5-analysis/generate_figures.py`, and three figure triples
under `paper/figures/`.

Independent orchestration checks returned:

```text
results.tsv data rows=42; lines including header=43
status counts: keep=26 exploratory=7 crash=6 discard=1 superseded=1 mechanics-only=1
Phase-4 analysis rows=15, all confirm/keep
python -I experiments/orf-phase5-analysis/generate_figures.py -> exit 0
all nine SVG/PNG/source-CSV hashes unchanged by deterministic rerun
comparison_chart: SVG text PASS; PNG 1050x750 at 299.9994 dpi
ablation_heatmap: SVG text PASS; PNG 1050x795 at 299.9994 dpi
scaling_curve: SVG text PASS; PNG 1050x765 at 299.9994 dpi
source-data equality against core/generalization/ablation/scaling tables=PASS
report headline/declaration/exclusion checks=PASS
python -m py_compile experiments/orf-phase5-analysis/generate_figures.py -> exit 0
git diff --check -> exit 0
```

The project venv does not contain matplotlib, so the reproducible figure command
uses the workspace's system `python`, which does. This is an environment note,
not a change to scientific output.

The figures visually pass the figure-spec contract: readable final-size type,
honest axes, no top/right spines or default grid, frameless legends, direct unit
labels, and no redundant panels. Their SVGs retain editable `<text`; every PNG
has 300-dpi metadata; source rows exactly reproduce plotted values. Each report
legend declares `n`, the independent unit, lack of error bars, no population
test, and `p = not applicable`.

## Headline recomputation by the orchestrator

The registered comparison is paired ADAPTIVE versus exhaustive PROBE_GLOBAL on
the same three fixed public masters. From the committed `core-by-master.tsv`:

```text
master gains (%) = [41.437632336565, 38.111186959411, 41.198294770946]
mean              = 40.24903802230733%
sample s.d.       = 1.8552967398570896 percentage points
mean / s.d.       = 21.694124264675658 measured-master s.d. units
paired raw gains  = [3482320, 3363172, 3534508]
mean raw gain     = 3460000
finite min-max    = 38.111186959411–41.437632336565%
```

Rounded to the committed precision, the headline is **40.249038022308%**, with
sample s.d. **1.855296739857 pp** and descriptive standardized gain
**21.694124264676 measured-master s.d. units**. Every master clears the 5%
materiality threshold. Because these are three pre-specified deterministic
masters and no sampling population was declared, the valid result is an exact
finite contrast: `test: none; p: not applicable`. A population t-test or CI
would add an assumption the experiment did not earn.

### Statistical-rigor P0 checklist

- **Pseudoreplication:** PASS. `n=3` masters, never 960 profiles, 6,720 scores,
  320 profile decisions, 15 ablation cells, or nine reused scale cells.
- **Comparison family:** PASS. One pre-specified primary comparison; five OAT,
  one changed-regime, and three scale summaries are explicitly descriptive.
- **Interaction error:** PASS. No difference is inferred from different
  significance outcomes; no significance language is used.
- **Paired-design match:** PASS. The primary and OAT records preserve master
  pairing; changed-regime masters are explicitly unpaired and not tested.

## Seven required analysis answers

1. **Did it work?** Yes, on the registered public deterministic finite target.
   The exact 40.249% mean gain exceeds 5% for all three independent master
   units, with a descriptive 21.694-master-s.d. standardized effect. This does
   not license population inference.
2. **Why?** The inequality `sum_z max_m S_z(m) >= max_m sum_z S_z(m)` guarantees
   direction, while heterogeneous profile optima create magnitude. The crossed
   tables supplied that heterogeneity; the homogeneous control removed it and
   produced exact equality.
3. **What contributed?** OAT removal of cliffs reduced the core gain by
   32.627 pp and removal of reset overhead by 21.275 pp. Curvature contributed
   2.389 pp, the novelty constant only 0.154 pp, and saturation suppressed
   4.106 pp of conditional value. Effects are non-additive. The distinguishing
   crossed-positive/homogeneous-zero prediction held exactly.
4. **How robust, and where does it fail?** Three disjoint changed-regime masters
   averaged 36.394%, and all nine nested cells cleared 5%. These are public
   deterministic checks, not nine independent samples. The mechanism fails by
   construction when profiles share an optimum (zero gain); without cliffs the
   mean falls to 7.622%, close enough that less heterogeneous support could fall
   below materiality. It also fails operationally until a learner can infer the
   action and replay-tail safety is established.
5. **What was surprising?** Phase 4 had no disconfirm/partial/null signal. The
   largest forecast deviations were no-reset at -3.026 pp and no-curvature at
   +2.860 pp. Historically, the discarded equal-round-robin run and superseded
   real-LB v1 were informative disconfirmations: high constructed scores did not
   imply a high live aggregate under latency and reserve dilution. Six ORF
   calibration-v1 nulls were numeric implementation crashes; exact per-parameter
   Fraction conversion fixed the design. The remaining cumulative null was an
   exploratory Go-Explore timeout, whose fix is cost prescreening or an adequate
   declared budget before treating it as an experiment.
6. **How does it compare to literature and the tuned baseline?** PROBE_GLOBAL is
   the strongest local comparator: an exact seven-action argmax under identical
   inputs/resources with no tuning degree left. No published result shares this
   bespoke metric. The freshness check found that adaptive allocation is already
   a mature neighboring idea: Snell et al. (ICLR 2025), Plan-and-Budget (2025),
   Learning When to Plan (2025/2026), SCALE (AAAI 2026), and Budget-Aware Value
   Tree Search (2026) all condition inference resources on instance, subproblem,
   trajectory, or budget state. Exact sources and distinctions are in
   `research-log/043-orf-phase5-freshness-check.md`.
7. **Does it solve `PROBLEM.md`?** Only a proxy. It establishes exact public
   synthetic oracle information value under SDK-shaped scoring. It does not
   produce a learnable online selector, demonstrate live model heterogeneity,
   control replay-tail void risk, transfer across private guardrails, or beat a
   leaderboard baseline. The problem cannot honestly be marked solved.

## Search diagnosis

### Kind audit and run-flow counts

The single `search_log` entry remains correctly classified `kind: metric`: its
ledger contains the primary row predicted to beat the comparator, and the
result improves the active public-synthetic primary state.

| Scope | Keep | Discard | Crash | Exploratory | Other | Search denominator | Keep rate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Iteration 4 ORF (`orf-cal-*`, `poc`, `orf-p4-*`) | 18 | 0 | 6 | 6 | 0 | 30 | 60.0% |
| Before iteration 4 | 8 | 1 | 0 | 1 | 2 | 10 | 80.0% |
| Cumulative | 26 | 1 | 6 | 7 | 2 | 40 | 65.0% |

“Other” is one `superseded` and one `mechanics-only` row and is excluded from
the keep-rate denominator. The lower iteration keep rate reflects the preserved
six-row numeric crash plus six explicitly exploratory calibration rows; the
confirmatory Phase-4 batch itself is 15/15 keep.

Null signals are **6 this iteration and 7 cumulative**. Each has a named design
fix above; Phase 4 contains none.

### Forecast calibration

Rates below use all ledger signals, including nulls, because silent removal of a
crash would overstate calibration.

| Confidence | Iteration-4 confirm / total | Iteration-4 rate | Cumulative confirm / total | Cumulative rate |
|---|---:|---:|---:|---:|
| High | 9/9 | 100.0% | 15/15 | 100.0% |
| Medium | 5/5 | 100.0% | 6/9 | 66.7% |
| Low | 10/16 | 62.5% | 10/18 | 55.6% |

The high-confidence tier does not trigger the below-50% distrust rule. Phase 4
alone confirmed all seven high-, five medium-, and three low-confidence rows;
that perfect local record must not be extrapolated to the live target.

### Dimension and verdict

| `varies` dimension | Metric iterations | Best-state improvements |
|---|---:|---:|
| `candidate-structure-policy` | 1 | 1 public-synthetic improvement |

Set the iteration outcome to canonical `improved`. Verdict: **healthy but
externally incomplete**. Only one metric iteration exists, so neither the
two-entry same-dimension escalation trigger nor the two-entry diminishing-return
rule can fire.

## Budget and validation-overfitting audit

- Research iterations: 1/5 spent; four remain.
- Hypothesis-review rounds: 11/20 spent; nine remain.
- Paper-review rounds: 0/2 spent; two remain before Phase 6 dispatch.
- Compute: the Phase-4 batch used 4.456198161 reported CPU seconds and at most
  0.583507538 GB peak memory; no further experimental compute is required for
  the authorized report.
- Validation overfitting: the disjoint public changed-regime result tracks the
  primary direction, but it is not a locked validation/test tier. With
  `orf-heldout-v7` unfrozen and unopened, validation-overfitting and engineered-
  support risk remain unresolved.
- Retryable `implementation_defeated` options: none. Both recorded failed
  approaches are empirical refutations and are not eligible for silent retry.

## Path C and publish decision

### Steelman against publishing

The strongest venue-standard objection is cumulative: no locked test is
authorized; all positive evidence is public and purpose-built; `n=3` is a fixed
finite description; ADAPTIVE is an oracle rather than a deployable learner; the
result does not answer replay safety or live/private transfer; and fresh work
already covers the broad adaptive-allocation idea. Publishing a contribution
paper now would invite readers to infer novelty and deployment evidence that are
not present. A negative-result paper is also inappropriate because the tested
proxy is strongly positive and the unresolved operational question was not
tested with power.

Therefore choose outcome **(c), internal technical report — no submission**.
The user's advance authorization was: “then go on with next phases up until
phase 6 then, define a goal”, followed after Phase-4 closure by “continue
working”. The user-defined goal explicitly calls for a “Phase-6 paper/report”
while prohibiting Kaggle and held-out actions. That authorizes local report
assembly, not external publication.

The normal empirical Path-C instruction to run the locked test exactly once is
**not executed and not marked satisfied**. The user's explicit authorization
boundary forbids held-out/beacon/freeze/target/evaluation actions. The report
must carry this as an evidence limitation and a deliberate gate exception. No
Kaggle or held-out action occurred.

## Gate Check

- Seven analysis questions: PASS, explicitly answered above.
- Analyzer output, row counts, exclusions, figures, source data, and headline:
  PASS by independent checks.
- Statistical declaration and P0 rigor: PASS.
- Orchestrator headline recomputation: PASS, exact evidence above.
- Freshness: PASS in research-log/043; adjacent novelty risk recorded.
- Search diagnosis, calibration, canonical outcome, and verdict: PASS.
- Budget and validation-overfitting checks: PASS.
- Escalation/candidate rubric: not triggered; no retryable candidate exists.
- Publish decision and local-report authorization: PASS for internal reporting;
  no submission authorized.
- Locked test exactly once: **NOT RUN — explicit user-scope exception, openly
  carried as a limitation rather than falsely checked.**
- Retrospective: enqueued as the final task after the requested Phase-6 report.

## Problem alignment

Advancing only an internal report preserves the core problem: the evidence is
useful as an exact diagnostic of possible online-structure value but is not
misrepresented as a replay-safe, transferable attack algorithm.

## Decision

Advance to Phase 6 for a source-backed, paper-shaped **internal technical
report**, not a submission manuscript. Preserve the locked-test and Kaggle bans.
