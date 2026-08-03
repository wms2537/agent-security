# Targeted public-notebook audit — burst-2 evidence

Date: 2026-08-03

## Commands

Current public notebook metadata was refreshed with:

```text
comp/.venv/bin/kaggle kernels list --competition ai-agent-security-multi-step-tool-attacks --sort-by scoreDescending --page-size 50 --format csv
comp/.venv/bin/kaggle kernels list --competition ai-agent-security-multi-step-tool-attacks --sort-by dateRun --page-size 50 --format csv
```

The audit set was pulled with:

```text
comp/.venv/bin/kaggle kernels pull dimong4/ai-agent-security -p research-log/public-notebook-audit/dimong4 -m
comp/.venv/bin/kaggle kernels pull tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery -p research-log/public-notebook-audit/tetsutani-two-probe -m
comp/.venv/bin/kaggle kernels pull pilkwang/ai-agent-v3-1-2-single-post-exfiltration -p research-log/public-notebook-audit/pilkwang-single-post -m
comp/.venv/bin/kaggle kernels pull nctuan/jed-v25 -p research-log/public-notebook-audit/nctuan-v25 -m
comp/.venv/bin/kaggle kernels pull foysalemonshanto/ai-agent-security-v12 -p research-log/public-notebook-audit/foysal-v12 -m
```

The raw notebooks are third-party public artifacts and are used here only as audit inputs, not as committed solution code.

## Extracted facts

The five pulled notebooks all contain the expected code-competition output contract: a placeholder `Id,Score` CSV on commit and direct `JEDAttackInferenceServer().serve()` on rerun.

Compact extraction returned the following mechanism signals:

| Notebook | Key mechanism signals |
| --- | --- |
| `dimong4/ai-agent-security` | `BURST_K = 2`, `SLOW_MULTIPOST_N = 4`, public-control validation-fill constants `MARGIN_S=47`, `FILL_BUDGET_FRAC=0.95`, `REPLAY_SAFE_FRAC=0.97`, `HARD_N_CAP=2000`, `SPLIT_BY_LATENCY=True`, `SPLIT_CLASSIFY_N=8` |
| `pilkwang/ai-agent-v3-1-2-single-post-exfiltration` | Single-post fill stack: `BURST_K=1`, `SLOW_MULTIPOST_N=1`, same validation-fill/replay-safe constants |
| `foysalemonshanto/ai-agent-security-v12` | Same single-post fill stack as Pilkwang-style controls |
| `nctuan/jed-v25` | Same fill stack plus a verbose Harmony `FRAME_TEMPLATE` and `REPLAY_SAFE_FRAC=0.98` variant |
| `tetsutani/ai-agent-sec-adaptive-uniform-two-probe-recovery` | One-post uniform template race, `PROBE_REPS=2`, `REPLAY_SAFE=0.99`, reported lineage scores `88.515` and `89.055` in notebook markdown |

Fresh leaderboard head from report 265 remained above the single-post floor:

```text
112.865, 112.165, 110.250, 110.130, 109.485, ...
```

## Interpretation

The public ecosystem points to two separable tracks:

1. High-80s single-post throughput controls.
2. Above-100 candidate-internal post density.

Our failed v36/v37 branch was not the same as the strongest public signal:

- v36 used blind four-endpoint dense emission and blanked.
- v37 measured 93-96 four-endpoint candidates and visibly regressed.
- The public-audit above-ceiling signal uses a smaller `BURST_K=2` default, inside the validation-fill loop, not a four-endpoint measured prefix.

This is enough new evidence to test a small, controlled burst-2 branch without retrying the refuted four-endpoint branch.

## Candidate critique rubric

| Candidate | Most likely failure mode | Hardest implementation trap | Evidence check | Score |
| --- | --- | --- | --- | ---: |
| A. Burst-2 validation-fill control | Two-post messages slow replay enough that returned count falls, or only one post fires often enough to dilute the density gain | Preserving v35 fallback semantics while changing only candidate-internal post cardinality | Public audit: `dimong4` has `BURST_K=2`; v35 validates the fill loop; v33 showed two-call density can score but fixed count under-returned | `5 impact × 4 feasibility ÷ 2 complexity = 10.0` |
| B. Slow-row Harmony multipost only | Row classifier misroutes or slow-row multipost times out; exact slow model identity is hidden | Applying Harmony-only behavior without target model labels | Public audit: `SLOW_MULTIPOST_N=4`; but our K=4 dense attempts failed and model-specific logs are unavailable | `4 × 2 ÷ 4 = 2.0` |
| C. Two-probe uniform single-post recovery | Improves high-80s floor but cannot reach the current 107-113 frontier | It may consume submissions without addressing score density | Public audit: Tetsutani lineage reports `88.515`/`89.055`; still below above-100 leaders | `3 × 5 ÷ 2 = 7.5` |

## Selection

Select Candidate A: burst-2 validation-fill control.

Rejected:

- B is too close to the refuted K=4 failures without a model-label telemetry source.
- C is useful as a fallback control but does not target the above-100 requirement.

## Gate check

- Public notebook metadata refreshed: PASS.
- Audit set pulled: PASS.
- Mechanism constants extracted: PASS.
- Candidate critique rubric applied: PASS.
- Next hypothesis selected: burst-2 validation-fill control.
