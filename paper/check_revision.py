#!/usr/bin/env python3
"""Deterministic structural and evidence checks for PS-PIR revision 2."""

from __future__ import annotations

import csv
import json
import re
import subprocess
from difflib import SequenceMatcher
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PAPER = REPO / "paper"
SECTIONS = [PAPER / "sections" / f"{index:02d}-{name}.md" for index, name in [
    (1, "abstract"),
    (2, "introduction"),
    (3, "related-work"),
    (4, "methodology"),
    (5, "experimental-setup"),
    (6, "results"),
    (7, "discussion"),
    (8, "conclusion"),
    (9, "references"),
    (10, "supplementary"),
]]
V1_COMMIT = "08f300f"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def prose_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    in_fence = False
    for block in re.split(r"\n\s*\n", text):
        stripped = block.strip()
        if stripped.startswith("```"):
            in_fence = not (stripped.count("```") % 2 == 0)
            continue
        if in_fence or not stripped:
            continue
        lines = stripped.splitlines()
        if any(line.startswith(("#", "|", "- ", "* ", ">")) for line in lines):
            continue
        normalized = re.sub(r"\s+", " ", stripped)
        if len(normalized.split()) >= 30:
            paragraphs.append(normalized)
    return paragraphs


def near_identical_ratio() -> tuple[int, int, float]:
    current: list[str] = []
    previous: list[str] = []
    for path in SECTIONS[:8]:
        current.extend(prose_paragraphs(path.read_text(encoding="utf-8")))
        relative = path.relative_to(REPO).as_posix()
        old = subprocess.run(
            ["git", "show", f"{V1_COMMIT}:{relative}"],
            cwd=REPO,
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        previous.extend(prose_paragraphs(old))
    matched = sum(
        1
        for paragraph in current
        if previous
        and max(SequenceMatcher(None, paragraph, old).ratio() for old in previous) >= 0.90
    )
    ratio = matched / len(current) if current else 1.0
    return matched, len(current), ratio


def main() -> None:
    require(all(path.is_file() for path in SECTIONS), "one or more section files missing")
    report = PAPER / "orf-internal-technical-report.md"
    require(report.is_file(), "assembled report missing")
    main_text = "\n".join(path.read_text(encoding="utf-8") for path in SECTIONS[:8])
    full_text = report.read_text(encoding="utf-8")

    require("Public-Synthetic Perfect-Information Regret" in main_text, "PS-PIR name missing")
    require("value of perfect information" in main_text.lower(), "VOI framing missing")
    require("post-calibration" in main_text.lower(), "calibration chronology missing")
    require("designer-specified" in main_text.lower(), "construction provenance missing")
    require(
        any(token in main_text for token in [r"q_z(m)\geq0", r"q_z(m)\geq 0", r"q_z(m) \geq 0"]),
        "q>=0 fix missing",
    )
    require("1.855" not in main_text, "sample SD remains in scientific prose")
    require("21.694" not in main_text, "standardized mean remains in scientific prose")
    require("/home/soh" not in full_text, "machine-specific path remains")

    for value in ["41.437632", "38.111187", "41.198295", "10,380,000"]:
        require(value in full_text, f"required diagnostic/result value missing: {value}")

    action_rows = read_tsv(PAPER / "tables/action-distributions.tsv")
    require(len(action_rows) == 3, "action distribution must contain three masters")
    for row in action_rows:
        count = sum(int(value) for key, value in row.items() if key.startswith("adaptive_count_"))
        require(count == 320, f"master {row['master_index']} action counts do not sum to 320")
        require(row["global_fill_length"] == "16", "global action differs from 16")

    strata = read_tsv(PAPER / "tables/stratum-regret-decomposition.tsv")
    require(len(strata) == 40, "stratum table must have 40 rows")
    require(sum(int(row["profiles"]) for row in strata) == 960, "stratum profiles != 960")
    require(sum(int(row["regret_raw"]) for row in strata) == 10_380_000, "stratum regret mismatch")

    oat = read_tsv(PAPER / "tables/oat-raw-summary.tsv")
    require(len(oat) == 6 and oat[0]["condition"] == "core", "raw OAT table must contain core + five transforms")

    for path in [REPO / "research-log/lit/phase6-foundational.json", REPO / "research-log/lit/phase6-primary.json"]:
        data = json.loads(path.read_text(encoding="utf-8"))
        require(len(data["papers"]) == 5, f"unexpected literature count: {path}")
        require(all(p["reference_verification"]["status"] == "verified" for p in data["papers"]), f"unverified reference: {path}")
        require(sum(p["reference_verification"].get("critical_mismatches", 0) for p in data["papers"]) == 0, f"critical reference mismatch: {path}")

    references = SECTIONS[8].read_text(encoding="utf-8")
    cited_text = "\n".join(path.read_text(encoding="utf-8") for path in SECTIONS[:8])
    for number in range(1, 11):
        require(re.search(rf"^\[{number}\] ", references, flags=re.MULTILINE) is not None, f"reference [{number}] missing")
        require(f"[{number}]" in cited_text, f"reference [{number}] is uncited")

    supplement = SECTIONS[9].read_text(encoding="utf-8")
    marker = "experiment_id\tmetric\texpected\tdirection\tconfidence\tobserved\tsignal\truntime_sec\tpeak_memory_gb\tstatus\tnotes"
    require(marker in supplement, "embedded ledger header missing")
    start = supplement.index(marker)
    end = supplement.index("\n```", start)
    embedded = supplement[start:end] + "\n"
    require(embedded.encode() == (REPO / "results.tsv").read_bytes(), "embedded ledger differs from results.tsv")

    blueprint = (PAPER / "revision-round1-blueprint.md").read_text(encoding="utf-8")
    require(blueprint.count("| Issue |") == 1, "issue-routing table missing")
    require(all(f"| {issue} |" in blueprint for issue in range(1, 13)), "not all reviewer issues routed")
    matrix = (PAPER / "writing-rationale-matrix.md").read_text(encoding="utf-8")
    operations = re.findall(r"\| (REWRITE|ADD(?:/MOVE)?|MERGE|MOVE|KEEP(?:-AS-ARCHIVE)?) \|", matrix)
    require(operations.count("REWRITE") > operations.count("ADD"), "ADD dominates revision operations")
    require(operations.count("KEEP") == 0, "scientific KEEP operation present")

    matched, total, ratio = near_identical_ratio()
    require(total > 0, "no scientific prose paragraphs found")
    require(ratio < 0.35, f"near-identical paragraph ratio too high: {ratio:.3f}")

    print("revision_check=PASS")
    print(f"near_identical_paragraphs={matched}/{total} ratio={ratio:.6f} threshold=0.35")
    print("tables=PASS action_masters=3 profiles=960 strata=40 regret=10380000 oat_rows=6")
    print("references=PASS cited=10 field_verified=10 critical_mismatches=0")
    print("ledger=PASS byte_identical=true")


if __name__ == "__main__":
    main()
