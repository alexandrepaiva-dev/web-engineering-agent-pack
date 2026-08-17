# Codex MCP

Codex stores MCP configuration in global `~/.codex/config.toml` or trusted project `.codex/config.toml`.

Each server uses a `[mcp_servers.<name>]` table.

Codex supports stdio and Streamable HTTP servers, environment forwarding, OAuth/bearer authentication, tool allow/deny lists, and approval modes.

WEAP writes only inside its explicitly marked MCP block and preserves unrelated Codex configuration.
