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
for s in "${ADD[@]-}"; do RESOLVE_ARGS+=(--add-skill "$s"); done
for s in "${REMOVE[@]-}"; do RESOLVE_ARGS+=(--remove-skill "$s"); done
SKILLS=()
while IFS= read -r item; do SKILLS+=("$item"); done < <(resolve_profile_skills "$ROOT" "$PROFILE" "${RESOLVE_ARGS[@]}")

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_HOME="$HOME/.agents/skills"
SKILLS_PARENT="$(dirname "$SKILLS_HOME")"

if [[ "$DRY" -eq 1 ]]; then
  echo "Codex transactional install preview"
  echo "Profile: $PROFILE"
  echo "Skills (${#SKILLS[@]}): ${SKILLS[*]}"
  echo "Will build and validate staging directories before swapping targets."
  echo "Snapshot: $CODEX_HOME/AGENTS.md, $CODEX_HOME/agents/, $SKILLS_HOME/"
  echo "Preserve: $CODEX_HOME/config.toml and unrelated Codex files"
  exit 0
fi

backup=""
if [[ "$SKIP" -eq 0 ]]; then
  backup="$(snapshot_state "codex-install:$PROFILE")"
  echo "Snapshot created: $backup"
fi

mkdir -p "$CODEX_HOME" "$SKILLS_PARENT"

stage_skills="$SKILLS_PARENT/.weap-skills-stage-$$"
stage_agents="$CODEX_HOME/.weap-agents-stage-$$"
# Do not differ from the agent-directory staging path only by letter case:
# default macOS filesystems are case-insensitive.
stage_agents_md="$CODEX_HOME/.weap-codex-instructions-stage-$$"

cleanup_stage() {
  rm -rf "$stage_skills" "$stage_agents"
  rm -f "$stage_agents_md"
}
trap cleanup_stage EXIT

mkdir -p "$stage_skills" "$stage_agents"
cp "$ROOT/codex/global/.codex/AGENTS.md" "$stage_agents_md"
cp -a "$ROOT/codex/global/.codex/agents/." "$stage_agents/"
for skill in "${SKILLS[@]}"; do
  cp -a "$ROOT/shared/skills/$skill" "$stage_skills/$skill"
done

validate_skill_stage "$stage_skills" "${#SKILLS[@]}"
[[ -s "$stage_agents_md" ]] || { echo "Staged AGENTS.md is empty" >&2; exit 1; }

transactional_replace_dir "$stage_agents" "$CODEX_HOME/agents"
transactional_replace_dir "$stage_skills" "$SKILLS_HOME"
transactional_replace_file "$stage_agents_md" "$CODEX_HOME/AGENTS.md"

write_install_state "$PROFILE" "codex" false "${SKILLS[@]}"
trap - EXIT
cleanup_stage

echo "Codex transactional install complete. Profile: $PROFILE"
echo "Installed skills: ${#SKILLS[@]}"
