---
name: async-jobs
description: Redis/Valkey and BullMQ engineering. Use for queues, workers, delayed jobs, retries, concurrency, locks, deduplication, caching, or asynchronous side effects.
---


# Async Jobs, Redis/Valkey and BullMQ

Assume queued work may execute more than once.

## Workflow
1. Identify durable source of truth.
2. Define/validate job contract.
3. Define idempotency before side effects.
4. Classify retryable vs terminal errors.
5. Choose bounded retries/backoff.
6. Set concurrency from downstream capacity.
7. Define timeout/stall behavior where relevant.
8. Define observability/failed-job handling.
9. Implement graceful shutdown.
10. Test duplicates and transient failures.

## Payloads
Keep payloads small, serializable, versionable, validated and free of secrets.

## Idempotency
Prefer durable operation IDs/constraints/provider idempotency keys for durable side effects.

## Redis/Valkey
Treat cache loss as expected unless durability is explicitly guaranteed.
Namespace keys, define TTLs and avoid wildcard scans on hot paths.

## References
- `references/redis-valkey.md`
- `references/bullmq.md`
- `references/idempotency.md`
- `references/retries.md`
- `references/concurrency.md`
- `references/caching.md`
- `references/locks-deduplication.md`
- `references/operations.md`
