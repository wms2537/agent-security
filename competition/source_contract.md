# Competition Source Contract

Date: 2026-07-26

Active path:

- `experiments/attack.py` is the only source of the attack policy.
- `submission/build_notebook.py` renders the two Kaggle notebook copies from `experiments/attack.py`.
- `submission/kernel/kernel-metadata.json` and root `kernel-metadata.json` bind the Kaggle kernel metadata.
- `competition/leaderboard_experiments.tsv` records target-owned Kaggle submission evidence only.
- `competition/mechanics_experiments.tsv` records local SDK/mock/static evidence only.

Stage A hypothesis:

Fixed-count deterministic single-post fill with only a three-arm fingerprint will recover throughput lost to over-probing, full-candidate verification, and unidentifiable replay-cost sizing.

Immutable incumbent control:

- Tag: `lb-81.225-ref-54923079`
- Kaggle submission ref: `54923079`
- Public score: `81.225`
- Scope: complete bundled artifact only; no component attribution.

Current active variant:

- Candidate structure: one user message containing one `http.post` instruction to a deterministic unique clean domain.
- Arms: `plain`, `bare`, `harmony`.
- Probe policy: one probe per arm plus at most one confirmation probe under ambiguity.
- Verification mode: no full-candidate generation-side verification after arm selection.
- Sizing mode: fixed returned candidate count.
- Initial count: `1950`.

Submission gate:

A Kaggle competition submission is allowed only after static checks pass, the notebook rebuild is committed, and the active control path is validated in a two-point comparison batch.

Current rule:

- `Kaggle commit runs and pushes` are measurement actions only.
- Before any interpretation of attack improvements, run:
  1) a known-good historical control reference,
  2) current Stage-A candidate control,
  3) compare whether blank-score failures are shared.
- Only when the reference is confirmed to score correctly should we attribute changes to attack logic.
