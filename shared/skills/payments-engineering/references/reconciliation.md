# Reconciliation

Persist provider IDs required to join local orders/payments/refunds/disputes to provider records.

Regularly reconcile:
- succeeded payments
- refunds
- disputes
- fees
- transfers/payouts where relevant

Flag orphaned or contradictory states.

Reconciliation should be restartable and idempotent.
