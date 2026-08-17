---
name: mysql-engineering
description: MySQL/InnoDB-specific database engineering. Use for MySQL indexes, EXPLAIN plans, InnoDB locking/isolation, deadlocks, collations, utf8mb4, generated columns, JSON, foreign keys, transaction behavior, or MySQL-specific performance and migrations.
---


# MySQL Engineering
Use `database-engineering` for generic relational design.

1. Inspect actual MySQL/MariaDB version and SQL mode.
2. Inspect engine, charset, and collation.
3. Use EXPLAIN evidence for real query analysis.
4. Understand InnoDB clustered/secondary indexes.
5. Review isolation, locks, and deadlocks for concurrent code.
6. Review DDL for rebuild/lock impact.
7. Use utf8mb4 and deliberate collation semantics.

## References
- `references/indexes-plans.md`
- `references/innodb-transactions.md`
- `references/charset-collation.md`
- `references/json-generated-columns.md`
- `references/migrations-operations.md`
