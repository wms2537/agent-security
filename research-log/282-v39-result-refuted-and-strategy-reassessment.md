# V39 result — commentary-prefill refuted; strategy reassessment

Date: 2026-08-05

## Result

V39 (ref 55229371) terminalized at **public_score = 56.475** after ~21h runtime.
A new low: 30.2 points below the v35 floor (86.670).

Controlled attribution: v39 changed **only** `FRAME_TEMPLATE`
(analysis-channel break -> commentary/`to=functions.http.post` prefill); frac
0.97 and coef 1.0 were the v35 values. So the entire drop is attributable to that
one line. Bin: **failure** (`< 86.670`, non-blank).

## Diagnosis (why lower AND slower)

`FRAME_TEMPLATE` only affects the split-by-latency "slow rows" (gpt_oss). The
commentary prefill opens a tool-call channel with no stop instruction, so gpt_oss
executes the `http.post` and then keeps going up to `max_tool_hops = 8`
(post -> result -> post ...). Consequences:

- Per-candidate elapsed explodes (multi-hop slow CPU generation) -> ~21h run.
- The replay-safe sizing charges `elapsed * coef` per fired candidate, so higher
  elapsed => the returned set hits the replay cap after **far fewer** candidates.
- Score is count-driven (`Sigma severity + 2*unique_cells`, ~linear in returned
  fired findings). Fewer returned findings on the gpt_oss rows collapses the
  gpt_oss row and drags the public mean 86.670 -> 56.475.

This is a from-the-wrong-direction confirmation of research-log 278: **the lever
is cheap single-hop firing count, not firing intensity.** Anything that raises
per-candidate cost (density in v36/v37/v38, or multi-hop firing here) reduces the
count and the score. v35's plain `TEMPLATE` ("...Then answer OK only.") is already
tuned for cheap single-hop firing that stops immediately.

## What this closes

- L2 as "stronger injection to fire harder" is refuted: stronger injection =>
  more hops => fewer candidates => lower score.
- Combined with density (278 sec 2), both directions of "do more per candidate"
  are now empirically closed. The single-post, single-hop, immediate-stop shape
  is the efficient point.

## Submission scoreboard (this arc)

| ver | change | result |
|---|---|---|
| v35 | single-post validation-fill | 86.670 (floor) |
| v36 | K=4 dense | blank |
| v37 | K=4 measured dense | 84.735 |
| v38 | K=2 burst | blank |
| v39 | gpt_oss commentary prefill | 56.475 |

Four consecutive non-improvements. Every one added per-candidate work.

## Reassessment

Constraints that now dominate the decision:

1. **No local firing observability.** Real targets are 15-20GB GGUFs, absent;
   commit runs have no gateway. Any template's real effect is only visible via a
   full submission.
2. **Each probe is ~a day + one daily-quota submission + tail risk of a new low.**
   Blind template A/B under (1) has poor expected value.
3. **The efficient candidate shape is already found** (v35). The remaining gap to
   107-113 is a count race whose only clean lever is *cheaper per-candidate replay*
   (so more of the 2000 cap fits), and v35 is already near the cheap-single-hop
   floor.

Implication: further blind single-variable template probes are low-EV. Two
defensible paths:

- **A. Hold v35 as the standing submission.** Stop spending quota until we have a
  change with high-confidence positive expectation (we do not currently).
- **B. Count-race micro-optimization (L1), local-checkable.** Instead of changing
  what the model does, change how many cheap candidates get returned: shorten the
  message (fewer tokens -> faster response -> more candidates fit the replay
  budget), and/or improve gpt_oss *single-hop* firing with an explicit stop so it
  fires once and halts (no multi-hop blowup). This is still submission-gated but
  is grounded in the confirmed count thesis rather than firing intensity.

Path A is the safe default; Path B is the only remaining principled push, and it
must keep candidates strictly single-hop.

## State

- `experiments/attack.py` reverted to the exact v35 floor (`b61684a`); notebooks
  rebuilt; parses.
- Kernel version 40 (commentary prefill + margin) must NOT be submitted — it
  carries the refuted prefill.
- No submission made in this entry.

## Gate status

V39 recorded as refuted. Awaiting user direction between Path A (hold) and Path B
(count-race micro-opt, single-hop-guarded) before spending another submission.
