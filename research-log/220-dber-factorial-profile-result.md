# DBER four-policy factorial profile — result

Date: 2026-07-26  
Phase: 2  
Task: T088  
Frozen implementation commit: `fb1c9f5`  
Process exit: `2`  
Outcome: `DISCONFIRM / 3 OF 12 UNITS VALID`

## Integrity

The complete frozen 12-unit population ran once in its preregistered order.
Nothing was dropped or rerun. All four expected stop classes matched the
controller's direct terminal instrumentation:

- G: generation on seeds 41, 42, 43;
- R0: replay on seeds 41, 42, 43;
- R1: replay on seeds 41, 42, 43;
- K: candidate on seeds 41, 42, 43.

Independent artifact reconstruction passes:

```text
candidate_rows=526
policy_portfolios_checked=48
units=12
status=PASS
```

Artifact identities:

- summary JSON:
  `908545a81e39e9faaa628123c96651834efdc8d98edde6b88ee0c9592a04d970`;
- candidate JSONL:
  `b5ada8f7e69422e6104867e9ecb226c00627109993a08b6276a72d19d2388944`;
- summary TSV:
  `cb8337ab42beb88ae7566ede1cbbf8dc4a9a8374852c298a4015f42781c6332b`;
- verification JSON:
  `822c2a64e2cde7ef03dbce35b89634d78eac21838309eb5a27139d84c4f88849`.

The candidate artifact has 526 rows. The summary TSV has one header plus all 12
units.

## Complete result

| unit | stop | valid | counts I/H/G/B | raw I/H/G/B | actual replay cost I/H/G/B (s) | safe cap (s) |
|---|---|---:|---:|---:|---:|---:|
| G-41 | generation | no | 47/73/73/73 | 846/1314/1314/1314 | 5.003/7.852/7.852/7.852 | 5.940 |
| G-42 | generation | no | 45/69/69/69 | 810/1242/1242/1242 | 4.791/7.474/7.474/7.474 | 5.940 |
| G-43 | generation | no | 47/73/73/73 | 846/1314/1314/1314 | 5.110/8.007/8.007/8.007 | 5.940 |
| R0-41 | replay | no | 5/5/5/31 | 90/90/90/558 | 0.555/0.555/0.555/3.346 | 0.178 |
| R0-42 | replay | no | 4/4/4/32 | 72/72/72/576 | 0.414/0.414/0.414/3.560 | 0.178 |
| R0-43 | replay | no | 5/5/5/32 | 90/90/90/576 | 0.557/0.557/0.557/3.521 | 0.178 |
| R1-41 | replay | no | 2/3/2/43 | 36/54/36/774 | 0.279/0.372/0.279/4.203 | 0.178 |
| R1-42 | replay | no | 2/2/2/43 | 36/36/36/774 | 0.296/0.296/0.296/4.148 | 0.178 |
| R1-43 | replay | no | 3/3/3/42 | 54/54/54/756 | 0.440/0.440/0.440/4.090 | 0.178 |
| K-41 | candidate | yes | 3/3/3/3 | 54/54/54/54 | 0.340/0.340/0.340/0.340 | 5.940 |
| K-42 | candidate | yes | 3/3/3/3 | 54/54/54/54 | 0.328/0.328/0.328/0.328 | 5.940 |
| K-43 | candidate | yes | 3/3/3/3 | 54/54/54/54 | 0.346/0.346/0.346/0.346 | 5.940 |

`I/H/G/B` means incumbent, headroom-only, generation-gated, and bank-all.

## Prediction disposition

### Generation-wide: score gain exists, safety fails

Headroom-only and generation-gated are identical as predicted and add 432–468
official raw. Their per-seed gain is 53.33–55.32%. But actual full replay is
7.474–8.007 seconds against a 5.94-second safe cap and even exceeds the
6-second hard budget. The joint score-and-safety prediction is disconfirmed in
all three units.

### Replay no-fit: no additions, but the incumbent itself is unsafe

Both bounded policies equal the incumbent and bank-all overflows, as predicted.
However, full fresh replay of the unchanged incumbent costs 0.414–0.557 seconds
against a 0.1782-second safe cap and 0.18-second hard budget. These units expose
an upstream estimator defect rather than support the reuse policy.

### Replay residual-fit: distinguishing score prediction is unstable and unsafe

Seed 41 gives the intended distinction: headroom-only admits one probe and gains
18 raw while generation-gated remains at the incumbent. Seeds 42 and 43 admit no
probe, so the positive-gain prediction fails. More importantly, every incumbent
already exceeds the actual replay budget, and seed 41's added candidate raises
cost from 0.279 to 0.372 seconds. All three R1 units are invalid.

### Candidate cap: exact no-op passes

All four policies return the same three candidates and 54 raw. These are the
only three valid units. They confirm only cap totality, not a useful mechanism.

## New measured bottleneck

The earlier profile reused one already-built generation environment and therefore
omitted fresh per-candidate construction and scoring work. Across verified-fill
candidates, full replay divided by generation-episode time was:

| regime | n | mean ratio | min | max | mean additive gap (s) |
|---|---:|---:|---:|---:|---:|
| G | 139 | 3.013 | 1.487 | 4.543 | 0.0705 |
| R0 | 14 | 3.130 | 2.475 | 3.719 | 0.0740 |
| R1 | 7 | 2.269 | 1.687 | 2.991 | 0.0795 |
| K | 9 | 3.128 | 2.687 | 3.903 | 0.0765 |

This is not random score noise. It is a missing lifecycle component: the
controller observes interaction/reset time inside one existing environment,
whereas the evaluator constructs a new environment/agent/guardrail and computes
predicates/signatures for every returned candidate.

`alpha=2` applied only to supplements cannot repair an underestimated incumbent
base. The profile therefore refutes both the generation-gated and headroom-only
mechanisms as currently formulated. Bank-all is also unsafe. The generation
classifier earns no distinct safety credit.

## Competition interpretation

The controlled budgets deliberately amplify fixed local SDK overhead, so this
does not prove that the completed 81.225 live submission exceeded its real
replay budget; completion is evidence that it did not void. It does prove that
attack-side episode latency alone is not a portable complete-replay estimator,
and that the proposed extra candidates cannot pass a confidence-before-submission
gate without a separately justified full-lifecycle cost model.

No DBER/headroom admission code will be added to the candidate-producing path
from this result. No Kaggle push, commit run, or submission occurred.
