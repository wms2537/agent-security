#!/usr/bin/env python3
"""Exploratory, non-target calibration for the ORF-B materiality prediction.

This program never contacts NIST or Kaggle.  Its 64 public calibration masters are
domain-separated hashes of their indices.  It uses CPython's stable Random stream
only for exact binary-rational draws, then Decimal transcendental functions under
a frozen context and Fraction resource arithmetic.
"""

from __future__ import annotations

import json
import platform
from dataclasses import dataclass
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_EVEN, localcontext
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

from random import Random


LENGTHS = (1, 2, 4, 8, 16, 24, 32)
CLIFFS = (-1, 4, 8, 16, 24)
MASTER_COUNT = 64
B_GEN = Fraction(9000, 1)
B_REP = Fraction(8100, 1)
CANDIDATE_CAP = 2000
SATURATIONS = (200_000, 10**18)
PRECISION = 80
FLOOR_CERTIFICATE_THRESHOLD = Decimal("1e-60")
OUTPUT_DIR = Path("experiments/runs/orf-support-calibration-v1")


@dataclass(frozen=True)
class Profile:
    cliff: int
    costs: tuple[Fraction, ...]
    events: tuple[int, ...]
    floor_margin: Decimal | None


def canonical_json(value: object) -> bytes:
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


def random_decimal(rng: Random) -> Decimal:
    numerator, denominator = rng.random().as_integer_ratio()
    with localcontext() as ctx:
        ctx.prec = PRECISION
        ctx.rounding = ROUND_HALF_EVEN
        return Decimal(numerator) / Decimal(denominator)


def log_uniform(rng: Random, lower: str, upper: str) -> Decimal:
    lo = Decimal(lower)
    hi = Decimal(upper)
    u = random_decimal(rng)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        ctx.rounding = ROUND_HALF_EVEN
        return (lo.ln() + (hi.ln() - lo.ln()) * u).exp()


def keyed_rng(master: bytes, stream_key: str) -> Random:
    digest = sha256(master + b"|" + stream_key.encode("ascii")).digest()
    return Random(int.from_bytes(digest, "big"))


def event_count(length: int, cliff: int, lam: Decimal | None) -> tuple[int, Decimal | None]:
    if cliff == -1 or length <= cliff:
        return length, None
    assert lam is not None
    with localcontext() as ctx:
        ctx.prec = PRECISION
        ctx.rounding = ROUND_HALF_EVEN
        exponent = -lam * Decimal(length - cliff) / Decimal(cliff)
        raw = Decimal(length) * exponent.exp()
        floor_value = int(raw.to_integral_value(rounding=ROUND_FLOOR))
        distance = min(raw - Decimal(floor_value), Decimal(floor_value + 1) - raw)
    return max(0, min(length, floor_value)), distance


def build_profiles(master: bytes) -> tuple[list[Profile], Decimal]:
    profiles: list[Profile] = []
    minimum_floor_margin: Decimal | None = None
    for reset_index in range(2):
        for linear_index in range(2):
            for curvature_index in range(2):
                for cliff_index, cliff in enumerate(CLIFFS):
                    stratum = (
                        ((reset_index * 2 + linear_index) * 2 + curvature_index) * 5
                        + cliff_index
                    )
                    for replicate in range(8):
                        rng = keyed_rng(
                            master,
                            f"primary|stratum={stratum:02d}|replicate={replicate:02d}",
                        )
                        a = log_uniform(rng, "5", "20") if reset_index == 0 else log_uniform(rng, "40", "80")
                        b = log_uniform(rng, "0.1", "1") if linear_index == 0 else log_uniform(rng, "2", "8")
                        d = Decimal(0) if curvature_index == 0 else log_uniform(rng, "0.05", "0.2")
                        lam = None if cliff == -1 else log_uniform(rng, "0.5", "3")
                        costs: list[Fraction] = []
                        events: list[int] = []
                        profile_margin: Decimal | None = None
                        for length in LENGTHS:
                            costs.append(Fraction(a + b * length + d * length * length))
                            count, margin = event_count(length, cliff, lam)
                            events.append(count)
                            if margin is not None:
                                profile_margin = margin if profile_margin is None else min(profile_margin, margin)
                                minimum_floor_margin = margin if minimum_floor_margin is None else min(minimum_floor_margin, margin)
                        profiles.append(Profile(cliff, tuple(costs), tuple(events), profile_margin))
    assert len(profiles) == 320
    assert minimum_floor_margin is not None
    return profiles, minimum_floor_margin


def ceil_positive_fraction(value: Fraction) -> int:
    assert value >= 0
    return (value.numerator + value.denominator - 1) // value.denominator


def score_table(profile: Profile, saturation: int) -> tuple[int, ...]:
    generation_probe = sum(profile.costs, Fraction(0, 1))
    positive = [index for index, count in enumerate(profile.events) if count > 0]
    returned_probe = len(positive)
    replay_probe = sum((profile.costs[index] for index in positive), Fraction(0, 1))
    raw_probe = sum(16 * profile.events[index] + 2 for index in positive)
    scores: list[int] = []
    for index, _length in enumerate(LENGTHS):
        event = profile.events[index]
        if event == 0:
            scores.append(raw_probe)
            continue
        candidate_raw = 16 * event + 2
        saturation_capacity = (
            0
            if raw_probe >= saturation
            else ceil_positive_fraction(Fraction(saturation - raw_probe, candidate_raw))
        )
        capacity = max(
            0,
            min(
                CANDIDATE_CAP - returned_probe,
                int((B_GEN - generation_probe) // profile.costs[index]),
                int((B_REP - replay_probe) // profile.costs[index]),
                saturation_capacity,
            ),
        )
        scores.append(min(saturation, raw_probe + capacity * candidate_raw))
    return tuple(scores)


def profile_weight(profile: Profile, weighting: str) -> int:
    if weighting == "equal":
        return 1
    if weighting == "balanced_cliff_presence":
        return 4 if profile.cliff == -1 else 1
    if weighting == "no_cliff_only":
        return 1 if profile.cliff == -1 else 0
    if weighting == "cliff_only":
        return 0 if profile.cliff == -1 else 1
    raise AssertionError(weighting)


def gain_for_design(
    profiles: list[Profile], tables: list[tuple[int, ...]], weighting: str
) -> tuple[int, int, int, int]:
    weights = [profile_weight(profile, weighting) for profile in profiles]
    adaptive = sum(weight * max(table) for weight, table in zip(weights, tables))
    global_by_length = [
        sum(weight * table[index] for weight, table in zip(weights, tables))
        for index in range(len(LENGTHS))
    ]
    best_index = max(range(len(LENGTHS)), key=lambda index: (global_by_length[index], -LENGTHS[index]))
    global_score = global_by_length[best_index]
    assert global_score > 0
    assert adaptive >= global_score
    return adaptive, global_score, adaptive - global_score, LENGTHS[best_index]


def percent_fraction(numerator: int, denominator: int) -> Fraction:
    return Fraction(100 * numerator, denominator)


def fixed_12(value: Fraction) -> str:
    with localcontext() as ctx:
        ctx.prec = PRECISION
        ctx.rounding = ROUND_HALF_EVEN
        decimal_value = Decimal(value.numerator) / Decimal(value.denominator)
        return format(decimal_value.quantize(Decimal("0.000000000001")), "f")


def median(values: list[Fraction]) -> Fraction:
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2


def main() -> int:
    print("command: comp/.venv/bin/python -I experiments/poc/orf_support_calibration.py")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    weightings = ("equal", "balanced_cliff_presence", "no_cliff_only", "cliff_only")
    records: list[dict[str, object]] = []
    floor_margins: list[Decimal] = []
    for master_index in range(MASTER_COUNT):
        master = sha256(
            f"orf-nontarget-calibration-v1|master|{master_index:03d}".encode("ascii")
        ).digest()
        profiles, floor_margin = build_profiles(master)
        floor_margins.append(floor_margin)
        for saturation in SATURATIONS:
            tables = [score_table(profile, saturation) for profile in profiles]
            for weighting in weightings:
                adaptive, global_score, numerator, global_length = gain_for_design(
                    profiles, tables, weighting
                )
                gain = percent_fraction(numerator, global_score)
                records.append(
                    {
                        "master_index": master_index,
                        "master_digest_hex": master.hex(),
                        "weighting": weighting,
                        "saturation": saturation,
                        "adaptive_score": adaptive,
                        "global_score": global_score,
                        "gain_numerator": numerator,
                        "gain_denominator": global_score,
                        "gain_percent_fixed_12": fixed_12(gain),
                        "clears_5_percent": gain >= 5,
                        "global_length": global_length,
                    }
                )

    aggregates: dict[str, dict[str, object]] = {}
    for saturation in SATURATIONS:
        for weighting in weightings:
            subset = [
                record
                for record in records
                if record["saturation"] == saturation and record["weighting"] == weighting
            ]
            gains = [
                percent_fraction(int(record["gain_numerator"]), int(record["gain_denominator"]))
                for record in subset
            ]
            clears = sum(bool(record["clears_5_percent"]) for record in subset)
            key = f"{weighting}|H={saturation}"
            aggregates[key] = {
                "master_count": len(subset),
                "clears_5_percent_count": clears,
                "clears_5_percent_fraction_fixed_12": fixed_12(Fraction(clears, len(subset))),
                "minimum_gain_percent_fixed_12": fixed_12(min(gains)),
                "median_gain_percent_fixed_12": fixed_12(median(gains)),
                "maximum_gain_percent_fixed_12": fixed_12(max(gains)),
            }

    minimum_floor_margin = min(floor_margins)
    support_checks = {
        "equal_H200k_at_least_48_of_64": aggregates["equal|H=200000"]["clears_5_percent_count"] >= 48,
        "balanced_H200k_at_least_32_of_64": aggregates["balanced_cliff_presence|H=200000"]["clears_5_percent_count"] >= 32,
        "no_cliff_H200k_at_least_32_of_64": aggregates["no_cliff_only|H=200000"]["clears_5_percent_count"] >= 32,
        "cliff_H200k_at_least_32_of_64": aggregates["cliff_only|H=200000"]["clears_5_percent_count"] >= 32,
        "equal_unsaturated_at_least_32_of_64": aggregates[f"equal|H={10**18}"]["clears_5_percent_count"] >= 32,
        "floor_distance_at_least_1e_minus_60": minimum_floor_margin >= FLOOR_CERTIFICATE_THRESHOLD,
    }
    summary = {
        "status": "EXPLORATORY_NON_TARGET",
        "master_derivation": "SHA256(ASCII('orf-nontarget-calibration-v1|master|{index:03d}'))",
        "master_count": MASTER_COUNT,
        "python": platform.python_version(),
        "decimal_precision": PRECISION,
        "decimal_rounding": "ROUND_HALF_EVEN",
        "floor_certificate_threshold": str(FLOOR_CERTIFICATE_THRESHOLD),
        "minimum_cliff_floor_distance": str(minimum_floor_margin),
        "aggregates": aggregates,
        "support_checks": support_checks,
        "support_criterion_passed": all(support_checks.values()),
    }

    header = (
        "master_index\tmaster_digest_hex\tweighting\tsaturation\tadaptive_score\t"
        "global_score\tgain_numerator\tgain_denominator\tgain_percent_fixed_12\t"
        "clears_5_percent\tglobal_length\n"
    )
    lines = [header]
    for record in records:
        lines.append(
            "\t".join(
                [
                    str(record["master_index"]),
                    str(record["master_digest_hex"]),
                    str(record["weighting"]),
                    str(record["saturation"]),
                    str(record["adaptive_score"]),
                    str(record["global_score"]),
                    str(record["gain_numerator"]),
                    str(record["gain_denominator"]),
                    str(record["gain_percent_fixed_12"]),
                    str(record["clears_5_percent"]).lower(),
                    str(record["global_length"]),
                ]
            )
            + "\n"
        )
    (OUTPUT_DIR / "masters.tsv").write_text("".join(lines), encoding="utf-8", newline="")
    (OUTPUT_DIR / "summary.json").write_bytes(canonical_json(summary))
    print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
