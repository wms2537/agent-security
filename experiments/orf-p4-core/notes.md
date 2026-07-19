# ORF Phase-4 core implementation notes

`run_core.py` is prepared for the separately authorized core run. It validates
the frozen Phase-4 config and the exact 960-row baseline table contract before
recomputing the global comparator and applying exhaustive per-profile action
selection. It does not trust or consume the baseline summary's reported `G`.
The runner also requires the committed baseline table's exact SHA-256
`331e8b5e16b42d8781df68fd49aa9cd83a4d77c8f5ec0ab9de15e09137e59cbf`,
so a shape-preserving data substitution cannot enter the core run.

`test_toy_core.py` uses only tiny hard-coded score tables. It neither reads the
primary table nor generates any Phase-4 master.

No core scientific data have been executed or aggregated while preparing these
files. An authorized run may replace this file with the canonical run notes.

Scope remains public deterministic non-target validation only. Synthetic-profile
evidence cannot establish live heterogeneity, learnability, private transfer,
held-out performance, Kaggle performance, or a live-deadline claim.
