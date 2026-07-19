#!/usr/bin/env python3
"""Run the preregistered ORF Phase-4 one-at-a-time attribution batch."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import resource
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Sequence


REPO = Path(__file__).resolve().parents[2]
RUNNER_PATH = Path("experiments/orf-p4-ablations/run_ablations.py")
BUNDLE_PATH = Path("experiments/orf_bundle.py")
CONFIG_PATH = Path("experiments/configs/orf-phase4-v1.json")
SUPPORT_PATH = Path("experiments/poc/orf_support_calibration.py")
BASELINE_PATH = Path("experiments/orf-p4-baseline/score-tables.tsv")
CORE_RUNNER_PATH = Path("experiments/orf-p4-core/run_core.py")
CORE_COMPLETE_PATH = Path("experiments/runs/orf-p4-core-v1/COMPLETE.json")
CORE_SUMMARY_PATH = Path("experiments/runs/orf-p4-core-v1/core-summary.json")
RUNS_PARENT = Path("experiments/runs")
ATTEMPT_PATH = Path("experiments/runs/orf-p4-ablations-v1")
CANONICAL_COMMAND = (
    "comp/.venv/bin/python -I experiments/orf-p4-ablations/run_ablations.py "
    "--config experiments/configs/orf-phase4-v1.json "
    "--baseline-tables experiments/orf-p4-baseline/score-tables.tsv "
    "--attempt-dir experiments/runs/orf-p4-ablations-v1"
)
EXPECTED_HASHES = {
    BUNDLE_PATH: "8c4b9cd3bf4ea0053e96a851b88a60bb6a92972b2e7f8a6e3a4c6bd91550aedd",
    CONFIG_PATH: "e3ebe822094c91d6b6e83de6bc55324e43301b74df9a6e3bc3ee3e932b0ba748",
    SUPPORT_PATH: "fdc68ce08923be8d693155bb2641841a3a706164ebcb9d05e6a330a1d8c67fe9",
    BASELINE_PATH: "331e8b5e16b42d8781df68fd49aa9cd83a4d77c8f5ec0ab9de15e09137e59cbf",
    CORE_RUNNER_PATH: "41aa108f5f18c60a7072666d32fe010b447a1617c7c5938a1f54573b01e74715",
    CORE_COMPLETE_PATH: "a6630cde76050ed5c6a227bf79cc809d12ddcad14a9e67551ebd37123d3a2809",
    CORE_SUMMARY_PATH: "93e2030dbc1718947208ae041b5884046e0eb078a61815dee290d75946e77d88",
}
OUTPUT_ARTIFACTS = (
    "ablation-score-tables.tsv",
    "ablation-by-master.tsv",
    "ablation-summary.json",
    "notes.md",
    "run.log",
)
LENGTHS = (1, 2, 4, 8, 16, 24, 32)
PRIMARY_PREIMAGES = tuple(
    f"orf-public-phase4-v1|master|{index:03d}" for index in range(3)
)
PROFILES_PER_MASTER = 320
B_GEN = Fraction(9000, 1)
B_REP = Fraction(8100, 1)
CANDIDATE_CAP = 2000
DEFAULT_SATURATION = 200_000
UNSATURATED = 10**18
ABLATION_IDS = (
    "no_cliff",
    "no_curvature",
    "no_reset",
    "no_novelty",
    "unsaturated",
)
PREDICTIONS = {
    "no_cliff": Fraction(7, 1),
    "no_curvature": Fraction(35, 1),
    "no_reset": Fraction(22, 1),
    "no_novelty": Fraction(40, 1),
    "unsaturated": Fraction(44, 1),
}
EXPECTED_ABLATIONS = [
    {
        "id": "no_cliff",
        "change": "Replace every primary profile's event vector with e(m)=m; retain realized costs and all other mechanics.",
    },
    {
        "id": "no_curvature",
        "change": "Set every realized d fraction to zero and recompute costs a+b*m; retain events and all other mechanics.",
    },
    {
        "id": "no_reset",
        "change": "Set every realized a fraction to zero and recompute costs b*m+d*m^2; retain events and all other mechanics.",
    },
    {
        "id": "no_novelty",
        "change": "Replace each positive singleton raw q=16e+2 with q=16e; retain probe/fill costs, events, caps, and policies.",
    },
    {
        "id": "unsaturated",
        "change": "Replace H=200000 with H=1000000000000000000; retain all other primary mechanics.",
    },
]


@dataclass(frozen=True)
class ProfileRow:
    master_index: int
    master_digest_hex: str
    profile_index: int
    stratum_index: int
    replicate_index: int
    cliff: int
    costs: tuple[Fraction, ...]
    events: tuple[int, ...]
    default_scores: tuple[int, ...]


@dataclass(frozen=True)
class TransformedProfile:
    costs: tuple[Fraction, ...]
    events: tuple[int, ...]
    saturation: int
    novelty_offset: int


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


def parse_nonnegative(raw: str, field: str) -> int:
    if not raw or any(character < "0" or character > "9" for character in raw):
        raise ValueError(f"{field} must be a canonical nonnegative integer")
    return int(raw)


def parse_positive(raw: str, field: str) -> int:
    value = parse_nonnegative(raw, field)
    if value <= 0:
        raise ValueError(f"{field} must be positive")
    return value


def ceil_nonnegative(value: Fraction) -> int:
    if value < 0:
        raise ValueError("ceil_nonnegative requires a nonnegative value")
    return (value.numerator + value.denominator - 1) // value.denominator


def score_table(
    costs: Sequence[Fraction],
    events: Sequence[int],
    *,
    saturation: int,
    novelty_offset: int,
) -> tuple[int, ...]:
    if len(costs) != len(LENGTHS) or len(events) != len(LENGTHS):
        raise ValueError("one exact cost and event count is required per action")
    if any(cost <= 0 for cost in costs):
        raise ValueError("all costs must be positive")
    if any(type(event) is not int or event < 0 for event in events):
        raise ValueError("events must be nonnegative integers")
    if saturation <= 0 or novelty_offset not in (0, 2):
        raise ValueError("unexpected scoring constants")

    generation_probe = sum(costs, Fraction())
    positive = [index for index, event in enumerate(events) if event > 0]
    returned_probe = len(positive)
    replay_probe = sum((costs[index] for index in positive), Fraction())
    raw_probe = sum(16 * events[index] + novelty_offset for index in positive)
    scores: list[int] = []
    for index, event in enumerate(events):
        if event == 0:
            scores.append(raw_probe)
            continue
        candidate_raw = 16 * event + novelty_offset
        if candidate_raw <= 0:
            raise AssertionError("positive event must produce positive raw score")
        saturation_capacity = (
            0
            if raw_probe >= saturation
            else ceil_nonnegative(Fraction(saturation - raw_probe, candidate_raw))
        )
        capacity = max(
            0,
            min(
                CANDIDATE_CAP - returned_probe,
                int((B_GEN - generation_probe) // costs[index]),
                int((B_REP - replay_probe) // costs[index]),
                saturation_capacity,
            ),
        )
        scores.append(min(saturation, raw_probe + capacity * candidate_raw))
    return tuple(scores)


def recover_coefficients(costs: Sequence[Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    if len(costs) != len(LENGTHS):
        raise ValueError("seven costs are required")
    c1, c2, c4 = costs[0], costs[1], costs[2]
    curvature = (c4 - 3 * c2 + 2 * c1) / 6
    linear = c2 - c1 - 3 * curvature
    reset = c1 - linear - curvature
    if min(reset, linear, curvature) < 0:
        raise ValueError("recovered coefficients must be nonnegative")
    reconstructed = tuple(
        reset + linear * length + curvature * length * length
        for length in LENGTHS
    )
    if reconstructed != tuple(costs):
        raise ValueError("costs do not follow the exact quadratic protocol")
    return reset, linear, curvature


def transform_profile(profile: ProfileRow, ablation: str) -> TransformedProfile:
    if ablation not in ABLATION_IDS:
        raise ValueError(f"unknown ablation: {ablation}")
    reset, linear, curvature = recover_coefficients(profile.costs)
    costs = profile.costs
    events = profile.events
    saturation = DEFAULT_SATURATION
    novelty_offset = 2
    if ablation == "no_cliff":
        events = LENGTHS
    elif ablation == "no_curvature":
        costs = tuple(reset + linear * length for length in LENGTHS)
    elif ablation == "no_reset":
        costs = tuple(
            linear * length + curvature * length * length for length in LENGTHS
        )
    elif ablation == "no_novelty":
        novelty_offset = 0
    elif ablation == "unsaturated":
        saturation = UNSATURATED
    return TransformedProfile(tuple(costs), tuple(events), saturation, novelty_offset)


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


def parse_profiles(text: str) -> list[list[ProfileRow]]:
    reader = csv.reader(io.StringIO(text), delimiter="\t", strict=True)
    try:
        header = next(reader)
    except StopIteration as exc:
        raise ValueError("baseline table is empty") from exc
    if header != baseline_header():
        raise ValueError("baseline schema differs from the frozen protocol")
    masters: list[list[ProfileRow]] = [[] for _ in PRIMARY_PREIMAGES]
    expected_rows = len(PRIMARY_PREIMAGES) * PROFILES_PER_MASTER
    observed = 0
    for observed, row in enumerate(reader, start=1):
        if observed > expected_rows or len(row) != len(header):
            raise ValueError("baseline row count or width exceeds the protocol")
        master_index = (observed - 1) // PROFILES_PER_MASTER
        profile_index = (observed - 1) % PROFILES_PER_MASTER
        stratum_index, replicate_index = divmod(profile_index, 8)
        expected_exact = {
            "master_index": master_index,
            "profile_index": profile_index,
            "stratum_index": stratum_index,
            "replicate_index": replicate_index,
        }
        for field, expected in expected_exact.items():
            if parse_nonnegative(row[header.index(field)], field) != expected:
                raise ValueError(f"baseline {field} sequence differs from protocol")
        digest = hashlib.sha256(
            PRIMARY_PREIMAGES[master_index].encode("ascii")
        ).hexdigest()
        if row[header.index("master_digest_hex")] != digest:
            raise ValueError("baseline master digest mismatch")
        cliff_raw = row[header.index("cliff")]
        if cliff_raw not in {"-1", "4", "8", "16", "24"}:
            raise ValueError("baseline cliff is outside the frozen set")
        costs = tuple(
            Fraction(
                parse_nonnegative(
                    row[header.index(f"cost_numerator_m{length}")],
                    f"cost_numerator_m{length}",
                ),
                parse_positive(
                    row[header.index(f"cost_denominator_m{length}")],
                    f"cost_denominator_m{length}",
                ),
            )
            for length in LENGTHS
        )
        events = tuple(
            parse_nonnegative(
                row[header.index(f"events_m{length}")], f"events_m{length}"
            )
            for length in LENGTHS
        )
        if any(event > length for event, length in zip(events, LENGTHS)):
            raise ValueError("baseline event count exceeds its action length")
        default_scores = tuple(
            parse_nonnegative(
                row[header.index(f"score_m{length}")], f"score_m{length}"
            )
            for length in LENGTHS
        )
        if score_table(
            costs,
            events,
            saturation=DEFAULT_SATURATION,
            novelty_offset=2,
        ) != default_scores:
            raise ValueError("baseline default score does not reproduce exactly")
        recover_coefficients(costs)
        masters[master_index].append(
            ProfileRow(
                master_index,
                digest,
                profile_index,
                stratum_index,
                replicate_index,
                int(cliff_raw),
                costs,
                events,
                default_scores,
            )
        )
    if observed != expected_rows or any(
        len(master) != PROFILES_PER_MASTER for master in masters
    ):
        raise ValueError("baseline must contain exactly three complete masters")
    return masters


def fraction_payload(value: Fraction) -> dict[str, int]:
    return {"denominator": value.denominator, "numerator": value.numerator}


def peak_memory_gb() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    divisor = 1024**3 if sys.platform == "darwin" else 1024**2
    return usage / divisor


def score_table_header() -> list[str]:
    header = [
        "ablation",
        "master_index",
        "master_digest_hex",
        "profile_index",
        "stratum_index",
        "replicate_index",
        "original_cliff",
        "saturation",
        "novelty_offset",
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
    ablation: str,
    profile: ProfileRow,
    transformed: TransformedProfile,
    scores: Sequence[int],
) -> str:
    row = [
        ablation,
        str(profile.master_index),
        profile.master_digest_hex,
        str(profile.profile_index),
        str(profile.stratum_index),
        str(profile.replicate_index),
        str(profile.cliff),
        str(transformed.saturation),
        str(transformed.novelty_offset),
    ]
    for cost, event, score in zip(transformed.costs, transformed.events, scores):
        row.extend(
            [str(cost.numerator), str(cost.denominator), str(event), str(score)]
        )
    return "\t".join(row)


def master_record(
    core: ModuleType,
    *,
    ablation: str,
    master_index: int,
    digest: str,
    result: Any,
    reference: Any,
) -> dict[str, Any]:
    delta = result.gain_percent - reference.gain_percent
    return {
        "ablation": ablation,
        "adaptive_fill_length_counts": {
            str(length): count
            for length, count in zip(LENGTHS, result.adaptive_length_counts)
        },
        "adaptive_gain_percent_decimal": core.fixed_12(result.gain_percent),
        "adaptive_gain_percent_exact": fraction_payload(result.gain_percent),
        "adaptive_score_raw": result.adaptive_score,
        "conditional_regret_raw": result.regret,
        "delta_vs_core_percentage_points_decimal": core.fixed_12(delta),
        "delta_vs_core_percentage_points_exact": fraction_payload(delta),
        "global_fill_length": result.global_length,
        "global_score_raw": result.global_score,
        "master_digest_hex": digest,
        "master_index": master_index,
        "reference_core_gain_percent_decimal": core.fixed_12(
            reference.gain_percent
        ),
    }


def render_master_table(records: Sequence[dict[str, Any]]) -> str:
    header = [
        "ablation",
        "master_index",
        "master_digest_hex",
        "adaptive_score_raw",
        "global_score_raw",
        "conditional_regret_raw",
        "gain_numerator",
        "gain_denominator",
        "gain_percent_decimal",
        "global_fill_length",
        "adaptive_fill_length_counts_json",
        "reference_core_gain_percent_decimal",
        "delta_numerator",
        "delta_denominator",
        "delta_percentage_points_decimal",
    ]
    lines = ["\t".join(header)]
    for record in records:
        gain = record["adaptive_gain_percent_exact"]
        delta = record["delta_vs_core_percentage_points_exact"]
        lines.append(
            "\t".join(
                [
                    str(record["ablation"]),
                    str(record["master_index"]),
                    str(record["master_digest_hex"]),
                    str(record["adaptive_score_raw"]),
                    str(record["global_score_raw"]),
                    str(record["conditional_regret_raw"]),
                    str(gain["numerator"]),
                    str(gain["denominator"]),
                    str(record["adaptive_gain_percent_decimal"]),
                    str(record["global_fill_length"]),
                    json.dumps(
                        record["adaptive_fill_length_counts"],
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                    str(record["reference_core_gain_percent_decimal"]),
                    str(delta["numerator"]),
                    str(delta["denominator"]),
                    str(record["delta_vs_core_percentage_points_decimal"]),
                ]
            )
        )
    return "\n".join(lines) + "\n"


def validate_core_evidence(core: ModuleType, references: Sequence[Any]) -> Fraction:
    summary = json.loads((REPO / CORE_SUMMARY_PATH).read_text(encoding="utf-8"))
    records = summary["primary"]["masters"]
    if len(records) != len(references):
        raise ValueError("committed core master count mismatch")
    for index, (record, reference) in enumerate(zip(records, references)):
        exact = record["adaptive_gain_percent_exact"]
        if (
            record["master_index"] != index
            or record["adaptive_score_raw"] != reference.adaptive_score
            or record["global_score_raw"] != reference.global_score
            or record["conditional_regret_raw"] != reference.regret
            or Fraction(exact["numerator"], exact["denominator"])
            != reference.gain_percent
        ):
            raise ValueError("committed core evidence differs from recomputation")
    mean = sum((reference.gain_percent for reference in references), Fraction()) / len(
        references
    )
    summary_exact = summary["primary"]["aggregate"][
        "mean_adaptive_gain_percent_exact"
    ]
    if Fraction(summary_exact["numerator"], summary_exact["denominator"]) != mean:
        raise ValueError("committed core mean differs from recomputation")
    return mean


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
    if args.config != CONFIG_PATH or args.baseline_tables != BASELINE_PATH:
        raise ValueError("input paths differ from the preregistration")
    if args.attempt_dir != ATTEMPT_PATH:
        raise ValueError("attempt identity differs from the preregistration")

    for relative, expected_hash in EXPECTED_HASHES.items():
        path = REPO / relative
        if path.is_symlink() or not path.is_file() or file_sha256(path) != expected_hash:
            raise ValueError(f"frozen binding mismatch: {relative}")
    bundle = load_module(REPO / BUNDLE_PATH, "orf_p4_ablation_bundle")
    core = load_module(REPO / CORE_RUNNER_PATH, "orf_p4_ablation_core")
    binding_paths = (
        RUNNER_PATH,
        BUNDLE_PATH,
        CONFIG_PATH,
        SUPPORT_PATH,
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
        if config.get("ablations") != EXPECTED_ABLATIONS:
            raise ValueError("ablation config differs from the frozen protocol")
        masters = parse_profiles((REPO / BASELINE_PATH).read_text(encoding="utf-8"))
        references = [
            core.evaluate_master_score_tables(
                [profile.default_scores for profile in profiles]
            )
            for profiles in masters
        ]
        reference_mean = validate_core_evidence(core, references)

        score_lines = ["\t".join(score_table_header())]
        master_records: list[dict[str, Any]] = []
        summaries: dict[str, dict[str, Any]] = {}
        for ablation in ABLATION_IDS:
            ablation_results: list[Any] = []
            for master_index, profiles in enumerate(masters):
                tables: list[tuple[int, ...]] = []
                for profile in profiles:
                    transformed = transform_profile(profile, ablation)
                    scores = score_table(
                        transformed.costs,
                        transformed.events,
                        saturation=transformed.saturation,
                        novelty_offset=transformed.novelty_offset,
                    )
                    tables.append(scores)
                    score_lines.append(
                        render_score_row(ablation, profile, transformed, scores)
                    )
                result = core.evaluate_master_score_tables(tables)
                ablation_results.append(result)
                master_records.append(
                    master_record(
                        core,
                        ablation=ablation,
                        master_index=master_index,
                        digest=profiles[0].master_digest_hex,
                        result=result,
                        reference=references[master_index],
                    )
                )
            gains = [result.gain_percent for result in ablation_results]
            mean_gain = sum(gains, Fraction()) / len(gains)
            clear_fraction = Fraction(sum(gain >= 5 for gain in gains), len(gains))
            summaries[ablation] = {
                "all_masters_clear_fraction_decimal": core.fixed_12(clear_fraction),
                "all_masters_clear_fraction_exact": fraction_payload(clear_fraction),
                "delta_vs_core_mean_percentage_points_decimal": core.fixed_12(
                    mean_gain - reference_mean
                ),
                "delta_vs_core_mean_percentage_points_exact": fraction_payload(
                    mean_gain - reference_mean
                ),
                "maximum_gain_percent_decimal": core.fixed_12(max(gains)),
                "mean_gain_percent_decimal": core.fixed_12(mean_gain),
                "mean_gain_percent_exact": fraction_payload(mean_gain),
                "minimum_gain_percent_decimal": core.fixed_12(min(gains)),
                "predicted_mean_gain_percent": int(PREDICTIONS[ablation]),
            }
        if len(score_lines) != 1 + len(ABLATION_IDS) * 3 * PROFILES_PER_MASTER:
            raise AssertionError("ablation score table row count mismatch")
        if len(master_records) != len(ABLATION_IDS) * 3:
            raise AssertionError("ablation master record count mismatch")

        elapsed = time.perf_counter() - started
        memory = peak_memory_gb()
        summary = {
            "ablations": summaries,
            "claim_scope": "public deterministic non-target attribution only",
            "inputs": {
                path.as_posix(): digest for path, digest in EXPECTED_HASHES.items()
            },
            "limitations": [
                "Attribution is conditional on three fixed public synthetic masters.",
                "One-at-a-time effects need not add because mechanisms interact.",
                "No live, held-out, learnability, deadline, private-transfer, or Kaggle claim is supported.",
            ],
            "master_records": master_records,
            "predictions": {
                name: int(value) for name, value in PREDICTIONS.items()
            },
            "reference_core_mean_gain_percent_decimal": core.fixed_12(reference_mean),
            "reference_core_mean_gain_percent_exact": fraction_payload(reference_mean),
            "resources": {
                "peak_memory_gb": round(memory, 9),
                "runtime_seconds": round(elapsed, 9),
            },
            "run_id": "orf-p4-ablations",
            "schema_version": "orf-phase4-ablations-v1",
            "status": "PUBLIC_NON_TARGET_ATTRIBUTION",
        }
        metrics = {
            f"{ablation}_mean_gain_percent": summaries[ablation][
                "mean_gain_percent_decimal"
            ]
            for ablation in ABLATION_IDS
        }
        metrics.update(
            {
                "reference_core_mean_gain_percent": core.fixed_12(reference_mean),
                "ablation_master_cells": str(len(master_records)),
                "ablation_profile_rows": str(len(score_lines) - 1),
                "peak_memory_gb": f"{memory:.9f}",
                "runtime_seconds": f"{elapsed:.9f}",
            }
        )
        notes = (
            "# ORF Phase-4 ablation notes\n\n"
            "Each condition changes exactly the mechanism named in the frozen config. "
            "The reference is recomputed from the committed default score table and "
            "checked against the committed reviewed core summary.\n\n"
            "All arithmetic is exact until fixed-decimal rendering. There were no "
            "deviations or retries. Scope is public deterministic non-target "
            "attribution only; interactions make one-at-a-time effects non-additive.\n"
        )
        writer.write_text("ablation-score-tables.tsv", "\n".join(score_lines) + "\n")
        writer.write_text("ablation-by-master.tsv", render_master_table(master_records))
        writer.write_text("ablation-summary.json", canonical_json(summary))
        writer.write_text("notes.md", notes)
        writer.log_metrics(metrics)
        writer.complete()

    for name, value in metrics.items():
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
