#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIR="${1:-.}"
if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
"$PY" "$ROOT/scripts/profile_manager.py" detect --project-dir "$DIR"
