#!/usr/bin/env python3
"""Evaluate the preregistered public, non-target ORF Phase-4 core policy.

The primary calculation consumes the frozen baseline's per-profile score table.
It never regenerates primary profiles and never trusts a baseline aggregate.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import math
import resource
import statistics
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Sequence


REPO = Path(__file__).resolve().parents[2]
EXPECTED_CONFIG = Path("experiments/configs/orf-phase4-v1.json")
EXPECTED_BASELINE_TABLE = Path("experiments/orf-p4-baseline/score-tables.tsv")
EXPECTED_OUTPUT_DIR = Path("experiments/orf-p4-core")
SUPPORT_PATH = Path("experiments/poc/orf_support_calibration.py")
EXPECTED_CONFIG_SHA256 = "e3ebe822094c91d6b6e83de6bc55324e43301b74df9a6e3bc3ee3e932b0ba748"
EXPECTED_SUPPORT_SHA256 = "fdc68ce08923be8d693155bb2641841a3a706164ebcb9d05e6a330a1d8c67fe9"
EXPECTED_BASELINE_TABLE_SHA256 = "331e8b5e16b42d8781df68fd49aa9cd83a4d77c8f5ec0ab9de15e09137e59cbf"
CONTRACT_VERSION = "orf-phase4-public-nontarget-v1"
CLAIM_SCOPE = "public deterministic non-target validation only"
LENGTHS = (1, 2, 4, 8, 16, 24, 32)
PRIMARY_PREIMAGES = (
    "orf-public-phase4-v1|master|000",
    "orf-public-phase4-v1|master|001",
    "orf-public-phase4-v1|master|002",
)
PROFILES_PER_MASTER = 320
STRATA = 40
REPLICATES_PER_STRATUM = 8
SATURATION = 200_000
MATERIALITY_THRESHOLD = Fraction(5, 1)
CORE_PREDICTION = Fraction(40, 1)
CORE_CONFIRM_INTERVAL = (Fraction(30, 1), Fraction(50, 1))
HOMOGENEOUS_SUFFIX = "|homogeneous"
HOMOGENEOUS_PROFILES = 64
HOMOGENEOUS_EXPECTED_DIFFERENCE = 0
HOMOGENEOUS_EXPECTED_GLOBAL_LENGTH = 1
HOMOGENEOUS_BOUNDS = ("5", "12")
T_CRITICAL_DF_TWO = 4.302652729911275
FORBIDDEN = (
    "Kaggle action",
    "beacon fetch",
    "held-out freeze",
    "held-out target derivation",
    "held-out profile generation",
    "held-out evaluation",
    "external terminal post",
)


@dataclass(frozen=True)
class MasterResult:
    adaptive_score: int
    global_score: int
    regret: int
    gain_percent: Fraction
    global_length: int
    adaptive_length_counts: tuple[int, ...]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def fixed_12(value: Fraction) -> str:
    """Render a Fraction to twelve places using round-half-away from zero."""
    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    quotient, remainder = divmod(magnitude.numerator * 10**12, magnitude.denominator)
    if remainder * 2 >= magnitude.denominator:
        quotient += 1
    whole, fractional = divmod(quotient, 10**12)
    return f"{sign}{whole}.{fractional:012d}"


def fraction_payload(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def best_index(values: Sequence[int], lengths: Sequence[int] = LENGTHS) -> int:
    if len(values) != len(lengths) or not values:
        raise ValueError("values and lengths must have the same nonzero size")
    return max(range(len(lengths)), key=lambda index: (values[index], -lengths[index]))


def evaluate_master_score_tables(
    tables: Sequence[Sequence[int]], lengths: Sequence[int] = LENGTHS
) -> MasterResult:
    """Compute exact adaptive and global scores from per-profile action scores."""
    if not tables:
        raise ValueError("a master must contain at least one profile")
    if tuple(sorted(lengths)) != tuple(lengths) or len(set(lengths)) != len(lengths):
        raise ValueError("lengths must be unique and increasing")

    totals = [0] * len(lengths)
    adaptive_score = 0
    adaptive_counts = [0] * len(lengths)
    for row in tables:
        if len(row) != len(lengths):
            raise ValueError("every score row must contain one value per length")
        if any(type(value) is not int or value < 0 for value in row):
            raise ValueError("scores must be nonnegative integers")
        row_best = best_index(row, lengths)
        adaptive_score += row[row_best]
        adaptive_counts[row_best] += 1
        for index, value in enumerate(row):
            totals[index] += value

    global_index = best_index(totals, lengths)
    global_score = totals[global_index]
    if global_score <= 0:
        raise ValueError("the selected global score must be positive")
    regret = adaptive_score - global_score
    if regret < 0:
        raise AssertionError("adaptive score cannot be below exhaustive global score")
    return MasterResult(
        adaptive_score=adaptive_score,
        global_score=global_score,
        regret=regret,
        gain_percent=Fraction(100 * regret, global_score),
        global_length=lengths[global_index],
        adaptive_length_counts=tuple(adaptive_counts),
    )


def resolve_exact_repo_path(raw: Path, expected: Path, *, must_exist: bool) -> Path:
    candidate = raw if raw.is_absolute() else REPO / raw
    resolved = candidate.resolve(strict=must_exist)
    expected_resolved = (REPO / expected).resolve(strict=must_exist)
    if resolved != expected_resolved:
        raise ValueError(f"path must resolve to {expected.as_posix()}")
    if not resolved.is_relative_to(REPO):
        raise ValueError("path leaves repository")
    return resolved


def load_support(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("orf_phase4_core_support", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load immutable support module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_config(config: dict[str, Any]) -> None:
    expected_top_level = {
        "ablations",
        "base_contract",
        "baseline",
        "claim_scope",
        "contract_version",
        "distinguishing_negative",
        "forbidden",
        "generalization",
        "generalization_master_preimages_ascii",
        "immutable_paths",
        "lengths",
        "master_derivation",
        "primary",
        "primary_master_preimages_ascii",
        "run_limits",
        "scaling_robustness",
    }
    if set(config) != expected_top_level:
        raise ValueError("config top-level fields differ from frozen Phase-4 protocol")
    exact_top_level = {
        "base_contract": "experiments/configs/evaluation-contract.md",
        "claim_scope": CLAIM_SCOPE,
        "contract_version": CONTRACT_VERSION,
        "lengths": list(LENGTHS),
        "master_derivation": "SHA256(ASCII preimage)",
        "primary_master_preimages_ascii": list(PRIMARY_PREIMAGES),
        "forbidden": list(FORBIDDEN),
    }
    for key, expected in exact_top_level.items():
        if config.get(key) != expected:
            raise ValueError(f"unexpected frozen config value for {key}")

    primary = config.get("primary")
    if not isinstance(primary, dict):
        raise ValueError("config primary block is missing")
    exact_primary = {
        "profiles_per_master": PROFILES_PER_MASTER,
        "strata": STRATA,
        "replicates_per_stratum": REPLICATES_PER_STRATUM,
        "saturation": SATURATION,
        "weighting": "equal",
        "baseline_policy": "PROBE_GLOBAL: one exhaustively selected fill length per master",
        "core_policy": "ADAPTIVE: one exhaustively selected fill length per profile",
        "primary_metric": "mean_adaptive_gain_percent",
        "per_master_metric": "100*(A-G)/G",
        "materiality_threshold_inclusive": float(MATERIALITY_THRESHOLD),
        "core_prediction": float(CORE_PREDICTION),
        "core_prediction_confirm_interval_inclusive": [
            float(CORE_CONFIRM_INTERVAL[0]),
            float(CORE_CONFIRM_INTERVAL[1]),
        ],
    }
    if set(primary) != set(exact_primary):
        raise ValueError("primary config fields differ from frozen Phase-4 protocol")
    for key, expected in exact_primary.items():
        if primary.get(key) != expected:
            raise ValueError(f"unexpected primary config value for {key}")

    negative = config.get("distinguishing_negative")
    exact_negative = {
        "profiles_per_master": HOMOGENEOUS_PROFILES,
        "master_preimage_suffix": HOMOGENEOUS_SUFFIX,
        "expected_difference_raw": HOMOGENEOUS_EXPECTED_DIFFERENCE,
        "expected_global_fill_length": HOMOGENEOUS_EXPECTED_GLOBAL_LENGTH,
    }
    if negative != exact_negative:
        raise ValueError("homogeneous negative config differs from frozen protocol")

    limits = config.get("run_limits")
    expected_limits = {
        "cpu_only": True,
        "maximum_minutes_per_run": 5,
        "fix_attempts_per_change": 2,
        "network": False,
    }
    if limits != expected_limits:
        raise ValueError("resource/action limits differ from frozen protocol")


def baseline_header() -> list[str]:
    header = [
        "master_index",
        "master_digest_hex",
        "profile_index",
        "stratum_index",
        "replicate_index",
        "cliff",
        "minimum_cliff_floor_distance",
    ]
    for length in LENGTHS:
        header.extend(
            [
                f"cost_numerator_m{length}",
                f"cost_denominator_m{length}",
                f"events_m{length}",
            ]
        )
    header.extend(f"score_m{length}" for length in LENGTHS)
    return header


def canonical_nonnegative_int(raw: str, field: str) -> int:
    if not raw or any(character < "0" or character > "9" for character in raw):
        raise ValueError(f"{field} must be a nonnegative base-ten integer")
    return int(raw)


def parse_baseline_tables(text: str) -> list[list[tuple[int, ...]]]:
    rows = csv.reader(io.StringIO(text), delimiter="\t", strict=True)
    try:
        header = next(rows)
    except StopIteration as exc:
        raise ValueError("baseline table is empty") from exc
    expected_header = baseline_header()
    if header != expected_header:
        raise ValueError("baseline table columns or column sequence differ from protocol")
    score_indices = [header.index(f"score_m{length}") for length in LENGTHS]
    if len(score_indices) != 7:
        raise AssertionError("exactly seven score columns are required")

    masters: list[list[tuple[int, ...]]] = [[] for _ in PRIMARY_PREIMAGES]
    expected_rows = len(PRIMARY_PREIMAGES) * PROFILES_PER_MASTER
    observed_rows = 0
    for observed_rows, row in enumerate(rows, start=1):
        if observed_rows > expected_rows:
            raise ValueError("baseline table contains more than 960 data rows")
        if len(row) != len(expected_header):
            raise ValueError(f"baseline row {observed_rows} has the wrong width")
        expected_master = (observed_rows - 1) // PROFILES_PER_MASTER
        expected_profile = (observed_rows - 1) % PROFILES_PER_MASTER
        expected_stratum, expected_replicate = divmod(
            expected_profile, REPLICATES_PER_STRATUM
        )
        expected_digest = hashlib.sha256(
            PRIMARY_PREIMAGES[expected_master].encode("ascii")
        ).hexdigest()
        exact_fields = {
            "master_index": expected_master,
            "profile_index": expected_profile,
            "stratum_index": expected_stratum,
            "replicate_index": expected_replicate,
        }
        for field, expected in exact_fields.items():
            observed = canonical_nonnegative_int(row[header.index(field)], field)
            if observed != expected:
                raise ValueError(
                    f"baseline row {observed_rows} violates {field} sequence"
                )
        if row[header.index("master_digest_hex")] != expected_digest:
            raise ValueError(f"baseline row {observed_rows} has the wrong master digest")
        scores = tuple(
            canonical_nonnegative_int(row[index], header[index])
            for index in score_indices
        )
        masters[expected_master].append(scores)

    if observed_rows != expected_rows:
        raise ValueError(f"baseline table must contain exactly {expected_rows} data rows")
    if any(len(rows_for_master) != PROFILES_PER_MASTER for rows_for_master in masters):
        raise AssertionError("baseline table master partition is incomplete")
    return masters


def build_homogeneous_controls(
    support: ModuleType,
) -> tuple[list[MasterResult], list[str]]:
    if tuple(support.LENGTHS) != LENGTHS:
        raise ValueError("immutable support lengths differ from frozen protocol")
    for name in ("Profile", "keyed_rng", "log_uniform", "score_table"):
        if not hasattr(support, name):
            raise ValueError(f"immutable support is missing {name}")

    results: list[MasterResult] = []
    digests: list[str] = []
    for preimage in PRIMARY_PREIMAGES:
        master = hashlib.sha256((preimage + HOMOGENEOUS_SUFFIX).encode("ascii")).digest()
        digests.append(master.hex())
        tables: list[tuple[int, ...]] = []
        for profile_index in range(HOMOGENEOUS_PROFILES):
            rng = support.keyed_rng(master, f"negative|profile={profile_index:02d}")
            b = support.log_uniform(rng, *HOMOGENEOUS_BOUNDS)
            profile = support.Profile(
                cliff=-1,
                costs=tuple(Fraction(b) * length for length in LENGTHS),
                events=LENGTHS,
                floor_margin=None,
            )
            table = tuple(support.score_table(profile, SATURATION))
            if best_index(table) != 0:
                raise AssertionError("homogeneous row argmax is not smaller-tie length one")
            tables.append(table)
        result = evaluate_master_score_tables(tables)
        if result.regret != HOMOGENEOUS_EXPECTED_DIFFERENCE:
            raise AssertionError("homogeneous control adaptive-minus-global is nonzero")
        if result.global_length != HOMOGENEOUS_EXPECTED_GLOBAL_LENGTH:
            raise AssertionError("homogeneous control global length is not one")
        if result.adaptive_length_counts[0] != HOMOGENEOUS_PROFILES:
            raise AssertionError("not every homogeneous adaptive choice is length one")
        results.append(result)
    return results, digests


def peak_memory_gb() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    divisor = 1024**3 if sys.platform == "darwin" else 1024**2
    return usage / divisor


def result_record(
    master_index: int, digest: str, result: MasterResult
) -> dict[str, Any]:
    return {
        "adaptive_fill_length_counts": {
            str(length): count
            for length, count in zip(LENGTHS, result.adaptive_length_counts)
        },
        "adaptive_gain_percent_decimal": fixed_12(result.gain_percent),
        "adaptive_gain_percent_exact": fraction_payload(result.gain_percent),
        "adaptive_score_raw": result.adaptive_score,
        "conditional_regret_raw": result.regret,
        "global_fill_length": result.global_length,
        "global_score_raw": result.global_score,
        "master_digest_hex": digest,
        "master_index": master_index,
    }


def write_primary_tsv(
    path: Path, records: Sequence[dict[str, Any]]
) -> None:
    header = [
        "master_index",
        "master_digest_hex",
        "adaptive_score_raw",
        "global_score_raw",
        "conditional_regret_raw",
        "adaptive_gain_percent_numerator",
        "adaptive_gain_percent_denominator",
        "adaptive_gain_percent_decimal",
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
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_homogeneous_tsv(
    path: Path, records: Sequence[dict[str, Any]]
) -> None:
    header = [
        "master_index",
        "master_digest_hex",
        "profiles",
        "adaptive_score_raw",
        "global_score_raw",
        "adaptive_minus_global_raw",
        "global_fill_length",
        "all_adaptive_fill_lengths_one",
    ]
    lines = ["\t".join(header)]
    for record in records:
        counts = record["adaptive_fill_length_counts"]
        lines.append(
            "\t".join(
                [
                    str(record["master_index"]),
                    str(record["master_digest_hex"]),
                    str(HOMOGENEOUS_PROFILES),
                    str(record["adaptive_score_raw"]),
                    str(record["global_score_raw"]),
                    str(record["conditional_regret_raw"]),
                    str(record["global_fill_length"]),
                    str(counts["1"] == HOMOGENEOUS_PROFILES).lower(),
                ]
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=EXPECTED_CONFIG)
    parser.add_argument("--baseline-tables", type=Path, default=EXPECTED_BASELINE_TABLE)
    parser.add_argument("--output-dir", type=Path, default=EXPECTED_OUTPUT_DIR)
    args = parser.parse_args()

    config_path = resolve_exact_repo_path(args.config, EXPECTED_CONFIG, must_exist=True)
    baseline_path = resolve_exact_repo_path(
        args.baseline_tables, EXPECTED_BASELINE_TABLE, must_exist=True
    )
    output_dir = resolve_exact_repo_path(
        args.output_dir, EXPECTED_OUTPUT_DIR, must_exist=True
    )
    support_path = resolve_exact_repo_path(SUPPORT_PATH, SUPPORT_PATH, must_exist=True)
    if file_sha256(config_path) != EXPECTED_CONFIG_SHA256:
        raise ValueError("frozen Phase-4 config hash mismatch")
    if file_sha256(support_path) != EXPECTED_SUPPORT_SHA256:
        raise ValueError("immutable calibration support hash mismatch")

    started = time.perf_counter()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("config must be a JSON object")
    validate_config(config)

    baseline_bytes = baseline_path.read_bytes()
    baseline_hash = hashlib.sha256(baseline_bytes).hexdigest()
    if baseline_hash != EXPECTED_BASELINE_TABLE_SHA256:
        raise ValueError("committed baseline score-table hash mismatch")
    baseline_text = baseline_bytes.decode("utf-8")
    primary_tables = parse_baseline_tables(baseline_text)
    primary_results = [
        evaluate_master_score_tables(tables) for tables in primary_tables
    ]
    primary_digests = [
        hashlib.sha256(preimage.encode("ascii")).hexdigest()
        for preimage in PRIMARY_PREIMAGES
    ]

    support = load_support(support_path)
    homogeneous_results, homogeneous_digests = build_homogeneous_controls(support)
    primary_records = [
        result_record(index, digest, result)
        for index, (digest, result) in enumerate(
            zip(primary_digests, primary_results, strict=True)
        )
    ]
    homogeneous_records = [
        result_record(index, digest, result)
        for index, (digest, result) in enumerate(
            zip(homogeneous_digests, homogeneous_results, strict=True)
        )
    ]

    gains = [result.gain_percent for result in primary_results]
    mean_gain = sum(gains, Fraction(0, 1)) / len(gains)
    minimum_gain = min(gains)
    maximum_gain = max(gains)
    gain_floats = [float(gain) for gain in gains]
    sample_std = statistics.stdev(gain_floats)
    half_width = T_CRITICAL_DF_TWO * sample_std / math.sqrt(len(gains))
    t_low = float(mean_gain) - half_width
    t_high = float(mean_gain) + half_width
    clear_count = sum(gain >= MATERIALITY_THRESHOLD for gain in gains)
    clear_fraction = Fraction(clear_count, len(gains))
    homogeneous_zero_count = sum(result.regret == 0 for result in homogeneous_results)
    homogeneous_one_count = sum(
        result.global_length == 1
        and result.adaptive_length_counts[0] == HOMOGENEOUS_PROFILES
        for result in homogeneous_results
    )
    homogeneous_zero_fraction = Fraction(
        homogeneous_zero_count, len(homogeneous_results)
    )
    homogeneous_one_fraction = Fraction(
        homogeneous_one_count, len(homogeneous_results)
    )
    elapsed = time.perf_counter() - started
    memory_gb = peak_memory_gb()

    summary = {
        "claim_scope": CLAIM_SCOPE,
        "homogeneous_controls": {
            "all_masters_zero_fraction_decimal": fixed_12(
                homogeneous_zero_fraction
            ),
            "all_masters_zero_fraction_exact": fraction_payload(
                homogeneous_zero_fraction
            ),
            "all_rows_and_globals_length_one_fraction_decimal": fixed_12(
                homogeneous_one_fraction
            ),
            "all_rows_and_globals_length_one_fraction_exact": fraction_payload(
                homogeneous_one_fraction
            ),
            "masters": homogeneous_records,
            "profiles_per_master": HOMOGENEOUS_PROFILES,
        },
        "inputs": {
            "baseline_table": {
                "path": EXPECTED_BASELINE_TABLE.as_posix(),
                "sha256": baseline_hash,
            },
            "config": {
                "path": EXPECTED_CONFIG.as_posix(),
                "sha256": EXPECTED_CONFIG_SHA256,
            },
            "immutable_support": {
                "path": SUPPORT_PATH.as_posix(),
                "sha256": EXPECTED_SUPPORT_SHA256,
            },
        },
        "limitations": [
            "Synthetic public profiles do not establish live-model heterogeneity.",
            "The interval is conditional on exactly these three deterministic masters and is not a population claim.",
            "This run does not test learnability, private transfer, Kaggle performance, or any held-out target.",
            "No live-deadline claim is supported.",
        ],
        "primary": {
            "aggregate": {
                "all_masters_clear_materiality_fraction_decimal": fixed_12(
                    clear_fraction
                ),
                "all_masters_clear_materiality_fraction_exact": fraction_payload(
                    clear_fraction
                ),
                "conditional_two_sided_t95_interval": {
                    "critical_value": T_CRITICAL_DF_TWO,
                    "degrees_of_freedom": 2,
                    "label": "conditional descriptive interval over the three fixed public masters; not a population claim",
                    "lower_percent_decimal": format(t_low, ".12f"),
                    "sample_standard_deviation_percent_decimal": format(
                        sample_std, ".12f"
                    ),
                    "upper_percent_decimal": format(t_high, ".12f"),
                },
                "maximum_adaptive_gain_percent_decimal": fixed_12(maximum_gain),
                "maximum_adaptive_gain_percent_exact": fraction_payload(
                    maximum_gain
                ),
                "mean_adaptive_gain_percent_decimal": fixed_12(mean_gain),
                "mean_adaptive_gain_percent_exact": fraction_payload(mean_gain),
                "minimum_adaptive_gain_percent_decimal": fixed_12(minimum_gain),
                "minimum_adaptive_gain_percent_exact": fraction_payload(
                    minimum_gain
                ),
            },
            "core_prediction_confirm_interval_inclusive": [30.0, 50.0],
            "core_prediction_percent": 40.0,
            "materiality_threshold_percent_inclusive": 5.0,
            "masters": primary_records,
            "masters_evaluated": len(primary_results),
            "profiles_evaluated": len(primary_results) * PROFILES_PER_MASTER,
        },
        "resources": {
            "peak_memory_gb": round(memory_gb, 9),
            "runtime_seconds": round(elapsed, 9),
        },
        "run_id": "orf-p4-core",
        "schema_version": "orf-phase4-core-summary-v1",
        "status": "PUBLIC_NON_TARGET_CORE_VALIDATION",
    }

    write_primary_tsv(output_dir / "core-by-master.tsv", primary_records)
    write_homogeneous_tsv(
        output_dir / "homogeneous-by-master.tsv", homogeneous_records
    )
    (output_dir / "core-summary.json").write_text(
        canonical_json(summary), encoding="utf-8"
    )
    (output_dir / "notes.md").write_text(
        "# ORF Phase-4 core run notes\n\n"
        "The core calculation recomputed `G` from the seven committed score columns "
        "and computed `A` by exhaustive per-row argmax, always breaking ties toward "
        "the smaller fill length. No baseline summary or reported `G` entered the "
        "calculation.\n\n"
        "The separately generated homogeneous controls used the frozen immutable "
        "calibration primitives. All controls were asserted before output.\n\n"
        "Deviations: none.\n\n"
        "Scope is public deterministic non-target validation only. Synthetic-profile "
        "results do not establish live heterogeneity, learnability, private transfer, "
        "held-out performance, Kaggle performance, or a live-deadline claim.\n",
        encoding="utf-8",
    )

    metrics = {
        "mean_adaptive_gain_percent": fixed_12(mean_gain),
        "minimum_adaptive_gain_percent": fixed_12(minimum_gain),
        "maximum_adaptive_gain_percent": fixed_12(maximum_gain),
        "all_masters_clear_fraction": fixed_12(clear_fraction),
        "homogeneous_zero_fraction": fixed_12(homogeneous_zero_fraction),
        "homogeneous_length_one_fraction": fixed_12(homogeneous_one_fraction),
        "masters_evaluated": str(len(primary_results)),
        "profiles_evaluated": str(len(primary_results) * PROFILES_PER_MASTER),
        "peak_memory_gb": format(memory_gb, ".9f"),
        "runtime_seconds": format(elapsed, ".9f"),
    }
    for name, value in metrics.items():
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
