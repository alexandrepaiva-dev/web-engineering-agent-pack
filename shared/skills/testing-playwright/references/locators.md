# Locators

Prefer:
```ts
page.getByRole('button', { name: 'Save' })
page.getByLabel('Email')
page.getByRole('heading', { name: 'Settings' })
```

Use test IDs only when semantic/user-facing targeting is impractical.

Avoid generated CSS classes, nth-child and DOM-shape-dependent chains.
