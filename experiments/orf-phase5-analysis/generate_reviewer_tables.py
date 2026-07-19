#!/usr/bin/env python3
"""Generate deterministic reviewer-requested diagnostics from committed tables."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
CORE = REPO / "experiments/runs/orf-p4-core-v1/core-by-master.tsv"
ABLATIONS = REPO / "experiments/runs/orf-p4-ablations-v1/ablation-by-master.tsv"
SCORES = REPO / "experiments/orf-p4-baseline/score-tables.tsv"
OUTPUT = REPO / "paper/tables"
LENGTHS = (1, 2, 4, 8, 16, 24, 32)
CLIFFS = (-1, 4, 8, 16, 24)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, header: list[str], body: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(body)


def action_distributions(core_rows: list[dict[str, str]]) -> None:
    body: list[list[object]] = []
    for row in core_rows:
        counts = json.loads(row["adaptive_fill_length_counts_json"])
        body.append(
            [row["master_index"], row["global_fill_length"]]
            + [counts[str(length)] for length in LENGTHS]
        )
    write_tsv(
        OUTPUT / "action-distributions.tsv",
        ["master_index", "global_fill_length"]
        + [f"adaptive_count_m{length}" for length in LENGTHS],
        body,
    )


def oat_raw_summary(
    core_rows: list[dict[str, str]], ablation_rows: list[dict[str, str]]
) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in ablation_rows:
        grouped[row["ablation"]].append(row)
    core_count = Decimal(len(core_rows))
    core_mean_a = sum(Decimal(row["adaptive_score_raw"]) for row in core_rows) / core_count
    core_mean_g = sum(Decimal(row["global_score_raw"]) for row in core_rows) / core_count
    core_mean_delta = (
        sum(Decimal(row["conditional_regret_raw"]) for row in core_rows) / core_count
    )
    # Recompute from integer score fields rather than averaging the 12-decimal
    # display values stored in the source table.
    core_mean_gain = (
        sum(
            Decimal(100)
            * Decimal(row["conditional_regret_raw"])
            / Decimal(row["global_score_raw"])
            for row in core_rows
        )
        / core_count
    )
    body: list[list[object]] = [
        [
            "core",
            len(core_rows),
            f"{core_mean_a:.3f}",
            f"{core_mean_g:.3f}",
            f"{core_mean_delta:.3f}",
            f"{core_mean_gain:.12f}",
        ]
    ]
    for condition in sorted(grouped):
        group = grouped[condition]
        count = Decimal(len(group))
        mean_a = sum(Decimal(row["adaptive_score_raw"]) for row in group) / count
        mean_g = sum(Decimal(row["global_score_raw"]) for row in group) / count
        mean_delta = sum(Decimal(row["conditional_regret_raw"]) for row in group) / count
        mean_gain = sum(Decimal(row["gain_percent_decimal"]) for row in group) / count
        body.append(
            [
                condition,
                len(group),
                f"{mean_a:.3f}",
                f"{mean_g:.3f}",
                f"{mean_delta:.3f}",
                f"{mean_gain:.12f}",
            ]
        )
    write_tsv(
        OUTPUT / "oat-raw-summary.tsv",
        [
            "condition",
            "fixed_masters",
            "mean_adaptive_score_raw",
            "mean_global_score_raw",
            "mean_conditional_regret_raw",
            "mean_gain_percent",
        ],
        body,
    )


def stratum_decomposition(
    core_rows: list[dict[str, str]], score_rows: list[dict[str, str]]
) -> None:
    global_lengths = {
        int(row["master_index"]): int(row["global_fill_length"]) for row in core_rows
    }
    grouped: dict[int, dict[str, object]] = defaultdict(
        lambda: {"regret": 0, "profiles": 0, "actions": Counter()}
    )
    for row in score_rows:
        scores = {length: int(row[f"score_m{length}"]) for length in LENGTHS}
        best_score = max(scores.values())
        best_length = min(length for length, score in scores.items() if score == best_score)
        global_length = global_lengths[int(row["master_index"])]
        record = grouped[int(row["stratum_index"])]
        record["regret"] = int(record["regret"]) + best_score - scores[global_length]
        record["profiles"] = int(record["profiles"]) + 1
        actions = record["actions"]
        assert isinstance(actions, Counter)
        actions[best_length] += 1

    total_regret = sum(int(record["regret"]) for record in grouped.values())
    body: list[list[object]] = []
    with localcontext() as context:
        context.prec = 40
        for stratum in range(40):
            value = stratum
            cliff_index = value % 5
            value //= 5
            curvature_index = value % 2
            value //= 2
            linear_index = value % 2
            value //= 2
            reset_index = value % 2
            record = grouped[stratum]
            actions = record["actions"]
            assert isinstance(actions, Counter)
            maximum_count = max(actions.values())
            modal_action = min(action for action, count in actions.items() if count == maximum_count)
            regret = int(record["regret"])
            share = Decimal(100 * regret) / Decimal(total_regret)
            body.append(
                [
                    stratum,
                    "low" if reset_index == 0 else "high",
                    "low" if linear_index == 0 else "high",
                    "none" if curvature_index == 0 else "high",
                    CLIFFS[cliff_index],
                    record["profiles"],
                    regret,
                    f"{share:.6f}",
                    modal_action,
                ]
            )
    write_tsv(
        OUTPUT / "stratum-regret-decomposition.tsv",
        [
            "stratum",
            "reset_band",
            "linear_band",
            "curvature",
            "cliff",
            "profiles",
            "regret_raw",
            "regret_share_percent",
            "modal_adaptive_length",
        ],
        body,
    )


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    core_rows = rows(CORE)
    action_distributions(core_rows)
    oat_raw_summary(core_rows, rows(ABLATIONS))
    stratum_decomposition(core_rows, rows(SCORES))
    print("reviewer_tables=PASS files=3")


if __name__ == "__main__":
    main()
