# Data bugs

Check whether bad behavior comes from:
- invalid historical data
- migration/backfill
- missing constraint
- stale cache
- timezone/rounding
- inconsistent derived state

Inspect source-of-truth data before patching presentation logic.
