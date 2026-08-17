---
name: payments-engineering
description: Payment-system engineering. Use for Stripe-style payments, webhooks, refunds, disputes, connected accounts/marketplaces, idempotency, money state, fees, reconciliation, or financial correctness.
---


# Payments Engineering

Payment code is correctness- and integrity-sensitive. Treat provider APIs as external distributed systems with retries, asynchronous events and partial failure.

## Workflow

1. Define merchant/marketplace money flow.
2. Define source of truth for order/payment state.
3. Model payment state transitions.
4. Define idempotency for user requests and provider events.
5. Define webhook verification and duplicate/out-of-order handling.
6. Define refund/dispute behavior.
7. Define fees, currency, rounding and accounting boundaries.
8. Define reconciliation strategy.
9. Test partial failures and retries.
10. Review security and observability.

## Principles

- Never infer paid status solely from browser redirect success.
- Provider webhooks/events must be verified and idempotent.
- Store provider identifiers needed for reconciliation.
- Use exact monetary representations.
- Keep application order state distinct from provider payment state.
- Define who bears fees/losses/refunds in marketplace flows.
- Prefer provider-native idempotency where available plus durable local invariants.
- Avoid destructive edits to financial history; prefer explicit state transitions/audit records.

## References

- `references/payment-state.md`
- `references/idempotency-webhooks.md`
- `references/refunds-disputes.md`
- `references/marketplaces.md`
- `references/money-currency.md`
- `references/reconciliation.md`
- `references/security-compliance.md`
- `references/testing.md`
