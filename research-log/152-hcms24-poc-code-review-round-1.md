# HCMS-24 Phase-3 PoC code review round 1

**Date:** 2026-07-22 · **Phase:** 3 · **Cycle:** 3 · **Fixed diff:** `9f3101d...4a1156a` · **Status:** NEEDS_REVISION before execution

The code-review skill ran independent standards and scientific-spec axes. Both
reports are recorded below.

## Standards

**Hard documented violations:** None. No repository standards source was available; tooling-enforced issues were excluded.

**Judgement-call smells**

- `experiments/poc/hcms24_phase3_v1.py:348-416` — **Primitive Obsession.** Policy concepts are represented by `Mapping[str, Any]` and magic strings such as `"always propose 24"`, `"monotone"`, and `"scalar_removal"`. A typed `Policy` plus enums/value objects would make valid states explicit and remove string-driven branching.

- `experiments/poc/hcms24_phase3_v1.py:637-912` — **Data Clumps / Duplicated Code.** The coordinate group `namespace/profile/master/order_index/position/predecessor/method` travels through the function signature and is copied into candidate, path, successful-cell, and failed-cell dictionaries. Bundle it into a cell-coordinate type and centralize common row construction.

- `experiments/poc/hcms24_phase3_v1.py:1180-1267` — **Duplicated Code.** Primary and safety execution repeat timeout wrapping, `run_method_cell` invocation, two exception branches, and failed-cell creation; even the timeout/non-timeout handlers duplicate nearly every argument. Extract one execution wrapper returning candidates, paths, and cell status.

- `experiments/poc/hcms24_phase3_v1.py` (file-wide) — **Divergent Change.** The 1,355-line module owns filesystem transaction validation/publication, policy compilation, agent factories, experiment execution, replay/scoring, aggregation, provenance, reporting, and CLI orchestration. These are distinct change reasons; split along those responsibilities while retaining a thin runner.

No judgement-call smells found in `test_hcms24_phase3_v1.py`, `research-log/151-hcms24-poc-implementation.md`, `research-log/progress.md`, or `state.json`.

## Spec

### (a) Missing/partial requirements

- **HIGH — Runtime provenance is incomplete.** The runner executes `evaluation.ops`, attack contracts, guardrail code, and `experiments/mock_agents.py` (`runner:33-40`, `runner:533-584`), but `verify_bindings` emits only the runner/config/hypothesis/design/review/attack and config-listed SDK sources (`runner:995-1012`). Mock-agent source, environment builder, contracts, guardrail implementation, and fixture contents are unbound. This fails the exact-source transaction requirement (`design:58-61`, `hypothesis:324`).

- **HIGH — Scientific outputs cannot independently establish nested attribution or scorer identity.** Generation/replay suffix vectors, qualifying-event evidence, predicates, and traces are computed (`runner:594-633`, `runner:688-703`) but discarded; emitted candidate/path schemas retain only booleans, counts, hashes, and hosts (`runner:79-132`, `runner:808-820`). An auditor cannot verify the required `E_i,s_i` evidence (`hypothesis:181-196`) or five scorer-identity conditions (`hypothesis:324-329`) without rerunning the one-shot experiment.

- **HIGH — Exceptions have no evidence.** Broad catches replace failures with zero-valued placeholder cells (`runner:1204-1228`, `runner:873-911`); no exception type, message, phase, traceback digest, elapsed time, or partial-record evidence is emitted. The batch becomes invalid, but its cause is unauditable.

- **MEDIUM — Transaction integrity is partial.** `run.log` is intentionally excluded from hashes (`runner:297-305`, `runner:1331`); `COMPLETE.json` is published before stdout (`runner:1343-1350`), so a tee-appended log changes afterward. This falls short of command-first, COMPLETE-last auditability (`design:88-91`). `malformed_artifact_count` is also hard-coded zero without reload/schema reconciliation (`runner:1057`).

### (b) Scope creep

- **LOW:** No scientific method/clock/profile/attack scope creep. Administrative log/state files exceed the design’s literal runner-plus-tests implementation list (`design:71-76`) but do not alter the experiment.

### (c) Scientifically wrong implemented-looking behavior

Timing boundaries, shared kernel, endogenous ledger/replay, HCMS/scalar policy equality, Williams checks, safety filtering, and 144-cell enumeration appear aligned. Toy PASS does not resolve the provenance/evidence defects above.

**Verdict: NEEDS_REVISION**

## Main-agent disposition

- Scientific execution remains forbidden; canonical attempt is absent.
- Fix all three HIGHs and the MEDIUM at their owning implementation/tests.
- The standards findings are maintainability coaching, not hard gate failures;
  use a shared execution wrapper where it reduces the exception duplication,
  but do not split the frozen two-file implementation into unreviewed modules.
- Dispatch a fresh targeted re-review of the repaired immutable implementation
  before any scientific command.
