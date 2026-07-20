# OMST trust-boundary research and structural pivot

**Date:** 2026-07-20 · **Phase:** 2 · **Cycle:** 2 · **Iteration:** 5→6  
**Status:** targeted research complete; OMST executable bridge concluded;
PDPF selected as the next active direction

## Question

Can round 9's nine defects be closed by a bounded OMST correction, or would the
required trust root turn the schema-sufficiency control into a separate
software-supply-chain system?

## Five-source primary investigation

1. **SLSA Build Provenance v1.2.** Provenance binds output subjects to a build
   definition and builder, but the `builder.id` represents the transitive
   closure of entities trusted to run and record the build. External parameters
   must be verified downstream, and resolved dependencies are recorded only
   when known. This confirms that a manifest cannot self-declare its own trust
   boundary.  
   Source: <https://slsa.dev/spec/v1.2/build-provenance>

2. **SLSA artifact verification v1.2.** Consumers must start from a
   preconfigured root of trust, verify the provenance envelope signature,
   match the statement subject to the artifact digest, and check builder/build
   expectations. A digest plus `status=passed` is not authentication.  
   Source: <https://slsa.dev/spec/v1.2/verifying-artifacts>

3. **in-toto Attestation Framework v1.2.** Its four layers are deliberately
   separate: predicate, subject-binding statement, authentication envelope,
   and multi-attestation bundle. v9 implemented only self-relative statement
   consistency; it had no independently rooted envelope or verified bundle.  
   Source: <https://github.com/in-toto/attestation/blob/main/spec/README.md>

4. **PEP 751.** The final Python `pylock.toml` standard records installation
   inputs and file hashes so installation does not resolve dependencies at
   consumption time. Its goal is installation reproducibility and auditability,
   not proof that every subsequently importable filesystem byte or loaded code
   object matches the lock. Round 9 was therefore correct that hashing an
   arbitrary lock does not authenticate an executable closure.  
   Source: <https://peps.python.org/pep-0751/>

5. **Linux fs-verity and sealed memfd.** fs-verity makes a file read-only and
   verifies every read against a kernel-maintained Merkle tree; the enforced
   digest can be retrieved in constant time. `memfd_create` plus write/grow/
   shrink/seal seals prevents a shared in-memory object from changing after it
   is populated. These mechanisms can close time-of-check/time-of-use mutation,
   but require OS support and still need an external key/policy trust root.  
   Sources: <https://docs.kernel.org/6.15/filesystems/fsverity.html> and
   <https://www.man7.org/linux/man-pages/man2/memfd_create.2.html>

## Synthesis

The minimal trustworthy execution capsule would require all of the following:

```text
preconfigured verifier root
-> verified signed in-toto/SLSA envelope
-> subject digest for a complete executable capsule
-> exact dependency/build closure
-> kernel-enforced immutable loaded bytes
-> broker-owned child launch and atomic pair envelope
-> direct fixture-owned capture bytes.
```

This is technically coherent. It is not a bounded fix to OMST. It introduces a
new supply-chain/control-plane trust model, OS portability constraints, signing
and key governance, capsule construction, and a large verification surface.
Without those pieces, calling v9 “authenticated” is false; with them, the
infrastructure dominates the scientific question.

The source result also explains why adding more hashes is the wrong move:
hashes answer *which bytes?*; an external trust root answers *who is authorized
to name those bytes?*; immutable loading answers *were those the bytes actually
executed?*; an atomic broker receipt answers *did both observations belong to
one pair?* These are different properties and cannot be collapsed into one
self-hashed JSON file.

## Candidate critique

### A — Attested Pair Capsule repair

- **Move:** replace v9's mutable self-relative manifest with signed in-toto/SLSA
  provenance, an fs-verity/sealed capsule, exact PEP-751-derived closure, and an
  atomic pair broker.
- **Most likely failure:** the supply-chain platform becomes the contribution,
  while OMST's schema control remains a classical two-state witness.
- **Hardest trap:** binding interpreter, stdlib, native modules, dynamic imports,
  builder identity, keys, and every executed byte without an unverifiable
  bootstrap.
- **Evidence check:** the five primary sources show the necessary mechanisms,
  but also prove v9 omitted their trust roots and that PEP 751 alone is
  insufficient. No acquired capsule or measured bottleneck exists.
- **Score:** impact 3 × feasibility 1 ÷ complexity 5 = **0.60**.
- **Decision:** reject. It is principled infrastructure, but it changes the
  problem and triggers the engineering/Bridge×Synthesis burden without the
  required profile artifact.

### B — theorem-only OMST downgrade

- **Move:** retain only the reviewer-accepted factorization theorem and exact
  record witness; drop every executable framework correspondence claim.
- **Most likely failure:** honest but scientifically thin; it does not answer
  whether orchestration rewrites preserve security properties.
- **Hardest trap:** presenting a standard quotient result as a novel OMST
  contribution despite repeated novelty disclaimers.
- **Evidence check:** rounds 5–9 repeatedly found the theorem and witness
  correct. They also repeatedly rejected standalone novelty/security scope.
- **Score:** impact 1 × feasibility 5 ÷ complexity 1 = **5.00**.
- **Decision:** retain as a bounded negative/design result, not as the next
  active study.

### C — close OMST and pivot to a Progress Quotient Firewall

- **Move:** conclude OMST's empirical contrast as theory-refuted and its
  executable bridge as implementation-defeated; preserve the theorem/witness;
  activate PDPF with a narrower single-process abstract control. The firewall
  observes only verifier-owned obligation deltas, never worker text, raw tool
  payloads, or worker-authored “progress.”
- **Most likely failure:** progress becomes definitionally safe because the
  verifier and success predicate are co-designed, repeating OMST v3's forced
  contrast.
- **Hardest trap:** defining independently checkable obligation transitions
  that preserve benign completion without leaking untrusted content through
  IDs, counts, timing, or failure reasons.
- **Evidence check:** `PROBLEM.md` already defines progress integrity; LoopTrap
  motivates independent progress verification; round 9 shows whole-runtime
  authentication is a distracting trust layer. A local verifier-owned receipt
  can be observed directly without claiming remote authenticity.
- **Score:** impact 5 × feasibility 4 ÷ complexity 2 = **10.00**.
- **Decision:** **select**. It changes the system dimension from schema
  projection to continuation-decision observation, directly matching the
  second portfolio study.

## New conceptual direction

The selected local move is **Progress Quotient Firewall (PQF)**, a sharpened
form of PDPF.

Let an inert execution trace `z` contain worker text, tool payloads, and
verifier-owned obligation state. Define a quotient observation:

```text
q(z)=(verified_open_obligation_ids,
      verified_completed_obligation_ids,
      verified_effect_ids,
      remaining_step_budget).
```

The continuation controller receives only `q(z)`. It never receives raw text,
tool arguments/results, worker summaries, or worker-authored progress labels.
The verifier that updates `q` is fixed independently of the controller and
writes the receipt directly into fixture-owned storage.

The distinguishing question is not “can a safer controller be built?” It is:

> When task obligations and decision tapes are matched, does erasing
> worker-controlled content from the continuation decision reduce abstract
> termination-integrity failures without exceeding the preregistered benign
> completion and step-overhead limits?

This remains falsifiable: if content erasure does not reduce failures, causes
more than five percentage points completion loss, or adds more than 20% steps,
the hypothesis fails. Co-designed safety is a named primary rival that the next
hypothesis must defeat with independent oracle construction and negative
controls before any run.

## Decision and accounting

- OMST's accepted theorem/witness remain immutable historical findings.
- OMST's framework bridge does not pass Phase 2 and will not be repaired by
  adding unattested hashes.
- The portfolio moves to PDPF/PQF as a new research iteration.
- Research-iteration accounting advances from 2/5 to 3/5.
- Hypothesis-review accounting remains 20/20. The next hypothesis may be written
  and statically checked, but no reviewer may be dispatched without a user-set
  numeric extension.

## Problem alignment

PQF directly tests an independently checkable control over agent-loop
continuation while avoiding the false claim that a self-consistent local
manifest authenticates an entire runtime supply chain.

## Authorization boundary

No framework acquisition/import/execution, package installation, live target,
attack or jailbreak reproduction, Kaggle action, held-out/locked-test action,
model API, external message, or publication occurred.
