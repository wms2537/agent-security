# PORF profile recovery result — disconfirmed prediction, sharper mechanism

**Date:** 2026-07-22  
**Phase/task:** Phase 2 / T046 adverse-review resolution  
**Freeze commit:** `121993c`  
**Attempt:** `experiments/runs/porf-c3-profile-v2`  
**Envelope status:** `FAIL`  
**Artifact-integrity status:** `PASS`

No Kaggle kernel or submission was mutated. This was a public-SDK controlled-mock
profile, not a target-model run.

## Frozen prediction and result

The protocol predicted 5/5 exact deterministic profiles and 9/9 SDK decisions.
The one-use run returned:

```text
command=comp/.venv/bin/python -I experiments/porf_c3_profile_v2.py --config experiments/configs/porf-c3-profile-v2.json --attempt-dir experiments/runs/porf-c3-profile-v2
status=FAIL
deterministic_profiles_passed=5/5
sdk_decisions_passed=6/9
stability_fraction=0.666666666667
sample_rows=360
runtime_s=57.762814461
max_rss_gb=1.411659241
decision=per_turn_linear master=41 selected=24 expected_ok=false max_replay_gen_ratio=3.137901
decision=per_turn_linear master=42 selected=24 expected_ok=false max_replay_gen_ratio=3.070086
decision=per_turn_linear master=43 selected=24 expected_ok=false max_replay_gen_ratio=3.620353
decision=reset_heavy master=41 selected=24 expected_ok=true max_replay_gen_ratio=2.494685
decision=reset_heavy master=42 selected=24 expected_ok=true max_replay_gen_ratio=2.696213
decision=reset_heavy master=43 selected=24 expected_ok=true max_replay_gen_ratio=2.755875
decision=context_cliff master=41 selected=8 expected_ok=true max_replay_gen_ratio=5.151831
decision=context_cliff master=42 selected=8 expected_ok=true max_replay_gen_ratio=5.429977
decision=context_cliff master=43 selected=8 expected_ok=true max_replay_gen_ratio=5.543718
```

Bundle verification independently recomputed every artifact and binding hash:

```text
profile_bundle=PASS envelope_status=FAIL deterministic=5/5 sdk=6/9 stability=0.666666666667 rows=360
```

The failed expectation is not retried or relabeled. It remains a disconfirmation
of the claim that a per-action-linear target implies `m=1` once the complete
trusted replay path is included.

## Why the negative control selected 24

The frozen runner intentionally measured two different source-authentic scopes:

- generation reused one attack environment and called `reset()` per candidate;
- replay constructed a fresh SDK environment/agent, called `reset()`, and then
  replayed the candidate, matching `_replay_candidate_trace` and the gateway.

Even when the mock agent itself had no explicit fixed reset cost, fresh replay
construction added a fixed per-candidate cost. On the three per-turn masters:

| master | worst `m=1` generation / replay s | worst `m=24` generation / replay s | constrained raw `m=1` / `m=24` | selected |
|---:|---:|---:|---:|---:|
| 41 | 0.07475 / 0.12342 | 0.57742 / 0.65734 | 576 / 2,316 | 24 |
| 42 | 0.06429 / 0.14438 | 0.58114 / 0.64412 | 486 / 2,316 | 24 |
| 43 | 0.05184 / 0.13858 | 0.59198 / 0.64659 | 504 / 2,316 | 24 |

The result is stable across all three masters and does not depend on picking the
fastest of several templates: the profile fixed one plain template and used five
paired observations per arm. The new measured bottleneck is therefore
**candidate-boundary replay construction**, not merely model reset latency.

This is a scope mismatch between the live quantity visible to attack code
(`reset + interact` on an already-created environment) and the trusted evaluator
quantity that controls replay (`construct + reset + interact` for each candidate).
Packing multiple messages into one candidate amortizes the hidden fixed term.

## Why the frontier is still required

Always choosing the longest chain is not supported. In every context-cliff master,
`m=24` fired only through the first eight messages, failed the frozen 0.75
admissibility rule, and the joint selector chose `m=8`. Thus the same exact profile
artifact contains both sides of the decision:

- complete firing plus replay construction overhead favors `m=24`; and
- a context-compliance cliff makes `m=24` invalid and favors an interior `m=8`.

The deterministic counterexample also passed: raw/replay-second selected `m=4`,
but the exact generation/replay/candidate-cap objective selected `m=8`. This
directly verifies the round-1 reviewer's objection that rate alone is not the
competition objective.

## Scope and next decision

This run supports one component only: an exact multiplicity selector that accounts
for candidate-boundary replay construction and rejects context-cliff arms. It does
not establish the magnitude of construction overhead for remote gpt-oss/Gemma,
their multi-turn firing, private-guardrail transfer, or a leaderboard gain.

Hypothesis v2 may use the following evidence honestly:

1. target-linked baseline `69.570` from exact commit `8c44eb4` (note 118);
2. source-level fresh-environment construction per replay candidate;
3. 360-row paired SDK profile showing stable endpoint choices `24/24/24`,
   `24/24/24`, and `8/8/8`; and
4. the failed original prediction, which narrows the concept from generic reset
   amortization to **replay-construction-aware multiplicity selection**.

The external target claim must remain predictive and relative to the linked
baseline. A valid subthreshold official result will disconfirm it; an invalid or
timeout result will disconfirm the composite engineering prediction. The final
theory-review round remains unspent until this revision is frozen.
