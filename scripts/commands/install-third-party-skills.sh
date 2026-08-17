#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
command -v git >/dev/null 2>&1 || { echo "git is required."; exit 1; }
exec "$PY" "$ROOT/scripts/install_locked_third_party.py" "$@"
