"""Local end-to-end validation of attack.py through the real SDK scoring pipeline.

Runs `evaluate_redteam` (the scorer-equivalent harness) against mock target agents
and prints the official AttackExecution fields. This validates the mechanics we
control: candidate generation, predicate firing, cell counting, per-model TEMPLATE
SELECTION, verified-firing fill, and scoring. It does NOT validate message efficacy
against gpt-oss/gemma -- impossible without the models, which is why the attack
probes/selects online at run time.

Because the mocks have ~zero latency, we cap `max_candidates` so the LOCAL replay
finishes within the local budget. The real Kaggle run sizes N by measured latency
against the 9000 s replay budget (see attack.py AttackConfig).

Usage:  python experiments/local_eval.py [max_candidates] [budget_s]
"""

from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SDK = HERE.parent / "comp" / "sdk"
sys.path.insert(0, str(SDK))
sys.path.insert(0, str(HERE))

from aicomp_sdk.core.env.api import EnvSelection  # noqa: E402
from aicomp_sdk.evaluation.runner import evaluate_redteam  # noqa: E402
from mock_agents import (  # noqa: E402
    CompliantAgent,
    HarmonyOnlyAgent,
    StochasticAgent,
)


def _load_attack_cls():
    spec = importlib.util.spec_from_file_location("user_attack", HERE / "attack.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["user_attack"] = mod
    spec.loader.exec_module(mod)
    return mod.AttackAlgorithm


def run(label, agent_factory, attack_config, budget_s):
    AttackAlgorithm = _load_attack_cls()
    t0 = time.time()
    ex = evaluate_redteam(
        AttackAlgorithm,
        budget_s=budget_s,
        agent_factory=agent_factory,
        agent_label=label,
        env_selection=EnvSelection.SANDBOX,
        fixtures_dir=SDK / "aicomp_sdk" / "fixtures",
        attack_config=attack_config,
    )
    a = ex.attack
    print(f"\n===== {label} =====")
    print(f"  wall: {time.time()-t0:6.1f}s | findings={a.findings_count} "
          f"unique_cells={a.unique_cells}")
    print(f"  raw={a.score_raw:.1f}  normalized(0-1000)={a.score:.2f}")
    return a


if __name__ == "__main__":
    max_c = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    budget_s = float(sys.argv[2]) if len(sys.argv) > 2 else 600.0
    cfg = {"probe_reps": 3, "gen_margin_s": 5, "max_candidates": max_c,
           "probe_time_cap_s": 120.0}

    run("compliant", lambda: CompliantAgent(), cfg, budget_s)
    run("harmony_only", lambda: HarmonyOnlyAgent(), cfg, budget_s)
    run("stochastic", lambda: StochasticAgent(), cfg, budget_s)
