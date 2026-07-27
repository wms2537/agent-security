"""Build the Kaggle submission notebook from experiments/attack.py.

The notebook: (1) puts the competition SDK on sys.path, (2) writes attack.py to /kaggle/working/,
(3) starts the JED attack inference server. Keeping the notebook generated from attack.py means the
single source of truth for the algorithm is experiments/attack.py.

Run:  python submission/build_notebook.py
"""

from __future__ import annotations

import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATTACK_SRC = (ROOT / "experiments" / "attack.py").read_text()
OUTS = (
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
# Write a placeholder submission.csv so the commit run produces the output file the
# Kaggle submit API expects. Kaggle's real competition rerun overwrites it with true
# per-cell scores.
from pathlib import Path
import csv
import json
import traceback

SUBMISSION_ROWS = [
    ("Id", "Score"),
    ("gpt_oss_public", "0.05"),
    ("gpt_oss_private", "0.05"),
    ("gemma_public", "0.05"),
    ("gemma_private", "0.05"),
]


def _write_placeholder_submission_csv() -> None:
    submit_path = Path('/kaggle/working/submission.csv')
    with submit_path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(SUBMISSION_ROWS)
    submit_path.write_text(submit_path.read_text(encoding='utf-8'), encoding='utf-8')


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


_write_placeholder_submission_csv()
with Path('/kaggle/working/submission.csv').open('r', newline='') as f:
    rows = list(csv.reader(f))
print("placeholder submission.csv written (rows=", len(rows) - 1, ")", sep="")

# Local validation only verifies the notebook runs; real scoring happens in Kaggle's rerun.
import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv
try:
    srv.JEDAttackInferenceServer().serve()
except Exception:
    _write_run_error()
    print("[build_notebook] serve() raised; fallback artifacts written.")
    traceback.print_exc()
    raise
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
