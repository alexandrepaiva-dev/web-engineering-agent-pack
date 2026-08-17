---
name: auth-security
description: Framework-agnostic identity, authentication and authorization engineering. Use for access control models, sessions/tokens, password security, account recovery, OAuth/OIDC concepts, CSRF/cookies, object-level authorization, or tenant isolation independent of Auth.js/Symfony implementation.
---


# Authentication and Authorization

Authentication proves identity; authorization decides whether an identity may perform an action on a resource.

1. Identify actor, action, resource, and tenant/context.
2. Define authentication/session lifecycle.
3. Enforce resource-level authorization server-side.
4. Define recovery/revocation behavior.
5. Apply abuse controls where sensitive.
6. Test unauthenticated, unauthorized, expired, replayed, and ownership-mismatch cases.
7. Use framework-specific security skills for concrete APIs.

Never trust browser-supplied roles or ownership. Fail closed, use least privilege, never log credentials/tokens, and use modern password hashing.

## References
- `references/authorization.md`
- `references/sessions.md`
- `references/passwords.md`
- `references/oauth-oidc.md`
- `references/recovery.md`
- `references/cookies-csrf.md`
