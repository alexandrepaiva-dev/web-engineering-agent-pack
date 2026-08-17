# Dockerfile

Order layers for caching:
1. base/runtime setup
2. lockfile/package metadata
3. dependency install
4. source
5. build

Use deterministic install commands.

Use multi-stage builds when build dependencies differ materially from runtime requirements.
