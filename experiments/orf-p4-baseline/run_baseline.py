#!/usr/bin/env python3
"""Run the preregistered public non-target ORF Phase-4 global baseline."""

from __future__ import annotations

import argparse
import importlib.util
import json
import resource
import sys
import time
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from types import ModuleType
from typing import Sequence


ROOT = Path("/home/soh/agent-security")
OUTPUT_DIR = Path("experiments/orf-p4-baseline")
EXPECTED_CONFIG = Path("experiments/configs/orf-phase4-v1.json")
SUPPORT_PATH = Path("experiments/poc/orf_support_calibration.py")
LENGTHS = (1, 2, 4, 8, 16, 24, 32)
B_GEN = Fraction(9000, 1)
B_REP = Fraction(8100, 1)
CANDIDATE_CAP = 2000
SATURATION = 200_000
EXPECTED_PREIMAGES = (
    "orf-public-phase4-v1|master|000",
    "orf-public-phase4-v1|master|001",
    "orf-public-phase4-v1|master|002",
)
EXPECTED_IMMUTABLE_PATHS = (
    "experiments/configs/evaluation-contract.md",
    "experiments/configs/orf-phase4-v1.json",
    "experiments/poc/orf_support_calibration.py",
    "experiments/poc/orf_v7_contract_reference.py",
    "experiments/fixtures/orf-heldout-v7-golden-fixtures.json",
    "comp/sdk/aicomp_sdk/core/cells.py",
    "comp/sdk/aicomp_sdk/core/predicates.py",
    "comp/sdk/aicomp_sdk/scoring.py",
)


def canonical_json(value: object) -> str:
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


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def load_support(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("orf_phase4_immutable_support", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load immutable support module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ceil_nonnegative(value: Fraction) -> int:
    if value < 0:
        raise ValueError("ceil_nonnegative requires a nonnegative Fraction")
    return (value.numerator + value.denominator - 1) // value.denominator


def independent_score_table(
    costs: Sequence[Fraction], events: Sequence[int]
) -> tuple[int, ...]:
    """Exact frozen score formula, independent of immutable score_table()."""
    if len(costs) != len(LENGTHS) or len(events) != len(LENGTHS):
        raise ValueError("profile does not contain exactly seven legal actions")
    if any(cost <= 0 for cost in costs):
        raise ValueError("all costs must be positive")
    if any(event < 0 for event in events):
        raise ValueError("all event counts must be nonnegative")

    generation_probe = sum(costs, Fraction(0, 1))
    positive_indices = tuple(i for i, event in enumerate(events) if event > 0)
    returned_probe = len(positive_indices)
    replay_probe = sum((costs[i] for i in positive_indices), Fraction(0, 1))
    raw_probe = sum(16 * events[i] + 2 for i in positive_indices)

    recomputed: list[int] = []
    for index in range(len(LENGTHS)):
        event = events[index]
        if event == 0:
            recomputed.append(raw_probe)
            continue

        candidate_raw = 16 * event + 2
        remaining_raw = SATURATION - raw_probe
        saturation_capacity = (
            0
            if remaining_raw <= 0
            else ceil_nonnegative(Fraction(remaining_raw, candidate_raw))
        )
        generation_capacity = int((B_GEN - generation_probe) // costs[index])
        replay_capacity = int((B_REP - replay_probe) // costs[index])
        capacity = max(
            0,
            min(
                CANDIDATE_CAP - returned_probe,
                generation_capacity,
                replay_capacity,
                saturation_capacity,
            ),
        )
        recomputed.append(min(SATURATION, raw_probe + capacity * candidate_raw))
    return tuple(recomputed)


def fixed_12(value: Fraction) -> str:
    sign = "-" if value < 0 else ""
    value = abs(value)
    scaled_numerator = value.numerator * 10**12
    quotient, remainder = divmod(scaled_numerator, value.denominator)
    if remainder * 2 >= value.denominator:
        quotient += 1
    whole, fractional = divmod(quotient, 10**12)
    return f"{sign}{whole}.{fractional:012d}"


def validate_config(config: dict[str, object]) -> None:
    primary = config.get("primary")
    if not isinstance(primary, dict):
        raise ValueError("config primary block is missing")
    required = {
        "contract_version": "orf-phase4-public-nontarget-v1",
        "claim_scope": "public deterministic non-target validation only",
        "master_derivation": "SHA256(ASCII preimage)",
        "lengths": list(LENGTHS),
        "primary_master_preimages_ascii": list(EXPECTED_PREIMAGES),
        "immutable_paths": list(EXPECTED_IMMUTABLE_PATHS),
    }
    for key, expected in required.items():
        if config.get(key) != expected:
            raise ValueError(f"unexpected config value for {key}")
    primary_required = {
        "profiles_per_master": 320,
        "strata": 40,
        "replicates_per_stratum": 8,
        "saturation": SATURATION,
        "weighting": "equal",
        "baseline_policy": "PROBE_GLOBAL: one exhaustively selected fill length per master",
    }
    for key, expected in primary_required.items():
        if primary.get(key) != expected:
            raise ValueError(f"unexpected primary config value for {key}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    if Path.cwd().resolve() != ROOT:
        raise RuntimeError(f"execution root must be {ROOT}")
    config_path = Path(args.config)
    if config_path != EXPECTED_CONFIG:
        raise ValueError(f"config path must be {EXPECTED_CONFIG}")

    started = time.perf_counter()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    validate_config(config)
    support = load_support(SUPPORT_PATH)
    if tuple(support.LENGTHS) != LENGTHS:
        raise ValueError("immutable support length set differs from frozen config")

    immutable_hashes = {
        path: file_sha256(Path(path)) for path in EXPECTED_IMMUTABLE_PATHS
    }
    config_hash = file_sha256(config_path)
    if immutable_hashes[config_path.as_posix()] != config_hash:
        raise AssertionError("config hash mismatch within immutable input set")

    table_header = [
        "master_index",
        "master_digest_hex",
        "profile_index",
        "stratum_index",
        "replicate_index",
        "cliff",
        "minimum_cliff_floor_distance",
    ]
    for length in LENGTHS:
        table_header.extend(
            [f"cost_numerator_m{length}", f"cost_denominator_m{length}", f"events_m{length}"]
        )
    table_header.extend(f"score_m{length}" for length in LENGTHS)
    table_lines = ["\t".join(table_header)]
    aggregate_lines = [
        "master_index\tmaster_digest_hex\tlength\ttotal_score\tselected_global_length\tis_selected"
    ]
    master_summaries: list[dict[str, object]] = []
    profile_sections: list[str] = []
    total_pairs = 0
    total_matches = 0

    for master_index, preimage in enumerate(EXPECTED_PREIMAGES):
        master = sha256(preimage.encode("ascii")).digest()
        profiles, master_floor_distance = support.build_profiles(master)
        if len(profiles) != 320:
            raise ValueError(f"master {master_index} did not produce 320 profiles")
        totals = [0] * len(LENGTHS)
        master_matches = 0
        for profile_index, profile in enumerate(profiles):
            stratum_index, replicate_index = divmod(profile_index, 8)
            if stratum_index >= 40 or replicate_index >= 8:
                raise AssertionError("profile ordering violates frozen crossed design")
            reference = tuple(support.score_table(profile, SATURATION))
            independent = independent_score_table(profile.costs, profile.events)
            if reference != independent:
                raise AssertionError(
                    f"mechanical mismatch at master={master_index}, profile={profile_index}"
                )
            master_matches += len(LENGTHS)
            total_matches += len(LENGTHS)
            total_pairs += len(LENGTHS)
            for action_index, score in enumerate(reference):
                totals[action_index] += score

            row = [
                str(master_index),
                master.hex(),
                str(profile_index),
                str(stratum_index),
                str(replicate_index),
                str(profile.cliff),
                "" if profile.floor_margin is None else str(profile.floor_margin),
            ]
            for cost, event in zip(profile.costs, profile.events):
                row.extend([str(cost.numerator), str(cost.denominator), str(event)])
            row.extend(str(score) for score in reference)
            table_lines.append("\t".join(row))

        best_index = max(
            range(len(LENGTHS)), key=lambda i: (totals[i], -LENGTHS[i])
        )
        global_length = LENGTHS[best_index]
        global_score = totals[best_index]
        ranked = sorted(
            zip(LENGTHS, totals), key=lambda item: (-item[1], item[0])
        )
        top_second_gap = ranked[0][1] - ranked[1][1]
        for length, total in zip(LENGTHS, totals):
            aggregate_lines.append(
                "\t".join(
                    [
                        str(master_index),
                        master.hex(),
                        str(length),
                        str(total),
                        str(global_length),
                        str(length == global_length).lower(),
                    ]
                )
            )
        master_summaries.append(
            {
                "by_length_totals": {
                    str(length): total for length, total in zip(LENGTHS, totals)
                },
                "global_length": global_length,
                "global_score_raw": global_score,
                "master_digest_hex": master.hex(),
                "master_index": master_index,
                "minimum_cliff_floor_distance": str(master_floor_distance),
                "reference_matches": master_matches,
                "reference_pairs": 320 * len(LENGTHS),
            }
        )
        profile_sections.extend(
            [
                f"## Master {master_index}",
                "",
                f"Digest: `{master.hex()}`",
                "",
                "| Length | Aggregate raw score |",
                "|---:|---:|",
                *(f"| {length} | {total} |" for length, total in zip(LENGTHS, totals)),
                "",
                f"Selected global length: {global_length}",
                "",
                f"Top-vs-second aggregate gap: {top_second_gap}",
                "",
            ]
        )

    if len(table_lines) != 1 + 3 * 320:
        raise AssertionError("score table row count is not 960")
    if len(aggregate_lines) != 1 + 3 * len(LENGTHS):
        raise AssertionError("aggregate table row count is not 21")
    if total_pairs != 3 * 320 * len(LENGTHS) or total_matches != total_pairs:
        raise AssertionError("mechanical pair count or equality check failed")

    global_scores = [int(item["global_score_raw"]) for item in master_summaries]
    m16_count = sum(item["global_length"] == 16 for item in master_summaries)
    elapsed = time.perf_counter() - started
    peak_memory_gb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024**2)
    mean_global = Fraction(sum(global_scores), len(global_scores))
    m16_fraction = Fraction(m16_count, len(master_summaries))
    mechanical_fraction = Fraction(total_matches, total_pairs)
    summary = {
        "claim_scope": config["claim_scope"],
        "config_path": config_path.as_posix(),
        "config_sha256": config_hash,
        "global_length_16_fraction": fixed_12(m16_fraction),
        "immutable_input_sha256": immutable_hashes,
        "masters": master_summaries,
        "masters_evaluated": len(master_summaries),
        "max_global_score_raw": max(global_scores),
        "mean_global_score_raw": fixed_12(mean_global),
        "mean_global_score_raw_exact": {
            "denominator": mean_global.denominator,
            "numerator": mean_global.numerator,
        },
        "mechanical_reference_match_fraction": fixed_12(mechanical_fraction),
        "mechanical_reference_matches": total_matches,
        "mechanical_reference_pairs": total_pairs,
        "min_global_score_raw": min(global_scores),
        "peak_memory_gb": round(peak_memory_gb, 9),
        "profiles_evaluated": 3 * 320,
        "run_id": "orf-p4-baseline",
        "runtime_seconds": round(elapsed, 9),
        "status": "PUBLIC_NON_TARGET_BASELINE_VALIDATION",
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "score-tables.tsv").write_text(
        "\n".join(table_lines) + "\n", encoding="utf-8"
    )
    (OUTPUT_DIR / "aggregate-by-length.tsv").write_text(
        "\n".join(aggregate_lines) + "\n", encoding="utf-8"
    )
    (OUTPUT_DIR / "baseline-summary.json").write_text(
        canonical_json(summary), encoding="utf-8"
    )
    (OUTPUT_DIR / "profile.md").write_text(
        "\n".join(
            [
                "# ORF Phase-4 public baseline profile",
                "",
                "This profile reports only aggregate `PROBE_GLOBAL` baseline scores for the",
                "three preregistered public non-target masters. It contains no adaptive",
                "aggregate or per-profile preferred-action summary.",
                "",
                *profile_sections,
            ]
        ),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "notes.md").write_text(
        "\n".join(
            [
                "# ORF Phase-4 baseline notes",
                "",
                "- Scope: public deterministic non-target validation only.",
                "- Policy: exhaustive `PROBE_GLOBAL` choice over all seven legal lengths,",
                "  independently for each master, with smaller length breaking ties.",
                "- Mechanical check: every immutable score-table result exactly equaled a",
                "  separately implemented exact recomputation from profile costs and events.",
                "- These constructed profiles do not establish live-target heterogeneity,",
                "  learnability, replay-deadline safety, private transfer, or Kaggle performance.",
                "- No network, beacon, held-out target, or external service was used.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"mean_global_score_raw: {fixed_12(mean_global)}")
    print(f"min_global_score_raw: {min(global_scores)}")
    print(f"max_global_score_raw: {max(global_scores)}")
    print(f"global_length_16_fraction: {fixed_12(m16_fraction)}")
    print(f"mechanical_reference_match_fraction: {fixed_12(mechanical_fraction)}")
    print(f"masters_evaluated: {len(master_summaries)}")
    print("profiles_evaluated: 960")
    print(f"peak_memory_gb: {peak_memory_gb:.9f}")
    print(f"runtime_seconds: {elapsed:.9f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
