Status: DONE

File reviewed: `research-log/174-hypothesis-iter-8-ahcms24-v4.md`
Line count: **686** in both the working tree and `HEAD`.
SHA-256: `4e66cab8f8e0aa5c155332303cfaa7e2110e3b181e9904c55bc36f87ea55032f`

## 1. Blind Assessment

### Previous-review issue disposition

1. **Endpoint-aligned Occam comparison — RESOLVED.**
   Lines 377–426 replace raw-only `rho_simple` with the same raw/generation-work efficiency comparison used by the headline, condition it on explicit feasibility, and add exact raw/work Pareto non-domination. The integer form at lines 393–403 is correct.

2. **Exact overage formulas and accounting boundaries — IMPROVED, not fully resolved.**
   Lines 278–322 now provide per-unit formulas, selected-path/accepted-occurrence sets, clock boundaries, empty-sum behavior, and strict `>` semantics. However, the claimed clock exclusions are false for the specified clock, and the historical profile does not measure the newly defined quantity; details below.

3. **Zero-denominator handling — RESOLVED, with one new branch inconsistency.**
   Lines 324–375 totalize `Delta_E`, `rho_raw`, and `rho_tail` through the `R_r=0` disconfirmation branch and retire decision use of `rho_simple`. Simple-control comparison is denominator-free. However, lines 405–408 make a false implication for the `R_a=R_s=0, R_r>0` case.

### Justification Correctness

The mathematical core is correct and non-decorative:

\[
\frac{E_a}{E_r}
=\frac{R_a/W_a}{R_r/W_r}
=\frac{R_aW_r}{R_rW_a},
\]

so `10*R_a*W_r >= 11*R_r*W_a` is exactly the `1.10` threshold on the positive domain. Given `W_r=W_a+W_tail` and `R_r=R_a+R_tail`, the efficiency identity at lines 193–209 also follows correctly when the displayed denominators are positive. The text appropriately does not pretend this proves the empirical `1.10` magnitude.

I reran the sealed-artifact audit. It reproduced the stated 415/59.1819-second primary tail, 146/18.3665-second HCMS tail, `39240/39258` retention, and `1.355754716874` retrospective ratio. I also independently rescored the HCMS accepted sequences with the bound set-based scorer: retry raw is `39258`, absorbing raw is `39240`, and the marginal loss is genuinely `18`. Thus the raw profile is authentic.

The load-bearing defect is the work construct:

- Lines 264 and 280–285 define durations by `time.monotonic_ns()` around an operation, then assert that scheduler delay is excluded.
- A monotonic clock measures elapsed interval time. It necessarily includes any descheduling, sleep, or preemption between the two readings. A local check around a 50 ms sleep measured `50.107 ms` monotonic elapsed but only `0.054 ms` process CPU.
- Therefore lines 285, 311–312, 518–519, and 533–535 misstate what is measured. The quantity is a sum of captured elapsed intervals, not scheduler-excluded work.

This also breaks the claimed alignment between the profile and the new endpoint. The historical `path_cost_s` timer started before and ended after several controller snapshot serializations (`experiments/poc/hcms24_phase3_v1.py`, lines 1125–1271; snapshot serialization is at lines 670–679). Historical replay timing likewise ends before final scoring, whereas v4’s `ell` ends after scorer completion. Yet lines 159–183 and 475–483 use those historical seconds as the measured bottleneck for the new controller-bookkeeping-excluded, scorer-inclusive definitions. The old artifact contains real measurements, but not measurements of the quantity v4 now claims it measures. Consequently, the `1.25` expectation and the engineering profile gate lack a boundary-aligned source.

### Mathematical Depth & Validity Domains

The equations carry the argument; there is no mathiness. Symbols are bound to raw, selected paths, accepted occurrences, and measured durations. Positive denominator domains and the `W_tail=0` branch are explicit.

The missing validity domain is measurement-related: when is elapsed monotonic time a faithful measure of “generation work,” and how is in-boundary scheduler noise treated? The entry currently asserts it cannot occur rather than bounding or acknowledging it. Because nine fixed units offer little averaging, tail-specific descheduling could directly inflate the apparent removal benefit.

### Logical Soundness

The matched-trace causal attribution is otherwise strong: the primary methods share the trace and state through the trigger, and absorption removes only a suffix. The fixed-sample scope prevents overclaiming population or target effects.

A new logical error occurs at lines 405–408. From `R_a=0` and `R_s=0`, it does not follow that `R_r=0`; retry may obtain all positive raw after the absorbing trigger. For example, `R_a=0, R_tail=1, R_r=1, R_s=0` is consistent with every prefix identity. The attempt still disconfirms through primary efficiency and retention, and the simple cross-product remains defined, but the stated decision explanation is wrong and the author checker lacks this adversarial case.

### Assumption Completeness

The entry adequately states potential consistency, support, trigger identity, prefix attribution, raw monotonicity, constrained scope, and fixed-sample scope.

Two load-bearing assumptions are missing:

- equivalence between the historical timing bracket and the newly specified prospective bracket;
- treatment or boundedness of in-interval scheduling/preemption noise under `monotonic_ns`.

Violating the first removes the measured profile support for the numerical work claim. Violating the second changes the meaning of `W`, `G`, and `Q` and permits an alternative explanation based on machine scheduling rather than candidate-generation work.

### Taxonomy Verification

The classification is accurate:

- **Resource Bottleneck**, secondarily Failure/Risk Gap;
- **Artifact/System**, secondarily Robustification;
- dominant operation **replace**.

The contribution replaces one retry transition with absorption. It is not Bridge Opportunity × Synthesis/Unification, and the heightened default-template tripwire does not apply.

### Anti-Stacking Check

Tests 2 and 3 pass:

- the absorb/retry primary pair is a genuine per-component removal;
- the contribution is the constrained end-to-end system outcome, not the combination.

Test 1 is only partially satisfied. The path count and marginal raw profile are real, but the historical seconds are not boundary-aligned with the current work endpoint. Until the entry either supplies a matched profile or narrows what those seconds justify, the complete engineering anti-stacking gate does not pass.

### Occam’s Razor Check

The previous Occam defect is repaired. Absorption is the single local move, and fixed8/fixed24 controls now face the claimed endpoint.

A reduced global path cap remains a plausible simpler alternative: it could remove a low-yield suffix without conditioning on replay no-fit. This is not a blocker to the narrowly stated comparison against the two preregistered controls, but the text should avoid implying those controls exhaust every simpler explanation.

### Alternative Explanations

The entry handles absent saturation, valuable recovery, simple-policy adequacy, profile construction, excluded system overhead, replay mismatch, and target scaling.

It does not handle:

- tail intervals receiving disproportionate descheduling/preemption;
- the historical ratio being partly due to controller snapshot overhead excluded from the new metric;
- a lower fixed path cap producing the same aggregate retention/efficiency outcome.

The literature boundary is sound and non-load-bearing: CQR gives marginal coverage under exchangeability, CRC controls expected loss under exchangeability, online conformal work describes retrospective sequence-average guarantees, and the recovery-deadline paper explicitly separates statistical autonomy from a verified safety backstop. [CQR](https://proceedings.neurips.cc/paper_files/paper/2019/file/5103c3584b063c431bd1268e9b5e76fb-Paper.pdf), [Conformal Risk Control](https://proceedings.iclr.cc/paper_files/paper/2024/file/f3549ef9b5ff520a7e41ff3cc306ab2b-Paper-Conference.pdf), [online conformal prediction](https://proceedings.mlr.press/v235/angelopoulos24a.html), [recovery-deadline certificates](https://arxiv.org/abs/2606.25371).

### Overall: NEEDS_REVISION

Required fixes, ordered by severity:

1. **Make the work construct and profile evidence boundary-consistent** — lines 159–183, 260–322, 475–483, 517–519, and 533–535.
   Stop claiming `monotonic_ns` excludes in-interval scheduler delay. Define the quantity as elapsed interval time including preemption, or specify a defensible alternative measurement. Then either provide a profile measured with the same prospective boundaries or explicitly withdraw the historical seconds/ratio as support for the current work endpoint.

2. **Correct the all-zero AHCMS/simple branch** — lines 338–375 and 405–408.
   Specify the `R_a=0, R_s=0, R_r>0` outcome: primary efficiency and retention disconfirm; the simple-control cross-product is defined; any retired raw-only diagnostic uses its zero-simple sentinel. Add this case to the checker.

## 2. Actionable Coaching

- Use a measurement table with columns: quantity, start event, end event, included in-boundary waiting, excluded code regions, and interpretation. Avoid claiming that a wall clock measures CPU work.
- If simulated latency is part of the intended construct, retain monotonic elapsed time and explicitly include scheduler/preemption noise. Randomize capture order and report sensitivity to unusually delayed arms.
- The old artifact cannot establish the new exact boundary merely by re-labeling `path_cost_s`. Either run a separate exploratory boundary-aligned profile on non-confirmatory masters or narrow the profile claim to measured tail path count and marginal raw.
- Add adversarial checker fixtures for `R_a=0,R_r>0,R_s=0`, all-simple-zero, and positive retry raw appearing only in the removed tail.
- As an additional Occam stress, preregister one reduced global path-cap control, or narrow “tests whether HCMS complexity is needed” to “tests HCMS against these two specified simple policies.”
