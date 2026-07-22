# HCMS-24 resource diagnosis and replacement selection

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 3/5 · **Status:** completed retrospective diagnosis

## Context

The sealed HCMS-24 Phase-3 attempt was correctly classified `invalid` despite a
diagnostic raw ratio of `1.391831525207`. Report 161 localized two
high-confidence prediction failures: candidate-level replay coverage was
`187/189`, and four primary method-cells crossed the two-second generation
budget. This note asks which structural replacement best serves the competition
endpoint without weakening the failed protocol after observing its output.

The deterministic read-only checker is
`experiments/poc/rahcms_resource_diagnostic.py`. It binds the sealed
`COMPLETE.json`, verifies every named artifact hash, and recomputes the
diagnostics below. It never invokes the scientific runner.

## Exact diagnostic evidence

Command:

```text
comp/.venv/bin/python -I experiments/poc/rahcms_resource_diagnostic.py
```

Decisive output:

```text
rahcms_resource_diagnostic=PASS
calibrated_candidate_coverage=470/472
hcms_candidate_coverage=187/189
hcms_aggregate_replay_overage_cells=0/36
scalar_aggregate_replay_overage_cells=19/36
primary_generation_overage_cells=4/144
primary_hcms_prefix_cumulative_ratio_max=0.910666621123
primary_hcms_cell_total_ratio_max=0.779857104646
safety_hcms_prefix_cumulative_ratio_max=1.102552878986
first_ledger_no_fit_cells=97
post_first_no_fit_paths=420
post_first_no_fit_seconds=59.767362233368
primary_post_first_no_fit_paths=415
primary_post_first_no_fit_seconds=59.181928537553
later_recovery_candidates=3
later_recovery_raw=54.0
absorbing_hcms_raw=39240.0
absorbing_fixed8_raw=28170.0
absorbing_fixed24_raw=23160.0
absorbing_hcms_to_best_simple_ratio=1.392971246006
first_no_fit_max_generation_elapsed_s=1.917339173960
primary_zero_interaction_paths_gt_point_one=44/84
inference=retrospective_diagnosis_only
```

### Replay estimand mismatch

The two HCMS individual replay misses did not produce an aggregate replay
overage. Across all 36 HCMS primary cells, every cumulative accepted prefix had
actual replay below its cumulative point charge; the worst cumulative prefix
ratio was `0.910666621123`, and the worst full-cell ratio was
`0.779857104646`. The excluded delayed-cliff safety cell differed: its first
candidate produced a prefix ratio `1.102552878986`, although its complete-cell
ratio was only `0.728885443448`.

The competition source constrains the total replay phase per model/guardrail,
not correctness of every candidate-specific cost prediction. A new protocol may
therefore calibrate a complete-cell, all-prefix risk object. It may not relabel
the old run: candidate-wise coverage was a frozen validity condition and remains
failed.

### Futile generation tail

After the first `drop_ledger_no_fit`, 97 cells continued generating. The tail
contained 420 paths and consumed `59.767362233368` seconds, recovering only
three one-message candidates worth 54 total raw. In the primary grid the tail
was 415 paths and `59.181928537553` seconds. Every one of the four generation
overages occurred inside this post-no-fit tail; no first no-fit itself crossed
two seconds, and the latest first no-fit ended at `1.917339173960`.

A retrospective absorbing stop removes only one HCMS candidate and two fixed-8
candidates. Its diagnostic aggregates are HCMS `39240`, fixed 8 `28170`, fixed
24/no-salvage `23160`, leaving the HCMS/simple ratio at `1.392971246006`. This
counterfactual is strong design evidence, not confirmation: its rule was chosen
after seeing the result and must face fresh data.

The immediate physical cause of the overages is also measurable: `44/84`
primary zero-interaction terminal paths cost more than the fixed `0.1`-second
reserve. A point reserve that is smaller than the non-interaction
construction/reset tail cannot be a deadline certificate.

## Literature boundary

The targeted five-source pass is report 162. Its result is not “use conformal
prediction” in the abstract:

- CQR gives finite-sample **marginal** coverage under exchangeability, not
  conditional or hard deadline safety.
- conformal risk control gives expected bounded loss under exchangeable random
  loss functions, not zero failure in one cell;
- arbitrary-dependence online conformal controls retrospective average coverage,
  so misses may cluster inside the one cell that matters;
- time-uniform Chernoff machinery tolerates predictable selection only after a
  conditional `sub-psi` process is proved; and
- the June-2026 recovery-deadline preprint obtains hard safety from a separate
  verified backstop, not from its conformal quantile.

The competition's `RemoteEnv` is an important negative fact. Attack code blocks
on an in-flight remote operation and cannot cancel it; the inference server's
five-second finalization grace accepts a promptly returned candidate list but
does not turn an unbounded model call into a safe operation. Any official
non-void claim must therefore remain probabilistic and conditional on a target
atomic-cost tail. Controlled mocks may test a bounded backstop, but they cannot
prove that target assumption.

## Candidate critique

Scores are `impact × feasibility / complexity`, each factor 1--5. Evidence
checks are decisive: a high arithmetic score cannot rescue a candidate whose
premise conflicts with source or prospective evidence.

| Candidate | Most likely failure mode | Hardest implementation trap | Evidence check | I | F | C | Score | Decision |
|---|---|---|---|---:|---:|---:|---:|---|
| A. Larger fixed reserve/multiplier | underfills or still misses an unseen tail; no risk meaning | choosing the constant after this run | old 0.1 failed; 90s/1.10 historical target settings are valid evidence of one completed artifact, not a tail bound | 2 | 2 | 1 | 4.00 | reject: post-hoc threshold fitting |
| B. Absorb on first replay no-fit only | generation becomes safe but replay risk remains unquantified | preserving one shared transition across all controls | removes all observed generation overages at 54 raw retrospective cost; HCMS aggregate overage was already 0/36 | 2 | 4 | 2 | 4.00 | retain as one transition, insufficient alone |
| C. Candidate-wise conformal charge | marginal 1-alpha compounds over hundreds of candidates | pooling adaptively selected candidate rows as if exchangeable | 470/472 candidate coverage still coexisted with joint invalidity; literature rejects the family-wise shortcut | 3 | 3 | 3 | 3.00 | reject as primary safety object |
| D. Time-uniform martingale ledger | a convenient unconditional tail model is mistaken for the required conditional MGF | proving and retaining the filtration, censored costs and `sub-psi` increments | no present target artifact identifies those conditional tails | 4 | 1 | 5 | 0.80 | park until target telemetry exists |
| E. Cancellable hard timeout wrapper | target RemoteEnv call continues while user code is blocked | safely cancelling stateful remote environment operations | source explicitly says attack code cannot cancel an in-flight operation | 5 | 1 | 4 | 1.25 | source-refuted for target |
| F. Prefix-Risk Absorbing Controller | episode exchangeability fails or envelope is too conservative | calibrating the maximal cumulative-prefix score without leaking evaluation and preserving COMPLETE-last censored outcomes | matches total replay endpoint; post-no-fit tail is a measured bottleneck; conformal theorem applies only to independent complete-cell units | 5 | 4 | 3 | **6.67** | **select** |

Rejected candidates are not hidden: A lacks a prospective basis; B leaves the
resource-risk gate incomplete; C controls the wrong sampling unit; D needs an
unproved tail process; E is physically unavailable in the target protocol.

## Selected concept: Prefix-Risk Absorbing Controller (PRAC-24)

### Plain language

PRAC-24 keeps HCMS's high-ceiling, exact-prefix salvage policy but changes the
unit of resource reasoning. It calibrates one score for a complete adaptive
cell: the worst cumulative actual-replay/point-ledger ratio over every prefix of
the eligible candidate sequence. This retains all dependence among candidates
inside a cell and directly covers whichever prefix the replay budget eventually
accepts. When the next exact candidate cannot fit the risk-adjusted replay
ledger, the cell enters an absorbing stop rather than sampling hundreds of
additional paths in hope of a cheaper timing draw. A separate pre-path terminal
reserve and adverse timeout fixture test the generation backstop; statistical
coverage is never called a deterministic target guarantee.

### Formal core

For calibration cell `e`, let eligible candidates appear in policy order
`i=1,...,K_e`. Let `a_ei` be actual fresh replay cost and `l_ei>0` the frozen
base ledger charge. Define

```text
A_e(k) = sum_{i<=k} a_ei
L_e(k) = sum_{i<=k} l_ei
Z_e    = max_{1<=k<=K_e} A_e(k)/L_e(k)
```

Set `Z_e=+infinity` for any missing, censored, timed-out or malformed required
cost. On `n` independent complete calibration cells, with cell-level risk
`alpha`, use the split-conformal rank

```text
j = ceil((n+1)*(1-alpha));
q = j-th smallest Z_e when j<=n, otherwise +infinity.
```

In a fresh cell, accept the longest sequential candidate prefix `k` satisfying
`q*L_e(k) <= replay_budget`. Stop permanently at the first otherwise-exact
candidate that does not fit. If complete calibration cells and the fresh cell
are exchangeable under the fixed proposal policy, rank symmetry gives marginal
`P(Z_new<=q) >= 1-alpha`. On that event, every accepted prefix—including the
adaptively selected terminal prefix—has actual replay within budget.

This is a mapping move: a dependent within-cell candidate stream is mapped to
one scalar complete-cell score. The theorem needs exchangeability of cells, not
of candidate rows. It remains marginal over calibration and the fresh cell.

### Generation backstop

The replay envelope and absorbing transition do not make environment calls
cancellable. PRAC therefore separates:

1. a pre-path one-sided bound for the entire next atomic path plus terminal
   publication work, calibrated on complete cells and charged before starting;
2. an absorbing return of the current candidate list when this bound does not
   fit; and
3. an injected bounded-latency fixture in which the full controller must return
   a valid truncated bundle while an envelope-only removal crosses the deadline.

If a future implementation cannot demonstrate bounded cancellation/publication
in its claimed environment, its claim is narrowed to empirical controlled
non-overage. It cannot call the target solution void-proof.

## Component roles and interfaces

| Component | Role | Input → output | Measured bottleneck | Removal |
|---|---|---|---|---|
| HCMS exact-prefix structure (fixed inherited base) | create high-raw 24/8/1 candidates | indexed path evidence → eligible ordered candidate | controlled ratio `1.3918`, retained absorbing diagnostic `1.3930` | fixed8 and fixed24/no-salvage |
| complete-cell prefix envelope | convert dependent replay costs into one cell-risk multiplier | calibration trajectories → `q` or abstain | individual coverage 187/189 but aggregate HCMS overage 0/36; safety first-prefix ratio 1.1026 | point-ledger HCMS and candidate-wise-envelope diagnostic |
| absorbing no-fit transition | prevent futile timing lottery after replay saturation | first otherwise-exact no-fit → terminal current prefix | 420 tail paths, 59.77s, only three recovered candidates | retry-after-no-fit removal |
| terminal admission/backstop control | preserve time to return auditable evidence | remaining time + next-path envelope → start or truncate | 4 primary overages; 44/84 zero-interaction paths exceeded 0.1s | envelope-only adverse fixture |

The contribution claim is the valid end-to-end constrained result, not the
number of rows in this table. Every component has one role and one removal.

## Taxonomy and anti-stacking

- opportunity: **Failure/Risk Gap**, secondary Resource Bottleneck;
- method paradigm: **Robustification**, secondary Formal Derivation;
- dominant operation: **replace**.

PRAC replaces candidate-level point coverage with a complete-cell all-prefix
risk object and replaces retry-after-no-fit with an absorbing state. It is not
Bridge Opportunity × Synthesis/Unification.

The distinguishing prediction is not “a larger margin is safer.” Under the
same base charge and nominal cell risk, candidate-wise calibration can achieve
high pooled candidate coverage while missing the complete-cell family-wise
target; PRAC predicts coverage of the accepted cumulative prefix at the
declared cell level. On a bounded injected long-construction fixture, an
envelope-only variant may begin work and overrun, while the full terminal gate
must truncate before it. A plain combination of a multiplier and early stop
does not imply either prediction.

## Decision

Select PRAC-24 for one superseding Phase-2 hypothesis. The hypothesis must:

- preserve the old invalid result and use it only for diagnosis/design;
- use fresh, never-inspected complete calibration/evaluation cell identities;
- freeze the calibration rank, infinity/abstain behavior, proposal stream,
  controls, risks and materiality threshold before execution;
- retain timeouts and censoring as infinity rather than silently dropping them;
- compare HCMS with symmetric fixed8 and fixed24/no-salvage controls under the
  same risk controller;
- test envelope, absorbing-stop and terminal-gate removals separately;
- withhold official-score and target non-void claims until a separate
  target-confidence bridge; and
- leave `experiments/attack.py` and Kaggle untouched through theory review.

No hypothesis-review round is charged by this diagnosis.
