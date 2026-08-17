# Error reporting

Group unexpected errors by stable fingerprints rather than user-specific messages.

Attach safe context:
- release/version
- route/job
- environment
- correlation ID
- feature area

Redact secrets and personal data.

Expected validation/auth/domain failures should not necessarily become noisy error-reporting events.
