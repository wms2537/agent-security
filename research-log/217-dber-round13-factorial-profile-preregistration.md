# DBER round-13 repair — four-policy factorial profile preregistration

Date: 2026-07-26  
Phase: 2  
Task: T088  
Status: frozen before instrumentation, harness implementation, or execution

## Decision this profile must make

Round-13 review showed that the generation-stop classifier has no measured
incremental role. A simpler policy applies the same bounded packing rule whenever
headroom exists. Under the frozen model, that headroom-only policy is identical
to generation-gated DBER on the existing generation profile, identical on
controls where nothing fits, and strictly better whenever a smaller successful
probe fits after a replay-bound incumbent stops.

This profile does not attempt to rescue DBER. It must decide whether the
generation classifier earns distinct safety credit. If it does not, the
generation gate is removed from the next hypothesis.

## Immutable inputs

The pre-instrumentation identities are:

- `experiments/attack.py`:
  `efac97119321c2cafdd1f0df87e756d206a59073ffbd1ebd4f7bf95d52fea883`
- `experiments/dber_profile.py`:
  `e004d29e18e96044c1ce2c79acec19aac4aab6e01178ce0522dc1a9969530c37`
- `experiments/mock_agents.py`:
  `5103115cd9a5e2265837bf4971b1e12804b678522133a61d2fdb0c7734bedd4c`
- official replay operations:
  `455a835e0a58abab79b24c986a937b99712e69ef83d6068fc68873e3c051fe74`
- official scoring:
  `13a0969ea6c64b257c46d47490b4259ade3a4965f19d2d6c6fe0ed151f618d4f`
- official predicates:
  `9d9de5118d8883a0074a5405ed85cf2dec3f68e8516908cbc48f409e3ba56f37`
- official cell signatures:
  `2fc9cbe5b2488b3f3c472cb31787de2b6a50aa29dd1abf2a67366ffd2b9d7369`

Runtime is CPython 3.14.3 on local x86_64 CPU. Execution is single-process and
sequential. No profile unit may be dropped because it is inconvenient; a crash,
timeout, unexpected binding, or missing artifact remains an invalid unit in the
complete population.

## Behavior-neutral controller instrumentation

The only permitted change to `experiments/attack.py` before this profile runs is
to expose the exact fill-loop terminal state in `self.debug`:

- which ordered loop guard failed: candidate cap, replay cap, or generation
  deadline;
- exact unrounded `unit`, accumulated replay estimate, safe cap, candidate count,
  and candidate cap at the terminal check;
- how many candidates the existing late-overage clamp removed.

The fill loop, candidates, messages, ordering, timing calls, thresholds, and
fallbacks must not change. A regression test must compare candidates from the
pre-instrumentation and instrumented modules under deterministic clock/env
fixtures. If candidate messages differ, the whole profile is invalid.

## Profile population

Every one of the following 12 units is included: four named regimes crossed
with seeds `41`, `42`, and `43`. Unit order is regime order below, then ascending
seed. All use:

- `OptimalGuardrail`;
- `EnvSelection.SANDBOX`;
- packaged fixtures under `comp/sdk/aicomp_sdk/fixtures`;
- `max_tool_hops=8`;
- `probe_reps=5`, `probe_time_cap_s=0.90`, `min_fire_rate=0.2`;
- `replay_safe=0.99`, `cost_inflation=1.0`, `gen_margin_s=0.05`;
- `multi_probe_reps=2`, `multi_probe_messages=6`,
  `multi_fill_messages=24`, `multi_min_fire_fraction=0.75`,
  `multi_rate_gain=1.10`;
- `enable_scoc=false`;
- active candidate cap `L` equal to the regime's `max_candidates`, with
  `L <= 2000`.

### G — generation-wide

- agent: existing `AmortizingAgent(fixed_latency_s=0.015,
  per_action_latency_s=0.001)`;
- generation budget: `4.00 s`;
- replay budget: `6.00 s`;
- candidate cap: `200`;
- multi-message routing enabled.

This unit must terminate on the directly recorded generation guard. It measures
whether either bounded reuse policy can recover positive marginal official raw
score with ample replay/candidate headroom.

### R0 — replay-bound, no residual fit

- agent: existing `AmortizingAgent(fixed_latency_s=0.015,
  per_action_latency_s=0.001)`;
- generation budget: `3.00 s`;
- replay budget: `0.18 s`;
- candidate cap: `200`;
- multi-message routing enabled.

This unit must terminate on the directly recorded replay guard, and no
positive-marginal probe may pass the alpha-stressed packing constraint. It is the
no-fit replay control.

### R1 — replay-bound, smaller probe can fit

- agent: new controlled `IndexSplitLatencyAgent` declared here before code:
  it always follows the existing compliant http.post behavior; on each agent
  action it parses the numeric `x<index>.example` destination from the latest
  user message and sleeps `0.002 s` when `index >= 900000`, otherwise `0.020 s`;
  malformed or absent indices use `0.020 s`; reset/snapshot/restore are stateless;
- generation budget: `3.00 s`;
- replay budget: `0.18 s`;
- candidate cap: `200`;
- multi-message and SCOC routing disabled.

Attack probes use indices beginning at `900000`; fill candidates begin at zero.
This is an adversarial resource fixture, not target-efficacy evidence. It creates
the exact case omitted from report 215: a replay-bound incumbent whose next fill
candidate is too expensive while at least one already-successful probe is
smaller. The direct replay guard and at least one safe headroom-only admission
are required for a valid R1 unit.

### K — candidate-bound

- agent: existing `AmortizingAgent(fixed_latency_s=0.015,
  per_action_latency_s=0.001)`;
- generation budget: `3.00 s`;
- replay budget: `6.00 s`;
- candidate cap: `3`;
- multi-message routing enabled.

This unit must terminate on the directly recorded candidate guard. All bounded
policies must return the incumbent exactly because `K=max(0,L-|C|)=0`.

## Complete official-replay measurement

Generation is traced transparently. Each episode retains its complete trace and
elapsed time. After generation, every deduplicated incumbent and successful
discarded probe is replayed independently through the official lifecycle:

1. start the timer;
2. construct a fresh environment with `build_attack_env`;
3. reset it;
4. replay every candidate message in order;
5. export the trace;
6. call `eval_predicates`;
7. compute both canonical and score-driving `cell_signature`;
8. stop the timer.

The full replay measurement therefore includes fresh environment/agent/guardrail
construction and predicate/signature work. No already-built environment is
reused across candidate replays.

For each candidate the durable JSONL record must contain:

- unit id, source phase, seed, ordered messages, canonical message signature;
- generation trace and SHA-256;
- generation elapsed time;
- official generation predicates and both cell signatures;
- full replay trace and SHA-256;
- full replay elapsed time;
- official replay predicates and both cell signatures;
- isolated official raw;
- marginal official raw against the incumbent/current packed prefix;
- admission and rejection reason for each policy.

An independent verifier must reload the JSONL, reconstruct every portfolio from
messages and policy decisions, recompute official raw with `score_attack_raw`,
and match the summary exactly. A proxy raw formula is forbidden.

## Four frozen policies

Let:

- `C` be the ordered incumbent list returned by the unchanged controller;
- `P` be the nonempty, message-deduplicated successful probe inventory absent
  from `C`;
- `L` be the active cap for the unit, `1 <= L <= 2000`;
- `K=max(0,L-|C|)`;
- `B=0.99 * replay_budget_s`;
- `g(x)` be the observed generation-episode elapsed time for candidate `x`;
- `R_g(C)=sum(g(c) for c in C)`;
- `DeltaRaw(p | A)=raw(A appended with p)-raw(A)` using the official scorer;
- `alpha=2.0`, an accounting stress factor only, not a probabilistic guarantee.

Inventory items are considered in stable order:

1. descending positive `DeltaRaw(p | current_prefix)/(alpha*g(p))`;
2. ascending `alpha*g(p)`;
3. lexicographic canonical message signature.

Policies are:

1. **INCUMBENT:** return exactly `C`.
2. **HEADROOM_ONLY:** when `P` is nonempty and `K>0`, greedily append at most
   `K` positive-marginal items while
   `R_g(C)+sum(alpha*g(p)) <= B`; otherwise return exactly `C`.
3. **GENERATION_GATED:** return `HEADROOM_ONLY` only when the controller's
   directly recorded stop reason is generation; otherwise exactly `C`.
4. **BANK_ALL:** append every positive-isolated-raw item in stable signature
   order until the active candidate cap, without a replay-cost guard.

Portfolio safety is evaluated separately from admission using the sum of full
fresh-replay elapsed times. This prevents the policy's generation-time estimate
from also defining its own success.

## Frozen predictions and decision rule

All 12 units must satisfy identity/cap/provenance invariants. Regime-level
predictions apply to each of its three seeds:

- G: `HEADROOM_ONLY == GENERATION_GATED`, both have positive official marginal
  raw over INCUMBENT, and neither exceeds actual replay/candidate limits.
- R0: `HEADROOM_ONLY == GENERATION_GATED == INCUMBENT`; BANK_ALL exceeds the
  actual replay cap.
- R1: HEADROOM_ONLY has positive official marginal raw over INCUMBENT and stays
  within actual replay/candidate limits; GENERATION_GATED equals INCUMBENT;
  BANK_ALL exceeds the actual replay cap.
- K: `HEADROOM_ONLY == GENERATION_GATED == INCUMBENT`; BANK_ALL may not exceed
  the active candidate cap because output is clamped to `L`.

The generation classifier earns a distinct role only if, across all valid
units, it prevents at least one actual replay/candidate overflow that
HEADROOM_ONLY incurs while never rejecting a safe positive-marginal admission.

If HEADROOM_ONLY has zero actual overflows and R1 confirms safe positive gain,
the generation classifier is rejected as dominated. The next hypothesis must
be the simpler bounded headroom-only mechanism and must not claim
generation-binding specificity.

If R1 fails because no probe fits, the profile is inconclusive and cannot be
relabelled as support. If HEADROOM_ONLY overflows, alpha=2 is refuted for this
population; no implementation or Kaggle action follows without a new
cost-calibration hypothesis.

## Scope boundary

These are controlled real-SDK mock resource fixtures. They can select between
mechanisms and validate evaluator/accounting semantics. They cannot establish
target-model firing prevalence, private/final transfer, leaderboard gain, or
submission confidence.

No Kaggle push, commit run, or submission is part of this profile.
