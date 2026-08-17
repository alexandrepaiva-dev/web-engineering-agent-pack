# Networking and storage

Separate containers reach each other by service/network DNS name, not by each other's `localhost`.

Treat container filesystems as ephemeral.

Use explicit volumes/services for durable data and an independent backup strategy.
