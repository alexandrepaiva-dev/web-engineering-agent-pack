#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT/scripts/backup-lib.sh"
source "$ROOT/scripts/profile-lib.sh"
source "$ROOT/scripts/state-lib.sh"
source "$ROOT/scripts/transaction-lib.sh"

DRY=0
SKIP=0
PROFILE=""
ADD=()
REMOVE=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --skip-snapshot) SKIP=1; shift ;;
    --profile) PROFILE="${2:-}"; shift 2 ;;
    --profile=*) PROFILE="${1#*=}"; shift ;;
    --add-skill) ADD+=("${2:-}"); shift 2 ;;
    --add-skill=*) ADD+=("${1#*=}"); shift ;;
    --remove-skill) REMOVE+=("${2:-}"); shift 2 ;;
    --remove-skill=*) REMOVE+=("${1#*=}"); shift ;;
    *) echo "Usage: $0 [--profile PROFILE] [--add-skill NAME] [--remove-skill NAME] [--dry-run] [--skip-snapshot]"; exit 2 ;;
  esac
done

if [[ -z "$PROFILE" ]]; then
  if [[ -t 0 ]]; then PROFILE="$(choose_profile_interactive core)"; else PROFILE="core"; fi
fi

RESOLVE_ARGS=()
for s in "${ADD[@]}"; do RESOLVE_ARGS+=(--add-skill "$s"); done
for s in "${REMOVE[@]}"; do RESOLVE_ARGS+=(--remove-skill "$s"); done
SKILLS=()
while IFS= read -r item; do SKILLS+=("$item"); done < <(resolve_profile_skills "$ROOT" "$PROFILE" "${RESOLVE_ARGS[@]}")

CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SKILLS_HOME="$CLAUDE_HOME/skills"

if [[ "$DRY" -eq 1 ]]; then
  echo "Claude Code transactional install preview"
  echo "Profile: $PROFILE"
  echo "Skills (${#SKILLS[@]}): ${SKILLS[*]}"
  echo "Will build and validate staging directories before swapping targets."
  echo "Snapshot: $CLAUDE_HOME/CLAUDE.md, $CLAUDE_HOME/agents/, $SKILLS_HOME/"
  echo "Preserve: settings.json, settings.local.json and unrelated Claude files"
  exit 0
fi

backup=""
if [[ "$SKIP" -eq 0 ]]; then
  backup="$(snapshot_state "claude-install:$PROFILE")"
  echo "Snapshot created: $backup"
fi

mkdir -p "$CLAUDE_HOME"

stage_skills="$CLAUDE_HOME/.weap-skills-stage-$$"
stage_agents="$CLAUDE_HOME/.weap-agents-stage-$$"
stage_claude_md="$CLAUDE_HOME/.weap-CLAUDE-stage-$$"

cleanup_stage() {
  rm -rf "$stage_skills" "$stage_agents"
  rm -f "$stage_claude_md"
}
trap cleanup_stage EXIT

mkdir -p "$stage_skills" "$stage_agents"
cp "$ROOT/claude/global/.claude/CLAUDE.md" "$stage_claude_md"
cp -a "$ROOT/claude/global/.claude/agents/." "$stage_agents/"
for skill in "${SKILLS[@]}"; do
  cp -a "$ROOT/shared/skills/$skill" "$stage_skills/$skill"
done

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
"$PY" "$ROOT/scripts/install-claude-skill-overlays.py" "$stage_skills"

validate_skill_stage "$stage_skills" "${#SKILLS[@]}"
[[ -s "$stage_claude_md" ]] || { echo "Staged CLAUDE.md is empty" >&2; exit 1; }

transactional_replace_dir "$stage_agents" "$CLAUDE_HOME/agents"
transactional_replace_dir "$stage_skills" "$SKILLS_HOME"
transactional_replace_file "$stage_claude_md" "$CLAUDE_HOME/CLAUDE.md"

write_install_state "$PROFILE" "claude" false "${SKILLS[@]}"
trap - EXIT
cleanup_stage

echo "Claude Code transactional install complete. Profile: $PROFILE"
echo "Installed skills: ${#SKILLS[@]}"
