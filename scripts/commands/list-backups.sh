#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT/scripts/backup-lib.sh"
ensure_backup_root
dirs=()
for d in "$BACKUP_ROOT"/*; do
  [[ -d "$d" ]] || continue
  dirs+=("$(basename "$d")")
done
IFS=$'\n' sorted=($(printf '%s\n' "${dirs[@]}" | sort -r)); unset IFS
for name in "${sorted[@]}"; do
  manifest="$BACKUP_ROOT/$name/manifest.json"
  [[ -f "$manifest" ]] || continue
  PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
  "$PY" - "$manifest" "$name" <<'PY'
import json,sys
m=json.load(open(sys.argv[1]))
print(f"{sys.argv[2]}\t{m.get('packVersion','?')}\t{m.get('reason','?')}\t{m.get('createdAt','?')}")
PY
done
