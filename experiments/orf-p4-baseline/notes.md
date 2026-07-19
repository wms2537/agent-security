# ORF Phase-4 baseline notes

- Scope: public deterministic non-target validation only.
- Policy: exhaustive `PROBE_GLOBAL` choice over all seven legal lengths,
  independently for each master, with smaller length breaking ties.
- Mechanical check: every immutable score-table result exactly equaled a
  separately implemented exact recomputation from profile costs and events.
- These constructed profiles do not establish live-target heterogeneity,
  learnability, replay-deadline safety, private transfer, or Kaggle performance.
- No network, beacon, held-out target, or external service was used.
