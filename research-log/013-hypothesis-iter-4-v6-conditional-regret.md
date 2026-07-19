# Hypothesis iteration 4 v6 — Beacon-Held-Out Conditional-Regret Stress Test

**Supersedes:** `research-log/012-hypothesis-iter-4-v5-beacon-heldout.md` and all
earlier ORF entries  
**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** ready for theory review round 8

## Context and round-7 resolutions

Round 7 accepted the NIST timestamp conversion, `I→F→A` freeze enforcement,
split-specific negative control, normative threshold label, preregistration custody,
score algebra, and anti-stacking contrast. It rejected v5 because positive results
below 5% were insulated as inconclusive, `OPENED.json` required a digest before the
digest was derived, prose schemas remained multi-valued, prediction-ledger
resolution was absent, floating capacity arithmetic did not carry the exact
negative proof, notation collided, and taxonomy dominance was unstated.

This superseding entry and its two machine artifacts make the following changes:

| Round-7 blocker | v6 resolution |
|---|---|
| Sub-5% classified inconclusive | One binary `materiality_prediction`: every valid result below 5% is `DISCONFIRMED`. A separate descriptive subtype records `ZERO`, `POSITIVE_SUBTHRESHOLD`, or `MATERIAL`. |
| Impossible opening order/two-file atomicity | Use monotone one-file transitions: preserve target bytes; derive master; create complete `OPENED.json`; create `EVALUATION_STARTED.json`; only then construct profiles. A crash between any transitions is terminal and never resumes. No multi-file atomic transaction is claimed. |
| Schemas not single-valued | Add strict Draft 2020-12 JSON Schemas for every structured ledger and summary, plus exact TSV enums, sentinels, widths, orders, types, counts, tie direction, and fixed 12-decimal ratio formatting. |
| Prediction rows never resolved | Freeze exact pre-run rows and whole-file hash; map valid/invalid outcomes deterministically into `metric_value`, `signal`, and `status`; then commit the resolved ledger, new log, progress, and terminal artifacts. |
| Floating proof gap | Realized parameters remain frozen CPython floats, but all costs and resources are converted to exact `fractions.Fraction` before capacity arithmetic. The negative costs are exactly `m·Fraction.from_float(b)`. |
| Notation collision | Generation budget is `B_gen`; global aggregate is `S_global(D)`; primary adaptive aggregate is `A(D)`; conditional regret is `Delta(D)`. |
| Taxonomy ordering | Dominant paradigm is **Empirical Mapping**; Optimization/Search is secondary. |

The reviewed v5 files remain immutable. At review time there is no evaluator,
freeze, ACK, target pulse, master digest, profile, experiment, submission, or Kaggle
action.

## Named concept

### Beacon-Held-Out Conditional-Regret Stress Test (ORF-B)

**Plain language.** Both policies retain the same one-candidate measurement at all
seven legal lengths. The global policy must choose one fill length for the entire
realized synthetic split; the conditional policy may choose separately on each
profile. The test measures exactly how much objective the global restriction loses
on one post-freeze, equal-stratum realization. A homogeneous split must lose
nothing. This is a deterministic oracle-information stress test, not evidence for
noisy live selection.

**Formal definition.** For fixed split `D` and exact post-probe objective table
`S_z(m)`, define

```text
A(D)        = Σ_{z∈D} max_m S_z(m),
S_global(D) = max_m Σ_{z∈D} S_z(m),
Delta(D)    = A(D)-S_global(D)
            = Σ_z[max_m S_z(m)-S_z(m_global)] ≥ 0.
```

The inequality is algebra. The low-confidence prediction is the normative material
claim `100·Delta(D)/S_global(D)≥5` on the single held-out primary realization.

## Claim, variables, and outcome semantics

**Falsifiable claim.** On the one valid 320-profile primary split, the exact
`ADAPTIVE` aggregate will be at least 5.0% above `PROBE_GLOBAL_PRIMARY`. On the
64-profile homogeneous split, `ADAPTIVE` minus separately selected
`PROBE_GLOBAL_NEGATIVE` will equal integer zero.

- **Independent variable:** per-profile versus split-global scope of the fill
  argmax after identical probes.
- **`varies` slug:** `candidate-structure-policy`; `kind=metric`.
- **Primary dependent variable:**
  `100·(A(D)-S_global(D))/S_global(D)` for the primary split.
- **Primary comparison:** `ADAPTIVE` versus `PROBE_GLOBAL_PRIMARY`; it alone decides
  the narrow materiality prediction.
- **Expected direction:** nonnegative by identity.
- **Expected magnitude:** the 5% cut is a normative ex-ante materiality threshold,
  not evidence-derived; prediction confidence is low.
- **Secondary controls:** `STATIC0_GLOBAL_PRIMARY`, `ORACLE0`, and strongest member
  of the fully enumerated denominator-eight class, `MIX8_GLOBAL_PRIMARY`.
- **Controls:** identical profile table, probes, retained findings, resources,
  score, action set, code, source hashes, ordering, and failure/output rules.

For a valid exact outcome:

```text
materiality_prediction = CONFIRMED     iff 100·Delta ≥ 5·S_global;
materiality_prediction = DISCONFIRMED  iff 100·Delta < 5·S_global.

contrast_subtype = ZERO                   iff Delta=0;
contrast_subtype = POSITIVE_SUBTHRESHOLD  iff 0<100·Delta<5·S_global;
contrast_subtype = MATERIAL               iff 100·Delta≥5·S_global.
```

Thus a 3% result is unambiguously `DISCONFIRMED / POSITIVE_SUBTHRESHOLD`, not
inconclusive. `Delta<0` contradicts the argmax implementation and makes the protocol
invalid. A protocol failure is `NOT_EVALUABLE`, never a scientific outcome.

If adaptive fails to beat `MIX8_GLOBAL_PRIMARY`, confirmation still establishes
the identical-probe conditional-regret fact, but no end-to-end superiority over
that nonadaptive class is supported.

## Authoritative score and constructed findings

For finding set `F`, SDK raw is

```text
Q(F)=Σ_{f∈F}Σ_{p∈predicates(f)}w(severity(p))
     +2·|{non-null unique score-cell hashes in F}|,
w(1..5)={1,2,4,8,16}.
```

SDK normalized score is `min(1000,Q/200)`, so the raw-equivalent objective is

```text
S(F)=min(200000,Q(F)).
```

A positive-yield candidate has one finding built from exactly `e_z(m)` successful
`http.post` events. Each event posts literal `SECRET_MARKER` to a domain-separated
`.invalid` URL; `eval_predicates` must return exactly that many severity-5
EXFILTRATION predicates and no others. A candidate-specific SHA-256 is its unique
score-cell hash. Therefore

```text
q_z(m)=16e_z(m)+2 when e_z(m)>0.
```

A zero-yield attempt consumes generation but creates no finding or score. Every
attempt has a candidate audit row. IDs use exact three-digit profile, four-digit
candidate ordinal, and two-digit length fields; policy and phase vocabularies are
closed enums in the contract. SDK predicates and score remain authoritative, with
per-row equality assertions.

The first candidate to reach or cross raw-equivalent saturation is retained:

```text
n_sat(Q,q)=0 if Q≥200000 else ceil((200000-Q)/q).
```

The SDK raw may exceed 200,000, while the objective does not.

## Exact numeric resource model

Use distinct notation:

```text
B_gen=9000, B_rep=8100, C=2000, H=200000.
```

`B_rep` is solely a common synthetic constraint, not a calibrated replay-safety
allowance.

CPython 3.14.3 `random.Random` and `math.log/exp` generate the realized parameter
floats. Those binary floats define this finite estimand. Before any cost or capacity
calculation:

```text
aF=Fraction.from_float(a), bF=Fraction.from_float(b),
dF=Fraction.from_float(d),
cF_z(m)=aF+bF·m+dF·m².
```

All costs, sums, remaining budgets, divisions, and floors use exact `Fraction`.
`B_gen` and `B_rep` are `Fraction(integer,1)`. Costs/resources are serialized as
coprime integer numerator and positive denominator. Hence no IEEE-754 floor error
can change a candidate capacity. Primary cliff events use the frozen CPython
`math.exp` result before integer floor; negative profiles use no exponential.

## Policies

### Shared probes and fill

Attempt one probe in order `L={1,2,4,8,16,24,32}`. Define

```text
gF_z = Σ_m cF_z(m),
p_z  = count_m[e_z(m)>0],
rF_z = Σ_{m:e_z(m)>0} cF_z(m),
Q_z  = Σ_{m:e_z(m)>0} q_z(m).
```

For positive `q_z(m)`:

```text
n_z(m)=max(0,min(
 C-p_z,
 floor((B_gen-gF_z)/cF_z(m)),
 floor((B_rep-rF_z)/cF_z(m)),
 n_sat(Q_z,q_z(m))
)),
S_z(m)=min(H,Q_z+n_z(m)q_z(m)).
```

Zero `q` gives zero fill. There is no eligibility threshold.

```text
m_A(z) = argmax_m S_z(m),
m_GP   = argmax_m Σ_{primary z}S_z(m),
m_GN   = argmax_m Σ_{negative z}S_z(m),
```

ties always choosing smaller length. `m_GN` is selected independently on the
negative split.

### Static, oracle, and mixture controls

For no-probe static positive `q`:

```text
n_static=min(C,floor(B_gen/cF),floor(B_rep/cF),ceil(H/q)),
S_static=min(H,n_static q).
```

Zero yield gives zero. Report all seven lengths, the primary aggregate best pure
length, and the per-profile pure oracle.

The nonadaptive mixture class contains all `C(14,6)=3003` weak integer
compositions of eight slots over the seven lengths. Its deficit scheduler and
resource stops are fixed. Selection maximizes primary aggregate and resolves ties
to the **lexicographically smallest** tuple
`(h_1,h_2,h_4,h_8,h_16,h_24,h_32)`. This is strongest in the exact class, not a
universal nonadaptive optimum.

## Primary coverage design

The primary crosses 40 equal-weight cells:

| Factor | Levels |
|---|---|
| reset `a` | low LogUniform `[5,20]`; high `[40,80]` seconds |
| linear `b` | low LogUniform `[0.1,1]`; high `[2,8]` seconds/message |
| curvature `d` | none `0`; high LogUniform `[0.05,0.2]` seconds/message² |
| cliff `k` | absent `-1`, `4`, `8`, `16`, `24` |

Eight profiles per cell give 320. Exact indexing is

```text
stratum=(((reset_index·2)+linear_index)·2+curvature_index)·5+cliff_index,
profile=8·stratum+replicate.
```

Fresh keyed PRNGs draw `a`, `b`, optional `d`, optional `lambda` in that order.
LogUniform is `exp(log(lo)+(log(hi)-log(lo))·rng.random())`. No rejection,
regeneration, or outcome conditioning occurs.

```text
e_z(m)=m                                      if k=-1 or m≤k,
       clamp(floor(m exp(-lambda(m-k)/k)),0,m) otherwise.
```

Every profile is equally weighted, equivalently `1/40` per cell and `1/8` within
cell. All cell results are mandatory. The support is designed stress coverage, not
a target prevalence model. Only realized within-cell floats are held out; the full
generator is public.

## Exact homogeneous consequence

The 64 negative profiles draw positive binary float `b∈[5,12]`, then define the
cost exactly as

```text
bF=Fraction.from_float(b), cF_z(m)=bF·m, e_z(m)=m.
```

Seven probes cost `87bF` and contribute common raw `16·87+2·7=1406`. Define exact
rational `T=B_rep/bF-87`. Since the realized float lies within `[5,12]`,
`T∈[588,1533]`. Generation, candidate cap, and saturation do not bind. For every
`m>1`:

```text
floor(T/m)(16m+2) ≤ T(16+2/m) ≤ 17T
                  < 18(T-1) ≤ 18floor(T),
```

because `T>18`. Thus `m=1` is the unique exact fill maximizer. Both `ADAPTIVE` and
`PROBE_GLOBAL_NEGATIVE` choose it and their integer aggregate difference is zero.

## Fixed finite estimand and mechanism metrics

There is no bootstrap, interval, p-value, or generator-population claim. The exact
finite metrics include:

- primary `Delta(D)` and gain with exact integer numerator/denominator;
- each profile's regret under `m_GP` and positive-regret count;
- each stratum's adaptive/global scores and regret;
- best-minus-second-best action separation histogram with six fixed bins;
- gains over static and mixture controls, signed pure-oracle gap, probe-cost share,
  selection histograms, resource bindings, and failures; and
- exact negative aggregate difference.

Percentage strings are uniquely serialized: use `Decimal` precision 80 and
`ROUND_HALF_EVEN`, quantize `100·numerator/denominator` to
`0.000000000001`, then `format(value,'f')`. Every string has exactly 12 fractional
digits.

## Machine schemas and records

Two immutable machine artifacts are reviewed with this hypothesis:

- `experiments/configs/orf-heldout-v4.json` — algorithms, enums, sentinels, TSV
  columns/types/orders/counts, cross-field rules, transition rules, commands, and
  hashes;
- `experiments/configs/orf-heldout-v4-artifacts.schema.json` — strict Draft
  2020-12 `$defs` for NIST pulse envelope, freeze, publication, opening,
  evaluation-start, abandonment, and the complete nested summary tree.

The artifact schema forbids additional properties in project-authored JSON. The
contract freezes:

- all policy IDs, phases, statuses, decisions, bindings, and error codes;
- `-1` as nonapplicable integer/absent cliff, `NA` as nonapplicable string;
- length fields or `-1`, and seven separate `h` fields for mixtures;
- exact raw NIST bytes, candidate traces/IDs, parameter hex strings, resource
  fractions, integer scores, and boolean spellings;
- 5,760 primary plus 192 negative policy rows, every attempted-candidate row,
  960,960 mixture/profile rows, and 3,003 aggregate mixture rows;
- nested schemas for 40 stratum metrics, six histogram bins, four secondary
  rational metrics, resource bindings, row counts, and failure counts; and
- required golden fixtures for primary, negative, zero-yield, mixture, invalid
  artifact, and full summary cases.

All cross-field constraints are deterministic: selected mixture entries sum to
eight, primary gain numerator is `A(D)-S_global(D)`, denominator is positive
`S_global(D)`, summary hashes match artifacts, and every error-code key is emitted
including zeros.

## Prediction ledger resolution

Before freezing, append exactly two unresolved rows specified in the contract to
`results.tsv`: low-confidence primary 5% and high-confidence negative zero. Freeze
records the hash of the complete pre-run ledger and all pre-outcome commands require
that exact hash.

After terminal output validates, and never before:

- for a valid primary result, set `metric_value` to the exact fixed-12 summary
  string; `signal=confirm,status=keep` iff materiality confirms, otherwise
  `signal=disconfirm,status=discard`;
- for a valid negative result, set `metric_value=0`, `signal=confirm,status=keep`;
- for any protocol-invalid result, set both values `NA`, `signal=null`, and
  `status=crash`;
- never change prediction, confidence, description, memory `NA`, or runtime `NA`.

The `resolve-ledger` command performs the one update only after summary validation.
Then a new research log records Prediction versus Reality, progress is appended,
and the resolved ledger, log, progress, and all terminal artifacts are explicitly
committed. The pre-run ledger remains recoverable at implementation commit `I` and
by the hash in `FREEZE.json`.

## One-way held-out custody state machine

The future protocol is a monotone chain:

```text
IMPLEMENTED → FROZEN → ACKNOWLEDGED → PULSE_PRESERVED
            → OPENED → EVALUATION_STARTED → COMPLETED
```

Any failure enters terminal `ABANDONED`. Every transition uses one exclusive atomic
file create; no two-file transaction is claimed.

1. **IMPLEMENTED→FROZEN.** From clean `HEAD=I`, freeze fetches and atomically
   preserves the exact nonempty `/pulse/last` HTTP response bytes as
   `freeze-anchor.raw.json`. Parsed JSON must satisfy the NIST envelope schema.
   Convert its ISO timestamp to integer milliseconds using `datetime.strptime`,
   UTC, and integer `calendar.timegm`; never float timestamp conversion. Set target
   exactly 1,440 periods (24 hours) later. Atomically create schema-valid
   `FREEZE.json`. Commit exactly these two artifacts as `F`, parent `I`.
2. **FROZEN→ACKNOWLEDGED.** Before target, post exact `F`, manifest hash, and target
   in this user thread and receive the exact `ACK`-prefixed string. Preserve
   `USER_ACK.txt` and schema-valid `PUBLICATION.json`, committing exactly them as
   `A`, parent `F`. No timely ACK permanently abandons the one freeze.
3. **ACKNOWLEDGED→PULSE_PRESERVED.** From clean `HEAD=A` and exact `I→F→A`
   paths/hashes, fetch the target after its time, validate the response in memory,
   require parsed returned milliseconds equal the requested target, then atomically
   preserve the exact raw bytes as `revealed-pulse.raw.json`. It is never fetched
   again.
4. **PULSE_PRESERVED→OPENED.** Parse only preserved bytes, derive the master in
   memory, then atomically create complete schema-valid `OPENED.json`, including
   `master_digest_hex`. Failure before/after this transition is terminal; a later
   invocation writes `ABANDONED` and does not resume.
5. **OPENED→EVALUATION_STARTED.** Atomically create schema-valid
   `EVALUATION_STARTED.json`. Failure/crash is terminal and cannot resume.
6. **EVALUATION_STARTED→COMPLETED.** Only now may a profile substream exist.
   Evaluate primary and negative together, validate every row and summary, then
   resolve the prediction ledger. A crash is terminal and cannot rerun.

The master is

```text
SHA256(ASCII("orf-heldout-v4|master|") || bytes.fromhex(outputValue)).
```

There is one freeze, one target fetch, one opening, and one evaluation start. No
seed, pulse, target, output-path, overwrite, retry, profile-count, or weighting
argument exists. Raw pulse files are never canonicalized or rewritten.

The pre-pulse user-thread ACK is a future custody checkpoint, not current
authorization for an external account action. No Kaggle command exists.

## Evidence and source validity

The contract hashes:

- `comp/sdk/aicomp_sdk/scoring.py:14,30-31,41-101` — weights, set score,
  denominator, saturation;
- `comp/sdk/aicomp_sdk/core/predicates.py:11,22-24,215-281` — literal sentinel,
  sink, EXFIL rule;
- `comp/sdk/aicomp_sdk/evaluation/ops.py:47,791-812` — candidate cap/deadline;
- gateway lines 55–63, 611–635, 740–770 — eight-hop and 9,000-second mechanics;
- `research-log/006-adaptive-multi-message.md` — controlled score geometry;
- official NIST description and pulse endpoint:
  <https://csrc.nist.gov/Projects/interoperable-randomness-beacons/beacon-20> and
  <https://beacon.nist.gov/beacon/2.0/pulse/last>.

Validity requires deterministic stationary exact probe continuation, additive
independent profile resources, no concurrency/cache/shared overhead, correct
predicate/hash construction, CPython/PRNG reproducibility, NIST forward
unpredictability, honest transcript custody, and execution of the exact frozen
code/schemas. Violating the first group invalidates the synthetic conditional-regret
interpretation; violating the second invalidates held-out status. None is asserted
for live models.

## Fixed bias surface

1. **Selection.** Support, equal cells, samplers, material threshold, one freeze,
   and terminal outcomes are fixed before realized parameters. The beacon does not
   remove prior analytical selection of support, so scope stays on this design.
2. **Confounding.** Same probes/resources isolate decision scope. Static and all
   3,003 class members expose probe-portfolio and fixed-mixture alternatives.
3. **Assignment.** Every policy is paired on every profile; policy-free keyed
   substreams and exact indices eliminate execution-order allocation effects.
4. **Protocol deviation.** Strict schemas, exact `I→F→A`, clean-head/hash checks,
   one-way one-file transitions, raw bytes, forbidden overrides, and no retry make
   deviations terminal rather than replaceable.
5. **Missing data.** Required aggregate/candidate rows cannot be omitted. Shared
   failure preserves partial data and abandons; policy failure zeros only its row,
   preserves unaffected rows, and invalidates the protocol.
6. **Measurement.** Source-hashed SDK code is authoritative; candidate-level traces,
   IDs, predicates, and raw equality are audited. The construct remains a noiseless
   finite oracle table.
7. **Analysis flexibility.** One exact estimand, weighting, primary contrast,
   threshold, binary falsification, subtype, regret identity, fixed controls, and
   no uncertainty/timing analysis are frozen.
8. **Selective reporting.** Frozen prediction rows, full-ledger hash, published
   pre-pulse freeze, exact ACK, one target, inseparable opening/evaluation start,
   terminal abandonment, deterministic ledger resolution, and mandatory commit of
   every artifact/status prevent replacing an inconvenient outcome.

## Failure modes and alternative explanations

- Different optima with negligible separation yield a positive-subthreshold
  disconfirmation.
- Cliff-heavy equal cells, integer floors, saturation, and novelty bonuses may
  cause material regret; stratum and separation outputs expose this limited domain.
- The generic advantage of 320 oracle choices over one is the exact narrow object,
  not proof of learnability.
- Denominator-eight mixtures do not span all fixed sequences.
- Noisy or drifting continuation can erase the result and requires a later
  hypothesis.
- Any timestamp, custody, schema, scorer, hash, numeric, negative, or row failure
  is terminal `NOT_EVALUABLE`, not scientific evidence.

## Taxonomy and anti-stacking

- **Opportunity:** Evidence Gap dominant; Resource Bottleneck secondary.
- **Method paradigm:** **Empirical Mapping dominant**; Optimization/Search
  secondary.
- **Dominant operation:** **replace** a split-global argmax with a
  profile-conditioned argmax.
- This is not Bridge Opportunity × Synthesis/Unification.

**Distinguishing prediction.** With identical probes and resources, profile
conditioning must clear a fixed material threshold on the crossed realization but
have exact zero conditional regret on the homogeneous realization. The global
control already includes the identical probe portfolio, so a fixed portfolio or
plain component combination cannot explain their paired difference.

Occam's scientific statement is only the finite conditional-regret prediction.
SDK, beacon, schemas, and custody are measurement/anti-tuning infrastructure, not
the mechanism.

## Self-critique and problem alignment

`Delta≥0` is algebra; only the material size is risky. The 5% threshold is
normative and low-confidence. The beacon hides realized parameter floats but not
the public generator, so prior analytical support selection remains possible. The
thread ACK is auditable custody, not a public cryptographic transparency log. The
test assumes perfect one-probe stationarity and cannot justify a deployable selector.

Confirmation would establish one necessary synthetic fact for `PROBLEM.md`: an
actually post-freeze coverage realization contains material profile-conditioned
structure value beyond identical probes and the best one-length global fill. It
would not answer the live four-cell objective.

## Decision

Dispatch one sterile round-8 theory re-review against this committed entry, v4
contract, and artifact schema. Do not implement, freeze, acknowledge, reveal,
evaluate, submit, or perform any Kaggle action before a rigorous verdict and later
explicit checkpoints.
