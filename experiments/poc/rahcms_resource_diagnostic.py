#!/usr/bin/env python3
"""Read-only diagnosis of the sealed HCMS-24 resource-risk failure.

This script is deliberately retrospective.  It verifies and summarizes the
already-sealed attempt; it does not turn the absorbing-stop counterfactual into
confirmatory evidence and it never executes the scientific runner.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
ATTEMPT = ROOT / "experiments/runs/hcms24-c3-poc-v1"
EXPECTED_COMPLETE_SHA256 = "34e9dc0274e0828f325cb280b2f392a6e867fabf4315c0c962cf3746dc200b07"
CALIBRATED = {
    "hcms_calibrated",
    "fixed8_calibrated",
    "fixed24_no_salvage_calibrated",
}
CELL_KEY = (
    "namespace",
    "profile",
    "master",
    "order_index",
    "position",
    "method",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    path = ATTEMPT / name
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular {name}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
    require(reader.fieldnames is not None, f"missing header: {name}")
    require(all(None not in row for row in rows), f"row-width drift: {name}")
    return rows


def key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row[field] for field in CELL_KEY)


def grouped(rows: Iterable[dict[str, str]]) -> dict[tuple[str, ...], list[dict[str, str]]]:
    result: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        result[key(row)].append(row)
    return result


def verify_manifest() -> dict[str, Any]:
    complete_path = ATTEMPT / "COMPLETE.json"
    require(sha256(complete_path) == EXPECTED_COMPLETE_SHA256, "COMPLETE identity drift")
    complete = json.loads(complete_path.read_text(encoding="utf-8"))
    require(complete["status"] == "invalid", "sealed status was rewritten")
    expected_names = set(complete["artifacts"])
    observed_names = {path.name for path in ATTEMPT.iterdir()} - {"COMPLETE.json"}
    require(observed_names == expected_names, "attempt artifact-set drift")
    for name, expected in complete["artifacts"].items():
        require(sha256(ATTEMPT / name) == expected, f"artifact hash drift: {name}")
    require(
        complete_path.stat().st_mtime_ns
        >= max((ATTEMPT / name).stat().st_mtime_ns for name in expected_names),
        "COMPLETE is not last",
    )
    return complete


def main() -> None:
    complete = verify_manifest()
    candidates = read_tsv("candidates.tsv")
    paths = read_tsv("paths.tsv")
    cells = read_tsv("method_cells.tsv")

    primary_cells = [row for row in cells if row["namespace"] == "primary"]
    hcms_cells = [row for row in primary_cells if row["method"] == "hcms_calibrated"]
    scalar_cells = [row for row in primary_cells if row["method"] == "hcms_scalar"]
    primary_candidates = [row for row in candidates if row["namespace"] == "primary"]
    calibrated_candidates = [
        row for row in primary_candidates if row["method"] in CALIBRATED
    ]
    hcms_candidates = [
        row for row in primary_candidates if row["method"] == "hcms_calibrated"
    ]

    require(len(primary_cells) == 144 and len(hcms_cells) == 36, "primary grid drift")
    require(len(calibrated_candidates) == 472, "calibrated candidate count drift")
    require(len(hcms_candidates) == 189, "HCMS candidate count drift")
    calibrated_covered = sum(row["replay_covered"] == "True" for row in calibrated_candidates)
    hcms_covered = sum(row["replay_covered"] == "True" for row in hcms_candidates)
    hcms_overages = sum(row["actual_replay_overage"] == "True" for row in hcms_cells)
    scalar_overages = sum(row["actual_replay_overage"] == "True" for row in scalar_cells)
    generation_overages = sum(row["generation_overage"] == "True" for row in primary_cells)
    require((calibrated_covered, hcms_covered) == (470, 187), "coverage diagnosis drift")
    require((hcms_overages, scalar_overages, generation_overages) == (0, 19, 4), "overage diagnosis drift")

    candidate_groups = grouped(row for row in candidates if row["method"] == "hcms_calibrated")
    primary_prefix_max: list[float] = []
    primary_total_ratio: list[float] = []
    safety_prefix_max: list[float] = []
    safety_total_ratio: list[float] = []
    for cell_key, rows in candidate_groups.items():
        rows.sort(key=lambda row: int(row["candidate_index"]))
        cumulative_actual = 0.0
        cumulative_charge = 0.0
        prefix_max = 0.0
        for row in rows:
            cumulative_actual += float(row["actual_replay_s"])
            cumulative_charge += float(row["ledger_charge_s"])
            require(cumulative_charge > 0.0, "nonpositive replay charge")
            prefix_max = max(prefix_max, cumulative_actual / cumulative_charge)
        target_prefix = primary_prefix_max if cell_key[0] == "primary" else safety_prefix_max
        target_total = primary_total_ratio if cell_key[0] == "primary" else safety_total_ratio
        target_prefix.append(prefix_max)
        target_total.append(cumulative_actual / cumulative_charge)
    require(len(primary_prefix_max) == 36 and len(safety_prefix_max) == 1, "HCMS scope drift")

    path_groups = grouped(paths)
    first_no_fit: dict[tuple[str, ...], tuple[int, dict[str, str]]] = {}
    for cell_key, rows in path_groups.items():
        rows.sort(key=lambda row: int(row["path_index"]))
        for index, row in enumerate(rows):
            if row["outcome"] == "drop_ledger_no_fit":
                first_no_fit[cell_key] = (index, row)
                break
    require(len(first_no_fit) == 97, "first-no-fit cell count drift")

    tail_paths: list[dict[str, str]] = []
    primary_tail_paths: list[dict[str, str]] = []
    for cell_key, (index, _row) in first_no_fit.items():
        tail = path_groups[cell_key][index + 1 :]
        tail_paths.extend(tail)
        if cell_key[0] == "primary":
            primary_tail_paths.extend(tail)
    require(len(tail_paths) == 420 and len(primary_tail_paths) == 415, "post-no-fit tail drift")

    removed_candidates = [
        row
        for row in candidates
        if key(row) in first_no_fit
        and int(row["path_index"]) > int(first_no_fit[key(row)][1]["path_index"])
    ]
    require(len(removed_candidates) == 3, "recovered candidate count drift")
    removed_raw = sum(float(row["actual_raw"]) for row in removed_candidates)
    require(removed_raw == 54.0, "recovered raw drift")

    original_raw: dict[str, float] = defaultdict(float)
    removed_raw_by_method: dict[str, float] = defaultdict(float)
    for row in primary_candidates:
        original_raw[row["method"]] += float(row["actual_raw"])
    for row in removed_candidates:
        if row["namespace"] == "primary":
            removed_raw_by_method[row["method"]] += float(row["actual_raw"])
    absorbing_raw = {
        method: value - removed_raw_by_method[method]
        for method, value in original_raw.items()
    }
    require(absorbing_raw["hcms_calibrated"] == 39240.0, "absorbing HCMS raw drift")
    require(absorbing_raw["fixed8_calibrated"] == 28170.0, "absorbing fixed8 raw drift")
    require(absorbing_raw["fixed24_no_salvage_calibrated"] == 23160.0, "fixed24 raw drift")
    absorbing_ratio = absorbing_raw["hcms_calibrated"] / max(
        absorbing_raw["fixed8_calibrated"],
        absorbing_raw["fixed24_no_salvage_calibrated"],
    )

    overage_keys = {key(row) for row in primary_cells if row["generation_overage"] == "True"}
    require(overage_keys <= set(first_no_fit), "overage before first no-fit")
    require(
        all(int(first_no_fit[cell_key][1]["path_index"]) < len(path_groups[cell_key]) for cell_key in overage_keys),
        "overage not in post-no-fit tail",
    )
    first_no_fit_max_elapsed = max(
        float(row["generation_elapsed_s"])
        for cell_key, (_index, row) in first_no_fit.items()
        if cell_key[0] == "primary"
    )
    require(first_no_fit_max_elapsed < 2.0, "first no-fit already exceeded budget")

    primary_zero_paths = [
        row for row in paths if row["namespace"] == "primary" and row["completed_interactions"] == "0"
    ]
    zero_gt_reserve = sum(float(row["path_cost_s"]) > 0.1 for row in primary_zero_paths)

    print("rahcms_resource_diagnostic=PASS")
    print(f"complete_artifacts={len(complete['artifacts'])}")
    print(f"primary_cells={len(primary_cells)}")
    print(f"calibrated_candidate_coverage={calibrated_covered}/{len(calibrated_candidates)}")
    print(f"hcms_candidate_coverage={hcms_covered}/{len(hcms_candidates)}")
    print(f"hcms_aggregate_replay_overage_cells={hcms_overages}/36")
    print(f"scalar_aggregate_replay_overage_cells={scalar_overages}/36")
    print(f"primary_generation_overage_cells={generation_overages}/144")
    print(f"primary_hcms_prefix_cumulative_ratio_max={max(primary_prefix_max):.12f}")
    print(f"primary_hcms_cell_total_ratio_max={max(primary_total_ratio):.12f}")
    print(f"safety_hcms_prefix_cumulative_ratio_max={max(safety_prefix_max):.12f}")
    print(f"safety_hcms_cell_total_ratio={max(safety_total_ratio):.12f}")
    print(f"first_ledger_no_fit_cells={len(first_no_fit)}")
    print(f"post_first_no_fit_paths={len(tail_paths)}")
    print(f"post_first_no_fit_seconds={sum(float(row['path_cost_s']) for row in tail_paths):.12f}")
    print(f"primary_post_first_no_fit_paths={len(primary_tail_paths)}")
    print(f"primary_post_first_no_fit_seconds={sum(float(row['path_cost_s']) for row in primary_tail_paths):.12f}")
    print(f"later_recovery_candidates={len(removed_candidates)}")
    print(f"later_recovery_raw={removed_raw:.1f}")
    print(f"absorbing_hcms_raw={absorbing_raw['hcms_calibrated']:.1f}")
    print(f"absorbing_fixed8_raw={absorbing_raw['fixed8_calibrated']:.1f}")
    print(f"absorbing_fixed24_raw={absorbing_raw['fixed24_no_salvage_calibrated']:.1f}")
    print(f"absorbing_hcms_to_best_simple_ratio={absorbing_ratio:.12f}")
    print(f"first_no_fit_max_generation_elapsed_s={first_no_fit_max_elapsed:.12f}")
    print(f"primary_zero_interaction_paths_gt_point_one={zero_gt_reserve}/{len(primary_zero_paths)}")
    print("inference=retrospective_diagnosis_only")


if __name__ == "__main__":
    main()
