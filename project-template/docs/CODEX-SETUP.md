# Repository Codex setup

Instruction chain:
```text
~/.codex/AGENTS.md
  ↓
repo/AGENTS.md
  ↓
nearest nested AGENTS.md
```

Global skills cover frontend, Next.js, backend, auth/security, database, queues, Playwright, Docker and review.

Use project `.agents/skills/` only for product/domain-specific reusable knowledge.

Update `AGENTS.md` when a convention is recurring/non-obvious.
Do not store secrets, temporary debug notes or one-off task requirements there.
