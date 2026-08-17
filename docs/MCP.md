# MCP Integration

WEAP treats Model Context Protocol capabilities as a separate, opt-in layer.

Skills describe how an agent should work. MCP servers give an agent external capabilities. Installing a skill profile never installs MCP servers automatically.

## Supported clients

- Codex
- Claude Code

## Supported transports

- stdio
- Streamable HTTP

## Registry

Canonical definitions live in:

```text
mcp/registry/
```

Profiles live in:

```text
mcp/profiles/
```

List servers:

```bash
./weap mcp list
```

List MCP profiles:

```bash
./weap mcp profiles
```

## Plan before install

```bash
./weap mcp plan \
  --profile development \
  --scope project \
  --project-dir=.
```

No configuration is changed.

## Install

```bash
./weap mcp install \
  --profile development \
  --scope project \
  --project-dir=.
```

Target only one client:

```bash
./weap mcp install \
  --server playwright \
  --scope project \
  --project-dir=. \
  --target codex
```

## High-risk capabilities

High and critical risk definitions require explicit acknowledgement:

```bash
./weap mcp install \
  --server filesystem-project \
  --scope project \
  --project-dir=. \
  --allow-high-risk
```

WEAP intentionally refuses to install project-bound filesystem access at user scope.

## Disable / enable

```bash
./weap mcp disable playwright --scope project --project-dir=.
./weap mcp enable playwright --scope project --project-dir=.
```

## Remove

```bash
./weap mcp remove playwright --scope project --project-dir=.
```

## Doctor

```bash
./weap mcp doctor --scope project --project-dir=.
```

The doctor checks registry hashes, required commands, required environment variables, and risk warnings.

## Codex adapter

Project MCP definitions are written into the WEAP-managed block in:

```text
.codex/config.toml
```

User-scoped definitions are written into:

```text
~/.codex/config.toml
```

WEAP preserves configuration outside its marked block.

## Claude Code adapter

Project MCP definitions are merged into:

```text
.mcp.json
```

User-scoped definitions are merged into:

```text
~/.claude.json
```

WEAP preserves unrelated MCP servers and unrelated JSON properties.

## Secrets

Registry files never contain credentials.

Definitions may declare required environment variable names. For Claude Code, generated project configuration uses environment expansion. Codex uses environment forwarding or environment-backed HTTP headers.

Do not commit `.env` files or literal secrets to MCP configuration.

## Project lockfile

When a project MCP state exists, `weap project lock` records its definition hashes and targets.

MCP capabilities are never auto-granted by `weap project apply-lock`. Install them explicitly, then run:

```bash
./weap project verify --project-dir=.
```

This keeps external capabilities opt-in even in reproducible team repositories.


## Reset a scope

Preview:

```bash
./weap mcp reset --scope project --project-dir=. --dry-run
```

Apply:

```bash
./weap mcp reset --scope project --project-dir=. --yes
```

Reset removes only MCP servers tracked by the WEAP MCP state for that scope. Manually configured servers are preserved.
