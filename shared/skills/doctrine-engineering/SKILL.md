---
name: doctrine-engineering
description: Doctrine ORM/DBAL engineering. Use for entities, mappings, repositories, EntityManager, Unit of Work, DQL/QueryBuilder, relations, lazy/eager loading, Doctrine migrations, transactions, lifecycle events, or ORM-specific performance.
---


# Doctrine Engineering
Inspect installed Doctrine ORM/DBAL/Migrations versions.

1. Inspect entity/mapping style.
2. Use `database-engineering` for invariants and the vendor skill for DB behavior.
3. Define relation ownership/cardinality carefully.
4. Avoid N+1/lazy-loading storms.
5. Keep EntityManager transaction boundaries explicit.
6. Review generated migrations/SQL.
7. Parameterize DQL/QueryBuilder/native SQL values.

## References
- `references/entities-mapping.md`
- `references/unit-of-work.md`
- `references/queries.md`
- `references/relations-loading.md`
- `references/transactions-migrations.md`
- `references/security.md`
