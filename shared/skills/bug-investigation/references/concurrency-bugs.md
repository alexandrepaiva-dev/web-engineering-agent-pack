# Concurrency bugs

Look for check-then-write, duplicate delivery, overlapping jobs, stale reads and missing unique constraints.

Reproduce with concurrent execution where possible.

Prefer atomic DB operations/constraints or durable idempotency over timing-based fixes.
