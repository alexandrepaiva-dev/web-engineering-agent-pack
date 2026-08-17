---
name: ci-cd
description: CI/CD pipeline engineering. Use when explicitly changing or reviewing build/test/deploy pipelines, GitHub Actions, environment promotion, migration sequencing, deployment verification, rollback, or CI secrets.
---


# CI/CD

A delivery pipeline should make unsafe changes harder to ship and safe changes boring to release.

## Workflow

1. Identify repository branches/release model.
2. Define required quality gates.
3. Make builds reproducible.
4. Cache dependencies/artifacts safely.
5. Separate build/test from deployment.
6. Define environment promotion.
7. Define database migration sequencing.
8. Define secrets and permissions.
9. Define rollback/forward-fix strategy.
10. Add observability around deployment outcomes.

## Principles

- Least privilege for CI credentials.
- Pin third-party actions/dependencies according to project security policy.
- Never expose secrets to untrusted fork PRs.
- Avoid duplicated expensive jobs.
- Cache only reproducible/appropriate artifacts.
- Run destructive migrations only with an explicit rollout plan.
- Production deployment should have a traceable revision.
- Failed post-deploy verification must have a defined response.

## References

- `references/pipeline-design.md`
- `references/github-actions-security.md`
- `references/caching-artifacts.md`
- `references/tests-quality-gates.md`
- `references/deployments-environments.md`
- `references/database-migrations.md`
- `references/secrets-permissions.md`
- `references/rollback-verification.md`
