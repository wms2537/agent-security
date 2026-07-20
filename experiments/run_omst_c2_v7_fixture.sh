#!/usr/bin/env bash
set -euo pipefail

/usr/bin/env -i \
  LANG=C LC_ALL=C TZ=UTC PYTHONHASHSEED=0 PYTHONNOUSERSITE=1 \
  /home/soh/agent-security/comp/.venv/bin/python -I -B \
  /home/soh/agent-security/experiments/omst_c2_v7_fixture.py \
  --cell task_s0

/usr/bin/env -i \
  LANG=C LC_ALL=C TZ=UTC PYTHONHASHSEED=0 PYTHONNOUSERSITE=1 \
  /home/soh/agent-security/comp/.venv/bin/python -I -B \
  /home/soh/agent-security/experiments/omst_c2_v7_fixture.py \
  --cell task_s1

/usr/bin/env -i \
  LANG=C LC_ALL=C TZ=UTC PYTHONHASHSEED=0 PYTHONNOUSERSITE=1 \
  /home/soh/agent-security/comp/.venv/bin/python -I -B \
  /home/soh/agent-security/experiments/omst_c2_v7_fixture.py \
  --cell full_s0

/usr/bin/env -i \
  LANG=C LC_ALL=C TZ=UTC PYTHONHASHSEED=0 PYTHONNOUSERSITE=1 \
  /home/soh/agent-security/comp/.venv/bin/python -I -B \
  /home/soh/agent-security/experiments/omst_c2_v7_fixture.py \
  --cell full_s1
