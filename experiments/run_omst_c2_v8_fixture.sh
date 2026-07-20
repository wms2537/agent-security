#!/bin/bash
set -euo pipefail

[[ -z "${BASH_ENV-}" ]]
[[ -z "${ENV-}" ]]

/usr/bin/env -i \
  HOME=/nonexistent LANG=C LC_ALL=C TZ=UTC \
  /home/soh/agent-security/comp/.venv/bin/python -I -B \
  /home/soh/agent-security/experiments/omst_c2_v8_fixture.py \
  --cell task_s0

/usr/bin/env -i \
  HOME=/nonexistent LANG=C LC_ALL=C TZ=UTC \
  /home/soh/agent-security/comp/.venv/bin/python -I -B \
  /home/soh/agent-security/experiments/omst_c2_v8_fixture.py \
  --cell task_s1

/usr/bin/env -i \
  HOME=/nonexistent LANG=C LC_ALL=C TZ=UTC \
  /home/soh/agent-security/comp/.venv/bin/python -I -B \
  /home/soh/agent-security/experiments/omst_c2_v8_fixture.py \
  --cell full_s0

/usr/bin/env -i \
  HOME=/nonexistent LANG=C LC_ALL=C TZ=UTC \
  /home/soh/agent-security/comp/.venv/bin/python -I -B \
  /home/soh/agent-security/experiments/omst_c2_v8_fixture.py \
  --cell full_s1
