---
name: docker-devops
description: Docker/container engineering. Use for Dockerfiles, Compose, multi-stage builds, runtime images, health checks, networking, storage, or container deployment behavior.
---


# Docker and Container Engineering

Containerize the application, not an entire workstation.

## Workflow
1. Inspect package manager, build output, runtime and deployment target.
2. Separate build/runtime dependencies.
3. Design cache-friendly layers.
4. Use multi-stage builds where useful.
5. Define runtime user/permissions.
6. Keep secrets out of layers.
7. Ensure proper signals.
8. Add meaningful health checks.
9. Model persistent storage explicitly.
10. Test clean build/start.

## Rules
- Use `.dockerignore`.
- Prefer deterministic installs.
- Keep dev tools out of production when practical.
- Run non-root when practical.
- Inject secrets at runtime/build-secret mechanisms, never `.env` into image.
- Pin base strategy intentionally.

## References
- `references/dockerfile.md`
- `references/node-runtime.md`
- `references/compose.md`
- `references/security.md`
- `references/healthchecks.md`
- `references/networking-storage.md`
