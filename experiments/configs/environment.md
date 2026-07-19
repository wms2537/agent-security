# Reproducible environment

**Recorded:** 2026-07-19

- Host kernel: Linux 6.11.0-29-generic x86_64 GNU/Linux.
- Interpreter: `/home/soh/agent-security/comp/.venv/bin/python`, CPython 3.14.3.
- Platform: Linux x86_64, glibc 2.40.
- Required Python package: `jsonschema==4.26.0`.
- Execution root: `/home/soh/agent-security`.
- Accelerator: none; all ORF public non-target runs are CPU-only.
- Network: forbidden for the Phase-3 PoC and all public non-target ORF runs unless a later task explicitly authorizes it.
- Kaggle: forbidden. No push, submission, API call, notebook execution, or leaderboard read is part of the ORF Phase-3–6 scope.

Canonical invocation pattern:

```text
comp/.venv/bin/python -I <script> [arguments]
```

Logs must begin with the exact executed command, followed by parseable
`metric_name: value` lines. Run artifacts are written only beneath the named
local `experiments/` run directory.
