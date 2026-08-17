# Token and Context Efficiency — v8

Version 7 optimizes context by separating **CORE** from **stack-specific project profiles**.

## Recommended model

```text
Global context:
  CORE only

Next.js repository:
  global CORE
  + project Next.js delta

Symfony repository:
  global CORE
  + project Symfony delta
```

This avoids advertising every framework/ORM/database skill in every repository.

## Always-present context

Keep small:

- global `~/.codex/AGENTS.md`
- global `~/.claude/CLAUDE.md`
- project `AGENTS.md`
- project `CLAUDE.md`
- metadata/descriptions of skills actually visible in that scope

Do not place framework tutorials in persistent instruction files.

## On-demand context

Detailed knowledge belongs in:

```text
SKILL.md
references/*.md
subagents
external skills
```

The agent should load those only when relevant.

## Skill body targets

Recommended heuristic:

```text
description: generally < ~75 estimated tokens
SKILL.md: generally < ~900 estimated tokens
```

Move detail to `references/`.

## Profile budgets

Run:

```bash
python scripts/analyze-context-budget.py
```

The report now calculates metadata budgets for:

```text
core
nextjs
symfony
nextjs-mysql
symfony-postgresql
full
```

The important number for the recommended setup is not the `full` profile.

It is:

```text
global CORE metadata
+
project stack-delta metadata
```

## Manual-only Claude skills

The Claude installer adds:

```yaml
disable-model-invocation: true
```

to selected heavy/specialized workflows:

- `architecture-review`
- `ci-cd`
- `dependency-upgrades`
- `performance-profiling`

They remain explicitly invokable but are less likely to enter context unnecessarily.

## Subagents

Recommended use:

```text
small task       0
medium task      0–1
large/high-risk  1–4 read-only specialists
```

Do not launch all reviewers mechanically.

## Project profiles

Project installation normally installs only the stack delta.

Example:

```text
nextjs project delta:
typescript
react
tailwind
nextjs
node
authjs
prisma
postgresql
async-jobs
```

CORE remains global.

Use:

```bash
--include-core
```

only when you intentionally want a self-contained repository.

## External skills

`ui-ux-pro-max` and `web-quality-audit` are optional external skills.

Use them only when task type warrants them.

## Analyzer

```bash
python scripts/analyze-context-budget.py
```

It reports:

- persistent global token estimates
- each skill description
- each `SKILL.md`
- reference size
- trigger overlap
- duplicate long paragraphs
- effective profile metadata
- stack-only project-delta metadata

Output:

```text
context-budget-report.json
```

The estimator uses approximately four characters per token. It is a budgeting heuristic, not the model's exact tokenizer.


Version 8 adds uninstall/state tooling only; it does not add skill metadata or change the profile token budgets.
