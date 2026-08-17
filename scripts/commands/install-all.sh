#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT/scripts/backup-lib.sh"
source "$ROOT/scripts/profile-lib.sh"
source "$ROOT/scripts/state-lib.sh"

DRY=0
THIRD=0
PROFILE=""
ADD=()
REMOVE=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --with-third-party) THIRD=1; shift ;;
    --profile) PROFILE="${2:-}"; shift 2 ;;
    --profile=*) PROFILE="${1#*=}"; shift ;;
    --add-skill) ADD+=("${2:-}"); shift 2 ;;
    --add-skill=*) ADD+=("${1#*=}"); shift ;;
    --remove-skill) REMOVE+=("${2:-}"); shift 2 ;;
    --remove-skill=*) REMOVE+=("${1#*=}"); shift ;;
    *) echo "Usage: $0 [--profile PROFILE] [--with-third-party] [--add-skill NAME] [--remove-skill NAME] [--dry-run]"; exit 2 ;;
  esac
done

if [[ -z "$PROFILE" ]]; then
  if [[ -t 0 ]]; then PROFILE="$(choose_profile_interactive core)"; else PROFILE="core"; fi
fi

COMMON=(--profile "$PROFILE")
for s in "${ADD[@]}"; do COMMON+=(--add-skill "$s"); done
for s in "${REMOVE[@]}"; do COMMON+=(--remove-skill "$s"); done

if [[ "$DRY" -eq 1 ]]; then
  "$ROOT/scripts/commands/install-codex.sh" "${COMMON[@]}" --dry-run
  echo
  "$ROOT/scripts/commands/install-claude.sh" "${COMMON[@]}" --dry-run
  echo
  [[ "$THIRD" -eq 1 ]] && "$ROOT/scripts/commands/install-third-party-skills.sh" --dry-run || echo "Third-party skills not installed by default."
  exit 0
fi

backup="$(snapshot_state "install-all:$PROFILE")"
backup_name="$(basename "$backup")"
echo "Snapshot created: $backup"

rollback() {
  status=$?
  if [[ "$status" -ne 0 ]]; then
    echo "Installation failed. Restoring snapshot: $backup_name" >&2
    "$ROOT/scripts/commands/restore-backup.sh" "$backup_name" || true
  fi
  exit "$status"
}
trap rollback ERR

"$ROOT/scripts/commands/install-codex.sh" "${COMMON[@]}" --skip-snapshot
"$ROOT/scripts/commands/install-claude.sh" "${COMMON[@]}" --skip-snapshot

if [[ "$THIRD" -eq 1 ]]; then
  "$ROOT/scripts/commands/install-third-party-skills.sh"
fi

STATE_ARGS=()
for s in "${ADD[@]}"; do STATE_ARGS+=(--add-skill "$s"); done
for s in "${REMOVE[@]}"; do STATE_ARGS+=(--remove-skill "$s"); done
STATE_SKILLS=()
while IFS= read -r item; do STATE_SKILLS+=("$item"); done < <(resolve_profile_skills "$ROOT" "$PROFILE" "${STATE_ARGS[@]}")
if [[ "$THIRD" -eq 1 ]]; then STATE_THIRD=true; else STATE_THIRD=false; fi
write_install_state "$PROFILE" "both" "$STATE_THIRD" "${STATE_SKILLS[@]}"

trap - ERR
echo "Codex + Claude Code transactional installation complete. Profile: $PROFILE"
