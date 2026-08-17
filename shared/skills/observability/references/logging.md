# Structured logging

Use stable event names and structured fields.

Useful fields include:
- request/job correlation ID
- actor/resource IDs that are safe to log
- operation name
- dependency/provider
- duration
- outcome/error class

Do not log secrets, raw tokens, passwords, recovery tokens or unnecessarily sensitive personal data.

Log unexpected failures at the layer that owns handling. Avoid duplicate logging at every rethrow.
