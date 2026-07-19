#!/usr/bin/env python3
"""Toy-only checks for the ORF Phase-4 generalization runner."""

from __future__ import annotations

import hashlib
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


RUNNER = load(HERE / "run_generalization.py", "orf_p4_generalization_toy")
CORE = load(
    REPO / "experiments/orf-p4-core/run_core.py",
    "orf_p4_generalization_toy_core",
)
SUPPORT = load(
    REPO / "experiments/poc/orf_support_calibration.py",
    "orf_p4_generalization_toy_support",
)


class GeneralizationToyTests(unittest.TestCase):
    def test_frozen_labels_hash_once(self) -> None:
        self.assertEqual(
            RUNNER.PREIMAGES[0],
            "orf-public-phase4-generalization-v1|master|000",
        )
        self.assertEqual(
            hashlib.sha256(RUNNER.PREIMAGES[0].encode("ascii")).hexdigest(),
            "96a4e42669a3349e9b74388e952642cb46ac28977b57f7f432422ac10ab353e3",
        )

    def test_weight_rule_balances_crossed_counts(self) -> None:
        cliffs = [-1] * 64 + [4] * 64 + [8] * 64 + [16] * 64 + [24] * 64
        weights = [RUNNER.profile_weight(cliff) for cliff in cliffs]
        self.assertEqual(sum(weights[:64]), 256)
        self.assertEqual(sum(weights[64:]), 256)
        self.assertEqual(sum(weights), 512)

    def test_replication_matches_manual_weighted_scores(self) -> None:
        tables = [(10, 5, 0, 0, 0, 0, 0), (1, 20, 0, 0, 0, 0, 0)]
        weights = (4, 1)
        result = RUNNER.evaluate_weighted(CORE, tables, weights)
        adaptive = 4 * 10 + 20
        totals = (4 * 10 + 1, 4 * 5 + 20, 0, 0, 0, 0, 0)
        self.assertEqual(result.adaptive_score, adaptive)
        self.assertEqual(result.global_score, max(totals))
        self.assertEqual(result.regret, adaptive - max(totals))
        self.assertEqual(result.global_length, 1)

    def test_immutable_unsaturated_scorer_returns_exact_table(self) -> None:
        costs = tuple(Fraction(5) + Fraction(3, 2) * m for m in RUNNER.LENGTHS)
        profile = SUPPORT.Profile(-1, costs, RUNNER.LENGTHS, None)
        table = tuple(SUPPORT.score_table(profile, RUNNER.SATURATION))
        self.assertEqual(len(table), 7)
        self.assertTrue(all(type(value) is int and value >= 0 for value in table))

    def test_rendered_profile_schema_width_is_exact(self) -> None:
        costs = tuple(Fraction(5) + Fraction(3, 2) * m for m in RUNNER.LENGTHS)
        profile = SUPPORT.Profile(-1, costs, RUNNER.LENGTHS, None)
        scores = tuple(SUPPORT.score_table(profile, RUNNER.SATURATION))
        row = RUNNER.render_score_row(0, "0" * 64, 0, profile, 4, scores)
        self.assertEqual(len(row.split("\t")), len(RUNNER.score_header()))


if __name__ == "__main__":
    unittest.main()
