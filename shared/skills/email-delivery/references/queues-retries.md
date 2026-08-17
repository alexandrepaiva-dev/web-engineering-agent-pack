# Email queueing and retries

Use bounded retries with backoff for transient provider/network errors.

Do not retry hard recipient failures indefinitely.

Make logical sends idempotent when duplicate emails are harmful.

Respect provider rate limits and account quotas.
