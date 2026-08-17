---
name: code-review
description: Production-readiness review. Use when explicitly reviewing completed code, a PR, refactor, migration, architecture change, or when asked whether code is safe/correct/production-ready.
---


# Production Code Review

Prioritize material defects before style.

## Review order
1. correctness
2. security/authorization
3. data integrity/migrations
4. concurrency/idempotency
5. error handling
6. compatibility
7. performance
8. frontend accessibility/UX regressions
9. test quality
10. maintainability

## Evidence standard
Each finding needs severity, file/symbol, concrete failure mode, impact and fix direction.

Do not report speculative issues without a plausible path.
Do not flood reviews with formatter/style comments.

## Severity
- Critical: severe compromise/data loss/systemic outage.
- High: material security/data/payment/reliability defect.
- Medium: real bug/race/regression/operational issue.
- Low: limited-impact correctness/maintainability issue.

For broad changes consider read-only reviewer subagents, then deduplicate findings centrally.

## References
- `references/security.md`
- `references/database.md`
- `references/frontend.md`
- `references/backend.md`
- `references/testing.md`
- `references/performance.md`
