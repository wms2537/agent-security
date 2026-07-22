#!/usr/bin/env python3
"""Frozen read-only Occam audit for MPC-24 versus symmetric salvage controls.

This is an exploratory re-analysis of the retained PORF profile artifact.  It is
not the nested Phase-3 run: prefix measurements come from independent arms.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


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

STATES = (24, 8, 1)
HOLDOUT_REPLICATES = (3, 4)
GAMMA = 1.25
KAPPA = 6.25
ACTIVATION_MARGIN = 1.10
SCALAR = 1.10
STATIC_MAX_PERIOD = 6


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


@dataclass(frozen=True)
class Candidate:
    requested: int
    returned: int
    generation_cost: float
    ledger_replay_cost: float
    actual_replay_cost: float
    raw: float


@dataclass(frozen=True)
class Portfolio:
    raw: float
    candidates: int
    generation_cost: float
    ledger_replay_cost: float
    actual_replay_cost: float
    first_returned: int
    final_state: int


def primitive_period(pattern: tuple[int, ...]) -> tuple[int, ...]:
    for size in range(1, len(pattern) + 1):
        if len(pattern) % size == 0 and pattern == pattern[:size] * (len(pattern) // size):
            return pattern[:size]
    raise AssertionError("unreachable primitive-period branch")


def main() -> None:
    started = time.monotonic()
    for path, expected in EXPECTED_SHA256.items():
        require(sha256(path) == expected, f"artifact hash mismatch: {path.relative_to(ROOT)}")

    config = json.loads(CONFIG.read_text())
    complete = json.loads(COMPLETE.read_text())
    summary = json.loads(SUMMARY.read_text())
    rows = load_rows()
    require(complete["status"] == "FAIL", "antecedent failure disclosure changed")
    require(summary["status"] == "FAIL", "summary failure disclosure changed")
    require(summary["sdk_decisions_passed"] == 6, "antecedent decision count changed")
    require(len(rows) == 360, "sample row count changed")
    require(config["arms"] == [1, 4, 8, 24], "arm grid changed")

    by_key = {
        (row["profile"], row["master"], row["replicate"], row["arm"], row["phase"]): row
        for row in rows
    }
    profiles = sorted(profile["id"] for profile in config["profiles"])
    masters = sorted(int(master) for master in config["masters"])
    cells = [(profile, master) for profile in profiles for master in masters]
    generation_budget = float(config["generation_budget_s"])
    replay_budget = float(config["replay_budget_s"])
    candidate_cap = int(config["candidate_cap"])
    minimum_coverage = float(config["min_fire_fraction"])

    def source(profile: str, master: int, replicate: int, arm: int, phase: str) -> dict[str, Any]:
        return by_key[(profile, master, replicate, arm, phase)]

    def replay_cost(profile: str, master: int, replicate: int, arm: int, ledger: str) -> float:
        generation = source(profile, master, replicate, arm, "generation")["cost_s"]
        if ledger == "calibrated":
            first = source(profile, master, replicate, 1, "generation")["cost_s"]
            return GAMMA * generation + KAPPA * first
        require(ledger == "scalar", "unknown replay ledger")
        return SCALAR * generation

    def eligible(profile: str, master: int, replicates: tuple[int, ...], arm: int) -> bool:
        return all(
            source(profile, master, replicate, arm, "generation")["fire_fraction"] >= minimum_coverage
            and source(profile, master, replicate, arm, "generation")["raw"] > 0.0
            for replicate in replicates
        )

    def longest_prefix(profile: str, master: int, replicates: tuple[int, ...], requested: int) -> int:
        admissible = [arm for arm in STATES if arm <= requested and eligible(profile, master, replicates, arm)]
        require(admissible, "arm 1 must be an eligible terminal fallback")
        return max(admissible)

    def candidate(
        profile: str,
        master: int,
        requested: int,
        ledger: str,
        first: bool,
        forced_return: int | None = None,
        salvage: bool = True,
    ) -> Candidate | None:
        replicates = (0,) if first else HOLDOUT_REPLICATES
        if forced_return is not None:
            returned = forced_return
            require(returned <= requested and eligible(profile, master, replicates, returned), "forced return invalid")
        elif salvage:
            returned = longest_prefix(profile, master, replicates, requested)
        elif eligible(profile, master, replicates, requested):
            returned = requested
        else:
            return None

        generation_costs = [
            source(profile, master, replicate, requested, "generation")["cost_s"]
            for replicate in replicates
        ]
        ledger_costs = [replay_cost(profile, master, replicate, returned, ledger) for replicate in replicates]
        actual_costs = [
            source(profile, master, replicate, returned, "replay")["cost_s"]
            for replicate in replicates
        ]
        raw_values = [
            source(profile, master, replicate, returned, "generation")["raw"]
            for replicate in replicates
        ]
        return Candidate(
            requested=requested,
            returned=returned,
            generation_cost=max(generation_costs),
            ledger_replay_cost=max(ledger_costs),
            actual_replay_cost=max(actual_costs),
            raw=min(raw_values),
        )

    def select_mpc(profile: str, master: int, ledger: str) -> int:
        sentinel_generation = source(profile, master, 0, 24, "generation")["cost_s"]
        estimates: dict[int, float] = {}
        for arm in (8, 24):
            if not eligible(profile, master, (0,), arm):
                continue
            first_replay = replay_cost(profile, master, 0, arm, ledger)
            fill_generation = max(
                source(profile, master, replicate, arm, "generation")["cost_s"]
                for replicate in HOLDOUT_REPLICATES
            )
            fill_replay = max(
                replay_cost(profile, master, replicate, arm, ledger)
                for replicate in HOLDOUT_REPLICATES
            )
            additional = min(
                candidate_cap - 1,
                math.floor(max(0.0, generation_budget - sentinel_generation) / fill_generation),
                math.floor(max(0.0, replay_budget - first_replay) / fill_replay),
            )
            raw = source(profile, master, 0, arm, "generation")["raw"]
            estimates[arm] = raw * (1 + additional)
        if 8 in estimates and 24 in estimates and estimates[24] >= ACTIVATION_MARGIN * estimates[8]:
            return 24
        if 8 in estimates:
            return 8
        return 1

    def run_policy(
        profile: str,
        master: int,
        proposal: Callable[[int], int],
        ledger: str = "calibrated",
        mpc: bool = False,
        salvage: bool = True,
    ) -> Portfolio:
        remaining_generation = generation_budget
        remaining_replay = replay_budget
        total_actual_replay = 0.0
        total_generation = 0.0
        total_ledger_replay = 0.0
        total_raw = 0.0
        state = 24
        first_returned = 0
        count = 0
        chosen = select_mpc(profile, master, ledger) if mpc else None

        while count < candidate_cap:
            requested = min(24 if mpc and count == 0 else proposal(count), state)
            forced_return = chosen if mpc and count == 0 else None
            item = candidate(
                profile,
                master,
                requested,
                ledger,
                first=(count == 0),
                forced_return=forced_return,
                salvage=salvage,
            )
            if item is None:
                # A no-salvage control spends the attempted generation cost and
                # produces no candidate.  Repetition would only repeat the same
                # failed request, so terminate after this witnessed failure.
                attempted = source(profile, master, 0, requested, "generation")["cost_s"]
                total_generation += attempted
                break
            if item.generation_cost > remaining_generation + 1e-12:
                break
            if item.ledger_replay_cost > remaining_replay + 1e-12:
                break
            remaining_generation -= item.generation_cost
            remaining_replay -= item.ledger_replay_cost
            total_generation += item.generation_cost
            total_ledger_replay += item.ledger_replay_cost
            total_actual_replay += item.actual_replay_cost
            total_raw += item.raw
            count += 1
            if first_returned == 0:
                first_returned = item.returned
            state = min(state, item.returned)

        return Portfolio(
            raw=total_raw,
            candidates=count,
            generation_cost=total_generation,
            ledger_replay_cost=total_ledger_replay,
            actual_replay_cost=total_actual_replay,
            first_returned=first_returned,
            final_state=state,
        )

    fixed8 = {
        cell: run_policy(*cell, proposal=lambda _index: 8)
        for cell in cells
    }
    fixed24_ceiling = {
        cell: run_policy(*cell, proposal=lambda _index: 24)
        for cell in cells
    }
    fixed24_no_salvage = {
        cell: run_policy(*cell, proposal=lambda _index: 24, salvage=False)
        for cell in cells
    }
    mpc = {
        cell: run_policy(*cell, proposal=lambda _index: 24, mpc=True)
        for cell in cells
    }
    scalar_mpc = {
        cell: run_policy(*cell, proposal=lambda _index: 24, ledger="scalar", mpc=True)
        for cell in cells
    }

    primitive_patterns = {
        primitive_period(pattern)
        for size in range(1, STATIC_MAX_PERIOD + 1)
        for pattern in itertools.product((8, 24), repeat=size)
    }
    static_results: dict[tuple[int, ...], dict[tuple[str, int], Portfolio]] = {}
    for pattern in sorted(primitive_patterns, key=lambda item: (len(item), item)):
        static_results[pattern] = {
            cell: run_policy(*cell, proposal=lambda index, frozen=pattern: frozen[index % len(frozen)])
            for cell in cells
        }

    def aggregate(portfolios: dict[tuple[str, int], Portfolio]) -> float:
        return sum(item.raw for item in portfolios.values())

    best_static_pattern, best_static_cells = min(
        static_results.items(),
        key=lambda item: (-aggregate(item[1]), len(item[0]), item[0]),
    )
    mpc_total = aggregate(mpc)
    ceiling_total = aggregate(fixed24_ceiling)
    fixed8_total = aggregate(fixed8)
    no_salvage_total = aggregate(fixed24_no_salvage)
    best_static_total = aggregate(best_static_cells)
    match_count = sum(
        mpc[cell].first_returned == fixed24_ceiling[cell].first_returned
        for cell in cells
    )
    scalar_overage_cells = sum(
        item.actual_replay_cost > replay_budget + 1e-12
        for item in scalar_mpc.values()
    )
    calibrated_overage_cells = sum(
        item.actual_replay_cost > replay_budget + 1e-12
        for item in mpc.values()
    )

    ratio = mpc_total / ceiling_total
    selector_incremental_gain = ratio - 1.0
    if match_count == len(cells) and ratio <= 1.01:
        decision = "retire_selector_pivot_to_high_ceiling_salvage"
    elif ratio >= 1.05 and match_count < len(cells):
        decision = "retain_selector_for_superseding_hypothesis"
    else:
        decision = "inconclusive_do_not_implement"

    require(all(item.ledger_replay_cost <= replay_budget + 1e-12 for item in mpc.values()), "calibrated ledger accounting overage")
    require(all(item.generation_cost <= generation_budget + 1e-12 for item in mpc.values()), "generation accounting overage")
    require(best_static_pattern in primitive_patterns, "static search result outside frozen class")

    print("mpc24_symmetry_occam_audit=PASS")
    print("antecedent_artifact_status=FAIL")
    print("analysis_scope=exploratory_independent_arm_proxy_not_nested_phase3")
    print(f"artifact_rows={len(rows)}")
    print(f"cells={len(cells)}")
    print(f"static_primitive_patterns={len(primitive_patterns)}")
    print("static_period_limit=6")
    print(f"fixed8_aggregate_raw={fixed8_total:.6f}")
    print(f"fixed24_ceiling_aggregate_raw={ceiling_total:.6f}")
    print(f"fixed24_no_salvage_aggregate_raw={no_salvage_total:.6f}")
    print(f"mpc_calibrated_aggregate_raw={mpc_total:.6f}")
    print(f"best_static_pattern={','.join(map(str, best_static_pattern))}")
    print(f"best_static_aggregate_raw={best_static_total:.6f}")
    print(f"mpc_first_state_matches_fixed24_ceiling={match_count}/{len(cells)}")
    print(f"mpc_to_fixed24_ceiling_ratio={ratio:.12f}")
    print(f"selector_incremental_gain_fraction={selector_incremental_gain:.12f}")
    print(f"calibrated_mpc_actual_replay_overage_cells={calibrated_overage_cells}/{len(cells)}")
    print(f"scalar_mpc_actual_replay_overage_cells={scalar_overage_cells}/{len(cells)}")
    print(f"decision={decision}")
    print("official_target_inference=none")
    print(f"runtime_s={time.monotonic() - started:.9f}")


if __name__ == "__main__":
    main()
