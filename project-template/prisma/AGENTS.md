# Prisma/database scoped instructions

Before schema changes:
1. inspect recent migrations
2. inspect affected queries
3. define nullability/uniqueness/relationships
4. consider production rollout
5. consider indexes/concurrency

Rules:
- create new migrations according to project policy
- do not casually edit applied history
- do not remove/rename populated fields without a rollout/data plan
- define referential actions deliberately
- use DB constraints for invariants
- protect tenant relationships
- document justified raw SQL
