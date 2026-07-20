# Cycle-2 setup repair — orchestration security portfolio

**Date:** 2026-07-20 · **Phase:** 0 · **Cycle:** 2 · **Iteration:** 5 ·
**Status:** completed, evaluation contract approved

## Context

The Cycle-2 literature checkpoint was complete, and the user selected all three
directions verbatim: `go try all please`. ORIENT then found that `PROBLEM.md`,
idea DNA, and the evaluation contract still described the closed Cycle-1
Kaggle/ORF question. Advancing directly to a new hypothesis would therefore have
violated SciAgent's problem-anchor and Phase-0 gates.

The topic redirection was explicit in the earlier user instruction about moving
from harness engineering to loop and graph engineering and examining agent
orchestration. The portfolio selection is also explicit, but SciAgent's
one-active-hypothesis rule means the studies must run sequentially.

## Setup decisions

- Current core question: which independently checkable controls preserve
  security properties as agent harnesses, loops, and graphs are rewritten or
  evolve under controlled inert workloads?
- Project type: empirical systems research.
- Question type: causal only within paired/randomized local interventions;
  outside-scope interpretation is diagnostic.
- Intensity: Medium, with LangGraph as primary and CrewAI as an independently
  implemented generalization runtime.
- Output: Markdown research report plus reproducible code and machine-readable
  evidence; target venue remains undecided.
- Sequence: OMST active first; PDPF second; IPHE third. Results and budgets are
  never pooled.
- Safety: abstract labels and inert in-memory tools only; no operational attacks,
  live target, model API, personal data, Kaggle, or external message.

## Source and environment verification

Official-repository checks on 2026-07-20:

```text
git ls-remote --tags https://github.com/langchain-ai/langgraph.git 'refs/tags/1.2.9*'
95af6a00718588e7b7ce17310e8006d267896a77 refs/tags/1.2.9

git ls-remote --tags https://github.com/crewAIInc/crewAI.git 'refs/tags/1.14.7*'
b01fa74038c0519bd6a4223d20a0fc05bf55dd74 refs/tags/1.14.7
21fa8e32d91f87565ffa49e124abea8304d4fb8a refs/tags/1.14.7^{}
```

Both pinned tag sources contain MIT license text. No repository or package was
downloaded. The local environment probe reported 12 logical CPUs, 30 GiB RAM,
an NVIDIA GTX 1080 Ti with 11,264 MiB, CPython 3.14.3,
`jsonschema==4.26.0`, and `numpy==2.5.1`. The primary design is CPU-only.

## Contract rationale

The primary OMST comparison uses deterministic decision tapes and exact
task-equivalence eligibility. This is deliberately stronger than comparing
benign accuracy or final text. The primary outcome counts base-pass →
rewrite-fail security regressions; identity rewriting must produce exact zero.
The 10-percentage-point target is explicitly normative and must survive Phase-2
theory review before any PoC.

The locked test is specified but absent. Even after contract approval it cannot
be generated or executed without a later explicit user authorization. If that
authorization never arrives, the conclusion remains validation-only internal
evidence.

## Gate Check

- `PROBLEM.md`: written with Supersedes header, question type, proxy caveat,
  non-goals, and six-construct table; direction/portfolio approval quoted.
- Idea DNA, project type, success criteria, scope, intensity, output, and venue:
  drafted in `state.json`.
- Environment: recorded in
  `experiments/configs/environment-orchestration-c2.md` from direct probes.
- Data governance: recorded in
  `experiments/configs/data-governance-orchestration-c2.md`; no PII, human
  subjects, downloaded dataset, or live attack surface.
- Evaluation contract: drafted at
  `experiments/configs/evaluation-contract-orchestration-c2.md`; exact config at
  `experiments/configs/omst-c2-v1.json`.
- Deterministic validation and git evidence: pending the RECORD step.
- User approval of the exact evaluation contract: **APPROVED**. After the draft
  was presented with its metric, 10 pp threshold, runtime matrix, data tiers, and
  authorization boundary, the user's complete response was verbatim: `ok`.
- Deterministic closure command returned:
  `cycle2_setup_gate=PASS status=approved_for_phase2_hypothesis constructs=6 rewrites=4 locked_test_absent=true`.

## Problem alignment

Repairing the anchor prevents the new research from optimizing the closed Kaggle
proxy and makes every later hypothesis answer the user-selected orchestration
security question.

## Decision

Enter Phase 2 with OMST as the sole active hypothesis. PDPF and IPHE remain
parked. Contract approval does not authorize a framework download, experiment,
locked-test action, Kaggle action, live attack, model API, or external message.

## Next Steps

1. Write the complete immutable OMST Phase-2 hypothesis.
2. Pass deterministic hypothesis checks before spending a review round.
3. Dispatch one sterile theory review; no experiment may begin before RIGOROUS.
