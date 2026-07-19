# ORF public non-target PoC notes

Implemented the frozen `orf-poc-v1` design as a thin deterministic wrapper around the immutable calibration and SDK reference functions. Exactly one replicate from each of 40 fixed strata entered the primary metric; the other profiles constructed internally by `build_profiles` were excluded. The homogeneous negative and two preserved SDK fixtures were asserted before any metric was emitted.

Deviations: none.

This run validates public mechanics and finite-table conditional regret only. It is not evidence of live-model prevalence, learnability, private transfer, Kaggle performance, or the unexecuted beacon-held-out v9 claim.
