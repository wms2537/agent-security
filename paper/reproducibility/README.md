# PS-PIR local reproducibility guide

This guide reproduces the deterministic public-synthetic scorer calculations
from a repository checkout. It does not fetch a beacon, open or freeze a
held-out tier, contact Kaggle, submit a result, or access a live target.

## Evidence boundary

The package is an internal repository artifact. It has no external archive,
DOI, public durability guarantee, or publication release. A content manifest
and local Git revision are recorded during final Phase-6 assembly; those provide
local integrity, not external availability.

## Recorded execution environments

The Phase-4 scorer runs used Linux x86_64, glibc 2.40, CPython 3.14.3 at
`comp/.venv/bin/python`, and `jsonschema==4.26.0`. They were CPU-only and made no
network calls. The Phase-5 figures were generated separately with CPython
3.11.11 and `matplotlib==3.10.9`. The reviewer diagnostic tables use only the
Python standard library and reproduce under either interpreter.

Dependency pins are in `paper/reproducibility/requirements-core.txt` and
`paper/reproducibility/requirements-figures.txt`. These are package-version
records, not a bit-for-bit operating-system container.

## Repository-relative verification

Run these commands from the repository root:

```bash
comp/.venv/bin/python -m unittest \
  experiments/orf-p4-core/test_toy_core.py \
  experiments/orf-p4-ablations/test_toy_ablations.py \
  experiments/orf-p4-generalization/test_toy_generalization.py \
  experiments/orf-p4-scaling/test_toy_scaling.py

comp/.venv/bin/python experiments/orf-phase5-analysis/generate_reviewer_tables.py

python experiments/orf-phase5-analysis/generate_figures.py

python paper/assemble_report.py
python paper/reproducibility/build_manifest.py
python paper/check_revision.py
```

The first command tests the exact finite policy calculations and transformed
constructions. The second regenerates the action-distribution, raw OAT, and
stratum-decomposition TSVs under `paper/tables/`. The third regenerates the
three Phase-5 figures and source CSVs using the recorded figure environment.
The last three commands assemble the ordered section sources, record the local
source revision and content hashes, and run the manuscript evidence checks.

## Scientific-family commands

The commands below are the original repository-relative invocations. The
transactional runners publish an attempt directory exactly once. Re-execution
must therefore use a fresh direct child of `experiments/runs/`; never overwrite
the committed completed attempts.

```bash
comp/.venv/bin/python -I experiments/orf-p4-baseline/run_baseline.py \
  --config experiments/configs/orf-phase4-v1.json

comp/.venv/bin/python -I experiments/orf-p4-core/run_core.py \
  --config experiments/configs/orf-phase4-v1.json \
  --baseline-tables experiments/orf-p4-baseline/score-tables.tsv \
  --attempt-dir experiments/runs/<fresh-core-attempt>

comp/.venv/bin/python -I experiments/orf-p4-ablations/run_ablations.py \
  --config experiments/configs/orf-phase4-v1.json \
  --baseline-tables experiments/orf-p4-baseline/score-tables.tsv \
  --attempt-dir experiments/runs/<fresh-ablation-attempt>

comp/.venv/bin/python -I experiments/orf-p4-generalization/run_generalization.py \
  --config experiments/configs/orf-phase4-v1.json \
  --attempt-dir experiments/runs/<fresh-changed-attempt>

comp/.venv/bin/python -I experiments/orf-p4-scaling/run_scaling.py \
  --config experiments/configs/orf-phase4-v1.json \
  --baseline-tables experiments/orf-p4-baseline/score-tables.tsv \
  --attempt-dir experiments/runs/<fresh-scaling-attempt>
```

`<fresh-...>` is documentation syntax and must be replaced with a new explicit
directory name. The baseline's committed score table is already present; its
runner enforces its own publication rules and should not be used to overwrite
the committed evidence.

## Canonical inputs and outputs

| Family | Input/code | Committed output |
|---|---|---|
| Baseline | `experiments/configs/orf-phase4-v1.json`; `experiments/orf-p4-baseline/run_baseline.py` | `experiments/orf-p4-baseline/score-tables.tsv`; `aggregate-by-length.tsv`; `baseline-summary.json` |
| Core/sanity check | `experiments/orf-p4-core/run_core.py`; baseline score table | `experiments/runs/orf-p4-core-v1/core-by-master.tsv`; `homogeneous-by-master.tsv`; `COMPLETE.json` |
| OAT | `experiments/orf-p4-ablations/run_ablations.py` | `experiments/runs/orf-p4-ablations-v1/ablation-by-master.tsv`; `COMPLETE.json` |
| Changed construction | `experiments/orf-p4-generalization/run_generalization.py` | `experiments/runs/orf-p4-generalization-v1/generalization-by-master.tsv`; `COMPLETE.json` |
| Nested prefixes | `experiments/orf-p4-scaling/run_scaling.py` | `experiments/runs/orf-p4-scaling-v1/scaling-by-cell.tsv`; `COMPLETE.json` |
| Reviewer diagnostics | `experiments/orf-phase5-analysis/generate_reviewer_tables.py` | `paper/tables/action-distributions.tsv`; `oat-raw-summary.tsv`; `stratum-regret-decomposition.tsv` |

The `COMPLETE.json` manifests bind source, input, and output hashes for each
transactional family. The report's full historical ledger remains `results.tsv`.

## Known reproducibility limits

- No OS image or container is archived.
- The repository has no public clone URL or permanent archive.
- Hardware timing is not expected to match across systems; scientific outputs
  are integer/rational deterministic calculations.
- No command in this guide validates live transfer, learns a selector, or opens
  an untouched evaluation tier.
