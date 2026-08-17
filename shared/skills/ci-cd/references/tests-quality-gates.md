# Quality gates

Required gates should reflect real risk:
- lint/static checks
- typecheck
- unit/integration tests
- E2E for critical flows
- build
- migration validation where relevant

Do not make flaky tests acceptable by retrying forever.

Keep required gates deterministic enough to be trusted.
