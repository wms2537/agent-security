# SCOC-32 Phase-0 execution environment

**Recorded:** 2026-07-23

- Interpreter: `/home/soh/agent-security/comp/.venv/bin/python`
- Python: CPython 3.14.3
- Execution root: `/home/soh/agent-security`
- Host in prior captures: `Linux x86_64`, `glibc 2.40`
- Canonical command pattern: `comp/.venv/bin/python -I <script> [args]`

## Immutable command framing

- Kaggle action itself is out-of-scope for T065.
- All run logs must begin with the exact command on line 1.
- A parsed run log must include:
  - mechanism id,
  - comparison matrix arm,
  - per-arm coverage and raw/sec,
  - wall-second split by generation/replay.

## Safety controls

- no network calls from Phase-0 run code paths except already authorized and logged local reads,
- no external secret use,
- no model or endpoint tuning outside the fixed contract.

## Time accounting

- use wall-clock seconds split into generation seconds and replay seconds,
- use exact integer raw counts from official scorer cells,
- do not infer savings from token counts or compressed message length.
