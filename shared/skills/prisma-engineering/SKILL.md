---
name: prisma-engineering
description: Prisma ORM engineering independent of PostgreSQL/MySQL choice. Use for Prisma schema, generated client, relations, query shape, migrations, transactions, Prisma configuration, or ORM-specific behavior.
---


# Prisma ORM Engineering
Inspect installed Prisma version and database provider.

1. Inspect schema/config/migrations/generated-client conventions.
2. Use `database-engineering` for relational invariants.
3. Use the selected database-vendor skill for engine behavior.
4. Bound queries and avoid N+1 relation loops.
5. Understand transaction/nested-write semantics.
6. Regenerate client and run relevant checks after schema changes.

## References
- `references/schema.md`
- `references/queries.md`
- `references/transactions.md`
- `references/migrations.md`
- `references/database-provider.md`
