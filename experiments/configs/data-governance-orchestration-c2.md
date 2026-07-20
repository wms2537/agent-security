# Cycle-2 orchestration-security data governance

**Recorded:** 2026-07-20
**Status:** draft contract; no framework or dataset download has occurred

## Data and code sources

- Primary workloads will be repository-authored finite graphs, decision tapes,
  obligation sets, and abstract security contracts. They contain no natural-person
  records, production logs, credentials, or real service endpoints.
- Primary runtime target after approval: LangGraph `1.2.9`, tag object
  `95af6a00718588e7b7ce17310e8006d267896a77`, MIT License.
- Generalization runtime after approval: CrewAI `1.14.7`, peeled tag commit
  `21fa8e32d91f87565ffa49e124abea8304d4fb8a`, MIT License.
- The exact source archives and lockfile will be hashed before any framework-bound
  validation. A newer version requires a new config version; it may not silently
  replace a pinned runtime.

The tags and licenses were checked from the official GitHub repositories on
2026-07-20. AutoGen is not included: its current maintenance transition and
split license files introduce needless scope and provenance ambiguity for the
first study.

## Human subjects, privacy, and contamination

- Personal data: none.
- Human-subjects material: none; no user study or annotation collection.
- Restrictive datasets: none planned.
- Benchmark contamination: the primary study uses generated finite-state tasks
  and fixed decision tapes rather than an LLM's memorized knowledge. If a learned
  model is introduced later, that is a contract change requiring contamination
  analysis and user approval.

## Safety and dual use

Adversarial conditions are encoded as abstract provenance, permission,
termination, and state-transition labels. Tools operate only on in-memory fake
objects and reserved `.invalid` identifiers. The repository must not retain
jailbreak strings, executable exploit payloads, real secrets, destructive shell
commands, or live-target procedures.

The work is dual-use because a graph-level regression map could reveal where an
orchestration runtime is weak. Reporting therefore prioritizes invariants,
aggregate failure classes, and defensive tests. Any framework-specific defect
that appears plausibly exploitable must be withheld from public artifacts and
handled through coordinated disclosure before publication consideration.

## Authorization boundary

- Local source inspection, static checks, inert simulators, and approved
  validation runs are in scope.
- Network access during confirmatory runs is forbidden.
- Kaggle, model APIs, live services, external messages, locked-test generation,
  and locked-test execution require separate explicit authorization.
