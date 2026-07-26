# DBER full-lifecycle cost identifiability audit and retirement

Date: 2026-07-26  
Phase: 2 to 5  
Task: T089  
Decision: retire DBER and headroom-only evidence reuse

## Question

Can the attack-side controller conservatively estimate the full fresh-replay cost
that invalidated 9 of 12 frozen units, without importing a mock-specific
constant or observing post-return evaluator behavior?

No.

## Source trace

The official attack-side protocol exposes:

- `seed`;
- `reset`;
- `interact`;
- `export_trace_dict`;
- `snapshot`;
- `restore`.

`_OpaqueAttackEnv.__dir__` is exactly that surface. It exposes neither an agent
factory nor a guardrail factory, environment constructor, evaluator deadline,
candidate replay result, or replay-duration feedback.

The evaluator builds the generation environment once before the attack runs:

```text
run_env = OpaqueAttackEnv(build_attack_env(...))
run_env.reset()
attacker.run(run_env, run_config)
```

After the attack returns, each candidate is replayed in a separate hidden phase.
For every candidate, `_replay_candidate_trace`:

1. validates messages;
2. calls `build_attack_env` with a fresh agent and guardrail;
3. resets;
4. interacts;
5. exports the trace;
6. later computes predicates and signatures.

The Kaggle gateway implements the same separation. It constructs one real
generation environment, drives the attack through a command-response protocol,
then creates a fresh replay environment for each candidate under public and
private guardrails. Each replay phase has its own `9000 s` deadline.

The attack code cannot observe any replay-phase clock or result.

## Non-identifiability argument

Let the attack observe generation-side episode data:

```text
O = {(messages_i, generation_elapsed_i, projected_trace_i)}
```

Let complete evaluator replay cost be:

```text
T = sum_i(g_i + h_i)
```

where `g_i` is interaction/reset work represented in `O`, and `h_i` is hidden
fresh-environment, agent/guardrail construction, transport, predicate,
signature, scheduling, and evaluator bookkeeping work.

Two evaluator executions can produce the same attack-side `O` while differing
only in `h_i`; the attack returns the same candidate list in both, but one can
fit the replay deadline and the other can time out. Therefore `h_i`, replay
slack, and `T` are not identified by the attack-side observation.

The official interface gives no finite upper bound on `h_i`. A static additive
constant learned from the local mock is not a proof for remote GPT-OSS, Gemma,
public guardrail, or private guardrail cells. A multiplicative factor has the
same problem and, in run04, `alpha=2` already fails.

## Candidate repairs considered

### Local additive overhead

Run04 estimates a local mean additive gap of roughly `0.07–0.08 s` per verified
fill candidate. This is precise for that committed CPU/mock process and not
transportable to remote model servers or the private guardrail. Reject.

### Stress every incumbent and supplement cost

Applying a larger multiplier to the whole portfolio would correctly reveal that
the low-budget run04 incumbents are unsafe. No target-calibrated multiplier or
finite guarantee exists, so choosing one would be arbitrary. Reject.

### Infer slack from completed live submissions

Refs `54923079`, `54922298`, and `54920038` completed, so their hidden replay
totals were below the applicable deadline. Kaggle exposes no episode-level
diagnostics for these refs (`No episodes found`) and no per-cell replay duration.
Completion yields only the right-censored fact `T <= 9000 s`; it does not reveal
`9000-T`, so it cannot justify one additional candidate. Reject.

### Substitute probes for returned fill candidates

Replacing a successful fill with a successful single-post probe preserves count
and approximate cost but also preserves the same 18-raw structure. It cannot
explain or predict a gain. It is safe but useless. Reject.

## Retirement

The original generation-gated DBER is weakly dominated by headroom-only under
its own cost model. The stronger full-replay profile then refutes the shared cost
model. The missing variable is hidden by the official attack interface and
cannot be repaired with attack-side engineering alone.

Therefore:

- do not implement either reuse policy in the returned candidate path;
- do not re-review report 215;
- do not tune alpha or an additive constant on run04;
- do not submit a DBER variant to Kaggle;
- preserve reports 215–221 and run04 as a complete negative chain.

This is a mechanism retirement, not a claim that the active 81.225 live
incumbent is invalid.

## Competition-facing consequence

The next useful direction must improve score without adding an unmeasured amount
of replay work. The strongest admissible family is per-candidate latency/quality
engineering:

- preserve or reduce candidate count;
- preserve the replay-safe single-post floor;
- test protocol-native tool-call wording that reduces model response latency;
- use sequential elimination so a larger wording bank does not consume the
  generation budget;
- exclude the already-refuted one-message multi-post design and the refuted SCOC
  shorthand path;
- require an online distinguishing prediction in measured raw per replay second,
  plus exact fallback identity when no candidate beats the incumbent template.

That is a new research dimension, not a DBER revision. It requires a new
research-iteration authorization because Cycle-3 research is now `6/6`.

No Kaggle action occurred.
