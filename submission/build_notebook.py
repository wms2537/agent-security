"""Build the Kaggle submission notebook from experiments/attack.py.

The notebook: (1) puts the competition SDK on sys.path, (2) writes attack.py to /kaggle/working/,
(3) starts the JED attack inference server. Keeping the notebook generated from attack.py means the
single source of truth for the algorithm is experiments/attack.py.

Run:  python submission/build_notebook.py
"""

from __future__ import annotations

import csv
import json
import math
import os
import subprocess
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATTACK_SRC = (ROOT / "experiments" / "attack.py").read_text()
OUTS = (
    ROOT / "ai-agent-security-attack.ipynb",
    ROOT / "submission" / "kaggle_notebook.ipynb",
    ROOT / "submission" / "kernel" / "kaggle_notebook.ipynb",
)

setup = """\
import sys, glob
from pathlib import Path
# argparse guard for Kaggle
sys.argv = [sys.argv[0]]
for candidate in glob.glob('/kaggle/input/**/kaggle_evaluation', recursive=True):
    root = str(Path(candidate).parent)
    if root not in sys.path:
        sys.path.insert(0, root)
    print('Dataset root:', root)
    break
print('Setup complete')
"""

write_cell = (
    "attack_code = r'''\n"
    + ATTACK_SRC.replace("'''", "\\'\\'\\'")
    + "\n'''\n"
    "with open('/kaggle/working/attack.py', 'w') as f:\n"
    "    f.write(attack_code)\n"
    "print('attack.py written:', len(attack_code), 'bytes')\n"
)

serve = """\
# Write a placeholder submission.csv so the commit run produces the output file
# Kaggle's real competition rerun overwrites it with the true per-cell scores.
from pathlib import Path
import csv
import json
import math
import os
import sys
import traceback
import subprocess

SUBMISSION_PATHS = (
    Path('/kaggle/working/submission.csv'),
    Path('submission.csv'),
    Path('/tmp/submission.csv'),
)
SUBMISSION_ROWS = [
    ("Id", "Score"),
    ("gpt_oss_public", "0.0"),
    ("gpt_oss_private", "0.0"),
    ("gemma_public", "0.0"),
    ("gemma_private", "0.0"),
]
EXPECTED_ROW_IDS = [row_id for row_id, _ in SUBMISSION_ROWS[1:]]


def _write_placeholder_submission_csv() -> None:
    for submit_path in SUBMISSION_PATHS:
        submit_path.parent.mkdir(parents=True, exist_ok=True)
        with submit_path.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(SUBMISSION_ROWS)


def _validate_submission_csv() -> None:
    # Fail fast if the output file cannot be parsed as valid competition csv.
    for submit_path in SUBMISSION_PATHS:
        with submit_path.open('r', newline='') as f:
            rows = list(csv.reader(f))

        if len(rows) != 5:
            raise ValueError(f"{submit_path} row count mismatch: {len(rows)}")
        if rows[0] != ["Id", "Score"]:
            raise ValueError(f"{submit_path} header mismatch: {rows[0]}")

        got_ids = [row_id for row_id, _ in rows[1:]]
        if got_ids != EXPECTED_ROW_IDS:
            raise ValueError(f"{submit_path} row-id mismatch: {got_ids}")

        for row_id, score in rows[1:]:
            if row_id not in EXPECTED_ROW_IDS:
                raise ValueError(f"{submit_path} unexpected row id: {row_id}")
            score_value = float(score)
            if not math.isfinite(score_value):
                raise ValueError(f"{submit_path} non-finite score for {row_id}: {score_value}")


def _write_run_error() -> None:
    # Ensure reruns have at least a schema-valid submission when the rerun path throws.
    Path('/kaggle/working/result.json').write_text(
        json.dumps(
            {
                "Succeeded": False,
                "ErrorType": "gateway_error",
                "ErrorName": "RUNTIME_EXCEPTION",
                "ErrorDetails": "Kaggle serve path failed before completion. Placeholder submission written.",
            }
        ),
        encoding='utf-8',
    )
    _write_placeholder_submission_csv()


def _run_gateway_in_subprocess() -> None:
    gateway_source = '''import sys
import glob
from pathlib import Path

# argparse guard for Kaggle
sys.argv = [sys.argv[0]]
for candidate in glob.glob('/kaggle/input/**/kaggle_evaluation', recursive=True):
    root = str(Path(candidate).parent)
    if root not in sys.path:
        sys.path.insert(0, root)
    print('Dataset root:', root)
    break

import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv

srv.JEDAttackInferenceServer().serve()
'''

    child_script = Path('/tmp/kaggle_jed_gateway_subprocess.py')
    child_script.write_text(gateway_source, encoding='utf-8')

    result = subprocess.run(
        [sys.executable, str(child_script)],
        check=False,
        env=os.environ.copy(),
    )
    if result.returncode != 0:
        raise RuntimeError(f"gateway subprocess failed with return code {result.returncode}")


_write_placeholder_submission_csv()
_validate_submission_csv()
for submit_path in SUBMISSION_PATHS:
    with submit_path.open('r', newline='') as f:
        rows = list(csv.reader(f))
    print(f"submission csv candidate={submit_path} rows=", len(rows) - 1, sep="")

# Local validation only verifies the notebook runs; real scoring happens in Kaggle's rerun.
try:
    _run_gateway_in_subprocess()
    _validate_submission_csv()
except Exception:
    _write_run_error()
    print("[build_notebook] serve() raised; fallback artifacts written.")
    traceback.print_exc()
"""


def cell(src: str) -> dict:
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src.splitlines(keepends=True)}


nb = {
    "cells": [cell(setup), cell(write_cell), cell(serve)],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

rendered = json.dumps(nb, indent=1)
for out in OUTS:
    out.write_text(rendered)
    print(f"wrote {out} ({out.stat().st_size} bytes)")

# Sanity: the embedded attack.py must round-trip to valid Python.
import ast
ast.parse(ATTACK_SRC)
print("attack.py parses OK")
