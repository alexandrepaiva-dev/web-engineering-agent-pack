#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT/scripts/backup-lib.sh"

TARGET=""
CURRENT_PATHS=0
for arg in "$@"; do
  case "$arg" in
    --current-paths) CURRENT_PATHS=1 ;;
    latest|*) [[ -z "$TARGET" ]] && TARGET="$arg" || { echo "Usage: $0 latest|<backup-name> [--current-paths]"; exit 2; } ;;
  esac
done

[[ -n "$TARGET" ]] || { echo "Usage: $0 latest|<backup-name> [--current-paths]"; exit 2; }
if [[ "$TARGET" == "latest" ]]; then
  TARGET="$(latest_backup)"
  [[ -n "$TARGET" ]] || { echo "No backups found."; exit 1; }
else
  [[ "$TARGET" =~ ^[0-9]{8}-[0-9]{6}(-[0-9]+)?$ ]] || { echo "Invalid backup name: $TARGET"; exit 2; }
fi

SRC="$BACKUP_ROOT/$TARGET"
MANIFEST="$SRC/manifest.json"
[[ -f "$MANIFEST" ]] || { echo "Invalid backup: $SRC"; exit 1; }

current="$(snapshot_state "pre-restore-$TARGET")"
echo "Current managed state snapshotted: $current"

if [[ "$CURRENT_PATHS" -eq 1 ]]; then
  CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
  CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  CODEX_SKILLS="$HOME/.agents/skills"
else
  PY=python3; command -v python3 >/dev/null 2>&1 || PY=python
  recorded_file="${TMPDIR:-/tmp}/weap-restore-paths-$$"
  "$PY" - "$MANIFEST" > "$recorded_file" <<'PY'
import json,sys
m=json.load(open(sys.argv[1]))
print(m.get("codexHome",""))
print(m.get("claudeHome",""))
print(m.get("codexSkillsHome",""))
PY
  RECORDED=()
  while IFS= read -r item; do RECORDED+=("$item"); done < "$recorded_file"
  rm -f "$recorded_file"
  CODEX_HOME="${RECORDED[0]:-${CODEX_HOME:-$HOME/.codex}}"
  CLAUDE_HOME="${RECORDED[1]:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}}"
  CODEX_SKILLS="${RECORDED[2]:-$HOME/.agents/skills}"
fi

STATE_FILE="${AI_AGENT_PACK_STATE_FILE:-$HOME/.ai-agent-pack-state.json}"
mkdir -p "$CODEX_HOME" "$CLAUDE_HOME" "$(dirname "$CODEX_SKILLS")"

rm -f "$CODEX_HOME/AGENTS.md" "$CLAUDE_HOME/CLAUDE.md" "$STATE_FILE"
rm -rf "$CODEX_HOME/agents" "$CODEX_SKILLS" "$CLAUDE_HOME/agents" "$CLAUDE_HOME/skills"

[[ -f "$SRC/codex/AGENTS.md" ]] && cp -a "$SRC/codex/AGENTS.md" "$CODEX_HOME/AGENTS.md"
[[ -d "$SRC/codex/agents" ]] && cp -a "$SRC/codex/agents" "$CODEX_HOME/agents"
[[ -d "$SRC/codex/skills" ]] && cp -a "$SRC/codex/skills" "$CODEX_SKILLS"
[[ -f "$SRC/claude/CLAUDE.md" ]] && cp -a "$SRC/claude/CLAUDE.md" "$CLAUDE_HOME/CLAUDE.md"
[[ -d "$SRC/claude/agents" ]] && cp -a "$SRC/claude/agents" "$CLAUDE_HOME/agents"
[[ -d "$SRC/claude/skills" ]] && cp -a "$SRC/claude/skills" "$CLAUDE_HOME/skills"
[[ -f "$SRC/state/install-state.json" ]] && cp -a "$SRC/state/install-state.json" "$STATE_FILE"

echo "Restore complete: $TARGET"
echo "Codex path: $CODEX_HOME"
echo "Claude path: $CLAUDE_HOME"
