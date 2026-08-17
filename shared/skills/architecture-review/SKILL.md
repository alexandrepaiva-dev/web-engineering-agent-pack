---
name: architecture-review
description: Software architecture evaluation. Use only for explicit architecture/design review, module/service boundaries, dependency direction, data ownership, sync/async choices, scalability, reliability, or ADR decisions.
---


# Architecture Review

Prefer simple architecture that matches current scale and failure modes.

## Workflow

1. Define business/system goal.
2. Map current boundaries and data flow.
3. Identify invariants and ownership.
4. Identify coupling and dependency direction.
5. Identify scaling/reliability constraints.
6. Evaluate proposed alternatives.
7. Compare complexity, operability and migration cost.
8. Recommend the smallest architecture that satisfies requirements.
9. Record meaningful decisions in an ADR when warranted.

## Review dimensions

- cohesion
- coupling
- ownership
- data consistency
- transaction boundaries
- asynchronous boundaries
- failure isolation
- security boundaries
- deployment/operational complexity
- observability
- testability
- migration path

Do not recommend microservices, event buses, CQRS or additional infrastructure without a concrete problem they solve.

## References

- `references/boundaries-modularity.md`
- `references/data-ownership.md`
- `references/sync-async.md`
- `references/reliability.md`
- `references/scalability.md`
- `references/security-operability.md`
- `references/adrs.md`
- `references/review-checklist.md`
