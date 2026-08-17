# Metrics

Use metrics for aggregate operational questions.

Good metric dimensions are bounded and stable. Avoid high-cardinality labels such as user ID, request ID, email, URL with arbitrary IDs, or exception message.

Useful families:
- request count/error rate/duration
- queue depth/age/processing duration
- dependency error/latency
- DB pool saturation
- business-critical workflow success/failure

Use histograms for latency distributions when supported.
