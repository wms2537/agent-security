# T080 — SCOC-32 Phase-3 recovery, live-score reconciliation, and mechanism decision

**Date:** 2026-07-26 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 5/5 · **Status:** completed

## Context

The continuation resumed with a coherent but uncommitted SCOC-32 worktree: tasks T065–T079, Phase-0/1 contracts, mechanism and holdout scripts, prediction-ledger rows, attack-engine changes, and rebuilt Kaggle notebooks were present, while `HEAD` remained at the first SCOC review dispatch. This task recovers that evidence without erasing history, checks the now-completed Kaggle submissions, and applies the frozen SCOC mechanism gate before any new submission.

## Recovered artifact checks

- `comp/.venv/bin/python -m py_compile experiments/attack.py experiments/mock_agents.py experiments/multi_message_eval.py experiments/scoc32_mechanism_harness.py experiments/scoc32_holdout_matrix.py` exited `0`.
- `comp/.venv/bin/python -m json.tool` parsed `state.json` and both SCOC contract JSON files.
- `python submission/build_notebook.py` wrote both notebook copies at `36,355` bytes; `cmp` returned `notebook_pair_cmp_exit=0`.
- The embedded notebook attack differs from `experiments/attack.py` only by one terminal blank line.
- `PYTHONPATH=/home/soh/agent-security/comp/sdk comp/.venv/bin/python experiments/multi_message_eval.py` ended with `PASS: adaptive routing, multi raw=390, fallback raw=54`.
- `results.tsv` has `148` data rows, `11` fields, `0` malformed rows, and `0` duplicate `(run_id, metric)` pairs.
- All sixteen numbered SCOC notes `189` through `204` are present.

Two accidental verification copies of the full 36-case holdout matrix continued running after their yielded wrappers returned. They were not preregistered experiments, produced no accepted registry artifact, and their exact PIDs were terminated. Existing run artifacts remain unchanged.

## Live Kaggle evidence

Read-only command:

`comp/.venv/bin/kaggle competitions submissions -c ai-agent-security-multi-step-tool-attacks --format csv --page-size 20`

returned:

| Ref | Description | Status | Public score |
|---:|---|---|---:|
| 54923079 | SCOC32 chain exploratory run 5 CPU | COMPLETE | **81.225** |
| 54922298 | SCOC32 chain exploratory run 3 | COMPLETE | 79.920 |
| 54920038 | SCOC32 chain exploratory run 2026-07-23 | COMPLETE | 81.090 |
| 54808132 | prior verified-fill incumbent | COMPLETE | 69.570 |

The best live score is therefore `81.225`, a `16.752911%` relative improvement over `69.570`. This is a useful complete-system result, but the three submissions bundle selector, routing, accounting, and SCOC-path changes and expose no episode-level component attribution. `kaggle competitions episodes` returned `No episodes found` for all three references.

No Kaggle push or submission was made in T080.

## Frozen SCOC mechanism gate

The Phase-0 preregistration requires:

`CHAIN_SCOC / CHAIN_FULL raw_per_sec >= 1.25`

at fixed chain length and coverage at least `0.95`.

Direct extraction from the preserved m=32 mechanism tables gives:

| Run | CHAIN_FULL raw/s | CHAIN_SCOC raw/s | Ratio | SCOC coverage |
|---|---:|---:|---:|---:|
| run03 | 13,224.396069 | 14,363.784627 | **1.086158079** | 1.0 |
| run04 | 13,158.699273 | 13,475.494739 | **1.024074983** | 1.0 |

Both independent runs pass coverage but miss the preregistered `1.25` mechanism threshold. In run03, `CHAIN_GENERIC` also slightly exceeds SCOC (`14,364.666321` versus `14,363.784627`), directly triggering the frozen generic-compression retraction condition. The paired end-to-end local evaluation is likewise flat: SCOC off and on both score `23.28`.

The narrative in report 196 contains a different run04 timing tuple than the currently preserved ignored artifact. That provenance mismatch is an additional reason not to use the exact timing magnitude as confirmatory evidence. It does not change the gate verdict: both preserved tables remain far below `1.25`, and the paired end-to-end result remains flat.

The unlogged run27/run28 scaling artifacts and their ledger rows lack a command-first provenance log. They stay exploratory history and are excluded from all mechanism, ranking, and confidence claims.

## Prediction vs. reality

**Prediction:** one exact successful anchor plus destination-only operands would preserve at least `0.95` exact-chain coverage and improve fixed-length raw/s by at least `1.25x` over full repetition, with a distinct advantage over generic shorthand.

**Reality:** coverage confirmed, but the efficiency and distinctiveness predictions were refuted. The best observed SCOC/full ratios were only `1.086` and `1.024`, and generic shorthand matched or slightly beat SCOC in one run.

The leaderboard bundle improved, but it cannot rescue the failed component claim because the scored artifact changed multiple non-contributing mechanisms and no component-fixed live ablation exists.

## Decision

SCOC-32 is **REFUTED at Phase 3** as a proprietary mechanism contribution. It is not eligible for another confidence-gated submission or for contribution credit.

The live complete-system incumbent is updated to `81.225` with submission reference `54923079`. That score remains tuning/public-leaderboard evidence, not private/final transfer.

Research-iteration budget is exhausted at `5/5`, so no Phase-2 replacement hypothesis or new competition experiment may be started without an explicit user budget extension. The next legal task is Phase-5 analysis/conclusion of the current cycle, including the live-score bundle as an unattributed system result and SCOC as a refuted component.

## Problem alignment

This decision advances the competition objective by retaining the verified `81.225` system improvement while preventing a failed, non-distinct mechanism from consuming another submission or being misrepresented as the source of that gain.

## Machine-readable close

```text
t080_scoc32_recovery=PASS logs_189_204=16 results_rows=148 malformed=0 duplicate_pairs=0 notebook_pair=identical routing=PASS live_best_ref=54923079 live_best=81.225 prior=69.570 relative_gain_percent=16.752911 run03_scoc_full_ratio=1.086158079 run04_scoc_full_ratio=1.024074983 required_ratio=1.25 coverage=1.0 mechanism=REFUTED submission=false next_phase=5 next_task=T081 research_budget=5/5
```
