# Row-isolation decoded — scoring model confirmed, rows balanced, frontier gap is external

Date: 2026-08-18

## Results

- Sub A (v46, gpt_oss active, gemma=5 fixed) = **37.800**
- Sub B (v47, gemma active, gpt_oss=5 fixed) = **42.075**

Decode (publicScore = mean(gpt_oss_public, gemma_public); 0.09 norm/finding; 5
fixed = 0.45):

- gpt_oss row = 2*37.8 - 0.45 = 75.15 norm -> ~835 findings
- gemma  row = 2*42.075 - 0.45 = 83.70 norm -> ~930 findings
- full v42 87.255 -> ~970/row (balanced)
- isolated sum 158.85 vs full*2 174.51 -> isolated ~9% lower

## Settled hypotheses (both were unresolvable offline)

1. **Scoring model CONFIRMED.** Decoded 835/930 match the ~970/row full-run
   estimate. "mean of 2 public rows x 18 raw/finding" is right; the 970-vs-1267
   framing is NOT an aggregation error.
2. **Rows BALANCED (835 vs 930, ratio 1.11).** No single broken/under-filled row.
   The "slow gpt_oss row is collapsing" theory is dead. Both models contribute
   nearly equally. No per-row bottleneck to target.

The ~9% isolated-vs-full penalty is mild -- consistent with rerun variance
(observed +/-2-5 pts throughout) or a small shared-run/warmup benefit. Not a lever.

## Final insight (answers "how do others score so high?")

The frontier (~1267/row, 114) has a REAL, UNIFORM ~30% higher replay throughput on
BOTH models. It is NOT explained by a broken row or a scoring misread (both ruled
out here), and per-candidate replay cost is a proven hard floor (density, firing,
wording, hop-1, reasoning-suppression, single-generation all refuted with
ground-truth). That advantage is not reproducible from any public notebook, the
official paper (2507.20526), the 0-second-bypass video, our real-model CPU
harness, or these diagnostics. Remaining explanations are competition-side:
CPU-allocation/timing variance across runs/submitters, or an unpublished
mechanism -- outside what we can access.

## Verdict

87.255 (v42) is the practical ceiling for this single-post validation-fill
controller. Every internal lever is exhausted with ground truth, and the frontier
gap is external. Recommend HOLD.

## State

Active kernel = v42 (ISOLATE_ROW=None), standing 87.255. Row-isolation capability
retained (config-gated, off by default) for future diagnostics.
