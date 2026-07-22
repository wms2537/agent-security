# Phase-3 PoC implementation — AHCMS-24

**Date:** 2026-07-22 · **Phase:** 3 · **Task:** T060 · **Run ID:** `ahcms24-c3-poc-v1` · **Status:** implemented and unexecuted

## Outcome

The one-use AHCMS-24 matched-trace runner and its synthetic/adversarial test
surface are implemented against the frozen report-181 design. No scientific
environment was constructed, no master or arm order was sampled, no canonical
attempt directory was created, and no Kaggle action occurred.

The implementation identities before commit are:

```text
experiments/poc/ahcms24_phase3_v1.py
  lines   1703
  sha256  bfeaed3b6147cd889901a274bcf2505048171a3e811052e2d4dabfc356a0a501
experiments/poc/test_ahcms24_phase3_v1.py
  lines   716
  sha256  9e29043b6746fed0b4f47ed3d2f4004c2e74e6bb559e2c122bb2cce3729e1cd3
preregistration commit
  12c303dcc1560ba5fc32e6508a5eb2605642bda4
report 181 sha256
  297370408b0f5af0ec44ae10e2295bfb594b6285c5397150db17ff0813e47055
```

## Implemented contract

The runner captures nine fresh units, three per controlled profile. For every
unit it captures all 16 slots and all three generation arms (`24`, `8`, `1`) in
the preregistered random order, giving 432 generation arms. Each arm exposes
every exact eligible prefix, and each exact eligible prefix receives a separate
source-authentic replay occurrence. Capture children receive profiles, the path
cap, and prefix support only; evaluated method labels are absent.

Four deterministic projections consume that complete potential table:
AHCMS absorbing, retry HCMS, fixed8 absorbing, and fixed24/no-salvage
absorbing. The inherited controller scans permitted exact prefixes from longest
to shortest and selects the first whose exact quarter-nanosecond replay charge
fits the cumulative ledger. A true all-prefix no-fit returns zero and changes
state to one; AHCMS and the absorbing simple control terminate, while retry HCMS
may propose the next state-one path. Fixed24 never salvages to a shorter arm.

The historical generation and replay `monotonic_ns` landmarks are checked from
source AST order. Set-aware raw is scored once over each complete accepted
method-unit finding sequence. Aggregate rules use integer cross-products,
explicit zero-denominator branches, exact floor-half tail elapsed, the frozen
simple-control feasibility/Pareto rules, and exactly the eleven preregistered
ledger metrics.

## Durable one-use evidence path

`SAMPLING.json` is written and fsynced before capture. Every completed unit is
then written to `capture-staging/` as canonical generation rows, replay rows,
and a bound manifest. The implementation validates exact capture coordinates,
arm order, replay support, schema, counts, hashes, regular-file status, absence
of extra entries, and capture-prefix order. A killed or failed attempt retains
these per-unit records.

Final tables are built from independently reloaded staged records, not trusted
in-memory child results. The complete bundle is independently reconstructed and
compared with staging before staging and progress are retired. The command-first
log is fsynced, its eleven metric lines are reloaded and checked, and only then
is the exact-set/hash-bound `COMPLETE.json` atomically published last. Existing,
symlinked, dangling, malformed, or uncommitted-code attempts fail closed.

## Corrections made before sealing

Two implementation corrections were required and consumed the full `2/2`
implementation-correction allowance:

1. The first draft represented only one longest exact prefix and tested one
   ledger charge. It was corrected to retain every eligible exact prefix, replay
   every occurrence, implement longest-fitting ledger salvage, enforce the
   state-one true-no-fit transition, and emit the exact eleven frozen metrics.
2. The next draft retained only in-memory child rows plus counts/hashes. It was
   corrected to durably stage complete per-unit arm/replay rows and manifests,
   independently reload them in capture order, retain them on failure, and
   retire them only after final-bundle reconstruction succeeds.

No third correction was used. The scientific debug allowance remains `0/3`.

## Main-agent verification

The independent structural/ledger audit returned:

```text
ahcms24_phase3_implementation_check=PASS ledger_metrics=11 fixed_bindings=117 policies=4 generation_arms=432 canonical_attempt_absent=true publication_order=PASS method_blind_capture=PASS results_immutable=PASS attack_immutable=PASS
```

Static compilation returned:

```text
ahcms24_static_compile=PASS
```

The pure synthetic and adversarial suite returned:

```text
Ran 23 tests in 28.771s
OK
canonical_attempt_absent=true
```

Coverage includes exact path/replay grids, full-prefix salvage, fixed24
no-salvage, equality/just-over ledger admission, state-one absorption,
non-absorption prefix equality, set-aware scoring, tail/retention and all zero
branches, simple-control Pareto logic, strict two-second boundaries, historical
timer landmarks, immutable bindings, lexical attempt identity, symlink and
tamper rejection, double-buffer checkpoints, per-unit staging survival and
retirement, semantic reconstruction, metric logging, and `COMPLETE`-last hashes.
A tripwire makes any scientific factory or capture call fail the test suite.

The frozen data identities remain:

```text
results.tsv sha256          f485fdb8a6dbca61e2578009df0b0624b2bd09dabc3f2604d80fe1a6c9448afa
experiments/attack.py sha256 8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d
```

## Gate and next task

T060 is complete as an implementation task only. There is still no fresh
scientific result to confirm or disconfirm the hypothesis. The exact canonical
command remains forbidden until a separate sterile source/specification review
of the committed files returns `SOUND`:

```text
comp/.venv/bin/python -I experiments/poc/ahcms24_phase3_v1.py --config experiments/configs/ahcms24-c3-v5.json --attempt-dir experiments/runs/ahcms24-c3-poc-v1
```

T061 must inspect the committed runner and tests against immutable v5 and report
181, including timer landmarks, eligible-prefix support, longest-fitting ledger
semantics, the state-one no-fit transition, independent reconstruction, durable
staging, eleven-metric logging, and one-use publication. No scientific or
Kaggle action is authorized by this implementation record.
