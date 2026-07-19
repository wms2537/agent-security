# Hypothesis iteration 4 v7 — Beacon-Held-Out Conditional-Regret Stress Test

**Supersedes:** `research-log/013-hypothesis-iter-4-v6-conditional-regret.md`
and every earlier ORF hypothesis  
**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** ready for theory review round 9

## Context and round-8 resolutions

Round 8 accepted the score/regret algebra, exact negative result, binary
materiality partition, notation, taxonomy, and anti-stacking contrast. It rejected
v6 because failures could not always produce a terminal ledger resolution, a
crash after the target GET could permit another GET, TSV/summary cross-fields were
not fully specified, `math.log/exp` was platform-dependent, the 5% prediction was
unsupported, and selective-reporting language was too strong.

V7 creates two new machine artifacts and leaves all reviewed v6 files immutable:

- `experiments/configs/orf-heldout-v5.json`, 227 lines, SHA-256
  `fffd81d1b9f5b64b1a9d813e1ca0d57f0cf69708c71cc04b4889bdb340cf137c`;
- `experiments/configs/orf-heldout-v5-artifacts.schema.json`, 353 lines,
  SHA-256
  `7536fda3e9d4d01ecff3e6dafd29e2c1d82874dfda457c963efaed8fe62c1f3a`.

| Round-8 blocker | V7 resolution |
|---|---|
| Invalid and terminal outcomes | `OUTCOME.json` is a schema-discriminated `VALID` or `PROTOCOL_INVALID` union. The invalid branch requires no summary and covers failures from `IMPLEMENTED` onward. It directly carries the crash ledger resolution. `COMPLETED.json` is a durable transition with hashes of outcome, ledger, log, progress, and manifest. |
| Crash between target GET and raw write | An exclusively created and directory-fsynced `TARGET_FETCH_STARTED.json` precedes the GET. Its presence forbids every later GET. A marker without raw bytes becomes terminal invalid. The anchor GET receives the same protection through `FREEZE_STARTED.json`. |
| Incomplete machine specification | The contract defines closed bands, exact ordinal origins/order, lowercase booleans, status/error/retained/hash/count biconditionals, set-valued binding ties, every metric formula, fixed array order/bins, mixture sum/selection, all failure keys, and named validators `V01..V24` plus positive/negative golden fixtures. |
| Numeric reproducibility | CPython 3.14.3 and libmpdec 4.0.1 are pinned. PRNG floats are converted through their exact ratio into precision-80 Decimal; `ln/exp` are libmpdec operations; every parameter is converted individually to `Fraction` before cost arithmetic. Every cliff floor must be at least `1E-60` from an integer or the protocol is invalid without resampling. |
| No support for 5% | A preregistered public non-target ensemble now supplies exploratory support without touching the future target. The valid retry cleared 5% on 64/64 equal-weight masters, minimum 34.576%, and passed all weight/saturation sensitivities. Threshold, factors, weights, and target rule were unchanged. |
| Selective-reporting overclaim | Every valid or invalid terminal commit/status/outcome/completed/summary/results hash must be posted to this same thread and recorded. The claim is explicitly weakened to mitigation under honest reporting, not cryptographic prevention. |

There is still no held-out evaluator, frozen implementation, beacon target, target
GET, master, profile, held-out result, submission, or Kaggle action.

## Named concept

### Beacon-Held-Out Conditional Regret (ORF-B)

**Plain language.** Both policies retain the same seven one-candidate probes. A
global policy must use one fill length for every realized synthetic profile; a
conditional oracle may choose separately for each profile. ORF-B measures the
exact score forfeited by the global restriction on one future, post-freeze,
equal-stratum realization. A deliberately homogeneous split must forfeit exactly
nothing. This is an oracle-information stress test, not a live learning result.

**Formal definition.** On fixed finite primary split `D`, let `S_z(m)` be the
post-probe objective for profile `z` and length `m`:

```text
A(D)        = sum_z max_m S_z(m),
S_global(D) = max_m sum_z S_z(m),
Delta(D)    = A(D)-S_global(D)
            = sum_z [max_m S_z(m)-S_z(m_global)] >= 0.
```

The inequality is an identity. The empirical prediction is the material magnitude
`100*Delta(D)/S_global(D) >= 5` on exactly one valid held-out realization.

## Claim, variables, controls, and decision

**Falsifiable claim.** On the one valid 320-profile primary split, `ADAPTIVE` will
score at least 5.000000000000% above `PROBE_GLOBAL_PRIMARY`. On the 64-profile
homogeneous split, `ADAPTIVE-PROBE_GLOBAL_NEGATIVE` will equal integer zero.

- **Independent variable:** profile-conditioned versus split-global scope of the
  fill-length argmax after identical retained probes.
- **`varies`:** `candidate-structure-policy`; **kind:** `metric`.
- **Primary dependent variable:** exact reduced rational
  `(A-S_global)/S_global`, serialized as a fixed-12 percent.
- **Primary comparison:** `ADAPTIVE` versus `PROBE_GLOBAL_PRIMARY`; no secondary
  control can rescue its outcome.
- **Expected direction:** nonnegative by identity.
- **Expected magnitude/confidence:** at least 5%, still low confidence because the
  calibration distribution is purpose-built public support, not the held-out
  realization or a generator-population bound.
- **Controls:** identical profiles, probes, retained probe findings, resource
  arithmetic, objective, candidate cap, action set, code, source hashes, ordering,
  and terminal rules.

For every valid result:

```text
CONFIRMED / MATERIAL
    iff 100*(A-S_global) >= 5*S_global;

DISCONFIRMED / ZERO
    iff A-S_global = 0;

DISCONFIRMED / POSITIVE_SUBTHRESHOLD
    iff 0 < 100*(A-S_global) < 5*S_global.
```

Thus every valid result is decisive. `Delta<0`, a nonzero homogeneous difference,
or any protocol/schema/numeric failure is `PROTOCOL_INVALID`, not a scientific
outcome.

## Preregistered non-target support

Entry 014 preregistered 64 masters
`SHA256("orf-nontarget-calibration-v1|master|{000..063}")`, four fixed weightings,
two saturation settings, a floor certificate, and an all-or-nothing support rule
before execution. Its first run was rejected and preserved as `crash` because the
cost polynomial used Decimal's default precision before `Fraction` conversion.

Entry 015 and commit `47f50a2` preregistered a single implementation-only retry:
the same masters, predictions, factors, threshold, weights, and sensitivity rules,
but individual `Fraction(a)`, `Fraction(b)`, and `Fraction(d)` conversion before
exact rational costs. Commit `a120336` records:

| Fixed design | Clear 5% | Minimum | Median | Maximum |
|---|---:|---:|---:|---:|
| Equal weights, `H=200000` | 64/64 | 34.575811113981% | 40.924155277025% | 45.433610480180% |
| Balanced cliff presence, `H=200000` | 64/64 | 24.987661930465% | 32.324156091809% | 38.849300841017% |
| No cliff only, `H=200000` | 64/64 | 5.117860088584% | 6.991608265969% | 9.793532503442% |
| Cliff only, `H=200000` | 64/64 | 35.101784203438% | 39.796867096003% | 44.613150778688% |
| Equal weights, `H=10^18` | 64/64 | 41.372040363181% | 44.204209608439% | 48.319935695095% |

The no-cliff unsaturated sensitivity cleared on 62/64. Minimum cliff-floor
distance was `2.4702e-8`, above `1E-60`. An independent check validated 512 unique
design rows, all score identities, and all summary counts. Summary and master
ledger hashes are respectively
`602d3885232d44a26f22f002f463c314d37308188510e519512bea710e433c05`
and `9d0f5208a18b673713dcec3c80c08c20697bcf06b0d07f5d6470b920e117e235`.

This evidence supports plausibility on a public calibration ensemble. It cannot
confirm the future target. The calibration budget is exhausted at 2/2; no further
range, weight, saturation, threshold, or master tuning is allowed.

## Authoritative score and exact resources

For finding set `F`, source-hashed SDK code defines

```text
Q(F) = sum predicate severity weights
       +2*number of unique non-null score-cell hashes,
S(F) = min(200000,Q(F)).
```

A successful constructed candidate has exactly `e_z(m)` `http.post` events with
literal `SECRET_MARKER`, one unique candidate hash, exactly `e_z(m)` severity-5
EXFILTRATION predicates, and no other predicate. Consequently

```text
q_z(m)=16*e_z(m)+2  if e_z(m)>0;
q_z(m)=0            otherwise.
```

Zero-yield attempts consume generation but return no finding. Candidate records,
predicate counts, hashes, SDK raw, profile raw, and objective saturation must all
recompute under validators V09 and V12.

The resource constants are

```text
B_gen=9000, B_rep=8100, C=2000, H=200000.
```

`B_rep` is a shared synthetic constraint, not a live tail guarantee. All costs and
capacities use `Fraction`; a capacity floor never consumes a binary float or
Decimal result.

## Reproducible parameter and cliff arithmetic

The evaluator must report CPython 3.14.3 and `decimal.__libmpdec_version__=4.0.1`.
Every Decimal operation uses a local precision-80, half-even context with frozen
exponent settings. For each `Random.random()` draw:

```text
(u_num,u_den) = draw.as_integer_ratio()
u             = Decimal(u_num)/Decimal(u_den)
x             = exp(ln(lo)+(ln(hi)-ln(lo))*u)
xF            = Fraction(x).
```

The cost is then formed only as exact rational `aF+bF*m+dF*m^2`; it is never
formed as a Decimal expression. This closes the calibration-v1 defect.

For cliff profiles, the precision-80 libmpdec expression is

```text
r=m*exp(-lambda*(m-k)/k),
e=clamp(floor(r),0,m),
distance=min(r-floor(r),ceil(r)-r).
```

All realized cliff distances must be at least `1E-60`. A closer value invalidates
the single realization with `NUMERIC_STABILITY`; it is never regenerated.

## Shared probes, fill, and policies

Probe once in exact order `L={1,2,4,8,16,24,32}`. Let

```text
gF=sum_m cF(m),
p =count_m[e(m)>0],
rF=sum_{e(m)>0} cF(m),
Q =sum_{e(m)>0} q(m).
```

For positive `q(m)`, compute four nonnegative capacities:

```text
cap_candidate  = C-p,
cap_generation = floor((B_gen-gF)/cF(m)),
cap_replay     = floor((B_rep-rF)/cF(m)),
cap_saturation = 0 if Q>=H else ceil((H-Q)/q(m)),
n(m)           = min(the four capacities),
S_z(m)         = min(H,Q+n(m)q(m)).
```

For zero `q`, `n=0` and `S_z(m)=min(H,Q)`. Each binding field is a boolean set:
it is true exactly when its capacity attains the minimum. Multiple true fields
preserve ties; no precedence rule discards them.

`ADAPTIVE` chooses the best `m` per profile. `PROBE_GLOBAL_PRIMARY` and
`PROBE_GLOBAL_NEGATIVE` choose their own split-global best. Every score tie chooses
the smaller length.

Seven no-probe static policies, their per-profile oracle, and every denominator-8
mixture are secondary controls. The mixture file enumerates exactly all 3,003
nonnegative seven-tuples summing to eight, in ascending lexicographic order.
`selected` is lowercase `true` for exactly the maximum aggregate row, ties to the
lexicographically smallest tuple.

## Primary coverage and exact homogeneous consequence

The primary split crosses reset `{LOW,HIGH}`, linear `{LOW,HIGH}`, curvature
`{NONE,HIGH}`, and cliff `{-1,4,8,16,24}`. Eight profiles in each of 40 cells give
320. Stratum and profile indices are fixed formulas; fresh keyed PRNGs draw `a,b`,
optional `d`, and optional `lambda` in that order. There is no outcome-conditioned
generation. Equal profile weights are the estimand, not an estimate of target
prevalence.

The 64 negative profiles draw only `b in [5,12]` and use exact
`cF(m)=bF*m,e(m)=m`. Seven probes cost `87bF` and score 1,406 raw. With
`T=8100/bF-87`, the support guarantees `T in [588,1533]`. Replay capacity is at
most 1,533, below remaining candidate capacity 1,993; generation exceeds replay;
additional raw is below `18*1533=27,594`, below remaining saturation 198,594.
For every `m>1`:

```text
floor(T/m)(16m+2) <= T(16+2/m) <= 17T
                   < 18(T-1) <= 18floor(T).
```

Because `T>18`, `m=1` is the unique fill maximizer. Adaptive and independently
selected negative global policies must therefore produce exact aggregate equality.

## Exact metrics and TSV semantics

The contract freezes complete headers, types, enums, row orders, and conditional
rules for `profiles.tsv`, `candidate_records.tsv`, and `mixtures.tsv`.

- Primary bands are closed `LOW/HIGH`, `LOW/HIGH`, and `NONE/HIGH`; negative
  bands are exactly `NA`.
- Profile, candidate, and phase ordinals start at zero, are contiguous, and are
  checked against parent counts.
- Every candidate row is an attempted candidate, so `attempted=true` is constant.
  Unattempted candidates have no row.
- `retained`, hash, predicate count, raw, `status`, and `error_code` obey explicit
  biconditionals. A zero event cannot be retained or carry a hash. An error row
  cannot carry score.
- All rationals are reduced integer/positive-denominator pairs. All booleans are
  lowercase. Every nonapplicable value has one prescribed sentinel.
- Every policy error makes the protocol invalid; it cannot be silently averaged.

Let `A,G,T,O,M` be adaptive, global, selected static, static oracle, and selected
mixture primary aggregates. The exact metrics are:

```text
primary                    = (A-G)/G,
adaptive_over_static       = (A-T)/T,
adaptive_over_mixed8       = (A-M)/M,
signed_oracle0_gap         = (A-O)/O,
probe_generation_cost_share= P/U,
```

where `P` is exact total probe generation cost and `U` exact total adaptive
generation use. The profile regret, 40 ordered stratum sums/gains, positive-regret
fractions, and six ordered action-separation bins have exact formulas in the
contract. Histogram counts must sum to 320. Every one of 28 error-code keys is
present in failure counts, including zeros.

Validators `V01..V24` are normative algorithms, not comments. They cover custody,
hashes, Decimal execution, indices, headers, conditional fields, ordinals, score
identities, policies, binding sets, exhaustive mixtures, all primary/secondary
formulas, array order/uniqueness, the negative result, outcome branches, ledger
resolution, completion, and terminal publication. The implementation gate requires
12 positive and 18 negative golden cases, including duplicate strata, wrong bins,
sum-7 mixtures, two selected mixtures, status/error mismatches, binding ties,
second GET attempts, invalid-without-summary, and terminal hash mismatch.

## Minimal terminal outcome and prediction ledger

Two future prediction rows are appended only after reviewed implementation and
tests. Freeze binds their whole-ledger hash. They remain absent now.

`OUTCOME.json` has exactly one branch:

1. **VALID.** Requires a complete schema-valid summary, its hash, materiality and
   subtype, available artifact hashes, exact primary resolution
   (`confirm/keep` or `disconfirm/discard`), and negative `0/confirm/keep`.
2. **PROTOCOL_INVALID.** Requires no summary. It records last durable state from
   `IMPLEMENTED` through `EVALUATION_STARTED`, a closed reason code, nullable
   freeze/artifact hashes, partial row counts, and both exact
   `NA/null/crash` resolutions.

The results ledger mutates once and solely from this outcome. Therefore a crash
before freeze, after a GET, during evaluation, or with incomplete rows can always
resolve both predictions without fabricating a complete summary.

After ledger resolution, write a new Prediction-versus-Reality log and progress,
hash an artifact manifest, and exclusively create `COMPLETED.json` containing all
those hashes. Commit the terminal prefix. A crash after this marker may recover
only the custodial commit/publication; no fetch, profile generation, or evaluation
may resume.

## Crash-safe custody and external terminal notice

The monotone chain is

```text
IMPLEMENTED -> FREEZE_FETCH_STARTED -> FROZEN -> ACKNOWLEDGED
 -> TARGET_FETCH_STARTED -> PULSE_PRESERVED -> OPENED
 -> EVALUATION_STARTED -> OUTCOME_RECORDED -> LEDGER_RESOLVED
 -> COMPLETED -> TERMINAL_PUBLISHED.
```

Before the anchor GET, `FREEZE_STARTED.json` is exclusively created, file-fsynced,
and directory-fsynced. Before the target GET, `TARGET_FETCH_STARTED.json` receives
the same treatment. Presence of a marker forbids a second corresponding GET. A
crash between response receipt and raw-byte persistence is thus distinguishable
and terminal invalid, not retryable.

The target remains exactly 1,440 one-minute periods after the anchor, with integer
UTC parsing and exact returned-time equality. Before target, the freeze commit,
freeze hash, and target are posted here and exact user ACK is committed. The target
master is

```text
SHA256(ASCII("orf-heldout-v5|master|") || bytes.fromhex(outputValue)).
```

For both valid and invalid outcomes, post this exact terminal record to the same
thread:

```text
ORF-B TERMINAL COMMIT={T} STATUS={VALID|PROTOCOL_INVALID}
OUTCOME_SHA256={...} COMPLETED_SHA256={...}
SUMMARY_SHA256={hex|NA} RESULTS_SHA256={...}
```

The actual message is one line and is preserved in `TERMINAL_PUBLICATION.json`.
This creates an externally timestamped honest-reporting obligation. It mitigates
selective suppression; it does not cryptographically prevent a local operator
from concealing that a terminal event occurred.

No Kaggle command appears anywhere in the contract.

## Evidence, assumptions, and validity domain

The contract re-verifies exact hashes for:

- SDK scoring weights, uniqueness bonus, denominator, and saturation;
- predicate sentinel, sink, and EXFILTRATION rule;
- candidate cap and evaluator deadlines;
- gateway hop and 9,000-second mechanics; and
- `experiments/attack.py`.

The source hashes match the current workspace. Official provider semantics remain
anchored to NIST Randomness Beacon 2.0 and its pulse API. The beacon is assumed
forward-unpredictable until the selected future pulse; it does not make the public
support, ranges, weights, or threshold unselectable.

Scientific validity assumes deterministic stationary probe continuation, additive
per-profile resources, no concurrency/cache/shared overhead, exact SDK predicate
construction, and fully observed oracle selection. Held-out validity additionally
assumes the committed code and custody transcript are honestly executed. These
assumptions do not hold automatically for live models.

## Fixed bias surface

1. **Selection.** The calibration supports but may reflect the designed support.
   The target realization is hidden; the support and equal weighting are public.
   Claims stay on this finite stress design.
2. **Confounding.** Same profiles, probes, findings, resources, and score isolate
   the scope of the argmax. Static and exhaustive denominator-8 controls expose
   probe and fixed-mixture alternatives.
3. **Assignment.** Complete paired evaluation and policy-free keyed substreams
   eliminate order-dependent allocation.
4. **Protocol deviation.** Pre-GET durable markers, exact ancestry/hashes,
   exclusive creates, raw bytes, and no retry make every observable deviation
   invalid.
5. **Missing data.** A complete valid summary requires every row. Any prefix can
   instead terminate through minimal invalid outcome and resolve the ledger.
6. **Measurement.** Source-hashed SDK predicates and score remain authoritative;
   Decimal/Fraction execution and floor certificates make the finite table
   reproducible.
7. **Analysis flexibility.** One primary contrast, binary threshold, exact
   formulas, bins, arrays, controls, and terminal resolution are frozen.
8. **Selective reporting.** Pre-target ACK and post-terminal thread hashes create
   visible custody obligations. They mitigate but cannot prevent dishonest local
   suppression.

## Failure modes and alternative explanations

- A positive but sub-5% result falsifies materiality.
- Equal cliff-heavy cells, cost-band crossings, integer floors, saturation, and
  novelty bonuses may generate the magnitude; weight and saturation sensitivities
  reveal, but do not remove, this designed-support explanation.
- The generic advantage of 320 oracle choices is the narrow estimand, not evidence
  that a noisy selector can learn them.
- The denominator-8 class is not every nonadaptive sequence.
- Probe nonstationarity, drift, or shared overhead can erase the result in live
  execution.
- A marker, schema, hash, row, predicate, score, floor, negative, or publication
  failure is protocol-invalid, never evidence for or against the hypothesis.

## Taxonomy, anti-stacking, and Occam

- **Opportunity:** Evidence Gap dominant; Resource Bottleneck secondary.
- **Method:** **Empirical Mapping dominant**; Optimization/Search secondary.
- **Operation:** **replace** one split-global argmax with profile-conditioned
  argmaxes.
- This is not Bridge Opportunity × Synthesis/Unification.

**Distinguishing prediction.** Under identical retained probes and resources,
profile conditioning must produce material regret on the crossed split and exact
zero regret on the homogeneous split. A plain combination or probe-portfolio
change predicts neither paired contrast because the global policy already owns the
same probes and candidate family.

Occam's scientific object is the single finite conditional-regret ratio and exact
negative consequence. Beacon, schemas, validators, and custody are measurement
infrastructure rather than extra mechanism components.

## Self-critique and problem alignment

`Delta>=0` is algebra, while 5% remains empirical. The public ensemble provides
real ex-ante support but is purpose-designed and was observed before the target;
it is not a formal lower bound. The primary selector is an oracle, so confirmation
only justifies pursuing a later noisy-selection PoC. The synthetic replay budget
does not establish live void safety. Thread publication remains an honest-reporting
control, not an immutable public ledger.

**Problem alignment.** Confirmation would establish a necessary synthetic fact
for `PROBLEM.md`: post-probe profile information has material value beyond the
best identical-probe global fill on a genuinely future realization. It would not
establish a Kaggle gain, private transfer, or a deployable selector.

## Deterministic pre-review evidence

- Both JSON artifacts parse.
- The artifact schema passes the Draft 2020-12 metaschema.
- All five source hashes match.
- Calibration summary/master hashes match commits and the contract.
- The contract contains exactly named `V01..V24`, all 3,003 mixtures, closed row
  vocabularies, no numeric seed field, and an explicit prohibition on
  seed/pulse/target/output/retry overrides.
- No file exists at `experiments/runs/orf-heldout-v5`; no outcome has been opened.

## Decision

Commit this hypothesis and both machine artifacts, then dispatch one sterile round-9
theory review with only the six round-8 issues in the template's previous-issue
slot. Do not implement, freeze, fetch a target, derive profiles, submit, or perform
any Kaggle action before a `RIGOROUS` verdict and later phase checkpoints.
