PACK_VERSION="1.0.0"
BACKUP_ROOT="${AI_AGENT_PACK_BACKUP_ROOT:-$HOME/.ai-agent-pack-backups}"
PY="${PY:-python3}"
command -v "$PY" >/dev/null 2>&1 || PY=python

timestamp_now() { date +"%Y%m%d-%H%M%S"; }
ensure_backup_root() { mkdir -p "$BACKUP_ROOT"; }

copy_if_exists() {
  local src="$1" dst="$2"
  if [[ -e "$src" ]]; then
    mkdir -p "$(dirname "$dst")"
    cp -a "$src" "$dst"
    return 0
  fi
  return 1
}

snapshot_state() {
  local reason="${1:-install}"
  local codex_home="${CODEX_HOME:-$HOME/.codex}"
  local claude_home="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
  local codex_skills="$HOME/.agents/skills"
  local state_file="${AI_AGENT_PACK_STATE_FILE:-$HOME/.ai-agent-pack-state.json}"

  ensure_backup_root
  local stamp dest suffix
  stamp="$(timestamp_now)"
  dest="$BACKUP_ROOT/$stamp"
  suffix=0
  while [[ -e "$dest" ]]; do
    suffix=$((suffix+1))
    dest="$BACKUP_ROOT/${stamp}-$suffix"
  done
  mkdir -p "$dest"

  local ca=false cag=false cs=false cm=false clag=false cls=false istate=false
  copy_if_exists "$codex_home/AGENTS.md" "$dest/codex/AGENTS.md" && ca=true || true
  copy_if_exists "$codex_home/agents" "$dest/codex/agents" && cag=true || true
  copy_if_exists "$codex_skills" "$dest/codex/skills" && cs=true || true
  copy_if_exists "$claude_home/CLAUDE.md" "$dest/claude/CLAUDE.md" && cm=true || true
  copy_if_exists "$claude_home/agents" "$dest/claude/agents" && clag=true || true
  copy_if_exists "$claude_home/skills" "$dest/claude/skills" && cls=true || true
  copy_if_exists "$state_file" "$dest/state/install-state.json" && istate=true || true

  cat > "$dest/manifest.json" <<EOF
{
  "schemaVersion": 1,
  "packVersion": "$PACK_VERSION",
    "createdAt": "$("$PY" - <<'PY'
from datetime import datetime,timezone
print(datetime.now(timezone.utc).isoformat())
PY
)",
  "reason": "$reason",
  "codexHome": "$codex_home",
  "claudeHome": "$claude_home",
  "codexSkillsHome": "$codex_skills",
  "items": {
    "codexAgentsMd": $ca,
    "codexAgents": $cag,
    "codexSkills": $cs,
    "claudeMd": $cm,
    "claudeAgents": $clag,
    "claudeSkills": $cls,
    "installState": $istate
  }
}
EOF
  echo "$dest"
}

latest_backup() {
  ensure_backup_root
  for d in "$BACKUP_ROOT"/*; do [[ -d "$d" ]] && basename "$d"; done 2>/dev/null | sort | tail -n 1
}
