# ORF Phase-4 core run notes

The core calculation recomputed `G` from the seven committed score columns and computed `A` by exhaustive per-row argmax, always breaking ties toward the smaller fill length. No baseline summary or reported `G` entered the calculation.

The separately generated homogeneous controls used the frozen immutable calibration primitives. All controls were asserted before output.

Deviations: none.

Scope is public deterministic non-target validation only. Synthetic-profile results do not establish live heterogeneity, learnability, private transfer, held-out performance, Kaggle performance, or a live-deadline claim.
