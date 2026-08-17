---
name: appsec-review
description: Broad application-security review beyond authentication. Use for explicit threat modeling or review of XSS, CSRF, SSRF, injection, IDOR, uploads, webhooks, secrets, abuse controls, or multi-tenant security.
---


# Application Security Review

Use `auth-security` for authentication/session implementation details. Use this skill for broad application security analysis.

## Workflow

1. Define assets, actors and trust boundaries.
2. Identify externally controllable inputs.
3. Trace inputs to sensitive sinks and privileged operations.
4. Review tenant/resource isolation.
5. Review browser and server attack surfaces.
6. Review external integrations and webhooks.
7. Review secrets and sensitive logging.
8. Review abuse/rate-limit controls.
9. Prioritize concrete exploit paths.
10. Recommend least-complexity fixes and regression tests.

## Review standard

Every finding needs:
- severity
- affected entry point
- concrete attack/failure path
- impact
- evidence
- fix direction
- recommended regression test when practical

Do not produce speculative checklist noise.

## References

- `references/threat-modeling.md`
- `references/web-security.md`
- `references/ssrf-injection.md`
- `references/idor-multitenancy.md`
- `references/file-uploads.md`
- `references/webhooks-integrations.md`
- `references/secrets-dependencies.md`
- `references/abuse-rate-limiting.md`
