# Faster-replay wording measurement — v42 is near-optimal; no throughput lever

Date: 2026-08-14

Offline real-CPU measurement of per-candidate REPLAY elapsed (8 hops = gateway
replay condition) + firing, across candidate wordings, both real models. Faster +
100% firing would mean more candidates fit the replay budget -> higher count.

## Results (median of 4, warmup excluded)

gpt-oss: current_frame 6.31s (4/4) | bare 15.79s (4/4) | terse_frame 6.03s (4/4)
         | plainshort 15.62s (4/4)
gemma:   current 8.57s (4/4) | bare 11.94s (4/4) | terse 8.46s (4/4)
         | onlypost 8.45s (4/4)

## Conclusions

1. "Bare/short candidate replays faster" (the k1-short intuition) is REFUTED:
   bare is 2.5x SLOWER on gpt-oss and 1.4x slower on gemma. Without a brevity
   directive the models emit long reasoning. This also explains v41: plain/bare
   on gpt-oss is 2.5x slower replay -> 2.5x fewer candidates -> the 62.280 crash.
2. The harmony frame is essential for gpt-oss SPEED (6.3s vs 15.6s), not only
   firing.
3. v42's wording ("...answer OK only" / harmony frame) is already near-optimal for
   replay speed. Terse/onlypost land within noise (~8.5s gemma; gpt terse ~6.0 vs
   6.3 is a noisy ~5% on the fragile gpt-oss frame that regressed in v39/v41).

No meaningful faster-replay wording exists. Combined with the full lever map
(density/multipost/frame/multipredicate/fillwidth/hop1 all closed), 87.255 is the
true replay-throughput ceiling for this single-post controller. The frontier's
edge is not reproducible from any public source, our real-model harness, or any
candidate we can construct; likeliest remaining explanations are competition
CPU-allocation variance or an unpublished mechanism.

## Decision

Do NOT submit a terse-wording variant: the only non-noise signal (gpt-oss terse
~5%) is within measurement noise and sits on the gpt-oss frame path that regressed
twice (v39 56.5, v41 62.3) when reworded. Poor EV. Hold at v42 = 87.255.

## State

attack.py = v42 (frac 0.98 single-post), standing 87.255. All levers exhausted
with ground truth. Recommendation: hold.
