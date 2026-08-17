# Web Engineering Agent Pack

**Web Engineering Agent Pack (WEAP) v1.0.0** is a multi-stack engineering skill, agent, MCP, and lifecycle toolkit for Codex and Claude Code.

It provides reusable engineering standards without forcing every repository to load every framework, ORM, database, or external tool.

## What WEAP includes

- Stack-agnostic CORE engineering skills
- Next.js / TypeScript / React stack profile
- Symfony / PHP / Doctrine stack profile
- Codex reviewer/explorer agents
- Claude Code reviewer/explorer subagents
- Opt-in MCP registry and MCP profiles
- Unified `weap` CLI
- Transactional global installation and rollback
- Project-local profiles and reproducibility lockfiles
- Backup, restore, uninstall, migration, doctor, and audit tooling
- Linux, macOS, and Windows CI
- Release checksums and GitHub artifact attestations
- Static GitHub Pages documentation/landing site

## Repository name

```text
web-engineering-agent-pack
```

Suggested clone:

```bash
git clone https://github.com/OWNER/web-engineering-agent-pack.git
cd web-engineering-agent-pack
```

---

# 1. Recommended architecture

Use stack-agnostic CORE globally and stack-specific skills locally in each repository.

```text
GLOBAL
└── CORE

PROJECT
├── Next.js profile
│   ├── TypeScript
│   ├── React
│   ├── Tailwind
│   ├── Next.js
│   ├── Node.js
│   ├── Auth.js
│   ├── Prisma
│   ├── PostgreSQL / MySQL
│   └── BullMQ
│
└── Symfony profile
    ├── PHP
    ├── Symfony
    ├── Symfony Security
    ├── Doctrine
    ├── MySQL / PostgreSQL
    └── Twig

MCP
└── Explicit opt-in only
```

This design minimizes trigger noise and unnecessary context.

---

# 2. Requirements

Recommended:

```text
Python 3
Git
Bash on Linux/macOS/WSL
PowerShell on Windows
Node.js when using Node-based external skills or MCP servers
```

Check:

```bash
python3 --version
git --version
node --version
```

Windows:

```powershell
python --version
git --version
node --version
```

---

# 3. Quick installation

Preview:

```bash
./weap install --profile core --dry-run
```

Install CORE for Codex and Claude Code:

```bash
./weap install --profile core
```

Install CORE plus the recommended third-party UI/web-quality skills:

```bash
./weap install \
  --profile core \
  --with-third-party
```

Windows:

```powershell
.\weap.ps1 install --profile core --with-third-party
```

The individual shell/PowerShell scripts remain available for compatibility.

---

# 4. Profiles

List profile definitions:

```bash
python scripts/profile_manager.py list
```

Built-in profiles:

```text
core
nextjs
nextjs-mysql
symfony
symfony-postgresql
full
```

## Next.js repository

```bash
./weap project init \
  --profile nextjs \
  --project-dir=/path/to/repository \
  --yes
```

## Symfony repository

```bash
./weap project init \
  --profile symfony \
  --project-dir=/path/to/repository \
  --yes
```

## Automatic detection

```bash
./weap project init \
  --detect \
  --project-dir=/path/to/repository \
  --yes
```

Detection inspects safe repository metadata such as:

```text
package.json
composer.json
prisma/schema.prisma
config/packages/doctrine.yaml
```

It does not read real secrets from `.env`.

---

# 5. Team mode

For a fully self-contained repository:

```bash
./weap project init \
  --detect \
  --team \
  --project-dir=. \
  --yes
```

Team mode installs CORE + stack-specific skills locally and creates:

```text
.web-engineering-agent-pack.json
.web-engineering-agent-pack.lock.json
```

Commit the lockfile when the repository should reproduce the exact WEAP configuration.

Verify:

```bash
./weap project verify --project-dir=.
```

Apply the locked skill configuration:

```bash
./weap project apply-lock --project-dir=.
```

External MCP capabilities recorded in the lockfile are **not** automatically granted. Install them explicitly.

---

# 6. MCP support

MCP is a separate, opt-in capability layer.

Installing a WEAP skill profile never installs MCP servers automatically.

List registry entries:

```bash
./weap mcp list
```

List MCP profiles:

```bash
./weap mcp profiles
```

Built-in MCP profiles:

```text
docs
browser
development
project-files
development-full
```

## Preview

```bash
./weap mcp plan \
  --profile development \
  --scope project \
  --project-dir=.
```

## Install

```bash
./weap mcp install \
  --profile development \
  --scope project \
  --project-dir=.
```

Target only Codex:

```bash
./weap mcp install \
  --server playwright \
  --scope project \
  --project-dir=. \
  --target codex
```

Target only Claude Code:

```bash
./weap mcp install \
  --server playwright \
  --scope project \
  --project-dir=. \
  --target claude
```

## High-risk MCP capabilities

High/critical risk definitions require explicit acknowledgement:

```bash
./weap mcp install \
  --server filesystem-project \
  --scope project \
  --project-dir=. \
  --allow-high-risk
```

Project-bound filesystem capability cannot be installed at user scope.

## MCP doctor

```bash
./weap mcp doctor \
  --scope project \
  --project-dir=.
```

## Disable / enable / remove

```bash
./weap mcp disable playwright --scope project --project-dir=.
./weap mcp enable playwright --scope project --project-dir=.
./weap mcp remove playwright --scope project --project-dir=.
```

Remove every WEAP-managed MCP server in a scope:

```bash
./weap mcp reset --scope project --project-dir=. --dry-run
./weap mcp reset --scope project --project-dir=. --yes
```

MCP has an independent lifecycle. `weap uninstall` does not silently revoke separately installed MCP capabilities.

## Configuration targets

Codex project:

```text
.codex/config.toml
```

Codex user:

```text
~/.codex/config.toml
```

Claude Code project:

```text
.mcp.json
```

Claude Code user:

```text
~/.claude.json
```

WEAP preserves unrelated configuration and refuses unsafe name ownership conflicts.

See:

```text
docs/MCP.md
docs/MCP-SECURITY.md
```

---

# 7. MCP secrets and permissions

Never place credentials in `mcp/registry/*.json`.

Registry definitions contain environment variable names, not secret values.

Recommended policy:

```text
documentation lookup     low risk
browser automation       medium risk
project filesystem       high risk
production DB write      critical risk
```

Prefer:

- OAuth for remote user-authorized services
- read-only database credentials for analysis
- project-scoped filesystem roots
- explicit tool approval for writes/destructive actions
- separate development/staging/production credentials

WEAP intentionally ships a database **template**, not a default production database server.

---

# 8. Doctor

Global diagnostics:

```bash
./weap doctor
```

Project diagnostics:

```bash
./weap doctor --project-dir=.
```

Machine-readable:

```bash
./weap doctor --project-dir=. --json
```

Doctor checks runtime prerequisites, writable paths, install state, project state, stack detection, and project MCP state when present.

---

# 9. Audit

Run the repository quality gates:

```bash
./weap audit
```

This runs:

```text
pack validation
skill lint
profile lint
documentation consistency
context-budget analysis
package-size analysis
formal JSON Schema validation when jsonschema is installed
```

Standalone commands:

```bash
python scripts/validate-pack.py
python scripts/validate-schemas.py
python scripts/lint-skills.py
python scripts/lint-profiles.py
python scripts/docs-consistency.py
python scripts/analyze-context-budget.py
python scripts/analyze-package-size.py
```

---

# 10. Project update safety

WEAP hashes pack-managed project skills.

If a managed skill was edited locally, update refuses to overwrite it.

Review the local change and move project-specific behavior into a custom skill.

To intentionally replace local modifications:

```bash
./weap project install \
  --profile nextjs \
  --project-dir=. \
  --force
```

Before replacing managed project skills, WEAP creates:

```text
.web-engineering-agent-pack-backups/<timestamp>/
```

List project backups:

```bash
./weap project backup list --project-dir=.
```

Restore:

```bash
./weap project backup restore latest --project-dir=.
```

---

# 11. Global backup and restore

Global installation creates snapshots under:

```text
~/.ai-agent-pack-backups/
```

List:

```bash
./weap backup list
```

Restore latest:

```bash
./weap backup restore latest
```

Backups record the original Codex/Claude paths. Restore uses those recorded paths by default.

Use current machine paths intentionally:

```bash
./weap backup restore latest --current-paths
```

---

# 12. Uninstall

Preview:

```bash
./weap uninstall --dry-run
```

Remove WEAP-managed global state:

```bash
./weap uninstall
```

Keep recommended third-party skills:

```bash
./weap uninstall --keep-third-party
```

Remove and restore the state that existed before installation:

```bash
./weap uninstall --restore-previous
```

Project profile uninstall:

```bash
./weap project uninstall --project-dir=.
```

Also remove AI configuration that WEAP can prove it created:

```bash
./weap project uninstall \
  --project-dir=. \
  --remove-ai-config
```

Unknown/custom skills and agents are preserved.

---

# 13. Migrations

Public v1 is the first stable release.

The repository contains compatibility fixtures for historical internal development builds 7, 8, and 9.

Preview migration:

```bash
./weap migrate --project-dir=.
```

Apply:

```bash
./weap migrate --project-dir=. --apply
```

Global state:

```bash
python scripts/migrate.py --global-state
python scripts/migrate.py --global-state --apply
```

Migration creates a backup before changing an existing manifest/state file.

---

# 14. Self-update

Check stable releases:

```bash
./weap update
```

If repository discovery is unavailable:

```bash
./weap update \
  --repo OWNER/web-engineering-agent-pack
```

Apply:

```bash
./weap update \
  --repo OWNER/web-engineering-agent-pack \
  --apply
```

The updater verifies:

```text
GitHub release metadata
SHA-256 checksum
GitHub artifact attestation (by default)
incoming pack validation
```

GitHub CLI (`gh`) is required for attestation verification.

Only explicitly bypass provenance verification when necessary:

```bash
./weap update --apply --skip-attestation
```

Checksum verification is never skipped.

---

# 15. Releases

WEAP follows Semantic Versioning from public v1 onward.

Preview:

```bash
./weap release \
  --version 1.0.1 \
  --channel stable \
  --dry-run
```

Build:

```bash
./weap release \
  --version 1.0.1 \
  --channel stable
```

Output:

```text
web-engineering-agent-pack-<version>.zip
SHA256SUMS
RELEASE-NOTES-<version>.md
release.json
```

Git tags:

```text
v1.0.0
v1.1.0
v2.0.0
```

Preview versions:

```text
1.1.0-preview.1
1.1.0-rc.1
```

See `docs/VERSIONING.md`.

---

# 16. GitHub Releases and provenance

The release workflow:

```text
.github/workflows/release.yml
```

publishes GitHub releases and generates GitHub artifact provenance attestations for release ZIPs.

Verify a downloaded ZIP:

```bash
sha256sum -c SHA256SUMS
```

and:

```bash
gh attestation verify \
  web-engineering-agent-pack-1.0.0.zip \
  -R OWNER/web-engineering-agent-pack
```

See `docs/RELEASE-VERIFICATION.md`.

---

# 17. GitHub Pages

The public site source is:

```text
site/
```

Build locally:

```bash
python scripts/build-site.py
```

Output:

```text
_site/
```

One-time GitHub setup:

```text
Repository → Settings → Pages → Source → GitHub Actions
```

The included workflow:

```text
.github/workflows/pages.yml
```

then publishes changes from `main`.

See `docs/GITHUB-PAGES.md`.

---

# 18. CI

CI runs on:

```text
Ubuntu
macOS
Windows
```

It validates pack structure, schemas, skills, profiles, documentation, migration compatibility, security regressions, installers, lifecycle operations, release packaging, and the public site.

---

# 19. Third-party skills

WEAP supports:

```text
ui-ux-pro-max
web-quality-audit
```

Their reviewed Git commits are recorded in:

```text
third-party.lock.json
```

Preview:

```bash
./scripts/commands/install-third-party-skills.sh --dry-run
```

Install:

```bash
./scripts/commands/install-third-party-skills.sh
```

Check upstream:

```bash
python scripts/update-third-party-lock.py
```

See [the third-party skills guide](docs/THIRD-PARTY-SKILLS.md).

---

# 20. Adding a stack

The architecture is profile-based.

A future Laravel integration would normally require:

```text
shared/skills/laravel-engineering/
profiles/laravel.json
tests
documentation
```

Installer architecture does not need to be rewritten.

---

# 21. Adding an MCP server

Create:

```text
mcp/registry/my-server.json
```

Validate against:

```text
schemas/mcp-server.schema.json
```

Do not include credentials.

For a reusable group, create:

```text
mcp/profiles/my-profile.json
```

Then:

```bash
./weap mcp plan --profile my-profile --scope project --project-dir=.
```

High/critical risk servers remain opt-in.

---

# 22. Repository development

Before a pull request:

```bash
python scripts/validate-pack.py
python scripts/validate-schemas.py
python scripts/lint-skills.py
python scripts/lint-profiles.py
python scripts/docs-consistency.py
python -m unittest discover -s tests -p "test_*.py"
bash tests/run-shell-tests.sh
```

On Windows:

```powershell
.\tests\run-powershell-tests.ps1
```

See:

```text
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
```

---

# 23. Documentation

```text
docs/AI-AGENTS-SETUP.md
docs/BACKUP-RESTORE.md
docs/COMPATIBILITY.md
docs/GITHUB-PAGES.md
docs/MCP.md
docs/MCP-SECURITY.md
docs/PROFILE-CATALOG.md
docs/RELEASE-VERIFICATION.md
docs/REPOSITORY.md
docs/THIRD-PARTY-SKILLS.md
docs/TOKEN-EFFICIENCY.md
docs/VERSIONING.md
docs/QUICKSTART.md
```

---

# 24. License

MIT. See `LICENSE`.
