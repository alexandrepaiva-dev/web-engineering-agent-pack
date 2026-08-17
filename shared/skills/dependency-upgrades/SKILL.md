---
name: dependency-upgrades
description: Dependency/framework upgrade workflow. Use only for explicit upgrades or migrations of Next.js, React, Node.js, Prisma, Auth.js, Playwright, Tailwind, BullMQ, Docker images, or other dependencies.
---


# Dependency Upgrades

Treat upgrades as behavior changes, not version-number edits.

## Workflow

1. Record current versions and runtime constraints.
2. Define target version/range.
3. Read official migration/release notes for skipped versions.
4. Identify breaking/deprecated APIs.
5. Inspect peer dependency and runtime compatibility.
6. Apply official codemods/migrations when appropriate.
7. Update code/config incrementally.
8. Run typecheck, tests and build.
9. Review lockfile and transitive-impact changes.
10. Document manual follow-up when needed.

## Principles

- Prefer one coherent upgrade scope at a time.
- Do not mix unrelated refactors into framework upgrades.
- Do not silence new compiler/runtime warnings without understanding them.
- Verify production runtime compatibility.
- Review schema/client generation changes for Prisma.
- Review cache/render behavior for Next.js upgrades.
- Review authentication/session behavior for Auth.js upgrades.
- Review browser/test runner compatibility for Playwright upgrades.

## References

- `references/upgrade-strategy.md`
- `references/next-react.md`
- `references/prisma-database.md`
- `references/authjs.md`
- `references/playwright.md`
- `references/tailwind.md`
- `references/node-docker.md`
- `references/lockfile-validation.md`
