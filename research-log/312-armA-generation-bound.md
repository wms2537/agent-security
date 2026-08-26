# Arm A decode — validated fills are GENERATION-bound; replay was never the wall

Date: 2026-08-25

## Results

- v59 canary (kernel v60): **85.095** — ambiguous band per log 311; coincides
  with the aiagsec@0.97 current-regime anchor (85.05) ⇒ most consistent with
  both gates rejecting packing. Static A/B decides.
- Static Arm A (gpt_oss blind M1 control, kernel v61): **44.730**
  ⇒ gpt_row = 2×44.730 − 0.45 = **89.01 norm ≈ 989 fired findings** of 2000
  blind singles.

## The correction this forces

Our campaign model said: "score is a count race bounded by REPLAY time;
~970/row at ~9.3s/candidate; frac peaks 0.98; zero headroom." Arm A falsifies
half of it:

- True slow-row replay capacity ≈ **1,360 candidates** (989 fired ÷ 0.727
  v48-measured blind fire rate), i.e. **≈6.6s/candidate**, not 9.3s.
- v42's adaptive fill returns only ~835 on that row. **+18% headroom exists**
  and our policy forfeits it.
- Why the frac ladder cliffs then? Validated fills pay a ~9s live probe from
  the SAME 9,000s generation budget for every candidate returned. At ~970
  probes generation is exhausted; raising frac pushes run() into the hardened
  generation-timeout truncation zone → fewer/partial credit → the observed
  85.3 regressions at 0.985+. The cliff was never a replay wall.
- Cross-check: v48 (blind 1250, both rows) = 81.81 mean ⇒ replay fit all
  1250 and scored the ~909 fired per row. Consistent with capacity ≥ 1250.

Reframes the frontier question: top teams' 100+ likely comes from maximizing
**fired findings per generation-second** (cheap probes or high-fire-rate
blind emission), not exotic value stacking. Ceiling if filled honestly to
replay-fit: row ≈ 1360×18/200 ≈ **122 norm**.

## Consequences for the running programme

1. Arms B/D (packed M2) now measure packing under a GENERATION-bound regime:
   packing doubles raw per probe (34 vs 18) but also roughly doubles probe
   cost. Net decided empirically — exactly what the arms are for.
2. New independent lever surfaced (post-A/B): **honest-coefficient cheap
   probing** — hop-1 validation (v45's mechanism) with correctly measured
   hops1/hops8 ratio instead of the over-charged coefficients that sank v45.
   Target: validated count → min(gen-budget/t_probe, replay-fit ≈ 1,360).
   v45's failure mode (over-charging → under-fill) is fixable with one local
   calibration run on the real-CPU harness.
3. Blind emission wastes 27% replay on unfired candidates; validated wastes
   nothing but binds on generation. Optimum is cheap-validation, not pure
   blindness.

## Slot plan update

- Aug 26: Arm B (gpt M2 packed, sha 97502318da8d) — answers packing on slow row.
- Aug 27: Arm C (gemma M1 control) — measures fast-row capacity symmetric to A.
- Aug 28: Arm D (gemma M2 packed) — packing on fast row.
- Then: either deploy winning structure, or pivot to honest-coef hop-1 fill
  (L2), which now has the larger expected value if B/D show packing ≤ neutral.

Deployed-kernel hygiene unchanged: final pre-deadline push reverts to canonical
v42 config unless an arm/hybrid beats it.
