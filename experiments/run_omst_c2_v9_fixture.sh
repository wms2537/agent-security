#!/bin/bash
set -euo pipefail

[[ -z "${BASH_ENV-}" ]]
[[ -z "${ENV-}" ]]

PAIR="${1:?usage: run_omst_c2_v9_fixture.sh task|full /absolute/manifest.json}"
MANIFEST_PATH="${2:?usage: run_omst_c2_v9_fixture.sh task|full /absolute/manifest.json}"
[[ "$MANIFEST_PATH" = /* ]]
[[ -f "$MANIFEST_PATH" ]]

run_cell() {
  local cell="$1"
  local run_id="$2"
  /usr/bin/env -i \
    HOME=/nonexistent LANG=C LC_ALL=C TZ=UTC \
    /home/soh/agent-security/comp/.venv/bin/python -I -B \
    /home/soh/agent-security/experiments/omst_c2_v9_fixture.py \
    --manifest "$MANIFEST_PATH" \
    --cell "$cell" \
    --run-id "$run_id"
}

case "$PAIR" in
  task)
    run_cell task_s0 R_task_s0
    run_cell task_s1 R_task_s1
    ;;
  full)
    run_cell full_s0 R_full_s0
    run_cell full_s1 R_full_s1
    ;;
  *)
    exit 64
    ;;
esac
