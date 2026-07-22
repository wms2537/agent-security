# AHCMS-24 Phase-3 PoC repair design

**Date:** 2026-07-23 · **Phase:** 3 · **Cycle:** 3 · **Iteration:** 3 · **Status:** frozen design, waiting at correction budget

## Context

Sterile report 183 and main-agent audit 184 reproduce four pre-execution
defects in the committed AHCMS-24 runner: the inherited point clock starts too
late, actual process invocation is not authenticated, durable staging is
deleted before all late failures close, and the attempt directory is not pinned
against replacement. The canonical attempt is still absent and scientific debug
remains `0/3`.

This entry freezes the repair architecture and adversarial tests without
changing either implementation file. It is non-committal work permitted while
T062 waits at the exhausted `2/2` implementation-correction gate. It does not
raise that gate, spend correction attempt 3, or authorize execution.

## Decision alternatives

The SciAgent candidate rubric is applied before selection. Scores are
`impact x feasibility / complexity`, each input on 1--5; a high numerical score
cannot override a failed validity gate.

| Candidate | Likely failure mode | Hardest implementation trap | Evidence check | I/F/C | Score | Decision |
|---|---|---|---|---:|---:|---|
| Minimal assertions around the current path-based runner | Leaves time-of-check/time-of-use windows and can still destroy recovery evidence | Mistaking repeated `lstat` checks for descriptor ownership | F3/F4 require lifetime and recovery closure, not another static precheck | 3/5/2 | 7.5 | Reject: fails the evidence gate despite low complexity |
| Reuse the whole ORF staged-directory publisher | A crash before final rename leaves the canonical AHCMS attempt absent and makes an outcome-driven retry possible | Reconciling hidden staging, one-use identity and failure publication | `experiments/orf_bundle.py` is strong for final publication but its canonical path appears only at completion | 5/2/5 | 2.0 | Reject: conflicts with “crash consumes canonical attempt” |
| Stable canonical descriptor plus permanent per-unit capture journal | A partial descriptor migration could leave one path-based escape hatch | Converting every attempt read/write/verify operation and testing replacement at every boundary | Directly closes F1--F4 while preserving the frozen attempt and scientific contract | 5/4/4 | 5.0 | **Select if correction budget is extended** |
| Retire AHCMS and spend the last research iteration on a new strategy | Loses the only current source-profiled structural mechanism without scientific evidence against it | Finding a genuinely new dimension rather than renaming the same retry-tail policy | Current evidence defeats implementation, not the AHCMS scientific premise | 3/2/4 | 1.5 | Fallback only if extension is denied |
| Run the current code | Produces a self-consistent but source-wrong result | None; it is merely unsafe | Reports 183--184 directly contradict admissibility | 1/1/5 | 0.2 | Forbidden |

The selected repair is preferable to a pivot because the active hypothesis has
not been scientifically refuted and every blocker has a concrete local owner.
The minimal-assertion option is easier but does not close the mechanism.

## Local mechanisms reused

The design borrows mechanisms, not scientific results, from four committed
local sources:

```text
experiments/orf_bundle.py             605 lines  sha256 8c4b9cd3bf4ea0053e96a851b88a60bb6a92972b2e7f8a6e3a4c6bd91550aedd
experiments/test_orf_bundle.py        366 lines  sha256 9c79599f7cd6f4803379402b623bd8ba39a0980d12b635688e1c5be8ca449fef
experiments/orf-p4-core/run_core.py   742 lines  sha256 41aa108f5f18c60a7072666d32fe010b447a1617c7c5938a1f54573b01e74715
experiments/omst_c2_v9_fixture.py     456 lines  sha256 e9e95741cd306d0aa11456f0977b4e129654653a24a00669fe9aa58e47e20284
```

Useful patterns are exact isolated `sys.argv` validation, interpreter
link/target/hash authentication, `(st_dev, st_ino)` equality around descriptor
reads, exact no-follow file identity, no-replace publication, and injected
failure tests at every structural boundary. `orf_bundle.py` is not imported or
copied wholesale because its delayed canonical-directory publication conflicts
with the frozen AHCMS one-use rule.

The exact current interpreter facts, gathered without the scientific runner,
are:

```text
command link     /home/soh/agent-security/comp/.venv/bin/python
link target      python3.14
resolved target  /home/linuxbrew/.linuxbrew/Cellar/python@3.14/3.14.3_1/bin/python3.14
target sha256    eca90b668424db6f2105504128f02cac91c2805de9a928abcc272d1444abfde0
isolated probe   sys.flags.isolated == 1
```

These are process-provenance bindings, not scientific choices. Drift must fail
before canonical attempt creation.

## Repair architecture

### R1 — authenticate the actual process before any attempt entry exists

Add one pure `ProcessIdentity` validator, called as the first operation of both
`main` and `run_scientific`. It must require all of the following:

1. repository root is the exact current working directory;
2. `sys.flags.isolated == 1`;
3. `sys.argv` is exactly the runner plus the two ordered flag/value pairs;
4. `sys.orig_argv` is exactly the frozen interpreter token, `-I`, runner token,
   and ordered arguments, with no equals form, extra token or wrapper;
5. `sys.executable` is the exact absolute command link;
6. its resolved target, link target, interpreter version and target SHA match
   committed constants; and
7. a final live-process check repeats before COMPLETE.

The command-first log line must be reconstructed from the already-validated
actual tokens and byte-equal `EXPECTED_COMMAND`; it may not be invented from an
unchecked literal. `SAMPLING.json`, bindings and COMPLETE must retain the full
process-identity record. A direct imported call therefore fails before any
directory, sampling, master or scientific environment exists.

### R2 — restore the inherited point-clock landmark

In `capture_generation_arm`, read the calibrated point-clock origin immediately
after `env_builder` returns and before the `generation_reset` checkpoint. Keep
the overall `g_ns` start before `generation_environment_construction` and its
existing end after the interaction loop. Keep each cumulative sample after its
interaction trace export and before `generation_interaction_complete`, exactly
as in the bound historical runner.

Inject the monotonic-ns clock and checkpoint writer into the capture function.
A deterministic fake clock must prove that environment construction is excluded
from `c_k`, both reset checkpoints and reset are included, and interaction/trace
costs are included. Add an AST/source binding for the point-clock ordering in
addition to the existing generation/replay elapsed timer bindings. The bound
historical source at SHA
`7b030c67a7f18c4bce77db67f7db757b817aede7cbaf75aa1195a09d42f6b1f6`
is normative.

### R3 — one stable descriptor-owned attempt transaction

Create an `AttemptTransaction` before sampling that retains, until final return:

- repository, `experiments`, and `runs` directory descriptors;
- the newly created canonical attempt descriptor;
- the attempt's `(st_dev, st_ino)` and its exact parent-entry name;
- process identity and initial live bindings; and
- a `complete_published` state bit.

Every attempt artifact operation must be descriptor-relative: exclusive writes,
atomic progress replacement, JSON/JSONL reads, hashes, directory listing,
regular-file checks, failure record, run-log append, recovery reads and COMPLETE
publication. Production code may not reopen the attempt by pathname. Before and
after every high-level boundary, compare `fstat(attempt_fd)` with
`stat(attempt_name, dir_fd=runs_fd, follow_symlinks=False)`. Replacement,
renaming, symlinking, unlinking or type drift fails without writing to the
replacement. File reads also compare opened and named `(st_dev, st_ino, size,
mtime, ctime)` before accepting bytes.

Spawned scientific children never receive these descriptors; only the parent
owns evidence publication. Python descriptors remain non-inheritable and the
child still receives only the method-blind capture contract.

### R4 — make per-unit staging permanent final evidence

Eliminate the delete-before-COMPLETE lifecycle. Each completed unit is durably
written directly into three fixed top-level journal artifacts keyed only by
capture index:

```text
capture-unit-00.generation.jsonl
capture-unit-00.replay.jsonl
capture-unit-00.manifest.json
...
capture-unit-08.generation.jsonl
capture-unit-08.replay.jsonl
capture-unit-08.manifest.json
```

The manifest binds the sampled unit ID, capture index, counts, exact coordinate
support and hashes. `capture-progress.json` is also permanent evidence. Final
consolidated tables are rebuilt only from independently reloaded unit journals,
then compared back to every journal byte/count/hash. All 28 journal/progress
artifacts become declared, hash-bound COMPLETE artifacts; none is retired or
deleted. Thus every pre-COMPLETE failure retains the completed capture prefix,
and a successful bundle is self-contained with the original per-unit evidence.

This is an evidence-format repair only. It changes no master, arm, trace,
method, projection, scorer, threshold, metric or decision.

## Exact production order

The repaired runner must enforce this order:

1. authenticate actual process and committed runner;
2. create and retain the canonical transaction descriptors;
3. recheck source/process bindings and write the actual command-first log;
4. draw once and fsync `SAMPLING.json`;
5. capture each method-blind unit and fsync its three permanent journal files,
   then atomically advance permanent progress;
6. reload every unit journal through the stable descriptor;
7. build consolidated evidence and deterministic projections;
8. independently reload journals and all final tables and recompute projections,
   per-unit set-aware raw, eleven metrics and decision;
9. construct and fsync terminal metric lines;
10. repeat process, source, runner, named-inode and metric-log checks;
11. publish and fsync exact-set/hash-bound COMPLETE last through the stable
    descriptor;
12. independently validate COMPLETE, all hashes, exact directory contents and
    parent-entry identity, then print the already-hashed lines and return zero.

Any exception before step 11 writes `FAILURE.json` and an invalid log line
through the original descriptor when possible, retains all unit journals, and
never publishes COMPLETE. An exception after a durable COMPLETE is not allowed
to rewrite or relabel the scientific bundle.

## Adversarial test contract

All current 23 tests remain mandatory. The repair adds at least these tests,
using injected clocks, metadata and temporary directories only:

1. **Point clock:** distinguish construction, both reset checkpoints, reset,
   trace export and interaction increments; assert exact `c_1` and
   `c_returned`; assert exact fit versus one-quarter-nanosecond no-fit.
2. **Point AST:** calibrated origin is after environment construction and before
   reset checkpoint; cumulative sample remains before completed checkpoint.
3. **Invocation matrix:** accept one synthetic exact process record; reject
   missing `-I`, alternate interpreter, changed target/hash/version, wrong cwd,
   reordered flags, equals-form flags, extra tokens, changed `sys.argv`, changed
   `sys.orig_argv`, and direct imported `run_scientific` before attempt creation.
4. **Stable inode:** after creation rename the original attempt and install a
   replacement directory/symlink/file; the next operation fails, replacement is
   byte-untouched, displaced original retains its evidence, and no COMPLETE is
   written.
5. **Stable file reads:** replace a journal between open/read/name check and
   require rejection.
6. **Permanent capture prefix:** inject failure after every unit journal write,
   progress update, consolidated artifact, log append, live-binding check,
   semantic reload, COMPLETE write and fsync boundary. Every pre-COMPLETE case
   has no valid COMPLETE and retains exactly the durable completed-unit prefix.
7. **Successful exact set:** all 27 unit files plus progress are present in the
   COMPLETE artifact map and independently reconstruct byte-identical final
   arms/replays/checkpoints.
8. **Journal tamper:** mutation, missing file, extra journal, reordered capture,
   wrong unit binding, duplicate coordinate, symlink and nonregular entry all
   fail reload or COMPLETE verification.
9. **Late binding drift:** process, runner, source or ledger drift after capture
   but before COMPLETE fails while journals remain.
10. **Scientific tripwire:** the full test suite cannot construct a scientific
    environment, draw a fresh scientific master, create the canonical attempt,
    contact a target, or perform Kaggle/network action.

No synthetic assertion may substitute for a fresh sterile source/spec review.

## Component roles and removal checks

These safeguards receive no AHCMS scientific contribution credit. Each exists
only because a measured review defect requires it:

| Safeguard | Sole role | Removal consequence |
|---|---|---|
| Process identity | Prove the recorded command/interpreter actually ran | Recreates F2 |
| Historical point-clock binding | Make ledger decisions source-faithful | Recreates F1 |
| Descriptor transaction | Keep one-use evidence on the created inode | Recreates F4 |
| Permanent unit journal | Preserve independently captured evidence through every failure | Recreates F3 |

No additional controller, heuristic, fallback, threshold or candidate arm is
introduced. This is repair engineering, not a method stack.

## Verification command

The design gate must return exactly one PASS line after checking the four
finding-to-repair mappings, three architecture alternatives, ten adversarial
test classes, permanent 27-file unit journal, process binding, descriptor
identity, immutable-input hashes and canonical-attempt absence.

## Budget and authorization boundary

The preferred repair remains blocked by the recorded `2/2`
implementation-correction limit. This design does not interpret the persistent
goal, Kaggle authorization, or hypothesis-review extension as permission to
change that number. Explicit user authorization to raise the limit from 2 to 4
is still required before either implementation file can change.

If the same missing authorization recurs for a third consecutive goal turn and
no further meaningful non-mutating work remains, the active goal meets the
strict blocked-audit threshold. Until then, T062 remains in progress and the
canonical command remains closed.

## Problem alignment

This design makes the controlled evidence source-faithful and audit-preserving
before it can influence the competition system. It advances mechanical
correctness, resource evidence and regression safety while explicitly retaining
the separate Kaggle target-derived and submission-confidence gates.

## Decision

Freeze the stable-descriptor/permanent-journal repair contract. Do not implement
or run it without the correction-limit extension. If extended, one cohesive
repair must address F1--F4 and receive a new sterile review before any science.

## Next Steps

1. Record explicit user authorization raising implementation corrections 2 to
   4, or retire the implementation and pivot.
2. If authorized, implement only this frozen repair and its adversarial tests.
3. Commit the unexecuted repair and dispatch a fresh sterile round-2 review.
