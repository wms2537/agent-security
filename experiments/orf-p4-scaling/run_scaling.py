#!/usr/bin/env python3
"""Run the preregistered ORF Phase-4 nested-scale robustness check."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Sequence


REPO = Path(__file__).resolve().parents[2]
RUNNER_PATH = Path("experiments/orf-p4-scaling/run_scaling.py")
BUNDLE_PATH = Path("experiments/orf_bundle.py")
CONFIG_PATH = Path("experiments/configs/orf-phase4-v1.json")
BASELINE_PATH = Path("experiments/orf-p4-baseline/score-tables.tsv")
CORE_RUNNER_PATH = Path("experiments/orf-p4-core/run_core.py")
CORE_COMPLETE_PATH = Path("experiments/runs/orf-p4-core-v1/COMPLETE.json")
CORE_SUMMARY_PATH = Path("experiments/runs/orf-p4-core-v1/core-summary.json")
RUNS_PARENT = Path("experiments/runs")
ATTEMPT_PATH = Path("experiments/runs/orf-p4-scaling-v1")
CANONICAL_COMMAND = (
    "comp/.venv/bin/python -I experiments/orf-p4-scaling/run_scaling.py "
    "--config experiments/configs/orf-phase4-v1.json "
    "--baseline-tables experiments/orf-p4-baseline/score-tables.tsv "
    "--attempt-dir experiments/runs/orf-p4-scaling-v1"
)
EXPECTED_HASHES = {
    BUNDLE_PATH: "8c4b9cd3bf4ea0053e96a851b88a60bb6a92972b2e7f8a6e3a4c6bd91550aedd",
    CONFIG_PATH: "e3ebe822094c91d6b6e83de6bc55324e43301b74df9a6e3bc3ee3e932b0ba748",
    BASELINE_PATH: "331e8b5e16b42d8781df68fd49aa9cd83a4d77c8f5ec0ab9de15e09137e59cbf",
    CORE_RUNNER_PATH: "41aa108f5f18c60a7072666d32fe010b447a1617c7c5938a1f54573b01e74715",
    CORE_COMPLETE_PATH: "a6630cde76050ed5c6a227bf79cc809d12ddcad14a9e67551ebd37123d3a2809",
    CORE_SUMMARY_PATH: "93e2030dbc1718947208ae041b5884046e0eb078a61815dee290d75946e77d88",
}
OUTPUT_ARTIFACTS = ("scaling-by-cell.tsv", "scaling-summary.json", "notes.md", "run.log")
LENGTHS = (1, 2, 4, 8, 16, 24, 32)
PRIMARY_PREIMAGES = tuple(f"orf-public-phase4-v1|master|{i:03d}" for i in range(3))
REPLICATE_COUNTS = (1, 4, 8)
PROFILE_COUNTS = (40, 160, 320)
MATERIALITY = Fraction(5, 1)
EXPECTED_SCALING = {
    "replicates_per_stratum": [1, 4, 8],
    "profiles_per_master": [40, 160, 320],
    "selection": "For scale k, include replicate indices 0..k-1 in every stratum.",
    "primary_metric": "all_scale_master_cells_clear_fraction",
    "predicted_value": 1.0,
    "support_rule": "All 9 master-by-scale cells have gain >=5%; report scale means and range.",
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False) + "\n"


def fraction_payload(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def selected_indices(replicates_per_stratum: int) -> tuple[int, ...]:
    if replicates_per_stratum not in REPLICATE_COUNTS:
        raise ValueError("replicate count is outside the frozen scales")
    indices = tuple(
        profile_index
        for profile_index in range(320)
        if profile_index % 8 < replicates_per_stratum
    )
    expected = 40 * replicates_per_stratum
    if len(indices) != expected:
        raise AssertionError("nested scale size differs from crossed design")
    return indices


def peak_memory_gb() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    divisor = 1024**3 if sys.platform == "darwin" else 1024**2
    return usage / divisor


def cell_record(core: ModuleType, master_index: int, k: int, result: Any) -> dict[str, Any]:
    return {
        "adaptive_fill_length_counts": {
            str(length): count
            for length, count in zip(LENGTHS, result.adaptive_length_counts)
        },
        "adaptive_gain_percent_decimal": core.fixed_12(result.gain_percent),
        "adaptive_gain_percent_exact": fraction_payload(result.gain_percent),
        "adaptive_score_raw": result.adaptive_score,
        "conditional_regret_raw": result.regret,
        "global_fill_length": result.global_length,
        "global_score_raw": result.global_score,
        "master_digest_hex": hashlib.sha256(
            PRIMARY_PREIMAGES[master_index].encode("ascii")
        ).hexdigest(),
        "master_index": master_index,
        "profiles": 40 * k,
        "replicates_per_stratum": k,
    }


def render_cells(records: Sequence[dict[str, Any]]) -> str:
    header = [
        "master_index",
        "master_digest_hex",
        "replicates_per_stratum",
        "profiles",
        "adaptive_score_raw",
        "global_score_raw",
        "conditional_regret_raw",
        "gain_numerator",
        "gain_denominator",
        "gain_percent_decimal",
        "global_fill_length",
        "adaptive_fill_length_counts_json",
    ]
    lines = ["\t".join(header)]
    for record in records:
        exact = record["adaptive_gain_percent_exact"]
        lines.append(
            "\t".join(
                [
                    str(record["master_index"]),
                    str(record["master_digest_hex"]),
                    str(record["replicates_per_stratum"]),
                    str(record["profiles"]),
                    str(record["adaptive_score_raw"]),
                    str(record["global_score_raw"]),
                    str(record["conditional_regret_raw"]),
                    str(exact["numerator"]),
                    str(exact["denominator"]),
                    str(record["adaptive_gain_percent_decimal"]),
                    str(record["global_fill_length"]),
                    json.dumps(
                        record["adaptive_fill_length_counts"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                ]
            )
        )
    return "\n".join(lines) + "\n"


def validate_full_scale_against_core(records: Sequence[dict[str, Any]]) -> None:
    summary = json.loads((REPO / CORE_SUMMARY_PATH).read_text(encoding="utf-8"))
    committed = summary["primary"]["masters"]
    full = [record for record in records if record["replicates_per_stratum"] == 8]
    if len(full) != 3 or len(committed) != 3:
        raise ValueError("full-scale/core master count mismatch")
    for record, reference in zip(full, committed):
        exact = reference["adaptive_gain_percent_exact"]
        if (
            record["master_index"] != reference["master_index"]
            or record["adaptive_score_raw"] != reference["adaptive_score_raw"]
            or record["global_score_raw"] != reference["global_score_raw"]
            or record["conditional_regret_raw"] != reference["conditional_regret_raw"]
            or record["adaptive_gain_percent_exact"]
            != {"denominator": exact["denominator"], "numerator": exact["numerator"]}
        ):
            raise ValueError("full scale differs from committed reviewed core")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--baseline-tables", type=Path, required=True)
    parser.add_argument("--attempt-dir", type=Path, required=True)
    args = parser.parse_args()
    if Path.cwd().resolve() != REPO or not sys.flags.isolated:
        raise RuntimeError("runner requires repository root and Python isolated mode")
    if sys.argv != [
        RUNNER_PATH.as_posix(),
        "--config",
        CONFIG_PATH.as_posix(),
        "--baseline-tables",
        BASELINE_PATH.as_posix(),
        "--attempt-dir",
        ATTEMPT_PATH.as_posix(),
    ]:
        raise ValueError(f"runner requires exact command: {CANONICAL_COMMAND}")
    if (args.config, args.baseline_tables, args.attempt_dir) != (
        CONFIG_PATH,
        BASELINE_PATH,
        ATTEMPT_PATH,
    ):
        raise ValueError("argument paths differ from preregistration")
    for relative, expected in EXPECTED_HASHES.items():
        path = REPO / relative
        if path.is_symlink() or not path.is_file() or file_sha256(path) != expected:
            raise ValueError(f"frozen binding mismatch: {relative}")

    bundle = load_module(REPO / BUNDLE_PATH, "orf_p4_scaling_bundle")
    core = load_module(REPO / CORE_RUNNER_PATH, "orf_p4_scaling_core")
    binding_paths = (
        RUNNER_PATH,
        BUNDLE_PATH,
        CONFIG_PATH,
        BASELINE_PATH,
        CORE_RUNNER_PATH,
        CORE_COMPLETE_PATH,
        CORE_SUMMARY_PATH,
    )
    with bundle.AttemptBundle(
        REPO / ATTEMPT_PATH,
        repo_root=REPO,
        allowed_parent=REPO / RUNS_PARENT,
        canonical_command=CANONICAL_COMMAND,
        binding_paths=binding_paths,
        expected_artifacts=OUTPUT_ARTIFACTS,
    ) as writer:
        started = time.perf_counter()
        config = json.loads((REPO / CONFIG_PATH).read_text(encoding="utf-8"))
        core.validate_config(config)
        if config.get("scaling_robustness") != EXPECTED_SCALING:
            raise ValueError("scaling block differs from frozen protocol")
        masters = core.parse_baseline_tables(
            (REPO / BASELINE_PATH).read_text(encoding="utf-8")
        )
        records: list[dict[str, Any]] = []
        for k in REPLICATE_COUNTS:
            indices = selected_indices(k)
            for master_index, master in enumerate(masters):
                selected = [master[index] for index in indices]
                if len(selected) != 40 * k:
                    raise AssertionError("selected table size mismatch")
                result = core.evaluate_master_score_tables(selected)
                records.append(cell_record(core, master_index, k, result))
        if len(records) != 9:
            raise AssertionError("scaling cell count mismatch")
        validate_full_scale_against_core(records)
        gains = [
            Fraction(
                record["adaptive_gain_percent_exact"]["numerator"],
                record["adaptive_gain_percent_exact"]["denominator"],
            )
            for record in records
        ]
        clear_fraction = Fraction(sum(gain >= MATERIALITY for gain in gains), len(gains))
        by_scale: dict[str, dict[str, Any]] = {}
        for k, n in zip(REPLICATE_COUNTS, PROFILE_COUNTS):
            subset = [
                gain
                for record, gain in zip(records, gains)
                if record["replicates_per_stratum"] == k
            ]
            mean = sum(subset, Fraction()) / len(subset)
            by_scale[str(n)] = {
                "maximum_gain_percent_decimal": core.fixed_12(max(subset)),
                "mean_gain_percent_decimal": core.fixed_12(mean),
                "mean_gain_percent_exact": fraction_payload(mean),
                "minimum_gain_percent_decimal": core.fixed_12(min(subset)),
                "profiles_per_master": n,
                "replicates_per_stratum": k,
            }
        elapsed = time.perf_counter() - started
        memory = peak_memory_gb()
        summary = {
            "all_scale_master_cells_clear_fraction_decimal": core.fixed_12(clear_fraction),
            "all_scale_master_cells_clear_fraction_exact": fraction_payload(clear_fraction),
            "by_scale": by_scale,
            "cells": records,
            "claim_scope": "public deterministic non-target scaling robustness only",
            "inputs": {path.as_posix(): digest for path, digest in EXPECTED_HASHES.items()},
            "limitations": [
                "Nested deterministic subsets are robustness checks, not independent samples.",
                "No live, held-out, learnability, deadline, private-transfer, or Kaggle claim is supported.",
            ],
            "predicted_all_cells_clear_fraction": 1.0,
            "resources": {"peak_memory_gb": round(memory, 9), "runtime_seconds": round(elapsed, 9)},
            "run_id": "orf-p4-scaling",
            "schema_version": "orf-phase4-scaling-v1",
            "status": "PUBLIC_NON_TARGET_SCALING_ROBUSTNESS",
        }
        metrics = {
            "all_scale_master_cells_clear_fraction": core.fixed_12(clear_fraction),
            "scale_forty_mean_gain_percent": by_scale["40"]["mean_gain_percent_decimal"],
            "scale_one_hundred_sixty_mean_gain_percent": by_scale["160"]["mean_gain_percent_decimal"],
            "scale_three_hundred_twenty_mean_gain_percent": by_scale["320"]["mean_gain_percent_decimal"],
            "minimum_cell_gain_percent": core.fixed_12(min(gains)),
            "maximum_cell_gain_percent": core.fixed_12(max(gains)),
            "scale_master_cells": str(len(records)),
            "peak_memory_gb": f"{memory:.9f}",
            "runtime_seconds": f"{elapsed:.9f}",
        }
        notes = (
            "# ORF Phase-4 scaling notes\n\n"
            "Each scale is a strict nested subset selected by replicate index in every "
            "stratum. The reviewed evaluator consumes the committed score rows without "
            "regeneration or retuning. Full-scale records are checked against the "
            "committed core evidence.\n\nThere were no deviations or retries.\n"
        )
        writer.write_text("scaling-by-cell.tsv", render_cells(records))
        writer.write_text("scaling-summary.json", canonical_json(summary))
        writer.write_text("notes.md", notes)
        writer.log_metrics(metrics)
        writer.complete()

    for name, value in metrics.items():
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
