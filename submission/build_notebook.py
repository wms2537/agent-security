"""Build the Kaggle submission notebook from experiments/attack.py.

The notebook: (1) puts the competition SDK on sys.path, (2) writes attack.py to /kaggle/working/,
(3) starts the JED attack inference server. Keeping the notebook generated from attack.py means the
single source of truth for the algorithm is experiments/attack.py.

Run:  python submission/build_notebook.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATTACK_SRC = (ROOT / "experiments" / "attack.py").read_text()
OUT = ROOT / "submission" / "kaggle_notebook.ipynb"

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

OUT.write_text(json.dumps(nb, indent=1))
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")

# Sanity: the embedded attack.py must round-trip to valid Python.
import ast
ast.parse(ATTACK_SRC)
print("attack.py parses OK")
