# v45 hop-1 validation refuted -> fill is REPLAY-bound; 87.255 is the ceiling

Date: 2026-08-13

v45 (hop-1 bulk validation, per-row coef gpt2.0/gem1.7) = **79.020**, vs v42 87.255.
Reverted to v42.

## Why it regressed (and what it proves)

Hop-1 validation halves generation cost. It can only raise the count if the fill
is GENERATION-bound. It regressed, which proves the fill is REPLAY-bound: the
returned count = replay_cap / true_replay_cost (physics), and generation was never
the binding constraint. Worse, the "conservative" per-row coefs charged MORE
replay than v42's exact-t8 (gemma 9.0 vs 8.23, gpt 6.7 vs 6.25) -> ~9% fewer
candidates -> 79.020.

Corollary: v42 (frac 0.98, 8-hop validation, coef 1.0) already charges the exact
replay cost and fills to the replay ceiling. Charging less to get more count would
overrun the real replay wall (blank, cf. v43 0.985). So 87.255 is the replay-bound
ceiling for this controller.

## Lever map — now complete

| lever | result |
|---|---|
| density / burst / multi-post | dead (real-CPU harness: single-post 2.61 raw/s optimal) |
| firing intensity | dead |
| frame wording | v35 harmony optimal |
| multi-predicate | guardrail-blocked |
| fill width (REPLAY_SAFE_FRAC) | peaks 0.98 (=87.255) |
| hop-1 validation | refuted -> replay-bound |

Every candidate-shape and count lever is exhausted. The score is a replay-throughput
race and we are at the replay ceiling for single-post. The only remaining unknown
is whether the frontier (114) uses a faster-replaying primitive we have not found;
real-CPU data says single-post at ~6-9s/candidate is already minimal.

## State

attack.py = v42 (frac 0.98 single-post), standing 87.255. No further lever
identified.
