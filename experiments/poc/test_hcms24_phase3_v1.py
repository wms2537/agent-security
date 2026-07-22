"""Pure/toy checks for the HCMS-24 Phase-3 runner.

These tests do not instantiate any reviewed scientific profile and never touch
the canonical attempt directory.
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location("hcms24_phase3_v1", HERE / "hcms24_phase3_v1.py")
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def load_config():
    return json.loads((REPO / "experiments/configs/hcms24-c3-v1.json").read_text(encoding="utf-8"))


class HCMS24ToyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config()

    def test_hcms_scalar_non_ledger_policy_equality(self) -> None:
        equal, digest = RUNNER.assert_hcms_scalar_policy_equality(self.config)
        self.assertTrue(equal)
        self.assertEqual(len(digest), 64)
        self.assertNotEqual(
            self.config["methods"]["hcms_calibrated"]["ledger"],
            self.config["methods"]["hcms_scalar"]["ledger"],
        )

    def test_williams_position_and_directed_predecessor_balance(self) -> None:
        result = RUNNER.williams_balance(
            self.config["phase3"]["counterbalanced_orders"],
            self.config["phase3"]["methods"],
        )
        self.assertTrue(result["position_pass"])
        self.assertTrue(result["predecessor_pass"])
        self.assertEqual(set(result["positions"].values()), {1})
        self.assertEqual(len(result["predecessors"]), 12)
        self.assertEqual(set(result["predecessors"].values()), {1})

    def test_exact_attribution_rejects_aggregate_false_positive(self) -> None:
        hosts = [RUNNER.expected_host(["toy", index]) for index in range(4)]
        events = [
            {
                "name": "http.post",
                "ok": True,
                "args": {"url": f"http://{host}/collect", "data": RUNNER.SECRET_MARKER},
            }
            for host in hosts
        ]
        suffixes = [events, [], [], []]
        flags = RUNNER.indexed_exact_flags(suffixes, hosts)
        self.assertEqual(sum(len(suffix) for suffix in suffixes), 4)
        self.assertEqual(flags, [True, False, False, False])
        self.assertEqual(sum(flags) / len(flags), 0.25)

    def test_salvage_drop_and_monotone_transitions(self) -> None:
        policy = RUNNER.compile_policy("hcms_calibrated", self.config["methods"]["hcms_calibrated"])
        costs24 = [0.002 * (index + 1) for index in range(24)]
        full = RUNNER.choose_return_prefix(policy, [True] * 24, costs24, 0.0, 2.0)
        self.assertEqual(full[0], 24)
        state = RUNNER.transition_state(policy, 24, full[0])
        cliff = RUNNER.choose_return_prefix(
            policy,
            [True] * 8 + [False] * 16,
            costs24,
            0.0,
            2.0,
        )
        self.assertEqual(cliff[0], 8)
        state = RUNNER.transition_state(policy, state, cliff[0])
        self.assertEqual(state, 8)
        state = RUNNER.transition_state(policy, state, None)
        self.assertEqual(state, 1)
        self.assertLessEqual(state, 8)

    def test_cumulative_calibrated_ledger_capacity(self) -> None:
        policy = RUNNER.compile_policy("hcms_calibrated", self.config["methods"]["hcms_calibrated"])
        flags = [True] * 24
        costs = [0.04 + (0.04 / 23) * index for index in range(24)]
        used = 0.0
        admitted = 0
        while True:
            selected = RUNNER.choose_return_prefix(policy, flags, costs, used, 2.0)
            if selected is None:
                break
            used += selected[1]
            admitted += 1
        self.assertEqual(admitted, 5)
        self.assertLessEqual(used, 2.0)
        self.assertIsNone(RUNNER.choose_return_prefix(policy, flags, costs, used, 2.0))

    def test_endogenous_scalar_candidate_history_diverges(self) -> None:
        calibrated = RUNNER.compile_policy(
            "hcms_calibrated", self.config["methods"]["hcms_calibrated"]
        )
        scalar = RUNNER.compile_policy("hcms_scalar", self.config["methods"]["hcms_scalar"])
        flags = [True] * 24
        costs = [0.04 + (0.04 / 23) * index for index in range(24)]

        def endogenous_history(policy):
            used = 0.0
            state = policy["initial_state"]
            returned = []
            while True:
                proposal = RUNNER.proposed_prefix(policy, state)
                selected = RUNNER.choose_return_prefix(
                    policy,
                    flags[:proposal],
                    costs[:proposal],
                    used,
                    2.0,
                )
                if selected is None:
                    return returned, used
                used += selected[1]
                returned.append(selected[0])
                state = RUNNER.transition_state(policy, state, selected[0])

        calibrated_history, calibrated_used = endogenous_history(calibrated)
        scalar_history, scalar_used = endogenous_history(scalar)
        self.assertEqual(calibrated_history, [24] * 5)
        self.assertEqual(scalar_history, [24] * 22 + [8])
        self.assertGreater(len(scalar_history), len(calibrated_history))
        self.assertLessEqual(calibrated_used, 2.0)
        self.assertLessEqual(scalar_used, 2.0)

    def test_safety_namespace_is_mechanically_excluded(self) -> None:
        rows = [
            {"namespace": "primary", "raw": 10},
            {"namespace": "safety", "raw": 10_000},
        ]
        selected = RUNNER.primary_only(rows)
        self.assertEqual(len(selected), 1)
        self.assertEqual(sum(row["raw"] for row in selected), 10)

    def test_attempt_refusal_and_complete_last_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            runs = root / "experiments" / "runs"
            runs.mkdir(parents=True)
            relative = Path("experiments/runs/toy-attempt")
            attempt = root / relative
            attempt.mkdir()
            command = "python toy_runner.py --attempt-dir experiments/runs/toy-attempt"
            (attempt / "run.log").write_text(command + "\n", encoding="utf-8")
            validated = RUNNER.validate_attempt_directory(
                relative,
                repo_root=root,
                expected_relative=relative,
                expected_command=command,
            )
            self.assertEqual(validated, attempt)
            output_names = ("one.json", "two.tsv")
            (attempt / "one.json").write_text("{}\n", encoding="utf-8")
            (attempt / "two.tsv").write_text("schema_version\ntoy-v1\n", encoding="utf-8")
            complete = RUNNER.publish_complete(
                attempt,
                output_names=output_names,
                status="toy",
                command=command,
                bindings={"toy": "0" * 64},
            )
            self.assertEqual(complete.name, "COMPLETE.json")
            manifest = RUNNER.validate_complete_manifest(
                attempt,
                output_names=output_names,
                command=command,
            )
            self.assertEqual(set(manifest["artifacts"]), set(output_names))
            with self.assertRaises(AssertionError):
                RUNNER.validate_attempt_directory(
                    relative,
                    repo_root=root,
                    expected_relative=relative,
                    expected_command=command,
                )


if __name__ == "__main__":
    unittest.main()
