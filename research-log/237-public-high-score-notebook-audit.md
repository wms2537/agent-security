# Public high-score notebook audit and control-restoration decision

Date: 2026-08-01

## Status

`v34` ref `55153594` completed with blank public/private score. The kernel commit-run artifact had already passed placeholder `submission.csv` schema checks and embedded the intended `return_count: int = 650` guarded two-call source. Therefore this result is treated as a hidden rerun/runtime/replay-boundary failure, not as a local CSV/header problem.

## Chrome and CLI evidence

The audit used Chrome/headless page captures plus Kaggle CLI notebook pulls in `/tmp/kaggle-public-audit-W8yCU6`.

Observed public notebook scores from Chrome page captures:

| Notebook | Captured public score | Runtime metadata |
| --- | ---: | --- |
| `foysalemonshanto/ai-agent-security-v12` | 89.190 | GPU/T4 family |
| `nctuan/jed-v25` | 89.145 | GPU/T4 family |
| `dimong4/ai-agent-security` | 89.100 | GPU/T4 family |
| `canqiang/aiagsec-ea-b-0721` | 88.560 | 18s, GPU T4 x2 |
| `tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery?scriptVersionId=336810494` | 88.515 | 27s, GPU T4 x2 |
| `pilkwang/ai-agent-v3-1-2-single-post-exfiltration?scriptVersionId=337366526` | 84.555 | GPU/T4 family |

Pulled notebook source and metadata show the public high-score family is not using the fixed-count/no-validation path. The common single-post control uses:

- one user message per returned candidate;
- one intended `http.post`;
- literal `SECRET_MARKER` payload;
- unique `.co` destination labels;
- live generation-side validation and keep-only-if-fired fill;
- replay-safe accumulated cost cap;
- small latency-based routing between the verbose imperative template and a Harmony/channel-shaped frame;
- GPU/T4 metadata.

## Decision

Retire the active rc650 guarded two-call path for now and restore a public-control validation-fill single-post kernel as the next control floor.

This does not claim a proprietary mechanism. It is a required floor-recovery step: we need a stable high-80s control before testing any above-90 density mechanism.

## Prediction before target run

If the public-control family transfers to our notebook runner and GPU/T4 metadata is honored, the expected public score is roughly `88.5-89.2`.

Decision gates:

- `<81.225`: regression; revert to the incumbent/floor branch and inspect runner differences.
- blank public/private score: hidden rerun/runtime/replay-boundary failure; do not submit another count/density variant until the public-control runner contract is isolated.
- `88-90`: freeze this as the restored single-post floor, then restart above-ceiling work with exact one-factor density experiments.
- `>90`: unexpected; inspect whether the validation-fill kernel created multi-event or scorer-cell effects before expanding.

## Implementation notes

The active `experiments/attack.py` now implements the public-control mechanism concisely:

- default `REPLAY_SAFE_FRAC=0.97`;
- `SPLIT_BY_LATENCY=True`;
- `SPLIT_CLASSIFY_N=8`;
- `SPLIT_THRESHOLD_S=12.0`;
- `HARD_N_CAP=2000`;
- `FALLBACK_N=300`;
- no two-call, no fixed `return_count`, no SCOC, no multi-message branch.

The Kaggle kernel metadata is changed from CPU to `NvidiaTeslaT4`.

## Local verification before remote mutation

Commands and outcomes:

- `python -m py_compile experiments/attack.py submission/build_notebook.py` passed.
- `jq empty state.json` passed.
- `awk` TSV-width checks passed for `results.tsv` and `competition/leaderboard_experiments.tsv`.
- no-env contract passed: `none_env_contract=PASS fallback_n=300 forced=5`.
- local SDK mechanics passed: `sdk_live_fill_smoke=PASS compliant=5 harmony=5`.
- notebook rebuild passed: `attack.py parses OK`.
- notebook contract passed for all three generated notebook copies.
- kernel metadata passed: `kernel_metadata=PASS True NvidiaTeslaT4`.

Source hashes after implementation:

```text
experiments/attack.py                         1e18beda6589f43dbbd2bcc500a876aeb6cef272579894c828bd31289a7aa87e
submission/kernel/kaggle_notebook.ipynb       acd34876203b770c251b55c699c1a6d5bc35d604fd26aaf35938a15a0406588e
submission/kernel/kernel-metadata.json        6d16226f6623c00b598e51b40ce454d386eb67e8dfd0930f94b32349d03d6426
```
