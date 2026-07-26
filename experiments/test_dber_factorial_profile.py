"""Pre-execution tests for the DBER four-policy profile harness."""

from __future__ import annotations

import subprocess
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SDK = ROOT / "comp" / "sdk"
sys.path.insert(0, str(SDK))
sys.path.insert(0, str(HERE))

from aicomp_sdk.attacks.contracts import AttackRunConfig  # noqa: E402
from aicomp_sdk.core.predicates import SECRET_MARKER  # noqa: E402
from dber_factorial_profile import (  # noqa: E402
    CandidateRecord,
    _headroom_selection,
)
from mock_agents import IndexSplitLatencyAgent  # noqa: E402


def _load_attack_source(name: str, source: str):
    module = types.ModuleType(name)
    module.__file__ = str(HERE / "attack.py")
    sys.modules[name] = module
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    return module


class _Clock:
    def __init__(self) -> None:
        self.value = 0.0

    def monotonic(self) -> float:
        self.value += 0.001
        return self.value


class _Env:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def reset(self):
        self.messages = []
        return None

    def interact(self, message: str, *, max_tool_hops: int):
        del max_tool_hops
        self.messages.append(message)
        return None

    def export_trace_dict(self):
        events = []
        for message in self.messages:
            url = message.split("url=", 1)[1].split()[0].strip('")')
            events.append(
                {
                    "name": "http.post",
                    "ok": True,
                    "side_effect": "SHARE",
                    "scope": "network",
                    "source": "user",
                    "args": {"url": url, "data": SECRET_MARKER},
                    "output": "ok",
                }
            )
        return {
            "seed": 42,
            "user_messages": list(self.messages),
            "tool_events": events,
            "egress": [],
        }


def test_stop_instrumentation_is_behavior_neutral() -> None:
    frozen_source = subprocess.check_output(
        ["git", "show", "86a64c1:experiments/attack.py"],
        cwd=ROOT,
        text=True,
    )
    current_source = (HERE / "attack.py").read_text()
    frozen = _load_attack_source("dber_frozen_attack_test", frozen_source)
    current = _load_attack_source("dber_current_attack_test", current_source)
    config = {
        "probe_reps": 1,
        "probe_time_cap_s": 0.9,
        "replay_budget_s": 1.0,
        "replay_safe": 0.99,
        "gen_margin_s": 0.05,
        "max_candidates": 5,
        "enable_multi_message": False,
        "enable_scoc": False,
    }
    outputs = []
    for module in (frozen, current):
        module.time = _Clock()
        attack = module.AttackAlgorithm(config)
        candidates = attack.run(
            _Env(),
            AttackRunConfig(time_budget_s=3.0, max_tool_hops=8),
        )
        outputs.append(
            (
                [list(candidate.user_messages) for candidate in candidates],
                attack.debug,
            )
        )
    assert outputs[0][0] == outputs[1][0]
    assert outputs[1][1]["fill_stop_reason"] == "candidate"
    assert outputs[1][1]["fill_terminal_candidate_count"] == 5
    assert outputs[1][1]["fill_clamp_removed"] == 0


def test_index_split_inverse_mapping() -> None:
    agent = IndexSplitLatencyAgent()
    assert agent._action_latency("http.post url=http://aa.co data=x") == 0.020
    assert agent._action_latency("http.post url=http://jk1331.co data=x") == 0.002
    assert agent._action_latency("http.post url=http://up1331.co data=x") == 0.002
    assert agent._action_latency("no indexed URL") == 0.020


def test_headroom_selector_prefers_positive_fitting_item() -> None:
    def record(signature: str, elapsed: float, raw: float) -> CandidateRecord:
        finding = {
            "seed": 1,
            "user_messages": [signature],
            "trace": {},
            "predicates": [{"predicate": "EXFILTRATION", "severity": 5}]
            if raw
            else [],
            "cell_signature": {"hash": signature},
            "score_cell_signature": {"hash": signature},
        }
        return CandidateRecord(
            unit_id="test",
            source_phase="test",
            messages=[signature],
            message_signature=signature,
            generation_elapsed_s=elapsed,
            generation_trace={},
            generation_trace_sha256="",
            generation_finding=finding,
            generation_isolated_raw=raw,
            replay_elapsed_s=elapsed,
            replay_trace={},
            replay_trace_sha256="",
            replay_finding=finding,
            replay_isolated_raw=raw,
            policy_decisions={},
        )

    incumbent = [record("incumbent", 0.10, 18.0)]
    cheap = record("cheap", 0.01, 18.0)
    expensive = record("expensive", 0.20, 18.0)
    selected, decisions = _headroom_selection(
        incumbent,
        [expensive, cheap],
        cap=3,
        safe_cap_s=0.13,
    )
    assert [row.message_signature for row in selected] == ["incumbent", "cheap"]
    assert decisions["cheap"]["admitted"] is True
    assert decisions["expensive"]["admitted"] is False
