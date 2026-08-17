# Health checks

Distinguish liveness, readiness and dependency health.

Health endpoints should be cheap.

Do not make liveness fail merely because a temporary downstream dependency is unavailable unless process restart is corrective.
