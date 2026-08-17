# App Router scoped instructions

- Prefer Server Components.
- Keep `"use client"` boundaries as small as practical.
- Validate and authorize sensitive mutations server-side.
- Never expose secrets or privileged records through serialized props.
- Reuse existing route/layout/loading/error/not-found conventions.
- Use URL state intentionally for filters/pagination where appropriate.
- Do not disable caching/dynamic behavior globally to solve a local issue.
- For substantial UI work, follow the project design system and frontend/UI skills.
