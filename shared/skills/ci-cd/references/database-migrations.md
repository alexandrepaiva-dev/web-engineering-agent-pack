# Database migrations in delivery

Separate schema rollout from application assumptions for risky changes.

Prefer expand/contract.

Do not run a destructive migration automatically before a compatible app is deployed unless explicitly safe.

Backups do not replace migration design.

Make migration failures visible and halt dependent deployment steps.
