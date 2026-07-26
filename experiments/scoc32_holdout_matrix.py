"""Run a held-out SCOC local matrix for long-horizon continuation feasibility checks."""

from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path
from typing import Any, Callable
from collections import Counter

from aicomp_sdk.attacks.contracts import AttackRunConfig
from aicomp_sdk.core.env.api import EnvSelection
from aicomp_sdk.evaluation.ops import build_attack_env
from aicomp_sdk.evaluation.runner import evaluate_redteam
from aicomp_sdk.guardrails import OptimalGuardrail

from mock_agents import CompliantAgent, ContextLimitedAgent


def _load_attack_cls():
    from importlib import util
    import sys

    spec = util.spec_from_file_location("scoc_experiment_attack", Path(__file__).resolve().parent / "attack.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to locate attack.py")
    mod = util.module_from_spec(spec)
    sys.modules["scoc_experiment_attack"] = mod
    spec.loader.exec_module(mod)
    return mod.AttackAlgorithm


ATTACK_CONFIG_BASE = {
    "probe_reps": 1,
    "probe_time_cap_s": 5.0,
    "gen_margin_s": 0.5,
    "replay_budget_s": 6.0,
    "replay_safe": 0.99,
    "max_candidates": 24,
    "multi_probe_reps": 1,
    "multi_probe_messages": 6,
    "multi_fill_messages": 12,
    "multi_min_fire_fraction": 0.75,
    "multi_rate_gain": 1.10,
    "scoc_probe_reps": 1,
    "scoc_fill_messages": 12,
    "scoc_probe_messages": 6,
    "scoc_min_fire_fraction": 0.75,
    "scoc_rate_gain": 1.05,
}


def _scenario_factory(scenario: str, latency_s: float = 0.0) -> Callable[[], Any]:
    if scenario == "compliant_zero_overhead":
        return lambda: CompliantAgent(latency_s=latency_s)
    if scenario == "context_limited_8":
        return lambda: ContextLimitedAgent(max_user_messages=8, latency_s=latency_s)
    raise ValueError(f"unknown scenario {scenario}")


def _run_case(
    *,
    scenario: str,
    seed: int,
    tag: str,
    cfg: dict[str, Any],
    run_config: AttackRunConfig,
):
    AttackAlgorithm = _load_attack_cls()
    attack_env = {
        "seed": seed,
        "fixtures_dir": Path("comp") / "sdk" / "aicomp_sdk" / "fixtures",
        "agent_factory": _scenario_factory(scenario),
        "guardrail": OptimalGuardrail(),
        "env_selection": EnvSelection.SANDBOX,
        "max_tool_hops": 8,
    }

    # Capture routing debug from algorithm pass.
    env = build_attack_env(**attack_env)
    attack = AttackAlgorithm(cfg)
    route_t0 = time.monotonic()
    candidates = attack.run(env, run_config)
    route_wall_s = time.monotonic() - route_t0
    debug = attack.debug or {}
    run_candidate_lengths = [len(candidate.user_messages) for candidate in candidates]
    run_candidate_length_hist: dict[str, str] = {str(k): str(v) for k, v in Counter(run_candidate_lengths).items()}

    # Exact local evaluator pass with fixed seed and budget.
    ex = evaluate_redteam(
        AttackAlgorithm,
        budget_s=run_config.time_budget_s,
        agent_factory=_scenario_factory(scenario),
        agent_label=f"scoc32-holdout-{scenario}-seed{seed}",
        env_selection=EnvSelection.SANDBOX,
        fixtures_dir=Path("comp") / "sdk" / "aicomp_sdk" / "fixtures",
        attack_config=cfg,
        attack_run_config=run_config,
        attack_env_seed=seed,
    )
    a = ex.attack

    return {
        "run_id": f"scoc32-local-scoc-holdout-{scenario}-seed{seed}-{tag}",
        "scenario": scenario,
        "seed": str(seed),
        "tag": tag,
        "cfg_tag": tag,
        "enable_scoc": str(bool(cfg.get("enable_scoc", False))),
        "findings": str(a.findings_count),
        "normalized": str(a.score),
        "score_raw": str(a.score_raw),
        "run_time_s": str(a.time_taken),
        "unique_cells": str(a.unique_cells),
        "structure": str(debug.get("structure", "single_post")),
        "selected_raw_per_s": str(debug.get("selected_structure_rate", -1.0)),
        "multi_raw_per_s": str(debug.get("multi_raw_per_s", -1.0)),
        "scoc_raw_per_s": str(debug.get("scoc_raw_per_s", -1.0)),
        "route_wall_s": f"{route_wall_s:.6f}",
        "candidate_message_lengths": json.dumps(run_candidate_length_hist),
        "candidate_message_length_mode": str(Counter(run_candidate_lengths).most_common(1)[0][0]) if run_candidate_lengths else "0",
        "replay_cost_s": str(debug.get("replay_cost_s", 0.0)),
        "unit_cost_s": str(debug.get("unit_cost_s", 0.0)),
        "route_returned": str(debug.get("returned", 0)),
        "multi_kept": str(debug.get("multi_kept", 0)),
        "scoc_kept": str(debug.get("scoc_kept", 0)),
        "multi_fallback": str(debug.get("multi_fallback", False)),
        "scoc_fallback": str(debug.get("scoc_fallback", False)),
        "env_seed": str(seed),
        "cfg": json.dumps(cfg, sort_keys=True),
        "predicted_value": "",
    }


def _to_float_or_default(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _coerce_predicted_value(scenario: str) -> float:
    return 23.28 if scenario.startswith("compliant") else 2.16


def _coerce_signal(predicted_value: float, metric_value: float, predicted_direction: str) -> str:
    if metric_value is None:
        return "null"
    if predicted_direction == "match-baseline":
        return "confirm" if abs(metric_value - predicted_value) <= 1e-6 else "partial"
    if predicted_direction == "beat-baseline":
        if metric_value >= predicted_value:
            return "confirm"
        if metric_value >= 0.95 * predicted_value:
            return "partial"
        return "disconfirm"
    return "confirm" if metric_value == predicted_value else "partial"


def _registry_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reg_rows: list[dict[str, Any]] = []
    for row in rows:
        predicted_value = _coerce_predicted_value(row["scenario"])
        metric_value = _to_float_or_default(row["normalized"], 0.0)
        signal = _coerce_signal(predicted_value, metric_value, "match-baseline")
        reg_rows.append(
            {
                "run_id": row["run_id"],
                "metric": "normalized",
                "predicted_value": predicted_value,
                "predicted_direction": "match-baseline",
                "confidence": "low",
                "metric_value": metric_value,
                "signal": signal,
                "memory_gb": 0.5,
                "runtime_s": _to_float_or_default(row["run_time_s"], 0.0),
                "status": "exploratory",
                "description": (
                    f"held-out matrix scenario={row['scenario']} seed={row['seed']} "
                    f"tag={row['tag']} findings={row['findings']} structure={row['structure']} "
                    f"normalized={row['normalized']}"
                ),
            }
        )
        row["predicted_value"] = f"{predicted_value:.12f}"
    return reg_rows


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=Path("artifacts/scoc32/run10"))
    parser.add_argument(
        "--results-tsv",
        type=Path,
        default=Path("results.tsv"),
        help="kept for compatibility; script writes only registry artifacts",
    )
    args = parser.parse_args(argv)

    run_config = AttackRunConfig(time_budget_s=6.0, max_tool_hops=8)
    scenarios = ["compliant_zero_overhead", "context_limited_8"]
    seeds = [42, 777, 2026]
    cfgs = {
        "scoc_off": {"enable_scoc": False, **ATTACK_CONFIG_BASE},
        "scoc_default": {"enable_scoc": True, **ATTACK_CONFIG_BASE},
        "scoc_probe12": {
            "enable_scoc": True,
            "scoc_fill_messages": 12,
            "scoc_probe_messages": 12,
            **{k: v for k, v in ATTACK_CONFIG_BASE.items() if k not in {"scoc_fill_messages", "scoc_probe_messages"}},
        },
        "scoc_long_fill": {
            "enable_scoc": True,
            "scoc_fill_messages": 24,
            "scoc_probe_messages": 6,
            **{k: v for k, v in ATTACK_CONFIG_BASE.items() if k not in {"scoc_fill_messages", "scoc_probe_messages"}},
        },
        "scoc_anchor4": {
            "enable_scoc": True,
            "scoc_fill_messages": 12,
            "scoc_probe_messages": 6,
            "scoc_anchor_period": 4,
            **{k: v for k, v in ATTACK_CONFIG_BASE.items() if k not in {"scoc_fill_messages", "scoc_probe_messages"}},
        },
        "scoc_anchor8": {
            "enable_scoc": True,
            "scoc_fill_messages": 12,
            "scoc_probe_messages": 6,
            "scoc_anchor_period": 8,
            **{k: v for k, v in ATTACK_CONFIG_BASE.items() if k not in {"scoc_fill_messages", "scoc_probe_messages"}},
        },
    }

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for scenario in scenarios:
        for seed in seeds:
            for tag, cfg in cfgs.items():
                rows.append(
                    _run_case(
                        scenario=scenario,
                        seed=seed,
                        tag=tag,
                        cfg=cfg,
                        run_config=run_config,
                    )
                )

    matrix_tsv = out_dir / "scoc32-local-scoc-holdout-matrix.tsv"
    matrix_json = out_dir / "scoc32-local-scoc-holdout-matrix.json"

    tsv_cols = [
        "run_id",
        "scenario",
        "seed",
        "tag",
        "cfg_tag",
        "enable_scoc",
        "findings",
        "normalized",
        "score_raw",
        "run_time_s",
        "unique_cells",
        "structure",
        "selected_raw_per_s",
        "multi_raw_per_s",
        "scoc_raw_per_s",
        "replay_cost_s",
        "unit_cost_s",
        "route_returned",
        "multi_kept",
        "scoc_kept",
        "multi_fallback",
        "scoc_fallback",
        "env_seed",
        "candidate_message_lengths",
        "candidate_message_length_mode",
        "route_wall_s",
        "cfg",
        "predicted_value",
    ]

    with matrix_tsv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(tsv_cols)
        reg_rows = _registry_rows(rows)
        for row in rows:
            writer.writerow([row.get(k, "") for k in tsv_cols])

    matrix_json.write_text(
        json.dumps(
            {
                "run_id": "scoc32-local-scoc-holdout-matrix",
                "run_config": {
                    "attack_config_base": ATTACK_CONFIG_BASE,
                    "attack_run_config": {
                        "time_budget_s": run_config.time_budget_s,
                        "max_tool_hops": run_config.max_tool_hops,
                    },
                },
                "cfgs": cfgs,
                "rows": rows,
            },
            sort_keys=True,
            indent=2,
        ),
        encoding="utf-8",
    )

    reg_rows_path = out_dir / "scoc32-local-scoc-holdout-registry-payload.json"
    reg_rows_path.write_text(json.dumps(reg_rows, sort_keys=True, indent=2), encoding="utf-8")

    print(f"WROTE {len(rows)} rows to {matrix_tsv}")
    print(f"WROTE payload {len(reg_rows)} rows to {reg_rows_path}")
    print(f"run_id {run_config}")
    print(f"results payload path {args.results_tsv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
