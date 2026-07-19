"""Public, non-target reference checks for the ORF held-out-v7 contract.

This module never fetches a beacon, derives a target master, generates held-out
profiles, evaluates the hypothesis, or invokes Kaggle.  It checks only frozen SDK
semantics, the finite mixture scheduler, schemas, hashes, and preserved fixtures.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Iterator, Mapping, Sequence
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO = Path(__file__).resolve().parents[2]
SDK_ROOT = REPO / "comp" / "sdk"
sys.path.insert(0, str(SDK_ROOT))

from aicomp_sdk.core.cells import cell_signature  # noqa: E402
from aicomp_sdk.core.predicates import eval_predicates  # noqa: E402
from aicomp_sdk.scoring import get_score_cell_hash, score_attack_raw  # noqa: E402


LENGTHS = (1, 2, 4, 8, 16, 24, 32)
HEX16 = re.compile(r"^[0-9a-f]{16}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def compositions(total: int, width: int, prefix: tuple[int, ...] = ()) -> Iterator[tuple[int, ...]]:
    if width == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from compositions(total - value, width - 1, prefix + (value,))


def mixture_cycle(h: Sequence[int]) -> tuple[int, ...]:
    """Return the unique eight-attempt cycle defined by held-out-v7.

    Counts are cycle-local.  Slot ``t`` is zero-based.  Eligibility is strict
    ``count[i] < h[i]``.  The chosen action maximizes the exact integer deficit,
    with smaller action length breaking ties.  Counts advance only for an emitted
    attempt; the caller never invokes the next slot after a precheck stop.
    """

    require(len(h) == len(LENGTHS), "mixture width must be seven")
    require(all(isinstance(value, int) and value >= 0 for value in h), "invalid h")
    require(sum(h) == 8, "mixture denominator must be eight")
    counts = [0] * len(LENGTHS)
    scheduled: list[int] = []
    for t in range(8):
        eligible = [i for i, value in enumerate(h) if counts[i] < value]
        require(bool(eligible), f"empty eligibility at slot {t}")
        index = max(
            eligible,
            key=lambda i: ((t + 1) * h[i] - 8 * counts[i], -LENGTHS[i]),
        )
        scheduled.append(LENGTHS[index])
        counts[index] += 1
    require(tuple(counts) == tuple(h), "cycle counts do not equal h")
    return tuple(scheduled)


def terminal_key(payload: Mapping[str, Any]) -> str:
    return sha256_bytes(b"orf-terminal-post-v1\0" + canonical_json_bytes(payload))


def terminal_message(payload: Mapping[str, Any], key: str) -> str:
    return (
        f"ORF-B TERMINAL POST_KEY={key} "
        f"COMMIT={payload['terminal_commit']} "
        f"STATUS={payload['scientific_status']} "
        f"CUSTODY={payload['custody_status']} "
        f"OUTCOME_SHA256={payload['outcome_sha256']} "
        f"RESOLVED_RESULTS_SHA256={payload['resolved_results_sha256']} "
        f"TERMINAL_ARTIFACT_SHA256={payload['terminal_artifact_sha256']} "
        f"SUMMARY_SHA256={payload['summary_sha256_or_na']} "
        f"ROOT_RESULTS_SHA256={payload['root_results_sha256_or_na']}"
    )


def check_sdk_cases(fixtures: Mapping[str, Any]) -> list[str]:
    hashes: list[str] = []
    for case in fixtures["sdk_cases"]:
        require(sha256_bytes(case["candidate_preimage"].encode("utf-8")) == case["candidate_id"], f"{case['name']}: candidate ID")
        require(bool(HEX64.fullmatch(case["candidate_id"])), f"{case['name']}: candidate ID shape")
        trace = case["trace"]
        predicates = eval_predicates(trace)
        require(predicates == case["expected_predicates"], f"{case['name']}: predicates")
        require(len(predicates) == case["event_count"], f"{case['name']}: predicate count")
        score_signature = cell_signature(trace["tool_events"])
        score_hash = score_signature["hash"]
        require(score_hash == case["expected_score_cell_hash"], f"{case['name']}: score hash")
        require(bool(HEX16.fullmatch(score_hash)), f"{case['name']}: score hash shape")
        finding = {
            "trace": trace,
            "predicates": predicates,
            "score_cell_signature": score_signature,
        }
        require(get_score_cell_hash(finding) == score_hash, f"{case['name']}: scorer hash path")
        require(score_attack_raw([finding]) == case["expected_sdk_raw"], f"{case['name']}: raw score")
        require(case["expected_sdk_raw"] == 16 * case["event_count"] + 2, f"{case['name']}: q formula")
        hashes.append(score_hash)
    require(len(hashes) == len(set(hashes)), "golden score hashes collide")
    return hashes


def check_mixtures(fixtures: Mapping[str, Any]) -> int:
    all_h = list(compositions(8, 7))
    require(len(all_h) == 3003, "composition count")
    require(all_h == sorted(all_h), "composition order")
    for h in all_h:
        mixture_cycle(h)
    for case in fixtures["mixture_cases"]:
        require(mixture_cycle(case["h"]) == tuple(case["expected_cycle"]), f"{case['name']}: cycle")
        require(mixture_cycle(case["h"]) * 2 == tuple(case["expected_cycle"]) * 2, f"{case['name']}: repeat/reset")
    return len(all_h)


def check_terminal_fixtures(fixtures: Mapping[str, Any], validator: Draft202012Validator) -> None:
    terminal = fixtures["terminal_publication"]
    payload = terminal["payload"]
    key = terminal_key(payload)
    message = terminal_message(payload, key)
    require(key == terminal["expected_idempotency_key"], "terminal key")
    require(message == terminal["expected_message"], "terminal message")
    require(sha256_bytes(message.encode("utf-8")) == terminal["expected_message_sha256"], "terminal message hash")
    require(sha256_bytes(canonical_json_bytes(terminal["intent_sample"])) == terminal["intent_sample_sha256"], "intent sample hash")
    for name in ("intent_sample", "receipt_sample", "failure_sample"):
        errors = sorted(validator.iter_errors(terminal[name]), key=lambda error: list(error.path))
        require(not errors, f"{name}: {errors[0].message if errors else 'schema'}")
    require(terminal["intent_sample"]["idempotency_key"] == key, "intent/key cross-check")
    require(terminal["intent_sample"]["publication_message"] == message, "intent/message cross-check")
    require(terminal["receipt_sample"]["intent_sha256"] == terminal["intent_sample_sha256"], "receipt/intent cross-check")
    require(terminal["receipt_sample"]["external_message_sha256"] == terminal["expected_message_sha256"], "receipt/message cross-check")
    bad = dict(terminal["intent_sample"])
    bad["publication_message"] += " CORRUPTED"
    require(bool(list(validator.iter_errors(bad))), "corrupted terminal message must fail schema")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--fixtures", required=True, type=Path)
    args = parser.parse_args()

    contract_path = (REPO / args.contract).resolve() if not args.contract.is_absolute() else args.contract.resolve()
    schema_path = (REPO / args.schema).resolve() if not args.schema.is_absolute() else args.schema.resolve()
    fixtures_path = (REPO / args.fixtures).resolve() if not args.fixtures.is_absolute() else args.fixtures.resolve()
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    fixtures = json.loads(fixtures_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    require(contract["contract_version"] == "orf-heldout-v7", "contract version")
    expected_validators = [f"V{i:02d}" for i in range(1, 19)]
    require(list(contract["validator_predicates"]) == expected_validators, "validator key sequence")
    error_codes = contract["protocol_error_codes"]
    require(len(error_codes) == len(set(error_codes)) == 24, "protocol error codes")
    require(schema["$defs"]["protocolError"]["enum"] == error_codes, "schema protocol error codes")
    require(schema["$defs"]["failureCounts"]["required"] == error_codes, "failure-count keys")
    require(schema["$defs"]["sourceHashes"]["required"] == list(contract["source_hashes_sha256"]), "source-hash keys")
    require(contract["constants"]["mixture_count"] == 3003, "contract mixture count")
    require(contract["review_accounting"] == {"hypothesis_review_limit": 10, "hypothesis_review_spent": 10, "new_dispatch_authorized": False, "gate_status": "not_rigorous_revision_unreviewed"}, "review accounting")
    require(all(contract["commands"][key] is None for key in ("heldout_evaluator", "freeze", "reveal_evaluate", "kaggle")), "forbidden commands must be null")
    require(contract["golden_fixtures"]["path"] == str(fixtures_path.relative_to(REPO)), "fixture path")
    fixture_hash = sha256_file(fixtures_path)
    require(contract["golden_fixtures"]["sha256"] == fixture_hash, "fixture hash")
    require(contract["artifact_schema"]["path"] == str(schema_path.relative_to(REPO)), "schema path")
    require(contract["artifact_schema"]["sha256"] == sha256_file(schema_path), "schema hash")
    checker_path = Path(__file__).resolve()
    require(contract["reference_checker"]["path"] == str(checker_path.relative_to(REPO)), "checker path")
    require(contract["reference_checker"]["sha256"] == sha256_file(checker_path), "checker hash")

    for relative, expected in contract["source_hashes_sha256"].items():
        require(sha256_file(REPO / relative) == expected, f"source hash: {relative}")

    score_hashes = check_sdk_cases(fixtures)
    mixture_count = check_mixtures(fixtures)
    check_terminal_fixtures(fixtures, validator)
    run_dir = REPO / contract["outputs"]["directory"]
    require(not run_dir.exists(), "held-out run directory must remain absent")

    print(f"contract_version={contract['contract_version']}")
    print(f"sdk_golden_cases={len(fixtures['sdk_cases'])} score_hashes={','.join(score_hashes)}")
    print(f"mixture_compositions={mixture_count} cycles_exact={mixture_count}")
    print("terminal_artifact_samples=3 schema_valid=true")
    print(f"source_hashes={len(contract['source_hashes_sha256'])} valid=true")
    print(f"protocol_errors={len(error_codes)} validators={len(expected_validators)} aligned=true")
    print(f"fixtures_sha256={fixture_hash}")
    print("heldout_run_absent=true")


if __name__ == "__main__":
    main()
