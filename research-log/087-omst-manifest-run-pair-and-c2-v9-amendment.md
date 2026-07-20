# OMST common-manifest/run-pair and c2-v9 amendment

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** round-8 adverse verdict accepted; c2-v9 activated; no framework
acquisition, import, compilation, invocation, or correspondence observation

## Decision

Round 8 accepted the unconditional factorization theorem, exact typed witness,
corrected START/source-delivery trace, process-isolation form, scope, taxonomy,
and anti-stacking argument. It rejected the remaining engineering proposition
for four exact reasons:

1. one `E` contained one cell while the conclusions compared pairs;
2. the in-cell guard did not reauthenticate packages, lock, or sources;
3. environment checks actually preceded compile although the prose claimed one
   post-compile guard bundle; and
4. the optional full control shared an antecedent with the task consequence.

c2-v9 changes the engineering interface, not the accepted mathematics. It uses
one common immutable manifest `M` and four independently scoped run objects:

```text
R_task_s0, R_task_s1, R_full_s0, R_full_s1.
```

The two propositions are now separate:

```text
for every M,R_task_s0,R_task_s1,
P_task(M,R_task_s0,R_task_s1)
-> C_task(M,R_task_s0,R_task_s1)

for every M,R_full_s0,R_full_s1,
P_full(M,R_full_s0,R_full_s1)
-> C_full(M,R_full_s0,R_full_s1).
```

Neither antecedent mentions the other role's cells or runs.

## Common manifest and run objects

`M` is a canonical JSON object whose `manifest_payload_sha256` authenticates
all fields except that digest field itself. It binds:

- fixture, launcher, and normative configuration paths and hashes;
- interpreter link, target, version, and hash;
- standard-library JSON path and hash;
- the exact dependency lock;
- LangGraph and LangChain-core distribution names, versions, roots, module
  origins, package roots, and deterministic full-distribution tree hashes;
- all eight load-bearing LangGraph files and all three load-bearing
  LangChain-core files by installed path and SHA-256;
- a separately audited source report, its hash, and the exact six verified
  source/callback assertions;
- `sys.path`, import finders/hooks, site-package roots, and every `.pth` file;
  executable `.pth` files are forbidden;
- absent tracing, profiling, `sitecustomize`, and `usercustomize`; and
- the exact empty callback/tag/metadata/configurable mapping.

A run object `R_cell` is the record of one exact role-launcher child: its bound
cell/run-id pair, common manifest identity, fresh process and temporary
directory, compiled graph, successful final guard, single invoke, and sole
canonical output. Define:

```text
received(cell,M,R_cell)
```

as the UTF-8 canonical mapping serialized at `capture` callable entry before
the callable returns any write in that run.

The antecedents are:

```text
P_task(M,R_task_s0,R_task_s1)
= P_common(M)
  and P_cell(M,task_s0,R_task_s0)
  and P_cell(M,task_s1,R_task_s1)

P_full(M,R_full_s0,R_full_s1)
= P_common(M)
  and P_cell(M,full_s0,R_full_s0)
  and P_cell(M,full_s1,R_full_s1).
```

Thus a failure in `R_full_s0` cannot make the task antecedent false, and a
task-side failure cannot invalidate an otherwise admissible full control.

## Closed v9 bundle

The new unexecuted code-as-text artifacts are:

- `experiments/omst_c2_v9_fixture.py`, SHA-256
  `e9e95741cd306d0aa11456f0977b4e129654653a24a00669fe9aa58e47e20284`;
- `experiments/run_omst_c2_v9_fixture.sh`, SHA-256
  `312e104111cd901fddffd921b378b361d72eb082a728f97b3dbe742afa3f4ffd`;
- `experiments/configs/omst-c2-v9-manifest-run-pairs.json`, SHA-256
  `a93dcc281c995181c55e9e102030ad4da4c46a6208a10b6dd9af19478388249e`;
  and
- `experiments/configs/omst-c2-v9-M0-unacquired.json`, file SHA-256
  `0ee71cc664450cc752e82061d1c0da0a18346e7ce0785f8a712832f8b8b4c40e`,
  canonical payload SHA-256
  `846f502e2984ccfba22fedd7b686f8f56d38d351deb48e62dcec46f131301ec1`.

The fixture has no top-level LangGraph or LangChain-core import. In a future
authorized cell it performs this exact sequence:

```text
load M and verify its canonical payload
-> authenticate the complete common bundle before framework import
-> import LangGraph locally
-> compile exactly one graph
-> verify_all_guards(M,graph,expected_channels)
-> graph.invoke exactly once.
```

`verify_all_guards` immediately follows compilation and precedes invoke. It
reauthenticates every common identity checked before import—including the
config, distributions, distribution-tree hashes, dependency lock, eleven
load-bearing file hashes, source-audit report, and import context—and then
checks compiled channels, mapper, node cache/retry policies, checkpointer,
cache, and store. There is no split environment/compiled assertion window in
the claimed final antecedent. Any failed `require` raises
`OMST_RUNTIME_GUARD_FAILED` before an observation is emitted.

## Role-specific authoritative launch

The launcher accepts exactly two formal inputs: a role in `{task,full}` and an
absolute path naming `M`. Its authoritative outer argument prefix is:

```text
/usr/bin/env -i HOME=/nonexistent PATH=/usr/bin:/bin LANG=C LC_ALL=C TZ=UTC
/bin/bash --noprofile --norc
/home/soh/agent-security/experiments/run_omst_c2_v9_fixture.sh
```

The actual role and actual absolute manifest path are appended as two argv
elements. `task` starts only `task_s0/R_task_s0` and
`task_s1/R_task_s1`. `full` starts only `full_s0/R_full_s0` and
`full_s1/R_full_s1`. Every child uses its own `env -i`, absolute interpreter,
Python `-I -B`, process, and temporary directory. The launcher emits no
launcher-owned stdout.

## Current manifest M0

`M0` records the actual clean-child interpreter/stdlib/import state and exact
v9 artifact hashes. It records:

```text
LangGraph: absent
LangChain-core: absent
dependency lock: absent
source audit: absent
P_common(M0): false
```

Its status is `unacquired`. The first common guard therefore fails with
`manifest_status` before package discovery or framework import. This failure
was established statically from the manifest; the fixture and launcher were
not run.

An acquired manifest is a new immutable artifact. Creating one requires a
separate acquisition authorization and a committed exact LangChain-core source
audit. c2-v9 does not pretend that the currently absent source bundle is
complete.

## Round-8 disposition

| Requirement | c2-v9 author disposition before independent review |
|---|---|
| Common environment and pair quantification | **AUTHOR-RESOLVED:** one `M`, four bound `R_cell`; no free cell variable. |
| Runtime package/source/lock identity | **AUTHOR-RESOLVED:** pre-import authentication plus complete final reauthentication, including distribution trees, lock, eleven source hashes, and source-audit hash. |
| Exact final-guard ordering | **AUTHOR-RESOLVED:** `build_graph`, then `verify_all_guards`, then the only `graph.invoke`. |
| Task/full role separation | **AUTHOR-RESOLVED:** independent `P_task` and `P_full`; each launcher role has exactly two children. |

These are author claims, not reviewer dispositions.

## Static verification

The lower verification rungs, without importing or executing the framework,
established:

```text
v9_bundle_static=PASS fixture_lines=456
final_order=['verify_common_manifest','build_graph','verify_all_guards','invoke']
top_framework_imports=0
M0_payload=846f502e2984ccfba22fedd7b686f8f56d38d351deb48e62dcec46f131301ec1
P_common_M0=false
```

Python AST, both JSON files, Bash syntax, executable mode, every cross-file
hash, role separation, and canonical manifest payload were checked. The
accepted 1,555-case theorem enumeration will be rerun against the superseding
hypothesis before any final reviewer dispatch.

## Scope and authorization

The amendment preserves the classical theorem, exact record-reconstruction
witness, source-conditional scope, capture-before-write semantics, clean shell,
and all nonclaims. It establishes no current framework correspondence and no
empirical/security result.

Authorized: this local code-as-text correction, static syntax/hash checks,
source reasoning already in scope, and—only after deterministic verification—a
single final sterile theory review.

Not authorized: framework download/install/import/compile/invoke; Kaggle;
held-out or locked-test action; live targets; operational attacks; model APIs;
external messages; publication.

## Problem alignment

The correction makes the proposed independent orchestration control genuinely
checkable at a shared-environment/pair boundary without allowing an optional
control or unauthenticated runtime drift to determine the task-side claim.
