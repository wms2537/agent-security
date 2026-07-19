#!/usr/bin/env python3
"""Toy-only checks for ORF nested scaling selection."""

from __future__ import annotations

import importlib.util
import sys
import unittest
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


RUNNER = load(HERE / "run_scaling.py", "orf_p4_scaling_toy")
CORE = load(REPO / "experiments/orf-p4-core/run_core.py", "orf_p4_scaling_toy_core")


class ScalingToyTests(unittest.TestCase):
    def test_nested_indices_have_exact_counts(self) -> None:
        sets = [set(RUNNER.selected_indices(k)) for k in RUNNER.REPLICATE_COUNTS]
        self.assertEqual([len(value) for value in sets], [40, 160, 320])
        self.assertTrue(sets[0] < sets[1] < sets[2])

    def test_every_stratum_uses_prefix_replicates(self) -> None:
        for k in RUNNER.REPLICATE_COUNTS:
            indices = RUNNER.selected_indices(k)
            for stratum in range(40):
                observed = [index % 8 for index in indices if index // 8 == stratum]
                self.assertEqual(observed, list(range(k)))

    def test_reviewed_evaluator_handles_selected_rows(self) -> None:
        row_one = (10, 8, 6, 4, 2, 1, 0)
        row_two = (1, 12, 5, 4, 3, 2, 1)
        result = CORE.evaluate_master_score_tables([row_one, row_two])
        self.assertEqual(result.adaptive_score, 22)
        self.assertEqual(result.global_score, 20)
        self.assertEqual(result.regret, 2)
        self.assertEqual(result.global_length, 2)

    def test_cell_render_schema_is_exact(self) -> None:
        result = CORE.evaluate_master_score_tables([(10, 8, 6, 4, 2, 1, 0)])
        record = RUNNER.cell_record(CORE, 0, 1, result)
        rendered = RUNNER.render_cells([record]).splitlines()
        self.assertEqual(len(rendered), 2)
        self.assertEqual(len(rendered[0].split("\t")), len(rendered[1].split("\t")))


if __name__ == "__main__":
    unittest.main()
