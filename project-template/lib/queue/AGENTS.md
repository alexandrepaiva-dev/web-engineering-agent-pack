# Queue scoped instructions

Every job must define:
- stable name
- validated/versionable payload
- retry/backoff policy
- idempotency behavior
- concurrency/rate-limit expectations
- logging/correlation
- failure handling

Workers must tolerate duplicate execution.
Do not put secrets in job payloads.
Use durable DB state for durable invariants; Redis/Valkey dedupe only complements it.
