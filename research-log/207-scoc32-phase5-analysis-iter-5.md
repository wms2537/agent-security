# T081 — SCOC-32 Phase-5 analysis and path recommendation

**Date:** 2026-07-26 · **Phase:** 5 · **Cycle:** 3 · **Iteration:** 5/5 · **Status:** recommendation completed, path approval pending

## Context

T080 recovered the SCOC-32 worktree, reconciled three completed Kaggle submissions, and applied the frozen Phase-3 mechanism gate. The best official public score is now `81.225` at ref `54923079`, a `16.752911%` gain over the prior `69.570` incumbent. The active mechanism hypothesis was nevertheless refuted: the two preserved m=32 `CHAIN_SCOC / CHAIN_FULL` raw-per-second ratios were `1.086158079` and `1.024074983`, below the frozen `1.25` gate.

This Phase-5 task analyzes that split result: retain the live bundle as useful public tuning evidence, but decide whether SCOC-32 remains a valid contribution or competition direction.

## Exclusions

The following are excluded from rankings, statistics and submission confidence:

- all `status=exploratory`, `status=discard`, `status=crash`, `status=preregistered`, `status=mechanics-only`, and `status=superseded` ledger rows;
- cross-cycle ORF public-synthetic `keep` rows, because they are not SCOC evidence;
- unlogged run27/run28 scaling artifacts, because they lack command-first provenance;
- report 196's run04 timing tuple, because it does not match the currently preserved ignored artifact;
- the official `81.225` public score as SCOC attribution evidence, because it bundles multiple changes and has no component-fixed live ablation.

## Statistical declaration

```text
independent_unit: one preserved mechanism-harness rerun for mechanism ratio; one official public leaderboard submission for live bundle
n_units: mechanism ratio n=2 reruns; live bundle n=1 public submission per ref
comparison_family: 2 descriptive comparisons (mechanism ratio vs 1.25 gate; bundled public score vs 69.570 incumbent)
correction: none - descriptive gate checks, no p-value claim
```

Orchestrator recomputation from `artifacts/scoc32/run03/scoc32-mechanism-harness.tsv` and `artifacts/scoc32/run04/scoc32-mechanism-harness.tsv`:

```text
headline_recompute=PASS run03=1.086158078744 run04=1.024074983325 mean=1.055116531034 sd=0.043899377768 gate=1.25 both_fail=True
```

## Results summary

The analysis tables are in `research-log/206-scoc32-analysis-iter-5-tables.md`. They record:

- `results.tsv` row count: `148` data rows, `149` total lines;
- status counts: `keep=27`, `exploratory=95`, `preregistered=11`, `discard=7`, `crash=6`, `mechanics-only=1`, `superseded=1`;
- signal counts: `confirm=105`, `partial=20`, `null=18`, `disconfirm=5`;
- confidence calibration: high `23/30`, medium `12/22`, low `70/96`.

Figures:

- `paper/figures/scoc32_mechanism_comparison.svg`
- `paper/figures/scoc32_mechanism_comparison.png`
- `paper/figures/scoc32_mechanism_comparison.source.csv`
- `paper/figures/scoc32_public_leaderboard_bundle.svg`
- `paper/figures/scoc32_public_leaderboard_bundle.png`
- `paper/figures/scoc32_public_leaderboard_bundle.source.csv`

Figure QA:

```text
figure_qa=PASS paper/figures/scoc32_mechanism_comparison
figure_qa=PASS paper/figures/scoc32_public_leaderboard_bundle
```

## Seven analysis questions

### 1. Did it work?

No, not as a SCOC mechanism. The primary comparison required `CHAIN_SCOC / CHAIN_FULL >= 1.25` at m=32 with coverage at least `0.95`. Coverage was `1.0` in both preserved reruns, but the ratios were only `1.086158079` and `1.024074983`. The pre-specified gate fails mechanically.

The complete bundled system did improve the official public score to `81.225`, but that is not the primary SCOC mechanism comparison.

### 2. Why did it work or not?

The Phase-2 intuition was half right: conversation history can carry enough retained syntax and action state to keep coverage intact. The missing part was material efficiency. Destination-only continuation did not reduce the replay path enough relative to full repetition, and its measured advantage was close to generic message shortening rather than anchor-conditioned state transfer.

### 3. What contributed most?

For SCOC specifically, no component earned contribution credit. Coverage came from retained conversation/tool state, but contribution credit required efficiency and distinctiveness. The run03 `CHAIN_GENERIC >= CHAIN_SCOC` result directly triggers the frozen generic-compression retraction. The local paired SCOC-off/on comparison was also flat at `23.28`.

For the `81.225` live bundle, the contributing component is unknown. Selector, routing, accounting, candidate count and SCOC-path changes moved together; there is no official component-fixed ablation or episode telemetry.

### 4. How robust is it, and where does it fail?

The failure is robust across the two preserved mechanism reruns: both pass coverage and both miss `1.25`. The failure case is concrete: at m=32, `CHAIN_SCOC` has enough semantic coverage but not enough raw-per-second lift. It also fails the novelty/distinctiveness condition once a generic shorthand can match or beat it.

The live bundle robustness is weaker: three completed SCOC-era submissions scored `81.225`, `81.090`, and `79.920`, which is encouraging for the whole system but not a controlled component result.

### 5. What was surprising?

The surprise is that coverage was not the hard part. The prior risk model overweighted exact-chain retention failure and underweighted generic compression as a rival explanation. The prediction ledger now shows many low-confidence exploratory rows confirming flat local scores, plus partial rows where more returned findings changed local normalized score by candidate count rather than by SCOC mechanism quality. Those rows are useful debugging history, not confirmatory evidence.

### 6. How does it compare to current literature and baselines?

Freshness check on 2026-07-26 found no exact public analogue of "success-conditioned operand chains" or "destination-only operands" as a named mechanism. Adjacent 2026 work has moved strongly toward stateful, multi-turn and harness-level agent security:

- `Towards Long-Horizon Agents: A Survey`, posted 2026-07-17 and not peer reviewed, frames long-horizon agency as a co-evolution of externalized harness engineering and internalized model optimization, and explicitly flags attribution difficulty when model, harness, data and evaluation changes are entangled: <https://www.preprints.org/manuscript/202607.1328>
- `Adaptive Adversaries` introduces a 21-scenario adaptive multi-round benchmark where an autonomous attacker observes prior defender responses and pivots across rounds: <https://arxiv.org/html/2607.18063v1>
- `Beyond the Prompt` studies function-calling jailbreaks via simulated moderation traces and emphasizes accumulated execution history as an attack resource: <https://arxiv.org/html/2607.00481v1>
- `Toward Secure LLM Agents` synthesizes agent security around information flow, delegated authority and persistent state, and notes that long-horizon/stateful deployment risks remain underrepresented in benchmarks: <https://arxiv.org/html/2606.10749v1>
- Anthropic's Fable 5 post describes reported Fable 5 bypasses as minor or narrow rather than universal, and proposes capability gain, breadth, weaponization and discoverability as severity criteria: <https://www.anthropic.com/news/redeploying-fable-5>

This literature supports the broader direction of harness/state/orchestration research. It does not support continuing SCOC without a measured mechanism advantage.

Against competition baselines, `81.225` beats our prior `69.570` incumbent, but it remains below the recorded `110.235` leader from the Cycle-3 audit and is not submission-confidence evidence for a new SCOC run.

### 7. Does it solve the problem?

Partly, but not enough. The `81.225` bundle advances the competition objective by raising the public tuning incumbent. SCOC itself does not solve the core problem: it fails to identify a source-compliant candidate-generation/allocation policy with an attributable mechanism and confidence-gated path above the leaderboard frontier.

The problem proxy caveat applies: public score is a tuning signal, not final/private transfer, and mechanism claims require component isolation.

## Freshness check

The exact-claim search found no current primary source using the SCOC framing. The adjacent literature and Fable 5 official materials shift the next plausible research direction away from operand-chain compression and toward orchestration-level state, authority, harness verification, and adaptive multi-round attack/evaluation loops.

No freshness result invalidates the competition objective. It does invalidate a paper-style novelty claim that treats stateful multi-turn attacks or harness-state attribution as broadly new.

## Search diagnosis

Kind audit: SCOC-32 is correctly `kind=metric`, because it targeted the primary competition mechanism and produced leaderboard submissions. Its `search_log` outcome is correctly `refuted`.

Cycle-3 metric entries:

| Iteration | Direction | Varies | Outcome |
|---:|---|---|---|
| 1 | progressive-online-replay-frontier | candidate-message-multiplicity-and-cost-aware-online-allocation | inconclusive |
| 1 | nested-prefix-gate-8 | candidate-boundary-density-via-nested-prefix-gating | inconclusive |
| 2 | monotone-prefix-controller-24 | monotone-24-to-8-prefix-control | refuted |
| 3 | prefix-risk-absorbing-controller-24 | complete-cell-resource-risk-admission-and-absorbing-stop | inconclusive |
| 4 | success-conditioned-operand-chains-32 | conversation-resident-invariant-factorization-and-self-success-continuation | refuted |

Mechanical verdict: stalled for competition mechanism search. The most recent metric work did not produce an attributable `best_state` mechanism improvement, and research iteration budget is exhausted. The same-dimension escalation trigger does not fire because the last two metric entries vary different dimensions, but the budget rule is decisive.

Null-signal count is `18` ledger rows. Many are historical preregistration/crash artifacts, but the process lesson is still live: avoid runs that cannot distinguish mechanism attribution from bundled score movement.

## Budget check

```text
research_iterations: 5/5 exhausted
hypothesis_review_rounds: 12/32 used
paper_review_rounds: 0/2 used
```

SciAgent budget rule: `research_iterations.spent >= limit` means conclude. Review budget cannot substitute for research-iteration budget; another theory review would not authorize a new Phase-2 hypothesis or Kaggle experiment.

The Path-C locked-test step is not executed here. In this competition setting, the private/final test is not independently callable, and a new official submission would be a Kaggle action requiring the confidence gate to pass. The confidence gate fails because the active mechanism is refuted and the live bundle is unattributed. Running a submission as a "locked test" would violate the recorded submit-only-when-confident constraint.

## Path recommendation

Recommended path: **Path C, conclude this SCOC-32 hypothesis/cycle segment as an internal competition report; do not submit; do not proceed to an academic paper on SCOC.**

No-paper steelman: the strongest positive number, `81.225`, is a bundled leaderboard result without component attribution or private/final transfer. The mechanism claim is refuted, and the broader stateful-agent/harness literature is too active to support a broad novelty story from this evidence. A paper would either overclaim the live score or publish an underpowered negative mechanism result.

Negative-result paper option: not recommended. The negative result is valuable internally, but it has only two preserved mechanism reruns, competition-specific artifacts, and no clean external benchmark. It is a good engineering lesson, not a publishable negative result.

Internal technical report option: recommended. The report should preserve the `81.225` bundle as the current public best, retire SCOC contribution credit, and carry forward one design rule: no future leaderboard gain receives mechanism credit without a component-fixed ablation or a mechanism profile that isolates the bottleneck before submission.

If the user wants more competition research, the next move must be an explicit research-iteration budget extension or a new cycle. The fresh dimension should not be operand-chain compression; the evidence points toward orchestration/harness-state policy, official-output attribution, replay-tail risk modeling, or candidate-allocation under live public-score feedback.

## Gate Check

- Seven analysis questions answered explicitly: `rg -n '^### [1-7]\\.' research-log/207-scoc32-phase5-analysis-iter-5.md` finds all seven headings.
- Tables and figures verified: `figure_qa=PASS paper/figures/scoc32_mechanism_comparison` and `figure_qa=PASS paper/figures/scoc32_public_leaderboard_bundle`.
- Statistical declaration block present: see above; descriptive gate check only, no p-value claim.
- Headline claim recomputed: `headline_recompute=PASS run03=1.086158078744 run04=1.024074983325 mean=1.055116531034 sd=0.043899377768 gate=1.25 both_fail=True`.
- Freshness check done: five primary/official sources listed above, exact SCOC analogue not found.
- Search diagnosis recorded: kind audit, null count, calibration and per-dimension table included above.
- Budget check performed: research iterations `5/5` exhausted; review budget cannot authorize a new research iteration.
- Path recommendation made: Path C internal technical report/no submission/no SCOC paper.
- User approval: pending. This log recommends the path; it does not close the Phase-5 user checkpoint.

## Problem alignment

This analysis serves the competition objective by keeping the verified `81.225` public-score gain while preventing a failed mechanism from consuming more submissions, research iterations, or paper effort.

## Decision

T081 is complete as an analysis and recommendation task. The Phase-5 path gate remains open pending user approval or explicit new research-iteration budget.

## Next Steps

1. If the user approves Path C, write the internal SCOC-32 competition report and cycle retrospective.
2. If the user explicitly extends research-iteration budget, open a new Phase-2 task on a fresh dimension, not operand-chain compression.

## Machine-readable close

```text
t081_scoc32_phase5_analysis=PASS tables=research-log/206-scoc32-analysis-iter-5-tables.md results_rows=148 figure_qa=2/2 run03_ratio=1.086158078744 run04_ratio=1.024074983325 mean_ratio=1.055116531034 required_ratio=1.25 mechanism=REFUTED live_best=81.225 live_gain_percent=16.752911 search_verdict=stalled research_budget=5/5 recommendation=path_c_internal_report submission=false user_path_approval=pending
```
