# DBER sterile theory review — hypothesis round 13

Date: 2026-07-26  
Phase: 2  
Task: T087  
Reviewed artifact: `research-log/215-dber-generation-binding-hypothesis-iter6.md`  
Reviewed commit: `4f760a6`  
Main-agent immutable line count: `400`  
Main-agent SHA-256: `95700e6500c964be8c2c90d25a09f56bdee3c2e665bd88b306a8947b153e1bea`  
Reviewer-reported line count: `400`  
Integrity result: `PASS`  
Blind verdict: `NEEDS_REVISION`

The text below is the reviewer's returned report, recorded verbatim.

---

**Status:** DONE

Reviewed artifact: [215-dber-generation-binding-hypothesis-iter6.md](/home/soh/agent-security/research-log/215-dber-generation-binding-hypothesis-iter6.md:1)

**Verified line count:** 400.  
`git show HEAD:research-log/215-dber-generation-binding-hypothesis-iter6.md | wc -l` returned `400`; the working copy matches `HEAD`.

## Blind assessment

**Overall: NEEDS_REVISION**

### Justification Correctness

The numerical claims are reproducible:

- `468 / 846 × 100 = 55.3191489%`.
- `1.716649079 + 2 × 0.938870399 = 3.594389877 < 5.94`.
- Replay headroom and the `0.948190747 s` bank-all overflow recompute exactly from the JSON.
- Artifact hashes match report 214, and the profile commit predates the hypothesis commit.

The equations define an actual packing rule and are not decorative mathiness. The official-source claims about separate generation/replay deadlines, the 2,000/32 caps, and raw scoring are also correct. The two literature citations are appropriately described as adjacent rather than load-bearing: the [NeurIPS competition paper](https://proceedings.neurips.cc/paper_files/paper/2025/hash/73368bc7644c054b5bcc6490a8f2fb1c-Abstract-Datasets_and_Benchmarks_Track.html) supports heterogeneous competition evaluation, while the [long-horizon survey](https://www.preprints.org/manuscript/202607.1328) is indeed a non-peer-reviewed July-2026 preprint separating model and harness components.

However, the engineering evidence does not yet measure every named construct faithfully:

- The profile’s `468` and `846` values come from the hand-written `_trace_raw` proxy in [dber_profile.py](/home/soh/agent-security/experiments/dber_profile.py:114), not from `eval_predicates` plus the official raw scorer. It is exact only if all intended predicates and score-cell uniqueness assumptions hold.
- No per-probe traces, predicate rows, candidate signatures, or score-cell hashes are retained, so an independent verifier cannot reconstruct the claimed raw values from the artifact.
- Replay cost is timed inside one already-built environment. Official replay constructs a fresh environment per candidate in [jed_attack_gateway.py](/home/soh/agent-security/comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py:611). Thus `r(p)` omits a component of the official replay path.
- The load-bearing generation-binding label is inferred by `_classify_binding`, including a rounded `unit_cost_s`, rather than recorded from the controller’s actual terminal condition ([dber_profile.py](/home/soh/agent-security/experiments/dber_profile.py:180)). This conflicts with the stated assumption at lines 277–278.

### Mathematical Depth and Validity Domains

The appropriate lens is bounded resource allocation with an explicit uncertainty envelope, and the entry mostly uses that lens correctly. It does not pretend that greedy density order solves knapsack, and it correctly states that `alpha=2` is not a probability bound.

Several definitions are nevertheless incomplete:

- Lines 56–62 invoke `min_{p∈P} r(p)` without requiring `P ≠ ∅`.
- Line 51 defines `K` relative to the official 2,000 cap, but the cited candidate-binding evidence uses an artificial cap of 3. That control is not an instance of the formal definition as written.
- `q(p)` is defined as a per-candidate raw value, whereas portfolio raw contains a set-level uniqueness term. The packing objective should use marginal value `Δq(p | C∪S)`, or state and verify the domain-uniqueness condition that makes isolated and marginal values coincide.
- Cost comparability at lines 265–268 omits guardrail, fixture state, environment-construction overhead, process load, candidate order, and warm/cold-cache regime.

### Logical Soundness

The generation-stop test is not justified by the stated model and is weakly dominated by a simpler policy.

Let `H` apply the same positive-value, alpha-stressed headroom packing but omit `stop(C)=generation`. Then:

- On generation-bound profiles, `H` and DBER are identical.
- On replay/candidate controls where nothing fits, both are no-ops.
- If a small probe fits after replay stops because the next incumbent fill item is too large, `H` adds positive raw under the same formal bounds, while DBER rejects it.

Therefore `H` weakly dominates DBER under the entry’s own deterministic assumptions. The replay control at lines 206–209 cannot identify the generation classifier because no probe fits; it distinguishes bounded packing only from unsafe bank-all. Lines 233–239 incorrectly call the generation and headroom checks “inseparable.”

There is also an interaction contradiction. Lines 94–98, 169–182, and 246–253 say DBER changes no target interaction and freezes all target interactions. Appending candidates necessarily causes additional evaluator replay interactions. Either:

- only generation-phase interactions are frozen, while replay interactions differ and must be measured; or
- replay is not performed, in which case the result is an offline counterfactual rescore rather than an end-to-end official-SDK result.

The entry must choose and specify one design.

### Assumption Completeness

The listed assumptions are unusually explicit, but the following remain load-bearing:

- The three future profiles must not be researcher-constructed to guarantee the threshold.
- Generation-trace success must yield positive marginal raw under actual replay.
- The replay-cost surrogate must conservatively cover the complete replay path.
- Stored candidates must reproduce exact messages, ordering, predicate outcomes, and score-cell identities.
- The policy branch must leave `C` and `P` unchanged before admission.
- The stop reason must be directly observed rather than inferred.

Violating transfer, marginal scoring, or cost coverage invalidates the score/safety claim entirely.

The fixed bias surface does enumerate all eight required classes. Its selection control is insufficient, however: lines 143–147 and 284–285 allow the three confirmatory profiles to be designed after seeing run03 and the controller. “Enumerated before implementation results” does not prevent favorable profile engineering.

### Taxonomy Verification

`Resource Bottleneck` and `decouple` are defensible. The dominant paradigm is more accurately **Optimization/Search** than **Artifact/System**: the contribution is a resource-aware admission and packing policy inside an existing system.

This is not Bridge Opportunity × Synthesis/Unification, and the relabeling would not trigger the default-template tripwire. It appears to be a classification error rather than tripwire evasion. The underlying taxonomy source does report the stated distributional LLM bias ([Chen, Zhao, and Cohan](https://arxiv.org/abs/2607.01233)).

### Anti-Stacking Check

The three engineering tests do not all pass:

1. **Measured bottleneck per component:** inventory passes (`26`, `468`). The headroom guard has measured evidence. The generation-stop classifier does not: its label is inferred, it has no differing measured case, and headroom-only packing predicts all existing observations.
2. **Per-component ablation:** inventory removal is planned. Replacing the entire gate with bank-all does not isolate generation classification from resource-bound enforcement. This test fails.
3. **End-to-end constrained system claim:** stated correctly at lines 240–242, but the replay-versus-fixed-trace ambiguity prevents the proposed measurement from yet being unambiguously end-to-end.

Thus the current engineering anti-stacking argument is incomplete.

### Occam’s Razor

The omitted `headroom_only` policy is simpler, predicts all run03 observations, and weakly dominates DBER under the formal model. Bank-all is not the strongest simple alternative; it is an unnecessarily unsafe strawman.

The predicted gain also has simpler explanations:

- returning more always-successful candidates to a compliant deterministic mock;
- hand-selected budgets causing the desired binding regime;
- computing both admission and “overage” from the same latency surrogate;
- a synthetic 4-second regime dominated by the incumbent’s one-second reserve sentinel.

These alternatives are not ruled out by the planned three-profile mean.

### Required revisions, ordered by severity

1. **Freeze an auditable profile population and selection rule** — lines 82–85, 143–163, 274–280, and 284–285. Specify exact agent classes, budgets, caps, seeds, hardware regime, inclusion criteria, and all profile units before review. Report every eligible unit, not three profiles chosen afterward.

2. **Test the simpler headroom-only policy and isolate the stop classifier** — lines 56–73, 206–209, 231–239, and 353–375. Add a replay-bound profile where at least one probe fits residual capacity, and compare incumbent, headroom-only, DBER, and bank-all. Remove the generation gate unless it demonstrates a safety benefit unavailable from the same cap constraint.

3. **Repair the engineering profile’s construct and provenance** — lines 188–220 and 296–298. Persist per-candidate messages, trace hashes, predicates, score-cell signatures, measured timing, and inclusion decisions. Compute raw through official SDK functions and measure actual replay including environment setup.

4. **Resolve the paired-interaction contradiction** — lines 94–98, 169–182, and 246–253. Say “no additional generation-phase interaction”; explicitly acknowledge and measure the additional evaluator replay interactions.

5. **Totalize the formal rule** — lines 47–70. Require nonempty, deduplicated `P`; parameterize an active cap `L ≤ 2000` and define `K=max(0,L−|C|)`; use marginal portfolio raw or prove the unique-cell regime.

6. **Correct the taxonomy label** — lines 345–356. Use `(Resource Bottleneck, Optimization/Search, decouple)`, with Artifact/System at most secondary.

## Actionable coaching

Use a four-policy factorial comparison:

- incumbent discard;
- headroom-only bounded packing;
- DBER generation-stop plus headroom;
- bank-all.

The decisive test should include both replay-bound cases: one with no fitting probe and one with a smaller fitting probe. That directly determines whether the generation classifier earns its complexity.

For confirmatory artifacts, create one immutable row per candidate containing its source phase, messages, signature, generation trace hash, official predicates, score-cell hash, isolated raw, marginal raw, generation elapsed time, full replay elapsed time, admission decision, and rejection reason. The independent verifier should reconstruct both portfolios and invoke the official scorer from those rows.

Treat `alpha=2` only as an accounting stress scenario until repeated end-to-end replay measurements justify a calibrated bound. For live readiness, model the entire replay cost—including environment construction—and pre-specify the target quantile or conservative finite-sample bound.

Finally, derive the expected gain directly before execution:

\[
\text{gain}(S)=100\,
\frac{\operatorname{raw}(C\cup S)-\operatorname{raw}(C)}
     {\operatorname{raw}(C)}
\]

This exposes whether the experiment tests an uncertain mechanism or merely re-evaluates an already-known inventory ratio.
