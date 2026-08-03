# Hypothesis iteration 11 v2 — Burst-2 validation-fill calibration

Supersedes: `research-log/269-hypothesis-iter-11-burst2-validation-fill.md`

Date: 2026-08-03

## Claim

Changing only the active candidate message shape from one intended `http.post` to two intended `http.post` calls inside the restored v35 validation-fill/replay-safe controller will produce a visible Kaggle public-score measurement that tests whether the smallest candidate-internal density increase can cross the `100.000` score bin.

Plain-language statement:

> V35 spends one replayed candidate to get at most one intended post. K=4 dense branches crossed hidden failure boundaries. K=2 is the smallest possible above-ceiling candidate-internal density step. The experiment keeps the proven fill controller and changes only the message cardinality, then lets the target evaluator decide whether enough second posts survive replay.

This is a calibration hypothesis, not a claim that public notebook metadata proves the score.

## Concept

Name: **Burst-2 Validation Fill**.

Operational definition:

- `BUNDLE_POSTS = 2`.
- Candidate `i` contains exactly one user message.
- For `K=1`, the formatter must be byte-equivalent to the restored v35 `_msg(i, TEMPLATE)` path.
- For `K=2`, the formatter emits exactly two intended `http.post` calls in one message.
- The two destination URLs are globally unique: `_url(2*i)` and `_url(2*i+1)`.
- Each post carries the literal `SECRET_MARKER`.
- A candidate is retained if generation records at least one successful exfiltration event.
- No K=4 dense branch, no measured dense prefix, no slow-row Harmony multipost, no extra template race, no replay-cost multiplier change.
- For K>1, split-by-latency template switching is disabled because the burst message has one frozen shape; this is part of the message-shape replacement and prevents mixing K=2 with Harmony slow-row multipost in the same hypothesis.

## Variables and controls

Independent variable:

```text
candidate-internal post cardinality: K = 1 -> K = 2
```

Controls inherited from restored v35:

- `MARGIN_S = 47.0`
- `SLOWEST0 = 25.0`
- `FILL_BUDGET_FRAC = 0.95`
- `HARD_N_CAP = 2000`
- `REPLAY_SAFE_SIZING = True`
- `REPLAY_SAFE_FRAC = 0.97`
- `PROBE_HOPS = 0`
- `REPLAY_COST_COEF = 1.0`
- `REPLAY_BUDGET_MULT = 1.0`
- same placeholder `submission.csv` and direct `JEDAttackInferenceServer().serve()` wrapper

`varies`: `candidate-internal-post-cardinality-under-validation-fill`

`kind`: `metric`

## Primary comparison and bins

Primary target metric: first eligible Kaggle `public_score`.

Bins:

- Success: `public_score >= 100.000`.
- Partial: `86.670 <= public_score < 100.000`.
- Failure: blank/error or `public_score < 86.670`.

The `100.000` threshold is a target-owned success bin, not a calibrated estimate from public notebook score metadata.

## Evidence chain

1. Retained live floor: v35 public-control validation fill completed at `86.670`.
2. Negative large-density evidence: v36 K=4 blind dense blanked; v37 K=4 measured replacement completed but regressed to `84.735`.
3. Fresh leaderboard head remains in the `107-113` range, so single-post-only tuning is unlikely to win.
4. Report 268 public audit found current public notebooks exposing two tracks:
   - high-80s single-post validation-fill controls;
   - a plausible above-ceiling mechanism prior in `BURST_K=2`.
5. The public-notebook audit does **not** prove that any public notebook corresponds to the live leaderboard leader. It is used only to justify K=2 as the smallest plausible next mechanism, not as outcome evidence.

## Mechanism rationale

The measured bottleneck is score density per replayed candidate:

- v35 is reliable but below the current frontier.
- K=4 has already failed under our runner.
- K=2 is the smallest density increase and should be tested before larger, model-specific, or multi-component variants.

If K=2 works, it should improve because a nontrivial fraction of replayed candidates produce two scored exfiltration events. If it fails, the result tells us either second-event prevalence is too low, replay cost is too high, or the public-audit mechanism depends on additional components excluded here.

## Anti-stacking check

This hypothesis is a one-component replace move.

Measured bottleneck:

- Public score gap: v35 `86.670` versus current visible frontier above `107`.
- Prior failed density attempts: K=4 blind blank, K=4 measured regression.

Ablations/gates:

- `K=1` byte-equivalence check against restored v35 message.
- `K=2` serialization check: exactly one user message, two URLs, two `http.post` mentions, no empty messages, no K=4 wording.
- Fake-live K=2 mechanics check: retained candidate count positive when trace has successful posts; no dense branch markers.
- Commit-run output/source check before any competition submission.
- Public-score comparison against v35 after target submission, if confidence gate passes.

Contribution claim:

- The end-to-end target-owned public score under a K=2-only validation-fill controller.
- Not the public-code prior, and not a bundle of K=2 plus slow-row Harmony multipost.

Distinguishing prediction:

- K=2-only should reach the success bin if the smallest candidate-internal density step is sufficient.
- If the public-audit signal depends on additional components, K=2-only should produce only a partial or failure result.

## Threats to validity

- Selection: Public notebooks may not correspond to current leaderboard leaders; this is explicitly not assumed.
- Confounding: Public notebooks include additional mechanisms; this hypothesis isolates K=2 and may underperform them.
- Assignment: Kaggle submissions are unpaired and remote runtime variance is not exposed.
- Protocol deviation: Notebook wrapper/output mistakes can masquerade as mechanism failure; commit-run output/source checks gate submission.
- Missing data: Per-candidate replay outcomes, second-event prevalence, and private guardrail rows remain hidden.
- Measurement: Generation-side elapsed remains an imperfect replay proxy; no new replay-cost identification claim is made.
- Analysis flexibility: Success/partial/failure bins are frozen before implementation and target submission.
- Selective reporting: All target outcomes, including blank/error/regression, must be logged.

## Failure modes

- K=2 often produces only one scored event while costing more than K=1.
- K=2 returns fewer candidates and loses score density.
- K=2 behaves differently across hidden model/guardrail rows.
- The public-audit `BURST_K=2` prior depends on excluded components.
- The rerun blanks because K=2 still crosses a hidden replay or timeout boundary.

## Metrics

Local mechanics:

- `bundle_k1_byte_equivalent = 1`
- `bundle_k2_url_count = 2`
- `bundle_k2_post_mentions = 2`
- `bundle_k2_empty_messages = 0`
- `bundle_k2_no_dense4_wording = 1`
- `fake_live_k2_count > 0`
- `fake_live_k2_event_count = 2` in a two-event fake trace

Commit-run:

- `submission.csv` exists with header `Id,Score` and four data rows.
- downloaded `attack.py` source matches local source modulo notebook wrapping.
- no `MEASURED_DENSE`, `DENSE_ENABLED`, `_dense_msg`, `_measured_dense`, `SLOW_MULTIPOST`, or K=4 markers.

Target result:

- `public_score` binned as success/partial/failure above.

## Taxonomy

- Opportunity pattern: Optimization Bottleneck.
- Method paradigm: Empirical Mapping.
- Dominant operation: replace.

This is not Bridge × Synthesis because it changes one local structure and excludes other public components.

## Problem alignment

If confirmed, Burst-2 Validation Fill would answer the Cycle-3 core question by showing that source-compliant candidate-internal density can improve expected competition score over the single-post validation-fill floor without the refuted K=4 failure mode.

## Round-1 review fixes

This v2 resolves report 270 as follows:

1. Public-notebook audit is demoted to mechanism prior, not leaderboard explanation.
2. K=2 interface is frozen and excludes K=4/slow-row multipost/template expansion.
3. Split-by-latency behavior for K>1 is specified as disabled by frozen burst shape.
4. `>=100` is labeled as the target-owned success bin, not a calibrated public-notebook estimate.
5. Second-event prevalence risk is explicit in evidence, rationale, threats, and failure modes.

## Gate status

Re-review pending.
