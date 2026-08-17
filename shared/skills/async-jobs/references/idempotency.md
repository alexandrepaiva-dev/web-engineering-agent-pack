# Idempotency

Repeating the same logical operation must not duplicate unintended effects.

Durable patterns:
- unique operation table
- unique external event ID
- atomic state transition
- provider idempotency key

For durable side effects, do not rely only on a short-lived Redis key.
