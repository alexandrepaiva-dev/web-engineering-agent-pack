#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

PROFILE=""
PROJECT_DIR="."
TARGET="both"
INCLUDE_CORE=0
INIT_PROJECT=0
DRY=0
FORCE=0
EXTRA=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="${2:-}"; shift 2 ;;
    --profile=*) PROFILE="${1#*=}"; shift ;;
    --project-dir) PROJECT_DIR="${2:-}"; shift 2 ;;
    --project-dir=*) PROJECT_DIR="${1#*=}"; shift ;;
    --target) TARGET="${2:-}"; shift 2 ;;
    --target=*) TARGET="${1#*=}"; shift ;;
    --include-core) INCLUDE_CORE=1; shift ;;
    --init-project) INIT_PROJECT=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --force) FORCE=1; shift ;;
    --add-skill|--remove-skill)
      EXTRA+=("$1=${2:-}"); shift 2 ;;
    --add-skill=*|--remove-skill=*) EXTRA+=("$1"); shift ;;
    *) echo "Unknown argument: $1"; exit 2 ;;
  esac
done

if [[ -z "$PROFILE" ]]; then
  if [[ -t 0 ]]; then
    echo "Select project stack profile:"
    echo "1) nextjs"
    echo "2) symfony"
    echo "3) nextjs-mysql"
    echo "4) symfony-postgresql"
    echo "5) full"
    read -r -p "Choice [1]: " choice
    case "${choice:-1}" in
      1) PROFILE="nextjs" ;;
      2) PROFILE="symfony" ;;
      3) PROFILE="nextjs-mysql" ;;
      4) PROFILE="symfony-postgresql" ;;
      5) PROFILE="full" ;;
      *) echo "Invalid choice"; exit 2 ;;
    esac
  else
    echo "--profile is required in non-interactive mode."
    exit 2
  fi
fi

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
ARGS=(install-project --profile "$PROFILE" --project-dir "$PROJECT_DIR" --target "$TARGET")
[[ "$INCLUDE_CORE" -eq 1 ]] && ARGS+=(--include-core)
[[ "$INIT_PROJECT" -eq 1 ]] && ARGS+=(--init-project)
[[ "$DRY" -eq 1 ]] && ARGS+=(--dry-run)
[[ "$FORCE" -eq 1 ]] && ARGS+=(--force)
for e in "${EXTRA[@]}"; do
  key="${e%%=*}"; val="${e#*=}"
  ARGS+=("$key" "$val")
done

exec "$PY" "$ROOT/scripts/profile_manager.py" "${ARGS[@]}"
