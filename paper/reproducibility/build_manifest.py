#!/usr/bin/env python3
"""Build a non-circular local integrity manifest for the PS-PIR report package."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
OUTPUT = REPO / "paper/reproducibility/MANIFEST.tsv"
REVISION = REPO / "paper/reproducibility/SOURCE_REVISION.txt"

PATTERNS = [
    "results.tsv",
    "state.json",
    "experiments/configs/environment.md",
    "experiments/configs/orf-phase4-v1.json",
    "experiments/orf-p4-baseline/*.py",
    "experiments/orf-p4-baseline/*.tsv",
    "experiments/orf-p4-baseline/*.json",
    "experiments/orf-p4-core/*.py",
    "experiments/orf-p4-ablations/*.py",
    "experiments/orf-p4-generalization/*.py",
    "experiments/orf-p4-scaling/*.py",
    "experiments/orf-phase5-analysis/*.py",
    "experiments/runs/orf-p4-core-v1/*.tsv",
    "experiments/runs/orf-p4-core-v1/COMPLETE.json",
    "experiments/runs/orf-p4-ablations-v1/*.tsv",
    "experiments/runs/orf-p4-ablations-v1/COMPLETE.json",
    "experiments/runs/orf-p4-generalization-v1/*.tsv",
    "experiments/runs/orf-p4-generalization-v1/COMPLETE.json",
    "experiments/runs/orf-p4-scaling-v1/*.tsv",
    "experiments/runs/orf-p4-scaling-v1/COMPLETE.json",
    "paper/*.md",
    "paper/*.py",
    "paper/sections/*.md",
    "paper/tables/*.tsv",
    "paper/figures/*.svg",
    "paper/figures/*.png",
    "paper/figures/*.source.csv",
    "paper/reproducibility/README.md",
    "paper/reproducibility/requirements-*.txt",
    "paper/reproducibility/build_manifest.py",
    "research-log/042*.md",
    "research-log/044*.md",
    "research-log/046*.md",
    "research-log/047*.md",
    "research-log/048*.md",
    "research-log/lit/phase6-*.json",
    "comp/sdk/aicomp_sdk/attacks/contracts.py",
    "comp/sdk/aicomp_sdk/evaluation/ops.py",
    "comp/sdk/aicomp_sdk/scoring.py",
    "comp/sdk/kaggle_evaluation/jed_attack_134815/jed_attack_gateway.py",
]


def main() -> None:
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    REVISION.write_text(
        "# Local source revision\n\n"
        f"git_commit={revision}\n"
        "scope=committed section sources, code, configs, evidence tables, and review foundation\n"
        "external_archive=none\n",
        encoding="utf-8",
        newline="\n",
    )

    paths: set[Path] = set()
    for pattern in PATTERNS:
        paths.update(path for path in REPO.glob(pattern) if path.is_file())
    paths.discard(OUTPUT)
    paths.discard(REVISION)

    rows = ["path\tbytes\tsha256"]
    for path in sorted(paths):
        payload = path.read_bytes()
        rows.append(
            f"{path.relative_to(REPO).as_posix()}\t{len(payload)}\t{hashlib.sha256(payload).hexdigest()}"
        )
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    print(f"manifest=PASS files={len(rows) - 1} source_revision={revision}")


if __name__ == "__main__":
    main()
