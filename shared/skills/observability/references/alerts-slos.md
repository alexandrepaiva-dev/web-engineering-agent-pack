# Alerts and SLOs

Alert on user/system impact, not every anomaly.

Prefer signals such as:
- sustained elevated error rate
- latency SLO breach
- queue age/backlog
- payment/webhook failure rate
- exhausted worker capacity
- critical dependency unavailability

Every alert should have an owner, severity and first diagnostic action.

Avoid alerts that routinely self-resolve without action.
