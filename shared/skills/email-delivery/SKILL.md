---
name: email-delivery
description: Transactional email delivery engineering. Use for SES/Resend/Postmark-style sending, templates, queues, retries, bounce/complaint handling, suppression, domain authentication, or deliverability.
---


# Email Delivery

Treat email as an asynchronous external-delivery system.

## Workflow

1. Classify transactional vs marketing email.
2. Define template/data contract.
3. Queue delivery when synchronous sending is unnecessary.
4. Define idempotency/deduplication.
5. Handle provider rate limits and transient failures.
6. Process bounce/complaint/delivery events.
7. Maintain suppression behavior.
8. Verify domain authentication and sender policy.
9. Track operational delivery metrics.
10. Test rendering and failure paths.

## Principles

- Do not block critical HTTP requests on avoidable email delivery.
- Never retry permanent recipient failures indefinitely.
- Suppress known hard-bounce/complaint recipients appropriately.
- Keep templates deterministic and versionable.
- Avoid putting secrets or overly sensitive data in email.
- Treat provider webhook events as untrusted until verified.
- Separate transactional consent rules from marketing consent rules.

## References

- `references/architecture.md`
- `references/templates.md`
- `references/queues-retries.md`
- `references/bounces-complaints.md`
- `references/deliverability.md`
- `references/domain-auth.md`
- `references/compliance.md`
- `references/observability.md`
