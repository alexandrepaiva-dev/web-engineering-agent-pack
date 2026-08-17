# Repository Engineering Instructions

Profile: `{{PROFILE}}`

## Source of truth

Before substantial changes inspect:
- package/dependency manifests and lockfiles
- installed runtime/framework versions
- relevant configuration
- existing modules/components/services
- schema/migrations
- tests and CI commands

Existing repository conventions outrank generic examples.

## General rules

- use the repository package/dependency manager
- do not create a second lockfile
- validate external input at boundaries
- enforce authorization server-side
- preserve existing architecture before creating parallel patterns
- update tests when behavior changes
- do not commit secrets
- run repository-defined lint/static-analysis/typecheck/tests/build as applicable
- do not invent commands without checking repository configuration

## Design and web quality

For substantial visual work, use `ui-ux-pro-max` when installed.

For substantial browser-facing features, use `web-quality-audit` when installed before release.

## Project-specific domain

Put durable business rules in project-local skills such as:

```text
.agents/skills/project-domain/
.claude/skills/project-domain/
```

Do not duplicate framework tutorials in this file.
