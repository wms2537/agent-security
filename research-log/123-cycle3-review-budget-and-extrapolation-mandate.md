# Cycle-3 review budget and extrapolation mandate

**Date:** 2026-07-22 · **Phase:** 2 · **Cycle:** 3 · **Iteration:** 1 · **Status:** completed

## Context

RCMF v2 received `NEEDS_REVISION` in research-log/122 and exhausted the
Cycle-3 hypothesis-review budget at 2/2. The user then authorized more review
capacity and explicitly redirected the next revision toward extrapolation and
disciplined engineering.

## Content

### Verbatim user authorization

> authorise 10 review rounds, but please make sure you are doing things
> beneficial to the competiton. SOmetimes try tp think out of the box

### Verbatim follow-on directions

> extrapolate ideas

> and engineer the solution properly, make sure every component has its own
> role and does its role at its most

### Operational interpretation

- Add ten hypothesis-review rounds to the already spent/authorized two:
  Cycle-3 limit `2 -> 12`, spent remains `2` until the next dispatch.
- Competition value remains the objective. Review rounds are not a target to
  consume; deterministic/source checks precede every dispatch.
- Before writing RCMF v3, generate a source-grounded extrapolation slate that
  questions whether online multiplicity search is needed at all.
- Select only one active hypothesis. Alternatives remain parked and cannot be
  interleaved.
- For an engineered system, every retained component must have a measured
  bottleneck, a single explicit role/interface, a removal ablation, and an
  end-to-end contribution under the shared generation/replay/candidate caps.
  A component that does not earn its cost is removed.
- Kaggle mutation remains closed until the SciAgent Phase-2 theory gate passes.
  Competition submission remains additionally conditioned on the seven-part
  confidence gate in PROBLEM.md.

## Gate Check

- Consent evidence is the user's verbatim authorization above.
- `state.json.budgets.hypothesis_review_rounds.limit` is raised from `2` to
  `12`; `spent` remains `2`.
- No review dispatch, implementation, Kaggle push, commit run, or submission is
  performed by this budget-recording step.

## Problem alignment

The authorization funds rigorous correction while the extrapolation and
per-component requirements keep the work focused on a simpler, measurable
competition advantage rather than review-driven document growth.

## Decision

Run a main-agent source audit and an extrapolation candidate critique before
freezing v3. Prefer a local `replace` move over adding mechanisms, and require
adaptivity to beat a fixed packed candidate end to end after all search costs.

## Next Steps

Inspect the exact attack/replay/scorer path for three bedrock properties:
first-message prefix invariance, availability of message-indexed event
attribution, and the complete cost of candidate construction. Then compare a
repaired adaptive selector against simpler prefix-preserving fixed packing and
boundary-accounted portfolio alternatives using the SciAgent candidate rubric.
