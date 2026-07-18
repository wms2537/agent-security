# Memo completion audit

**Date:** 2026-07-18 · scope check requested: "make sure we completed everything in our memo first"

**Bottom line:** The memo is a two-track *company + research manifesto* (26 sections, a 12-week plan, an
11-layer platform, a cross-layer benchmark, a product wedge). Its own thesis (§26, §17) is that **the
Kaggle competition is the forcing function, not the product.** So "complete everything" cannot mean the
whole platform in one session — that would be scope-inflation away from the thing the memo says to do
first. What follows is an honest status of the memo's asks, competition-scope items first.

## A. Competition-scope asks — mostly DONE

| Memo ask | Status | Where |
|---|---|---|
| §1.1 Decide whether to enter (yes) | ✅ confirmed (competition verified live) | REVIEW.md §1 |
| §25 Gate 1: valid end-to-end submission | ✅ notebook builds + serves; runs through real pipeline | `submission/`, `experiments/local_eval.py` |
| §25 Gate 1: reproduce candidate-level outcomes locally | ✅ local scoring harness + per-template probe diagnostics | `experiments/local_eval.py`, attack `debug` |
| §25 Gate 1: ≥3 diverse attack families | ⚠️ partial — only 2 families actually *survive a guardrail* (EXFIL, CONFUSED_DEPUTY); we proved the other two are structurally blocked, which is a finding, not a gap | REVIEW.md §1 |
| §25 Gate 1: measurable (not anecdotal) improvement | ✅ results.tsv ledger; hardening 100.7→198.6 measured | `results.tsv` |
| §3.6 Build as a **portfolio optimiser**, not one attack | ✅ probe→select→value-weighted fill with private reserve | `experiments/attack.py` |
| §17.2 Track A: valid candidates, dedup, replay-cost estimate, stay in budget | ✅ measured replay-cost sizing + void-safety; unique-cell minting | attack PHASE 3 |
| §17.3 Track B: private-transfer attacks (memory/skill/tool poisoning, etc.) | ⚠️ partial — private-guardrail *insurance* via CONFUSED_DEPUTY reserve is in; the exotic vectors (memory/skill poisoning) are **not applicable** to this benchmark's tools/predicates | REVIEW.md §2 |
| §17.4 Candidate utility function (success×transfer×severity÷cost) | ✅ implemented as `value_density` (severity·fire_rate/cost) | attack `Probe.value_density` |
| §17.5 Local evaluator surrogate | ✅ mock agents + real pipeline; validity/latency/severity measured | `experiments/mock_agents.py` |
| §21 Weeks 1–2 exit: reproducible submission, ≥3 families, no manual editing | ✅ (with the 2-viable-family caveat above) | repo |

## B. Research/platform asks — DEFERRED (by design, not oversight)

These are the memo's §14 platform, §18 experiments, §19 benchmark, §22 roadmap. None are required to
compete, and the memo sequences them *after* the competition kernel. Deferred with rationale:

| Memo ask | Why deferred |
|---|---|
| §1.3 Cross-framework Trace IR; §14.2 | The competition gives one fixed harness; an IR abstraction earns nothing on the leaderboard. Build only if we pursue the platform. |
| §1.3 / §14.3 Security State Graph; §14.4 provenance plane | Graph-conditioned search is the memo's *research* differentiator (vs ARGUS/AuthGraph), not a competition need. The benchmark has ~10 tools and 4 predicates — no graph required. |
| §14.5 Attack DSL; §14.6 hybrid MCTS/RL search | We use targeted template probing; a full search engine is over-engineering for a 2-viable-predicate surface. Revisit only if online probing plateaus. |
| §14.9 runtime policy / §14.10 remediation / §14.11 Kertas | Defense/product layers; the public competition is attack-only. |
| §18 Experiments 1–8; §19 cross-layer benchmark | These build the *paper/product*, not the submission. In scope only for the optional Working-Note award (Sep 8) if we choose to write it. |
| §16 product wedge; §22 roadmap; §23 team | Company-building, out of scope for the competition entirely. |

## C. Corrections we made to the memo (memo was wrong/stale)

- Memo's "79.29 / 64.08" were public-notebook proxies; **real LB tops ~103.7** (Kaggle CLI).
- Memo framed the field as needing graph/provenance machinery; for *this competition* the decisive levers
  are far simpler: literal-`SECRET_MARKER` exfil past a URL-only guardrail check, multi-post severity
  stacking, unique-cell minting, and **not** voiding on replay timeout.
- Memo under-specified the real failure mode: **replay-timeout voids the whole submission.** That, not low
  score, is what sinks submissions — now handled explicitly.

## D. What's genuinely left to "complete" within competition scope

1. **T001 — submit** and get real 4-cell leaderboard feedback (needs your go-ahead: it's an account action).
2. **T002 — target-specific phrasing** tuning once we see which templates fire on gpt-oss vs gemma.
3. **T003 — confirm multi-post ceiling** under the real forced replay hop limit.
4. **(optional) Working-Note award** — the memo's §18-style write-up, due 8 Sep, worth $2.5k and aligned
   with the memo's research goals. Only if you want it.

Everything the memo asks for *to compete strongly* is done or is one submission away. Everything else is
the memo's longer platform/company arc, which it deliberately sequences after the competition.
