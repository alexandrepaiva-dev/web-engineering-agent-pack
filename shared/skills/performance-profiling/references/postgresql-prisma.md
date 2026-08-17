# PostgreSQL and Prisma performance

Use query logs/EXPLAIN evidence for expensive queries.

Look for:
- N+1
- missing/selectivity-poor indexes
- unbounded relation loading
- large sorts
- deep offsets
- connection pool saturation

Optimize query shape and indexes together.
