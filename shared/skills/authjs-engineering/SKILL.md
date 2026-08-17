---
name: authjs-engineering
description: Auth.js/NextAuth implementation. Use for Auth.js providers, adapters, callbacks, session strategy, cookies, OAuth/Credentials flows, account linking, protected Next.js routes, or Auth.js-specific configuration.
---


# Auth.js Engineering
Auth.js APIs/package names are version-sensitive. Inspect installed packages and existing config.

1. Inspect providers, adapter, session strategy, callbacks/events, cookies, and custom pages.
2. Keep generic authorization rules separate from authentication.
3. Keep protected reads/mutations server-side.
4. Review account-linking/provider-email semantics.
5. Test login, logout, expiry, unauthorized access, and provider callbacks.

## References
- `references/configuration.md`
- `references/sessions.md`
- `references/providers.md`
- `references/credentials.md`
- `references/account-linking.md`
