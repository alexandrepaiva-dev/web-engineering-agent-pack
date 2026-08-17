---
name: symfony-engineering
description: Symfony framework engineering. Use for Symfony controllers, services, dependency injection, routing, configuration, Validator, Serializer, Forms, Messenger, Events, Console, Cache, HttpFoundation, bundles, environments, or Symfony-specific architecture.
---


# Symfony Engineering
Inspect installed Symfony version/components before applying framework APIs.

1. Inspect service/autowiring conventions.
2. Reuse existing controller/service/domain boundaries.
3. Prefer installed Symfony components before adding dependencies.
4. Keep controllers focused on HTTP coordination when project architecture supports it.
5. Use Messenger only when asynchronous semantics are required.
6. Follow repository Validator/Serializer/Form/config conventions.
7. Run project-defined Composer/static-analysis/test/Symfony checks.

## References
- `references/services-di.md`
- `references/controllers-routing.md`
- `references/configuration.md`
- `references/validator-serializer-forms.md`
- `references/messenger-events-console.md`
- `references/cache-runtime.md`
