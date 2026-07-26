# T082 — Path A approval and Cycle-3 iteration-6 direction selection

**Date:** 2026-07-26 · **Phase:** 5 → 2 · **Cycle:** 3 · **Iteration:** 6/6 · **Status:** completed

## Context

T081 recommended concluding SCOC-32 because its defining mechanism was refuted,
even though the bundled live system raised the public score from `69.570` to
`81.225`. The required Phase-5 user checkpoint offered either Path C or an
explicit extension for a fresh non-SCOC competition direction.

The user responded:

> then continue improving

This is recorded as authorization for exactly one additional research iteration,
the minimum non-open-ended extension needed to continue. The research-iteration
limit and spend therefore move from `5/5` to `6/6`. The instruction does not
relax the submit-only-when-confident gate.

## Exact incumbent recovery

Read-only inspection of the latest pulled Kaggle notebook snapshot found:

```text
notebook_sha256=25655097c513602c4e9edc0ef15f054b4209394a3a0bba5df3a98aa56fee0213
embedded_write_cell_sha256=bfd6b4854b4750ba2552b4ad0f8fbb3f51fd6e5cdcd9c4ab97e35f74a3b86b45
enable_scoc=False
multi_fill_messages=24
multi_probe_reps=2
probe_reps=5
templates=8
```

Thus the live `81.225` version had SCOC disabled. Its active controller is the
adaptive single-post versus full-repeat multi-message route. The live gain does
not validate SCOC; it instead makes the active orchestration/controller surface
the most plausible place to search. This is still not a controlled attribution
claim because Kaggle exposes only the aggregate score.

The current controller schedules, when time permits:

```text
1 discarded cold-start call
8 templates * 5 probe repetitions = 40 single-message probe calls
2 multi-message route probes
43 candidate executions before fill
```

After route selection it initializes `candidates = []`; valid probe outputs are
not available to the returned portfolio. Those probes consume generation budget,
while the separate replay budget is charged only if a probe is returned.

Attempts to pull private historical kernel versions `7`, `8`, and `9` through the
versioned Kaggle CLI endpoint each returned `403 Client Error: Forbidden`. The
latest current snapshot and the scored submission ledger are available, but
version-by-version source attribution remains unavailable. No Kaggle mutation or
submission was made.

## Candidate critique rubric

Scores are `impact × feasibility / complexity`, with each input on `1–5`.

| Candidate | Most likely failure mode | Hardest implementation trap | Evidence check | I/F/C | Score | Decision |
|---|---|---|---|---:|---:|---|
| Dual-Budget Evidence Reuse (DBER) | slow probes displace denser fill candidates and reduce score per replay second | treating already-paid generation cost as zero replay cost, or banking all probes regardless of the binding resource | exact source shows 43 pre-fill executions and zero returned probe inventory; separate generation/replay budgets make conditional salvage possible; public controls bank probes but do not implement shadow-price admission | 4/5/2 | **10.00** | select for profile-first Phase 2 |
| Sequential-elimination probe scheduler | latency noise or rare firing eliminates the true best template | constructing confidence bounds from dependent single traces and then claiming target reliability | exact source shows a uniform 40-probe template sweep, but no target rerun telemetry identifies its variance or regret | 3/4/2 | 6.00 | reject for this iteration; premise less identified |
| Official-output attribution harness | Kaggle still exposes only one aggregate score, so instrumentation cannot recover component effects | mistaking commit-run logs for hidden competition-rerun logs | `episodes` returns no rows; versioned private pulls return 403; prior output recovery contains no competition-rerun attack telemetry | 5/1/2 | 2.50 | reject as externally blocked |
| Replay-tail certificate refinement | safer sizing lowers void risk but can reduce score without identifying unused budget | reusing observed maxima or an arbitrary margin as a tail guarantee | this dimension already consumed Cycle-3 work and lacks per-candidate live tail telemetry | 3/3/3 | 3.00 | reject as used and weakly identified |

## Selected structural move

**DBER changes one dimension:** the admission policy for already-validated probe
outputs under separate generation and replay budgets.

It does not change prompts, message multiplicity, scorer semantics, guardrails,
or the chosen fill structure. Its essential rule is:

1. retain exact successful probe candidates and their measured replay costs in a
   side inventory;
2. complete ordinary route selection and fill unchanged;
3. identify the binding resource from measured generation stop, replay headroom,
   and candidate headroom;
4. admit probe inventory only when generation stopped first, replay/candidate
   headroom remains, and each probe's raw-per-replay-second is at least the
   marginal admissible fill density;
5. otherwise return the unchanged incumbent portfolio.

This is not naive probe banking. The distinguishing prediction is conditional:

- in generation-limited/replay-headroom regimes, DBER increases returned exact
  raw score without another target interaction;
- in replay-limited or candidate-limited regimes, DBER returns exactly the
  incumbent portfolio and score;
- bank-all admits lower-density probes in at least one replay-limited control and
  must perform worse than DBER there.

Before any attack edit, T083 must produce a pre-change profile artifact showing
whether the incumbent ever reaches the required generation-limited/replay-headroom
regime. If it does not, DBER is rejected without implementation.

## Anti-stacking and component roles

| Component | Single role | Interface | Removal prediction |
|---|---|---|---|
| probe inventory | preserve exact successful probe candidate, raw value, and measured replay cost | probe result → immutable inventory row | removing it makes conditional salvage impossible |
| binding-resource classifier | decide whether replay/candidate headroom exists after incumbent fill | incumbent debug totals → `generation|replay|candidate|none` | removing it collapses to unsafe bank-all |
| density admission | admit only positive marginal-value inventory | inventory + headroom + marginal fill density → returned supplement | removing it admits slower probes and regresses replay-limited controls |
| incumbent fallback | preserve exact current output when the gate is not met | failed eligibility → byte-equivalent incumbent candidate list | removing it creates unconditional regression risk |

The system claim, if the work survives, is an end-to-end score improvement in
the pre-specified generation-limited regime with no loss in replay-limited
controls. No component receives standalone novelty credit.

## Gate Check

- User path authorization: exact quote above, interpreted as one iteration only.
- Budget: research iterations `5/5 → 6/6`; review budget unchanged at `12/32`.
- Fresh dimension: `probe-output-admission-under-separate-generation-and-replay-budgets`.
- Candidate rubric: four alternatives scored with failure mode, implementation
  trap, evidence check, and rejection reason.
- Exact incumbent fact: latest pulled notebook has `enable_scoc=False`.
- Submission boundary: no Kaggle mutation or submission; confidence gate remains.

## Problem alignment

DBER targets the competition's actual systems problem: recover score already paid
for during online generation only when it can be replayed without increasing
void risk, while preserving the exact `81.225` incumbent as the fallback.

## Decision

Take Phase-5 Path A for one iteration. Retire SCOC as the active mechanism,
select DBER provisionally, enter Phase 2, and require the pre-change bottleneck
profile before hypothesis freeze or implementation.

## Next Steps

T083 profiles the unchanged incumbent across pre-specified generation-, replay-,
and candidate-limited regimes. It records attempted probes, successful discarded
probes, generation time, replay cost/headroom, returned raw, and the oracle
salvage ceiling. No attack edit or Kaggle action is allowed in T083.

## Machine-readable close

```text
t082_path_a=PASS user_quote="then continue improving" research_budget=6/6 phase=2 iteration=6 selected=dber varies=probe-output-admission-under-separate-generation-and-replay-budgets incumbent_live=81.225 incumbent_scoc=false scheduled_prefill_calls=43 profile_first=true attack_edit=false kaggle_mutation=false submission=false next_task=T083
```
