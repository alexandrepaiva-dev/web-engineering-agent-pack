# Data ownership

For every important entity define which module/service owns writes and invariants.

Avoid multiple independent writers that can violate the same invariant.

Cross-module reads should preserve authorization and consistency requirements.

Shared databases do not imply shared ownership.
