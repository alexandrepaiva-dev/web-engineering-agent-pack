# Locks and deduplication

Distributed locks require explicit ownership token, expiration and safe release.

Protect durable invariants with DB constraints where possible.

A time-window dedupe is not permanent uniqueness.
