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
# Kaggle submit API requires.
# Kaggle's real competition rerun overwrites it with the true per-cell scores.
from pathlib import Path

SUBMISSION_ROWS = [
    ("Id", "Score"),
    ("gpt_oss_public", "0.05"),
    ("gpt_oss_private", "0.05"),
    ("gemma_public", "0.05"),
    ("gemma_private", "0.05"),
]

submit_path = Path('/kaggle/working/submission.csv')
import csv
with submit_path.open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(SUBMISSION_ROWS)

with submit_path.open('r', newline='') as f:
    rows = list(csv.reader(f))

assert rows[:1] == [["Id", "Score"]], "submission.csv header mismatch"
assert len(rows) == 5, f"submission.csv row count mismatch: {len(rows)}"
expected_ids = ["gpt_oss_public", "gpt_oss_private", "gemma_public", "gemma_private"]
actual_ids = [row_id for row_id, _ in rows[1:]]
assert actual_ids == expected_ids, f"submission.csv row-id order mismatch: {actual_ids}"
for row_id, score in rows[1:]:
    float(score)  # raises on empty/non-numeric values

print("submission.csv schema and ids are valid")

print(f"placeholder submission.csv written (rows={len(rows)-1})")

# Local validation only verifies the notebook runs; real scoring happens in Kaggle's rerun.
import kaggle_evaluation.jed_attack_134815.jed_attack_inference_server as srv
srv.JEDAttackInferenceServer().serve()
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
