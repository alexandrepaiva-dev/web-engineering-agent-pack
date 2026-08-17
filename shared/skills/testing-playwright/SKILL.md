---
name: testing-playwright
description: Playwright E2E/browser testing. Use for Playwright tests, fixtures, auth state, browser automation, network behavior, flaky tests, or critical user-flow coverage.
---


# Playwright Testing

Test user-observable behavior, not implementation details.

## Workflow
1. Read Playwright config/fixtures.
2. Identify setup conventions.
3. Define journey/preconditions.
4. Prefer accessible locators.
5. Make data deterministic/isolated.
6. Use web-first assertions.
7. Avoid arbitrary sleeps.
8. Preserve useful failure artifacts.
9. Run narrow test then affected suite.

## Locator priority
1. `getByRole`
2. `getByLabel`
3. stable user-visible locators
4. `getByTestId` when semantics are impractical

Never use `waitForTimeout()` as routine synchronization.

## Coverage
Critical flows should consider happy path, validation, auth/permissions, empty/error states and mobile when relevant.

## References
- `references/locators.md`
- `references/fixtures.md`
- `references/authentication.md`
- `references/network.md`
- `references/test-data.md`
- `references/flakiness.md`
- `references/accessibility.md`
