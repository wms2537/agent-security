# AHCMS-24 Phase-3 PoC code/spec review — round 1

**Status:** DONE

**Reviewed object:** committed `HEAD` `ebffcdfad430807e3ef6454361a00e15fee08d2d`

## Files reviewed + total line count

| Review target | HEAD lines |
|---|---:|
| `experiments/poc/ahcms24_phase3_v1.py` | 1,703 |
| `experiments/poc/test_ahcms24_phase3_v1.py` | 716 |
| **Total** | **2,419** |

The normative contract was read from `research-log/181-poc-ahcms24-design.md`
(232 lines), `research-log/178-hypothesis-iter-8-ahcms24-v5.md` (654
lines), and `experiments/configs/ahcms24-c3-v5.json` (230 lines). Source
fidelity was checked against the bound historical generation/replay timer
implementation in `experiments/poc/hcms24_phase3_v1.py`, the bound SDK
predicate/scorer sources, the configured source hashes, and
`experiments/attack.py`. Those are ground truth, not review targets.

## 1. Blind assessment

### Overall: NEEDS_REVISION

### Findings, ordered by severity

#### F1 — HIGH — The inherited point-replay charge excludes reset and reset-checkpoint time

**Review target:** `experiments/poc/ahcms24_phase3_v1.py:570-584`

`capture_generation_arm` constructs the environment at line 570, performs the
`generation_reset` checkpoint, `env.reset()`, and the
`generation_reset_complete` checkpoint at lines 571-573, and only then starts
`calibrated_started_ns` at line 576. The cumulative values later consumed as
`c_1` and `c_returned` are differences from that late start at line 584.

That is not the inherited controller. In the bound historical source,
`experiments/poc/hcms24_phase3_v1.py:1141-1159`, the calibrated point clock
starts immediately after environment construction and before the reset
checkpoint and reset. Historical cumulative point costs at line 1221 therefore
include reset and its checkpoint/controller work. The frozen formula is then
applied to those costs.

**Exact wrong-result mechanism:** every candidate's quarter-nanosecond charge
is systematically under-measured by omitting reset and the reset checkpoints.
The longest-fitting scan itself is arithmetically correct, but it scans against
the wrong ledger. Candidates can be accepted that should be true all-prefix
no-fits; the first absorbing trigger can move or disappear; accepted findings,
tail raw, generation tails, replay elapsed, overages, all eleven metrics, and
the terminal decision can all change. Independent reload cannot catch this:
it faithfully recomputes from the already-corrupted cumulative costs.

#### F2 — HIGH — The exact scientific command is self-reported, not enforced

**Review target:** `experiments/poc/ahcms24_phase3_v1.py:63-67`,
`:278-293`, `:1558-1597`, and `:1694-1699`

The runner validates only the two parsed path values. It never validates the
actual interpreter, `-I` isolation, raw argument tokenization/order, or
`sys.orig_argv`. It then writes the frozen command literal into `run.log` and
`SAMPLING.json` itself.

**Exact wrong-result mechanism:** a run invoked with a different Python,
without `-I`, with reordered/equals-form flags, or through an imported call to
`run_scientific` can publish evidence asserting that the exact frozen command
ran. Interpreter/import-environment differences can change constructed
objects and timings while every recorded source hash and downstream metric
reconstruction still passes. The test at
`experiments/poc/test_ahcms24_phase3_v1.py:251-283` checks the literal and path
validator, not the process invocation.

#### F3 — HIGH — Durable capture staging is destroyed before the last full validation, so late failure loses it

**Review target:** `experiments/poc/ahcms24_phase3_v1.py:1457-1486` and
`:1669-1676`

`retire_capture_staging` deletes every staged arm/replay/manifest and
`capture-progress.json`. `run_scientific` calls it at line 1670 before terminal
log construction/fsync and before the final reload that rechecks live bindings
and the metric log at line 1675.

**Exact wrong-result mechanism:** a log write/fsync error, late source/HEAD
drift, metric-log mismatch, or final reload error produces `FAILURE.json` after
all durable staging has already been deleted. This violates both “retain
staging on failure” and “retire staging only after successful final-bundle
validation,” and removes the independently staged capture evidence needed to
audit the consumed one-use attempt. The tests cover failure before retirement
and success after a provisional reload, but never inject a failure in this late
window (`test_ahcms24_phase3_v1.py:341-370`).

#### F4 — MEDIUM — The one-use attempt directory is not inode-pinned across the transaction

**Review target:** `experiments/poc/ahcms24_phase3_v1.py:1558-1592`, with
later path reopens at `:1249-1267`, `:1328-1343`, and `:1662-1676`

Creation uses safe descriptor-relative `mkdir` and `run.log` creation, but the
attempt descriptor is closed. All later stages reopen the pathname without
comparing device/inode identity to the directory originally created.

**Exact wrong-result mechanism:** a concurrent rename/replacement of the
canonical attempt directory after creation can redirect sampling, staging,
reload, log, or COMPLETE publication to a substituted directory. Static
pre-existing/symlink checks cannot detect a post-creation swap, so a
same-path-but-different transaction can reach hashes or COMPLETE. The test at
`test_ahcms24_phase3_v1.py:628-652` covers only pre-existing, dangling, and
static symlink cases.

### Hunt checklist

1. **Data leakage — PASS.** `draw_sampling` fixes masters/unit order/arm orders
   before capture (`ahcms24_phase3_v1.py:257-293`); the child config contract is
   exactly profiles/path cap/prefix support and contains no method label
   (`:655-666`, `:730-736`). No outcome-derived threshold, exclusion, redraw,
   profile, order, or method identity enters capture.

2. **Split hygiene — PASS.** Validation requires the 3-by-3 unit grid, three
   unique masters per profile, exact unit permutation, and all 16 independent
   arm permutations (`:296-321`). `validate_captured_unit_rows` requires 48
   arms in sampled order and the exact replay occurrence sequence (`:1270-1307`);
   `project_all` requires the exact `9 x 16 x 3` arm grid and exact all-prefix
   replay set (`:808-836`). Every projection consumes that shared table.

3. **Metric implementation — ISSUE (F1).** The projection scan is correctly
   longest-to-shortest with exact `5*c_returned + 25*c_1 <= 4*budget`, true
   all-prefix no-fit returns zero, HCMS/fixed8 transition to state 1, fixed24
   remains 24, and fixed24 never salvages (`:802-940`). Set-aware per-unit raw,
   strict overages, integer cross-products, zero branches, floor-half tail,
   retention, simple materiality/Pareto, and eleven metric order are correctly
   implemented (`:970-1096`). The generation/replay elapsed brackets themselves
   retain the frozen start/end and inclusion scope, but the point-ledger inputs
   are not the inherited measurement, so correct downstream algebra cannot
   validate the result.

4. **Train/eval separation — PASS.** Scientific capture completes all arms and
   all exact-prefix replay occurrences in spawned, method-blind children before
   `project_all` runs (`:655-727`, `:1390-1404`). Projection does not call a
   factory or capture function. Disk reload independently reconstructs arms,
   replays, paths, accepted sequences, method units, metrics, and decisions
   (`:1407-1454`).

5. **Baseline fairness — ISSUE (F1).** The primary policies are identical except
   `absorb` and shared-prefix rows/accepted occurrences are explicitly compared
   (`:419-424`, `:949-966`). Fixed8 and fixed24 transition/salvage code is correct.
   Nevertheless both primary policies are projections of a non-inherited point
   ledger, so this is not the frozen AHCMS-versus-retry comparison even though
   internal pairing is fair.

6. **Seed handling — PASS.** Masters use the required rejection domain; the
   Fisher–Yates implementation consumes one unbiased injected `randbelow(i+1)`
   per swap; master, unit, and arm draws occur once; and every generation/replay
   environment seed reconstructs to its unit master (`:229-293`, `:750-799`).
   No failure/outcome retry or redraw exists.

7. **Logged metrics provenance — ISSUE (F2, F3, F4).** The semantic reload and
   exact-set/hash-bound COMPLETE validation are strong (`:1407-1454`,
   `:1518-1555`), and metric lines are derived from reloaded metrics. However the
   command provenance is fabricated from a constant, late failure can occur
   after staging destruction, and pathname replacement is not excluded. Those
   gaps allow false invocation identity or loss/redirection of the one-use
   evidence transaction to survive otherwise self-consistent validation.

### Explicit required dispositions

| Required point | Disposition |
|---|---|
| Source timer landmark fidelity | **PASS:** generation starts before the environment checkpoint and ends after the interaction loop/final complete checkpoint before flags; replay has the corresponding pre-construction/post-loop-before-final-trace bracket. Checkpoint serialization, construction/reset, trace exports, interactions, and in-bracket scheduling remain between the reads. F1 is a separate inherited point-charge clock defect. |
| All-prefix replay support | **PASS:** every exact eligible prefix of every arm has one replay, with exact-set and duplicate rejection. |
| Longest-fitting ledger semantics | **ISSUE:** scan/order/inequality are correct, but the charged `c` values omit reset/checkpoint time (F1). |
| State-1 true-no-fit transition | **PASS:** zero returned prefix transitions inherited/fixed8 state to 1; fixed24 remains 24. |
| Full per-unit scoring | **PASS:** one bound set-aware scorer call per complete method-unit sequence per reconstruction; units are never merged. |
| Durable per-unit staging and failure retention | **ISSUE:** per-unit commits are durable and ordered, but late failures occur after staging deletion (F3). |
| Staged-to-final equality | **PASS:** final arms, replays, and checkpoint manifests are compared exactly to independently reloaded staging before retirement. |
| Exact eleven-metric logging | **PASS:** exact names/order, numerator/denominator/value/pass fields, terminal values, and disk-log reconciliation are enforced. |
| One-use transaction safety | **ISSUE:** atomic initial creation/refusal is good, but exact invocation is not enforced and directory identity is not pinned (F2, F4). |
| Child timeout/survivor handling | **PASS:** bounded queue wait, terminate-then-kill, joined exit, and survivor assertion fail closed (`:682-727`). |
| Canonical-attempt absence | **PASS:** absent before review, after tests, and after report creation checks; no canonical command ran. |
| Would tests catch the strongest bug? | **NO:** the strongest bug is F1. Synthetic tables inject `cumulative_costs_ns` directly and the timer test exercises replay/marker order only; no fake clock/reset test checks the cumulative-cost start boundary. |

The strongest potential issue considered but cleared was whether the offline
primary projections could diverge before the absorbing event. They cannot under
the stored-table implementation: policy dictionaries differ only in `absorb`,
and exact normalized path and accepted-occurrence prefix equality is checked per
unit at `ahcms24_phase3_v1.py:949-966`. That protection does not clear F1,
because both projections can still share the same wrong inherited ledger.

## 2. Actionable coaching

### F1 fix and structural invariant

Start the calibrated point clock immediately after `env_builder` returns and
before the `generation_reset` checkpoint, exactly as the bound historical
source does. Keep cumulative samples at the same post-interaction/pre-complete-
checkpoint landmark. Add an injected fake-clock/fake-env test in which reset and
both reset checkpoints advance distinguishable amounts; assert `c_1` includes
them and that a candidate flips from equality-fit to one-quarter-nanosecond
no-fit at the expected boundary.

### F2 fix and structural invariant

Fail before attempt creation unless the process invocation matches the frozen
token vector, `sys.flags.isolated == 1`, and `sys.executable` resolves to the
bound `comp/.venv/bin/python` inode/path. Prefer a command-first `run.log`
created by a tiny bound launcher that records and validates its actual argv;
the scientific runner must verify, not invent, that first line. Add negative
subprocess tests for missing `-I`, alternate interpreter, reordered flags,
equals-form flags, and direct imported calls.

### F3 fix and structural invariant

Append/fsync the terminal log, verify live bindings/code, reload every final
artifact, recompute all endpoints, validate the metric log, and compare final
capture rows to staging before any staging deletion. Preserve a durable recovery
copy or atomically quarantined staging object until COMPLETE publication is
known durable if “retain on any failure” is literal. Inject failures at log
write, fsync, live-binding verification, final reload, retirement, and COMPLETE
publication; every pre-COMPLETE failure must leave the staged rows/manifests
recoverable.

### F4 fix and structural invariant

Keep the originally created attempt directory descriptor open for the entire
transaction and perform all reads/writes/listing/retirement/publication with
descriptor-relative `openat` operations. Record its `(st_dev, st_ino)` and
recheck the canonical parent entry before COMPLETE publication. Add a temp-path
test that renames/replaces the attempt directory immediately after creation;
the next operation must fail without publishing into either replacement.

## Commands run and concise outputs

All repository reads were read-only and, for the review targets/contract, were
against `HEAD` via `git show`.

```text
git status --short
  -> no output before review or before report creation

git rev-parse HEAD
  -> ebffcdfad430807e3ef6454361a00e15fee08d2d

if [ -e experiments/runs/ahcms24-c3-poc-v1 ] || [ -L experiments/runs/ahcms24-c3-poc-v1 ]; then stat -c '%F %n' experiments/runs/ahcms24-c3-poc-v1; else echo 'CANONICAL_ATTEMPT_ABSENT'; fi
  -> CANONICAL_ATTEMPT_ABSENT

wc -l experiments/poc/ahcms24_phase3_v1.py experiments/poc/test_ahcms24_phase3_v1.py research-log/181-poc-ahcms24-design.md research-log/178-hypothesis-iter-8-ahcms24-v5.md experiments/configs/ahcms24-c3-v5.json
  -> 1703, 716, 232, 654, 230; total 3535

git ls-tree HEAD -- experiments/poc/ahcms24_phase3_v1.py experiments/poc/test_ahcms24_phase3_v1.py research-log/181-poc-ahcms24-design.md research-log/178-hypothesis-iter-8-ahcms24-v5.md experiments/configs/ahcms24-c3-v5.json
  -> all five are regular HEAD blobs

git show HEAD:experiments/configs/ahcms24-c3-v5.json
git show HEAD:research-log/181-poc-ahcms24-design.md | nl -ba
git show HEAD:research-log/178-hypothesis-iter-8-ahcms24-v5.md | nl -ba | sed -n '1,220p'
git show HEAD:research-log/178-hypothesis-iter-8-ahcms24-v5.md | nl -ba | sed -n '221,440p'
git show HEAD:research-log/178-hypothesis-iter-8-ahcms24-v5.md | nl -ba | sed -n '441,700p'
git show HEAD:research-log/178-hypothesis-iter-8-ahcms24-v5.md | nl -ba | sed -n '300,440p'
  -> complete normative contract read; the last command re-read an output-truncated overlap

git show HEAD:experiments/poc/ahcms24_phase3_v1.py | nl -ba | sed -n '<range>p'
  -> complete target read using ranges 1-260, 261-520, 521-780, 781-1040,
     840-970, 970-1160, 1150-1360, 1347-1510, 1488-1720, and 1561-1800;
     overlaps re-read tool-truncated sections

git show HEAD:experiments/poc/test_ahcms24_phase3_v1.py | nl -ba | sed -n '<range>p'
  -> complete target read using ranges 1-200, 201-400, 340-470, 401-600, 601-760

wc -l experiments/poc/hcms24_phase3_v1.py experiments/attack.py comp/sdk/aicomp_sdk/core/predicates.py comp/sdk/aicomp_sdk/scoring.py comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py comp/sdk/kaggle_evaluation/jed_attack_134815/remote_env.py comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_inference_server.py
  -> 2955, 493, 390, 168, 849, 176, 252

git show HEAD:experiments/poc/hcms24_phase3_v1.py | nl -ba | sed -n '900,1045p'
git show HEAD:experiments/poc/hcms24_phase3_v1.py | nl -ba | sed -n '1080,1285p'
git show HEAD:experiments/poc/hcms24_phase3_v1.py | nl -ba | sed -n '1286,1505p'
git show HEAD:experiments/poc/hcms24_phase3_v1.py | nl -ba | sed -n '650,690p'
  -> historical generation/replay brackets, point clock, and checkpoint serialization read

git show HEAD:experiments/attack.py | nl -ba | sed -n '1,250p'
git show HEAD:experiments/attack.py | nl -ba | sed -n '251,520p'
git show HEAD:comp/sdk/aicomp_sdk/scoring.py | nl -ba
git show HEAD:comp/sdk/aicomp_sdk/core/predicates.py | nl -ba | sed -n '1,390p'
  -> attack and bound set-aware scorer/predicate sources read in full

sha256sum experiments/poc/hcms24_phase3_v1.py experiments/attack.py comp/sdk/aicomp_sdk/core/predicates.py comp/sdk/aicomp_sdk/scoring.py comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py comp/sdk/kaggle_evaluation/jed_attack_134815/remote_env.py comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_inference_server.py
  -> every digest matched the frozen config/expanded historical bindings

sha256sum research-log/181-poc-ahcms24-design.md research-log/178-hypothesis-iter-8-ahcms24-v5.md experiments/configs/ahcms24-c3-v5.json research-log/180-ahcms24-v5-theory-review-round-12.md experiments/poc/ahcms24_phase2_reference_v5.py experiments/poc/ahcms24_round11_timer_audit.py results.tsv
  -> every digest matched the runner's frozen identity table

rg -n '^ahcms24-c3-poc-v1\t' results.tsv && head -1 results.tsv
  -> exactly eleven preregistered rows, in the runner's metric order

PYTHONDONTWRITEBYTECODE=1 comp/.venv/bin/python -c "from pathlib import Path; [compile(Path(p).read_text(encoding='utf-8'), p, 'exec') for p in ('experiments/poc/ahcms24_phase3_v1.py','experiments/poc/test_ahcms24_phase3_v1.py')]; print('STATIC_COMPILE_OK 2')"
  -> STATIC_COMPILE_OK 2

PYTHONDONTWRITEBYTECODE=1 comp/.venv/bin/python -I experiments/poc/test_ahcms24_phase3_v1.py
  -> Ran 23 tests in 24.403s; OK

if [ -e experiments/runs/ahcms24-c3-poc-v1 ] || [ -L experiments/runs/ahcms24-c3-poc-v1 ]; then stat -c '%F %n' experiments/runs/ahcms24-c3-poc-v1; else echo 'CANONICAL_ATTEMPT_ABSENT_AFTER_TESTS'; fi
  -> CANONICAL_ATTEMPT_ABSENT_AFTER_TESTS
```

## Scientific-action and absence statement

The canonical attempt path was absent before review and remained absent after
the permitted synthetic tests. No scientific command was run; no fresh
scientific master was sampled; none of the three scientific environments was
constructed; no target service, Kaggle, network, provider, submission, attack
mutation, or other scientific action occurred. The only filesystem change made
by this review is this report.
