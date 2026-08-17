---
name: observability
description: Production observability. Use for structured logs, metrics, tracing, OpenTelemetry, error reporting, correlation IDs, health/readiness, dashboards, alerts, or SLOs.
---


# Observability

Build observability around questions operators must answer, not around collecting every possible signal.

## Workflow

1. Identify critical user journeys and backend workflows.
2. Define the failure questions operators need to answer.
3. Choose logs, metrics and traces for those questions.
4. Propagate correlation context across HTTP, queues and external calls.
5. Define actionable dashboards and alerts.
6. Protect sensitive data in telemetry.
7. Validate health/readiness semantics.
8. Test observability for both success and failure paths.

## Principles

- Structured logs over free-form logs.
- Stable event names over arbitrary prose.
- Metrics for trends and alerting.
- Traces for distributed causal paths.
- Logs for high-cardinality diagnostic context.
- Alerts must be actionable and tied to user/system impact.
- Do not emit secrets, credentials, raw tokens, or unnecessary personal data.
- Avoid high-cardinality metric labels.
- Sampling must preserve important failures.

## References

- `references/logging.md`
- `references/metrics.md`
- `references/tracing-opentelemetry.md`
- `references/error-reporting.md`
- `references/health-readiness.md`
- `references/alerts-slos.md`
- `references/correlation-context.md`
- `references/privacy-cost.md`
