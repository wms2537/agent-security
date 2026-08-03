# Phase 3 result — Burst-2 Validation Fill mechanics

Date: 2026-08-03

## Objective

Prove local mechanics for the reviewed K=2-only Burst-2 Validation Fill branch before any Kaggle push.

## Commands

```text
set -e
comp/.venv/bin/python -m py_compile experiments/attack.py experiments/poc/burst2_validation_fill_check.py submission/build_notebook.py
PYTHONPATH=comp/sdk:experiments comp/.venv/bin/python experiments/poc/burst2_validation_fill_check.py > experiments/poc/burst2_validation_fill_check.log 2>&1
comp/.venv/bin/python submission/build_notebook.py
rg -n "SLOW_MULTIPOST|MEASURED_DENSE|DENSE_ENABLED|_dense_msg|_measured_dense|Perform exactly 4" experiments/attack.py ai-agent-security-attack.ipynb submission/kaggle_notebook.ipynb submission/kernel/kaggle_notebook.ipynb && exit 1 || true
grep "^[a-z_].*:" experiments/poc/burst2_validation_fill_check.log
```

## Output

```text
wrote /home/soh/agent-security/ai-agent-security-attack.ipynb (17701 bytes)
wrote /home/soh/agent-security/submission/kaggle_notebook.ipynb (17701 bytes)
wrote /home/soh/agent-security/submission/kernel/kaggle_notebook.ipynb (17701 bytes)
attack.py parses OK
bundle_k1_byte_equivalent: 1
bundle_k2_url_count: 2
bundle_k2_post_mentions: 2
bundle_k2_empty_messages: 0
bundle_k2_no_dense4_wording: 1
none_k1_count: 3
none_k1_max_urls: 1
none_k1_max_posts: 1
none_k2_count: 3
none_k2_max_urls: 2
none_k2_max_posts: 2
fake_live_k2_count: 5
fake_live_k2_env_calls: 6
fake_live_k2_max_urls: 2
fake_live_k2_max_posts: 2
fake_live_k2_event_count: 2
partial_fake_k2_count: 5
has_slow_multipost_marker: 0
has_measured_dense_marker: 0
max_message_len: 205
runtime_s: 0.000352
burst2_gate_pass: 1
```

## Interpretation

Phase 3 local mechanics pass.

The first implementation attempt failed because the K=2 formatter contained two URLs but only one literal `http.post` mention. That was corrected before the passing gate by moving `http.post` into each per-post instruction and removing it from the shared header.

The passing artifact satisfies the reviewed v2 hypothesis:

- K=1 is byte-equivalent to the restored v35 `_msg`.
- K=2 emits exactly two URLs and exactly two `http.post` mentions.
- K=2 has no K=4/dense/slow-row multipost markers.
- Fake-live two-event trace is counted as two events.
- Partial one-event K=2 traces are retained, matching the hypothesis risk model.
- Notebooks were rebuilt and parse.

## Scope

This is local mechanics only. It does not prove target-model second-event prevalence, replay safety beyond the inherited v35 ledger, public score, private transfer, or final leaderboard rank.

## Gate check

- Compile: PASS.
- Local mechanics: PASS.
- Notebook rebuild: PASS.
- Dense/slow-multipost marker absence: PASS.
- Proceed to Phase 4 code review and Kaggle commit-run confidence gate: YES.
