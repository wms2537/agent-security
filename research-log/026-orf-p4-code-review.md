# ORF Phase-4 baseline + core code review

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** NEEDS_REVISION

## Reviewer report (verbatim)

Status: DONE

Files reviewed:

- `experiments/orf-p4-baseline/run_baseline.py`: 395 lines
- `experiments/orf-p4-core/run_core.py`: 684 lines
- `experiments/orf-p4-core/test_toy_core.py`: 58 lines
- Total code: 1,137 lines

Evidence reviewed:

- `score-tables.tsv`: 961 lines
- `aggregate-by-length.tsv`: 22 lines
- `baseline-summary.json`: 1 line
- `run.log`: 10 lines

Toy-only tests passed: 4/4. The primary core was not executed or aggregated.

## 1. Blind Assessment

### 1. Data leakage — PASS

The primary labels are the three exact public preimages in
`run_baseline.py:28-32` and `run_core.py:39-43`. Their SHA-256 masters are derived
directly at `run_baseline.py:210-212` and checked again at
`run_core.py:312-328`.

No tuning labels enter the validation computation. No network, beacon, Kaggle,
subprocess, or held-out generation/evaluation path exists. The held-out fixtures
are only hashed by the baseline; their contents do not influence scores or action
selection.

### 2. Split hygiene — PASS

`run_core.py:286-339` requires exactly 960 ordered rows partitioned as three
masters × 320 profiles, with exact master, profile, stratum, replicate, and
digest values. Extra, missing, reordered, or substituted rows fail.

The validation domain `orf-public-phase4-v1` is distinct from the tuning
generator's `orf-nontarget-calibration-v1` domain. The test-tier target is
untouched.

### 3. Metric implementation — PASS

Exact mechanics are correct:

- Smaller-length tie-breaking: `run_core.py:110-113`
- Nonempty, seven-action, nonnegative-integer validation: `run_core.py:120-142`
- `A`, `G`, regret, and exact Fraction gain: `run_core.py:125-153`
- Mean of the three per-master gains: `run_core.py:535-545`
- Inclusive 5% materiality: `run_core.py:544-545`
- Homogeneous zero-regret, global `m=1`, and every adaptive `m=1`:
  `run_core.py:342-378`
- Conditional interval is explicitly labeled non-population:
  `run_core.py:607-615`

The baseline independently exhausts all seven lengths and selects smaller `m`
on ties at `run_baseline.py:247-267`. Its log and summary agree on mean, extrema,
selected-length fraction, 6,720/6,720 mechanical matches, and row counts.

### 4. Train/eval separation — PASS

There is no training. The core consumes only the frozen seven-score rows and
changes only action scope: per-profile argmax versus per-master global argmax. It
never regenerates primary profiles or consumes the baseline's reported
aggregate.

### 5. Baseline fairness — PASS

The core pins the exact committed 320×7 tables at `run_core.py:506-513`. Both
policies therefore use identical profiles, scores, action set, resources, and
tie rules. The global comparator is recomputed from score columns rather than
trusted from the baseline summary.

Exhaustive evaluation of all seven lengths gives tuning parity; no baseline
hyperparameter remains unsearched.

### 6. Seed handling — PASS

Primary SHA labels, profile ordering, and digests are exact. The complete
baseline table is pinned to SHA-256 `331e8b5e...e59cbf`.

Homogeneous controls use exactly:

- `preimage + "|homogeneous"` at `run_core.py:353-355`
- `negative|profile={profile:02d}` at `run_core.py:357-359`
- LogUniform `[5,12]`, `a=d=0`, `c(m)=bm`, `e(m)=m`

There is no outcome-dependent replacement or resampling.

### 7. Logged-metric provenance — ISSUE

**HIGH — stale or partial evidence can survive a failed invocation.**

- `run_baseline.py:339-380`
- `run_core.py:487-499`
- `run_core.py:644-664`

Both runners write canonical evidence files directly into reusable directories,
sequentially, without a fresh-attempt boundary, transactional publication, or
final completion manifest.

Exact failure mechanism:

1. A previous run leaves apparently valid summary/TSV artifacts.
2. A later invocation fails during input validation, before any write, or midway
   through sequential writes.
3. Old artifacts—or a mixture of old and new artifacts—remain at the canonical
   paths.
4. A downstream consumer reading the summary or TSVs can attribute those results
   to the failed/current invocation despite no valid completed evidence bundle.

The current baseline files are internally consistent; I found no evidence that
this happened in the existing run. The code nevertheless permits it structurally,
and the contract explicitly requires that outputs not survive failure in a
misleading valid form.

### Strongest potential non-issue considered

`parse_baseline_tables()` does not recompute scores from the cost/event columns.
This is not presently a substitution vulnerability because the entire table is
SHA-pinned, the baseline generated costs/events/scores together, and
`run_baseline.py:221-229` checked all 6,720 cells against a separately implemented
exact score calculation. The core intentionally recomputes `G` from score
columns instead of trusting an aggregate.

Overall: **NEEDS_REVISION**

## 2. Actionable Coaching

For the HIGH provenance issue:

- Put scientific outputs in a fresh, preregistered attempt directory separate
  from source code. Create it with `exist_ok=False`; never overwrite a completed
  attempt.
- Stage the complete artifact bundle in a temporary sibling directory.
- Have the command/log-owning wrapper atomically publish the bundle only after
  the process exits zero.
- Write `COMPLETE.json` last. It should contain hashes of the config, support,
  baseline table, runner, run log, and every output artifact.
- Make every verifier reject a bundle when `COMPLETE.json` is absent, mismatched,
  or lists unexpected/missing files.
- Preserve failed attempts under distinct failed-attempt paths rather than
  reusing canonical result paths.

Cheap structural tests:

- Inject a failure before each output write and assert no bundle is accepted.
- Inject a failure between every pair of writes and assert no completion marker
  exists.
- Attempt a second run into a completed attempt directory and assert it fails
  without altering any hash.
- Corrupt each output after completion and assert manifest verification rejects
  it.

## Orchestrator disposition

The adverse verdict stands. T016 remains open and blocks T017. T023 owns the
provenance fix; no scientific core execution is authorized until a sterile
re-review returns SOUND.
