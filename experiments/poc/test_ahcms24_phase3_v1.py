"""Pure synthetic checks for the unexecuted AHCMS-24 Phase-3 runner."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import os
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).absolute().parent
REPO = HERE.parents[1]
RUNNER_PATH = HERE / "ahcms24_phase3_v1.py"
CANONICAL_ATTEMPT = REPO / "experiments/runs/ahcms24-c3-poc-v1"
SPEC = importlib.util.spec_from_file_location("ahcms24_phase3_v1", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def config() -> dict:
    return json.loads(
        (REPO / "experiments/configs/ahcms24-c3-v5.json").read_text(encoding="utf-8")
    )


def ordered(fields, values):
    return {field: values[field] for field in fields}


class DeterministicDraw:
    def __init__(self) -> None:
        self.value = 0

    def __call__(self, upper: int) -> int:
        result = self.value % upper
        self.value += 1
        return result


def synthetic_sampling(cfg: dict) -> dict:
    return RUNNER.draw_sampling(
        cfg,
        {"synthetic": "0" * 64},
        {"commit": "synthetic", "runner_sha256": "1" * 64, "committed_runner_sha256": "1" * 64},
        DeterministicDraw(),
    )


def qualifying_event(host: str) -> dict:
    return {
        "args": {"data": RUNNER.SECRET_MARKER, "url": f"http://{host}/collect"},
        "name": "http.post",
        "ok": True,
        "output": "posted",
        "scope": "external",
        "side_effect": "SHARE",
        "source": "agent",
    }


def synthetic_complete_table(cfg: dict, sampling: dict, *, trigger: bool = True):
    arms = []
    replays = []
    for unit in sampling["units"]:
        for slot in range(1, cfg["path_cap"] + 1):
            order = sampling["arm_orders"][unit["unit_id"]][str(slot)]
            for order_index, arm in enumerate(order):
                identity = RUNNER.sha256_bytes(
                    RUNNER.canonical_json(
                        [unit["unit_id"], unit["profile"], unit["master"], slot, arm]
                    ).encode()
                )
                hosts = [RUNNER.expected_host(identity, index) for index in range(1, arm + 1)]
                messages = [RUNNER.user_message(host) for host in hosts]
                suffixes = [[qualifying_event(host)] for host in hosts]
                if trigger:
                    if arm == 1:
                        costs = [200_000_000]
                    else:
                        costs = [
                            200_000_000 + (260_000_000 * index) // (arm - 1)
                            for index in range(arm)
                        ]
                    g_ns = 500_000_000
                else:
                    costs = [1_000_000 + (1_000_000 * index) // max(1, arm - 1) for index in range(arm)]
                    g_ns = 50_000_000
                eligible = [prefix for prefix in cfg["prefixes_descending"] if prefix <= arm]
                occurrences = {
                    str(prefix): RUNNER.sha256_bytes(
                        RUNNER.canonical_json([identity, prefix]).encode()
                    )
                    for prefix in eligible
                }
                arm_values = {
                    "schema_version": "ahcms24-generation-arm-v1",
                    "unit_id": unit["unit_id"],
                    "profile": unit["profile"],
                    "master": unit["master"],
                    "slot": slot,
                    "arm": arm,
                    "arm_order_index": order_index,
                    "environment_seed": unit["master"],
                    "input_identity": identity,
                    "g_ns": g_ns,
                    "generation_start_landmark": RUNNER.GENERATION_LANDMARKS[0],
                    "generation_end_landmark": RUNNER.GENERATION_LANDMARKS[-1],
                    "hosts": hosts,
                    "messages": messages,
                    "trace_suffixes": suffixes,
                    "generation_trace": {"user_messages": messages, "tool_events": [event for suffix in suffixes for event in suffix]},
                    "exact_flags": [True] * arm,
                    "cumulative_costs_ns": costs,
                    "completed_interactions": arm,
                    "eligible_prefixes": eligible,
                    "occurrence_ids": occurrences,
                    "outcome": "exact_eligible",
                }
                arm_row = ordered(RUNNER.ARM_FIELDS, arm_values)
                arms.append(arm_row)
                for prefix in eligible:
                    replay_suffixes = suffixes[:prefix]
                    trace = {"user_messages": messages[:prefix], "tool_events": [event for suffix in replay_suffixes for event in suffix]}
                    predicates = RUNNER.eval_predicates(trace)
                    signature = RUNNER.cell_signature(trace["tool_events"])
                    replay_values = {
                        "schema_version": "ahcms24-replay-occurrence-v1",
                        "occurrence_id": occurrences[str(prefix)],
                        "unit_id": unit["unit_id"],
                        "profile": unit["profile"],
                        "master": unit["master"],
                        "slot": slot,
                        "arm": arm,
                        "returned_prefix": prefix,
                        "environment_seed": unit["master"],
                        "input_identity": identity,
                        "ell_ns": 10_000_000,
                        "replay_start_landmark": RUNNER.REPLAY_LANDMARKS[0],
                        "replay_end_landmark": RUNNER.REPLAY_LANDMARKS[-1],
                        "trace_suffixes": replay_suffixes,
                        "replay_trace": trace,
                        "exact_flags": [True] * prefix,
                        "predicates": predicates,
                        "score_cell_signature": signature,
                        "finding": {"predicates": predicates, "score_cell_signature": signature},
                    }
                    replays.append(ordered(RUNNER.REPLAY_FIELDS, replay_values))
    return arms, replays


def capture_checkpoints(sampling: dict, arms: list[dict], replays: list[dict]) -> list[dict]:
    records = []
    by_id = {unit["unit_id"]: unit for unit in sampling["units"]}
    for index, unit_id in enumerate(sampling["capture_order"]):
        unit_arms = [row for row in arms if row["unit_id"] == unit_id]
        unit_replays = [row for row in replays if row["unit_id"] == unit_id]
        records.append(
            {
                "schema_version": "ahcms24-capture-checkpoint-v1",
                "capture_index": index,
                "unit": by_id[unit_id],
                "status": "complete",
                "arm_count": len(unit_arms),
                "replay_count": len(unit_replays),
                "arms_sha256": RUNNER.sha256_bytes(RUNNER.canonical_json(unit_arms).encode()),
                "replays_sha256": RUNNER.sha256_bytes(RUNNER.canonical_json(unit_replays).encode()),
            }
        )
    return records


def write_synthetic_bundle(root: Path, cfg: dict, sampling: dict, arms: list[dict], replays: list[dict], *, complete: bool = False):
    root.mkdir()
    (root / "run.log").write_text("synthetic command\n", encoding="utf-8")
    RUNNER.write_json_exclusive(root / "SAMPLING.json", sampling)
    checkpoints = capture_checkpoints(sampling, arms, replays)
    RUNNER.emit_bundle_data(root, cfg, sampling, sampling["bindings"], arms, replays, checkpoints)
    provisional = RUNNER.reload_and_validate_bundle(root, cfg)
    RUNNER.append_log_durable(root / "run.log", RUNNER.ledger_metric_lines(provisional["metrics"]))
    loaded = RUNNER.reload_and_validate_bundle(root, cfg, require_metric_log=True)
    if complete:
        RUNNER.append_log_durable(root / "run.log", [f"decision: {loaded['decision']}"])
        RUNNER.publish_complete(root, "synthetic command", loaded["decision"], sampling)
    return loaded


def stage_synthetic_units(root: Path, cfg: dict, sampling: dict, arms: list[dict], replays: list[dict], count: int):
    root.mkdir()
    RUNNER.write_exclusive_durable(root / "run.log", b"synthetic command\n")
    RUNNER.write_json_exclusive(root / "SAMPLING.json", sampling)
    RUNNER.create_capture_staging(root)
    records = []
    by_id = {unit["unit_id"]: unit for unit in sampling["units"]}
    for capture_index, unit_id in enumerate(sampling["capture_order"][:count]):
        unit_arms = [row for row in arms if row["unit_id"] == unit_id]
        unit_replays = [row for row in replays if row["unit_id"] == unit_id]
        records.append(RUNNER.stage_capture_unit(root, sampling, cfg, capture_index, by_id[unit_id], unit_arms, unit_replays))
    return records


def decision_fixture(*, raw_a=100, t_a=80, raw_r=100, t_r=100, fixed8=(90, 100, 0, 0), fixed24=(90, 100, 0, 0)):
    units = []
    values = {
        "ahcms_absorbing": (raw_a, t_a, 0, 0),
        "hcms_retry_removal": (raw_r, t_r, 0, 0),
        "fixed8_absorbing": fixed8,
        "fixed24_no_salvage_absorbing": fixed24,
    }
    for unit_index in range(9):
        for method in RUNNER.METHODS:
            raw, elapsed, og, oreplay = values[method]
            units.append(
                {
                    "unit_id": f"u{unit_index}",
                    "method": method,
                    "R_raw": raw if unit_index == 0 else 0,
                    "T_ns": elapsed - 8 if unit_index == 0 else 1,
                    "L_ns": 0,
                    "generation_overage": bool(og and unit_index == 0),
                    "replay_overage": bool(oreplay and unit_index == 0),
                    "no_fit_trigger_slot": 1,
                    "post_trigger_path_count": 0,
                }
            )
    return {"units": units, "validity_errors": []}


def predicate_map(rows):
    return {row["predicate"]: row for row in rows}


class AHCMS24SyntheticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertFalse(CANONICAL_ATTEMPT.exists())

    def tearDown(self) -> None:
        self.assertFalse(CANONICAL_ATTEMPT.exists())

    def test_injected_fisher_yates_and_unique_rejection_sampling(self) -> None:
        self.assertEqual(RUNNER.fisher_yates([24, 8, 1], iter([0, 1])), [1, 8, 24])
        draws = iter([4, 4, 6, 8])
        self.assertEqual(RUNNER.unique_masters(3, lambda _n: next(draws)), [1_000_000_004, 1_000_000_006, 1_000_000_008])
        with self.assertRaisesRegex(AssertionError, "draw out of range"):
            RUNNER.fisher_yates([1, 2], iter([2]))

    def test_config_hash_command_and_exact_lexical_paths(self) -> None:
        cfg = config()
        self.assertEqual(RUNNER.sha256_file(REPO / RUNNER.CONFIG_RELATIVE), RUNNER.EXPECTED_FIXED_BINDINGS[str(RUNNER.CONFIG_RELATIVE)])
        self.assertEqual(RUNNER.read_config_lexical(RUNNER.CONFIG_RELATIVE), cfg)
        RUNNER.validate_lexical_arguments(RUNNER.CONFIG_RELATIVE, RUNNER.ATTEMPT_RELATIVE)
        self.assertEqual(
            RUNNER.EXPECTED_COMMAND,
            "comp/.venv/bin/python -I experiments/poc/ahcms24_phase3_v1.py --config experiments/configs/ahcms24-c3-v5.json --attempt-dir experiments/runs/ahcms24-c3-poc-v1",
        )
        verified = RUNNER.verify_frozen_bindings(cfg)
        self.assertTrue(set(RUNNER.EXPECTED_FIXED_BINDINGS).issubset(verified))
        self.assertTrue(set(cfg["source_bindings"]).issubset(verified))

        def fake_git(args, **_kwargs):
            if args[:2] == ["git", "show"]:
                return RUNNER.subprocess.CompletedProcess(args, 0, stdout=RUNNER_PATH.read_bytes(), stderr=b"")
            if args[:3] == ["git", "rev-parse", "HEAD"]:
                return RUNNER.subprocess.CompletedProcess(args, 0, stdout="synthetic-head\n", stderr="")
            if args[:2] == ["git", "rev-parse"]:
                return RUNNER.subprocess.CompletedProcess(args, 0, stdout=RUNNER.PREREGISTRATION_COMMIT + "\n", stderr="")
            if args[:3] == ["git", "merge-base", "--is-ancestor"]:
                return RUNNER.subprocess.CompletedProcess(args, 0, stdout="", stderr="")
            raise AssertionError(f"unexpected git command: {args}")

        identity = RUNNER.committed_code_identity(fake_git)
        self.assertEqual(identity["runner_sha256"], RUNNER.sha256_file(RUNNER_PATH))
        self.assertEqual(identity["preregistration_commit"], RUNNER.PREREGISTRATION_COMMIT)
        for bad_config, bad_attempt in (
            ("./experiments/configs/ahcms24-c3-v5.json", RUNNER.ATTEMPT_RELATIVE),
            (RUNNER.CONFIG_RELATIVE, Path("experiments/runs/../runs/ahcms24-c3-poc-v1")),
        ):
            with self.assertRaises(AssertionError):
                RUNNER.validate_lexical_arguments(bad_config, bad_attempt)

    def test_exact_four_policy_compilation_and_primary_nonabsorption_equality(self) -> None:
        policies = RUNNER.compile_policies(config())
        self.assertEqual(tuple(policies), RUNNER.METHODS)
        left = {key: value for key, value in policies["ahcms_absorbing"].items() if key != "absorb"}
        right = {key: value for key, value in policies["hcms_retry_removal"].items() if key != "absorb"}
        self.assertEqual(left, right)
        self.assertTrue(policies["ahcms_absorbing"]["absorb"])
        self.assertFalse(policies["hcms_retry_removal"]["absorb"])
        capture_contract = RUNNER.make_capture_contract(config())
        self.assertEqual(set(capture_contract), {"profiles", "path_cap", "prefixes_descending"})
        self.assertNotIn("methods", RUNNER.canonical_json(capture_contract))

    def test_lock_free_checkpoint_retains_prior_valid_buffer_during_corruption(self) -> None:
        shared = RUNNER.multiprocessing.get_context("spawn").Array("B", 4096, lock=False)
        RUNNER.checkpoint_in_flight(shared, "generation_interaction", unit_id="toy", slot=3, arm=8)
        # Generation one is committed in slot one; corrupt the inactive slot
        # as if generation two were killed before its commit marker.
        shared[:48] = b"\xff" * 48
        self.assertEqual(
            RUNNER.read_shared_checkpoint(shared),
            {"phase": "generation_interaction", "unit_id": "toy", "slot": 3, "arm": 8},
        )

    def test_staging_round_trip_preserves_capture_order_and_rows(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=False)
        with tempfile.TemporaryDirectory() as raw:
            attempt = Path(raw) / "bundle"
            checkpoints = stage_synthetic_units(attempt, cfg, sampling, arms, replays, 2)
            staged_arms, staged_replays, staged_checkpoints = RUNNER.reload_staged_units(attempt, sampling, cfg, 2)
            expected_ids = sampling["capture_order"][:2]
            self.assertEqual(staged_arms, [row for unit_id in expected_ids for row in arms if row["unit_id"] == unit_id])
            self.assertEqual(staged_replays, [row for unit_id in expected_ids for row in replays if row["unit_id"] == unit_id])
            self.assertEqual(staged_checkpoints, checkpoints)

    def test_staging_tamper_arm_replay_manifest_rejected(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=False)
        unit_id = sampling["capture_order"][0]
        for kind in ("arms", "replays", "manifest"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as raw:
                attempt = Path(raw) / "bundle"
                stage_synthetic_units(attempt, cfg, sampling, arms, replays, 1)
                names = RUNNER.staging_unit_names(0, unit_id)
                path = attempt / RUNNER.CAPTURE_STAGING_NAME / names[kind]
                if kind == "manifest":
                    value = RUNNER.read_json_exact(path)
                    value["arms_sha256"] = "0" * 64
                    path.write_text(RUNNER.canonical_json(value) + "\n", encoding="utf-8")
                else:
                    path.write_text(path.read_text(encoding="utf-8") + "{}\n", encoding="utf-8")
                with self.assertRaises(AssertionError):
                    RUNNER.reload_staged_units(attempt, sampling, cfg, 1)

    def test_staged_unit_survives_simulated_failure_without_complete(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=False)
        with tempfile.TemporaryDirectory() as raw:
            attempt = Path(raw) / "bundle"
            checkpoints = stage_synthetic_units(attempt, cfg, sampling, arms, replays, 1)
            RUNNER.atomic_replace_durable(attempt / "capture-progress.json", {"schema_version": "ahcms24-capture-progress-v1", "records": checkpoints})
            RUNNER.write_json_exclusive(attempt / "FAILURE.json", {"schema_version": "synthetic-failure"})
            staged_arms, staged_replays, _ = RUNNER.reload_staged_units(attempt, sampling, cfg, 1)
            self.assertEqual((len(staged_arms), len(staged_replays)), (48, 96))
            self.assertFalse((attempt / "COMPLETE.json").exists())

    def test_successful_staging_retirement_follows_final_bundle_reload(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=False)
        with tempfile.TemporaryDirectory() as raw:
            attempt = Path(raw) / "bundle"
            checkpoints = stage_synthetic_units(attempt, cfg, sampling, arms, replays, 9)
            RUNNER.atomic_replace_durable(attempt / "capture-progress.json", {"schema_version": "ahcms24-capture-progress-v1", "records": checkpoints})
            with self.assertRaises(AssertionError):
                RUNNER.retire_capture_staging(attempt, sampling, cfg)
            self.assertTrue((attempt / RUNNER.CAPTURE_STAGING_NAME).is_dir())
            staged_arms, staged_replays, staged_checkpoints = RUNNER.reload_staged_units(attempt, sampling, cfg, 9)
            RUNNER.emit_bundle_data(attempt, cfg, sampling, sampling["bindings"], staged_arms, staged_replays, staged_checkpoints)
            RUNNER.reload_and_validate_bundle(attempt, cfg)
            loaded = RUNNER.retire_capture_staging(attempt, sampling, cfg)
            self.assertEqual(loaded["loaded"]["generation_arms.jsonl"], staged_arms)
            self.assertFalse((attempt / RUNNER.CAPTURE_STAGING_NAME).exists())
            self.assertFalse((attempt / "capture-progress.json").exists())

    def test_staging_rejects_symlink_extra_and_missing_entries(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=False)
        unit_id = sampling["capture_order"][0]
        for kind in ("symlink", "extra", "missing"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as raw:
                attempt = Path(raw) / "bundle"
                stage_synthetic_units(attempt, cfg, sampling, arms, replays, 1)
                staging = attempt / RUNNER.CAPTURE_STAGING_NAME
                names = RUNNER.staging_unit_names(0, unit_id)
                if kind == "symlink":
                    (staging / names["arms"]).unlink()
                    os.symlink("missing-target", staging / names["arms"])
                elif kind == "extra":
                    (staging / "extra").write_text("x", encoding="utf-8")
                else:
                    (staging / names["manifest"]).unlink()
                with self.assertRaises((AssertionError, OSError)):
                    RUNNER.reload_staged_units(attempt, sampling, cfg, 1)

    def test_shared_trigger_prefix_absorbing_suffix_retry_suffix_and_no_trigger(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=True)
        projected = RUNNER.project_all(cfg, sampling, arms, replays)
        units = {(row["unit_id"], row["method"]): row for row in projected["units"]}
        for unit in sampling["units"]:
            a = units[(unit["unit_id"], "ahcms_absorbing")]
            r = units[(unit["unit_id"], "hcms_retry_removal")]
            self.assertEqual(a["no_fit_trigger_slot"], 2)
            self.assertEqual(a["post_trigger_path_count"], 0)
            self.assertGreater(r["post_trigger_path_count"], 0)
            self.assertEqual(a["selected_occurrence_ids"], r["selected_occurrence_ids"][: len(a["selected_occurrence_ids"])])
            a_paths = [row for row in projected["paths"] if row["unit_id"] == unit["unit_id"] and row["method"] == "ahcms_absorbing"]
            r_paths = [row for row in projected["paths"] if row["unit_id"] == unit["unit_id"] and row["method"] == "hcms_retry_removal"]
            for primary_paths in (a_paths, r_paths):
                self.assertEqual((primary_paths[1]["returned_prefix"], primary_paths[1]["outcome"], primary_paths[1]["state_after"]), (0, "drop_ledger_no_fit", 1))
            self.assertEqual(r_paths[2]["proposed_arm"], 1)
        no_trigger_arms, no_trigger_replays = synthetic_complete_table(cfg, sampling, trigger=False)
        no_trigger = RUNNER.project_all(cfg, sampling, no_trigger_arms, no_trigger_replays)
        no_units = {(row["unit_id"], row["method"]): row for row in no_trigger["units"]}
        for unit in sampling["units"]:
            self.assertEqual(no_units[(unit["unit_id"], "ahcms_absorbing")], {**no_units[(unit["unit_id"], "hcms_retry_removal")], "method": "ahcms_absorbing"})

    def test_strict_generation_and_overage_boundaries(self) -> None:
        budget = 2_000_000_000
        self.assertTrue(RUNNER.generation_admits(budget - 100_000_001, budget))
        self.assertFalse(RUNNER.generation_admits(budget - 100_000_000, budget))
        self.assertFalse(RUNNER.overage(budget, budget))
        self.assertTrue(RUNNER.overage(budget + 1, budget))

    def test_cumulative_replay_admission_at_equality_and_just_over(self) -> None:
        budget = 2_000_000_000
        self.assertTrue(RUNNER.replay_admits(4_000_000_000, 4_000_000_000, budget))
        self.assertFalse(RUNNER.replay_admits(4_000_000_000, 4_000_000_001, budget))
        self.assertEqual(RUNNER.replay_charge_qns(100, 20), 1_000)

    def test_longest_fitting_exact_prefix_salvage_and_fixed24_no_salvage(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=False)
        for arm in arms:
            if arm["arm"] == 24 and arm["slot"] == 1:
                arm["cumulative_costs_ns"] = [100_000_000] * 23 + [200_000_000]
                arm["g_ns"] = 600_000_000
            elif arm["arm"] == 24 and arm["slot"] == 2:
                arm["cumulative_costs_ns"] = [100_000_000] * 8 + [500_000_000] * 16
                arm["g_ns"] = 600_000_000
        projected = RUNNER.project_all(cfg, sampling, arms, replays)
        unit_id = sampling["units"][0]["unit_id"]
        for method in ("ahcms_absorbing", "hcms_retry_removal"):
            paths = [row for row in projected["paths"] if row["unit_id"] == unit_id and row["method"] == method]
            self.assertEqual((paths[1]["returned_prefix"], paths[1]["outcome"], paths[1]["no_fit_trigger"]), (8, "accepted", False))
        fixed24 = [row for row in projected["paths"] if row["unit_id"] == unit_id and row["method"] == "fixed24_no_salvage_absorbing"]
        self.assertNotEqual(fixed24[1]["returned_prefix"], 8)

    def test_exact24_false_exact8_true_selects8_but_fixed24_drops(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=False)
        target = next(row for row in arms if row["unit_id"] == sampling["units"][0]["unit_id"] and row["slot"] == 1 and row["arm"] == 24)
        target["trace_suffixes"][8] = []
        target["generation_trace"] = {"user_messages": target["messages"], "tool_events": [event for suffix in target["trace_suffixes"] for event in suffix]}
        target["exact_flags"][8] = False
        target["eligible_prefixes"] = [8, 1]
        removed_id = target["occurrence_ids"].pop("24")
        replays = [row for row in replays if row["occurrence_id"] != removed_id]
        projected = RUNNER.project_all(cfg, sampling, arms, replays)
        unit_id = sampling["units"][0]["unit_id"]
        primary = next(row for row in projected["paths"] if row["unit_id"] == unit_id and row["method"] == "ahcms_absorbing")
        fixed24 = next(row for row in projected["paths"] if row["unit_id"] == unit_id and row["method"] == "fixed24_no_salvage_absorbing")
        self.assertEqual((primary["returned_prefix"], primary["outcome"]), (8, "accepted"))
        self.assertEqual((fixed24["returned_prefix"], fixed24["outcome"], fixed24["state_after"]), (0, "drop_exact_ineligible", 24))

    def test_sdk_set_aware_raw_duplicate_elapsed_and_per_unit_tail_identity(self) -> None:
        finding = {"predicates": [{"severity": 5}], "score_cell_signature": {"hash": "same"}}
        self.assertEqual(RUNNER.score_raw_int([finding]), 18)
        self.assertEqual(RUNNER.score_raw_int([finding, deepcopy(finding)]), 34)
        self.assertNotEqual(RUNNER.score_raw_int([finding]) * 2, RUNNER.score_raw_int([finding, deepcopy(finding)]))
        self.assertEqual(sum([7, 7]), 14)
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling)
        projected = RUNNER.project_all(cfg, sampling, arms, replays)
        for unit_id in {row["unit_id"] for row in projected["units"]}:
            a = next(row for row in projected["units"] if row["unit_id"] == unit_id and row["method"] == "ahcms_absorbing")
            r = next(row for row in projected["units"] if row["unit_id"] == unit_id and row["method"] == "hcms_retry_removal")
            self.assertEqual(r["R_raw"], a["R_raw"] + (r["R_raw"] - a["R_raw"]))

    def test_nominal_retention_tail_half_tail_and_zero_branches(self) -> None:
        cfg = config()
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, t_a=100, raw_r=100, t_r=110))
        self.assertEqual(predicate_map(rows)["nominal"]["status"], "PASS")
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, t_a=100, raw_r=100, t_r=109))
        self.assertEqual(predicate_map(rows)["nominal"]["status"], "FAIL")

    def test_exact_prediction_ledger_metrics_and_terminal_lines(self) -> None:
        cfg = config()
        metrics, _, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, t_a=80, raw_r=100, t_r=100))
        self.assertEqual({row["metric"] for row in metrics}, set(RUNNER.LEDGER_METRIC_NAMES))
        by_name = {row["metric"]: row for row in metrics}
        self.assertEqual((by_name["ahcms_to_retry_efficiency_ratio"]["numerator"], by_name["ahcms_to_retry_efficiency_ratio"]["denominator"], by_name["ahcms_to_retry_efficiency_ratio"]["value"]), (10_000, 8_000, "1.250000000000"))
        self.assertEqual((by_name["retry_tail_elapsed_fraction"]["numerator"], by_name["retry_tail_elapsed_fraction"]["denominator"]), (20, 100))
        self.assertEqual((by_name["half_discounted_retry_tail_elapsed_fraction"]["numerator"], by_name["half_discounted_retry_tail_elapsed_fraction"]["denominator"]), (10, 90))
        lines = RUNNER.ledger_metric_lines(metrics)
        self.assertEqual(lines[0], "ahcms_to_retry_efficiency_ratio: 1.250000000000")
        self.assertEqual(len(lines), 11)
        zero_metrics, _, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=0, raw_r=0, fixed8=(0, 100, 0, 0), fixed24=(0, 100, 0, 0)))
        zero = {row["metric"]: row for row in zero_metrics}
        self.assertEqual(zero["ahcms_to_retry_efficiency_ratio"]["value"], "NA_zero_retry_raw")
        self.assertEqual(zero["ahcms_to_fixed8_efficiency_ratio"]["value"], "NA_zero_simple_raw")
        infeasible_metrics, _, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(fixed8=(90, 100, 1, 0)))
        infeasible = {row["metric"]: row for row in infeasible_metrics}
        self.assertEqual(infeasible["ahcms_to_fixed8_efficiency_ratio"]["value"], "NA_infeasible_simple")
        invalid_fixture = decision_fixture()
        invalid_fixture["validity_errors"] = ["synthetic invalidity"]
        invalid_metrics, _, _ = RUNNER.aggregate_and_decide(cfg, invalid_fixture)
        invalid = {row["metric"]: row for row in invalid_metrics}
        self.assertEqual(invalid["ahcms_to_retry_efficiency_ratio"]["value"], "NA_invalid")
        self.assertEqual(invalid["invalidity_count"]["value"], "1")
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling, trigger=False)
        with tempfile.TemporaryDirectory() as raw:
            attempt = Path(raw) / "bundle"
            loaded = write_synthetic_bundle(attempt, cfg, sampling, arms, replays)
            metric = next(row for row in loaded["metrics"] if row["metric"] == "ahcms_to_retry_efficiency_ratio")
            self.assertEqual((metric["numerator"], metric["denominator"], metric["value"]), (400_204_800_000_000, 400_204_800_000_000, "1.000000000000"))
            log_path = attempt / "run.log"
            log_path.write_text(log_path.read_text().replace("ahcms_to_retry_efficiency_ratio: 1.000000000000", "ahcms_to_retry_efficiency_ratio: 9.000000000000"), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "run.log prediction metrics drift"):
                RUNNER.reload_and_validate_bundle(attempt, cfg, require_metric_log=True)
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=995, raw_r=1000, t_a=80, t_r=100))
        self.assertEqual(predicate_map(rows)["retention"]["status"], "PASS")
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=994, raw_r=1000, t_a=80, t_r=101))
        mapped = predicate_map(rows)
        self.assertEqual(mapped["retention"]["status"], "FAIL")
        self.assertIn("H=10", mapped["half_tail_efficiency"]["detail"])
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, raw_r=100, t_a=90, t_r=100))
        self.assertEqual(predicate_map(rows)["nominal_tail"]["status"], "PASS")
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, raw_r=100, t_a=91, t_r=100))
        self.assertEqual(predicate_map(rows)["nominal_tail"]["status"], "FAIL")
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, raw_r=100, t_a=100, t_r=120))
        mapped = predicate_map(rows)
        self.assertEqual(mapped["half_tail_efficiency"]["status"], "PASS")
        self.assertEqual(mapped["half_tail_efficiency"]["lhs"], mapped["half_tail_efficiency"]["rhs"])
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, raw_r=100, t_a=100, t_r=119))
        self.assertEqual(predicate_map(rows)["half_tail_efficiency"]["status"], "FAIL")
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, raw_r=100, t_a=90, t_r=110))
        mapped = predicate_map(rows)
        self.assertEqual(mapped["half_tail_support"]["status"], "PASS")
        self.assertEqual(mapped["half_tail_support"]["lhs"], mapped["half_tail_support"]["rhs"])
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=100, raw_r=100, t_a=90, t_r=109))
        self.assertEqual(predicate_map(rows)["half_tail_support"]["status"], "FAIL")
        _, rows, decision = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=0, raw_r=0))
        self.assertEqual(decision, "DISCONFIRM")
        self.assertEqual(predicate_map(rows)["positive_retry_raw"]["detail"], "NA_zero_retry_raw")
        _, rows, decision = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=0, raw_r=1))
        self.assertEqual(decision, "DISCONFIRM")
        self.assertEqual(predicate_map(rows)["nominal"]["status"], "FAIL")

    def test_simple_feasibility_pareto_and_zero_zero_cross_product(self) -> None:
        cfg = config()
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(fixed8=(90, 100, 1, 0)))
        self.assertEqual(predicate_map(rows)["fixed8_gate"]["status"], "PASS")
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(fixed8=(101, 79, 0, 0)))
        self.assertEqual(predicate_map(rows)["fixed8_gate"]["status"], "FAIL")
        _, rows, decision = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=0, raw_r=1, fixed8=(0, 79, 0, 0)))
        self.assertEqual(decision, "DISCONFIRM")
        self.assertIn("rho_simple=NA_zero_simple_raw", predicate_map(rows)["fixed8_gate"]["detail"])
        self.assertEqual(predicate_map(rows)["fixed8_gate"]["status"], "FAIL")
        _, rows, _ = RUNNER.aggregate_and_decide(cfg, decision_fixture(raw_a=0, raw_r=1, fixed8=(0, 80, 0, 0)))
        fixed8 = predicate_map(rows)["fixed8_gate"]
        self.assertEqual((fixed8["lhs"], fixed8["rhs"], fixed8["status"]), ("0", "0", "PASS"))

    def test_exact_capture_projection_grids_and_malformed_rejection(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling)
        projected = RUNNER.project_all(cfg, sampling, arms, replays)
        self.assertEqual(len(arms), 9 * 16 * 3)
        self.assertEqual(len(replays), 9 * 16 * 6)
        self.assertEqual(len(projected["units"]), 36)
        for mutation in ("missing", "duplicate", "extra"):
            changed = deepcopy(arms)
            if mutation == "missing":
                changed.pop()
            elif mutation == "duplicate":
                changed.append(deepcopy(changed[0]))
            else:
                changed[0]["arm"] = 999
            with self.assertRaises(AssertionError):
                RUNNER.project_all(cfg, sampling, changed, replays)
        malformed = deepcopy(arms)
        malformed[0]["g_ns"] = True
        with self.assertRaises(AssertionError):
            RUNNER.project_all(cfg, sampling, malformed, replays)
        for mutation in ("missing", "duplicate", "extra", "malformed"):
            changed = deepcopy(replays)
            if mutation == "missing":
                changed.pop()
            elif mutation == "duplicate":
                changed.append(deepcopy(changed[0]))
            elif mutation == "extra":
                changed[0]["occurrence_id"] = "not-joined"
            else:
                changed[0]["ell_ns"] = -1
            with self.assertRaises(AssertionError):
                RUNNER.project_all(cfg, sampling, arms, changed)

    def test_timer_landmark_source_order_and_zero_interaction_endpoint(self) -> None:
        hashes = RUNNER.verify_timer_source_order()
        self.assertEqual(set(hashes), {"generation", "replay"})
        class EmptyEnv:
            def reset(self):
                return None
            def export_trace_dict(self):
                return {"user_messages": [], "tool_events": []}
        arm = {
            "eligible_prefixes": [1], "occurrence_ids": {"1": "toy"},
            "messages": [], "hosts": [],
            "unit_id": "toy", "slot": 1, "arm": 1, "master": 7, "profile": "toy",
            "input_identity": "identity",
        }
        row = RUNNER.capture_replay_occurrence(
            arm,
            1,
            {"id": "toy"},
            env_builder=lambda _factory, _seed: EmptyEnv(),
            factory_builder=lambda _profile: (lambda: None),
        )
        self.assertEqual(row["trace_suffixes"], [])
        self.assertGreaterEqual(row["ell_ns"], 0)
        self.assertEqual(row["replay_end_landmark"], RUNNER.REPLAY_LANDMARKS[-1])

    def test_attempt_refusal_symlink_dangling_and_complete_last_hash(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "experiments/runs").mkdir(parents=True)
            relative = Path("experiments/runs/toy")
            attempt = RUNNER.create_attempt_transaction(relative, root, relative, "toy command")
            self.assertEqual((attempt / "run.log").read_text(), "toy command\n")
            with self.assertRaises(AssertionError):
                RUNNER.create_attempt_transaction(relative, root, relative, "toy command")
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "experiments/runs").mkdir(parents=True)
            relative = Path("experiments/runs/toy")
            os.symlink("missing-target", root / relative)
            with self.assertRaisesRegex(AssertionError, "dangling alias"):
                RUNNER.create_attempt_transaction(relative, root, relative, "toy")
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "experiments").mkdir()
            target = root / "real-runs"
            target.mkdir()
            os.symlink(target, root / "experiments/runs")
            relative = Path("experiments/runs/toy")
            with self.assertRaisesRegex(AssertionError, "symlink/non-directory"):
                RUNNER.create_attempt_transaction(relative, root, relative, "toy")
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling)
        with tempfile.TemporaryDirectory() as raw:
            attempt = Path(raw) / "bundle"
            loaded = write_synthetic_bundle(attempt, cfg, sampling, arms, replays, complete=True)
            manifest = RUNNER.validate_complete_manifest(attempt, "synthetic command")
            self.assertEqual(manifest["decision"], loaded["decision"])
            with (attempt / "metrics.jsonl").open("a", encoding="utf-8") as handle:
                handle.write("{}\n")
            with self.assertRaisesRegex(AssertionError, "artifact hash drift"):
                RUNNER.validate_complete_manifest(attempt, "synthetic command")

    def test_independent_reload_detects_each_semantic_tamper(self) -> None:
        cfg = config()
        sampling = synthetic_sampling(cfg)
        arms, replays = synthetic_complete_table(cfg, sampling)
        cases = {
            "duration": ("generation_arms.jsonl", lambda rows: rows[0].__setitem__("g_ns", rows[0]["g_ns"] + 1)),
            "arm_outcome": ("generation_arms.jsonl", lambda rows: rows[0].__setitem__("outcome", "exact_ineligible")),
            "replay": ("replay_occurrences.jsonl", lambda rows: rows[0].__setitem__("ell_ns", rows[0]["ell_ns"] + 1)),
            "accepted": ("accepted_occurrences.jsonl", lambda rows: rows[0].__setitem__("ell_ns", rows[0]["ell_ns"] + 1)),
            "method_raw": ("method_units.jsonl", lambda rows: rows[0].__setitem__("R_raw", rows[0]["R_raw"] + 1)),
            "metric": ("metrics.jsonl", lambda rows: rows[0].__setitem__("value", "tampered")),
            "decision": ("decisions.jsonl", lambda rows: rows[0].__setitem__("status", "FAIL" if rows[0]["status"] != "FAIL" else "PASS")),
        }
        for name, (artifact, mutate) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as raw:
                attempt = Path(raw) / "bundle"
                write_synthetic_bundle(attempt, cfg, sampling, arms, replays)
                fields, schema = RUNNER.JSONL_SPECS[artifact]
                rows = RUNNER.read_jsonl_exact(attempt / artifact, fields, schema)
                mutate(rows)
                (attempt / artifact).write_text("".join(RUNNER.canonical_json(row) + "\n" for row in rows), encoding="utf-8")
                if artifact in {"generation_arms.jsonl", "replay_occurrences.jsonl"}:
                    checkpoint_path = attempt / "capture_checkpoints.json"
                    checkpoints = RUNNER.read_json_exact(checkpoint_path)
                    loaded_arms = rows if artifact == "generation_arms.jsonl" else RUNNER.read_jsonl_exact(attempt / "generation_arms.jsonl", *RUNNER.JSONL_SPECS["generation_arms.jsonl"])
                    loaded_replays = rows if artifact == "replay_occurrences.jsonl" else RUNNER.read_jsonl_exact(attempt / "replay_occurrences.jsonl", *RUNNER.JSONL_SPECS["replay_occurrences.jsonl"])
                    checkpoints["records"] = capture_checkpoints(sampling, loaded_arms, loaded_replays)
                    checkpoint_path.write_text(RUNNER.canonical_json(checkpoints) + "\n", encoding="utf-8")
                with self.assertRaises(AssertionError):
                    RUNNER.reload_and_validate_bundle(attempt, cfg)

    def test_scientific_factory_capture_tripwire_and_canonical_absence(self) -> None:
        original = (RUNNER.make_env, RUNNER.profile_factory, RUNNER.capture_scientific_units)
        def forbidden(*_args, **_kwargs):
            raise AssertionError("scientific factory/capture invoked by synthetic tests")
        RUNNER.make_env = forbidden
        RUNNER.profile_factory = forbidden
        RUNNER.capture_scientific_units = forbidden
        try:
            cfg = config()
            sampling = synthetic_sampling(cfg)
            arms, replays = synthetic_complete_table(cfg, sampling)
            projected = RUNNER.project_all(cfg, sampling, arms, replays)
            self.assertEqual(len(projected["units"]), 36)
        finally:
            RUNNER.make_env, RUNNER.profile_factory, RUNNER.capture_scientific_units = original
        self.assertFalse(CANONICAL_ATTEMPT.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
