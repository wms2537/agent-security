# Analysis Iteration 9 — Four-Endpoint Density Refutation

**Date:** 2026-08-02 · **Phase:** 5 · **Cycle:** 3 · **Iteration:** 9 · **Status:** completed

## Statistical declaration

```text
independent_unit:   one Kaggle code-competition submission for leaderboard rows; one local run/seed for local rows where present
n_units:            1 per leaderboard condition in iteration 9; no multi-seed statistical claim is supported
comparison_family:  kept public_score leaderboard rows only for rankings/statistics; crash/discard/exploratory/invalid rows excluded
correction:         none for the preregistered primary comparison; no p-values computed because n=1 per leaderboard condition
```

No t-test, p-value, seed-standardized effect size, or paper-bound statistical claim is valid for the v35/v36 leaderboard comparison. The useful signal is operational: visible score versus blank rerun/runtime boundary.

## Ledger and status counts

Orchestrator checks:

- `wc -l results.tsv` -> `175 results.tsv` (`174` data rows plus header).
- Status counts from `results.tsv`: `keep=28`, `exploratory=101`, `crash=13`, `discard=9`, `invalid=9`, `preregistered=12`, `mechanics-only=1`, `superseded=1`.
- Public-score rows:

| run_id | predicted | actual | signal | status | interpretation |
|---|---:|---:|---|---|---|
| `lb-stagea-fixed1950` | `87.750` | `NA` | `NA` | `preregistered` | superseded by later format/boundary diagnosis |
| `lb-stageb-sm2call-rc500` | `81.225` | `65.320` | `partial` | `discard` | partial per-candidate density but total regression |
| `lb-stageb-sm2call-rc650` | `84.916` | `NA` | `disconfirm` | `discard` | blank hidden-boundary failure |
| `lb-public-control-validation-fill-gpu` | `88.5-89.2` | `86.670` | `partial` | `keep` | current safe floor |
| `lb-stageb-four-endpoint-rc320` | `105.600` | `NA` | `disconfirm` | `crash` | v36 blank hidden-boundary failure |

Only one `public_score` row is currently `keep`: v35 at `86.670`. Therefore no comparison chart was generated; a one-bar chart would add no information, and crash/discard rows must not be plotted as zero.

## Prediction versus reality

The preregistered v36 hypothesis predicted `105.600` if `320` exact four-endpoint candidates fully fired and transferred through replay. Reality: ref `55177045` completed with blank public/private score despite a clean commit-run schema/source gate. The decision gate in report 239 classified this exact outcome as a hidden rerun/runtime/replay-boundary failure. Report 242 records the branch as refuted, and report 243 disables blind dense by default.

The most informative miss is not that local `CompliantAgent` could produce four predicates; that was already a mechanics fixture. The miss is that exact-shape probe admission plus blind dense emission is not enough under the hidden competition replay boundary. The next density path must charge exact dense-candidate generation cost and keep only fired candidates, rather than admit once and emit hundreds blindly.

## Seven Phase-5 analysis questions

1. **Did it work?** No. The primary comparison did not reach `105.600`, did not beat v35, and did not produce a visible score. It failed by the preregistered blank-score gate.

2. **Why did it work or not?** The evidence supports a resource/replay-boundary explanation, not a local CSV/schema explanation. Commit-run artifacts passed `Id,Score`, non-empty rows, source match after wrapper-newline normalization, dense constants, and no traceback. If dense admission had failed, the v35 fallback should have scored visibly. The likely failure surface is admitted blind dense rc320 crossing a hidden rerun/runtime/replay boundary.

3. **What contributed most?** The component that caused failure is blind post-admission dense emission. The v35 fallback remains valuable, but it was bypassed when dense admitted. The distinguishing prediction of four-event score density did not survive as an end-to-end system result.

4. **How robust is it, and where does it fail?** There is no robustness evidence: n=1 live submission and one blank result. The failure is decisive for this exact branch because blank score was preregistered as failure. It does not prove all multi-event density is impossible; it refutes this unmeasured rc320 blind-emission controller.

5. **What was surprising?** The surprise is operational rather than statistical: local exact-shape mechanics and clean commit-run schema were insufficient to prevent a blank hidden rerun. This repeats the project lesson that generation-side/local measurements do not identify full replay capacity.

6. **How does it compare to literature/public baselines?** A live check on 2026-08-02 shows the public leader remains `112.865`, with multiple public scores above `108`. A current public-kernel list still includes high-vote notebooks such as `foysalemonshanto/ai-agent-security-v12`, `nctuan/jed-v25`, `dimong4/ai-agent-security`, and `tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery`. The earlier pulled `nctuan/jed-v25` audit found active dense/burst settings effectively disabled (`BURST_K = 1`, `SLOW_MULTIPOST_N = 1`), so public high-80 controls do not solve the above-100 density requirement.

7. **Does it solve the problem?** No. It improves the search state by pruning a bad branch and restoring the safe floor, but it does not maximize the competition score. The core problem remains: find a source-compliant allocation policy that increases score density without voiding the hidden replay boundary.

## Freshness check

Current live checks:

- `comp/.venv/bin/kaggle competitions leaderboard -c ai-agent-security-multi-step-tool-attacks -s | head` -> leader `ADARSH REDDY B` score `112.865`.
- `comp/.venv/bin/kaggle kernels list --competition ai-agent-security-multi-step-tool-attacks --sort-by scoreDescending --page-size 5 --format json` -> top public refs include `foysalemonshanto/ai-agent-security-v12`, `nctuan/jed-v25`, `dimong4/ai-agent-security`, `canqiang/aiagsec-ea-b-0721`, and `tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery`.

No new evidence from these checks rescues blind four-endpoint rc320. They keep the competitive target above the single-post floor.

## Search diagnosis

Kind audit: iteration 9 is correctly `kind=metric` because it predicted a public-score improvement over the baseline.

Ledger counts:

- Cumulative status counts: `keep=28`, `exploratory=101`, `crash=13`, `discard=9`, `invalid=9`, `preregistered=12`, `mechanics-only=1`, `superseded=1`.
- Cumulative non-NA signal counts: `confirm=110`, `partial=22`, `disconfirm=17`, `null=24`.
- Confidence calibration over non-NA rows: `high` -> 27 confirm / 39 total; `medium` -> 13 confirm / 36 total; `low` -> 70 confirm / 98 total. This table mixes older synthetic/mechanics rows with live Kaggle rows, so it is useful as a miscalibration warning, not as a probability model for the next leaderboard run.

Cycle-3 metric dimensions:

| iteration | direction | varies | outcome |
|---:|---|---|---|
| 1 | progressive-online-replay-frontier | candidate-message-multiplicity-and-cost-aware-online-allocation | inconclusive |
| 1 | nested-prefix-gate-8 | candidate-boundary-density-via-nested-prefix-gating | inconclusive |
| 2 | monotone-prefix-controller-24 | monotone-24-to-8-prefix-control | refuted |
| 3 | prefix-risk-absorbing-controller-24 | complete-cell-resource-risk-admission-and-absorbing-stop | inconclusive |
| 4 | success-conditioned-operand-chains-32 | conversation-resident-invariant-factorization-and-self-success-continuation | refuted |
| 6 | dual-budget-evidence-reuse | probe-output-admission-under-separate-generation-and-replay-budgets | refuted |
| 7 | stagea-fixed-count-single-post-throughput | candidate-count-and-probe-overhead | improved |
| 8 | stageb-single-message-two-call-density | single-message-multi-tool-event-density | refuted |
| 9 | stageb-single-message-four-endpoint-density | exact-within-message-endpoint-density-admission | refuted |

Verdict: stalled by outcome. The last two metric iterations both failed to improve `best_state`, but they do not share the same `varies` dimension, so the same-dimension escalation trigger does not fire. The structural response is still required: do not retry blind dense; change the allocation mechanism.

## Budget check and path decision

Before this analysis, `research_iterations` was `9/9`, so the default SciAgent decision is conclude. The user then answered `ok, go on then` immediately after the recommended next repair path was stated. I interpret that as one bounded user-approved extension for the measured density repair only: `9/9 -> 10/10`.

Path comparison:

| candidate next step | failure mode | hardest trap | evidence check | score |
|---|---|---|---|---:|
| Measured validation-fill density controller | generation budget may admit too few dense candidates to beat v35 | accidentally recreating blind emission or double-counting probe cost | v33 proves partial within-message density; v36 proves blind emission unsafe; v35 fallback works | `5*3/4 = 3.75` |
| Shrink blind four-endpoint count | still blanks or cannot reach leader when made small enough | treating a lower count as a new mechanism | v36 directly refutes blind rc320; arithmetic requires ~342 fully firing four-event candidates to beat `112.865` | `2*2/3 = 1.33` |
| Single-post micro-tuning | cannot exceed the `90` single-post ceiling | spending submissions below the winning frontier | v35 `86.670` is useful floor but not enough | `1*4/2 = 2.00` |

Decision: Path A with the first option. Enqueue one Phase-2 task for a measured validation-fill density repair. The required distinguishing prediction is that charging exact dense fill cost and keeping only fired dense candidates avoids blank-score failure while preserving a route to above-ceiling score density. No Kaggle submission is authorized until the new preregistration and local/commit gates pass.

## Gate Check

- Analyzer dispatch attempted: `phase5_analyzer` was spawned, but after repeated waits it wrote no `research-log/244...` artifact and no new figure files; it was interrupted and this deterministic orchestrator analysis was written.
- Ledger row count: `wc -l results.tsv` -> `175 results.tsv`.
- Status counts: Python ledger scan -> `crash 13`, `discard 9`, `exploratory 101`, `invalid 9`, `keep 28`, `mechanics-only 1`, `preregistered 12`, `superseded 1`.
- Headline recomputation: `320 * ((4 * 16 + 2) / 200) = 105.600`; actual v36 metric is `NA`/blank, so primary prediction is disconfirmed by the preregistered blank-score gate.
- Freshness: Kaggle leaderboard head -> `ADARSH REDDY B ... 112.865`; public-kernel list includes current high-score public notebook refs.
- Figure QA: no new figure generated because there is only one kept `public_score` row; crash/discard rows are excluded from ranking figures.
- User approval for bounded continuation: `ok, go on then`.

## Problem alignment

This analysis advances the core competition question by pruning a hidden-boundary failure and selecting the next structural mechanism that directly targets score density without repeating the failed blind-emission controller.

## Next Steps

Phase 2 iteration 10: preregister a measured validation-fill density controller. It must probe exact dense shapes, charge all probe/fill costs, keep only candidates that actually fire, preserve the v35 fallback, and forbid blind dense scaling before target-owned evidence supports it.
