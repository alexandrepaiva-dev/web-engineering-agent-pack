#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT/scripts/backup-lib.sh"
KEEP=5
[[ "${1:-}" == "--keep" ]] && KEEP="${2:-5}"
ensure_backup_root
dirs=()
for d in "$BACKUP_ROOT"/*; do [[ -d "$d" ]] && dirs+=("$d"); done
IFS=$'\n' sorted=($(printf '%s\n' "${dirs[@]}" | sort -r)); unset IFS
i=0
for d in "${sorted[@]}"; do
  i=$((i+1))
  if [[ "$i" -gt "$KEEP" ]]; then
    echo "remove: $d"
    rm -rf "$d"
  fi
done
