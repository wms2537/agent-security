# ORF lexical attempt-identity fix

**Date:** 2026-07-19 · **Phase:** 4 · **Cycle:** 1 · **Iteration:** 4 · **Status:** implemented and locally verified, scientific core unexecuted

## Context

Sterile review round 2 resolved the original stale/partial-bundle HIGH but found
that resolving a raw attempt path before checking it allowed a dangling or live
symlink at the preregistered name to alias a different child. T024 repairs the
identity check at its source.

## Content

The bundle helper now:

1. normalizes raw attempt and expected paths lexically with absolute/normpath
   operations, without resolving the child;
2. requires that lexical path to be an exact direct child of the already
   resolved runs parent;
3. uses `os.path.lexists` and `lstat` to reject every existing creation name,
   including live and dangling symlinks;
4. rejects symlink/non-directory attempt or expected identities during
   verification and compares their exact lexical paths;
5. reads the final directory and artifacts through `O_DIRECTORY|O_NOFOLLOW`
   descriptors with inode/type/content stability checks; and
6. retains `renameat2(RENAME_NOREPLACE)` as the atomic publication-race
   backstop, while abort paths fail closed on changed aliases.

Five adversarial tests were added for constructor aliases, publish aliases with
untouched targets, raw-attempt verifier aliases, expected-identity aliases, and
a symlink installed immediately before publish.

## Gate Check

Independent checks after the implementation:

- static compilation passed for the helper and its tests;
- bundle suite: `Ran 15 tests in 0.081s` / `OK`;
- core toy suite: `Ran 4 tests in 0.000s` / `OK`;
- the publication-race test proves `RENAME_NOREPLACE` leaves the alias target
  absent and preserves one failed staging sibling without `COMPLETE.json`;
- the repository run parent still contains only the two historical support
  calibrations, and `experiments/runs/orf-p4-core-v1` is absent;
- `git diff --check` passes, and only the helper/test files changed before this
  record update.

T024's local implementation gate passes. T016 remains closed pending another
sterile reviewer verdict.

## Problem alignment

The exact preregistered attempt label is part of the experiment identity. This
repair makes the lexical command path and verified bundle path agree even in the
presence of malicious or accidental symlink aliases.

## Decision

Keep the fail-closed lexical identity repair and request sterile re-review.

## Next Steps

Commit the helper/tests and this evidence, then re-review source only. Do not run
the scientific core, held-out target, network, or Kaggle action before `SOUND`.
