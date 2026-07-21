#!/usr/bin/env python3
"""Prepare and verify a label-blind MAST development bundle for TBEA-PILOT-1.

This program never evaluates MAST labels. It creates a deterministic development
sample using only whitelisted metadata and trajectory bytes. Generated source
and bundle files live under the ignored artifacts/ tree and are not paper data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Candidate:
    source_ordinal: int
    mas_name: str
    llm_name: str
    benchmark_name: str
    trace_id: str
    trace_index: str
    trace_key: str
    trajectory: str
    trajectory_sha256: str
    cluster_id: str


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    return canonical_bytes(value).decode("utf-8")


def candidate_from_record(record: dict[str, Any], source_ordinal: int) -> Candidate:
    allowed_record = {
        "mas_name",
        "llm_name",
        "benchmark_name",
        "trace_id",
        "trace",
    }
    require(allowed_record.issubset(record), f"row {source_ordinal}: missing source field")
    trace = record["trace"]
    require(isinstance(trace, dict), f"row {source_ordinal}: trace is not an object")
    require(
        {"index", "key", "trajectory"}.issubset(trace),
        f"row {source_ordinal}: missing trace field",
    )
    trajectory = trace["trajectory"]
    require(isinstance(trajectory, str), f"row {source_ordinal}: trajectory is not text")
    mas_name = as_text(record["mas_name"])
    llm_name = as_text(record["llm_name"])
    benchmark_name = as_text(record["benchmark_name"])
    trace_id = as_text(record["trace_id"])
    trace_index = as_text(trace["index"])
    trace_key = as_text(trace["key"])
    trajectory_sha = sha256_bytes(trajectory.encode("utf-8"))
    cluster_payload = [mas_name, llm_name, benchmark_name, trace_id, trace_index]
    cluster_id = sha256_bytes(canonical_bytes(cluster_payload))
    return Candidate(
        source_ordinal=source_ordinal,
        mas_name=mas_name,
        llm_name=llm_name,
        benchmark_name=benchmark_name,
        trace_id=trace_id,
        trace_index=trace_index,
        trace_key=trace_key,
        trajectory=trajectory,
        trajectory_sha256=trajectory_sha,
        cluster_id=cluster_id,
    )


def cluster_representatives(candidates: Iterable[Candidate]) -> list[Candidate]:
    clusters: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        clusters.setdefault(candidate.cluster_id, []).append(candidate)
    return [
        min(rows, key=lambda row: (row.trajectory_sha256, row.source_ordinal))
        for _, rows in sorted(clusters.items())
    ]


def select_sample(
    records: list[dict[str, Any]], systems: list[str], per_system: int, seed: str
) -> tuple[list[Candidate], dict[str, int]]:
    candidates = [candidate_from_record(record, i) for i, record in enumerate(records)]
    representatives = cluster_representatives(candidates)
    selected: list[Candidate] = []
    population_by_system: dict[str, int] = {}
    for system in systems:
        eligible = [row for row in representatives if row.mas_name == system]
        population_by_system[system] = len(eligible)
        require(len(eligible) >= per_system, f"{system}: fewer than {per_system} clusters")
        ranked = sorted(
            eligible,
            key=lambda row: (
                sha256_bytes(seed.encode("utf-8") + b"\x00" + row.cluster_id.encode("ascii")),
                row.cluster_id,
            ),
        )
        selected.extend(ranked[:per_system])
    require(len({row.cluster_id for row in selected}) == len(selected), "duplicate sample cluster")
    return selected, population_by_system


def read_config(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    config = json.loads(raw)
    require(config["contract_version"] == "TBEA-PILOT-1", "wrong contract version")
    return config, sha256_bytes(raw)


def bundle_manifest(
    selected: list[Candidate],
    population_by_system: dict[str, int],
    config_sha256: str,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for sample_ordinal, row in enumerate(selected):
        text_name = f"trace-{sample_ordinal:02d}-{row.mas_name.lower()}-{row.cluster_id[:12]}.txt"
        text_bytes = row.trajectory.encode("utf-8")
        rows.append(
            {
                "sample_ordinal": sample_ordinal,
                "source_ordinal": row.source_ordinal,
                "mas_name": row.mas_name,
                "llm_name": row.llm_name,
                "benchmark_name": row.benchmark_name,
                "trace_id": row.trace_id,
                "trace_index": row.trace_index,
                "trace_key": row.trace_key,
                "cluster_id": row.cluster_id,
                "trajectory_sha256": row.trajectory_sha256,
                "trajectory_bytes": len(text_bytes),
                "trajectory_lines": len(row.trajectory.splitlines()),
                "text_file": text_name,
            }
        )
    return {
        "contract_version": "TBEA-PILOT-1",
        "blinding": "mast labels absent; development-only sample",
        "config_sha256": config_sha256,
        "population_cluster_representatives_by_system": population_by_system,
        "rows": rows,
    }


def prepare(source: Path, config_path: Path, output_dir: Path) -> dict[str, Any]:
    config, config_sha = read_config(config_path)
    require(source.stat().st_size == config["source"]["bytes"], "source byte-size mismatch")
    require(file_sha256(source) == config["source"]["sha256"], "source sha256 mismatch")
    records = json.loads(source.read_bytes())
    require(isinstance(records, list), "source root is not an array")
    require(len(records) == config["source"]["rows"], "source row-count mismatch")
    sample_config = config["sample"]
    selected, populations = select_sample(
        records,
        list(sample_config["systems"]),
        int(sample_config["per_system"]),
        str(sample_config["seed"]),
    )
    require(len(selected) == sample_config["total"], "sample total mismatch")
    require(not output_dir.exists(), "output directory already exists; stale reuse forbidden")
    output_dir.mkdir(parents=True)
    manifest = bundle_manifest(selected, populations, config_sha)
    manifest_bytes = canonical_bytes(manifest) + b"\n"
    forbidden_key = config["blinding"]["forbidden_output_key"].encode("utf-8")
    require(forbidden_key not in manifest_bytes, "forbidden label key reached manifest")
    for candidate, row in zip(selected, manifest["rows"], strict=True):
        text_path = output_dir / row["text_file"]
        text_path.write_text(candidate.trajectory, encoding="utf-8", newline="")
    (output_dir / "bundle.json").write_bytes(manifest_bytes)
    result = verify_bundle(config_path, output_dir)
    result["source_sha256"] = file_sha256(source)
    result["source_rows"] = len(records)
    return result


def verify_bundle(config_path: Path, output_dir: Path) -> dict[str, Any]:
    config, config_sha = read_config(config_path)
    manifest_path = output_dir / "bundle.json"
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)
    require(manifest["contract_version"] == config["contract_version"], "bundle version mismatch")
    require(manifest["config_sha256"] == config_sha, "bundle config hash mismatch")
    forbidden_key = config["blinding"]["forbidden_output_key"].encode("utf-8")
    require(forbidden_key not in raw, "forbidden label key in bundle")
    rows = manifest["rows"]
    require(len(rows) == config["sample"]["total"], "bundle row-count mismatch")
    require(len({row["cluster_id"] for row in rows}) == len(rows), "duplicate cluster in bundle")
    actual_counts = {system: 0 for system in config["sample"]["systems"]}
    for row in rows:
        require(row["mas_name"] in actual_counts, "unexpected system in bundle")
        actual_counts[row["mas_name"]] += 1
        text_path = output_dir / row["text_file"]
        text_bytes = text_path.read_bytes()
        require(sha256_bytes(text_bytes) == row["trajectory_sha256"], "trajectory hash mismatch")
        require(len(text_bytes) == row["trajectory_bytes"], "trajectory size mismatch")
        require(len(text_bytes.decode("utf-8").splitlines()) == row["trajectory_lines"], "line mismatch")
    expected_count = config["sample"]["per_system"]
    require(all(count == expected_count for count in actual_counts.values()), "system count mismatch")
    return {
        "bundle": "PASS",
        "rows": len(rows),
        "systems": len(actual_counts),
        "per_system": expected_count,
        "labels_exposed": False,
        "config_sha256": config_sha,
        "bundle_sha256": sha256_bytes(raw),
    }


def synthetic_record(system: str, trace_id: str, trajectory: str, annotation: int) -> dict[str, Any]:
    return {
        "mas_name": system,
        "llm_name": "model",
        "benchmark_name": "benchmark",
        "trace_id": trace_id,
        "trace": {"index": trace_id, "key": f"key-{trace_id}", "trajectory": trajectory},
        "mast_annotation": {"3.1": annotation},
    }


def self_test() -> dict[str, Any]:
    systems = ["AG2", "AppWorld", "MetaGPT"]
    records: list[dict[str, Any]] = []
    for system in systems:
        for index in range(4):
            records.append(synthetic_record(system, str(index), f"{system} trace {index}\n", index % 2))
    # Same composite identity, different bytes: lexical trajectory hash selects one deterministically.
    records.append(synthetic_record("AG2", "0", "AG2 duplicate trace\n", 1))
    first, populations = select_sample(records, systems, 2, "synthetic-seed")
    second, _ = select_sample(list(reversed(records)), systems, 2, "synthetic-seed")
    require([row.cluster_id for row in first] == [row.cluster_id for row in second], "order dependence")
    require(len(first) == 6 and all(value == 4 for value in populations.values()), "selection counts")
    with tempfile.TemporaryDirectory(prefix="tbea-pilot-self-test-") as directory:
        manifest = bundle_manifest(first, populations, "0" * 64)
        raw = canonical_bytes(manifest)
        require(b"mast_annotation" not in raw, "label key escaped synthetic blinding")
        require(all("mast_annotation" not in row for row in manifest["rows"]), "row label escaped")
        require(Path(directory).is_dir(), "temporary directory unavailable")
    return {
        "self_test": "PASS",
        "synthetic_records": len(records),
        "clusters": sum(populations.values()),
        "selected": len(first),
        "labels_exposed": False,
    }


def print_result(prefix: str, result: dict[str, Any]) -> None:
    fields = " ".join(f"{key}={str(value).lower() if isinstance(value, bool) else value}" for key, value in result.items())
    print(f"{prefix} {fields}")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test")
    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--source", type=Path, required=True)
    prepare_parser.add_argument("--config", type=Path, required=True)
    prepare_parser.add_argument("--output", type=Path, required=True)
    verify_parser = subparsers.add_parser("verify-bundle")
    verify_parser.add_argument("--config", type=Path, required=True)
    verify_parser.add_argument("--bundle", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "self-test":
        print_result("tbea_pilot", self_test())
    elif args.command == "prepare":
        print_result("tbea_pilot", prepare(args.source, args.config, args.output))
    elif args.command == "verify-bundle":
        print_result("tbea_pilot", verify_bundle(args.config, args.bundle))
    else:
        raise AssertionError(args.command)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"tbea_pilot error={exc}", file=sys.stderr)
        raise SystemExit(2) from exc
