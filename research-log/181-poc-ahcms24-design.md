# Phase-3 PoC design — AHCMS-24

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Run ID:** `ahcms24-c3-poc-v1` · **Status:** frozen before implementation and scientific execution

## Core assumption tested

The reviewed claim has one contribution component: after the first otherwise
exact candidate cannot fit the inherited cumulative point-replay ledger,
terminate the unit rather than attempting later paths. The smallest credible
fresh probe must determine whether that one event-aligned deletion:

1. raises aggregate integer raw per projected captured generation-path
   nanosecond by at least `1.10x` over otherwise identical retry HCMS;
2. still clears `1.10x` after floor-discounting half of every retry-only tail
   nanosecond while retaining all retry raw;
3. retains at least `99.5%` of positive retry raw and has both nominal and
   discounted tail support of at least `10%`;
4. gives AHCMS zero strict two-second generation or aggregate-replay elapsed
   overage units; and
5. clears the same constrained efficiency/Pareto endpoint against the two
   specified simple controls, fixed8 absorption and fixed24/no-salvage
   absorption.

The immutable scientific specification is
`research-log/178-hypothesis-iter-8-ahcms24-v5.md`, independently judged
`RIGOROUS` in report 180. Its normative machine contract is
`experiments/configs/ahcms24-c3-v5.json`. This design adds no method, threshold,
profile, sample, control, endpoint, or scientific freedom.

## Bound identities

Before implementation, the exact identities are:

```text
AHCMS v5 hypothesis SHA-256  1877c5023d16addcd029a9a9d9cacbbe34b5213deef9faa8bd9c86f8dc0025bb
AHCMS v5 config SHA-256      1d0e1128b4179b56604a00c60ad7461449f98815eb78ab1f85590da93f752715
Phase-2 checker SHA-256      b33c612ce930779d56446fd2e82ff3ced6c207385f0d3b0c8b5a36d24d2ecd84
timer audit SHA-256          304484543ce7471526408234f13fe83a5277bf756b10b11fcca891e5a47acf7d
historical runner SHA-256    7b030c67a7f18c4bce77db67f7db757b817aede7cbaf75aa1195a09d42f6b1f6
base attack SHA-256          8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d
```

The new runner and test files, canonical attempt directory, and prediction rows
were absent when these identities were checked. The old HCMS scientific bundle
is retrospective profile evidence only and can never be used as this run's
fresh outcome.

## Minimal matched-trace probe

The canonical attempt contains exactly three preregistered controlled profiles
times three freshly drawn unique masters: nine units. Each unit runs in a fresh
spawned child process without an evaluated method label. For every one of 16
path slots it captures fresh arms `24,8,1` in the independently sampled arm
order, even after a potential first no-fit. Every exact eligible potential
candidate needed by any projection also receives its own source-authentic
replay capture.

Only after all capture is complete do four pure deterministic projections walk
the same table:

- `ahcms_absorbing`;
- `hcms_retry_removal`;
- `fixed8_absorbing`; and
- `fixed24_no_salvage_absorbing`.

The primary pair shares every state and selected occurrence through its first
replay-ledger no-fit. AHCMS selects zero later paths; retry may continue under
the inherited path cap and strict `remaining > 100,000,000 ns` admission rule.
All methods publish, including scientifically infeasible simple controls.

This design is deliberately a complete potential table rather than four live
method executions. That removes evaluated-method order, cache, predecessor,
thermal, and live scheduling contrasts from the primary attribution. It does
not remove elapsed variability inside a captured arm; the mandatory half-tail
stress addresses only the prespecified 50% envelope.

## Operational definition of q-independent

Here `q-independent` means that no calibration quantity, threshold, sample
identity, profile parameter, arm order, timer rule, projection rule, exclusion,
or decision boundary is fitted from these nine outcomes. `q` is simply any
outcome-derived calibration or tuning quantity that could make the fixed sample
easier to pass. There is no such free quantity in this attempt. Cryptographic
rejection sampling chooses identities and orders once; `SAMPLING.json` is
fsynced before capture; a crash consumes the attempt; and a completed valid
sample maps mechanically to CONFIRM or DISCONFIRM.

## Exact timer and scorer endpoints

Generation captured elapsed starts immediately before the
`generation_environment_construction` checkpoint and ends at the
`monotonic_ns` read immediately after the interaction loop and final completed
`generation_interaction_complete` checkpoint, before exact-flag extraction or
prefix choice.

Replay captured elapsed starts immediately before the
`replay_environment_construction` checkpoint and ends at the `monotonic_ns`
read immediately after the interaction loop and final completed
`replay_interaction_complete` checkpoint, before final trace export,
predicates, signature, or scoring.

Both brackets include checkpoint serialization, construction/reset, in-loop
trace export, interaction, controller work, sleep, preemption, and scheduling
between reads. They do not measure CPU service or remote latency. Every
method-unit raw is recomputed exactly once over its complete accepted finding
sequence with the bound SDK `score_attack_raw`; candidates are never scored and
summed independently.

## Frozen predictions

The eleven `ahcms24-c3-poc-v1` rows in `results.tsv` are frozen before code
implementation. The headline numeric expectations and confirm floors are:

| Metric | Predicted | Confirm rule | Direction | Confidence |
|---|---:|---:|---|---|
| AHCMS/retry efficiency | `1.25` | `>=1.10` | beat baseline | medium |
| AHCMS/retry half-tail efficiency | `1.12` | `>=1.10` | beat baseline | medium |
| AHCMS/retry raw retention | `0.998` | `>=0.995` | match baseline | medium |
| retry-tail elapsed fraction | `0.20` | `>=0.10` | beat baseline | medium |
| half-discounted retry-tail fraction | `0.10` | `>=0.10` | beat baseline | medium |
| AHCMS/fixed8 efficiency | `1.20` | `>=1.10` if feasible | beat baseline | medium |
| AHCMS/fixed24 efficiency | `1.20` | `>=1.10` if feasible | beat baseline | medium |
| feasible-simple Pareto dominators | `0` | exactly `0` | match baseline | high |
| AHCMS generation-overage units | `0` | exactly `0` | match baseline | high |
| AHCMS replay-overage units | `0` | exactly `0` | match baseline | high |
| invalidity count | `0` | exactly `0` | match baseline | high |

Rationale: the sealed historical exact-bracket profile gives nominal `1.3621`,
half-tail `1.1808`, and raw retention `39240/39258 = 0.99954`. The predictions
haircut those retrospective values while preserving the independently reviewed
normative floors. This evidence supports a moderate prior for magnitude, not a
fresh result. Zero overage and invalidity expectations are high-confidence
protocol requirements, not empirical guarantees; the prior HCMS failure makes
their direct measurement especially load-bearing.

## Confirm, disconfirm, invalid, inconclusive

- **CONFIRM:** all nine traces, all 36 projections, source/timer identities,
  integer domains, prefix reconstruction, positive-retry branch, headline and
  half-tail inequalities, retention, both tail-support predicates, zero
  post-trigger AHCMS paths, zero AHCMS overages, both specified-simple rules,
  and every publication/attribution invariant pass.
- **DISCONFIRM:** the attempt is complete and valid but retry raw is zero, the
  trigger/tail is absent or weak, any magnitude/retention/sensitivity predicate
  fails, AHCMS has an overage, or a specified feasible simple defeats its rule.
- **INVALID:** any sampling redraw, crash, timeout, missing arm/replay/method,
  timer or source drift, malformed numeric domain, attribution/support error,
  incomplete artifact, or publication violation occurs. Invalid is not
  scientific disconfirmation and cannot be retried under the same canonical
  label.
- **INCONCLUSIVE:** only an external interruption leaves no complete fixed
  sample; a completed attempt is never called inconclusive to avoid a negative.

## Implementation-before-run safeguard

The implementation dispatch may create only:

- `experiments/poc/ahcms24_phase3_v1.py`;
- `experiments/poc/test_ahcms24_phase3_v1.py`; and
- `research-log/182-ahcms24-poc-implementation.md` only if the orchestrator
  assigns that path (the implementer will not do so in this task).

It may run static compilation and pure/toy tests. Those tests must use synthetic
records and may not construct the three scientific environments, sample fresh
masters, import a target service, or create `experiments/runs/ahcms24-c3-poc-v1`.
The exact scientific command is frozen as:

```text
comp/.venv/bin/python -I experiments/poc/ahcms24_phase3_v1.py --config experiments/configs/ahcms24-c3-v5.json --attempt-dir experiments/runs/ahcms24-c3-poc-v1
```

The runner must refuse any pre-existing attempt path; create and fsync
`SAMPLING.json` before capture; keep command-first `run.log`; emit full trace,
candidate/replay, projection-path, accepted-occurrence, method-unit, aggregate,
decision, and binding artifacts; hash every named artifact; and publish
`COMPLETE.json` last. Its validation path must independently reload those
artifacts and reconstruct all decisions rather than trusting an in-memory
summary.

A fresh independent code/spec review of the committed runner is mandatory.
Only a scrutinized `SOUND` verdict may open the canonical scientific command.
Implementation and tests must therefore leave both the attempt directory and
any fresh scientific outcome absent.

## Transferability argument

A confirmed PoC would establish one narrow fact: on nine fresh source-authentic
controlled potential tables, the event-aligned absorbing transition preserves
nearly all controlled raw while materially improving the exact reviewed
captured-elapsed endpoint, including the 50% tail stress and two named simple
controls. This is directly useful for deciding whether the stop rule merits a
separate 9000-second competition bridge.

It cannot establish target-model trigger prevalence, CPU savings, remote
deadline safety, leaderboard benefit, private-set transfer, or victory. Those
phenomena are model-, workload-, and scale-dependent. Therefore confirmation
opens Phase-4 bridge design; it does not mutate `experiments/attack.py`, push a
Kaggle notebook, or satisfy the seven submission-confidence gates. A technically
valid but target-irrelevant bridge result remains a legal later negative.

## Gate

- Phase 2: **PASS**, immutable v5 plus scrutinized `RIGOROUS` report 180.
- Predictions: **frozen before implementation** in eleven ledger rows.
- Transferability: **bounded to the controlled endpoint**, with target scaling
  explicitly unresolved.
- Scientific attempts: **0/3**; canonical attempt directory absent.
- Code/spec review: **required before execution**.
- Attack mutation, Kaggle commit run, and submission: **not opened by T060**.

## Problem alignment

This probe tests whether the proposed source-compatible stop actually buys
controlled allocation efficiency without hiding overage or raw loss; it moves
toward the measured-bottleneck and mechanical-correctness gates while preserving
the separate resource-safety, target-derived, and submission-decision gates in
`PROBLEM.md`.

## Decision

Freeze this design and its ledger rows, then implement only the unexecuted
runner and adversarial test surface. Do not inspect a fresh outcome before
independent code/spec review.

## Next Steps

1. Dispatch a specification-bound implementer with the scientific run removed
   from its authority.
2. Main-agent verify file scope, static compilation, pure/toy tests, source
   bindings, absence of the attempt directory, and prediction immutability.
3. Commit the unexecuted implementation and open a separate sterile code/spec
   review task.
