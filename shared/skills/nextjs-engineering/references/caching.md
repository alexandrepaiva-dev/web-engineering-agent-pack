# Caching

Next.js caching semantics are version-sensitive.

Before changing them:
- inspect installed Next.js
- inspect project conventions
- identify user/tenant scope
- identify freshness needs
- identify invalidation strategy

Never cache privileged user-specific data in a shared cross-user scope.

Avoid global dynamic/cache-disabling flags as a shortcut for a local data issue.
