#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_DIR="."; TARGET="both"; REMOVE_CONFIG=0; DRY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-dir) PROJECT_DIR="${2:-}"; shift 2 ;;
    --project-dir=*) PROJECT_DIR="${1#*=}"; shift ;;
    --target) TARGET="${2:-}"; shift 2 ;;
    --target=*) TARGET="${1#*=}"; shift ;;
    --remove-ai-config) REMOVE_CONFIG=1; shift ;;
    --dry-run) DRY=1; shift ;;
    *) echo "Usage: $0 [--project-dir DIR] [--target both|codex|claude] [--remove-ai-config] [--dry-run]"; exit 2 ;;
  esac
done
PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
ARGS=(--project-dir "$PROJECT_DIR" --target "$TARGET")
[[ "$REMOVE_CONFIG" -eq 1 ]] && ARGS+=(--remove-ai-config)
[[ "$DRY" -eq 1 ]] && ARGS+=(--dry-run)
"$PY" "$ROOT/scripts/uninstall_project.py" "${ARGS[@]}"
