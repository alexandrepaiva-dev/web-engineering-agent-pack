# Synchronous vs asynchronous boundaries

Use synchronous calls when the caller needs immediate authoritative outcome.

Use asynchronous processing for decoupling, retryable external work, fan-out or non-interactive latency.

Async boundaries introduce delivery semantics, ordering, retries, idempotency and observability requirements.
