# Codex + Claude Code Project Setup — v8

The recommended model is:

```text
Global: CORE
Project: stack-specific profile delta
```

## Next.js project

```bash
weap project install --profile=nextjs --project-dir=/path/to/repo --init-project
```

## Symfony project

```bash
weap project install --profile=symfony --project-dir=/path/to/repo --init-project
```

Codex project skills:

```text
.agents/skills/
```

Claude project skills:

```text
.claude/skills/
```

The installer records pack-managed project skills in:

```text
.web-engineering-agent-pack.json
```

On upgrade it replaces only those pack-managed skills and preserves custom project skills.

## Project instructions

`AGENTS.md` is the shared repository engineering policy.

`CLAUDE.md` imports:

```text
@AGENTS.md
```

so common repository rules are maintained once.

Keep project-specific domain knowledge in local skills such as:

```text
.agents/skills/project-domain/
.claude/skills/project-domain/
```

Do not copy framework tutorials into `AGENTS.md`.
