# Playwright/E2E scoped instructions

- Test user-observable outcomes.
- Prefer `getByRole`, `getByLabel`, and semantic locators.
- Use test IDs only when semantics are impractical.
- Never use `waitForTimeout()` as routine synchronization.
- Keep tests independent and parallel-safe.
- Create deterministic test data.
- Do not depend on manual records or execution order.
- Keep auth setup test-only and secure.
- Cover success plus important validation/auth/error paths for critical flows.
- Fix the root cause of flakes rather than only adding retries.
