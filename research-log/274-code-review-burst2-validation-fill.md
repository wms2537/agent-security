# Phase 4 code review — Burst-2 Validation Fill

Date: 2026-08-03

## Scope

Review active-source changes from restored v35 floor commit `b61684a` through current Burst-2 implementation.

Command:

```text
git diff b61684a..HEAD -- experiments/attack.py
```

## Review result

Overall: SOUND for Kaggle commit-run confidence.

## Findings

### 1. Single changed mechanism

PASS.

The active source adds only:

- `BUNDLE_TEMPLATE`
- `BUNDLE_POSTS = 2`
- `BUNDLE_POSTS_MAX = 2`
- `_bundle_msg(...)`
- routing of `_emit`, warmup, and fill messages through `_bundle_msg`
- disabling split-by-latency when `bundle_posts > 1`

No K=4 dense branch, measured dense branch, slow-row Harmony multipost, replay-cost multiplier change, or template-library expansion is present.

### 2. K=1 ablation preserved

PASS.

Local gate returned:

```text
bundle_k1_byte_equivalent: 1
none_k1_max_urls: 1
none_k1_max_posts: 1
```

### 3. K=2 serialization

PASS.

Local gate returned:

```text
bundle_k2_url_count: 2
bundle_k2_post_mentions: 2
bundle_k2_empty_messages: 0
bundle_k2_no_dense4_wording: 1
none_k2_max_urls: 2
none_k2_max_posts: 2
max_message_len: 205
```

### 4. Fake-live mechanics

PASS.

Local gate returned:

```text
fake_live_k2_count: 5
fake_live_k2_env_calls: 6
fake_live_k2_max_urls: 2
fake_live_k2_max_posts: 2
fake_live_k2_event_count: 2
partial_fake_k2_count: 5
burst2_gate_pass: 1
```

The branch retains candidates when at least one event fires and can count two events in a two-event trace, matching the reviewed hypothesis.

### 5. Excluded marker check

PASS.

The marker grep over source and notebooks found no prohibited markers:

```text
SLOW_MULTIPOST|MEASURED_DENSE|DENSE_ENABLED|_dense_msg|_measured_dense|Perform exactly 4
```

### 6. Notebook/source wrapper

PASS.

Compilation and rebuild passed:

```text
comp/.venv/bin/python -m py_compile experiments/attack.py experiments/poc/burst2_validation_fill_check.py submission/build_notebook.py
comp/.venv/bin/python submission/build_notebook.py
```

The rebuild returned:

```text
attack.py parses OK
```

## Remaining risks

- Target-model second-event prevalence is hidden.
- K=2 may cost enough replay time to reduce returned count.
- Public notebook metadata is only a mechanism prior, not outcome evidence.

These are target-evaluation risks, not local code defects. The next valid measurement is a Kaggle commit-run output/source/schema gate, followed by competition submission only if that gate is clean.

## Decision

Proceed to Kaggle commit-run measurement. Do not submit to the competition until downloaded output/schema/source checks pass.
