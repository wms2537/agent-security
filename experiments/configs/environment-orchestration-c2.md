# Cycle-2 orchestration-security environment

**Recorded:** 2026-07-20
**Status:** observed local environment; package installation has not begun

- OS/kernel: Linux 6.11.0-29-generic, x86_64, glibc 2.40.
- CPU: Intel Core i7-8700K, 6 physical cores / 12 logical CPUs.
- Memory: 30 GiB RAM; 975 MiB swap.
- GPU: NVIDIA GeForce GTX 1080 Ti, 11,264 MiB; driver 555.42.06.
- Interpreter: `/home/soh/agent-security/comp/.venv/bin/python`, CPython
  3.14.3.
- Present packages relevant to deterministic checks: `jsonschema==4.26.0`,
  `numpy==2.5.1`.
- Not presently installed: `pytest`, `networkx`, `scipy`, `pandas`, LangGraph,
  CrewAI. Their absence is not an implementation failure; dependencies may be
  installed only after the evaluation contract is approved and pinned.

The intended core is CPU-only. The GPU is not part of the primary comparison.
Runs will use inert model adapters and local tools; no model API, Kaggle service,
or live external target is required. Any later dependency installation must be
recorded with exact version, source, license, and lockfile hash before a result is
eligible for the ledger.

Verification source commands are recorded in
`research-log/055-cycle2-setup-repair.md`.
