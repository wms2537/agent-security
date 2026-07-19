# Multi-post ceiling source audit

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** completed

## Context

T003 predates the ORF hypothesis and asks whether the forced replay
`max_tool_hops` permits a higher-post candidate than the current 24-message
default. This audit is local and read-only; it performs no Kaggle action.

## Content

The gateway constrains two different dimensions:

- each attacker **message** is replayed with `DEFAULT_MAX_TOOL_HOPS=8`; and
- each finding may contain at most
  `MAX_REPLAY_MESSAGES_PER_FINDING=32` user messages.

The replay loop iterates all validated user messages and applies the eight-hop
cap independently to each. Therefore eight tool hops is not an eight-post
candidate ceiling. A 32-message candidate is source-legal.

No code addition is needed: `experiments/attack.py` already exposes
`multi_fill_messages`, clamps it to `_MAX_REPLAY_MESSAGES=32`, and constructs one
message per requested post. Setting `multi_fill_messages=32` is the higher-post
variant. Whether it is latency-safe on live models remains unmeasured and cannot
be inferred from the source audit.

## Gate Check

- Local constructor verification returned
  `m32_local_capability=PASS configured=32 messages=32 overrequest_clamped=32`.
- Source grep returned
  `comp/sdk/aicomp_sdk/evaluation/ops.py:48:MAX_REPLAY_MESSAGES_PER_FINDING: Final[int] = 32`
  and gateway lines 634–635 show `for msg in user_messages` followed by replay at
  `DEFAULT_MAX_TOOL_HOPS`.
- No repository code changed and no Kaggle/network action occurred.

## Problem alignment

This separates the legal candidate-shape ceiling from the replay-latency safety
constraint, preventing a false structural limit from truncating online candidate
optimization.

## Decision

Close T003. Treat M32 as a source-legal configuration, not a performance claim.
Any later live use would require a separately authorized, preregistered latency
experiment with a tail-risk target.

## Next Steps

Proceed with the active ORF Phase-4 public non-target experiment plan.
