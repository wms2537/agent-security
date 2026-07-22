# Cycle-3 evidence pivot — Monotone Prefix Controller-24

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Research iteration:** 2/5 · **Status:** direction selected, hypothesis not frozen

## Why v3 is not being patched

Round-3 review correctly rejected the claim that two validation extrema are
future lower/upper bounds. A second inspection found a more fundamental Occam
failure: the retained source-authentic controlled SDK evidence has **no winning
arm heterogeneity within `{1,4,8}`**. Fixed `m=8` is best in all `9/9` cells.
The v3 Phase-3 table that selected `m=1` was an algebraic conformance profile,
not measured evidence that NPG's `{1,4,8}` search would repay its cost.

The right move is therefore to replace the varied dimension, not add a more
elaborate statistical wrapper around an unmeasured decision.

## Immutable evidence audit

Read-only checker:
`experiments/poc/mpc24_evidence_audit.py`, SHA-256
`989ec1d97642589a099e8774e6b2a05b91906c31d0590094a28c537f86f5c456`.

It binds:

| Artifact | SHA-256 |
|---|---|
| `experiments/configs/porf-c3-profile-v2.json` | `6d15eb96013f94ae760faa9bfaa22dcdf15419df7bb1b68ec02ec6fc27add0c2` |
| `experiments/runs/porf-c3-profile-v2/COMPLETE.json` | `ea7a6d6d53cf7cf3453269e53ce14566943402aa5673022277ea8968f019a1b5` |
| `experiments/runs/porf-c3-profile-v2/samples.tsv` | `61395ac87dca4ace41993325372fd8dc7db6d960efcd502c04934095ed73276d` |
| `experiments/runs/porf-c3-profile-v2/summary.json` | `64c05a59d9006446a7eb35fcabef59368b63b7bc4ad06db252590bd085debf77` |

Exact command:

```bash
comp/.venv/bin/python -I experiments/poc/mpc24_evidence_audit.py
```

Output:

```text
mpc24_evidence_audit=PASS
artifact_rows=360
fixed8_best_within_1_4_8=9/9
full_frontier_best24=6/9
full_frontier_best8=3/9
replicate0_sentinel_select24=6/9
replicate0_sentinel_select8=3/9
heldout_controller_ge_fixed8=9/9
heldout_controller_gt_fixed8=6/9
heldout_aggregate_ratio=1.507376725838
prefix8_timing_scope=independent_proxy_not_nested_measurement
official_target_inference=none
```

The retrospective controller uses replicate 0 only for a preordered sentinel
choice and replicates 1–4 for the fill-cost/raw extrema. A same-budget fixed-8
portfolio gets its own arm-8 replicate-0 sentinel plus the same held-out rule.
The controller equals fixed-8 in all three context-cliff cells and beats it in
the six full-continuation cells.

This is a descriptive secondary analysis of an existing controlled artifact.
It is not a new experiment, an independent population sample, or official
target evidence. In particular, the prefix-8 timing inside a 24-message
sentinel was not recorded; the audit labels its independently generated arm-8
timing as a proxy. Phase 3 must measure the actual nested prefix.

## Selected v4 direction

**Monotone Prefix Controller-24 (MPC-24)** varies the observed decision boundary
`{8,24}`, not the already dominated `{1,4,8}` search.

Provisional state machine:

```text
START_24
  sentinel 24 admissible and plug-in total >= 1.10 × prefix-8 plug-in total
    -> FILL_24
  otherwise prefix 8 admissible -> FILL_8
  otherwise message 1 succeeds -> FILL_1
  otherwise -> FILL_1 with sentinel dropped

FILL_24
  every candidate verified at exact message indices
  any 24-prefix failure -> return eligible 8 or 1 prefix, then permanently FILL_8/FILL_1

FILL_8
  every candidate verified at exact message indices
  any 8-prefix failure -> return eligible message 1, then permanently FILL_1

FILL_1
  retain only verified message-1 candidates
```

The sentinel quantities will be named **plug-in estimates**, never bounds. The
single target-facing assumption is that the first path is directionally useful
for later paths; every subsequent returned path is nevertheless measured and
the controller can move only toward shorter prefixes. No transition returns to
a longer state.

## Component roles

| Module | Role | Contract | Status |
|---|---|---|---|
| MPC-24 selector | choose only the measured heterogeneous boundary | one exact 24 path with snapshots at 1/8/24 → initial state | sole new algorithmic component |
| indexed trace differencer | prevent aggregate events masquerading as continuation | before/after `export_trace_dict()` tool-event lists + `interact().tool_events_added` cross-check → exact event slice | correctness control |
| monotone fallback | make every failure branch total | current path and state → eligible returned prefix plus one strictly shorter permanent state | correctness control |
| replay ledger | cap returned portfolio | measured prefix cost × 1.10, 0.90×9000 seconds, cap 2000 → feasible list | inherited safety control |
| template selector | preserve exact incumbent wording selection | common probes → one builder | inherited/common control |

No component receives competition-score credit except the end-to-end MPC-24
policy. Fixed-8 is the strongest removal/Occam comparator. Fixed-24 is the
context-cliff stress comparator. A no-fallback state machine is diagnostic only
and can never be used officially.

## Public generation-to-replay scope

Generation and public replay use the same model name and seed, but replay builds
a fresh environment for every candidate and applies a replay guardrail. Thus a
generation trace is neither a replay success guarantee nor a replay-time bound.
The 0.90×1.10 ledger remains a target-linked heuristic inherited from the valid
69.570 artifact. MPC-24 will state this as an assumption; any invalid or timeout
official outcome disconfirms the composite prediction.

Per-message attribution must use trace differencing. `interact()` returns only
counts in `EnvInteractionResult`; event contents and exact URL matching come
from the suffix added to `export_trace_dict()["tool_events"]`. The count is a
cross-check, not the source of event identity.

## Required v4 freeze work

Before another review, v4 must:

1. bind the evidence paths/hashes above directly in the hypothesis and checker;
2. define the sentinel plug-in objective algebraically without L/U language;
3. define every state transition, returned prefix, generation/replay/candidate
   charge and terminal fill exactly;
4. include branch fixtures for sentinel 24/8/1/drop, late 24→8, late 8→1,
   incomplete path, replay binding, candidate-cap binding and fixed-8 beating
   MPC after sentinel overhead;
5. make source-authentic nested 8/24 measurement—not pre-encoded algebraic
   tables—the Phase-3 value test;
6. keep the official claim directional and low confidence.

## Gate Check

- New search dimension: `monotone-24-to-8-prefix-control`, metric.
- Evidence before theory: PASS at the controlled-artifact/descriptive rung.
- Occam: fixed-8 is the required end-to-end comparator.
- Hypothesis v4: not yet written.
- Review budget: `3/12`; no new dispatch.
- Phase 3 and Kaggle mutation: closed.

## Decision

Retire NPG-8 as inconclusive and write a structurally new MPC-24 hypothesis.
Do not edit v3, implement the attack, run Phase 3, or mutate Kaggle yet.
