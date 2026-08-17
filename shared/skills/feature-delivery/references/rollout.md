# Rollout

Identify:
- environment variables
- migrations/backfills
- feature flags if needed
- queue workers
- provider configuration
- DNS/storage/email/payment setup
- deployment ordering
- rollback/forward-fix constraints

Do not declare a feature done if production requires undocumented manual setup.
