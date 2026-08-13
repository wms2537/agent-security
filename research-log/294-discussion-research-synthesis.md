# Discussion/external research synthesis — no new throughput lever; one open thread

Date: 2026-08-13

Researched competition discussions + external sources for a lever past our 87.255
single-post replay ceiling.

## Sources

1. arXiv 2507.20526 "Security Challenges in AI Agent Deployment" — the paper for
   the Gray Swan *human* red-teaming challenge that seeds the ART benchmark our
   Kaggle competition scores against. Background only: 100% policy-violation
   rate, high attack transferability, single successful exploit compromises a
   system. No throughput/scoring mechanics.
2. Public notebooks (pilkwang, dimong4, nctuan, k1-short, others) — all the same
   validation-fill single-post family or older/weaker variants (k1-short uses
   PAYLOAD=TOKEN=admin123 which scores 0 on the current SECRET_MARKER grader).
3. YouTube "The 0-Second Bypass: Evaluating 1,000,000 Policies Offline"
   (Bangsaen AI Studio). Technique: capture one agent trace, extract transition
   dynamics into a surrogate, search the policy space offline via linear algebra;
   a policy passing the filter is "guaranteed to break the guardrail on the first
   attempt."

## Verdict

The 0-Second Bypass is an offline surrogate-search method for RELIABILITY of hard
multi-step attacks. It does not apply to our bottleneck: the OptimalGuardrail
forces single clean EXFILTRATION (log 288), which our real-CPU harness shows
already fires ~100% (log 291/292). We are replay-THROUGHPUT-bound, and offline
policy search cannot change how many candidates the gateway replays. No public
source reveals a way to exceed the single-post replay ceiling.

## One open thread worth noting

The video states the budget as **1,800 s**, while our SDK gateway copy uses
DEFAULT_BUDGET_S = 9000. If the real per-phase budget were smaller, per-candidate
REPLAY SPEED would dominate even harder, making a faster-replaying candidate the
only lever. Our candidate already minimizes the final response ("...answer OK
only"), but the real-CPU harness could measure whether a shorter/bare candidate
generates fewer replay tokens (faster replay -> more candidates fit -> higher
count) on gpt_oss/gemma. Expected gain is marginal (replay is already ~t8 with a
1-2 token final response), but it is the only untested throughput idea and it is
offline-measurable before any submission.

## State

attack.py = v42 (frac 0.98 single-post), standing 87.255. Research yields no new
high-confidence lever; the faster-replay-candidate idea is the only remaining
offline-testable thread.
