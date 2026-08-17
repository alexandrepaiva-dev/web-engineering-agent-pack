# Docker Compose

Use clear service roles.

For DB/Valkey:
- use named volumes when local persistence is desired
- remember `depends_on` is not readiness by itself
- use health/retry connection logic
- avoid exposing internal ports unless needed

Keep committed credentials development-only or inject them externally.
