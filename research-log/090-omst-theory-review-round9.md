# OMST theory review — round 9

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5

**Status:** NEEDS_REVISION

The complete reviewer response is preserved verbatim below.

---

**Status: DONE**

## Blind assessment

**Overall: NEEDS_REVISION**

The hypothesis file has **1,018 lines**.

I found no countermodel to the unconditional factorization theorem or exact two-state witness. The two role-specific implications are also valid if their semantic antecedents are interpreted literally. The adverse verdict concerns the engineering correspondence: the runtime protocol does not establish several facts it calls authenticated, permits run-specific fields in a purportedly common manifest, does not pin one manifest across a pair, and does not prove that emitted bytes are the bytes seen at callable entry.

### Previous-review disposition

| Item | Judgment | Basis |
|---|---|---|
| 1. Common manifest and four bound run objects | **IMPROVED** | The formal free-variable defect is fixed: all pair variables are quantified and role predicates are separate (`hypothesis`: 286–328, 697–720, 722–786). But “common immutable” is not enforced: the manifest schema accepts arbitrary extra cell/process fields, and sequential children can load different payloads from the same path. |
| 2. Runtime reauthentication | **IMPROVED** | The verifier is rerun before import and after compile (`fixture.py`: 362–371, 396–426). However, distribution/module identities are manifest-controlled, the lock is not reconciled with installed packages, the distribution inventory is incomplete, and the audit report has no trust/content verification. |
| 3. One complete final guard immediately before invoke | **RESOLVED** | Static AST order is exactly `verify_common_manifest` → `build_graph` → `verify_all_guards` → the sole `graph.invoke` (`fixture.py`: 416–427). There is no top-level LangGraph/LangChain-core import; the LangGraph import is local (`fixture.py`: 379–393). |
| 4. Independent task/full antecedents | **RESOLVED** | `P_task` contains only `task_s0/task_s1`; `P_full` contains only `full_s0/full_s1`; both implications bind all run objects (`hypothesis`: 697–720, 724–785). |

### Independent mathematical derivation

For total \(\pi:S\to Q\), with \(Q=\operatorname{im}\pi\), and total \(\tau:S\to Y\):

- If \(\tau=g\circ\pi\), then \(\pi(s)=\pi(s')\) implies \(\tau(s)=\tau(s')\). Thus \(\ker\pi\subseteq\ker\tau\).
- Conversely, under kernel inclusion, define \(g(q)=\tau(s)\) for any \(s\) satisfying \(\pi(s)=q\). Surjectivity onto \(Q=\operatorname{im}\pi\) gives existence; kernel inclusion gives representative independence.
- If \(g_1,g_2\) factor \(\tau\), every \(q\in Q\) is \(\pi(s)\) for some \(s\), so \(g_1(q)=\tau(s)=g_2(q)\).

Boundary checks:

- **Empty \(S\):** \(Q=\varnothing\); the empty factor is unique, including when \(Y=\varnothing\). Closure is vacuous.
- **Infinite \(S\):** no global choice function is needed; the graph relation defines \(g\). For example, parity factors through the parity projection on \(\mathbb Z\), whereas \(\tau(n)=n\) does not.
- **Strict larger codomain \(D\supsetneq\operatorname{im}\pi\):** assuming closure, off-image values must be supplied. If \(Y=\varnothing\), no extension exists because \(D\setminus Q\neq\varnothing\); if \(|Y|=1\), the extension is unique; if \(|Y|\ge2\), it is nonunique. This countermodel does not touch the stated theorem because the theorem fixes \(Q=\operatorname{im}\pi\).
- Partial and multivalued mappings remain outside the theorem.

For the witness, \(X=\{x\}\) and \(P=\{p_0,p_1\}\), with \(J(p_0)\ne J(p_1)\). The sole \(\pi_{\text{task}}\)-fiber contains both states but two target values, so any \(g_{\text{task}}:X\to J(P)\) chooses one value and fails on at least the other state. The full projection is the identity on \(X\times P\), so its factor is unique. Collapsing \(J(p_0),J(p_1)\), removing a witness state, or admitting external/nondeterministic reconstruction defeats the witness, but each is explicitly outside its declared domain.

### Quantification and non-circularity

- All four run objects are bound, and there is no free `cell` in either expanded role implication.
- The two antecedents contain only their respective cells.
- Failed/missing runs do not denote `received`; formally, both `P_cell` predicates must hold.
- PC1–PC6 do not state either cross-run conclusion. PR5 also does not literally state task equality or the exact full difference.
- There is nevertheless a testability problem: PR5 assumes the per-run delivery and output-origin fact needed to interpret future output, while the authenticated source trace stops at callable entry. Thus the implication is not cross-run circular, but the operational evidence for its antecedent is incomplete.
- `M0` itself contains no cell/process field. The universal manifest format does not enforce that restriction.

### Static checks that passed

- The committed hashes match the declarations for the config, `M0`, fixture, and launcher. Launcher mode is `100755`.
- `M0`’s raw SHA-256 and canonical payload digest both match the hypothesis. It has `status=unacquired`; after `load_manifest`, `verify_common_manifest` fails first at `manifest_status` (`fixture.py`: 212–229, 362–364).
- The four literal state/schema/channel/run-ID bindings are correct (`fixture.py`: 64–133).
- Capture canonicalizes before returning its write (`fixture.py`: 374–376).
- The task and full launcher branches each launch exactly their own two named cells (`launcher.sh`: 24–32).
- Checkpointer, cache, store, retry, cache policy, mapper, and compiled channels are checked in the single final guard (`fixture.py`: 396–413).
- The conditional source chain through START, `_get_updates`, `LastValue`, fresh checkpoint/channels/cache, `_proc_input`, task input, `PregelNode`/`RunnableSeq`, bound callable, callback/config premise, and capture entry is structurally coherent. Because `M0` lacks the framework sources and source-audit report, none of those external source lemmas is presently discharged.

### Severity-ordered defects

1. **The “common immutable manifest” is neither schema-enforced nor pair-pinned.**  
   What prevents an acquired `M` from containing `"cell"` or `"process"`? Nothing: `load_manifest` checks only schema-version equality, bound path, and a self-computed digest; it rejects no extra fields (`fixture.py`: 212–229). What forces both sequential children to load the same payload? Nothing: the launcher passes a path twice and never pins or compares the emitted manifest IDs (`launcher.sh`: 7–21, 24–32). The file can change between children. This contradicts `hypothesis`: 257–284, 315 and the common-bundle derivations at 735–767.

2. **Package authentication is not bound to the distributions or modules actually claimed.**  
   `verify_packages` fixes only the dictionary keys. Both `record["distribution"]` and `record["module"]` come from the manifest and are never required to equal `langgraph`/`langchain-core` and `langgraph`/`langchain_core` (`fixture.py`: 272–303). Therefore a record can authenticate another distribution’s version/tree/origin while `build_graph` imports `langgraph.graph`. No post-import check authenticates the actual imported module objects. This directly conflicts with `hypothesis`: 268–270, 423–425, 638–645.

3. **The dependency lock and “full distribution trees” do not authenticate the executable dependency closure.**  
   The lock check verifies only that an arbitrary nominated file exists and matches its manifest hash; it is not parsed or reconciled with installed distributions (`fixture.py`: 264–269). The tree hash iterates `Distribution.files`, normally RECORD-listed files, not every file physically present, and ignores other dependency distributions (`fixture.py`: 168–177). Unrecorded importable files and load-bearing dependencies remain outside the hash surface. The claim of inventories of “every installed distribution file” at `hypothesis`: 268–270 is too strong.

4. **Output origin is not proved or authenticated.**  
   The source trace ends when `capture` receives input (`hypothesis`: 612–624). Actual output is obtained later from `graph.invoke`’s returned state (`fixture.py`: 426–427), then hex-encoded and printed (`fixture.py`: 445–452). There is no authenticated lemma for `capture return → channel write → final graph result → result["received_input"]`, and the relevant writer/output implementation is not clearly in the eleven-file source surface. PR5 simply assumes that the sole output derives from entry bytes (`hypothesis`: 689–692). A framework implementation could preserve callable-entry delivery yet transform the returned update, making the emitted observation unusable without falsifying any listed L-lemma.

5. **Run-role and launcher origin are not attested.**  
   What proves a five-field record came from the claimed role launcher and outer argv? Nothing in the child checks its parent, role, or outer argv. Direct fixture invocation can emit the same record as long as cell and run ID agree (`fixture.py`: 416–452). The launcher also fails to require exactly two arguments; extra arguments are ignored (`launcher.sh`: 7–10). PR1’s “spawned only by the matching role launcher branch” (`hypothesis`: 673–675) cannot be recovered from the output record.

6. **Double hashing does not close the audit-to-invoke drift window.**  
   Files are hashed, then imported/compiled, then hashed again. A transient substitution restored before the final guard can leave unauthenticated in-memory code while all final disk hashes pass (`fixture.py`: 422–426). The final guard checks filesystem identities and selected compiled attributes, not code-object identity. Consequently the Occam claim that post-compile reauthentication “closes” the drift window (`hypothesis`: 909–917) is false without an immutable filesystem/snapshot or authenticated loading from pinned bytes.

7. **The verifier and canonicalizer depend on unauthenticated pre-import standard-library code.**  
   `json`, `hashlib`, `importlib`, `site`, and other verifier dependencies are imported before manifest authentication (`fixture.py`: 5–16). Only `json/__init__.py` is hashed (`fixture.py`: 247–261), not `json.encoder`, `_json`, import machinery, metadata parsing code, or relevant dynamic libraries. The manifest parser and digest computation already use the loaded `json`. Thus the exact canonicalizer and authentication mechanism are not fully source-bound.

8. **The source-audit report is bound as bytes, not verified as evidence.**  
   Runtime checks only `status="passed"`, path/hash, and an assertion-name list stored in the manifest (`fixture.py`: 332–346). It does not parse the report or anchor it to a trusted reviewer/tool identity. PC4 correctly says semantic truth is an extra premise (`hypothesis`: 647–655), which saves the formal implication, but a successful runtime guard cannot establish PC4. Calling this runtime “authentication” overstates what the protocol proves.

9. **Missing-run semantics are sound formally but not enforced at the role-output boundary.**  
   The first child’s record is streamed before the second child runs. If the second fails, a partial apparent observation remains on stdout (`launcher.sh`: 24–32). The logic excludes it because the pair antecedent is false, but there is no atomic role envelope or parser ensuring downstream consumers cannot treat it as a completed pair.

### Justification and scope

The mathematical assumptions and narrow scope are unusually clear. The fixed bias surface has exactly eight items; the anti-stacking argument is correct; the taxonomy does not inflate the theorem; and the document repeatedly avoids causal, prevalence, vulnerability, or production-security claims. The task/full separation also preserves the optional-control semantics.

The rival-explanation and parsimony sections are incomplete because they omit manifest mutation between children, direct child invocation, arbitrary distribution/module bindings, unrecorded/dependency code, transient file substitution, and post-capture result mutation. The causal project framing is not improperly acquired by this hypothesis, but “authentication” should be narrowed to self-consistency until a trust root and executable-code binding exist.

Uncertainty: I did not import or execute LangGraph/LangChain-core. Since `M0` contains neither package nor source-audit report, I could audit only the stated conditional source chain and its coverage, not verify the future source lemmas themselves.

## Actionable coaching

1. Define and enforce an exact manifest schema: exact top-level/nested key sets, types, absolute lexical paths, and explicit rejection of cell, run, PID, tempdir, and process fields.

2. Have the role launcher read one manifest once, pin its expected payload digest, pass both path and digest to each child, capture both outputs, require identical IDs, and emit a single pair envelope only after both children succeed. Require `"$#" -eq 2`.

3. Hard-code the expected distribution and module names. After import, check the actual `langgraph` and `langchain_core` module specs/origins and bind every imported load-bearing module to authenticated bytes.

4. Parse the dependency lock and compare it with the installed dependency closure. Inventory the filesystem beneath controlled package roots rather than relying only on `Distribution.files`, or execute in a content-addressed immutable environment.

5. Eliminate the transient-substitution window by loading authenticated source bytes from an immutable snapshot, verified file descriptors, or a sealed environment. Rehashing mutable paths before and after import is insufficient.

6. Make the source audit machine-readable and independently anchored. The runtime should verify the report’s bundle digest, assertions, tool/reviewer provenance, and result—not merely a manifest-supplied label list.

7. Capture callable-entry bytes in fixture-controlled storage before returning from `capture`, and produce `observed_hex` from that storage rather than from `graph.invoke`’s final state. Otherwise add and authenticate the entire post-capture writer/output trace and its source files.

8. Materialize real run objects containing role, parent/child argv, pinned manifest ID, exit status, event ordering, guard results, and exact stdout/stderr. A five-field child record is not evidence for PR1–PR5.

9. Add static negative tests for: extra manifest cell/process fields, manifest replacement between children, wrong distribution/module names, an empty or irrelevant lock, a meaningless audit report, extra launcher arguments, direct child invocation, unrecorded package files, and post-capture output transformation.

10. Retain the narrow record-reconstruction scope, but call the present mechanism “manifest-relative identity checking” until the authentication and output-origin gaps are closed.
