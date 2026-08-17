# Retries

Retry transient failures such as timeouts, temporary outages and rate limits according to provider semantics.

Usually do not retry unchanged validation/auth/authorization/domain failures.

Use bounded exponential backoff with jitter where appropriate.

Surface exhausted jobs operationally.
