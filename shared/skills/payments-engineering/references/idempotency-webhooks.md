# Idempotency and webhooks

Verify webhook authenticity before processing.

Persist provider event IDs or equivalent durable dedupe keys when duplicate delivery matters.

User-initiated payment creation should use stable idempotency when retry can create duplicate financial objects.

Handle out-of-order events using authoritative provider state/version or valid state-transition rules.
