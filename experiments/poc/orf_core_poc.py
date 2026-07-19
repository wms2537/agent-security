#!/usr/bin/env python3
"""Deterministic public, non-target Phase-3 ORF mechanics probe."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import resource
import sys
import time
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any


REPO = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO / "experiments" / "poc"
CONFIG_SHA256 = "786ff089cf5d0f1d88a320170ee4634de4ba3fe34d85a9813fbff6ebf02dedf1"


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def decimal_string(value: Fraction, places: int = 12) -> str:
    numerator = Decimal(value.numerator)
    denominator = Decimal(value.denominator)
    quantum = Decimal(1).scaleb(-places)
    return format((numerator / denominator).quantize(quantum), "f")


def resolve_repo_path(path: Path) -> Path:
    resolved = path.resolve() if path.is_absolute() else (REPO / path).resolve()
    if not resolved.is_relative_to(REPO):
        raise AssertionError(f"path leaves repository: {path}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    started = time.perf_counter()

    config_path = resolve_repo_path(args.config)
    config_hash = sha256_file(config_path)
    assert config_hash == CONFIG_SHA256, "unexpected PoC config hash"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert config["contract_version"] == "orf-poc-v1"

    calibration = load_module(
        "orf_support_calibration_immutable",
        OUTPUT_DIR / "orf_support_calibration.py",
    )
    sdk_reference = load_module(
        "orf_v7_contract_reference_immutable",
        OUTPUT_DIR / "orf_v7_contract_reference.py",
    )

    primary = config["primary"]
    assert tuple(primary["lengths"]) == calibration.LENGTHS
    assert primary["weighting"] == "equal"
    assert primary["profile_count"] == len(primary["stratum_indices"]) == 40
    assert primary["replicate_index"] == 0
    assert primary["stratum_indices"] == list(range(40))
    master = hashlib.sha256(primary["master_preimage_ascii"].encode("ascii")).digest()
    all_profiles, _all_floor_margin = calibration.build_profiles(master)
    selected_indices = [
        8 * stratum + primary["replicate_index"]
        for stratum in primary["stratum_indices"]
    ]
    profiles = [all_profiles[index] for index in selected_indices]
    tables = [
        calibration.score_table(profile, primary["saturation"])
        for profile in profiles
    ]
    adaptive, global_score, difference, global_length = calibration.gain_for_design(
        profiles,
        tables,
        primary["weighting"],
    )
    gain = Fraction(100 * difference, global_score)
    selected_floor_margins = [
        profile.floor_margin
        for profile in profiles
        if profile.floor_margin is not None
    ]
    assert selected_floor_margins
    minimum_floor_distance = min(selected_floor_margins)
    assert minimum_floor_distance >= Decimal("1e-60")

    profile_path = OUTPUT_DIR / "poc-profiles.tsv"
    score_fields = [f"score_m{length}" for length in calibration.LENGTHS]
    event_fields = [f"events_m{length}" for length in calibration.LENGTHS]
    fieldnames = [
        "stratum_index",
        "replicate_index",
        "profile_index",
        "cliff",
        "floor_distance",
        *event_fields,
        *score_fields,
    ]
    with profile_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for stratum, profile_index, profile, table in zip(
            primary["stratum_indices"], selected_indices, profiles, tables
        ):
            row: dict[str, Any] = {
                "stratum_index": stratum,
                "replicate_index": primary["replicate_index"],
                "profile_index": profile_index,
                "cliff": profile.cliff,
                "floor_distance": (
                    "NA" if profile.floor_margin is None else str(profile.floor_margin)
                ),
            }
            row.update(
                {
                    f"events_m{length}": event
                    for length, event in zip(calibration.LENGTHS, profile.events)
                }
            )
            row.update(
                {
                    f"score_m{length}": score
                    for length, score in zip(calibration.LENGTHS, table)
                }
            )
            writer.writerow(row)

    negative = config["negative"]
    assert negative["profile_indices"] == list(range(64))
    negative_master = hashlib.sha256(
        negative["master_preimage_ascii"].encode("ascii")
    ).digest()
    negative_profiles = []
    for profile_index in negative["profile_indices"]:
        rng = calibration.keyed_rng(
            negative_master,
            f"negative|profile={profile_index:02d}",
        )
        b = calibration.log_uniform(rng, *negative["b_log_uniform"])
        costs = tuple(Fraction(b) * length for length in calibration.LENGTHS)
        negative_profiles.append(
            calibration.Profile(
                cliff=negative["cliff"],
                costs=costs,
                events=tuple(calibration.LENGTHS),
                floor_margin=None,
            )
        )
    negative_tables = [
        calibration.score_table(profile, negative["saturation"])
        for profile in negative_profiles
    ]
    for table in negative_tables:
        best_index = max(
            range(len(calibration.LENGTHS)),
            key=lambda index: (table[index], -calibration.LENGTHS[index]),
        )
        assert calibration.LENGTHS[best_index] == 1
    neg_adaptive, neg_global, neg_difference, neg_global_length = (
        calibration.gain_for_design(negative_profiles, negative_tables, "equal")
    )
    assert neg_difference == 0
    assert neg_global_length == 1

    fixture_spec = config["sdk_fixtures"]
    fixture_path = resolve_repo_path(Path(fixture_spec["path"]))
    assert sha256_file(fixture_path) == fixture_spec["sha256"]
    fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))
    assert len(fixtures["sdk_cases"]) == fixture_spec["expected_cases"] == 2
    sdk_hashes = sdk_reference.check_sdk_cases(fixtures)
    assert len(sdk_hashes) == len(set(sdk_hashes)) == 2

    runtime_seconds = time.perf_counter() - started
    peak_memory_gb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024**2)
    gain_decimal = decimal_string(gain)
    summary = {
        "schema_version": "orf-public-poc-summary-v1",
        "claim_scope": (
            "deterministic public non-target validation of ORF mechanics and "
            "finite-table conditional regret only"
        ),
        "config": {
            "path": str(config_path.relative_to(REPO)),
            "sha256": config_hash,
        },
        "primary": {
            "master_sha256": master.hex(),
            "profiles_evaluated": len(profiles),
            "adaptive_score_raw": adaptive,
            "global_score_raw": global_score,
            "conditional_regret_raw": difference,
            "adaptive_gain_percent_rational": {
                "numerator": gain.numerator,
                "denominator": gain.denominator,
            },
            "adaptive_gain_percent_decimal": gain_decimal,
            "global_fill_length": global_length,
            "minimum_cliff_floor_distance": str(minimum_floor_distance),
        },
        "homogeneous_negative": {
            "master_sha256": negative_master.hex(),
            "profiles_evaluated": len(negative_profiles),
            "adaptive_score_raw": neg_adaptive,
            "global_score_raw": neg_global,
            "difference_raw": neg_difference,
            "global_fill_length": neg_global_length,
            "all_per_profile_argmax_length": 1,
        },
        "sdk": {
            "cases_verified": len(sdk_hashes),
            "score_cell_hashes": sdk_hashes,
        },
        "runtime_seconds": format(runtime_seconds, ".9f"),
        "peak_memory_gb": format(peak_memory_gb, ".9f"),
    }
    (OUTPUT_DIR / "poc-summary.json").write_bytes(canonical_json(summary))
    (OUTPUT_DIR / "notes.md").write_text(
        "# ORF public non-target PoC notes\n\n"
        "Implemented the frozen `orf-poc-v1` design as a thin deterministic wrapper "
        "around the immutable calibration and SDK reference functions. Exactly one "
        "replicate from each of 40 fixed strata entered the primary metric; the other "
        "profiles constructed internally by `build_profiles` were excluded. The "
        "homogeneous negative and two preserved SDK fixtures were asserted before any "
        "metric was emitted.\n\n"
        "Deviations: none.\n\n"
        "This run validates public mechanics and finite-table conditional regret only. "
        "It is not evidence of live-model prevalence, learnability, private transfer, "
        "Kaggle performance, or the unexecuted beacon-held-out v9 claim.\n",
        encoding="utf-8",
    )

    print(f"adaptive_gain_percent: {gain_decimal}")
    print(f"conditional_regret_raw: {difference}")
    print(f"global_score_raw: {global_score}")
    print(f"adaptive_score_raw: {adaptive}")
    print(f"global_fill_length: {global_length}")
    print(f"homogeneous_difference_raw: {neg_difference}")
    print(f"homogeneous_global_fill_length: {neg_global_length}")
    print(f"sdk_cases_verified: {len(sdk_hashes)}")
    print(f"profiles_evaluated: {len(profiles)}")
    print(f"minimum_cliff_floor_distance: {minimum_floor_distance}")
    print(f"peak_memory_gb: {peak_memory_gb:.9f}")
    print(f"runtime_seconds: {runtime_seconds:.9f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
