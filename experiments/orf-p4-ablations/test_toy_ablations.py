#!/usr/bin/env python3
"""Toy-only tests for the ORF Phase-4 ablation transforms."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = load(HERE / "run_ablations.py", "orf_p4_ablations_toy_runner")
SUPPORT = load(
    REPO / "experiments/poc/orf_support_calibration.py",
    "orf_p4_ablations_toy_support",
)
CORE = load(
    REPO / "experiments/orf-p4-core/run_core.py",
    "orf_p4_ablations_toy_core",
)


def toy_profile() -> object:
    reset = Fraction(7, 2)
    linear = Fraction(3, 5)
    curvature = Fraction(1, 10)
    costs = tuple(
        reset + linear * length + curvature * length * length
        for length in RUNNER.LENGTHS
    )
    events = (1, 2, 4, 7, 5, 3, 1)
    default_scores = RUNNER.score_table(
        costs,
        events,
        saturation=RUNNER.DEFAULT_SATURATION,
        novelty_offset=2,
    )
    return RUNNER.ProfileRow(
        0,
        "0" * 64,
        0,
        0,
        0,
        8,
        costs,
        events,
        default_scores,
    )


class AblationToyTests(unittest.TestCase):
    def test_exact_coefficient_recovery(self) -> None:
        profile = toy_profile()
        self.assertEqual(
            RUNNER.recover_coefficients(profile.costs),
            (Fraction(7, 2), Fraction(3, 5), Fraction(1, 10)),
        )

    def test_default_scorer_matches_immutable_support(self) -> None:
        profile = toy_profile()
        immutable = SUPPORT.Profile(
            cliff=profile.cliff,
            costs=profile.costs,
            events=profile.events,
            floor_margin=None,
        )
        self.assertEqual(
            RUNNER.score_table(
                profile.costs,
                profile.events,
                saturation=RUNNER.DEFAULT_SATURATION,
                novelty_offset=2,
            ),
            tuple(SUPPORT.score_table(immutable, RUNNER.DEFAULT_SATURATION)),
        )

    def test_each_transform_changes_only_its_named_component(self) -> None:
        profile = toy_profile()
        reset, linear, curvature = RUNNER.recover_coefficients(profile.costs)
        for name in RUNNER.ABLATION_IDS:
            with self.subTest(name=name):
                transformed = RUNNER.transform_profile(profile, name)
                if name == "no_cliff":
                    self.assertEqual(transformed.events, RUNNER.LENGTHS)
                    self.assertEqual(transformed.costs, profile.costs)
                else:
                    self.assertEqual(transformed.events, profile.events)
                if name == "no_curvature":
                    self.assertEqual(
                        transformed.costs,
                        tuple(reset + linear * length for length in RUNNER.LENGTHS),
                    )
                elif name == "no_reset":
                    self.assertEqual(
                        transformed.costs,
                        tuple(
                            linear * length + curvature * length * length
                            for length in RUNNER.LENGTHS
                        ),
                    )
                elif name != "no_cliff":
                    self.assertEqual(transformed.costs, profile.costs)
                self.assertEqual(
                    transformed.novelty_offset, 0 if name == "no_novelty" else 2
                )
                self.assertEqual(
                    transformed.saturation,
                    RUNNER.UNSATURATED
                    if name == "unsaturated"
                    else RUNNER.DEFAULT_SATURATION,
                )

    def test_reviewed_evaluator_and_tie_rule_are_reused(self) -> None:
        tables = [(10, 10, 1), (0, 20, 0)]
        result = CORE.evaluate_master_score_tables(tables, lengths=(1, 2, 4))
        self.assertEqual(result.adaptive_score, 30)
        self.assertEqual(result.global_score, 30)
        self.assertEqual(result.global_length, 2)
        self.assertEqual(result.adaptive_length_counts, (1, 1, 0))

    def test_rendered_score_schema_width_is_exact(self) -> None:
        profile = toy_profile()
        transformed = RUNNER.transform_profile(profile, "no_cliff")
        scores = RUNNER.score_table(
            transformed.costs,
            transformed.events,
            saturation=transformed.saturation,
            novelty_offset=transformed.novelty_offset,
        )
        row = RUNNER.render_score_row("no_cliff", profile, transformed, scores)
        self.assertEqual(len(row.split("\t")), len(RUNNER.score_table_header()))


if __name__ == "__main__":
    unittest.main()
