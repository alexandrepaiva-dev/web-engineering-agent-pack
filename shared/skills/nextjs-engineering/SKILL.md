---
name: nextjs-engineering
description: Next.js App Router implementation. Use for pages, layouts, route handlers, Server/Client Components, Server Actions, routing, metadata, caching, revalidation, streaming, or Next.js-specific behavior.
---


# Next.js Engineering

Treat framework behavior as version-sensitive. Inspect the installed `next` version and current project patterns.

## Workflow
1. Inspect package/version and `app/`.
2. Identify server/client boundaries.
3. Inspect auth and authorization.
4. Inspect data access, mutations and caching.
5. Choose rendering/mutation model.
6. Keep privileged logic server-side.
7. Add appropriate loading/error/not-found behavior.
8. Validate with typecheck/tests/build.

## Defaults
- Server Components by default.
- `"use client"` only for browser APIs, event handlers, client state/context or client-only packages.
- Keep client boundaries close to interaction.
- Pass serializable props across boundaries.
- Never import server-only secrets into client code.
- Authorize protected reads/writes server-side.
- Use URL state for shareable filters/pagination when appropriate.

## Mutations
Authenticate → validate → authorize → write atomically where needed → map domain errors → revalidate only affected data.

Never trust hidden fields for ownership.

## Caching
Inspect current Next.js behavior before changing cache policy.
Explicitly reason about user/tenant scope and freshness.

## References
- `references/app-router.md`
- `references/server-client-boundaries.md`
- `references/data-mutations.md`
- `references/caching.md`
- `references/routing-metadata.md`
- `references/errors-streaming.md`
- `references/security.md`
- `references/performance.md`
