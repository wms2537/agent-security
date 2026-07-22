# Cycle-3 baseline linkage and T006 reproducibility audit

**Date:** 2026-07-22  
**Phase/task:** Phase 2 / T046 adverse-review resolution  
**Purpose:** repair two evidence defects identified in review round 1  
**Result:** target baseline linkage `PASS`; T006 timing-profile reproduction `FAIL`

No source file, Kaggle kernel, Kaggle submission, or competition state was mutated.
The Kaggle actions in this audit were authenticated reads only.

## 1. Exact target-linked baseline recovered

The round-1 reviewer correctly rejected causal attribution from other authors'
visible notebooks to those authors' scores. That limitation does not apply to the
repository's own conservative baseline after the following identity recovery.

Authenticated submission history returned:

```text
ref,fileName,date,description,status,publicScore,privateScore
54808132,submission.csv,2026-07-18 12:49:46.303000,,SubmissionStatus.COMPLETE,69.570,
54799835,submission.csv,2026-07-18 05:37:08.013000,v1 attack: online probe/select + void-safe replay-budget fill; multi-post EXFIL + 22% CONFUSED_DEPUTY private reserve,SubmissionStatus.COMPLETE,36.705,
```

The current Whyme kernel output lists `attack.py` at 12:47 UTC on 2026-07-18,
about two minutes before submission `54808132`. Its SHA-256 is
`74998d1c518da818276b27ea38bcdc042215e6bc5db129a162b3083c95349e59`.
Removing the one wrapper-added leading and trailing blank line makes it byte-equal
to `git show 8c44eb4:experiments/attack.py`:

```text
kernel_artifact_match=PASS commit=8c44eb4 transformation=remove_one_leading_and_trailing_blank_line
```

Commit `8c44eb4` uses `replay_safe=0.90`, `cost_inflation=1.10`, the eight-template
single-message race, exact verified fill, and no sequential multi-message
candidate chain. This establishes a target-linked, non-void **69.570** baseline
for that exact artifact. It does not establish current target stationarity or any
benefit from a later multiplicity selector.

## 2. Reviewer-requested T006 reproduction

The T006 code paths are unchanged from their original experiment commit:

```text
git show f25fcd2:experiments/attack.py | sha256sum
8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d

experiments/attack.py
8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d

git show f25fcd2:experiments/multi_message_eval.py | sha256sum
fdce202f410f5b68469848953cba58442b4428a04ab1abf8e6d2e260af5d47e9

experiments/multi_message_eval.py
fdce202f410f5b68469848953cba58442b4428a04ab1abf8e6d2e260af5d47e9
```

Environment:

```text
command=/usr/bin/time -v comp/.venv/bin/python experiments/multi_message_eval.py
venv_python=3.14.3 (main, Feb 3 2026, 15:32:20) [GCC 12.3.0]
platform=Linux-6.11.0-29-generic-x86_64-with-glibc2.40
cpu=Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz
logical_cpus=12
seed=42
attack_sha256=8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d
eval_sha256=fdce202f410f5b68469848953cba58442b4428a04ab1abf8e6d2e260af5d47e9
mock_sha256=dc7c66bb5385e862fd7778f6d0a6326795442a0ec2ddad97f0c0c8a40f1807df
sdk_scorer_sha256=13a0969ea6c64b257c46d47490b4259ade3a4965f19d2d6c6fe0ed151f618d4f
sdk_ops_sha256=455a835e0a58abab79b24c986a937b99712e69ef83d6068fc68873e3c051fe74
elapsed_wall_s=4.38
max_rss_kb=79832
exit_status=1
```

Decisive raw output, preserved verbatim:

```text
per-turn-negative: structure=multi_message debug={'selected': 'plain', 'structure': 'multi_message', 'best_raw_per_s': 301.647, 'multi_raw_per_s': 339.524, 'multi_probe_messages': 4, 'multi_fill_messages': 8, 'multi_probe_events': [4, 4], 'multi_kept': 3, 'multi_fallback': False, 'unit_cost_s': 0.389, 'returned': 3, 'replay_cost_s': 1.1, 'safe_cap_s': 4.0, 'probes': {'plain': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.06}, 'bare': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.07}, 'bare_ok': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.06}, 'call_syntax': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.06}, 'inj_close': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.06}, 'inj_commentary': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.06}, 'inj_empty': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.07}, 'inj_done': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.07}}}
fixed-overhead-positive: structure=multi_message debug={'selected': 'inj_done', 'structure': 'multi_message', 'best_raw_per_s': 260.717, 'multi_raw_per_s': 850.195, 'multi_probe_messages': 4, 'multi_fill_messages': 8, 'multi_probe_events': [4, 4], 'multi_kept': 3, 'multi_fallback': False, 'unit_cost_s': 0.155, 'returned': 3, 'replay_cost_s': 0.2, 'safe_cap_s': 4.0, 'probes': {'plain': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.1}, 'bare': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.08}, 'bare_ok': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.09}, 'call_syntax': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.07}, 'inj_close': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.07}, 'inj_commentary': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.08}, 'inj_empty': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.08}, 'inj_done': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.07}}}
full-context-fallback: structure=single_post debug={'selected': 'bare_ok', 'structure': 'single_post', 'best_raw_per_s': 1249.084, 'multi_raw_per_s': 4142.617, 'multi_probe_messages': 4, 'multi_fill_messages': 8, 'multi_probe_events': [4, 4], 'multi_kept': 0, 'multi_fallback': True, 'unit_cost_s': 0.014, 'returned': 3, 'replay_cost_s': 0.1, 'safe_cap_s': 4.0, 'probes': {'plain': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.02}, 'bare': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.02}, 'bare_ok': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.01}, 'call_syntax': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.02}, 'inj_close': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.01}, 'inj_commentary': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.02}, 'inj_empty': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.01}, 'inj_done': {'fire_rate': 1.0, 'n': 1, 'raw': 18, 'med_lat': 0.02}}}
Traceback (most recent call last):
  File "/home/soh/agent-security/experiments/multi_message_eval.py", line 96, in <module>
    assert negative["structure"] == "single_post", negative
AssertionError: {'selected': 'plain', 'structure': 'multi_message', 'best_raw_per_s': 301.647, 'multi_raw_per_s': 339.524, 'multi_probe_messages': 4, 'multi_fill_messages': 8, 'multi_probe_events': [4, 4], 'multi_kept': 3, 'multi_fallback': False, 'unit_cost_s': 0.389, 'returned': 3, 'replay_cost_s': 1.1, 'safe_cap_s': 4.0, ...}
```

The unchanged negative control moved from the historical ratio `1.079` (below the
`1.10` route gate) to `339.524 / 301.647 = 1.1256` and selected multi-message.
The positive mock still showed a large observed ratio
`850.195 / 260.717 = 3.2609`, and the context-limited case still fell back, but the
script aborted before scorer assertions. The original T006 terminal stdout was not
committed in 2026-07-19 and cannot be reconstructed; this rerun is the first
immutable raw evidence for that exact code.

## 3. Scientific disposition

T006's exact `1.079` and `2.517` ratios are withdrawn as stable bottleneck
measurements. They remain historical exploratory observations only. The new run
supports the reviewer's selection-bias critique: one timing sample per template,
followed by selecting the fastest of eight, can move a near-threshold routing
decision across the `1.10` boundary under ordinary host jitter.

Before a superseding hypothesis can claim an engineering profile, a new exploratory
profile artifact must:

1. use deterministic virtual costs for allocator correctness and separately use
   real-SDK wall time only for mechanics;
2. use equal replication for every multiplicity arm;
3. isolate template selection as a fixed common control;
4. report every seed/run, not only the passing run;
5. solve total attainable raw under generation, replay, and candidate caps; and
6. set the external prediction relative to the exact target-linked `69.570`
   baseline, not an inferred public-author score.

No hypothesis v2 is frozen until that profile exists.
