# Stage A Single-Post Throughput Preregistration

**Date:** 2026-07-26 · **Phase:** 5→2 · **Cycle:** 3 · **Iteration:** 7 · **Status:** in-progress

## Context

The DBER branch ended with `research-log/221-dber-cost-identifiability-and-retirement.md`: attack-side generation timing cannot identify hidden fresh-replay lifecycle cost. The user then supplied a repository audit diagnosing the active failure mode as under-optimised single-post throughput plus over-research of unidentifiable variables.

The audit's three corrections are adopted as the new active competition path:

1. Stop verifying every fill candidate.
2. Stop deriving replay capacity from generation-side timing.
3. Stop bundled synthetic experiments; use one-factor leaderboard measurements.

## Content

The active attack has been replaced with a minimal fixed-count single-post kernel:

- three arms: `plain`, `bare`, `harmony`;
- one uniform probe per arm;
- at most one confirmation probe under true ambiguity;
- no multi-message branch;
- no SCOC branch;
- no per-candidate fill verification;
- no replay-time sizing from observed generation latency;
- deterministic unique destinations;
- fixed `return_count=1950`.

The first target-measured hypothesis is:

> If the previous `81.225` artifact was losing effective findings to over-probing, fill verification and false replay-cost precision, then a minimal three-arm fixed-count single-post kernel at `N=1950` should move the public score toward the all-firing expectation of `87.750` without requiring a new security mechanism.

Prediction row:

- run id: `lb-stagea-fixed1950`
- metric: `public_score`
- predicted value: `87.750`
- direction: beat incumbent
- confidence: medium
- disconfirm: score below `81.225` or timeout/failure
- partial: `81.225 <= score < 86.000`
- confirm: `86.000 <= score <= 90.000`

The current live leaderboard page from the Kaggle CLI has leader `111.795`, so Stage A is not a winning architecture by itself. Its role is restoring the single-post control before the Stage B density test.

## Gate Check

- Incumbent tag: `git tag --list 'lb-81.225-ref-54923079'` returns `lb-81.225-ref-54923079`.
- Live submissions: `comp/.venv/bin/kaggle competitions submissions -c ai-agent-security-multi-step-tool-attacks` returns refs `54923079/54922298/54920038` at `81.225/79.920/81.090`.
- Live frontier: `comp/.venv/bin/kaggle competitions leaderboard -c ai-agent-security-multi-step-tool-attacks -s` returns leader `111.795`.
- Build: `python submission/build_notebook.py` returns `attack.py parses OK`.
- Syntax: `python -m py_compile experiments/attack.py submission/build_notebook.py` exits `0`.
- Removed-branch check: `rg -n "enable_multi_message|enable_scoc|VERIFIED FILL|replay_safe|replay_budget_s|multi_message|scoc|trial_multi|trial_scoc|probe_reps|probe_time_cap_s|min_fire_rate|cost_inflation" experiments/attack.py` returns no matches.
- Smoke: `PYTHONPATH=comp/sdk python - <<'PY' ...` returns `smoke_count 5`.
- Fake env: `PYTHONPATH=comp/sdk python - <<'PY' ...` returns `fake_env_count 1950`, `unique_domains 1950`, `probe_count 4`, `selected_arm bare`, `single_message_candidates True`.

## Problem alignment

This directly serves the core question by changing the controlled policy variable that Kaggle exposes, returned single-post throughput, instead of fitting unobservable replay slack.

## Decision

Proceed with Stage A fixed-count single-post as the next competition experiment. Do not claim this is above-ceiling innovation; it is a control-recovery experiment.

## Next Steps

1. Commit the Stage A kernel and ledgers.
2. Push `main` and the incumbent tag.
3. Use a Kaggle commit run as a notebook execution check.
4. Submit only if the committed confidence checklist passes.
