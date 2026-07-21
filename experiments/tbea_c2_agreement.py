#!/usr/bin/env python3
"""Frozen annotation validation and agreement gate for TBEA-PILOT-1."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


EXPECTED_MANIFEST_SHA256 = "8379b954769189443faf2ce7c73a6fab993553c009aab46d06dd518c580e2c4c"
CONTRACT_VERSION = "TBEA-PILOT-1"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def exact_rate(pairs: list[tuple[Any, Any]]) -> float | None:
    if not pairs:
        return None
    return sum(left == right for left, right in pairs) / len(pairs)


def nominal_alpha(pairs: list[tuple[str, str]]) -> tuple[float | None, int]:
    if not pairs:
        return None, 0
    pooled = Counter(value for pair in pairs for value in pair)
    categories = len(pooled)
    total = sum(pooled.values())
    observed_disagreement = sum(left != right for left, right in pairs) / len(pairs)
    if total < 2:
        return None, categories
    expected_agreement = sum(count * (count - 1) for count in pooled.values()) / (total * (total - 1))
    expected_disagreement = 1.0 - expected_agreement
    if expected_disagreement == 0:
        return None, categories
    return 1.0 - observed_disagreement / expected_disagreement, categories


def schema_enums(schema: dict[str, Any]) -> dict[str, set[str]]:
    properties = schema["$defs"]["record"]["properties"]
    return {
        key: set(value["enum"])
        for key, value in properties.items()
        if isinstance(value, dict) and "enum" in value
    }


def load_parsed_manifest(path: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    raw = path.read_bytes()
    require(sha256_bytes(raw) == EXPECTED_MANIFEST_SHA256, "parsed manifest identity mismatch")
    manifest = json.loads(raw)
    require(manifest["contract_version"] == CONTRACT_VERSION, "parsed manifest version mismatch")
    by_alias = {row["trace_alias"]: row for row in manifest["rows"]}
    require(len(by_alias) == 18, "parsed manifest must contain 18 unique aliases")
    return manifest, by_alias


def parsed_events(parsed_dir: Path, manifest_rows: dict[str, dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    result: dict[str, dict[str, dict[str, Any]]] = {}
    for alias, row in manifest_rows.items():
        raw = (parsed_dir / row["parsed_file"]).read_bytes()
        require(sha256_bytes(raw) == row["parsed_sha256"], f"{alias}: parsed file drift")
        parsed = json.loads(raw)
        event_map = {event["event_id"]: event for event in parsed["events"]}
        require(len(event_map) == len(parsed["events"]), f"{alias}: duplicate event id")
        result[alias] = event_map
    return result


def validate_annotation(
    path: Path,
    schema: dict[str, Any],
    manifest_rows: dict[str, dict[str, Any]],
    events: dict[str, dict[str, dict[str, Any]]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], str]:
    raw = path.read_bytes()
    annotation = json.loads(raw)
    top_required = set(schema["required"])
    require(set(annotation) == top_required, f"{path.name}: top-level keys differ from schema")
    require(annotation["contract_version"] == CONTRACT_VERSION, f"{path.name}: wrong version")
    require(annotation["parsed_manifest_sha256"] == EXPECTED_MANIFEST_SHA256, f"{path.name}: manifest hash")
    require(isinstance(annotation["coder_id"], str) and annotation["coder_id"], f"{path.name}: coder id")
    records = annotation["records"]
    require(isinstance(records, list) and len(records) == 18, f"{path.name}: record count")
    record_schema = schema["$defs"]["record"]
    required_keys = set(record_schema["required"])
    enums = schema_enums(schema)
    reason_enum = set(record_schema["properties"]["reason_codes"]["items"]["enum"])
    by_alias: dict[str, dict[str, Any]] = {}
    for record in records:
        require(isinstance(record, dict), f"{path.name}: record is not object")
        require(set(record) == required_keys, f"{path.name}: record keys differ from schema")
        alias = record["trace_alias"]
        require(isinstance(alias, str) and re.fullmatch(r"T[0-9a-f]{12}", alias), f"{path.name}: alias")
        require(alias in manifest_rows and alias not in by_alias, f"{path.name}: unknown/duplicate alias")
        for field, allowed in enums.items():
            require(record[field] in allowed, f"{path.name}: {alias} invalid {field}")
        reasons = record["reason_codes"]
        require(isinstance(reasons, list) and len(reasons) == len(set(reasons)), f"{path.name}: reasons")
        require(set(reasons).issubset(reason_enum), f"{path.name}: invalid reason")
        for field in ("terminal_event_id", "authority_evidence_event_id", "candidate_evidence_event_id"):
            event_id = record[field]
            require(event_id is None or event_id in events[alias], f"{path.name}: {alias} invalid {field}")
        authority = record["effective_authority"]
        if authority is not None:
            require(isinstance(authority, str), f"{path.name}: {alias} authority type")
            observed_actors = {event["actor"] for event in events[alias].values() if event["actor"] is not None}
            require(authority in observed_actors, f"{path.name}: {alias} authority not source-grounded")
        terminal_status = record["terminal_status"]
        if terminal_status == "observed_deliberate":
            require(record["terminal_event_id"] is not None, f"{path.name}: {alias} missing terminal event")
        else:
            require(record["terminal_event_id"] is None, f"{path.name}: {alias} nonobserved terminal has event")
        authority_status = record["effective_authority_status"]
        if authority_status == "observed":
            require(authority is not None, f"{path.name}: {alias} missing authority")
            require(record["authority_evidence_event_id"] is not None, f"{path.name}: {alias} missing authority evidence")
        else:
            require(authority is None, f"{path.name}: {alias} nonobserved authority has value")
        relation = record["authority_evidence_relation"]
        if terminal_status == "no_observable_deliberate":
            require(
                relation == "no_observable_deliberate_terminal_transition",
                f"{path.name}: {alias} no-terminal relation mismatch",
            )
        candidate_event = record["candidate_evidence_event_id"]
        if candidate_event is None:
            require(
                record["visibility_to_authority"] in {"no_candidate_evidence", "indeterminate"},
                f"{path.name}: {alias} visibility without candidate",
            )
        if candidate_event is not None and record["terminal_event_id"] is not None:
            require(
                candidate_event < record["terminal_event_id"],
                f"{path.name}: {alias} candidate evidence is not before terminal",
            )
        by_alias[alias] = record
    require(set(by_alias) == set(manifest_rows), f"{path.name}: alias set mismatch")
    require([record["trace_alias"] for record in records] == sorted(by_alias), f"{path.name}: aliases not sorted")
    return annotation, by_alias, sha256_bytes(raw)


def finite_ge(value: float | None, threshold: float) -> bool:
    return value is not None and math.isfinite(value) and value >= threshold


def evaluate(
    manifest_rows: dict[str, dict[str, Any]],
    coder_a: dict[str, dict[str, Any]],
    coder_b: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    aliases = sorted(manifest_rows)
    both_terminal = [
        alias
        for alias in aliases
        if coder_a[alias]["terminal_status"] == "observed_deliberate"
        and coder_b[alias]["terminal_status"] == "observed_deliberate"
    ]
    jointly_recoverable = [
        alias
        for alias in both_terminal
        if coder_a[alias]["effective_authority_status"] == "observed"
        and coder_b[alias]["effective_authority_status"] == "observed"
    ]
    terminal_pairs = [(coder_a[a]["terminal_event_id"], coder_b[a]["terminal_event_id"]) for a in both_terminal]
    authority_pairs = [(coder_a[a]["effective_authority"], coder_b[a]["effective_authority"]) for a in jointly_recoverable]
    visibility_pairs = [(coder_a[a]["visibility_to_authority"], coder_b[a]["visibility_to_authority"]) for a in aliases]
    relation_pairs = [(coder_a[a]["authority_evidence_relation"], coder_b[a]["authority_evidence_relation"]) for a in aliases]
    terminal_rate = exact_rate(terminal_pairs)
    authority_rate = exact_rate(authority_pairs)
    visibility_rate = exact_rate(visibility_pairs)
    relation_rate = exact_rate(relation_pairs)
    visibility_alpha, visibility_categories = nominal_alpha(visibility_pairs)
    relation_alpha, relation_categories = nominal_alpha(relation_pairs)
    system_counts = Counter(manifest_rows[alias]["mas_name"] for alias in jointly_recoverable)
    qualifying_systems = sum(system_counts.get(system, 0) >= 4 for system in {row["mas_name"] for row in manifest_rows.values()})
    max_share = max(system_counts.values(), default=0) / len(jointly_recoverable) if jointly_recoverable else None
    checks = {
        "two_system_coverage": qualifying_systems >= 2,
        "single_system_share": max_share is not None and max_share <= 0.6,
        "terminal_event_agreement": finite_ge(terminal_rate, 0.8),
        "authority_agreement": finite_ge(authority_rate, 0.8),
        "visibility_raw_agreement": finite_ge(visibility_rate, 0.75),
        "relation_raw_agreement": finite_ge(relation_rate, 0.75),
        "visibility_alpha": visibility_categories >= 2 and finite_ge(visibility_alpha, 0.67),
        "relation_alpha": relation_categories >= 2 and finite_ge(relation_alpha, 0.67),
    }
    return {
        "gate": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "both_terminal": len(both_terminal),
        "jointly_recoverable": len(jointly_recoverable),
        "jointly_recoverable_by_system": dict(sorted(system_counts.items())),
        "qualifying_systems": qualifying_systems,
        "maximum_single_system_share": max_share,
        "terminal_event_exact_agreement": terminal_rate,
        "effective_authority_exact_agreement": authority_rate,
        "visibility_raw_agreement": visibility_rate,
        "visibility_nominal_alpha": visibility_alpha,
        "visibility_categories": visibility_categories,
        "relation_raw_agreement": relation_rate,
        "relation_nominal_alpha": relation_alpha,
        "relation_categories": relation_categories,
    }


def self_test() -> dict[str, Any]:
    systems = ["AG2"] * 6 + ["AppWorld"] * 6 + ["MetaGPT"] * 6
    manifest = {f"T{i:012x}": {"mas_name": system} for i, system in enumerate(systems)}
    a: dict[str, dict[str, Any]] = {}
    b: dict[str, dict[str, Any]] = {}
    for index, alias in enumerate(sorted(manifest)):
        relation = "supports_stop" if index % 2 == 0 else "conflicts_visible"
        visibility = "visible" if index % 3 else "not_visible"
        record = {
            "terminal_status": "observed_deliberate",
            "terminal_event_id": "e0001",
            "effective_authority_status": "observed",
            "effective_authority": "authority",
            "visibility_to_authority": visibility,
            "authority_evidence_relation": relation,
        }
        a[alias] = dict(record)
        b[alias] = dict(record)
    passed = evaluate(manifest, a, b)
    require(passed["gate"] == "PASS", "synthetic passing gate failed")
    for alias in list(b)[:12]:
        b[alias]["effective_authority_status"] = "indeterminate"
        b[alias]["effective_authority"] = None
    failed = evaluate(manifest, a, b)
    require(failed["gate"] == "FAIL", "synthetic failing gate passed")
    return {"self_test": "PASS", "pass_fixture": passed["gate"], "fail_fixture": failed["gate"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test")
    run = subparsers.add_parser("run")
    run.add_argument("--manifest", type=Path, required=True)
    run.add_argument("--parsed-dir", type=Path, required=True)
    run.add_argument("--schema", type=Path, required=True)
    run.add_argument("--coder-a", type=Path, required=True)
    run.add_argument("--coder-b", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "self-test":
        result = self_test()
    else:
        _, manifest_rows = load_parsed_manifest(args.manifest)
        events = parsed_events(args.parsed_dir, manifest_rows)
        schema = json.loads(args.schema.read_bytes())
        ann_a, coder_a, hash_a = validate_annotation(args.coder_a, schema, manifest_rows, events)
        ann_b, coder_b, hash_b = validate_annotation(args.coder_b, schema, manifest_rows, events)
        require(ann_a["coder_id"] != ann_b["coder_id"], "coder IDs must differ")
        result = evaluate(manifest_rows, coder_a, coder_b)
        result["coder_a_sha256"] = hash_a
        result["coder_b_sha256"] = hash_b
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"tbea_agreement error={exc}", file=sys.stderr)
        raise SystemExit(2) from exc
