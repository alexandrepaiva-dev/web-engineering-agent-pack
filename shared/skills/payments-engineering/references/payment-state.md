# Payment state

Model application order state separately from provider payment state.

Examples of concepts:
- order pending/confirmed/cancelled/refunded
- payment requires_action/processing/succeeded/failed/refunded/disputed

Do not mark paid from client redirect alone.

Transitions should be monotonic/validated where possible, with auditability for financial actions.
