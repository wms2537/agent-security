#!/usr/bin/env python3
"""Lossless deterministic segmenters for the TBEA-PILOT-1 development sample."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import re
import sys
import tempfile
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def byte_offset(text: str, char_offset: int) -> int:
    return len(text[:char_offset].encode("utf-8"))


def line_for_char(text: str, char_offset: int) -> int:
    return text.count("\n", 0, char_offset) + 1


@dataclass(frozen=True)
class Span:
    start_char: int
    end_char: int
    kind: str
    actor: str | None
    recipient: str | None
    markers: tuple[str, ...]


def event_record(event_id: str, text: str, span: Span) -> dict[str, Any]:
    raw = text[span.start_char : span.end_char].encode("utf-8")
    end_probe = max(span.start_char, span.end_char - 1)
    return {
        "event_id": event_id,
        "kind": span.kind,
        "actor": span.actor,
        "recipient": span.recipient,
        "markers": list(span.markers),
        "start_byte": byte_offset(text, span.start_char),
        "end_byte": byte_offset(text, span.end_char),
        "start_line": line_for_char(text, span.start_char),
        "end_line": line_for_char(text, end_probe),
        "source_sha256": sha256_bytes(raw),
        "source_bytes": len(raw),
    }


def ag2_dict_spans(text: str) -> list[tuple[int, int]]:
    tokens = tokenize.generate_tokens(io.StringIO(text).readline)
    depth = 0
    start: int | None = None
    spans: list[tuple[int, int]] = []
    for token in tokens:
        if token.type == tokenize.OP and token.string == "{":
            if depth == 0:
                require(token.start[0] == 1, "AG2 token unexpectedly spans physical lines")
                start = token.start[1]
            depth += 1
        elif token.type == tokenize.OP and token.string == "}":
            depth -= 1
            require(depth >= 0, "AG2 unbalanced closing brace")
            if depth == 0:
                require(start is not None, "AG2 missing opening brace")
                require(token.end[0] == 1, "AG2 token unexpectedly spans physical lines")
                spans.append((start, token.end[1]))
                start = None
    require(depth == 0 and spans, "AG2 top-level message parse failed")
    return spans


def parse_ag2(text: str) -> list[Span]:
    spans: list[Span] = []
    cursor = 0
    for start, end in ag2_dict_spans(text):
        if cursor < start:
            spans.append(Span(cursor, start, "raw_gap", None, None, ()))
        value = ast.literal_eval(text[start:end])
        require(isinstance(value, dict), "AG2 segment is not a dictionary")
        actor = str(value.get("name") or value.get("role") or "") or None
        content = value.get("content", [])
        if isinstance(content, list):
            semantic_text = "\n".join(str(item) for item in content)
        else:
            semantic_text = str(content)
        markers: list[str] = []
        if "SOLUTION_FOUND" in semantic_text:
            markers.append("explicit_terminal_token")
        if "\\boxed{" in semantic_text:
            markers.append("boxed_answer")
        spans.append(Span(start, end, "message", actor, None, tuple(markers)))
        cursor = end
    if cursor < len(text):
        spans.append(Span(cursor, len(text), "raw_gap", None, None, ()))
    return spans


APPWORLD_HEADERS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^\*+ Task .+\*+\s*$"), "task"),
    (re.compile(r"^Response from .+ Agent\s*$"), "agent_response"),
    (re.compile(r"^\s*Message to .+ Agent\s*$"), "agent_message"),
    (re.compile(r"^\s*Reply from .+ Agent to Supervisor\s*$"), "agent_reply"),
    (re.compile(r"^Entering .+ Agent message loop\s*$"), "loop_enter"),
    (re.compile(r"^Exiting .+ Agent message loop\s*$"), "loop_exit"),
    (re.compile(r"^Response from send_message API\s*$"), "api_response"),
    (re.compile(r"^Code Execution Output\s*$"), "code_output"),
    (re.compile(r"^Evaluation\s*$"), "evaluation"),
]


def appworld_header(line: str) -> tuple[str, str | None, str | None] | None:
    stripped = line.rstrip("\r\n")
    kind: str | None = None
    for pattern, candidate_kind in APPWORLD_HEADERS:
        if pattern.match(stripped):
            kind = candidate_kind
            break
    if kind is None:
        return None
    actor: str | None = None
    recipient: str | None = None
    match = re.match(r"^Response from (.+) Agent\s*$", stripped)
    if match:
        actor = match.group(1)
    match = re.match(r"^\s*Message to (.+) Agent\s*$", stripped)
    if match:
        actor = "delivery_path"
        recipient = match.group(1)
    match = re.match(r"^\s*Reply from (.+) Agent to Supervisor\s*$", stripped)
    if match:
        actor = match.group(1)
        recipient = "Supervisor"
    if kind in {"loop_enter", "loop_exit"}:
        actor = "orchestrator_log"
    elif kind == "api_response":
        actor = "send_message_api"
    elif kind == "code_output":
        actor = "execution_environment"
    elif kind == "evaluation":
        actor = "evaluation_harness"
    elif kind == "task":
        actor = "task_source"
    return kind, actor, recipient


def line_starts(text: str) -> list[int]:
    starts = [0]
    for match in re.finditer("\n", text):
        starts.append(match.end())
    return starts


def parse_appworld(text: str) -> list[Span]:
    starts = line_starts(text)
    headers: list[tuple[int, str, str | None, str | None]] = []
    for start in starts:
        end = text.find("\n", start)
        if end < 0:
            end = len(text)
        parsed = appworld_header(text[start:end])
        if parsed is not None:
            kind, actor, recipient = parsed
            headers.append((start, kind, actor, recipient))
    require(headers, "AppWorld headings absent")
    if headers[0][0] != 0:
        headers.insert(0, (0, "preamble", None, None))
    spans: list[Span] = []
    for index, (start, kind, actor, recipient) in enumerate(headers):
        end = headers[index + 1][0] if index + 1 < len(headers) else len(text)
        segment = text[start:end]
        markers: list[str] = []
        if re.search(r"\bapis\.supervisor\.complete_task\s*\(", segment):
            markers.append("explicit_terminal_api")
        if re.search(r"\b(status\s*=\s*['\"]fail['\"]|mark the task as failed)\b", segment, re.I):
            markers.append("failure_terminal_claim")
        if kind in {"agent_message", "agent_reply", "api_response"}:
            markers.append("explicit_delivery")
        spans.append(Span(start, end, kind, actor, recipient, tuple(markers)))
    return spans


META_HEADER = re.compile(r"^\[[^\]]+\] (?:FROM:|NEW MESSAGES:)", re.M)
META_END = re.compile(r"^=== Communication Log Ended at .+ ===\s*$", re.M)


def parse_metagpt(text: str) -> list[Span]:
    positions = [(match.start(), "message_block") for match in META_HEADER.finditer(text)]
    positions.extend((match.start(), "log_end") for match in META_END.finditer(text))
    positions.sort()
    require(positions, "MetaGPT headings absent")
    if positions[0][0] != 0:
        positions.insert(0, (0, "preamble"))
    spans: list[Span] = []
    for index, (start, kind) in enumerate(positions):
        end = positions[index + 1][0] if index + 1 < len(positions) else len(text)
        segment = text[start:end]
        actor: str | None = None
        recipient: str | None = None
        markers: list[str] = []
        if kind == "message_block":
            first_line = segment.splitlines()[0] if segment.splitlines() else ""
            from_match = re.search(r"FROM:\s*([^\s]+)\s+TO:\s*(.+)$", first_line)
            if from_match:
                actor = from_match.group(1)
                recipient = from_match.group(2)
            else:
                actor_match = re.search(r"\n\s*\n([A-Za-z][A-Za-z0-9_ -]*):", segment)
                if actor_match:
                    actor = actor_match.group(1).strip()
        elif kind == "log_end":
            actor = "logger"
            markers.append("implicit_log_end")
        spans.append(Span(start, end, kind, actor, recipient, tuple(markers)))
    return spans


PARSERS: dict[str, tuple[str, Callable[[str], list[Span]]]] = {
    "AG2": ("ag2-python-literal-messages-v1", parse_ag2),
    "AppWorld": ("appworld-heading-blocks-v1", parse_appworld),
    "MetaGPT": ("metagpt-timestamp-blocks-v1", parse_metagpt),
}


def randomized_alias(cluster_id: str) -> str:
    digest = sha256_bytes(b"TBEA-PILOT-1-CODER-ALIASES\x00" + cluster_id.encode("ascii"))
    return "T" + digest[:12]


def parser_source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def parse_bundle(bundle_dir: Path, output_dir: Path) -> dict[str, Any]:
    require(not output_dir.exists(), "parsed output already exists; stale reuse forbidden")
    bundle_raw = (bundle_dir / "bundle.json").read_bytes()
    bundle = json.loads(bundle_raw)
    require(bundle["contract_version"] == "TBEA-PILOT-1", "wrong bundle version")
    output_dir.mkdir(parents=True)
    parsed_rows: list[dict[str, Any]] = []
    for row in bundle["rows"]:
        system = row["mas_name"]
        require(system in PARSERS, f"no frozen parser for {system}")
        parser_id, parser = PARSERS[system]
        text_path = bundle_dir / row["text_file"]
        text = text_path.read_text(encoding="utf-8")
        require(sha256_bytes(text.encode("utf-8")) == row["trajectory_sha256"], "source drift")
        spans = parser(text)
        require(spans and spans[0].start_char == 0, "parser does not start at byte zero")
        require(spans[-1].end_char == len(text), "parser does not end at EOF")
        require(
            all(left.end_char == right.start_char for left, right in zip(spans, spans[1:])),
            "parser leaves a gap or overlap",
        )
        events = [event_record(f"e{index:04d}", text, span) for index, span in enumerate(spans)]
        alias = randomized_alias(row["cluster_id"])
        parsed_file = f"{alias}.json"
        parsed_record = {
            "contract_version": "TBEA-PILOT-1",
            "trace_alias": alias,
            "mas_name": system,
            "parser_id": parser_id,
            "source_text_file": row["text_file"],
            "source_sha256": row["trajectory_sha256"],
            "source_bytes": row["trajectory_bytes"],
            "events": events,
        }
        parsed_bytes = canonical_bytes(parsed_record) + b"\n"
        (output_dir / parsed_file).write_bytes(parsed_bytes)
        parsed_rows.append(
            {
                "trace_alias": alias,
                "mas_name": system,
                "cluster_id": row["cluster_id"],
                "source_text_file": row["text_file"],
                "source_sha256": row["trajectory_sha256"],
                "parser_id": parser_id,
                "parsed_file": parsed_file,
                "parsed_sha256": sha256_bytes(parsed_bytes),
                "event_count": len(events),
            }
        )
    require(len({row["trace_alias"] for row in parsed_rows}) == len(parsed_rows), "alias collision")
    parsed_rows.sort(key=lambda row: row["trace_alias"])
    manifest = {
        "contract_version": "TBEA-PILOT-1",
        "bundle_sha256": sha256_bytes(bundle_raw),
        "parser_source_sha256": parser_source_sha256(),
        "rows": parsed_rows,
    }
    manifest_raw = canonical_bytes(manifest) + b"\n"
    (output_dir / "parsed-manifest.json").write_bytes(manifest_raw)
    result = verify_parsed(bundle_dir, output_dir)
    result["parsed_manifest_sha256"] = sha256_bytes(manifest_raw)
    return result


def verify_parsed(bundle_dir: Path, parsed_dir: Path) -> dict[str, Any]:
    manifest_raw = (parsed_dir / "parsed-manifest.json").read_bytes()
    manifest = json.loads(manifest_raw)
    require(manifest["contract_version"] == "TBEA-PILOT-1", "manifest version mismatch")
    require(manifest["parser_source_sha256"] == parser_source_sha256(), "parser source drift")
    bundle_raw = (bundle_dir / "bundle.json").read_bytes()
    require(manifest["bundle_sha256"] == sha256_bytes(bundle_raw), "bundle identity mismatch")
    rows = manifest["rows"]
    require(len(rows) == 18, "parsed row count mismatch")
    total_events = 0
    marker_counts: dict[str, int] = {}
    for row in rows:
        parsed_raw = (parsed_dir / row["parsed_file"]).read_bytes()
        require(sha256_bytes(parsed_raw) == row["parsed_sha256"], "parsed file drift")
        parsed = json.loads(parsed_raw)
        source = (bundle_dir / row["source_text_file"]).read_bytes()
        require(sha256_bytes(source) == row["source_sha256"], "source file drift")
        cursor = 0
        for event in parsed["events"]:
            require(event["start_byte"] == cursor, "event coverage gap or overlap")
            segment = source[event["start_byte"] : event["end_byte"]]
            require(sha256_bytes(segment) == event["source_sha256"], "event source hash mismatch")
            require(len(segment) == event["source_bytes"], "event byte count mismatch")
            cursor = event["end_byte"]
            for marker in event["markers"]:
                marker_counts[marker] = marker_counts.get(marker, 0) + 1
        require(cursor == len(source), "event coverage does not reach EOF")
        require(len(parsed["events"]) == row["event_count"], "event count mismatch")
        total_events += len(parsed["events"])
    return {
        "parsed_bundle": "PASS",
        "rows": len(rows),
        "events": total_events,
        "source_span_match_rate": "1.0",
        "marker_counts": json.dumps(marker_counts, sort_keys=True, separators=(",", ":")),
    }


def self_test() -> dict[str, Any]:
    samples = {
        "AG2": "{'content':['SOLUTION_FOUND'], 'role':'assistant', 'name':'Verifier'} {'content':['next'], 'role':'user', 'name':'Worker'}",
        "AppWorld": "\nResponse from Supervisor Agent\n    apis.supervisor.complete_task(status=\"fail\")\n\nCode Execution Output\n    ok\n",
        "MetaGPT": "=== Log ===\n[2026-01-01 00:00:00] NEW MESSAGES:\n\nSimpleReviewer: done\n=== Communication Log Ended at 2026 ===\n",
    }
    counts: dict[str, int] = {}
    with tempfile.TemporaryDirectory(prefix="tbea-parser-self-test-") as directory:
        require(Path(directory).is_dir(), "temporary directory unavailable")
        for system, text in samples.items():
            _, parser = PARSERS[system]
            spans = parser(text)
            require(spans[0].start_char == 0 and spans[-1].end_char == len(text), "coverage boundary")
            require(all(a.end_char == b.start_char for a, b in zip(spans, spans[1:])), "coverage continuity")
            events = [event_record(f"e{i:04d}", text, span) for i, span in enumerate(spans)]
            raw = text.encode("utf-8")
            for event in events:
                segment = raw[event["start_byte"] : event["end_byte"]]
                require(sha256_bytes(segment) == event["source_sha256"], "synthetic source mismatch")
            counts[system] = len(events)
    require(any("explicit_terminal_token" in span.markers for span in parse_ag2(samples["AG2"])), "AG2 marker")
    require(any("explicit_terminal_api" in span.markers for span in parse_appworld(samples["AppWorld"])), "AppWorld marker")
    require(any("implicit_log_end" in span.markers for span in parse_metagpt(samples["MetaGPT"])), "MetaGPT marker")
    return {"self_test": "PASS", "systems": len(counts), "events": sum(counts.values())}


def print_result(result: dict[str, Any]) -> None:
    fields = " ".join(f"{key}={value}" for key, value in result.items())
    print(f"tbea_parser {fields}")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("self-test")
    parse_command = subparsers.add_parser("parse")
    parse_command.add_argument("--bundle", type=Path, required=True)
    parse_command.add_argument("--output", type=Path, required=True)
    verify_command = subparsers.add_parser("verify")
    verify_command.add_argument("--bundle", type=Path, required=True)
    verify_command.add_argument("--parsed", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "self-test":
        print_result(self_test())
    elif args.command == "parse":
        print_result(parse_bundle(args.bundle, args.output))
    elif args.command == "verify":
        print_result(verify_parsed(args.bundle, args.parsed))
    else:
        raise AssertionError(args.command)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, SyntaxError, json.JSONDecodeError) as exc:
        print(f"tbea_parser error={exc}", file=sys.stderr)
        raise SystemExit(2) from exc
