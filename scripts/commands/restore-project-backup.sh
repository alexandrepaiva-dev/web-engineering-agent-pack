#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP="${1:-latest}"
PROJECT="${2:-.}"
PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
exec "$PY" "$ROOT/scripts/project_backup.py" restore "$BACKUP" --project-dir "$PROJECT"
