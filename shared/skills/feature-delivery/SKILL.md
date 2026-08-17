---
name: feature-delivery
description: End-to-end workflow for substantial multi-layer features. Use only when a feature spans multiple engineering areas or requires coordinated implementation, testing, review, and rollout.
---


# Feature Delivery

This is an orchestration skill. Reuse specialized skills instead of duplicating their detailed rules.

## Workflow

### 1. Understand
- restate the product outcome
- inspect repository conventions
- map the current code path
- identify affected actors, data and integrations

Use `codebase-explorer` when useful.

### 2. Design
Identify:
- UI impact
- API/backend behavior
- data model/migrations
- authorization
- async/background work
- external integrations
- observability
- rollout risk

Use `architecture-review` for non-trivial structural choices.

### 3. Plan
Create a dependency-aware implementation sequence.

Typical order:
1. schema/domain contracts
2. backend/services
3. authorization/security
4. queues/integrations
5. UI
6. tests
7. observability
8. deployment/migration considerations

### 4. Implement
Activate specialized skills as needed:
- `web-frontend-engineering`
- `react-engineering` / `twig-engineering` when applicable
- `nextjs-engineering` / `symfony-engineering` when applicable
- `backend-engineering`
- `nodejs-engineering` / `php-engineering` when applicable
- `auth-security`
- `authjs-engineering` / `symfony-security` when applicable
- `database-engineering`
- `prisma-engineering` / `doctrine-engineering` when applicable
- `postgresql-engineering` / `mysql-engineering` when applicable
- `async-jobs`
- `payments-engineering`
- `email-delivery`
- `file-storage`
- `observability`

Do not activate irrelevant skills merely because they exist.

### 5. Test
Use the closest relevant test layer plus `testing-playwright` for critical user journeys.

Cover important failure/permission/retry cases.

### 6. Review
Use:
- `web-quality-audit` when installed and the feature has a meaningful browser-facing surface
- `appsec-review` for security-sensitive features
- `performance-profiling` when deeper performance diagnosis is material
- `code-review` for production readiness

`web-quality-audit` is a web-surface quality gate, not a universal gate. Skip it for database-only changes, background workers, pure backend services, CLI tools, and migrations with no relevant web surface.

Delegate read-only reviewer subagents for large changes when useful.

### 7. Validate
Run repository-defined lint/typecheck/tests/build.

Review migrations, deployment sequencing and configuration.

### 8. Finish
Summarize:
- what changed
- important architectural decisions
- migrations/config required
- tests run
- unresolved risks or follow-up

## References

- `references/scope.md`
- `references/planning.md`
- `references/implementation-order.md`
- `references/testing-review.md`
- `references/rollout.md`
- `references/completion.md`
- `references/web-quality-gate.md`
