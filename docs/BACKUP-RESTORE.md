# Backup, clean install and restore

Version 8 uses a clean-install model for the directories managed by the pack.

## Managed state

Codex:
- `~/.codex/AGENTS.md`
- `~/.codex/agents/`
- `~/.agents/skills/`

Claude Code:
- `~/.claude/CLAUDE.md`
- `~/.claude/agents/`
- `~/.claude/skills/`

## Preserved state

The installer does not replace the complete `~/.codex` or `~/.claude` directories.

Examples preserved:
- `~/.codex/config.toml`
- MCP/provider/model configuration
- `~/.claude/settings.json`
- `~/.claude/settings.local.json`
- unrelated configuration

## Snapshot

Before a normal install:

```text
~/.ai-agent-pack-backups/<timestamp>/
├── manifest.json
├── codex/
│   ├── AGENTS.md
│   ├── agents/
│   └── skills/
└── claude/
    ├── CLAUDE.md
    ├── agents/
    └── skills/
```

Only items that existed are stored.

Then the managed skill/agent directories are removed and recreated from the current pack. This prevents stale skills and agents from previous versions.

## Third-party skills

Because the skills directories are recreated, third-party skills are intentionally removed by a clean install.

Reinstall them afterward:

```bash
./scripts/commands/install-third-party-skills.sh
```

Or install first-party + recommended third-party skills in one operation:

```bash
./scripts/commands/install-all.sh --with-third-party
```

## Restore

```bash
./scripts/commands/list-backups.sh
./scripts/commands/restore-backup.sh latest
./scripts/commands/restore-backup.sh <backup-name>
```

A restore snapshots the current managed state first, so a restore can itself be undone.

## Cleanup

```bash
./scripts/commands/cleanup-backups.sh --keep 5
```

Windows equivalents are provided as `.ps1` files.

## Dry run

```bash
./scripts/commands/install-all.sh --dry-run
```

This shows managed paths and preserved configuration without changing files.


## Uninstall snapshots

Global uninstall creates a `pre-uninstall` snapshot before removing pack-managed items.

The default uninstall removes known first-party skills and the two recommended external skills, while preserving unknown custom skills/agents.

Use:

```bash
./scripts/commands/uninstall.sh --keep-third-party
```

to preserve `ui-ux-pro-max` and `web-quality-audit`.

Use:

```bash
./scripts/commands/uninstall.sh --restore-previous
```

to remove the current pack and restore the newest prior install snapshot.

The restore operation creates another safety snapshot before applying the historical state.


When a v8 install-state manifest exists, snapshots preserve it and restore it together with the managed skills/agents. This keeps future update/uninstall behavior consistent after restoring an older v8 snapshot.


## Recorded restore paths

Version 9 restores to the Codex/Claude paths stored in the backup manifest by default.

```bash
./scripts/commands/restore-backup.sh latest
```

Use current environment paths only when that is intentional:

```bash
./scripts/commands/restore-backup.sh latest --current-paths
```

## Project skill backups

Before replacing previously pack-managed project skills, the profile installer stores them in:

```text
.web-engineering-agent-pack-backups/<timestamp>/
```

List:

```bash
./scripts/commands/list-project-backups.sh /path/to/project
```

Restore:

```bash
./scripts/commands/restore-project-backup.sh latest /path/to/project
```

Local modifications to pack-managed skills are detected by SHA-256 and block overwrite unless `--force` is supplied.
