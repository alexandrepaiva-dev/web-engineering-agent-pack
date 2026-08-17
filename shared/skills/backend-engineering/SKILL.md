---
name: backend-engineering
description: Stack-agnostic backend architecture and service logic. Use for API boundaries, validation, service/domain behavior, error models, idempotency, webhooks, external integrations, transactions, logging, or server-side design independent of Node.js/PHP framework choice.
---


# Backend Engineering

1. Trace the external entry point to side effects.
2. Identify trusted and untrusted data.
3. Validate and normalize at boundaries.
4. Define domain/service ownership and error semantics.
5. Define transaction and external side-effect boundaries.
6. Add idempotency/retry behavior where re-execution is possible.
7. Keep authorization near protected operations.
8. Add tests for success and meaningful failure paths.
9. Use language/framework-specific skills for implementation details.

## References
- `references/api-boundaries.md`
- `references/validation.md`
- `references/errors.md`
- `references/idempotency.md`
- `references/webhooks.md`
- `references/transactions.md`
- `references/logging.md`
