# E2 fill-ladder plan — count-race tuning on the verbose-frame base

Date: 2026-08-05

Depends on E1 (v41, verbose FRAME_TEMPLATE) terminalizing non-blank. E2 widens
the returned firing-candidate count on the E1 base. Each rung is one
single-variable, commit-run-gated, quota-costing submission.

## Mechanic (verified against the fill loop)

Score per row = (returned firing candidates) x 18 raw / 200000 x 1000; public =
mean(gpt_oss_public, gemma_public). The fill loop stops via `_replay_stop`:

```text
replay_budget = budget * REPLAY_BUDGET_MULT           # 9000 * 1.0
replay_cap    = REPLAY_SAFE_FRAC * replay_budget - warmup_elapsed
wall_deadline = run_start + REPLAY_SAFE_FRAC * budget
per fired candidate: replay_cost += elapsed * REPLAY_COST_COEF
stop when replay_cost + next*COEF >= replay_cap  OR  now + next >= wall_deadline
```

Both gates scale with `REPLAY_SAFE_FRAC`. Under `REPLAY_SAFE_SIZING=True`,
`MARGIN_S`/adaptive-margin are NOT consulted (that path is the `else` branch). So:

- **Primary knob: `REPLAY_SAFE_FRAC`** — raises budget utilization -> more fired
  candidates returned, until the returned set's real replay exceeds the per-
  guardrail 9000s wall (timeout -> whole-row zero -> blank/"Submission Format
  Error").
- **Secondary knob: `REPLAY_COST_COEF`** — lowers the per-candidate replay-cost
  estimate so the loop fills wider at fixed frac. Riskier (if replay is actually
  costlier than estimate, timeout). Touch only after frac is maxed.
- `MARGIN_S` ladder is a no-op here and is deliberately excluded.

## Magnitude expectation (honest)

`REPLAY_SAFE_FRAC` is bounded near 1.0, so 0.97 -> 0.99 widens fill only ~2%
=> ~+2% count => low-single-digit score gain per the whole frac ladder. E2 is
fine-tuning, not a frontier jump. The large lever is E1 (fire-rate): if the
gpt_oss row was fire-rate-limited, verbose frame can lift that row substantially
and move the mean far more than E2. E2 harvests what E1 leaves. Reaching ~109
from 86.67 realistically needs E1's fire-rate win PLUS a full E2 ladder PLUS the
gpt_oss row's own replay-speed headroom (message brevity/early-stop, already near
max). The public code exposes no single 26% lever; the frontier authors laddered
many small private rungs.

## Row-cap note

`HARD_N_CAP = 2000` (== `MAX_REPLAY_FINDINGS`). The fast gemma row may already be
near 2000; if so, widening frac only helps the slow gpt_oss row (which is also the
most timeout-prone). So E2 primarily pushes gpt_oss, and the cliff will show up on
the gpt_oss row first.

## Ladder (one variable per submission, E1 verbose frame held)

Precondition: E1 non-blank. Baseline = E1's score at `REPLAY_SAFE_FRAC=0.97`.

| rung | change | rationale |
|---|---|---|
| R1 | `REPLAY_SAFE_FRAC 0.97 -> 0.98` | nctuan's shipped value; proven to run |
| R2 | `0.98 -> 0.985` | half-step past nctuan |
| R3 | `0.985 -> 0.99` | approach the wall |
| R4* | `REPLAY_COST_COEF 1.0 -> 0.95` | only if R1-R3 kept gaining with no blank; fills wider at fixed frac |
| R5* | `0.95 -> 0.90` | final squeeze; highest timeout risk |

## Per-rung protocol

1. Change exactly one constant on the current best kernel; keep E1 verbose frame.
2. Preregister row in results.tsv with frozen bins (below) before submit.
3. Commit-run gate: CSV schema + source identity + no density/harmony markers +
   clean log (same gate as v41).
4. Submit one probe; poll to terminal; record.

## Per-rung bins (frozen)

Let `B` = current best confirmed score (starts at E1's).

- **Advance:** `score > B + 0.5` and non-blank -> keep rung as new best, climb.
- **Plateau:** `B - 0.5 <= score <= B + 0.5` -> row cap or diminishing returns;
  stop the frac ladder, consider the secondary knob only if no blank seen yet.
- **Cliff:** blank / "Submission Format Error" or `score < B - 2` -> the rung
  crossed the replay wall; revert to the previous best rung and STOP laddering
  that knob. The last non-blank rung is the max.

## Campaign guardrails

- Never ladder two knobs in one submission.
- After any cliff, the standing kernel reverts to the last-good rung (leaderboard
  keeps best, but do not leave a timing-out config staged).
- ~1 rung/day (each eval is hours-to-a-day). E2 is a multi-day campaign.
- v35 floor remains the ultimate fallback; kernel v40 (v39 prefill) is never
  submitted.
- If E1 itself is null/blank, E2 does not start on that base — reassess first.

## Decision tree from E1

- E1 > ~90: fire-rate was the gap. Run the full E2 ladder to harvest fill; expect
  to approach the low end of the frontier band.
- E1 ~86.67 (null): frame did not matter on the current grader. Run R1-R3 anyway
  (fill is orthogonal and cheap-signal), but temper expectations; the 86->109 gap
  is then not explained by anything in the public code and may be
  hardware/variance or an unpublished per-model message.
- E1 blank/<86.67: revert; do not ladder.

## Status

Plan only. No code change or submission in this entry. Awaiting E1 (ref 55265683)
terminal score to select the branch above.
