# HCMS-24 Phase-3 PoC code review round 3

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Fixed commit:** `c259685` · **Status:** NEEDS_REVISION before execution

The fresh reviewer compiled the immutable runner, passed all 15 permitted toy
tests, confirmed a clean worktree and absent canonical attempt, and returned
the following final report verbatim.

## Reviewer report

- HIGH — Candidate/path reconstruction is still not decision-complete. Candidate replay coverage trusts emitted `ledger_charge_s`, while ledger kind/formula, proposal, state transition, and permitted return are never checked against the configured policy (`runner:687`, `runner:783`, `runner:1811`). Cell reconstruction only checks candidate→returned-path linkage; it never requires every `outcome=returned` path to have exactly one candidate (`runner:1890`). Consequently, coherent ledger/policy drift or omitted baseline candidates can remain `cell_valid` and alter the primary ratio, contrary to the exact policies and incomplete-artifact invalidation rules (`config:29`, `config:42`, `hypothesis:198`, `hypothesis:380`).

- HIGH — Real failure checkpointing still has evidence-loss windows. Generation and replay checkpoint before an interaction and on an interaction exception, but not immediately after a successful call (`runner:1158`, `runner:1201`, `runner:963`, `runner:995`). Likewise, after replay succeeds, the completed row is appended without updating `generated_unreplayed_candidates` until the next iteration or final aggregation (`runner:1315`, `runner:1338`, `runner:1377`). An asynchronous outer timeout in these windows can omit the latest trace/suffix or classify an already replayed candidate as unreplayed, contrary to the claimed before-and-after checkpointing (`repair:36`).

- MEDIUM — Exception-cell reconstruction trusts the semantic contents of `in_flight`. Validation checks its self-hash, but does not derive active-path timing, unreplayed ledger charges, or current replay elapsed from independent evidence (`runner:1506`, `runner:1875`). Those trusted fields directly determine reconstructed exception-cell totals. On any reconstruction error, reconciliation also falls back to the original source cell (`runner:2089`), short of the promised exception-cell rederivation (`repair:17`).

- MEDIUM — Source and reload audits are not required to produce the same malformed-artifact set. Only `len(malformed_artifacts)` enters the summary (`runner:2141`, `runner:2199`); `main` discards the reload result and never compares its set with the source audit (`runner:2494`, `runner:2576`). Different same-sized sets could therefore pass. The readable-malformation control flow otherwise can publish `status=invalid`, unreadable output fails before publication, and stdout→hashed `run.log`→COMPLETE ordering remains correct.

Compilation passed, all 15 permitted toy tests passed, the worktree remained clean, and the canonical attempt directory remained absent. No scientific runner was executed. Pre-run code fixes remain.

**NEEDS_REVISION**

## Main-agent disposition

Add per-path cumulative timing evidence and reconstruct configured proposal,
prefix selection, state transition and ledger formula; close post-success
checkpoint windows; exclude unverified in-flight timing from exception-cell
decision totals; never fall back to a trusted source cell; and record/compare
the exact malformed artifact set. Scientific execution remains forbidden,
attempts remain `0/3`, and no attack or Kaggle action occurred.
