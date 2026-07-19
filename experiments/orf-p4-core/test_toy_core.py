#!/usr/bin/env python3
"""Pure-function toy tests for the Phase-4 core evaluator."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from fractions import Fraction
from pathlib import Path


RUNNER_PATH = Path(__file__).resolve().with_name("run_core.py")
SPEC = importlib.util.spec_from_file_location("orf_p4_core_runner_toy", RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load run_core.py")
CORE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CORE
SPEC.loader.exec_module(CORE)


class ToyCoreTests(unittest.TestCase):
    def test_adaptive_and_global_use_exhaustive_smaller_tie_argmax(self) -> None:
        tables = (
            (10, 12, 0, 0, 0, 0, 0),
            (9, 0, 0, 0, 0, 0, 0),
        )
        result = CORE.evaluate_master_score_tables(tables)
        self.assertEqual(result.adaptive_score, 21)
        self.assertEqual(result.global_score, 19)
        self.assertEqual(result.regret, 2)
        self.assertEqual(result.gain_percent, Fraction(200, 19))
        self.assertEqual(result.global_length, 1)
        self.assertEqual(result.adaptive_length_counts, (1, 1, 0, 0, 0, 0, 0))

    def test_ties_choose_the_smaller_length_for_every_row_and_global(self) -> None:
        tables = (
            (5, 5, 1, 1, 1, 1, 1),
            (7, 7, 2, 2, 2, 2, 2),
        )
        result = CORE.evaluate_master_score_tables(tables)
        self.assertEqual(result.regret, 0)
        self.assertEqual(result.global_length, 1)
        self.assertEqual(result.adaptive_length_counts, (2, 0, 0, 0, 0, 0, 0))

    def test_nonnegative_integer_validation_is_exact(self) -> None:
        with self.assertRaises(ValueError):
            CORE.evaluate_master_score_tables(((1, 2, 3, 4, 5, 6, -1),))
        with self.assertRaises(ValueError):
            CORE.evaluate_master_score_tables(((1, 2, 3, 4, 5, 6, 7.0),))

    def test_fixed_rendering_does_not_drive_decisions(self) -> None:
        self.assertEqual(CORE.fixed_12(Fraction(1, 3)), "0.333333333333")
        self.assertEqual(CORE.fixed_12(Fraction(2, 3)), "0.666666666667")


if __name__ == "__main__":
    unittest.main()
