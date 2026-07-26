# SCOC-32 Phase-0 data governance

**Recorded:** 2026-07-23

## Scope and source legality

- Data/artifacts are repository-generated candidates, official SDK logic, and read-only Kaggle metadata.
- No private user data, no real secrets, no credential material, and no non-public personal data are introduced in Phase-0.
- Source-compatible controls are reuses of public mechanisms only; they are not attributed as target scores unless explicitly attributed.

## External dependencies

- official SDK source and pinned public notebooks are inspected for protocol and semantics.
- source licenses were already classified under project governance: both `gpt-oss` and `Gemma` paths remain open-source use-compatible in current scope.
- no additional model weights, frameworks, or dataset downloads are part of T065.

## Privacy and dual-use posture

This phase is dual-use:

- It studies candidate-chain mechanics and timing/coverage invariants.
- It does not include payload release or external abuse tooling.
- Findings are retained as internal mechanism claims with explicit retirement rules until target-envelope confidence passes.

## Action restrictions in this phase

- Kaggle actions remain allowed only under user scope from prior standing authorization, but **submission is gated** by confidence gate.
- no target payload extraction, no service attack, no model API calls beyond authorized Kaggle workflow.
- no benchmark generation, no external data egress, no destructive operations.
