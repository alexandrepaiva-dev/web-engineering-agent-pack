# Data and mutations

A protected mutation should normally:
1. authenticate
2. validate
3. authorize
4. perform atomic/domain work
5. map expected errors
6. revalidate/invalidate only affected data where applicable

Never trust client-supplied ownership identifiers.

Consider idempotency when mutation can be retried by users or infrastructure.
