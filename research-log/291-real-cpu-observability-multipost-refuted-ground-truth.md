# Real-CPU observability — multi-post refuted with ground truth; single-post is the efficiency ceiling

Date: 2026-08-12

Stood up faithful local observability: the exact competition GGUFs
(gpt-oss-20b Q4_K_M, gemma-4-26B-A4B Q4_K_M) run on CPU via llama.cpp
(py3.11 venv, n_gpu_layers=0), driving the real SDK gym env + OptimalGuardrail +
predicates + scoring. This measures REAL multi-hop firing and per-candidate CPU
elapsed -- the two signals OpenRouter could not (it parses tool-calls itself and
serves on GPU). Harness: experiments/real_cpu_harness.py.

## Measurements (steady state; first call excluded as warmup)

| model | candidate | elapsed | posts (asked) | raw | raw/sec |
|---|---|---|---|---|---|
| gpt-oss | single (h8) | 6.9s | 1 | 18 | **2.61** |
| gpt-oss | multi2 | 30.8s | 2 (2) | 34 | 1.10 |
| gpt-oss | multi4 | 143.7s | 2 (4) | 34 | 0.24 |
| gpt-oss | multi8 | 112.4s | 8 (8) | 130 | 1.16 |
| gemma | single (h8) | 6.9s | 1 | 18 | **2.61** |
| gemma | multi2 | 14.4s | 1 (2) | 18 | 1.25 |
| gemma | multi4 | 15.4s | 1 (4) | 18 | 1.17 |
| gemma | multi8 | 17.2s | 1 (8) | 18 | 1.05 |

## Conclusions (ground truth)

1. **Multi-post is refuted on the real stack.** gemma makes exactly ONE post
   regardless of K (ignores the sequential instruction); gpt-oss is wildly
   variable (2 posts at K=4 in 143s, 8 posts at K=8 in 112s). OpenRouter's
   uniform 8/8 was an artifact of its robust server-side tool parsing and does
   NOT transfer. This is exactly why v44 (K=8 both rows) collapsed to 25.040.

2. **Score is a raw/second (throughput) race, and single-post wins it.** The
   fixed ~9000s replay budget rewards raw-per-second. Single-post = 2.61 raw/s on
   BOTH models; every multi-post variant is 1.0-1.25 raw/s at best (2-11x worse).
   There is NO per-candidate density lever. The audit's R(K)=16K+2 is real but
   unreachable/net-negative here because real models don't reliably emit K
   sequential posts and CPU cost per multi-post candidate explodes.

3. **Real single-post cost = ~6.9s/candidate** (1 post gen + tool + final "OK").
   9000s / 6.9s ~= 1300 candidates/row ceiling -> ~117/row -> mean ~117 at full
   both-row saturation. The leaderboard frontier (114) sits right at this
   single-post throughput ceiling, i.e. the leaders are running OPTIMAL
   single-post, not multi-post.

4. Our 87.255 (~970 findings/row) is below that ceiling, but E2 already showed the
   count peaks at REPLAY_SAFE_FRAC 0.98 (0.985 regressed) -- so the remaining
   headroom is guarded by real replay-cost variance, not a missing mechanism.

## Net

The faithful harness definitively closes the multi-post/density question that
cost v44: single-post is optimal, confirmed on the real CPU models. 87.255 is
near the single-post throughput ceiling for our controller. Any future
candidate-shape idea can now be vetted offline on real models here instead of via
OpenRouter fiction or blind day-long submissions.

## State

attack.py = v42 best (frac 0.98 single-post), standing 87.255. No submission.
Models + venv live under gitignored local_obs/. Harness copied to
experiments/real_cpu_harness.py for provenance.
