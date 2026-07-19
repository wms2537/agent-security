# Hypothesis iteration 4 v8 — Crash-Atomic Beacon-Held-Out Conditional Regret

**Supersedes:** `research-log/016-hypothesis-iter-4-v7-conditional-regret.md`
and all earlier ORF entries  
**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** ready for final authorized theory review round 10

## Context and round-9 resolutions

Round 9 found the finite scientific claim, algebra, negative proof, target-fetch
safety, numeric reproducibility, calibration support as posed, bias surface,
taxonomy, anti-stacking test, and selective-reporting scope sound. It rejected v7
for three remaining reasons: direct creation could leave truncated authoritative
terminal files; policy-error and mixture stop branches were not single-valued; and
calibration-to-target exchangeability was not an explicit assumption.

V8 creates two new artifacts and does not edit the reviewed v7 files:

- `experiments/configs/orf-heldout-v6.json`, 180 lines, SHA-256
  `2be4b2809b31b26911c8070bfd2769ef70f3a17c553c7e920da75a67b537ec09`;
- `experiments/configs/orf-heldout-v6-artifacts.schema.json`, 148 lines,
  SHA-256
  `ac0b791f086aae0715b79c4dbfaff05ded7c35725b49d3e47e5ec7eed4e2dc3c`.

| Round-9 blocker | V8 resolution |
|---|---|
| Truncated terminal files and non-idempotent ledger mutation | Every authoritative new file is built at a fixed same-directory staging path, file-fsynced, hash-verified, and atomically published with `link(stage,final)` no-replace before directory fsync. Recovery has an exact state table for absent/partial/complete staging and final paths. The resolved ledger is first published immutably as `RESOLVED_RESULTS.tsv`; root `results.tsv` is only an atomic idempotent mirror under `WORKSPACE_TRANSACTION.json`. |
| Post-outcome completion failure | Scientific `OUTCOME` is never rewritten. Post-outcome terminalization is a separate custody layer: exact destination after-hashes produce `COMPLETED.json`; any third destination hash produces `TERMINALIZATION_FAILED.json`. Either branch posts the scientific outcome and authoritative resolved-ledger hash. Partial `COMPLETED` staging is recoverable and is not a new scientific error. |
| Policy-error contradiction | Final TSVs have no status/error columns and contain only complete valid rows. Any policy/schema/predicate/score error aborts to invalid outcome; partial staging rows are non-authoritative evidence only. Parameter fractions are therefore always the keyed profile values in every final row. |
| Mixture ambiguity | Executable step pseudocode now orders generation, candidate, and replay prechecks; specifies which attempts charge which resource; continues after zero yield; and stops immediately after a saturation-crossing retained candidate. |
| Calibration-target bridge | The hypothesis conditions inference on a SHA-256 random-oracle/PRF heuristic plus a fresh uniform NIST pulse. Without that assumption the 64 masters are only deterministic coverage. Under iid-equivalent masters, 64/64 has an exact one-sided 95% lower success bound of `0.9542702976692375...`. |

No evaluator implementation, freeze, NIST target, target GET, master, held-out
profile, scientific result, submission, or Kaggle action exists.

## Named concept

### Beacon-Held-Out Conditional Regret (ORF-B)

**Plain language.** Both policies retain the same seven measurement candidates. A
global policy must fill every realized synthetic profile with one common length;
a conditional oracle can choose a different length per profile. ORF-B measures the
exact objective lost by the global restriction on one future post-freeze finite
table. A homogeneous companion table must lose exactly zero. It measures oracle
information value, not live learnability.

**Formal definition.** For primary split `D`, profile `z`, legal length `m`, and
exact post-probe objective table `S_z(m)`:

```text
A(D)        = sum_z max_m S_z(m),
S_global(D) = max_m sum_z S_z(m),
Delta(D)    = A(D)-S_global(D)
            = sum_z(max_m S_z(m)-S_z(m_global)) >= 0.
```

The identity proves only direction. The prediction concerns the magnitude.

## Falsifiable claim and variables

**Claim.** On exactly one valid 320-profile primary split, `ADAPTIVE` will score
at least 5.000000000000% above `PROBE_GLOBAL_PRIMARY`. On the 64-profile
homogeneous validator split, `ADAPTIVE-PROBE_GLOBAL_NEGATIVE` will equal integer
zero.

- **Independent variable:** per-profile versus split-global scope of the
  fill-length argmax after the same retained probes.
- **`varies`:** `candidate-structure-policy`; **kind:** `metric`.
- **Dependent variable:** reduced exact `(A-S_global)/S_global`, serialized as a
  fixed-12 percent.
- **Primary comparison:** adaptive versus primary probe-global; this alone decides
  the materiality claim.
- **Expected direction:** nonnegative by action-class containment.
- **Expected magnitude/confidence:** at least 5%, low confidence.
- **Controls:** same profiles, probes, retained probe findings, candidates,
  source-hashed score, exact resources, cap, action set, and code.

Every valid result is decisive:

```text
CONFIRMED / MATERIAL
  iff 100*(A-S_global) >= 5*S_global;

DISCONFIRMED / ZERO
  iff A-S_global=0;

DISCONFIRMED / POSITIVE_SUBTHRESHOLD
  iff 0 < 100*(A-S_global) < 5*S_global.
```

Negative `Delta`, a nonzero homogeneous difference, or any contract violation is
`PROTOCOL_INVALID`, not evidence for or against the magnitude.

## Calibration evidence and the seed-domain assumption

Before any calibration outcome, entries 014–015 froze 64 public masters, all
factor cells, four weightings, two saturation settings, a cliff-floor certificate,
and an all-or-nothing support rule. The first execution was rejected as a numeric
implementation crash. An implementation-only retry retained every scientific
choice and converted each Decimal parameter individually to `Fraction`.

The valid exploratory retry reported:

| Design | Masters clearing 5% | Minimum gain | Median gain |
|---|---:|---:|---:|
| Equal, `H=200000` | 64/64 | 34.575811113981% | 40.924155277025% |
| Balanced cliff presence, `H=200000` | 64/64 | 24.987661930465% | 32.324156091809% |
| No cliff only, `H=200000` | 64/64 | 5.117860088584% | 6.991608265969% |
| Cliff only, `H=200000` | 64/64 | 35.101784203438% | 39.796867096003% |
| Equal, `H=10^18` | 64/64 | 41.372040363181% | 44.204209608439% |

The fixed masters are `SHA256` outputs on 64 distinct domain-separated labels.
The target master will be `SHA256` of a different prefix plus a fresh 512-bit NIST
output. Their connection requires this explicit assumption:

> Conditional on SHA-256 behaving as a random oracle/pseudorandom function on
> these distinct inputs, and on the selected NIST output being fresh uniform
> public randomness, calibration and target masters are iid-equivalent uniform
> 256-bit values. Seeding the frozen CPython PRNG with their big-endian integers
> then induces comparable profile distributions.

Forward unpredictability alone does not supply this. If either assumption is
rejected, calibration is only deterministic coverage of 64 chosen seeds and makes
no probabilistic target statement.

Conditional on iid Bernoulli indicators under that master distribution, 64/64
clearing 5% yields exact one-sided 95% Clopper-Pearson lower bound

```text
p_lower = 0.05^(1/64)
        = 0.95427029766923753936976169563270450199231817533648.
```

This interval is conditional, not a claim proved by cryptography. The ensemble is
exploratory, cannot confirm the future prediction, and exhausted the 2/2 budget.
The target threshold, factors, weights, and protocol were not changed afterward.

## Score, exact resources, and reproducible arithmetic

For finding set `F`, source-hashed SDK behavior gives severity weights
`{1,2,4,8,16}` plus two per unique non-null score-cell hash. A successful
constructed candidate with `e_z(m)` severity-5 EXFILTRATION predicates and one
unique hash has

```text
q_z(m)=16*e_z(m)+2,
```

while zero yield makes no finding and `q=0`. The objective is
`S(F)=min(200000,Q(F))`.

Resource constants are `B_gen=9000`, `B_rep=8100`, `C=2000`, and `H=200000`.
`B_rep` is synthetic, not a live deadline-tail guarantee.

The evaluator must be CPython 3.14.3 with libmpdec 4.0.1. Every Decimal operation
uses a frozen precision-80 half-even local context. A PRNG draw is converted through
its exact binary ratio to Decimal. LogUniform uses libmpdec `ln/exp`. Each generated
parameter is then converted separately to `Fraction`; costs use only
`aF+bF*m+dF*m^2`.

Cliff events use precision-80

```text
r=m*exp(-lambda*(m-k)/k), e=clamp(floor(r),0,m).
```

Every distance from `r` to the nearest integer must be at least `1E-60`. Failure
invalidates the one realization without regeneration. All resource arithmetic and
capacity floors are exact rational operations.

## Generator, policies, and exact mixture loop

The primary crosses 40 equal cells: reset `{LOW,HIGH}`, linear `{LOW,HIGH}`,
curvature `{NONE,HIGH}`, and cliff `{-1,4,8,16,24}`. Eight keyed replicates give
320 profiles. Index formulas, draw order, LogUniform ranges, and equal weights are
public and frozen. The negative has 64 profiles with exact `c(m)=bF*m,e(m)=m`.

Probe lengths `{1,2,4,8,16,24,32}` once. With common probe generation `gF`,
positive-return count `p`, replay `rF`, and raw `Q`, positive `q(m)` fills

```text
n(m)=max(0,min(
  C-p,
  floor((B_gen-gF)/cF(m)),
  floor((B_rep-rF)/cF(m)),
  0 if Q>=H else ceil((H-Q)/q(m))
)),
S_z(m)=min(H,Q+n(m)q(m)).
```

Zero `q` gives no fill and retains common probe score. Adaptive chooses per
profile; globals choose once per split; ties choose smaller length. Static and
per-profile static-oracle policies are fixed secondary controls.

The denominator-8 class contains all `C(14,6)=3003` ordered compositions. For
each scheduled mixture action, the algorithm is single-valued:

1. Compute exact intended `m,c,e,q` without charging resources.
2. If remaining generation is below `c`, stop before attempt and charge nothing.
3. If `e>0` and either no candidate slot remains or replay is below `c`, stop
   before attempt and charge nothing.
4. Otherwise emit the attempted row and charge generation `c`.
5. If `e=0`, retain nothing, advance the scheduler, and continue.
6. If `e>0`, charge replay `c`, retain the finding, decrement the candidate slot,
   and add `q`.
7. If the objective has reached 200,000, stop immediately after that retained
   crossing candidate; otherwise advance and continue.

No candidate exists after a stop. The selected composition has the maximum exact
primary aggregate, with lexicographically smallest tuple on a tie.

## Complete-only TSV semantics

V7 tried to serialize policy errors as score rows, creating contradictions. V8
removes that branch. Final `profiles.tsv`, `candidate_records.tsv`, and
`mixtures.tsv` contain only complete valid rows and no status/error columns.

Any profile, policy, predicate, score, schema, row, or numeric error aborts the
evaluation and produces an invalid outcome. A partial staging file may be retained
as non-authoritative evidence and counted in the invalid outcome, but can never be
published at a final TSV path or enter a valid metric.

Consequences are exact:

- every final profile parameter fraction is the keyed realized value for every
  policy row—never `0/1` substitution on failure;
- every candidate row is an actual attempted action, so `attempted=true`;
- ordinals start at zero and are contiguous;
- `length,cost,event_count,phase` equal the scheduled action;
- `e=0` iff unretained, hash `NA`, predicate/raw zero;
- `e>0` iff retained, hash equals candidate ID, predicates equal `e`, and raw is
  `16e+2`;
- final row counts/orders/headers and all sentinel types are exact; and
- mixture selected is lowercase true/false, exactly one true, and every tuple
  sums to eight.

Binding is set-valued: every capacity attaining the minimum is true, including
multiway ties. There is no arbitrary precedence.

## Exact metrics and homogeneous invariant

Let `A,G,T,O,M` be primary adaptive, probe-global, selected static, static oracle,
and selected mixture aggregates. All denominators are positive. Report reduced

```text
primary                 = (A-G)/G,
adaptive_over_static    = (A-T)/T,
adaptive_over_mixed8    = (A-M)/M,
signed_oracle0_gap      = (A-O)/O,
probe_generation_share = P/U.
```

`P/U` is exact probe generation over exact adaptive generation. Profile regrets,
ordered unique stratum regrets, positive fractions, and six exact action-separation
bins are formula-bound; the histogram sums to 320. All 23 failure keys are
mandatory zeros in a valid summary.

For the homogeneous split, seven probes cost `87bF`, common raw is 1,406, and
`T=8100/bF-87` lies in `[588,1533]`. Replay binds before generation, candidate,
or saturation. For `m>1`:

```text
floor(T/m)(16m+2) <= 17T < 18(T-1) <= 18floor(T).
```

Thus `m=1` uniquely maximizes every profile. Adaptive and independently selected
negative global aggregates must be identical. This is an implementation invariant,
not separate evidence for the 5% magnitude.

## Crash-atomic authoritative publication

Before freeze, disposable tests must establish one POSIX filesystem/device for the
workspace and run directory with atomic same-directory hard-link no-replace,
atomic replace, file fsync, and directory fsync. A preflight failure forbids
freeze. The failure model includes process crashes and partial writes. Permanent
media corruption, permanent ENOSPC, or a filesystem/kernel violating these tested
primitives is outside scope and is stated rather than silently assumed away.
Every mutating command holds one fixed exclusive `flock`, released by the kernel
on process death, so concurrent protocol mutation is forbidden.

For any recomputable authoritative new file `NAME`:

1. Construct all canonical bytes in memory and compute expected SHA-256.
2. Use fixed same-directory `.NAME.orf-stage`.
3. If final exists, require its exact hash; a matching staging file may be cleaned.
4. If final is absent and stage is complete/exact, continue. If stage is partial,
   unlink it, fsync the directory, and recreate it.
5. Create staging with `O_CREAT|O_EXCL`, write all bytes, fsync, close, and verify.
6. `link(stage,final)` atomically publishes without replacement.
7. Fsync directory, unlink stage, and fsync directory again.

A crash can leave no file, a partial non-authoritative stage, a complete stage, or
a complete final (possibly with stage hard link). Recovery deterministically
advances each state. It can never treat a truncated final path as authoritative.

For fetched raw bytes, a complete schema/time-valid stage may be published after
recovery without another GET. A partial raw stage plus pre-GET marker is invalid;
the response is never refetched.

## Scientific outcome and idempotent ledger transaction

`OUTCOME.json` remains a discriminated scientific union.

- **VALID** references complete validated TSVs/summary and exact decision fields.
- **PROTOCOL_INVALID** requires no summary and records last scientific state,
  closed reason, nullable hashes, partial staging row counts, and both
  `NA/null/crash` resolutions.

Both branches include `results_before_sha256` and the SHA-256 of the entire
deterministic resolved ledger after-image. Outcome publication uses the staged
no-replace algorithm and is idempotent.

Before changing root `results.tsv`, the evaluator constructs it from the exact
implementation-commit blob plus `OUTCOME` and atomically publishes the complete
immutable bytes as `RESOLVED_RESULTS.tsv`. This sidecar is the authoritative
terminal prediction resolution. It exists even if a later workspace mirror fails.

`WORKSPACE_TRANSACTION.json` binds outcome, ledger before/after, progress
before/after, progress sidecar, and exact frozen terminal-log path/hash. Root
results and progress update via same-directory hard-link staging plus atomic
`os.replace`:

- destination hash equals before: perform replace and fsync directory;
- destination hash equals after: already complete, continue;
- any third hash: do not overwrite; publish `TERMINALIZATION_FAILED.json`.

The terminal log is a new no-replace file. A process crash before or after any
replace is therefore idempotently recoverable.

If every destination reaches its after hash, atomically publish `COMPLETED.json`.
A crash while staging it is recovered by the same publication algorithm; there is
no contradictory `COMPLETED_CREATE` scientific error. If a third destination hash
appears, custody fails but scientific `OUTCOME` is unchanged and the immutable
resolved sidecar still resolves both predictions.

Both custody branches must be posted in this same thread with scientific status,
custody status, terminal commit, outcome hash, resolved-ledger hash, terminal
artifact hash, summary or `NA`, and root-results hash or `NA`. This mitigates
selective suppression under honest operation; it does not cryptographically
prevent concealment.

## One-way held-out chain

```text
IMPLEMENTED -> FREEZE_FETCH_STARTED -> FROZEN -> ACKNOWLEDGED
 -> TARGET_FETCH_STARTED -> PULSE_PRESERVED -> OPENED
 -> EVALUATION_STARTED -> OUTCOME_RECORDED
 -> RESOLVED_LEDGER_PUBLISHED -> WORKSPACE_TRANSACTION_PUBLISHED
 -> COMPLETED_OR_TERMINALIZATION_FAILED -> TERMINAL_PUBLISHED.
```

`FREEZE_STARTED.json` precedes the only anchor GET. Before the future target,
freeze commit/hash/time are posted here and exact ACK is committed.
`TARGET_FETCH_STARTED.json` precedes the only target GET and forever forbids a
second. Target bytes precede master derivation; `OPENED.json` precedes
`EVALUATION_STARTED.json`; no profile stream exists before both.

Scientific evaluation never resumes after an exception or outcome. Only the pure
terminal recovery state machine may resume. No Kaggle command exists.

## Fixed bias surface

1. **Selection.** Target realization is hidden, but support, equal weights, factor
   ranges, and threshold are designed. The claim remains on this finite support.
2. **Confounding.** Same profiles, probes, candidate family, resources, and score
   isolate action-scope relaxation. Engineered heterogeneity explains magnitude.
3. **Assignment.** Complete paired evaluation and policy-free keyed streams remove
   execution-order allocation.
4. **Protocol deviation.** Pre-GET markers, atomic publication, exact hashes, and
   no scientific retry turn observable deviations into invalid outcome.
5. **Missing data.** Only complete valid ledgers enter metrics. Any partial prefix
   resolves through invalid outcome and immutable resolved-ledger sidecar.
6. **Measurement.** Source-hashed predicates/score, Decimal/Fraction arithmetic,
   and cliff certificate define a reproducible finite table.
7. **Analysis flexibility.** One contrast, binary threshold, exact controls,
   formulas, bins, and terminal mappings are frozen.
8. **Selective reporting.** Pre-target ACK and post-terminal status/hashes are
   honest-reporting controls, explicitly not prevention.

## Assumptions, failure modes, and alternatives

Scientific validity assumes deterministic stationary probe continuation, additive
independent per-profile resources, no cache/concurrency/shared overhead, exact SDK
construction, and fully observed oracle actions. Violating these destroys the
finite score-table interpretation or turns the task into untested learning.

Held-out inference assumes the seed-domain heuristic above, honest NIST/thread/git
custody, and the preflighted POSIX crash model. Rejecting seed exchangeability
downgrades calibration to coverage but does not change the exact future estimand.

A confirmed magnitude may be driven by cliff-heavy equal cells, cost-band
separation, saturation, integer floors, novelty bonuses, or generic flexibility of
320 oracle choices. The weight/saturation controls describe these mechanisms; they
do not establish population prevalence or a deployable selector. A sub-5% result
falsifies materiality.

## Taxonomy, anti-stacking, Occam, and alignment

- **Opportunity:** Evidence Gap dominant; Resource Bottleneck secondary.
- **Method:** **Empirical Mapping dominant**; Optimization/Search secondary.
- **Operation:** **replace** one split-global optimizer with profile-conditioned
  optimizers.
- It is not Bridge Opportunity × Synthesis/Unification.

**Distinguishing prediction.** With identical retained probes and candidates,
profile conditioning must be materially better on the crossed table yet exactly
equal on the homogeneous table. A probe portfolio or plain component combination
does not predict this paired action-scope contrast.

The scientific object is minimal: one finite conditional-regret ratio and one
homogeneous invariant. Beacon, schemas, and transactions are one-shot measurement
infrastructure, not mechanism components.

**Problem alignment.** Confirmation would establish that future realized
post-probe profile information has material synthetic value beyond the best common
fill. It would not establish Kaggle improvement, private transfer, or learnability.

## Deterministic pre-review evidence

- Both JSON files parse; the schema passes Draft 2020-12 metaschema.
- Root samples validate for complete summary, both outcome branches, workspace
  transaction, completed, and custody failure; a malformed invalid outcome fails.
- Contract/schema contain the same 23 unique protocol error keys.
- Exactly `V01..V16`, 3,003 mixtures, five source hashes, and two calibration
  hashes pass audit.
- CPython 3.14.3 reports libmpdec 4.0.1.
- `experiments/runs/orf-heldout-v6` is absent.

## Decision

Commit v8 and its machine artifacts, then use the final authorized sterile theory
review round 10 with only the three round-9 issues in the previous-review slot. Do
not implement, freeze, fetch, evaluate, submit, or perform any Kaggle action before
a `RIGOROUS` verdict and later phase checkpoints.
