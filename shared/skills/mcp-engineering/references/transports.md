# MCP transports

Use stdio for local processes started by the MCP client.

Use Streamable HTTP for remote services. Prefer it over deprecated SSE-only integrations when HTTP is available.

Transport selection affects authentication, lifecycle, deployment, observability, and failure handling.
