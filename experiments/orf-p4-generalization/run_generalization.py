#!/usr/bin/env python3
"""Run the preregistered ORF Phase-4 public generalization regime."""

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
RUNNER_PATH = Path("experiments/orf-p4-generalization/run_generalization.py")
BUNDLE_PATH = Path("experiments/orf_bundle.py")
CONFIG_PATH = Path("experiments/configs/orf-phase4-v1.json")
SUPPORT_PATH = Path("experiments/poc/orf_support_calibration.py")
CORE_RUNNER_PATH = Path("experiments/orf-p4-core/run_core.py")
CORE_COMPLETE_PATH = Path("experiments/runs/orf-p4-core-v1/COMPLETE.json")
CORE_SUMMARY_PATH = Path("experiments/runs/orf-p4-core-v1/core-summary.json")
RUNS_PARENT = Path("experiments/runs")
ATTEMPT_PATH = Path("experiments/runs/orf-p4-generalization-v1")
CANONICAL_COMMAND = (
    "comp/.venv/bin/python -I experiments/orf-p4-generalization/run_generalization.py "
    "--config experiments/configs/orf-phase4-v1.json "
    "--attempt-dir experiments/runs/orf-p4-generalization-v1"
)
EXPECTED_HASHES = {
    BUNDLE_PATH: "8c4b9cd3bf4ea0053e96a851b88a60bb6a92972b2e7f8a6e3a4c6bd91550aedd",
    CONFIG_PATH: "e3ebe822094c91d6b6e83de6bc55324e43301b74df9a6e3bc3ee3e932b0ba748",
    SUPPORT_PATH: "fdc68ce08923be8d693155bb2641841a3a706164ebcb9d05e6a330a1d8c67fe9",
    CORE_RUNNER_PATH: "41aa108f5f18c60a7072666d32fe010b447a1617c7c5938a1f54573b01e74715",
    CORE_COMPLETE_PATH: "a6630cde76050ed5c6a227bf79cc809d12ddcad14a9e67551ebd37123d3a2809",
    CORE_SUMMARY_PATH: "93e2030dbc1718947208ae041b5884046e0eb078a61815dee290d75946e77d88",
}
OUTPUT_ARTIFACTS = (
    "generalization-score-tables.tsv",
    "generalization-by-master.tsv",
    "generalization-summary.json",
    "notes.md",
    "run.log",
)
LENGTHS = (1, 2, 4, 8, 16, 24, 32)
PREIMAGES = tuple(
    f"orf-public-phase4-generalization-v1|master|{index:03d}"
    for index in range(3)
)
SATURATION = 10**18
PHYSICAL_PROFILES = 320
NO_CLIFF_PHYSICAL = 64
CLIFF_PHYSICAL = 256
EFFECTIVE_WEIGHT = 512
PREDICTED_MEAN = Fraction(35, 1)
CONFIRM_INTERVAL = (Fraction(30, 1), Fraction(45, 1))
MATERIALITY = Fraction(5, 1)
EXPECTED_GENERALIZATION = {
    "benchmark": "unsaturated balanced-cliff synthetic regime",
    "saturation": SATURATION,
    "weights": "no-cliff profiles weight 4; cliff profiles weight 1",
    "primary_metric": "mean_generalization_gain_percent",
    "predicted_value": 35.0,
    "support_threshold_inclusive": 5.0,
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
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    )


def fraction_payload(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def profile_weight(cliff: int) -> int:
    if cliff not in (-1, 4, 8, 16, 24):
        raise ValueError("cliff is outside the frozen crossed design")
    return 4 if cliff == -1 else 1


def evaluate_weighted(core: ModuleType, tables: Sequence[Sequence[int]], weights: Sequence[int]) -> Any:
    if len(tables) != len(weights) or not tables:
        raise ValueError("tables and weights must have equal nonzero length")
    expanded: list[Sequence[int]] = []
    for table, weight in zip(tables, weights):
        if weight not in (1, 4):
            raise ValueError("only frozen weights one and four are allowed")
        expanded.extend([table] * weight)
    return core.evaluate_master_score_tables(expanded)


def peak_memory_gb() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    divisor = 1024**3 if sys.platform == "darwin" else 1024**2
    return usage / divisor


def score_header() -> list[str]:
    header = [
        "master_index",
        "master_digest_hex",
        "profile_index",
        "stratum_index",
        "replicate_index",
        "cliff",
        "weight",
        "minimum_cliff_floor_distance",
    ]
    for length in LENGTHS:
        header.extend(
            [
                f"cost_numerator_m{length}",
                f"cost_denominator_m{length}",
                f"events_m{length}",
                f"score_m{length}",
            ]
        )
    return header


def render_score_row(
    master_index: int,
    digest: str,
    profile_index: int,
    profile: Any,
    weight: int,
    scores: Sequence[int],
) -> str:
    stratum, replicate = divmod(profile_index, 8)
    row = [
        str(master_index),
        digest,
        str(profile_index),
        str(stratum),
        str(replicate),
        str(profile.cliff),
        str(weight),
        "" if profile.floor_margin is None else str(profile.floor_margin),
    ]
    for cost, event, score in zip(profile.costs, profile.events, scores):
        row.extend(
            [str(cost.numerator), str(cost.denominator), str(event), str(score)]
        )
    return "\t".join(row)


def master_record(core: ModuleType, index: int, digest: str, result: Any) -> dict[str, Any]:
    return {
        "adaptive_fill_length_counts_weighted": {
            str(length): count
            for length, count in zip(LENGTHS, result.adaptive_length_counts)
        },
        "adaptive_gain_percent_decimal": core.fixed_12(result.gain_percent),
        "adaptive_gain_percent_exact": fraction_payload(result.gain_percent),
        "adaptive_score_raw_weighted": result.adaptive_score,
        "conditional_regret_raw_weighted": result.regret,
        "effective_profile_weight": EFFECTIVE_WEIGHT,
        "global_fill_length": result.global_length,
        "global_score_raw_weighted": result.global_score,
        "master_digest_hex": digest,
        "master_index": index,
        "physical_profiles": PHYSICAL_PROFILES,
    }


def render_master_table(records: Sequence[dict[str, Any]]) -> str:
    header = [
        "master_index",
        "master_digest_hex",
        "physical_profiles",
        "effective_profile_weight",
        "adaptive_score_raw_weighted",
        "global_score_raw_weighted",
        "conditional_regret_raw_weighted",
        "gain_numerator",
        "gain_denominator",
        "gain_percent_decimal",
        "global_fill_length",
        "adaptive_fill_length_counts_weighted_json",
    ]
    lines = ["\t".join(header)]
    for record in records:
        exact = record["adaptive_gain_percent_exact"]
        lines.append(
            "\t".join(
                [
                    str(record["master_index"]),
                    str(record["master_digest_hex"]),
                    str(record["physical_profiles"]),
                    str(record["effective_profile_weight"]),
                    str(record["adaptive_score_raw_weighted"]),
                    str(record["global_score_raw_weighted"]),
                    str(record["conditional_regret_raw_weighted"]),
                    str(exact["numerator"]),
                    str(exact["denominator"]),
                    str(record["adaptive_gain_percent_decimal"]),
                    str(record["global_fill_length"]),
                    json.dumps(
                        record["adaptive_fill_length_counts_weighted"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                ]
            )
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--attempt-dir", type=Path, required=True)
    args = parser.parse_args()
    if Path.cwd().resolve() != REPO or not sys.flags.isolated:
        raise RuntimeError("runner requires repository root and Python isolated mode")
    if sys.argv != [
        RUNNER_PATH.as_posix(),
        "--config",
        CONFIG_PATH.as_posix(),
        "--attempt-dir",
        ATTEMPT_PATH.as_posix(),
    ]:
        raise ValueError(f"runner requires exact command: {CANONICAL_COMMAND}")
    if args.config != CONFIG_PATH or args.attempt_dir != ATTEMPT_PATH:
        raise ValueError("argument paths differ from preregistration")
    for relative, expected in EXPECTED_HASHES.items():
        path = REPO / relative
        if path.is_symlink() or not path.is_file() or file_sha256(path) != expected:
            raise ValueError(f"frozen binding mismatch: {relative}")

    bundle = load_module(REPO / BUNDLE_PATH, "orf_p4_generalization_bundle")
    support = load_module(REPO / SUPPORT_PATH, "orf_p4_generalization_support")
    core = load_module(REPO / CORE_RUNNER_PATH, "orf_p4_generalization_core")
    binding_paths = (
        RUNNER_PATH,
        BUNDLE_PATH,
        CONFIG_PATH,
        SUPPORT_PATH,
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
        if config.get("generalization_master_preimages_ascii") != list(PREIMAGES):
            raise ValueError("generalization master labels differ from protocol")
        if config.get("generalization") != EXPECTED_GENERALIZATION:
            raise ValueError("generalization regime differs from protocol")
        if tuple(support.LENGTHS) != LENGTHS:
            raise ValueError("support action set differs from protocol")

        score_lines = ["\t".join(score_header())]
        records: list[dict[str, Any]] = []
        floor_margins: list[Any] = []
        for master_index, preimage in enumerate(PREIMAGES):
            master = hashlib.sha256(preimage.encode("ascii")).digest()
            digest = master.hex()
            profiles, floor_margin = support.build_profiles(master)
            floor_margins.append(floor_margin)
            if len(profiles) != PHYSICAL_PROFILES:
                raise ValueError("generalization master does not have 320 profiles")
            no_cliff_count = sum(profile.cliff == -1 for profile in profiles)
            if no_cliff_count != NO_CLIFF_PHYSICAL:
                raise ValueError("no-cliff physical count differs from crossed design")
            if len(profiles) - no_cliff_count != CLIFF_PHYSICAL:
                raise ValueError("cliff physical count differs from crossed design")
            tables: list[tuple[int, ...]] = []
            weights: list[int] = []
            for profile_index, profile in enumerate(profiles):
                weight = profile_weight(profile.cliff)
                scores = tuple(support.score_table(profile, SATURATION))
                tables.append(scores)
                weights.append(weight)
                score_lines.append(
                    render_score_row(
                        master_index,
                        digest,
                        profile_index,
                        profile,
                        weight,
                        scores,
                    )
                )
            if sum(weights) != EFFECTIVE_WEIGHT:
                raise ValueError("effective balanced weight is not 512")
            result = evaluate_weighted(core, tables, weights)
            records.append(master_record(core, master_index, digest, result))

        if len(score_lines) != 1 + len(PREIMAGES) * PHYSICAL_PROFILES:
            raise AssertionError("generalization profile row count mismatch")
        gains = [
            Fraction(
                record["adaptive_gain_percent_exact"]["numerator"],
                record["adaptive_gain_percent_exact"]["denominator"],
            )
            for record in records
        ]
        mean_gain = sum(gains, Fraction()) / len(gains)
        clear_fraction = Fraction(sum(gain >= MATERIALITY for gain in gains), len(gains))
        elapsed = time.perf_counter() - started
        memory = peak_memory_gb()
        summary = {
            "claim_scope": "public deterministic non-target generalization only",
            "inputs": {
                path.as_posix(): digest for path, digest in EXPECTED_HASHES.items()
            },
            "limitations": [
                "The three deterministic public masters do not define a population sample.",
                "The weighted unsaturated synthetic regime does not establish live-model prevalence or learnability.",
                "No held-out, deadline, private-transfer, network, or Kaggle claim is supported.",
            ],
            "masters": records,
            "minimum_cliff_floor_distance": str(min(floor_margins)),
            "primary": {
                "all_masters_clear_fraction_decimal": core.fixed_12(clear_fraction),
                "all_masters_clear_fraction_exact": fraction_payload(clear_fraction),
                "confirm_interval_inclusive_percent": [30, 45],
                "maximum_gain_percent_decimal": core.fixed_12(max(gains)),
                "mean_gain_percent_decimal": core.fixed_12(mean_gain),
                "mean_gain_percent_exact": fraction_payload(mean_gain),
                "minimum_gain_percent_decimal": core.fixed_12(min(gains)),
                "predicted_mean_gain_percent": 35,
                "support_threshold_percent_inclusive": 5,
            },
            "resources": {
                "peak_memory_gb": round(memory, 9),
                "runtime_seconds": round(elapsed, 9),
            },
            "run_id": "orf-p4-generalization",
            "schema_version": "orf-phase4-generalization-v1",
            "status": "PUBLIC_NON_TARGET_GENERALIZATION",
        }
        metrics = {
            "mean_generalization_gain_percent": core.fixed_12(mean_gain),
            "minimum_generalization_gain_percent": core.fixed_12(min(gains)),
            "maximum_generalization_gain_percent": core.fixed_12(max(gains)),
            "all_generalization_masters_clear_fraction": core.fixed_12(clear_fraction),
            "physical_profiles_evaluated": str(len(PREIMAGES) * PHYSICAL_PROFILES),
            "effective_profile_weight_evaluated": str(len(PREIMAGES) * EFFECTIVE_WEIGHT),
            "peak_memory_gb": f"{memory:.9f}",
            "runtime_seconds": f"{elapsed:.9f}",
        }
        notes = (
            "# ORF Phase-4 generalization notes\n\n"
            "Three disjoint public SHA-256 masters use the immutable generator, "
            "H=10^18, and exact no-cliff weight four versus cliff weight one. "
            "The reviewed core evaluator consumes exact replicated rows, preserving "
            "the same adaptive/global policies and tie rule.\n\n"
            "There were no deviations or retries. Scope is public deterministic "
            "non-target generalization only.\n"
        )
        writer.write_text(
            "generalization-score-tables.tsv", "\n".join(score_lines) + "\n"
        )
        writer.write_text("generalization-by-master.tsv", render_master_table(records))
        writer.write_text("generalization-summary.json", canonical_json(summary))
        writer.write_text("notes.md", notes)
        writer.log_metrics(metrics)
        writer.complete()

    for name, value in metrics.items():
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
