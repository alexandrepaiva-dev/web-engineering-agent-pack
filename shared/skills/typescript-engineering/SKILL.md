---
name: typescript-engineering
description: TypeScript language and type-system engineering. Use for strict typing, domain types, generics, narrowing, unions, module boundaries, compiler configuration, or TypeScript refactors independent of React/Next.js.
---


# TypeScript Engineering
- use strict typing
- prefer inference locally and explicit types at important boundaries
- use `unknown` for untrusted values
- model variants with discriminated unions
- avoid `any`, unsafe assertions, and non-null shortcuts
- validate runtime data separately from static typing

Inspect `tsconfig.json`, preserve public compatibility unless intentionally changing it, and run typecheck after meaningful changes.

## References
- `references/domain-types.md`
- `references/narrowing.md`
- `references/generics.md`
- `references/config.md`
