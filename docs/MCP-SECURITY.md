# MCP Security Model

MCP capabilities can materially expand an agent's access.

## Risk levels

### Low

Read-oriented capability with limited external side effects.

### Medium

Capability can interact with a browser or external environment but is normally recoverable.

### High

Capability can write files, modify external state, or access broad project data.

### Critical

Capability can affect production systems, sensitive databases, infrastructure, credentials, or high-impact external state.

## WEAP rules

1. MCP installation is always explicit.
2. High and critical risk definitions require `--allow-high-risk`.
3. Secrets are never stored in registry definitions.
4. Project-bound filesystem access cannot be installed at user scope.
5. Existing unmanaged server names are not silently overwritten.
6. Project MCP configuration is included in reproducibility verification, but never automatically granted by lockfile application.
7. Third-party MCP output is treated as untrusted.
8. Production database write access should not be represented by a default WEAP registry entry.

## Database integrations

WEAP ships only a database template.

Create organization-specific database definitions using the narrowest privileges possible. Prefer read-only accounts for analysis. Separate development, staging, and production credentials.

## Filesystem integrations

Restrict roots to the active repository or a smaller path. Do not expose a user's entire home directory merely for convenience.

## Browser integrations

Browser automation can trigger external side effects such as form submission, account changes, or purchases. Keep write actions behind agent/client approval.

## Third-party trust

Review the source repository, release/version policy, permissions, and maintenance status of an MCP server before adopting it.
