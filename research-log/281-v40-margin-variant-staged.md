# V40 margin-added firing-rate variant — staged, submission held

Date: 2026-08-05

## Context

V39 (ref 55229371, gpt_oss commentary-channel prefill) has been PENDING ~21h,
far longer than v35/v37/v38 (hours). The gateway self-limits each phase to
`DEFAULT_BUDGET_S = 9000s`, so the run is bounded (~15h compute ceiling + queue)
and will terminalize; it cannot pend forever. The unusually long runtime is
consistent with the prefill raising gpt_oss firing so generation runs closer to
full budget and a larger fired set is replayed — i.e. the lever likely did
something, but may be overrunning the thin 97% replay margin.

## Staged change (not submitted)

Kernel version 40 = v39 prefill + conservative replay sizing (research-log 278
gate): `REPLAY_SAFE_FRAC 0.97 -> 0.85`, `REPLAY_COST_COEF 1.0 -> 1.15`. This
lowers the returned fired-candidate count so both generation and replay finish
with real headroom.

## Commit-run gate (v40) — PASS

- CSV rows=5, header `Id,Score`, widths [2], empty cells 0.
- `source_strip_match True`.
- prefill present x1; `REPLAY_SAFE_FRAC = 0.85` x1; `REPLAY_COST_COEF = 1.15` x1.
- no `BUNDLE_POSTS`/`MEASURED_DENSE`/`SLOW_MULTIPOST`/old `analysis<|message|>`.
- run-log error hits 0.

Version 40 is one `kaggle competitions submit -v 40` from submission.

## Decision rule (when v39 terminalizes)

- v39 scores **>86.670**: L2 works and fit in budget. Do NOT submit v40 (its
  lower count would give up score). Next lever: extend the prefill idea to the
  gemma JSON path.
- v39 **blank / "Submission Format Error"**: firing rose but overran replay.
  Submit v40 (prefill + margin) as the reliability fix. If v40 also blanks,
  lower the margin further (frac 0.75, coef 1.3) before the next probe.
- v39 scores **<86.670** but non-blank: prefill hurt gpt_oss compliance; revert
  FRAME_TEMPLATE to the v35 analysis channel and keep the floor.

## Note on observability

The gate's projected-replay logging (278 section 6) is not added: commit runs
have no gateway (fill loop never runs against a real env) and rerun stdout is not
retrievable, so the log would surface nothing actionable. Terminal
scored/blank remains the only real signal.
