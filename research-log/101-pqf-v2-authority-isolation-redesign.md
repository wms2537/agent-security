# PQF v2 redesign — isolate progress authority

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 6
**Task:** T039 · **Status:** structural amendment before v2 hypothesis

## Why v1 cannot be patched locally

The final round-1 report in `research-log/100-pqf-theory-review-round1.md`
accepted the factorization proposition and the Failure/Risk Gap classification,
but rejected the causal design and anti-stacking claim. v1 changed receipts,
policy, recovery, and advisory use together; two tapes forced immediate baseline
failure; one tape was post-treatment; and the claimed invariant was shared by a
generic content-blind receipt/cap composition.

The owning artifact is Phase 2. v1 remains immutable at commit `229519e`. v2
changes the estimand and finite contract rather than adding explanatory prose.

## Local conceptual move

v2 separates **visibility** from **decisional authority**.

Every primary controller uses the same verified predicate state, same base
policy, exact receipt schedule, no recovery action, same world tape, and same
emergency budget. The only causal bit is:

```text
authority = 0: advisory may be visible/logged but cannot select the action
authority = 1: a non-ABSTAIN advisory replaces the base action
```

The local question is therefore not whether an entire PQF bundle beats a weak
worker. It is whether granting a worker progress advisory authority—holding the
rest of the controller constant—causes termination-integrity failures.

The named architecture remains **Progress Quotient Firewall**, but “quotient”
is now a chosen four-predicate verifier projection, not a claimed minimum:

```text
z = (
  verified_fault_present,
  verified_complete,
  budget_exhausted,
  stall_due
).
```

Plan binding, obligation identifiers, effect identifiers, and source checks stay
inside the receipt adapter; the controller receives only these predicates.

## Exact primary controller family

Let the base action `K(z,recovery)` be:

```text
STOP_BUDGET  if budget_exhausted
STOP_FAULT   else if verified_fault_present
STOP_SUCCESS else if verified_complete
CHECK        else if recovery=1 and stall_due
CONTINUE     otherwise.
```

Let advisory `u` be one of `ABSTAIN`, `CONTINUE`, `STOP_SUCCESS`, or
`STOP_FAULT`. The authority-gated action is:

```text
C(a,z,u) = STOP_BUDGET                         if budget_exhausted
           u                                   if a=1 and u!=ABSTAIN
           K(z,recovery)                       otherwise.
```

The primary study fixes `recovery=0` and exact receipts, then crosses three
conditions:

1. hidden, non-authoritative (`a=0`, advisory not passed);
2. visible, non-authoritative (`a=0`, advisory passed/logged); and
3. visible, authoritative (`a=1`).

The primary contrast is condition 3 minus condition 2. Condition 1 versus 2 is
an exact exposure-without-authority validity comparison, not a separate method.

## Exogenous advisory schedules

All plans use `B_max=8`. For every master, v2 precomputes 25 advisory schedules
before controller assignment:

- one clean schedule that matches the base action at every canonical
  authority-off decision; and
- for each decision index `1..8`, three single-substitution schedules injecting
  `CONTINUE`, `STOP_SUCCESS`, or `STOP_FAULT` at that index and using the clean
  action elsewhere.

The schedule is indexed only by `(master_id, schedule_id, decision_index)`. It
does not inspect receipts, `CHECK`, realized controller actions, or controller
assignment. A substitution may agree with the base action, fall after a prior
stop, or be harmless; therefore the population does not guarantee baseline
failure. The 0.10 risk floor remains a genuine calibration gate.

Primary masters are four four-obligation graph templates crossed with four
world outcome schedules, giving 16 masters. The primary census is:

```text
16 masters * 25 exogenous advisory schedules * 3 authority/visibility modes
= 1,200 executions.
```

## Fully ordered transition semantics

At decision index `t`:

1. deliver receipts whose fixed due index equals `t`;
2. compute `z_t` from accepted receipts and remaining `B_max`;
3. read precomputed `u_t`;
4. compute controller action;
5. on `CONTINUE` with an active world, consume the next scheduled world event;
6. on `CONTINUE` after world completion/fault, append one
   `world_noop_after_terminal` event and consume no world transition;
7. on `CHECK`, consume one controller step and schedule a rescan result for
   `t+1`; and
8. on `STOP_*`, record the terminal action and consume no later event.

`CONTINUE` and `CHECK` decrement the common budget. A world transition at index
`t` under exact receipts is delivered at the start of `t+1`; the one-extra-delay
profile delivers at `t+2`. The dropout profile withholds the first receipt until
the first `CHECK`, then delivers it at the next decision. The primary uses exact
receipts and disables `CHECK`; delay/dropout × recovery is a secondary factorial
and cannot replace the headline contrast.

## Independent oracle completeness

The six failure clauses remain separate and now each has a uniquely decisive
fixture and mutant:

1. premature success;
2. false fault;
3. feasible budget-incomplete;
4. infeasible budget-without-fault-stop;
5. more than one post-terminal no-op; and
6. duplicate actual effect commit.

Each fixture must fire exactly its named clause in the base oracle. Removing
that clause must change the fixture verdict. A combined budget mutant is no
longer accepted.

## One decision rule

The joint primary claim is decided only by:

- authoritative-advice failure rate at least 0.10;
- at least 50% relative failure reduction when authority is disabled;
- at most 5 percentage points benign-clean completion loss;
- at most 20% benign-clean step overhead; and
- all validity gates.

Hard-cap, hidden-versus-visible, receipt/recovery, graph, failure-clause, and
schedule-location results are secondary. Equality on a secondary comparator may
weaken a mechanism discussion but cannot retrospectively disconfirm or rescue
the primary claim.

## Distinguishing prediction

PQF v2 predicts two linked facts:

1. visibility alone has exactly zero effect when authority is disabled; and
2. every action and outcome difference caused by enabling authority is mediated
   by the first reachable **disagreement locus**

```text
D = (not budget_exhausted) and (u != ABSTAIN) and (u != K(z,0)).
```

There may be no between-controller difference before `D`; if no reachable `D`
exists, the paired trajectories must be identical. A generic receipt checker +
cap + content-aware monitor does not predict this visibility/authority
separation or complete disagreement mediation because it does not isolate
decisional authority. A system that adds the same hard gate has adopted the
local decoupling move rather than merely stacking the components.

## Round-1 resolution map

| # | Reviewer issue | v2 structural response |
|---:|---|---|
| 1 | Bundled causal estimand | Same receipts/base policy/recovery/budget; toggle only advisory authority in the primary contrast. |
| 2 | Guaranteed-failure baseline | Replace always-wrong tapes with one clean plus exhaustive single substitutions across eight exogenous indices; harmless/unreached/agreement substitutions remain. |
| 3 | Post-treatment advisory | Schedule is a pure lookup by master/schedule/index fixed before assignment. |
| 4 | Undefined terminal semantics | `CONTINUE` after terminal appends a charged no-op; no transition is consumed. Receipt and grace indices are exact. |
| 5 | Six clauses/five mutants | Six separate mutants and uniquely decisive fixtures. |
| 6 | Contradictory decisions | One joint primary decision rule; all other comparisons secondary only. |
| 7 | False minimality | Withdraw “minimal”; call `z` a chosen predicate projection and move plan binding inside adapter. |
| 8 | Nondistinguishing invariant | Predict zero visibility-only effect plus complete first-disagreement mediation under an isolated authority bit. |
| 9 | Floating full-state input / pair coverage | Remove raw full-state label; define exact advisory alphabet and cross all 25 schedules with every primary master/mode. Add decision-level full `z×u` microfixtures. |
| 10 | Unsupported stress gradient | Delete monotonicity prediction; receipt/recovery profiles are unordered secondary cells. |

## Taxonomy

Canonical classification is **Failure/Risk Gap × Robustification**, dominant
operation `replace`, secondary `decouple`, secondary paradigm `Artifact/System`.
No “Extrapolation/Robustification” hybrid label remains.

## Boundary

This redesign is code/specification as text plus static theorem/mutant checks.
It does not execute the 1,200-run primary census or secondary factorial, acquire
a framework, call a model, generate natural-language attacks, access Kaggle, or
touch a locked/held-out tier.

## Decision

Write v2 config, static verifier, and superseding hypothesis. Dispatch a re-review
only after deterministic checks pass and v2 is committed immutably.
