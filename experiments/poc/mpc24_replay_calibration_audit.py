#!/usr/bin/env python3
"""Frozen read-only calibration audit for MPC-24 replay-cost accounting."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import time
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "experiments/configs/porf-c3-profile-v2.json"
COMPLETE = ROOT / "experiments/runs/porf-c3-profile-v2/COMPLETE.json"
SAMPLES = ROOT / "experiments/runs/porf-c3-profile-v2/samples.tsv"
SUMMARY = ROOT / "experiments/runs/porf-c3-profile-v2/summary.json"
RUN_LOG = ROOT / "experiments/runs/porf-c3-profile-v2/run.log"
RUNNER = ROOT / "experiments/porf_c3_profile_v2.py"

FREEZE_COMMIT = "121993c9b25c28d002803cd8f1a2c4af23bab158"
OUTPUT_COMMIT = "7bcd13b91eb8e28649067d20693cff3bcaae7c9b"
EXPECTED_SHA256 = {
    CONFIG: "6d15eb96013f94ae760faa9bfaa22dcdf15419df7bb1b68ec02ec6fc27add0c2",
    COMPLETE: "ea7a6d6d53cf7cf3453269e53ce14566943402aa5673022277ea8968f019a1b5",
    SAMPLES: "61395ac87dca4ace41993325372fd8dc7db6d960efcd502c04934095ed73276d",
    SUMMARY: "64c05a59d9006446a7eb35fcabef59368b63b7bc4ad06db252590bd085debf77",
    RUN_LOG: "98892f411275dc72379f504fb36fd9fae4ff6c7b678defcf452b5853d244f6c9",
    RUNNER: "30f6f847a81daed2665bc5c670aba00b48595e60d5c6472a3b8792c0553f987f",
}
DEPENDENCY_SHA256 = {
    "experiments/mock_agents.py": "dc7c66bb5385e862fd7778f6d0a6326795442a0ec2ddad97f0c0c8a40f1807df",
    "comp/sdk/aicomp_sdk/evaluation/ops.py": "455a835e0a58abab79b24c986a937b99712e69ef83d6068fc68873e3c051fe74",
    "comp/sdk/aicomp_sdk/guardrails/optimal.py": "6724fedf7bbf3e67dfcdd564ba8a73463e0f783d5c84e0a70dceff40c1bc61ed",
    "comp/sdk/aicomp_sdk/guardrails/base.py": "ec95f45a9bf4202514725690617c91e88f3f1ae889ac7828d423daafea527708",
    "comp/sdk/aicomp_sdk/core/env/api.py": "60f1e4424ec3dee73186f87ed1184d2ca1dbc4c2a0022004decec8b6e94c7cb1",
    "comp/sdk/aicomp_sdk/core/env/sandbox.py": "b781375c5aae3c2533f6992aae6d3c65ca56b7077822f1a27955756bef1168d0",
    "comp/sdk/aicomp_sdk/core/predicates.py": "9d9de5118d8883a0074a5405ed85cf2dec3f68e8516908cbc48f409e3ba56f37",
    "comp/sdk/aicomp_sdk/scoring.py": "13a0969ea6c64b257c46d47490b4259ade3a4965f19d2d6c6fe0ed151f618d4f",
    "comp/sdk/aicomp_sdk/core/cells.py": "2fc9cbe5b2488b3f3c472cb31787de2b6a50aa29dd1abf2a67366ffd2b9d7369",
}

CALIBRATION_REPLICATES = (0, 1, 2)
HOLDOUT_REPLICATES = (3, 4)
ARMS = (1, 8, 24)
GAMMA = 1.25
BOUNDARY_MARGIN = 1.25
ROUNDING_QUANTUM = 0.25
ACTIVATION_MARGIN = 1.10


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def committed_sha(commit: str, relative: str) -> str:
    data = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(data).hexdigest()


def capacity(budget: float, cost: float, cap: int) -> int:
    require(cost > 0.0, "cost must be positive")
    return min(cap, max(0, math.floor(max(0.0, budget) / cost)))


def load_rows() -> list[dict[str, Any]]:
    with SAMPLES.open(newline="") as handle:
        source = list(csv.DictReader(handle, delimiter="\t"))
    return [
        {
            "profile": row["profile"],
            "master": int(row["master"]),
            "replicate": int(row["replicate"]),
            "arm": int(row["arm"]),
            "phase": row["phase"],
            "cost_s": float(row["cost_s"]),
            "raw": float(row["raw"]),
            "fire_fraction": float(row["fire_fraction"]),
        }
        for row in source
    ]


def rounded_boundary_coefficient(value: float) -> float:
    expanded = BOUNDARY_MARGIN * max(0.0, value)
    return math.ceil(expanded / ROUNDING_QUANTUM) * ROUNDING_QUANTUM


def main() -> None:
    started = time.monotonic()
    for path, expected in EXPECTED_SHA256.items():
        require(sha256(path) == expected, f"artifact hash mismatch: {path.relative_to(ROOT)}")
    for relative, expected in DEPENDENCY_SHA256.items():
        require(sha256(ROOT / relative) == expected, f"dependency hash mismatch: {relative}")
        require(committed_sha(FREEZE_COMMIT, relative) == expected, f"freeze dependency mismatch: {relative}")
    require(committed_sha(FREEZE_COMMIT, "experiments/porf_c3_profile_v2.py") == EXPECTED_SHA256[RUNNER], "runner freeze mismatch")
    require(committed_sha(FREEZE_COMMIT, "experiments/configs/porf-c3-profile-v2.json") == EXPECTED_SHA256[CONFIG], "config freeze mismatch")
    require(committed_sha(OUTPUT_COMMIT, "experiments/runs/porf-c3-profile-v2/samples.tsv") == EXPECTED_SHA256[SAMPLES], "sample output mismatch")
    require(committed_sha(OUTPUT_COMMIT, "experiments/runs/porf-c3-profile-v2/summary.json") == EXPECTED_SHA256[SUMMARY], "summary output mismatch")

    config = json.loads(CONFIG.read_text())
    complete = json.loads(COMPLETE.read_text())
    summary = json.loads(SUMMARY.read_text())
    rows = load_rows()
    require(len(rows) == 360 and summary["sample_rows"] == 360, "row count mismatch")
    require(complete["bindings"]["experiments/porf_c3_profile_v2.py"] == EXPECTED_SHA256[RUNNER], "completion runner binding")
    require(complete["bindings"]["experiments/configs/porf-c3-profile-v2.json"] == EXPECTED_SHA256[CONFIG], "completion config binding")
    require(summary["environment"]["python"].startswith("3.14.3"), "Python environment changed")

    by_key = {
        (row["profile"], row["master"], row["replicate"], row["arm"], row["phase"]): row
        for row in rows
    }
    profiles = sorted(profile["id"] for profile in config["profiles"])
    masters = sorted(int(master) for master in config["masters"])

    scalar_violations_8_24 = 0
    scalar_pairs_8_24 = 0
    calibration_residuals: list[float] = []
    for profile in profiles:
        for master in masters:
            for replicate in range(int(config["replicates_per_arm_phase"])):
                g1 = by_key[(profile, master, replicate, 1, "generation")]["cost_s"]
                for arm in ARMS:
                    generation = by_key[(profile, master, replicate, arm, "generation")]["cost_s"]
                    replay = by_key[(profile, master, replicate, arm, "replay")]["cost_s"]
                    if arm in (8, 24):
                        scalar_pairs_8_24 += 1
                        scalar_violations_8_24 += int(replay > 1.10 * generation)
                    if replicate in CALIBRATION_REPLICATES:
                        calibration_residuals.append((replay - GAMMA * generation) / g1)

    require((scalar_violations_8_24, scalar_pairs_8_24) == (84, 90), "reviewer ratio count not reproduced")
    kappa = rounded_boundary_coefficient(max(calibration_residuals))

    def replay_proxy(profile: str, master: int, replicate: int, arm: int) -> float:
        g1 = by_key[(profile, master, replicate, 1, "generation")]["cost_s"]
        generation = by_key[(profile, master, replicate, arm, "generation")]["cost_s"]
        return GAMMA * generation + kappa * g1

    calibration_covered = 0
    calibration_total = 0
    holdout_covered = 0
    holdout_total = 0
    max_holdout_ratio = 0.0
    for profile in profiles:
        for master in masters:
            for replicate in range(int(config["replicates_per_arm_phase"])):
                for arm in ARMS:
                    replay = by_key[(profile, master, replicate, arm, "replay")]["cost_s"]
                    proxy = replay_proxy(profile, master, replicate, arm)
                    if replicate in CALIBRATION_REPLICATES:
                        calibration_total += 1
                        calibration_covered += int(replay <= proxy + 1e-12)
                    else:
                        holdout_total += 1
                        holdout_covered += int(replay <= proxy + 1e-12)
                        max_holdout_ratio = max(max_holdout_ratio, replay / proxy)

    generation_budget = float(config["generation_budget_s"])
    replay_budget = float(config["replay_budget_s"])
    candidate_cap = int(config["candidate_cap"])
    min_fire = float(config["min_fire_fraction"])
    selected24 = 0
    selected8 = 0
    cells_ge_fixed8 = 0
    cells_gt_fixed8 = 0
    controller_total = 0.0
    fixed8_total = 0.0

    for profile in profiles:
        for master in masters:
            sentinel_rep = 0
            sentinel_generation24 = by_key[(profile, master, sentinel_rep, 24, "generation")]["cost_s"]
            plugin: dict[int, float] = {}
            for arm in (8, 24):
                sentinel = by_key[(profile, master, sentinel_rep, arm, "generation")]
                proxy = replay_proxy(profile, master, sentinel_rep, arm)
                if sentinel["fire_fraction"] < min_fire:
                    continue
                fill = min(
                    candidate_cap - 1,
                    capacity(generation_budget - sentinel_generation24, sentinel["cost_s"], candidate_cap - 1),
                    capacity(replay_budget - proxy, proxy, candidate_cap - 1),
                )
                plugin[arm] = sentinel["raw"] * (1 + fill)
            require(8 in plugin, "retained sentinel lacks eligible arm 8")
            selected = 24 if 24 in plugin and plugin[24] >= ACTIVATION_MARGIN * plugin[8] else 8
            selected24 += int(selected == 24)
            selected8 += int(selected == 8)

            heldout = [
                by_key[(profile, master, replicate, selected, "generation")]
                for replicate in HOLDOUT_REPLICATES
            ]
            fill_generation = max(row["cost_s"] for row in heldout)
            fill_replay_proxy = max(
                replay_proxy(profile, master, replicate, selected)
                for replicate in HOLDOUT_REPLICATES
            )
            fill_raw = min(row["raw"] for row in heldout)
            sentinel_raw = by_key[(profile, master, sentinel_rep, selected, "generation")]["raw"]
            sentinel_replay_proxy = replay_proxy(profile, master, sentinel_rep, selected)
            fill_count = min(
                candidate_cap - 1,
                capacity(generation_budget - sentinel_generation24, fill_generation, candidate_cap - 1),
                capacity(replay_budget - sentinel_replay_proxy, fill_replay_proxy, candidate_cap - 1),
            )
            controller = sentinel_raw + fill_raw * fill_count

            fixed8_first = by_key[(profile, master, sentinel_rep, 8, "generation")]
            fixed8_generation = max(
                by_key[(profile, master, replicate, 8, "generation")]["cost_s"]
                for replicate in HOLDOUT_REPLICATES
            )
            fixed8_replay_proxy = max(
                replay_proxy(profile, master, replicate, 8)
                for replicate in HOLDOUT_REPLICATES
            )
            fixed8_raw = min(
                by_key[(profile, master, replicate, 8, "generation")]["raw"]
                for replicate in HOLDOUT_REPLICATES
            )
            fixed8_first_proxy = replay_proxy(profile, master, sentinel_rep, 8)
            fixed8_fill = min(
                candidate_cap - 1,
                capacity(generation_budget - fixed8_first["cost_s"], fixed8_generation, candidate_cap - 1),
                capacity(replay_budget - fixed8_first_proxy, fixed8_replay_proxy, candidate_cap - 1),
            )
            fixed8 = fixed8_first["raw"] + fixed8_raw * fixed8_fill

            controller_total += controller
            fixed8_total += fixed8
            cells_ge_fixed8 += int(controller >= fixed8)
            cells_gt_fixed8 += int(controller > fixed8)

    ratio = controller_total / fixed8_total
    elapsed = time.monotonic() - started
    print("mpc24_replay_calibration_audit=PASS")
    print(f"freeze_commit={FREEZE_COMMIT}")
    print(f"output_commit={OUTPUT_COMMIT}")
    print(f"provenance_dependencies={len(DEPENDENCY_SHA256)}")
    print(f"artifact_rows={len(rows)}")
    print(f"scalar_1_10_violations_8_24={scalar_violations_8_24}/{scalar_pairs_8_24}")
    print(f"calibration_pairs={calibration_total}")
    print(f"holdout_pairs={holdout_total}")
    print(f"gamma={GAMMA:.6f}")
    print(f"kappa={kappa:.6f}")
    print(f"calibration_envelope_coverage={calibration_covered}/{calibration_total}")
    print(f"holdout_envelope_coverage={holdout_covered}/{holdout_total}")
    print(f"max_holdout_actual_to_proxy={max_holdout_ratio:.12f}")
    print(f"proxy_controller_select24={selected24}/9")
    print(f"proxy_controller_select8={selected8}/9")
    print(f"proxy_controller_ge_fixed8={cells_ge_fixed8}/9")
    print(f"proxy_controller_gt_fixed8={cells_gt_fixed8}/9")
    print(f"proxy_controller_to_fixed8_ratio={ratio:.12f}")
    print("prefix8_timing_scope=independent_proxy_not_nested_measurement")
    print("official_target_inference=none")
    print(f"runtime_s={elapsed:.9f}")


if __name__ == "__main__":
    main()
