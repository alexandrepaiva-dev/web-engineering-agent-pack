#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT/scripts/backup-lib.sh"
source "$ROOT/scripts/state-lib.sh"

DRY=0
KEEP_THIRD=0
RESTORE_PREVIOUS=0
FORCE_LEGACY=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --keep-third-party) KEEP_THIRD=1 ;;
    --restore-previous) RESTORE_PREVIOUS=1 ;;
    --force-legacy) FORCE_LEGACY=1 ;;
    *) echo "Usage: $0 [--dry-run] [--keep-third-party] [--restore-previous] [--force-legacy]"; exit 2 ;;
  esac
done

if [[ ! -f "$STATE_FILE" && "$FORCE_LEGACY" -eq 0 ]]; then
  echo "No v8 install-state file found: $STATE_FILE"
  echo "Refusing automatic global uninstall to avoid deleting unrelated configuration."
  echo "If this is a v7-or-earlier installation, use --force-legacy after reviewing --dry-run."
  exit 1
fi

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
CODEX_SKILLS="$HOME/.agents/skills"
CLAUDE_SKILLS="$CLAUDE_HOME/skills"

FIRST_PARTY=()
for d in "$ROOT/shared/skills"/*; do [[ -d "$d" ]] && FIRST_PARTY+=("$(basename "$d")"); done
IFS=$'\n' FIRST_PARTY=($(printf '%s\n' "${FIRST_PARTY[@]}" | sort)); unset IFS
CODEX_AGENTS=()
for f in "$ROOT/codex/global/.codex/agents"/*.toml; do [[ -f "$f" ]] && CODEX_AGENTS+=("$(basename "$f")"); done
CLAUDE_AGENTS=()
for f in "$ROOT/claude/global/.claude/agents"/*.md; do [[ -f "$f" ]] && CLAUDE_AGENTS+=("$(basename "$f")"); done
THIRD_PARTY=("ui-ux-pro-max" "web-quality-audit")

TARGET="both"
if [[ -f "$STATE_FILE" ]]; then
  py=python3; command -v python3 >/dev/null 2>&1 || py=python
  TARGET="$("$py" - "$STATE_FILE" <<'PY'
import json,sys
try: print(json.load(open(sys.argv[1])).get("target","both"))
except Exception: print("both")
PY
)"
fi

remove_codex=0; remove_claude=0
case "$TARGET" in
  codex) remove_codex=1 ;;
  claude) remove_claude=1 ;;
  both|*) remove_codex=1; remove_claude=1 ;;
esac

if [[ "$DRY" -eq 1 ]]; then
  echo "Global uninstall preview"
  echo "Detected install target: $TARGET"
  echo "Will snapshot current managed state first."
  if [[ "$remove_codex" -eq 1 ]]; then
    echo "Codex: remove pack AGENTS.md, ${#CODEX_AGENTS[@]} known pack agents, and known first-party skill names."
  fi
  if [[ "$remove_claude" -eq 1 ]]; then
    echo "Claude: remove pack CLAUDE.md, ${#CLAUDE_AGENTS[@]} known pack agents, and known first-party skill names."
  fi
  [[ "$KEEP_THIRD" -eq 1 ]] && echo "Recommended third-party skills are preserved." || echo "Recommended third-party skills are also removed."
  echo "Unknown/custom skills and unknown/custom agents are preserved."
  echo "config.toml, settings.json, settings.local.json, MCP/provider config, and unrelated files are preserved."
  [[ "$RESTORE_PREVIOUS" -eq 1 ]] && echo "Newest prior install snapshot will be restored afterward."
  exit 0
fi

current="$(snapshot_state "pre-uninstall")"
echo "Current managed state snapshotted: $current"

if [[ "$remove_codex" -eq 1 ]]; then
  rm -f "$CODEX_HOME/AGENTS.md"
  for agent in "${CODEX_AGENTS[@]}"; do rm -f "$CODEX_HOME/agents/$agent"; done
  for skill in "${FIRST_PARTY[@]}"; do rm -rf "$CODEX_SKILLS/$skill"; done
  if [[ "$KEEP_THIRD" -eq 0 ]]; then
    for skill in "${THIRD_PARTY[@]}"; do rm -rf "$CODEX_SKILLS/$skill"; done
  fi
fi

if [[ "$remove_claude" -eq 1 ]]; then
  rm -f "$CLAUDE_HOME/CLAUDE.md"
  for agent in "${CLAUDE_AGENTS[@]}"; do rm -f "$CLAUDE_HOME/agents/$agent"; done
  for skill in "${FIRST_PARTY[@]}"; do rm -rf "$CLAUDE_SKILLS/$skill"; done
  if [[ "$KEEP_THIRD" -eq 0 ]]; then
    for skill in "${THIRD_PARTY[@]}"; do rm -rf "$CLAUDE_SKILLS/$skill"; done
  fi
fi

rm -f "$STATE_FILE"
echo "Global pack-managed installation removed."

if [[ "$RESTORE_PREVIOUS" -eq 1 ]]; then
  candidate=""
  while IFS= read -r dir; do
    [[ "$dir" == "$current" ]] && continue
    manifest="$dir/manifest.json"; [[ -f "$manifest" ]] || continue
    py=python3; command -v python3 >/dev/null 2>&1 || py=python
    reason="$("$py" - "$manifest" <<'PY'
import json,sys
try: print(json.load(open(sys.argv[1])).get("reason",""))
except Exception: print("")
PY
)"
    case "$reason" in install-all*|codex-install*|claude-install*) candidate="$dir"; break ;; esac
  done < <(for dir in "$BACKUP_ROOT"/*; do [[ -d "$dir" ]] && printf '%s\n' "$dir"; done | sort -r)
  [[ -n "$candidate" ]] || { echo "No prior install snapshot found."; exit 1; }
  "$ROOT/scripts/commands/restore-backup.sh" "$(basename "$candidate")"
fi
