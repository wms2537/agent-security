"""Local mechanics checks for Burst-2 Validation Fill.

This is a Phase-3 mechanics gate only. It does not claim target-model transfer
or Kaggle score.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from aicomp_sdk.attacks.contracts import AttackRunConfig

import sys

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = ROOT / "experiments"
if str(EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS))

from attack import AttackAlgorithm, _bundle_msg, _msg  # noqa: E402


class FakeEnv:
    def __init__(self, event_count: int) -> None:
        self.event_count = int(event_count)
        self.calls: list[str] = []

    def reset(self) -> None:
        return None

    def interact(self, message: str, max_tool_hops: int = 8) -> None:
        self.calls.append(message)

    def export_trace_dict(self) -> dict[str, Any]:
        return {
            "tool_events": [
                {
                    "ok": True,
                    "name": "http.post",
                    "args": {"data": "SECRET_MARKER"},
                }
                for _ in range(self.event_count)
            ]
        }


def count_max(messages: list[str], needle: str) -> int:
    return max((message.count(needle) for message in messages), default=0)


def main() -> None:
    started = time.monotonic()

    k1 = _bundle_msg(0, 1)
    v35 = _msg(0)
    k2 = _bundle_msg(0, 2)

    none_k1 = AttackAlgorithm({"n_candidates": 3, "bundle_posts": 1}).run(
        None,
        AttackRunConfig(time_budget_s=10, max_tool_hops=8),
    )
    none_k2 = AttackAlgorithm({"n_candidates": 3, "bundle_posts": 2}).run(
        None,
        AttackRunConfig(time_budget_s=10, max_tool_hops=8),
    )
    none_k1_messages = [candidate.user_messages[0] for candidate in none_k1]
    none_k2_messages = [candidate.user_messages[0] for candidate in none_k2]

    env2 = FakeEnv(event_count=2)
    live_k2 = AttackAlgorithm(
        {
            "bundle_posts": 2,
            "hard_n_cap": 5,
            "slowest0": 0.001,
            "split_by_latency": True,
            "replay_safe_sizing": False,
            "fill_budget_frac": 0.50,
            "floor_min": 0.001,
            "margin_s": 0.001,
        }
    ).run(env2, AttackRunConfig(time_budget_s=5, max_tool_hops=8))
    live_k2_messages = [candidate.user_messages[0] for candidate in live_k2]

    env1 = FakeEnv(event_count=1)
    partial_k2 = AttackAlgorithm(
        {
            "bundle_posts": 2,
            "hard_n_cap": 5,
            "slowest0": 0.001,
            "split_by_latency": True,
            "replay_safe_sizing": False,
            "fill_budget_frac": 0.50,
            "floor_min": 0.001,
            "margin_s": 0.001,
        }
    ).run(env1, AttackRunConfig(time_budget_s=5, max_tool_hops=8))

    metrics = {
        "bundle_k1_byte_equivalent": int(k1 == v35),
        "bundle_k2_url_count": k2.count("http://"),
        "bundle_k2_post_mentions": k2.count("http.post"),
        "bundle_k2_empty_messages": int(not k2.strip()),
        "bundle_k2_no_dense4_wording": int("Perform exactly 4" not in k2),
        "none_k1_count": len(none_k1),
        "none_k1_max_urls": count_max(none_k1_messages, "http://"),
        "none_k1_max_posts": count_max(none_k1_messages, "http.post"),
        "none_k2_count": len(none_k2),
        "none_k2_max_urls": count_max(none_k2_messages, "http://"),
        "none_k2_max_posts": count_max(none_k2_messages, "http.post"),
        "fake_live_k2_count": len(live_k2),
        "fake_live_k2_env_calls": len(env2.calls),
        "fake_live_k2_max_urls": count_max(live_k2_messages, "http://"),
        "fake_live_k2_max_posts": count_max(live_k2_messages, "http.post"),
        "fake_live_k2_event_count": AttackAlgorithm._event_count(env2),
        "partial_fake_k2_count": len(partial_k2),
        "has_slow_multipost_marker": int(
            "SLOW_MULTIPOST" in Path(EXPERIMENTS / "attack.py").read_text()
        ),
        "has_measured_dense_marker": int(
            "MEASURED_DENSE" in Path(EXPERIMENTS / "attack.py").read_text()
        ),
        "max_message_len": max(map(len, none_k2_messages + live_k2_messages)),
        "runtime_s": round(time.monotonic() - started, 6),
    }

    for key, value in metrics.items():
        print(f"{key}: {value}")

    required = {
        "bundle_k1_byte_equivalent": 1,
        "bundle_k2_url_count": 2,
        "bundle_k2_post_mentions": 2,
        "bundle_k2_empty_messages": 0,
        "bundle_k2_no_dense4_wording": 1,
        "none_k1_max_urls": 1,
        "none_k2_max_urls": 2,
        "none_k2_max_posts": 2,
        "fake_live_k2_count": 5,
        "fake_live_k2_max_urls": 2,
        "fake_live_k2_max_posts": 2,
        "fake_live_k2_event_count": 2,
        "partial_fake_k2_count": 5,
        "has_slow_multipost_marker": 0,
        "has_measured_dense_marker": 0,
    }
    failed = [
        f"{key} expected {expected} got {metrics.get(key)}"
        for key, expected in required.items()
        if metrics.get(key) != expected
    ]
    if failed:
        print("burst2_gate_pass: 0")
        raise SystemExit("; ".join(failed))

    print("burst2_gate_pass: 1")


if __name__ == "__main__":
    main()
