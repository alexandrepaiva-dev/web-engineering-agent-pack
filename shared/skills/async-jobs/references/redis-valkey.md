# Redis / Valkey

Use namespaced keys, explicit TTLs, bounded collections and connection reuse.

Treat durability according to actual server configuration.

Avoid `KEYS *`/wildcard scans on production hot paths.

Do not treat ephemeral cache state as permanent business truth.
