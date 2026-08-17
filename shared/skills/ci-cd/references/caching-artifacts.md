# CI caches and artifacts

Cache dependency/package-manager data that is safe and keyed by relevant lockfiles/platform.

Do not cache secrets.

Artifacts should be immutable, identifiable by revision and have retention appropriate to their purpose.

Prefer promoting the tested artifact to rebuilding differently for production.
