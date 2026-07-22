#!/usr/bin/env python3
"""Read-only audit selecting the evidence-grounded 24->8 prefix frontier."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "experiments/configs/porf-c3-profile-v2.json"
COMPLETE = ROOT / "experiments/runs/porf-c3-profile-v2/COMPLETE.json"
SAMPLES = ROOT / "experiments/runs/porf-c3-profile-v2/samples.tsv"
SUMMARY = ROOT / "experiments/runs/porf-c3-profile-v2/summary.json"

EXPECTED_SHA256 = {
    CONFIG: "6d15eb96013f94ae760faa9bfaa22dcdf15419df7bb1b68ec02ec6fc27add0c2",
    COMPLETE: "ea7a6d6d53cf7cf3453269e53ce14566943402aa5673022277ea8968f019a1b5",
    SAMPLES: "61395ac87dca4ace41993325372fd8dc7db6d960efcd502c04934095ed73276d",
    SUMMARY: "64c05a59d9006446a7eb35fcabef59368b63b7bc4ad06db252590bd085debf77",
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


def load_rows() -> list[dict[str, Any]]:
    with SAMPLES.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    typed: list[dict[str, Any]] = []
    for row in rows:
        typed.append(
            {
                "profile": row["profile"],
                "master": int(row["master"]),
                "replicate": int(row["replicate"]),
                "arm": int(row["arm"]),
                "phase": row["phase"],
                "cost_s": float(row["cost_s"]),
                "events": int(row["events"]),
                "raw": float(row["raw"]),
                "fire_fraction": float(row["fire_fraction"]),
            }
        )
    return typed


def capacity(budget: float, cost: float, cap: int) -> int:
    require(budget >= 0.0, "negative budget")
    require(cost > 0.0, "nonpositive cost")
    return min(cap, math.floor(budget / cost))


def main() -> None:
    for path, expected in EXPECTED_SHA256.items():
        require(sha256(path) == expected, f"hash mismatch: {path.relative_to(ROOT)}")

    config = json.loads(CONFIG.read_text())
    complete = json.loads(COMPLETE.read_text())
    summary = json.loads(SUMMARY.read_text())
    rows = load_rows()

    require(complete["status"] == "FAIL", "negative prediction must remain retained")
    require(complete["artifacts"]["samples.tsv"] == EXPECTED_SHA256[SAMPLES], "bundle sample hash")
    require(complete["artifacts"]["summary.json"] == EXPECTED_SHA256[SUMMARY], "bundle summary hash")
    require(len(rows) == 360, "wrong sample-row count")
    require(summary["sample_rows"] == 360, "summary row count")
    require(config["arms"] == [1, 4, 8, 24], "unexpected arms")
    require(config["replicates_per_arm_phase"] == 5, "unexpected replicates")

    expected_keys = {
        (profile["id"], master, replicate, arm, phase)
        for profile in config["profiles"]
        for master in config["masters"]
        for replicate in range(config["replicates_per_arm_phase"])
        for arm in config["arms"]
        for phase in ("generation", "replay")
    }
    observed_keys = {
        (row["profile"], row["master"], row["replicate"], row["arm"], row["phase"])
        for row in rows
    }
    require(observed_keys == expected_keys, "sample factorial mismatch")

    fixed8_within_short = 0
    best24 = 0
    best8 = 0
    for decision in summary["sdk_decisions"]:
        table = {int(arm): values for arm, values in decision["table"].items()}
        short_best = min((1, 4, 8), key=lambda arm: (-table[arm]["total_raw"], arm))
        require(short_best == 8, f"short-arm winner drift: {decision['profile']}/{decision['master']}")
        fixed8_within_short += 1
        if int(decision["selected"]) == 24:
            best24 += 1
        elif int(decision["selected"]) == 8:
            best8 += 1
        else:
            raise AssertionError("unexpected full-frontier winner")

    by_cell: dict[tuple[str, int, int, int], dict[str, dict[str, float]]] = defaultdict(dict)
    for row in rows:
        by_cell[(row["profile"], row["master"], row["replicate"], row["arm"])][row["phase"]] = row

    generation_budget = float(config["generation_budget_s"])
    replay_budget = float(config["replay_budget_s"])
    candidate_cap = int(config["candidate_cap"])
    margin = 1.10
    selected24 = 0
    selected8 = 0
    cells_ge_fixed8 = 0
    cells_gt_fixed8 = 0
    controller_total = 0.0
    fixed8_total = 0.0

    for profile in sorted(item["id"] for item in config["profiles"]):
        for master in sorted(config["masters"]):
            sentinel24 = by_cell[(profile, master, 0, 24)]
            full_generation_spent = sentinel24["generation"]["cost_s"]
            plugin: dict[int, float] = {}
            for arm in (8, 24):
                sentinel = by_cell[(profile, master, 0, arm)]
                generation_cost = sentinel["generation"]["cost_s"]
                replay_cost = sentinel["replay"]["cost_s"]
                raw = sentinel["generation"]["raw"]
                fill = min(
                    candidate_cap - 1,
                    capacity(generation_budget - full_generation_spent, generation_cost, candidate_cap - 1),
                    capacity(replay_budget - replay_cost, replay_cost, candidate_cap - 1),
                )
                plugin[arm] = raw * (1 + fill)

            choose24 = (
                sentinel24["generation"]["fire_fraction"] >= config["min_fire_fraction"]
                and plugin[24] >= margin * plugin[8]
            )
            selected = 24 if choose24 else 8
            selected24 += int(selected == 24)
            selected8 += int(selected == 8)

            def heldout_portfolio(arm: int, first_generation_spent: float) -> float:
                sentinel = by_cell[(profile, master, 0, arm)]
                heldout = [by_cell[(profile, master, replicate, arm)] for replicate in range(1, 5)]
                generation_cost = max(item["generation"]["cost_s"] for item in heldout)
                replay_cost = max(item["replay"]["cost_s"] for item in heldout)
                fill_raw = min(item["generation"]["raw"] for item in heldout)
                fill = min(
                    candidate_cap - 1,
                    capacity(generation_budget - first_generation_spent, generation_cost, candidate_cap - 1),
                    capacity(replay_budget - sentinel["replay"]["cost_s"], replay_cost, candidate_cap - 1),
                )
                return sentinel["generation"]["raw"] + fill_raw * fill

            controller = heldout_portfolio(selected, full_generation_spent)
            fixed8 = heldout_portfolio(8, by_cell[(profile, master, 0, 8)]["generation"]["cost_s"])
            controller_total += controller
            fixed8_total += fixed8
            cells_ge_fixed8 += int(controller >= fixed8)
            cells_gt_fixed8 += int(controller > fixed8)

    require((fixed8_within_short, best24, best8) == (9, 6, 3), "winner counts changed")
    require((selected24, selected8) == (6, 3), "sentinel choices changed")
    require(cells_ge_fixed8 == 9 and cells_gt_fixed8 == 6, "heldout comparison changed")
    ratio = controller_total / fixed8_total
    require(math.isclose(ratio, 1.5073767258382642), "aggregate ratio changed")

    print("mpc24_evidence_audit=PASS")
    print(f"artifact_rows={len(rows)}")
    print(f"fixed8_best_within_1_4_8={fixed8_within_short}/9")
    print(f"full_frontier_best24={best24}/9")
    print(f"full_frontier_best8={best8}/9")
    print(f"replicate0_sentinel_select24={selected24}/9")
    print(f"replicate0_sentinel_select8={selected8}/9")
    print(f"heldout_controller_ge_fixed8={cells_ge_fixed8}/9")
    print(f"heldout_controller_gt_fixed8={cells_gt_fixed8}/9")
    print(f"heldout_aggregate_ratio={ratio:.12f}")
    print("prefix8_timing_scope=independent_proxy_not_nested_measurement")
    print("official_target_inference=none")


if __name__ == "__main__":
    main()
