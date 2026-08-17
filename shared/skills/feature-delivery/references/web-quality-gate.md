# Web quality gate

Use the external `web-quality-audit` skill when installed and the delivered feature contains a meaningful browser-facing surface.

It complements `web-frontend-engineering`, `testing-playwright`, `performance-profiling`, `appsec-review`, and `code-review`.

Use it for landing pages, public pages, authenticated app pages, dashboards, forms, navigation, checkout pages, and substantial redesigns.

Skip it for database-only migrations, queue workers, cron jobs, CLI tools, pure backend services, and internal libraries with no browser surface.

Prioritize findings by real user impact, accessibility barriers, product regressions, Core Web Vitals/performance impact, SEO relevance, and concrete best-practice risk. Do not chase a perfect score at the expense of product behavior, security, or maintainability.
