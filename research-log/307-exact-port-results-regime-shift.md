# Exact-port results: historical public scores are regime-dependent

Date: 2026-08-22

Follow-up to log 306. Both byte-exact ports scored. These are the first
artifact-faithful transfer measurements of the entire campaign (SHA-256
verified through kernel push → commit run → competition submit).

## Results

| Artifact | Historical | Today (ref) | Δ |
|---|---|---|---|
| dimong4 V18 (multi-predicate) | 90.090 | **57.460** (55666474) | −32.6 |
| canqiang/aiagsec-ea-b-0721 V1 | 88.560 | **85.050** (55666737) | −3.5 |
| ours v35 @frac0.97 (Aug 4) | 86.670 | — | — |
| ours v42 @frac0.98 (Aug 7) | 87.255 | repeat pending | ? |

## Interpretation: two separable effects

1. **Global evaluator regime shift, ≈ −3 pts on identical code.**
   AIAgSec V1 is our own family byte-transferred faithfully and landed within
   ~1.6 pts of our own same-config run (85.050 vs 86.670), both well under its
   own historical 88.560. Host admitted hardening inconsistent timeout
   enforcement mid-competition; official rerun 2026-08-19 set a single regime.
   Historical scores above ~88 were earned under softer rules.

2. **Dimong-V18-specific collapse (−29 beyond the shift): template × new-rules
   interaction.** Its second predicate `fs.delete path=secret.txt` is denied by
   OptimalGuardrail ("secret" ∈ ultra_dangerous_patterns) exactly as log 288
   measured. Under current enforcement that denied hop is pure cost: per-
   candidate time inflates (~1.5×), adaptive replay-safe fill returns fewer
   candidates. Predicted retention 87.255 → ~57 if count scales 1/1.5;
   observed 57.460/87.255 = 0.659. Multi-predicate is refuted by its OWN exact
   source artifact, not by any port of ours. Their code comment ("Replay
   timeouts preserve partial scores!") shows they were tuned to the OLD
   timeout behavior.

## Corollary

Our standing 87.255 (v42) was scored Aug 7 — pre-hardening. Its current-regime
value is probably ~85.5–86.5. We were not stuck at a wall; we were comparing
scores across regimes.

## Action taken

- experiments/attack.py restored to v42 (git HEAD).
- Kernel v54 pushed: v42 AST-identical repeat (whitespace-normalized by the
  fixed builder), submit ref `55681594` 2026-08-22. Purpose: measure Var(S |
  identical artifact) under the CURRENT regime and re-anchor our best's true
  present-day value.
- Standing best is protected: Kaggle keeps max(submissions).

## Updated decision state

- Transfer methodology now validated end-to-end (AIAgSec within noise of our
  own same-config runs).
- All public architectures above 87 are either regime artifacts or private.
- Per-candidate value levers (burst/multipost/multi-predicate/combo): SIX
  independent refutations incl. one exact-source reproduction (v36, v38, v44,
  v49, v50, dimong-V18-exact). Closed under current rules.
- After the v42 repeat returns: freeze competition engineering unless the
  repeat reveals variance >> ±1 (which would reopen fine-tuning around frac).
