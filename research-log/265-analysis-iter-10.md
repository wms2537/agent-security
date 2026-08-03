# Phase 5 analysis — iteration 10 measured dense replacement

Date: 2026-08-03

## Inputs

- Active hypothesis: `stageb-measured-validation-fill-density`
- Preregistered hypothesis report: `research-log/254-hypothesis-iter-10-measured-density-overlay-v5.md`
- Theory review: `research-log/255-theory-review-measured-density-v5.md`
- Local implementation evidence: `research-log/259-exp-local-measured-dense-impl-gate.md`
- Code review: `research-log/260-code-review-measured-dense-replacement.md`
- Kaggle commit-run gate: `research-log/261-kaggle-v37-commit-run-gate.md`
- Submission result: `research-log/264-v37-measured-dense-result.md`

## Terminal result

The hypothesis is refuted on the target-owned metric.

The v37 submission completed visibly, which means the notebook wrapper, output-file path, and submission CSV mechanics were not the terminal blocker. The public score was `84.735`, below the retained v35 floor `86.670` and far below the preregistered success threshold `100.000`.

Verified evidence:

```text
comp/.venv/bin/kaggle competitions submissions ai-agent-security-multi-step-tool-attacks -v | rg "55189377|55158967|ref,fileName"
```

returned v37 ref `55189377` as `SubmissionStatus.COMPLETE` with public score `84.735`, and v35 ref `55158967` as `SubmissionStatus.COMPLETE` with public score `86.670`.

Arithmetic:

```text
delta_vs_v35 = 84.735 - 86.670 = -1.935
miss_vs_prediction = 84.735 - 100.000 = -15.265
```

## Seven-question analysis

### 1. Did the experiment work?

No.

The experiment passed the mechanical visibility gate but failed the target-score gate. Under report `254`, any visible score below `86.670` is failure. V37 scored `84.735`.

### 2. What mechanism does the result support?

It supports only a negative mechanism conclusion:

> Locally retaining 93-96 measured four-endpoint candidates before falling back to v35 validation fill does not transfer to a higher public leaderboard score.

It does not identify the hidden cause. Kaggle does not expose per-candidate replay logs, private guardrail decisions, per-cell timeouts, or exact scored-event counts. Therefore, the result must not be over-interpreted as one particular low-level failure.

Plausible non-identifiable explanations include:

- dense candidates replayed slower than their generation-side measurements suggested;
- some locally firing four-endpoint candidates lost events during fresh replay;
- the dense block displaced enough reliable fallback candidates to reduce total scored events;
- hidden per-candidate reset/construction/runtime costs differed from the local gate;
- model-specific behavior during the competition rerun differed from the commit-run/local probes.

### 3. Which component helped or hurt?

The wrapper and submission-format repair helped: v37 completed visibly rather than returning a submission format error or blank public/private score.

The measured dense replacement component hurt the competition score. The best direct comparator is v35:

| Run | Structure | Status | Public score |
| --- | --- | ---: | ---: |
| v35 | public-control validation-fill single-post floor | keep | 86.670 |
| v37 | capped measured dense replacement plus fallback | discard | 84.735 |

The observed delta is `-1.935`, so the dense replacement is not a keeper.

### 4. Is the result statistically robust?

No inferential statistics are justified.

The independent target unit is one Kaggle code-competition submission per condition. This is a leaderboard-controlled, hidden-evaluator measurement with no exposed per-candidate sample table. The correct analysis is descriptive and preregistered-bin based, not a p-value or confidence interval.

The decision is still valid because the result crossed a deterministic preregistered failure boundary:

```text
84.735 < 86.670
```

### 5. What was surprising, and what should not be "fixed" by guesswork?

The useful surprise is that v37 completed visibly after a long pending period but still regressed. That separates two failure classes:

- v34/v36-style blank/error outcomes: hidden format/runtime/replay-boundary failure before a usable score.
- v37 outcome: usable visible evaluation, but lower score density or lower throughput than fallback.

This means the right fix is not another CSV/wrapper/log-printing change. It also means local measured-dense score-rate profiles are insufficient as public-score predictors.

Do not patch this by increasing the dense cap, changing constants, or adding another validator without a fresh hypothesis. That would repeat the same unidentifiable replay-cost mistake.

### 6. How does this compare to current competition state?

Fresh leaderboard command:

```text
comp/.venv/bin/kaggle competitions leaderboard -c ai-agent-security-multi-step-tool-attacks -s | head -n 15
```

returned a visible frontier of `112.865`, `112.165`, `110.250`, `110.130`, `109.485`, `109.410`, `109.120`, and multiple other scores above `107`.

Therefore, the competition is no longer just a high-80s single-post throughput problem. Scores above `100` exist, but this measured dense replacement is not the route that demonstrated them in our repository.

### 7. Does this solve the original problem?

No.

The current retained competition floor remains v35 at `86.670`. The current measured-density hypothesis is refuted. The repository has not yet produced a valid target-owned above-ceiling mechanism.

## Ledger summary

Verified compact ledger extraction:

```text
public_score_rows=6
lb-stagea-fixed1950 87.750 medium NA NA preregistered
lb-stageb-sm2call-rc500 81.225 medium 65.320 partial discard
lb-stageb-sm2call-rc650 84.916 low NA disconfirm discard
lb-public-control-validation-fill-gpu 88.5-89.2 medium 86.670 partial keep
lb-stageb-four-endpoint-rc320 105.600 low NA disconfirm crash
lb-stageb-measured-density-fill 100.000 low 84.735 disconfirm discard
best_kept_public_score=86.670
latest_v37=84.735 delta_vs_best=-1.935
research_iterations_spent=10 limit=10
last_metric_outcomes=[(8, 'single-message-multi-tool-event-density', 'refuted'), (9, 'exact-within-message-endpoint-density-admission', 'refuted'), (10, 'measured-density-validation-fill-admission', 'refuted')]
```

## Search diagnosis

Cycle 3 has one productive metric iteration:

- iteration 7, `candidate-count-and-probe-overhead`: improved, producing v35 score `86.670`.

The subsequent above-ceiling Stage B attempts all failed:

- iteration 8, `single-message-multi-tool-event-density`: refuted/discarded by visible regression.
- iteration 9, `exact-within-message-endpoint-density-admission`: refuted/crashed by blank public/private score.
- iteration 10, `measured-density-validation-fill-admission`: refuted/discarded by visible regression.

The last two metric iterations varied different dimensions, so this is not a same-dimension retry-loop violation. It is still a practical diminishing-returns signal: the repository has exhausted the authorized 10/10 research iterations and the last three above-ceiling attempts did not improve the retained floor.

## Figure decision

No new figure is generated.

Reason: only one retained `public_score` row exists (`lb-public-control-validation-fill-gpu` at `86.670`). Crash, discard, invalid, and preregistered rows must not enter ranking figures.

## Budget and path decision

Research budget is exhausted:

```text
research_iterations_spent=10 limit=10
```

No new Phase 2/3/4 research iteration should begin without explicit additional research-iteration budget. No Kaggle submission should be made from the refuted v37 branch.

Recommended next path:

1. Freeze v35 as the retained live fallback floor.
2. Close measured dense replacement as refuted.
3. If the goal is still the competition, start only one separately authorized fresh dimension with a sharp prediction against v35 and the current 107-113 leaderboard frontier.
4. If no additional iteration is authorized, conclude the current research cycle with an internal report: v35 floor recovered, Stage B dense mechanisms refuted so far, above-ceiling mechanism still unsolved.

## State update requirements

- Mark T126 done.
- Record gate `5_cycle3_iter10`.
- Keep `results.tsv` row `lb-stageb-measured-density-fill` as `disconfirm/discard`.
- Keep search-log iteration 10 as `refuted`.
- Do not update `best_state`.
- Do not submit another Kaggle version from this branch.
