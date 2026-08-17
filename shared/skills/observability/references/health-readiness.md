# Health and readiness

Distinguish:
- liveness: should the process be restarted?
- readiness: should it receive traffic?
- dependency status: is a backing service degraded?

Keep checks cheap.

Do not make liveness fail merely because a transient dependency is down unless restarting the process helps.

Readiness may depend on critical startup state or unavailable required dependencies.
