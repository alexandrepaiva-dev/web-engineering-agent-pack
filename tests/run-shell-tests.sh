#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for script in \
  scripts/commands/install-all.sh scripts/commands/install-codex.sh scripts/commands/install-claude.sh scripts/commands/install-project.sh \
  scripts/commands/uninstall.sh scripts/commands/uninstall-project.sh scripts/commands/restore-backup.sh scripts/commands/list-backups.sh \
  scripts/commands/cleanup-backups.sh scripts/commands/install-third-party-skills.sh \
  scripts/backup-lib.sh scripts/profile-lib.sh scripts/state-lib.sh \
  scripts/transaction-lib.sh
do
  bash -n "$ROOT/$script"
done

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
export HOME="$tmp/home"
export AI_AGENT_PACK_BACKUP_ROOT="$HOME/.ai-agent-pack-backups"
export AI_AGENT_PACK_STATE_FILE="$HOME/.ai-agent-pack-state.json"
mkdir -p "$HOME/.codex" "$HOME/.claude"
echo 'keep=true' > "$HOME/.codex/config.toml"
echo '{"keep":true}' > "$HOME/.claude/settings.json"

"$ROOT/scripts/commands/install-all.sh" --profile core
test -f "$HOME/.codex/AGENTS.md"
test -f "$HOME/.claude/CLAUDE.md"
test -d "$HOME/.agents/skills/backend-engineering"
test "$(cat "$HOME/.codex/config.toml")" = "keep=true"

mkdir -p "$HOME/.agents/skills/custom-test" "$HOME/.claude/skills/custom-test"
echo custom > "$HOME/.agents/skills/custom-test/value"
echo custom > "$HOME/.claude/skills/custom-test/value"

"$ROOT/scripts/commands/uninstall.sh" --keep-third-party
test ! -f "$HOME/.codex/AGENTS.md"
test -d "$HOME/.agents/skills/custom-test"
test -d "$HOME/.claude/skills/custom-test"
test "$(cat "$HOME/.codex/config.toml")" = "keep=true"



# Transaction rollback: force Claude staging failure after Codex has installed.
rollback_home="$tmp/rollback-home"
repo_copy="$tmp/broken-repo"
cp -a "$ROOT" "$repo_copy"
rm -f "$repo_copy/claude/global/.claude/CLAUDE.md"
mkdir -p "$rollback_home/.codex" "$rollback_home/.claude"
echo OLD_CODEX > "$rollback_home/.codex/AGENTS.md"
echo OLD_CLAUDE > "$rollback_home/.claude/CLAUDE.md"
old_home="$HOME"
HOME="$rollback_home"
export HOME
export AI_AGENT_PACK_BACKUP_ROOT="$HOME/.ai-agent-pack-backups"
export AI_AGENT_PACK_STATE_FILE="$HOME/.ai-agent-pack-state.json"
if "$repo_copy/scripts/commands/install-all.sh" --profile core; then
  echo "Expected broken install to fail" >&2
  exit 1
fi
grep -q OLD_CODEX "$HOME/.codex/AGENTS.md"
grep -q OLD_CLAUDE "$HOME/.claude/CLAUDE.md"




# Restore defaults to paths recorded in the backup manifest.
recorded_home="$tmp/recorded-home"
custom_codex="$tmp/custom-codex"
custom_claude="$tmp/custom-claude"
mkdir -p "$recorded_home" "$custom_codex" "$custom_claude"
echo PRE_CODEX > "$custom_codex/AGENTS.md"
echo PRE_CLAUDE > "$custom_claude/CLAUDE.md"

export HOME="$recorded_home"
export CODEX_HOME="$custom_codex"
export CLAUDE_CONFIG_DIR="$custom_claude"
export AI_AGENT_PACK_BACKUP_ROOT="$recorded_home/.ai-agent-pack-backups"
export AI_AGENT_PACK_STATE_FILE="$recorded_home/.ai-agent-pack-state.json"

"$ROOT/scripts/commands/install-all.sh" --profile core
first_backup="$(for d in "$AI_AGENT_PACK_BACKUP_ROOT"/*; do [[ -d "$d" ]] && basename "$d"; done | sort | head -n 1)"
unset CODEX_HOME CLAUDE_CONFIG_DIR
"$ROOT/scripts/commands/restore-backup.sh" "$first_backup"
grep -q PRE_CODEX "$custom_codex/AGENTS.md"
grep -q PRE_CLAUDE "$custom_claude/CLAUDE.md"



# Security: restore path traversal must be rejected.
if "$ROOT/scripts/commands/restore-backup.sh" "../../outside"; then
  echo "restore path traversal was not rejected" >&2
  exit 1
fi

echo "Shell lifecycle tests OK."
