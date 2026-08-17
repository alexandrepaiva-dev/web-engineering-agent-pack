# Caching

Define key, value schema, TTL, invalidation, tenant/user scope, stale behavior and miss behavior.

Never omit tenant/user dimensions from cache keys for scoped values.

Cache failure should degrade safely rather than corrupt durable state.
