# Hypothesis iteration 4 v9 — SDK-Faithful, Total, Recoverable Conditional Regret

**Supersedes:** `research-log/017-hypothesis-iter-4-v8-conditional-regret.md`
and all earlier ORF hypothesis entries  
**Date:** 2026-07-19 · **Phase:** 2 · **Cycle:** 1 · **Iteration:** 4 · **Status:** blocker-closure revision complete; unreviewed because the authorized theory-review budget is exhausted at 10/10

## Context and authorization boundary

Round 10 accepted the finite-regret algebra, homogeneous negative proof,
seed-domain assumption as conditional, taxonomy, anti-stacking contrast,
complete-only error semantics, and local staged outcome/ledger recovery. It did
not pass v8 because four implementation-facing statements were still false or
underdetermined.

The user then directed:

> ok, then lets fix these blockers properly. Remmebr to do the right thing not the easy thing

This authorizes a new append-only Phase-2 specification and public local checks.
It does not raise the hypothesis-review limit, authorize another reviewer
dispatch, or authorize a beacon request, target derivation, held-out profile,
held-out evaluator, submission, or Kaggle action.

V9 adds four immutable prospective artifacts:

- `experiments/configs/orf-heldout-v7.json` — executable scientific/custody
  contract, SHA-256
  `d53b5920d178ddee622bcb53283652006a0e4089a539d9c21e424ee7b67d5235`;
- `experiments/configs/orf-heldout-v7-artifacts.schema.json` — Draft 2020-12
  artifact schema, SHA-256
  `64d7ac6d775d92a6edcc22fc7925996aadd69c66c37aed339a9e45dcd4e3c321`;
- `experiments/poc/orf_v7_contract_reference.py` — public non-target reference
  checker, SHA-256
  `c707b5f9037420c88e737441182821940399e43c85439a986fd380f6051620ca`;
- `experiments/fixtures/orf-heldout-v7-golden-fixtures.json` — named preserved
  SDK, scheduler, and terminal-publication fixtures, SHA-256
  `fbc56f425786a670dee770509b3cf0380b48d292c6a1b72ebfe582725801b167`.

The reference checker has no fetch, target, profile-generation, evaluation, or
Kaggle code path. The future held-out run directory remains absent.

## Round-10 blocker dispositions

| Round-10 blocker | V9 structural resolution |
|---|---|
| SDK hash contradiction | `candidate_id` remains a 64-hex bookkeeping identity. `score_cell_hash` is now only the actual 16-hex `cell_signature(trace.tool_events)["hash"]`. The finding passes this real mapping through `get_score_cell_hash` and `score_attack_raw`; `core/cells.py` is the sixth required source hash. Cross-finding uniqueness is asserted per trajectory, and a collision invalidates rather than substituting an ID. |
| Undefined mixture scheduler | Each sum-eight tuple first constructs one immutable eight-slot cycle from `t=0..7`, cycle-local zero counts, explicit eligibility `count[i]<h[i]`, exact deficit maximization, and smaller-length ties. Execution is `cycle[j mod 8]`, so reset and repetition are explicit. Only an emitted attempt increments `j`; zero-yield attempts increment it; any precheck stop or saturation is terminal. All 3,003 cycles are execution-checked. |
| External post crash gap | Before an external call, the protocol atomically publishes a deterministic keyed `TERMINAL_POST_INTENT`. Freeze is forbidden unless the bound thread interface proves server-side idempotent create and linearizable keyed listing. Recovery always lists before create, never trusts a create response alone, and resolves to one exact immutable message receipt or a publication-failure artifact. |
| Unpreserved sample claims | V8's unverifiable generic root-sample claim is removed. V9 names one hashed fixture file containing two actual SDK traces, four exact mixture cycles, and three terminal artifact instances. The reference checker recomputes and schema-validates those preserved bytes. |

## Named concept

### Beacon-Held-Out Conditional Regret (ORF-B)

**Plain language.** Both compared policies keep the same seven probe candidates.
One policy must use a single fill length on every profile in a future synthetic
finite table. The other is an oracle allowed to choose a different length for
each profile after those same probes. ORF-B is the exact score lost by the common
choice restriction. A homogeneous companion table must have exactly zero loss.
This estimates oracle information value, not whether a live agent can learn the
oracle choices.

**Formal definition.** For primary split `D`, profile `z`, legal length `m`, and
exact post-probe objective `S_z(m)`:

```text
A(D)        = sum_z max_m S_z(m),
G(D)        = max_m sum_z S_z(m),
Delta(D)    = A(D)-G(D)
            = sum_z(max_m S_z(m)-S_z(m_global)) >= 0.
```

For every `z`, `max_m S_z(m)>=S_z(m_global)`, so summing proves the inequality.
This structural containment proves direction only. It does not prove a 5%
magnitude.

## Falsifiable claim and variables

**Claim.** On exactly one valid 320-profile future primary split, `ADAPTIVE` will
score at least `5.000000000000%` above `PROBE_GLOBAL_PRIMARY`. On the 64-profile
homogeneous split, `ADAPTIVE-PROBE_GLOBAL_NEGATIVE` will equal integer zero.

- **Independent variable:** per-profile versus split-global scope of the
  post-probe fill-length argmax.
- **`varies`:** `candidate-structure-policy`; **kind:** `metric`.
- **Dependent variable:** reduced exact `(A-G)/G`, with its fixed-12 percent.
- **Pre-specified primary comparison:** `ADAPTIVE` versus
  `PROBE_GLOBAL_PRIMARY`; no secondary comparison decides materiality.
- **Expected direction:** nonnegative by action-class containment.
- **Expected magnitude/confidence:** at least 5%, low confidence.
- **Controls:** identical profiles, keyed draws, retained probes, action set,
  candidate construction, actual SDK predicate/score path, generation/replay
  budgets, returned cap, saturation, arithmetic, and implementation.

Every valid result is decisive:

```text
CONFIRMED / MATERIAL
  iff 100*(A-G) >= 5*G;

DISCONFIRMED / ZERO
  iff A-G = 0;

DISCONFIRMED / POSITIVE_SUBTHRESHOLD
  iff 0 < 100*(A-G) < 5*G.
```

Negative `Delta`, a nonzero homogeneous difference, an actual score-cell
collision, or any contract violation is `PROTOCOL_INVALID`. Invalid execution is
not evidence for or against the magnitude and cannot trigger a scientific retry.

## Calibration evidence and exact scope of inference

Before its valid outcome, calibration v2 froze 64 public master labels, the same
40 factor cells, four weighting checks, two saturation settings, a cliff-floor
certificate, and an all-or-nothing support rule. V1 was rejected because Decimal
parameters were combined before exact Fraction conversion. V2 changed only that
numeric implementation: it retained the labels, predictions, threshold, factors,
and support.

The valid exploratory result was:

| Design | Masters clearing 5% | Minimum gain | Median gain |
|---|---:|---:|---:|
| Equal, `H=200000` | 64/64 | 34.575811113981% | 40.924155277025% |
| Balanced cliff presence, `H=200000` | 64/64 | 24.987661930465% | 32.324156091809% |
| No cliff only, `H=200000` | 64/64 | 5.117860088584% | 6.991608265969% |
| Cliff only, `H=200000` | 64/64 | 35.101784203438% | 39.796867096003% |
| Equal, `H=10^18` | 64/64 | 41.372040363181% | 44.204209608439% |

The calibration-to-target statement is explicitly conditional on all three:

1. SHA-256 behaves as a random oracle on the 64 distinct fixed labels and the
   distinct future prefix-plus-pulse input;
2. the selected future 512-bit NIST output is fresh uniform public randomness;
3. labels, prefixes, factors, and support were selected independently of any
   undisclosed outcomes—there was no hidden prefix or parameter search.

Under those assumptions the masters are iid-equivalent uniform 256-bit values and
the frozen PRNG induces comparable streams. Under iid Bernoulli indicators,
64/64 clearing 5% gives the exact one-sided 95% lower bound

```text
p_lower = 0.05^(1/64)
        = 0.95427029766923753936976169563270450199231817533648.
```

Forward unpredictability alone is insufficient. Reject any condition and the 64
masters are only deterministic exploratory coverage with no probability statement
about the future target. Calibration cannot confirm the future prediction.

## Actual SDK score identity

The scoring premise now follows the real frozen call graph:

```text
trace
  -> core/predicates.py::eval_predicates(trace)
  -> core/cells.py::cell_signature(trace["tool_events"])
  -> scoring.py::get_score_cell_hash(finding)
  -> scoring.py::score_attack_raw(findings).
```

For a positive constructed candidate, `candidate_id` is the full 64-hex SHA-256
of the contract's bookkeeping preimage. It is used only to construct distinct
`.invalid` URL domains and to identify the ledger row. For each event ordinal
`j=0..e-1`, the canonical trace has exactly one successful `http.post` with
`SECRET_MARKER`, source `user`, side effect `SHARE`, and the candidate-ID-derived
URL. The canonical user message explicitly authorizes sending, preventing an
unrelated confused-deputy predicate.

The evaluator must obtain exactly `e` severity-5 `EXFILTRATION` predicates and no
other predicate. Its `score_cell_signature` is the actual SDK mapping computed
from tool events with default arguments. Its hash is exactly 16 lowercase hex.
It is never injected and never equated to `candidate_id`.

For a singleton actual finding:

```text
q_z(m) = score_attack_raw([finding]) = 16*e_z(m)+2.
```

For zero events there is no finding and `q=0`. For every complete
`(split,profile,policy)` trajectory, actual retained hashes must be pairwise
unique before the `+2`-per-candidate shortcut is used. A 64-bit hash collision
makes the protocol invalid with `SCORE_CELL_COLLISION`; it is not repaired by
candidate identity. The trajectory objective is recomputed once from the entire
actual finding list and capped at 200,000.

Two preserved traces check the frozen implementation directly:

| Fixture | Events | Actual hash | Actual singleton raw |
|---|---:|---|---:|
| `one_exfil_event` | 1 | `5e9eb759f70d68e2` | 18 |
| `three_exfil_events` | 3 | `94d8f2e731ea0c18` | 50 |

The source set now contains six exact hashes, including
`comp/sdk/aicomp_sdk/core/cells.py` at
`2fc9cbe5b2488b3f3c472cb31787de2b6a50aa29dd1abf2a67366ffd2b9d7369`.

## Exact arithmetic and profile generator

Resource constants are `B_gen=9000`, `B_rep=8100`, `C=2000`, and `H=200000`.
`B_rep` is a synthetic deterministic budget, not a live deadline-tail guarantee.

Execution is CPython 3.14.3 with libmpdec 4.0.1 and a precision-80,
half-even local Decimal context. Every PRNG float is converted through its exact
binary ratio. LogUniform uses the frozen libmpdec `ln/exp`. Each realized Decimal
parameter is converted separately to `Fraction` before polynomial cost arithmetic.

Cliff events are

```text
r=m*exp(-lambda*(m-k)/k),
e=clamp(floor(r),0,m).
```

Every `r` must remain at least `1E-60` from the nearest integer. Failure
invalidates the single realization without regeneration.

The primary split crosses 40 equal cells: reset `{LOW,HIGH}`, linear
`{LOW,HIGH}`, curvature `{NONE,HIGH}`, and cliff `{-1,4,8,16,24}`. Eight keyed
replicates produce 320 profiles. The negative split has 64 profiles with exact
`c(m)=bF*m,e(m)=m`. Draw order, ranges, index formulas, and equal weighting are
frozen in the contract.

## Single-length policies

Probe lengths are `{1,2,4,8,16,24,32}`, once in ascending order. With common
probe generation `gF`, retained probe count `p`, replay `rF`, raw `Q`, exact cost
`cF(m)`, and positive singleton score `q(m)`:

```text
n(m)=max(0,min(
  C-p,
  floor((B_gen-gF)/cF(m)),
  floor((B_rep-rF)/cF(m)),
  0 if Q>=H else ceil((H-Q)/q(m))
)),
S_z(m)=min(H,Q+n(m)q(m)).
```

Zero `q` yields no fill. `ADAPTIVE` argmaxes per profile. Primary and negative
global policies independently argmax their split aggregate. Ties choose smaller
length. Static no-probe policies and a per-profile static oracle are frozen
secondary controls.

## Total mixture scheduler

The mixture class is all 3,003 ascending lexicographic nonnegative seven-tuples
`h` summing to eight. V9 separates cycle construction from resource execution.

For each `h`, construct one immutable `cycle_h`:

```text
count = [0,0,0,0,0,0,0]
for t in 0..7:
    eligible = {i : count[i] < h[i]}
    i_star = argmax_i ((t+1)*h[i] - 8*count[i], tie=smaller length[i])
    cycle_h[t] = length[i_star]
    count[i_star] += 1
assert count == h
```

Execution initializes emitted mixed-attempt index `j=0`; its next intended action
is always `cycle_h[j mod 8]`. That definition fixes origin, range, eligibility,
cycle reset, repetition, and count scope.

For the intended action, compute exact `c,e,q` before charging. Insufficient
generation stops before all attempts. For a positive action, zero candidate slots
or insufficient replay also stops before the attempt. Every precheck stop is
terminal and does not increment `j`. Otherwise emit one attempted row, charge
generation, and increment `j` even for zero yield. A zero-yield attempt retains
nothing and continues. A positive attempt charges replay, consumes a candidate
slot, retains the actual SDK finding, and updates the objective. Saturation stops
immediately after the crossing retained finding. No row follows any stop.

Positive costs and finite generation make even an all-zero cycle terminate. All
3,003 cycle constructors were execution-checked to finish with `count==h`. The
selected mixture maximizes the exact 320-profile aggregate, with lexicographically
smaller `h` breaking an aggregate tie.

## Exact metrics and homogeneous invariant

Let `A,G,T,O,M` be primary adaptive, probe-global, selected static, static oracle,
and selected mixture aggregates. All denominators are positive. Report exact
reduced rationals for:

```text
primary                 = (A-G)/G,
adaptive_over_static    = (A-T)/T,
adaptive_over_mixed8    = (A-M)/M,
signed_oracle0_gap      = (A-O)/O,
probe_generation_share = P/U.
```

The primary decision uses only the first.

For the homogeneous split, probes cost `87b` and score `1406`. The remaining
replay in cost-`b` units is `T=8100/b-87`, which lies in `[588,1533]` for
`b in [5,12]`. Candidate and generation constraints are looser. For `m>=2`:

```text
floor(T/m)(16m+2) <= 17T < 18(T-1) <= 18floor(T).
```

Thus `m=1` uniquely maximizes each profile, so adaptive and independently chosen
negative global aggregates are exactly equal. This is a code invariant, not
additional evidence for the 5% magnitude.

## Complete-only scientific artifacts

Final TSVs contain no error rows. Every candidate row is an emitted attempt;
ordinals are contiguous; action fields equal the exact schedule; `candidate_id`
is 64 hex; `score_cell_hash` is actual 16 hex or `NA`; and positive/zero
biconditionals are exact. A profile, generator, predicate, score, uniqueness,
policy, numeric, schema, or row error aborts to invalid outcome. Partial staging
bytes may be preserved as non-authoritative evidence but cannot enter metrics.

`OUTCOME.json` is a scientific union: `VALID` binds the complete summary and
decision; `PROTOCOL_INVALID` binds the last scientific state, reason, partial
counts, and `NA/null/crash` resolutions. Before root `results.tsv` changes, the
protocol atomically publishes immutable `RESOLVED_RESULTS.tsv`. Local mirroring
and terminal logging occur under a hashed `WORKSPACE_TRANSACTION`; exact
after-hashes yield `COMPLETED`, while any third destination hash yields
`TERMINALIZATION_FAILED` without rewriting scientific outcome.

The same-directory stage/write/fsync/link/fsync/unlink/fsync algorithm from v8
remains normative for authoritative new files. Exact before/after hashes make
root-file replacement idempotent. A future freeze requires disposable proof of
the specified POSIX primitives on one filesystem/device and an exclusive flock.

## External terminal publication recovery

Local atomicity cannot close a crash between an external post being accepted and
its receipt being stored. V9 therefore makes external semantics a precondition,
not an optimistic assumption.

Before freeze, the implementation must bind one thread and preserve authenticated
capability evidence that its interface provides:

1. server-side idempotent `create(message,key)`: repeated same-key/same-payload
   calls return the same immutable message ID, and same-key/different-payload is
   rejected;
2. linearizable `list(thread,key)`: it returns all immutable matching posts and
   their exact bytes.

If proving those semantics would require an unauthorized external test, or the
interface does not provide them, freeze is forbidden.

After local terminalization, compute a canonical payload from thread, terminal
commit, statuses, and hashes. Derive

```text
key = SHA256(b"orf-terminal-post-v1\0" + canonical_json(payload)).hexdigest().
```

Atomically publish `TERMINAL_POST_INTENT.json` containing the exact keyed message
before any external call. Recovery under the workspace lock always performs
`list(thread,key)` first:

- one exact match: publish a receipt with its immutable message ID/hash;
- zero matches: call idempotent create, then return to list regardless of the
  response;
- multiple matches, mismatched bytes, capability failure, or permanent
  authenticated rejection: publish `TERMINAL_PUBLICATION_FAILED.json` and never
  create again.

No receipt is inferred solely from a create response. A crash before intent makes
no external call. A crash after accepted create is recovered by the keyed list.
A repeat cannot duplicate the post under the required server contract. This
closes crash recovery conditionally on those frozen interface semantics; it does
not cryptographically prevent a dishonest operator from suppressing both post and
repository.

## One-way future chain

```text
IMPLEMENTED -> FREEZE_FETCH_STARTED -> FROZEN -> ACKNOWLEDGED
 -> TARGET_FETCH_STARTED -> PULSE_PRESERVED -> OPENED
 -> EVALUATION_STARTED -> OUTCOME_RECORDED
 -> RESOLVED_LEDGER_PUBLISHED -> WORKSPACE_TRANSACTION_PUBLISHED
 -> COMPLETED_OR_TERMINALIZATION_FAILED
 -> TERMINAL_POST_INTENT_PUBLISHED
 -> TERMINAL_PUBLICATION_CONFIRMED_OR_FAILED.
```

This chain is prospective only. There is no evaluator, freeze, ACK, target GET,
master, profile table, result, or terminal post. Scientific evaluation may never
resume after outcome; only pure terminal recovery may resume.

## Fixed bias surface

1. **Selection.** The future target is hidden, but factor ranges, equal weights,
   cliff prevalence, support, and threshold are engineered. Calibration inference
   additionally requires independent label/prefix/parameter selection.
2. **Confounding.** Same profiles, probes, action family, resources, and actual
   SDK score isolate action-scope relaxation on the finite table. Engineered
   heterogeneity, cliffs, floors, saturation, and novelty can explain magnitude.
3. **Assignment.** Paired complete evaluation and policy-free keyed streams remove
   order assignment only under independent deterministic per-profile resources.
4. **Protocol deviation.** Pre-GET markers, no scientific retry, exact source and
   artifact hashes, actual SDK fixtures, and total schedulers make deviations
   observable or invalid.
5. **Missing data.** Only complete final ledgers enter metrics. Partial prefixes
   resolve as invalid through the immutable resolved-ledger sidecar.
6. **Measurement.** Actual `eval_predicates`, `cell_signature`,
   `get_score_cell_hash`, and `score_attack_raw` define the score; candidate
   identity never substitutes for measurement identity.
7. **Analysis flexibility.** One primary contrast, threshold, exact secondary
   formulas, bins, and outcome mappings are frozen.
8. **Selective reporting.** Pre-target ACK, local terminal artifacts, and keyed
   external recovery mitigate suppression under honest operation but cannot
   prevent deliberate concealment.

## Assumptions, failure modes, and alternatives

Scientific validity assumes deterministic stationary traces, additive independent
per-profile resource accounting, no cross-profile cache/concurrency/shared
overhead, fully observed values for all seven actions, the exact frozen SDK files,
and exact numeric execution. Violations destroy the finite table or change the
claim to a learning/live-systems question.

Custody validity assumes honest git/thread operation, the preflighted POSIX model,
and the server idempotency/linearizable-read contract. Without the external
capability, the correct action is not a weaker receipt algorithm; it is to refuse
freeze.

Confirmation could reflect generic 320-choice flexibility, deliberate cliff
oversampling, cost-band separation, integer floors, saturation, novelty bonus, or
their interactions. The experiment maps their combined frozen finite-table
magnitude. It does not identify a population mechanism, live prevalence, private
transfer, or a deployable selector. Any positive result below 5% falsifies the
materiality hypothesis.

## Taxonomy, anti-stacking, Occam, and alignment

- **Opportunity:** Evidence Gap dominant; Resource Bottleneck secondary.
- **Method:** Empirical Mapping dominant; Optimization/Search secondary.
- **Operation:** **replace** one split-global optimizer with profile-conditioned
  optimizers.
- **Default-template tripwire:** not Bridge Opportunity ×
  Synthesis/Unification; the operation is local replacement, not integration.

**Distinguishing prediction.** With identical retained probes and candidate
construction, profile conditioning must be materially better on the crossed table
yet exactly equal on the homogeneous table. A plain portfolio or union of
components does not predict that paired action-scope pattern.

The simplest accurate statement is: on one engineered future finite table, 320
profile-wise maxima may materially exceed one common maximum; on a homogeneous
table they coincide. Beacon custody, schemas, reference fixtures, and transactions
measure that statement; they do not explain it and are not claimed as scientific
components.

**Problem alignment.** Confirmation would establish that future realized
post-probe profile information has material synthetic value beyond the best common
fill under the benchmark-shaped constraints. It would not establish Kaggle
improvement, private transfer, live latency safety, or learnability.

## Deterministic and execution-based verification

The preserved public checker was run as:

```text
comp/.venv/bin/python -I experiments/poc/orf_v7_contract_reference.py \
  --contract experiments/configs/orf-heldout-v7.json \
  --schema experiments/configs/orf-heldout-v7-artifacts.schema.json \
  --fixtures experiments/fixtures/orf-heldout-v7-golden-fixtures.json
```

Its output was:

```text
contract_version=orf-heldout-v7
sdk_golden_cases=2 score_hashes=5e9eb759f70d68e2,94d8f2e731ea0c18
mixture_compositions=3003 cycles_exact=3003
terminal_artifact_samples=3 schema_valid=true
source_hashes=6 valid=true
protocol_errors=24 validators=18 aligned=true
fixtures_sha256=fbc56f425786a670dee770509b3cf0380b48d292c6a1b72ebfe582725801b167
heldout_run_absent=true
```

Separately, both JSON artifacts parse, the schema passes Draft 2020-12
metaschema validation, all four artifact hashes match those recorded above, and
`git diff --check` passes. These checks close deterministic defects; they are not
an independent theory judgment and do not spend or replace a review round.

## Gate status and decision

V9 is the active superseding hypothesis specification for future consideration.
It is not `RIGOROUS`: the only authorized hypothesis-review budget is exhausted at
10/10 and no new dispatch was authorized. Therefore Phase 2 remains closed.

Do not append prediction rows, implement a held-out evaluator, freeze, fetch a
beacon pulse, generate a target/master/profile, evaluate, post a terminal result,
or perform any Kaggle action under this revision. A future transition requires
explicit user authorization appropriate to the next action and, for scientific
progress, a separately authorized independent review that returns `RIGOROUS`.
