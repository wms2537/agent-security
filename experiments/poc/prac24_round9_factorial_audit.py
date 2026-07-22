#!/usr/bin/env python3
"""Read-only round-9 Occam/factorial audit over the sealed HCMS-24 trace.

This script asks which PRAC components have a same-trace counterfactual in the
already-sealed Phase-3 artifact.  It is retrospective mechanism-selection
evidence only: it never executes the scientific runner and cannot create new
held-out evidence.
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
CONFIG = ROOT / "experiments/configs/hcms24-c3-v1.json"
ATTACK = ROOT / "experiments/attack.py"
EXPECTED_COMPLETE_SHA256 = "34e9dc0274e0828f325cb280b2f392a6e867fabf4315c0c962cf3746dc200b07"
EXPECTED_CONFIG_SHA256 = "e71c8a6afb70459077a303652e21063a9c71f60d0650a502de8f63fbfb3c0e59"
EXPECTED_ATTACK_SHA256 = "8ab8d0528dc02ec4c269e6a49aac5979354e19efcf344e36bb3f6a7443e9d78d"
CELL_KEY = (
    "namespace",
    "profile",
    "master",
    "order_index",
    "position",
    "method",
)
BLOCK_KEY = ("namespace", "profile", "master", "order_index")
PRIMARY_METHODS = {
    "hcms_calibrated",
    "fixed8_calibrated",
    "fixed24_no_salvage_calibrated",
    "hcms_scalar",
}


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


def cell_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row[field] for field in CELL_KEY)


def block_key(row: dict[str, str]) -> tuple[str, ...]:
    return tuple(row[field] for field in BLOCK_KEY)


def grouped(
    rows: Iterable[dict[str, str]],
) -> dict[tuple[str, ...], list[dict[str, str]]]:
    result: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        result[cell_key(row)].append(row)
    return result


def verify_seal() -> dict[str, Any]:
    complete_path = ATTEMPT / "COMPLETE.json"
    require(sha256(complete_path) == EXPECTED_COMPLETE_SHA256, "COMPLETE identity drift")
    require(sha256(CONFIG) == EXPECTED_CONFIG_SHA256, "config identity drift")
    require(sha256(ATTACK) == EXPECTED_ATTACK_SHA256, "attack identity drift")
    complete = json.loads(complete_path.read_text(encoding="utf-8"))
    require(complete["status"] == "invalid", "sealed status was rewritten")
    expected_names = set(complete["artifacts"])
    observed_names = {path.name for path in ATTEMPT.iterdir()} - {"COMPLETE.json"}
    require(observed_names == expected_names, "attempt artifact-set drift")
    for name, expected_hash in complete["artifacts"].items():
        require(sha256(ATTEMPT / name) == expected_hash, f"artifact hash drift: {name}")
    return complete


def main() -> None:
    complete = verify_seal()
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    paths = read_tsv("paths.tsv")
    candidates = read_tsv("candidates.tsv")
    cells = read_tsv("method_cells.tsv")

    primary_cells = [row for row in cells if row["namespace"] == "primary"]
    require(len(primary_cells) == 144, "primary grid drift")
    require({row["method"] for row in primary_cells} == PRIMARY_METHODS, "method drift")

    path_groups = grouped(paths)
    candidate_groups = grouped(candidates)
    first_no_fit: dict[tuple[str, ...], tuple[int, dict[str, str]]] = {}
    for key, rows in path_groups.items():
        rows.sort(key=lambda row: int(row["path_index"]))
        for offset, row in enumerate(rows):
            if row["outcome"] == "drop_ledger_no_fit":
                first_no_fit[key] = (offset, row)
                break

    primary_no_fit = {key: value for key, value in first_no_fit.items() if key[0] == "primary"}
    require(len(first_no_fit) == 97 and len(primary_no_fit) == 96, "no-fit scope drift")

    primary_tail: list[dict[str, str]] = []
    hcms_tail: list[dict[str, str]] = []
    for key, (offset, _row) in primary_no_fit.items():
        tail = path_groups[key][offset + 1 :]
        primary_tail.extend(tail)
        if key[-1] == "hcms_calibrated":
            hcms_tail.extend(tail)
    require(len(primary_tail) == 415, "primary post-no-fit tail drift")

    removed_primary_candidates = [
        row
        for key, rows in candidate_groups.items()
        if key in primary_no_fit
        for row in rows
        if int(row["path_index"]) > int(primary_no_fit[key][1]["path_index"])
    ]
    removed_raw_by_method: dict[str, float] = defaultdict(float)
    for row in removed_primary_candidates:
        removed_raw_by_method[row["method"]] += float(row["actual_raw"])

    original_raw: dict[str, float] = defaultdict(float)
    for row in candidates:
        if row["namespace"] == "primary":
            original_raw[row["method"]] += float(row["actual_raw"])
    absorbing_raw = {
        method: original_raw[method] - removed_raw_by_method[method]
        for method in PRIMARY_METHODS
    }
    require(absorbing_raw["hcms_calibrated"] == 39240.0, "absorbing HCMS raw drift")
    require(absorbing_raw["fixed8_calibrated"] == 28170.0, "absorbing fixed8 raw drift")
    require(
        absorbing_raw["fixed24_no_salvage_calibrated"] == 23160.0,
        "absorbing fixed24 raw drift",
    )
    absorbing_ratio = absorbing_raw["hcms_calibrated"] / max(
        absorbing_raw["fixed8_calibrated"],
        absorbing_raw["fixed24_no_salvage_calibrated"],
    )

    original_generation_overages = {
        cell_key(row) for row in primary_cells if row["generation_overage"] == "True"
    }
    require(len(original_generation_overages) == 4, "generation-overage drift")
    require(original_generation_overages <= set(primary_no_fit), "overage before first no-fit")
    counterfactual_terminal_s = {
        key: float(primary_no_fit[key][1]["generation_elapsed_s"])
        for key in original_generation_overages
    }
    require(max(counterfactual_terminal_s.values()) < 2.0, "absorption does not remove overage")

    hcms_cells = [row for row in primary_cells if row["method"] == "hcms_calibrated"]
    hcms_replay_overages = sum(row["actual_replay_overage"] == "True" for row in hcms_cells)
    require(hcms_replay_overages == 0, "HCMS replay endpoint drift")
    original_hcms_generation_s = sum(float(row["generation_elapsed_s"]) for row in hcms_cells)
    hcms_tail_s = sum(float(row["path_cost_s"]) for row in hcms_tail)
    absorbing_hcms_generation_upper_s = original_hcms_generation_s - hcms_tail_s
    require(absorbing_hcms_generation_upper_s > 0.0, "invalid absorbing time projection")
    hcms_raw_retention = absorbing_raw["hcms_calibrated"] / original_raw["hcms_calibrated"]
    original_hcms_raw_per_s = original_raw["hcms_calibrated"] / original_hcms_generation_s
    absorbing_hcms_raw_per_s_lower = (
        absorbing_raw["hcms_calibrated"] / absorbing_hcms_generation_upper_s
    )
    efficiency_ratio_lower = absorbing_hcms_raw_per_s_lower / original_hcms_raw_per_s

    # Absorption is a same-trace truncation: all post-trigger paths and their
    # outcomes were observed in the sealed run.  The other factors are not.
    absorption_estimable_cells = len(primary_no_fit)

    block_methods: dict[tuple[str, ...], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in primary_cells:
        block_methods[block_key(row)][row["method"]] = row
    require(len(block_methods) == 36, "block count drift")
    replay_paired_blocks = 0
    replay_same_capture_cells = 0
    for methods in block_methods.values():
        calibrated = methods["hcms_calibrated"]
        scalar = methods["hcms_scalar"]
        replay_paired_blocks += 1
        # Separate Williams positions/predecessors are separate live captures,
        # not two projections of one stored potential trace.
        if (
            calibrated["position"] == scalar["position"]
            and calibrated["predecessor"] == scalar["predecessor"]
        ):
            replay_same_capture_cells += 1
    require(replay_paired_blocks == 36 and replay_same_capture_cells == 0, "capture audit drift")

    dropped_without_replay = 0
    candidate_path_keys = {
        (cell_key(row), int(row["path_index"])) for row in candidates
    }
    for row in paths:
        if row["namespace"] != "primary" or row["outcome"] != "drop_ledger_no_fit":
            continue
        if (cell_key(row), int(row["path_index"])) not in candidate_path_keys:
            dropped_without_replay += 1
    require(dropped_without_replay > 0, "unexpected complete replay potential outcomes")

    primary_zero_paths = [
        row
        for row in paths
        if row["namespace"] == "primary" and row["completed_interactions"] == "0"
    ]
    zero_gt_reserve = sum(float(row["path_cost_s"]) > 0.1 for row in primary_zero_paths)
    require((zero_gt_reserve, len(primary_zero_paths)) == (44, 84), "atomic-tail drift")

    methods = config["methods"]
    calibrated_policy = {k: v for k, v in methods["hcms_calibrated"].items() if k != "ledger"}
    scalar_policy = {k: v for k, v in methods["hcms_scalar"].items() if k != "ledger"}
    require(calibrated_policy == scalar_policy, "non-ledger policy mismatch")

    print("prac24_round9_factorial_audit=PASS")
    print(f"complete_artifacts={len(complete['artifacts'])}")
    print("scientific_runner_executed=false")
    print("factorial_factors=replay_envelope,absorbing_no_fit,atomic_gate")
    print("full_two_cubed_factorial_estimable_cells=0")
    print("absorption_same_trace_estimable=true")
    print(f"absorption_estimable_primary_cells={absorption_estimable_cells}")
    print(f"primary_post_no_fit_paths={len(primary_tail)}")
    print(f"primary_post_no_fit_seconds={sum(float(row['path_cost_s']) for row in primary_tail):.12f}")
    print(f"hcms_post_no_fit_paths={len(hcms_tail)}")
    print(f"hcms_post_no_fit_seconds={sum(float(row['path_cost_s']) for row in hcms_tail):.12f}")
    print(f"primary_later_recovery_candidates={len(removed_primary_candidates)}")
    print(f"primary_later_recovery_raw={sum(removed_raw_by_method.values()):.1f}")
    print(f"hcms_absorption_raw_loss={removed_raw_by_method['hcms_calibrated']:.1f}")
    print(f"absorbing_hcms_raw={absorbing_raw['hcms_calibrated']:.1f}")
    print(f"hcms_raw_retention={hcms_raw_retention:.12f}")
    print(f"original_hcms_generation_s={original_hcms_generation_s:.12f}")
    print(f"absorbing_hcms_generation_upper_s={absorbing_hcms_generation_upper_s:.12f}")
    print(f"original_hcms_raw_per_s={original_hcms_raw_per_s:.12f}")
    print(f"absorbing_hcms_raw_per_s_lower={absorbing_hcms_raw_per_s_lower:.12f}")
    print(f"absorbing_efficiency_ratio_lower={efficiency_ratio_lower:.12f}")
    print(f"absorbing_hcms_to_best_simple_ratio={absorbing_ratio:.12f}")
    print(f"generation_overages_without_absorption={len(original_generation_overages)}/144")
    print("generation_overages_with_absorption=0/144")
    print(f"hcms_aggregate_replay_overages={hcms_replay_overages}/36")
    print(f"replay_removal_block_pairs={replay_paired_blocks}")
    print(f"replay_removal_same_capture_pairs={replay_same_capture_cells}")
    print(f"dropped_paths_without_replay_outcome={dropped_without_replay}")
    print("replay_envelope_same_trace_estimable=false")
    print(f"zero_interaction_paths_gt_point_one={zero_gt_reserve}/{len(primary_zero_paths)}")
    print("atomic_gate_same_trace_estimable=false")
    print("round9_occam_decision=claim_absorbing_no_fit_only")
    print("replay_envelope_status=unclaimed_prospective_guardrail")
    print("atomic_gate_status=unclaimed_prospective_guardrail")
    print("inference=retrospective_mechanism_selection_only")


if __name__ == "__main__":
    main()
