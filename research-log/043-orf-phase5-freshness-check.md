# ORF Phase-5 freshness check — adaptive inference allocation

**Date:** 2026-07-19 · **Phase:** 5 · **Iteration:** 4 · **Scope:** narrow primary-source search, five papers maximum

## Exact query and boundary

The narrow claim searched was: **does conditioning inference/tool-use structure or
budget on the current instance or trajectory outperform one globally fixed or
uniform allocation under matched resource constraints?** The search covered work
available through 2026-07-19. It did not query or mutate Kaggle, request a beacon,
freeze/open a held-out set, derive a target, or inspect any private evaluation.

## Primary-source results

| Work | Directly relevant result | Relation to ORF-B |
|---|---|---|
| Snell et al., *Scaling LLM Test-Time Compute Optimally Can be More Effective than Scaling Parameters for Reasoning*, ICLR 2025 ([proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b623663fd9b874366f3ce019fdfdd44-Abstract-Conference.html)) | The effective inference strategy depends on prompt difficulty; a per-prompt compute-optimal allocation was reported as more than four times as efficient as best-of-N on mathematical reasoning. | Establishes the broad adaptive-versus-global allocation idea before ORF-B. It does not study tool-trajectory length, security findings, the ORF score, or ORF's exact finite conditional-regret estimand. |
| Lin et al., *Plan and Budget*, 2025 ([arXiv:2505.16122](https://arxiv.org/abs/2505.16122)) | Decomposes a query and assigns token budgets by estimated sub-question complexity; compares against global-budget strategies on reasoning, instruction following, and tool-free planning. | Strong conceptual neighbor: local heterogeneous allocation under a total budget. Its learned/heuristic token scheduler and accuracy-efficiency objective differ from ORF's oracle choice among seven retained-probe fill lengths. |
| Paglieri et al., *Learning When to Plan*, revised 2026 ([arXiv:2509.03581](https://arxiv.org/abs/2509.03581)) | Trains agents to decide dynamically when to spend test-time compute on planning; always planning was reported as costly and harmful on long-horizon Crafter tasks. | Makes adaptive planning in agentic trajectories a direct neighboring contribution. Unlike ORF-B, it evaluates a learned policy in a live environment rather than exact oracle information value on a deterministic score table. |
| Xiao et al., *SCALE*, AAAI 2026 ([proceedings and DOI](https://ojs.aaai.org/index.php/AAAI/article/view/40697)) | Selectively assigns reasoning modes/resources by sub-problem difficulty and reports improvements over uniform scaling while reducing compute. | Further weakens any broad novelty claim that heterogeneous tasks benefit from selective allocation. It is mathematical reasoning, not tool-use security or benchmark-shaped candidate construction. |
| Li et al., *Spend Less, Reason Better: Budget-Aware Value Tree Search for LLM Agents*, 2026 ([arXiv:2603.12634](https://arxiv.org/abs/2603.12634)) | Uses step-level values and remaining budget to adapt tree expansion for tool-using agents; reports better multi-hop QA performance than parallel sampling under strict tool/token budgets. | The closest fresh agentic neighbor. It studies online learnable control with tool calls, whereas ORF Phase 4 only proves a synthetic oracle gap and does not supply a selector that can infer the right action. |

## Freshness verdict

**New adjacent work exists; novelty risk is material but not a numerical
invalidation.** By July 2026, per-instance/per-step adaptive allocation under
resource constraints is a populated literature. ORF-B therefore cannot claim the
general idea that conditional allocation beats a global or uniform policy as a
new scientific concept. The Phase-4 numbers also cannot be compared numerically
to these papers because tasks, objectives, costs, and units differ.

The still-distinct contribution is narrower: an SDK-faithful, exactly auditable
finite conditional-regret construction for profile-specific candidate length in
one security-agent scoring system, with a homogeneous equality control and exact
matched-action comparator. Even that contribution is presently a **public
synthetic oracle-value result**, not a learned policy, live-target measurement,
or held-out confirmation. The fresh literature raises the evidence bar rather
than requiring a pivot: a venue-strength contribution would need to demonstrate
learnable profile signals and external/live transfer against current adaptive
allocation baselines. Those actions are outside the authorized scope.

## Gate consequence

Treat freshness as a potential publishability/novelty trigger, not a refutation of
the exact finite result. It strengthens the Phase-5 case for an internal technical
report unless stronger external evidence is later authorized; it does not justify
opening `orf-heldout-v7` or performing any Kaggle action.
