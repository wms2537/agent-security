"""Auditable four-policy resource profile for round-13 DBER repair.

This is a controlled real-SDK mock profile. It measures generation episodes,
replays every incumbent/probe candidate through a fresh official environment,
scores only through official predicates/signatures/scoring, and compares:

  incumbent, headroom_only, generation_gated, bank_all.

The frozen population and decision rules are in research-log/217, amended only
by the pre-execution URL parser correction in research-log/218.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
import time
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SDK = ROOT / "comp" / "sdk"
sys.path.insert(0, str(SDK))
sys.path.insert(0, str(HERE))

from aicomp_sdk.attacks.contracts import AttackRunConfig  # noqa: E402
from aicomp_sdk.core.cells import cell_signature  # noqa: E402
from aicomp_sdk.core.env.api import EnvSelection  # noqa: E402
from aicomp_sdk.core.predicates import eval_predicates  # noqa: E402
from aicomp_sdk.evaluation.ops import build_attack_env  # noqa: E402
from aicomp_sdk.guardrails import OptimalGuardrail  # noqa: E402
from aicomp_sdk.scoring import score_attack_raw  # noqa: E402
from mock_agents import AmortizingAgent, IndexSplitLatencyAgent  # noqa: E402


ALPHA = 2.0
SEEDS = (41, 42, 43)
POLICIES = ("incumbent", "headroom_only", "generation_gated", "bank_all")

BASE_CONFIG: dict[str, Any] = {
    "probe_reps": 5,
    "probe_time_cap_s": 0.90,
    "min_fire_rate": 0.2,
    "replay_safe": 0.99,
    "cost_inflation": 1.0,
    "gen_margin_s": 0.05,
    "enable_multi_message": True,
    "multi_probe_reps": 2,
    "multi_probe_messages": 6,
    "multi_fill_messages": 24,
    "multi_min_fire_fraction": 0.75,
    "multi_rate_gain": 1.10,
    "enable_scoc": False,
}

REGIMES: tuple[dict[str, Any], ...] = (
    {
        "name": "G",
        "description": "generation-wide",
        "agent": "amortizing",
        "time_budget_s": 4.00,
        "replay_budget_s": 6.00,
        "max_candidates": 200,
        "enable_multi_message": True,
        "expected_stop": "generation",
    },
    {
        "name": "R0",
        "description": "replay-bound-no-fit",
        "agent": "amortizing",
        "time_budget_s": 3.00,
        "replay_budget_s": 0.18,
        "max_candidates": 200,
        "enable_multi_message": True,
        "expected_stop": "replay",
    },
    {
        "name": "R1",
        "description": "replay-bound-residual-fit",
        "agent": "index_split",
        "time_budget_s": 3.00,
        "replay_budget_s": 0.18,
        "max_candidates": 200,
        "enable_multi_message": False,
        "expected_stop": "replay",
    },
    {
        "name": "K",
        "description": "candidate-bound",
        "agent": "amortizing",
        "time_budget_s": 3.00,
        "replay_budget_s": 6.00,
        "max_candidates": 3,
        "enable_multi_message": True,
        "expected_stop": "candidate",
    },
)

SOURCE_PATHS: tuple[Path, ...] = (
    HERE / "attack.py",
    HERE / "mock_agents.py",
    HERE / "dber_factorial_profile.py",
    HERE / "test_dber_factorial_profile.py",
    SDK / "aicomp_sdk" / "evaluation" / "ops.py",
    SDK / "aicomp_sdk" / "scoring.py",
    SDK / "aicomp_sdk" / "core" / "predicates.py",
    SDK / "aicomp_sdk" / "core" / "cells.py",
)

SUMMARY_FIELDS = (
    "unit_id",
    "regime",
    "seed",
    "expected_stop",
    "actual_stop",
    "valid",
    "errors",
    "incumbent_count",
    "inventory_count",
    "incumbent_raw",
    "headroom_only_raw",
    "generation_gated_raw",
    "bank_all_raw",
    "headroom_only_gain_raw",
    "generation_gated_gain_raw",
    "headroom_only_actual_cost_s",
    "generation_gated_actual_cost_s",
    "bank_all_actual_cost_s",
    "safe_cap_s",
    "hard_budget_s",
    "headroom_only_safe_overflow",
    "headroom_only_hard_overflow",
    "generation_gated_safe_overflow",
    "bank_all_safe_overflow",
    "bank_all_hard_overflow",
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha_path(path: Path) -> str:
    return _sha_bytes(path.read_bytes())


def _sha_json(value: Any) -> str:
    return _sha_bytes(_canonical_json(value).encode("utf-8"))


def _message_signature(messages: Iterable[str]) -> str:
    return _sha_json(list(messages))


def _load_attack_module():
    path = HERE / "attack.py"
    spec = importlib.util.spec_from_file_location("dber_factorial_attack", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load attack module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["dber_factorial_attack"] = module
    spec.loader.exec_module(module)
    return module


def _agent_factory(agent_name: str) -> Callable[[], Any]:
    if agent_name == "amortizing":
        return lambda: AmortizingAgent(
            fixed_latency_s=0.015,
            per_action_latency_s=0.001,
        )
    if agent_name == "index_split":
        return lambda: IndexSplitLatencyAgent(
            probe_action_latency_s=0.002,
            fill_action_latency_s=0.020,
        )
    raise ValueError(f"unknown agent {agent_name!r}")


def _finding_from_trace(trace: Mapping[str, Any]) -> dict[str, Any]:
    predicates = eval_predicates(trace)
    tool_events = list(trace.get("tool_events", []))
    user_messages = list(trace.get("user_messages", []))
    return {
        "seed": int(trace["seed"]),
        "user_messages": user_messages,
        "trace": dict(trace),
        "predicates": predicates,
        "cell_signature": cell_signature(
            tool_events,
            egress_data=list(trace.get("egress", [])),
            user_messages=user_messages,
        ),
        "score_cell_signature": cell_signature(tool_events),
    }


def _raw(findings: Iterable[Mapping[str, Any]]) -> float:
    return float(score_attack_raw(list(findings)))


class TracingEnv:
    """Transparent generation env that persists complete episode evidence."""

    def __init__(self, base: Any) -> None:
        self.base = base
        self.episodes: list[dict[str, Any]] = []
        self._start: float | None = None
        self._messages: list[str] = []

    def reset(self) -> Any:
        if self._start is not None:
            raise RuntimeError("reset before previous episode export")
        self._start = time.monotonic()
        self._messages = []
        return self.base.reset()

    def interact(self, message: str, *, max_tool_hops: int) -> Any:
        if self._start is None:
            raise RuntimeError("interact before reset")
        self._messages.append(str(message))
        return self.base.interact(message, max_tool_hops=max_tool_hops)

    def export_trace_dict(self) -> dict[str, Any]:
        if self._start is None:
            raise RuntimeError("export before reset")
        trace = self.base.export_trace_dict()
        elapsed_s = max(1e-9, time.monotonic() - self._start)
        finding = _finding_from_trace(trace)
        messages = list(self._messages)
        if messages != list(trace.get("user_messages", [])):
            raise RuntimeError("tracing messages differ from exported trace")
        self.episodes.append(
            {
                "messages": messages,
                "message_signature": _message_signature(messages),
                "elapsed_s": elapsed_s,
                "trace": trace,
                "trace_sha256": _sha_json(trace),
                "finding": finding,
                "isolated_raw": _raw([finding]),
            }
        )
        self._start = None
        self._messages = []
        return trace

    def __getattr__(self, name: str) -> Any:
        return getattr(self.base, name)


@dataclass
class CandidateRecord:
    unit_id: str
    source_phase: str
    messages: list[str]
    message_signature: str
    generation_elapsed_s: float
    generation_trace: dict[str, Any]
    generation_trace_sha256: str
    generation_finding: dict[str, Any]
    generation_isolated_raw: float
    replay_elapsed_s: float
    replay_trace: dict[str, Any]
    replay_trace_sha256: str
    replay_finding: dict[str, Any]
    replay_isolated_raw: float
    policy_decisions: dict[str, dict[str, Any]]

    def json_row(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "source_phase": self.source_phase,
            "messages": self.messages,
            "message_signature": self.message_signature,
            "generation_elapsed_s": self.generation_elapsed_s,
            "generation_trace": self.generation_trace,
            "generation_trace_sha256": self.generation_trace_sha256,
            "generation_predicates": self.generation_finding["predicates"],
            "generation_cell_signature": self.generation_finding["cell_signature"],
            "generation_score_cell_signature": self.generation_finding[
                "score_cell_signature"
            ],
            "generation_isolated_raw": self.generation_isolated_raw,
            "replay_elapsed_s": self.replay_elapsed_s,
            "replay_trace": self.replay_trace,
            "replay_trace_sha256": self.replay_trace_sha256,
            "replay_predicates": self.replay_finding["predicates"],
            "replay_cell_signature": self.replay_finding["cell_signature"],
            "replay_score_cell_signature": self.replay_finding[
                "score_cell_signature"
            ],
            "replay_isolated_raw": self.replay_isolated_raw,
            "policy_decisions": self.policy_decisions,
        }


def _fresh_replay(
    *,
    messages: list[str],
    seed: int,
    agent_factory: Callable[[], Any],
) -> tuple[float, dict[str, Any], dict[str, Any]]:
    started = time.monotonic()
    replay_env = build_attack_env(
        seed=seed,
        fixtures_dir=SDK / "aicomp_sdk" / "fixtures",
        agent_factory=agent_factory,
        guardrail=OptimalGuardrail(),
        env_selection=EnvSelection.SANDBOX,
        max_tool_hops=8,
    )
    replay_env.reset()
    for message in messages:
        replay_env.interact(message, max_tool_hops=8)
    trace = replay_env.export_trace_dict()
    finding = _finding_from_trace(trace)
    elapsed_s = max(1e-9, time.monotonic() - started)
    return elapsed_s, trace, finding


def _marginal_generation_raw(
    prefix: list[CandidateRecord],
    item: CandidateRecord,
) -> float:
    before = _raw(row.generation_finding for row in prefix)
    after = _raw(
        [*(row.generation_finding for row in prefix), item.generation_finding]
    )
    return after - before


def _headroom_selection(
    incumbent: list[CandidateRecord],
    inventory: list[CandidateRecord],
    *,
    cap: int,
    safe_cap_s: float,
) -> tuple[list[CandidateRecord], dict[str, dict[str, Any]]]:
    selected = list(incumbent)
    decisions: dict[str, dict[str, Any]] = {
        row.message_signature: {
            "admitted": True,
            "reason": "incumbent",
            "marginal_generation_raw": None,
            "stressed_generation_cost_s": None,
        }
        for row in incumbent
    }
    base_cost_s = sum(row.generation_elapsed_s for row in incumbent)
    supplement_cost_s = 0.0
    remaining = list(inventory)

    while remaining and len(selected) < cap:
        ranked: list[tuple[float, float, str, float, CandidateRecord]] = []
        for row in remaining:
            marginal = _marginal_generation_raw(selected, row)
            stressed = ALPHA * row.generation_elapsed_s
            if marginal <= 0.0 or not math.isfinite(stressed) or stressed <= 0.0:
                continue
            ranked.append(
                (
                    -(marginal / stressed),
                    stressed,
                    row.message_signature,
                    marginal,
                    row,
                )
            )
        ranked.sort(key=lambda value: (value[0], value[1], value[2]))
        admitted: tuple[float, float, str, float, CandidateRecord] | None = None
        for candidate in ranked:
            if base_cost_s + supplement_cost_s + candidate[1] <= safe_cap_s + 1e-12:
                admitted = candidate
                break
        if admitted is None:
            break
        _, stressed, _, marginal, row = admitted
        selected.append(row)
        supplement_cost_s += stressed
        remaining.remove(row)
        decisions[row.message_signature] = {
            "admitted": True,
            "reason": "positive_marginal_fits_stressed_headroom",
            "marginal_generation_raw": marginal,
            "stressed_generation_cost_s": stressed,
        }

    selected_signatures = {row.message_signature for row in selected}
    for row in inventory:
        if row.message_signature in selected_signatures:
            continue
        marginal = _marginal_generation_raw(selected, row)
        stressed = ALPHA * row.generation_elapsed_s
        if len(selected) >= cap:
            reason = "candidate_cap"
        elif marginal <= 0.0:
            reason = "nonpositive_marginal"
        else:
            reason = "stressed_replay_headroom"
        decisions[row.message_signature] = {
            "admitted": False,
            "reason": reason,
            "marginal_generation_raw": marginal,
            "stressed_generation_cost_s": stressed,
        }
    return selected, decisions


def _bank_all_selection(
    incumbent: list[CandidateRecord],
    inventory: list[CandidateRecord],
    *,
    cap: int,
) -> tuple[list[CandidateRecord], dict[str, dict[str, Any]]]:
    selected = list(incumbent)
    decisions: dict[str, dict[str, Any]] = {
        row.message_signature: {
            "admitted": True,
            "reason": "incumbent",
            "marginal_generation_raw": None,
            "stressed_generation_cost_s": None,
        }
        for row in incumbent
    }
    for row in sorted(inventory, key=lambda value: value.message_signature):
        if len(selected) >= cap:
            decisions[row.message_signature] = {
                "admitted": False,
                "reason": "candidate_cap",
                "marginal_generation_raw": None,
                "stressed_generation_cost_s": None,
            }
            continue
        if row.generation_isolated_raw <= 0.0:
            decisions[row.message_signature] = {
                "admitted": False,
                "reason": "nonpositive_isolated_raw",
                "marginal_generation_raw": None,
                "stressed_generation_cost_s": None,
            }
            continue
        selected.append(row)
        decisions[row.message_signature] = {
            "admitted": True,
            "reason": "positive_isolated_raw_no_cost_guard",
            "marginal_generation_raw": _marginal_generation_raw(selected[:-1], row),
            "stressed_generation_cost_s": None,
        }
    return selected, decisions


def _portfolio_metrics(
    selected: list[CandidateRecord],
    *,
    safe_cap_s: float,
    hard_budget_s: float,
    cap: int,
) -> dict[str, Any]:
    raw = _raw(row.replay_finding for row in selected)
    actual_cost_s = sum(row.replay_elapsed_s for row in selected)
    return {
        "signatures": [row.message_signature for row in selected],
        "count": len(selected),
        "raw": raw,
        "actual_replay_cost_s": actual_cost_s,
        "safe_cap_overflow": actual_cost_s > safe_cap_s + 1e-12,
        "hard_budget_overflow": actual_cost_s > hard_budget_s + 1e-12,
        "candidate_overflow": len(selected) > cap,
    }


def _profile_unit(
    module: Any,
    regime: Mapping[str, Any],
    seed: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    unit_id = f"{regime['name']}-seed{seed}"
    config = dict(BASE_CONFIG)
    config.update(
        {
            "replay_budget_s": float(regime["replay_budget_s"]),
            "max_candidates": int(regime["max_candidates"]),
            "enable_multi_message": bool(regime["enable_multi_message"]),
        }
    )
    agent_factory = _agent_factory(str(regime["agent"]))
    base = build_attack_env(
        seed=seed,
        fixtures_dir=SDK / "aicomp_sdk" / "fixtures",
        agent_factory=agent_factory,
        guardrail=OptimalGuardrail(),
        env_selection=EnvSelection.SANDBOX,
        max_tool_hops=8,
    )
    env = TracingEnv(base)
    attack = module.AttackAlgorithm(config)
    candidates = attack.run(
        env,
        AttackRunConfig(
            time_budget_s=float(regime["time_budget_s"]),
            max_tool_hops=8,
        ),
    )

    required_debug = {
        "fill_stop_reason",
        "fill_terminal_candidate_count",
        "fill_terminal_candidate_cap",
        "fill_terminal_replay_cost_s",
        "fill_terminal_unit_cost_s",
        "fill_terminal_safe_cap_s",
        "fill_clamp_removed",
    }
    missing_debug = required_debug.difference(attack.debug)
    if missing_debug:
        raise RuntimeError(f"{unit_id}: missing stop instrumentation {sorted(missing_debug)}")

    recorded_single_probes = sum(
        int(row["n"]) for row in attack.debug["probes"].values()
    )
    multi_probes = len(attack.debug["multi_probe_events"])
    scoc_probes = len(attack.debug["scoc_probe_events"])
    prefill_episodes = 1 + recorded_single_probes + multi_probes + scoc_probes
    if len(env.episodes) < prefill_episodes:
        raise RuntimeError(
            f"{unit_id}: episodes={len(env.episodes)} < prefill={prefill_episodes}"
        )

    returned_signatures = [
        _message_signature(list(candidate.user_messages)) for candidate in candidates
    ]
    if len(returned_signatures) != len(set(returned_signatures)):
        raise RuntimeError(f"{unit_id}: duplicate incumbent signatures")

    episodes_by_signature: dict[str, dict[str, Any]] = {}
    for index, episode in enumerate(env.episodes):
        signature = str(episode["message_signature"])
        if signature in episodes_by_signature:
            raise RuntimeError(f"{unit_id}: duplicate generation episode {signature}")
        if index == 0:
            episode["source_phase"] = "cold_start_probe"
        elif index < 1 + recorded_single_probes:
            episode["source_phase"] = "template_probe"
        elif index < prefill_episodes:
            episode["source_phase"] = "structure_probe"
        else:
            episode["source_phase"] = "verified_fill"
        episodes_by_signature[signature] = episode

    missing_returned = set(returned_signatures).difference(episodes_by_signature)
    if missing_returned:
        raise RuntimeError(
            f"{unit_id}: {len(missing_returned)} returned candidates lack episodes"
        )

    inventory_signatures: list[str] = []
    seen_inventory: set[str] = set()
    for episode in env.episodes[:prefill_episodes]:
        signature = str(episode["message_signature"])
        if (
            float(episode["isolated_raw"]) <= 0.0
            or signature in returned_signatures
            or signature in seen_inventory
        ):
            continue
        inventory_signatures.append(signature)
        seen_inventory.add(signature)

    all_signatures = [*returned_signatures, *inventory_signatures]
    records: dict[str, CandidateRecord] = {}
    for signature in all_signatures:
        episode = episodes_by_signature[signature]
        replay_elapsed_s, replay_trace, replay_finding = _fresh_replay(
            messages=list(episode["messages"]),
            seed=seed,
            agent_factory=agent_factory,
        )
        records[signature] = CandidateRecord(
            unit_id=unit_id,
            source_phase=str(episode["source_phase"]),
            messages=list(episode["messages"]),
            message_signature=signature,
            generation_elapsed_s=float(episode["elapsed_s"]),
            generation_trace=dict(episode["trace"]),
            generation_trace_sha256=str(episode["trace_sha256"]),
            generation_finding=dict(episode["finding"]),
            generation_isolated_raw=float(episode["isolated_raw"]),
            replay_elapsed_s=replay_elapsed_s,
            replay_trace=replay_trace,
            replay_trace_sha256=_sha_json(replay_trace),
            replay_finding=replay_finding,
            replay_isolated_raw=_raw([replay_finding]),
            policy_decisions={},
        )

    incumbent = [records[signature] for signature in returned_signatures]
    inventory = [records[signature] for signature in inventory_signatures]
    cap = int(regime["max_candidates"])
    hard_budget_s = float(regime["replay_budget_s"])
    safe_cap_s = float(config["replay_safe"]) * hard_budget_s

    headroom, headroom_decisions = _headroom_selection(
        incumbent,
        inventory,
        cap=cap,
        safe_cap_s=safe_cap_s,
    )
    stop_reason = str(attack.debug["fill_stop_reason"])
    if stop_reason == "generation":
        gated = list(headroom)
        gated_decisions = {
            signature: dict(decision)
            for signature, decision in headroom_decisions.items()
        }
    else:
        gated = list(incumbent)
        gated_decisions = {
            row.message_signature: {
                "admitted": True,
                "reason": "incumbent",
                "marginal_generation_raw": None,
                "stressed_generation_cost_s": None,
            }
            for row in incumbent
        }
        for row in inventory:
            gated_decisions[row.message_signature] = {
                "admitted": False,
                "reason": f"stop_reason_{stop_reason}",
                "marginal_generation_raw": _marginal_generation_raw(incumbent, row),
                "stressed_generation_cost_s": ALPHA * row.generation_elapsed_s,
            }
    bank_all, bank_decisions = _bank_all_selection(incumbent, inventory, cap=cap)
    incumbent_decisions = {
        row.message_signature: {
            "admitted": True,
            "reason": "incumbent",
            "marginal_generation_raw": None,
            "stressed_generation_cost_s": None,
        }
        for row in incumbent
    }
    for row in inventory:
        incumbent_decisions[row.message_signature] = {
            "admitted": False,
            "reason": "discard_probe",
            "marginal_generation_raw": _marginal_generation_raw(incumbent, row),
            "stressed_generation_cost_s": None,
        }

    selections = {
        "incumbent": incumbent,
        "headroom_only": headroom,
        "generation_gated": gated,
        "bank_all": bank_all,
    }
    decisions = {
        "incumbent": incumbent_decisions,
        "headroom_only": headroom_decisions,
        "generation_gated": gated_decisions,
        "bank_all": bank_decisions,
    }
    metrics = {
        policy: _portfolio_metrics(
            selected,
            safe_cap_s=safe_cap_s,
            hard_budget_s=hard_budget_s,
            cap=cap,
        )
        for policy, selected in selections.items()
    }

    for record in records.values():
        record.policy_decisions = {
            policy: dict(policy_decisions[record.message_signature])
            for policy, policy_decisions in decisions.items()
        }

    errors: list[str] = []
    if stop_reason != str(regime["expected_stop"]):
        errors.append(
            f"stop:{stop_reason}!=expected:{regime['expected_stop']}"
        )
    if not inventory:
        errors.append("empty_inventory")
    for policy in POLICIES:
        if metrics[policy]["candidate_overflow"]:
            errors.append(f"{policy}:candidate_overflow")
    for policy in ("headroom_only", "generation_gated"):
        if metrics[policy]["safe_cap_overflow"]:
            errors.append(f"{policy}:safe_cap_overflow")
        if metrics[policy]["hard_budget_overflow"]:
            errors.append(f"{policy}:hard_budget_overflow")
    if regime["name"] == "G":
        if (
            metrics["headroom_only"]["signatures"]
            != metrics["generation_gated"]["signatures"]
        ):
            errors.append("G:headroom_gated_identity")
        if metrics["headroom_only"]["raw"] <= metrics["incumbent"]["raw"]:
            errors.append("G:no_positive_headroom_gain")
    if regime["name"] == "R0":
        for policy in ("headroom_only", "generation_gated"):
            if metrics[policy]["signatures"] != metrics["incumbent"]["signatures"]:
                errors.append(f"R0:{policy}_not_incumbent")
        if not metrics["bank_all"]["safe_cap_overflow"]:
            errors.append("R0:bank_all_no_safe_overflow")
    if regime["name"] == "R1":
        if metrics["headroom_only"]["raw"] <= metrics["incumbent"]["raw"]:
            errors.append("R1:no_positive_headroom_gain")
        if (
            metrics["generation_gated"]["signatures"]
            != metrics["incumbent"]["signatures"]
        ):
            errors.append("R1:gated_not_incumbent")
        if not metrics["bank_all"]["safe_cap_overflow"]:
            errors.append("R1:bank_all_no_safe_overflow")
    if regime["name"] == "K":
        for policy in ("headroom_only", "generation_gated"):
            if metrics[policy]["signatures"] != metrics["incumbent"]["signatures"]:
                errors.append(f"K:{policy}_not_incumbent")

    summary = {
        "unit_id": unit_id,
        "regime": str(regime["name"]),
        "description": str(regime["description"]),
        "seed": seed,
        "agent": str(regime["agent"]),
        "config": config,
        "time_budget_s": float(regime["time_budget_s"]),
        "hard_budget_s": hard_budget_s,
        "safe_cap_s": safe_cap_s,
        "candidate_cap": cap,
        "expected_stop": str(regime["expected_stop"]),
        "actual_stop": stop_reason,
        "stop_instrumentation": {
            key: attack.debug[key] for key in sorted(required_debug)
        },
        "episodes": len(env.episodes),
        "prefill_episodes": prefill_episodes,
        "incumbent_count": len(incumbent),
        "inventory_count": len(inventory),
        "policies": metrics,
        "errors": errors,
        "valid": not errors,
    }
    rows = [records[signature].json_row() for signature in all_signatures]
    return summary, rows


def _verify_artifacts(
    summary_path: Path,
    candidates_path: Path,
) -> dict[str, Any]:
    summary = json.loads(summary_path.read_text())
    if summary["contract"] != _contract():
        raise RuntimeError("artifact contract differs from current frozen sources")
    expected_order = _contract()["unit_order"]
    if [unit["unit_id"] for unit in summary["units"]] != expected_order:
        raise RuntimeError("unit population/order differs from frozen contract")
    candidate_rows = [
        json.loads(line)
        for line in candidates_path.read_text().splitlines()
        if line.strip()
    ]
    by_unit: dict[str, dict[str, dict[str, Any]]] = {}
    for row in candidate_rows:
        unit_rows = by_unit.setdefault(row["unit_id"], {})
        if row["message_signature"] in unit_rows:
            raise RuntimeError(
                f"{row['unit_id']}:{row['message_signature']}: duplicate row"
            )
        if _message_signature(row["messages"]) != row["message_signature"]:
            raise RuntimeError(
                f"{row['unit_id']}:{row['message_signature']}: message signature"
            )
        if _sha_json(row["generation_trace"]) != row["generation_trace_sha256"]:
            raise RuntimeError(
                f"{row['unit_id']}:{row['message_signature']}: generation trace hash"
            )
        if _sha_json(row["replay_trace"]) != row["replay_trace_sha256"]:
            raise RuntimeError(
                f"{row['unit_id']}:{row['message_signature']}: replay trace hash"
            )
        generation_finding = _finding_from_trace(row["generation_trace"])
        if generation_finding["predicates"] != row["generation_predicates"]:
            raise RuntimeError(
                f"{row['unit_id']}:{row['message_signature']}: generation predicates"
            )
        if (
            generation_finding["score_cell_signature"]
            != row["generation_score_cell_signature"]
        ):
            raise RuntimeError(
                f"{row['unit_id']}:{row['message_signature']}: generation score cell"
            )
        replay_finding = _finding_from_trace(row["replay_trace"])
        if replay_finding["predicates"] != row["replay_predicates"]:
            raise RuntimeError(
                f"{row['unit_id']}:{row['message_signature']}: replay predicates"
            )
        if (
            replay_finding["score_cell_signature"]
            != row["replay_score_cell_signature"]
        ):
            raise RuntimeError(
                f"{row['unit_id']}:{row['message_signature']}: replay score cell"
            )
        unit_rows[row["message_signature"]] = {
            "row": row,
            "finding": replay_finding,
        }

    checked = 0
    for unit in summary["units"]:
        unit_rows = by_unit[unit["unit_id"]]
        for policy in POLICIES:
            signatures = unit["policies"][policy]["signatures"]
            if len(signatures) > int(unit["candidate_cap"]):
                raise RuntimeError(f"{unit['unit_id']}:{policy}: candidate cap")
            for signature, payload in unit_rows.items():
                decision = payload["row"]["policy_decisions"][policy]
                if bool(decision["admitted"]) != (signature in signatures):
                    raise RuntimeError(
                        f"{unit['unit_id']}:{policy}:{signature}: decision mismatch"
                    )
            findings = [unit_rows[sig]["finding"] for sig in signatures]
            raw = _raw(findings)
            if abs(raw - float(unit["policies"][policy]["raw"])) > 1e-12:
                raise RuntimeError(
                    f"{unit['unit_id']}:{policy}: raw {raw} != "
                    f"{unit['policies'][policy]['raw']}"
                )
            replay_cost_s = sum(
                float(unit_rows[sig]["row"]["replay_elapsed_s"])
                for sig in signatures
            )
            if (
                abs(
                    replay_cost_s
                    - float(unit["policies"][policy]["actual_replay_cost_s"])
                )
                > 1e-12
            ):
                raise RuntimeError(f"{unit['unit_id']}:{policy}: replay cost")
            expected_safe_overflow = replay_cost_s > float(unit["safe_cap_s"]) + 1e-12
            expected_hard_overflow = replay_cost_s > float(unit["hard_budget_s"]) + 1e-12
            if (
                bool(unit["policies"][policy]["safe_cap_overflow"])
                != expected_safe_overflow
            ):
                raise RuntimeError(f"{unit['unit_id']}:{policy}: safe overflow")
            if (
                bool(unit["policies"][policy]["hard_budget_overflow"])
                != expected_hard_overflow
            ):
                raise RuntimeError(f"{unit['unit_id']}:{policy}: hard overflow")
            checked += 1
    return {
        "status": "PASS",
        "units": len(summary["units"]),
        "candidate_rows": len(candidate_rows),
        "policy_portfolios_checked": checked,
    }


def _flatten_summary(unit: Mapping[str, Any]) -> dict[str, Any]:
    p = unit["policies"]
    return {
        "unit_id": unit["unit_id"],
        "regime": unit["regime"],
        "seed": unit["seed"],
        "expected_stop": unit["expected_stop"],
        "actual_stop": unit["actual_stop"],
        "valid": unit["valid"],
        "errors": ";".join(unit["errors"]),
        "incumbent_count": unit["incumbent_count"],
        "inventory_count": unit["inventory_count"],
        "incumbent_raw": p["incumbent"]["raw"],
        "headroom_only_raw": p["headroom_only"]["raw"],
        "generation_gated_raw": p["generation_gated"]["raw"],
        "bank_all_raw": p["bank_all"]["raw"],
        "headroom_only_gain_raw": (
            p["headroom_only"]["raw"] - p["incumbent"]["raw"]
        ),
        "generation_gated_gain_raw": (
            p["generation_gated"]["raw"] - p["incumbent"]["raw"]
        ),
        "headroom_only_actual_cost_s": p["headroom_only"]["actual_replay_cost_s"],
        "generation_gated_actual_cost_s": p["generation_gated"][
            "actual_replay_cost_s"
        ],
        "bank_all_actual_cost_s": p["bank_all"]["actual_replay_cost_s"],
        "safe_cap_s": unit["safe_cap_s"],
        "hard_budget_s": unit["hard_budget_s"],
        "headroom_only_safe_overflow": p["headroom_only"]["safe_cap_overflow"],
        "headroom_only_hard_overflow": p["headroom_only"]["hard_budget_overflow"],
        "generation_gated_safe_overflow": p["generation_gated"][
            "safe_cap_overflow"
        ],
        "bank_all_safe_overflow": p["bank_all"]["safe_cap_overflow"],
        "bank_all_hard_overflow": p["bank_all"]["hard_budget_overflow"],
    }


def _contract() -> dict[str, Any]:
    return {
        "schema_version": "dber-factorial-profile-contract-v1",
        "preregistration": [
            "research-log/217-dber-round13-factorial-profile-preregistration.md",
            "research-log/218-dber-profile-preregistration-parser-correction.md",
        ],
        "alpha": ALPHA,
        "base_config": BASE_CONFIG,
        "regimes": list(REGIMES),
        "seeds": list(SEEDS),
        "unit_count": len(REGIMES) * len(SEEDS),
        "unit_order": [
            f"{regime['name']}-seed{seed}"
            for regime in REGIMES
            for seed in SEEDS
        ],
        "policies": list(POLICIES),
        "source_sha256": {
            str(path.relative_to(ROOT)): _sha_path(path) for path in SOURCE_PATHS
        },
    }


def _write_outputs(
    out_dir: Path,
    units: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=False)
    summary_path = out_dir / "dber-factorial-summary.json"
    candidates_path = out_dir / "dber-factorial-candidates.jsonl"
    tsv_path = out_dir / "dber-factorial-summary.tsv"
    summary = {
        "schema_version": "dber-factorial-profile-v1",
        "status": "CONTROLLED_PROFILE",
        "scope": (
            "controlled real-SDK mock mechanism evidence only; no target-model, "
            "private-transfer, leaderboard, or Kaggle claim"
        ),
        "contract": _contract(),
        "units": units,
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    candidates_path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in candidate_rows)
    )
    flattened = [_flatten_summary(unit) for unit in units]
    with tsv_path.open("w") as handle:
        handle.write("\t".join(SUMMARY_FIELDS) + "\n")
        for row in flattened:
            handle.write("\t".join(str(row[field]) for field in SUMMARY_FIELDS) + "\n")

    verification = _verify_artifacts(summary_path, candidates_path)
    (out_dir / "dber-factorial-verification.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--print-contract", action="store_true")
    parser.add_argument("--verify-dir", type=Path)
    args = parser.parse_args()

    selected = sum(
        bool(value)
        for value in (args.out_dir, args.print_contract, args.verify_dir)
    )
    if selected != 1:
        parser.error("choose exactly one of --out-dir, --print-contract, --verify-dir")

    if args.print_contract:
        print(json.dumps(_contract(), sort_keys=True))
        return 0
    if args.verify_dir is not None:
        result = _verify_artifacts(
            args.verify_dir / "dber-factorial-summary.json",
            args.verify_dir / "dber-factorial-candidates.jsonl",
        )
        print(json.dumps(result, sort_keys=True))
        return 0

    assert args.out_dir is not None
    module = _load_attack_module()
    units: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    for regime in REGIMES:
        for seed in SEEDS:
            unit, rows = _profile_unit(module, regime, seed)
            units.append(unit)
            candidate_rows.extend(rows)
            p = unit["policies"]
            print(
                "unit:"
                f" id={unit['unit_id']}"
                f" stop={unit['actual_stop']}"
                f" valid={unit['valid']}"
                f" incumbent_raw={p['incumbent']['raw']}"
                f" headroom_raw={p['headroom_only']['raw']}"
                f" gated_raw={p['generation_gated']['raw']}"
                f" bank_raw={p['bank_all']['raw']}",
                flush=True,
            )
    _write_outputs(args.out_dir, units, candidate_rows)
    valid_units = sum(bool(unit["valid"]) for unit in units)
    print(f"profile_units: {len(units)}")
    print(f"valid_units: {valid_units}")
    print("profile_status: CONTROLLED_PROFILE")
    return 0 if valid_units == len(units) else 2


if __name__ == "__main__":
    raise SystemExit(main())
