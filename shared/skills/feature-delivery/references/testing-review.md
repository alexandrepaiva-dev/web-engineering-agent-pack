# Testing and review

Use unit/integration coverage for core invariants and Playwright for critical user journeys.

Review high-risk dimensions explicitly:
- authorization
- money/data integrity
- retries/idempotency
- migration compatibility
- accessibility
- failure states

Use read-only specialized reviewers when the change is broad enough.
