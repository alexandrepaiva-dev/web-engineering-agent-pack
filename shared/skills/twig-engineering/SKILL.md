---
name: twig-engineering
description: Twig template engineering for Symfony/PHP applications. Use for Twig templates, inheritance, components/macros, escaping, forms, localization, template performance, or server-rendered UI implemented with Twig.
---


# Twig Engineering
Use `web-frontend-engineering` for generic accessibility/responsive principles.

- keep auto-escaping enabled for untrusted content
- avoid domain/business logic in templates
- use inheritance/includes/components/macros consistently
- keep template data contracts explicit
- localize user-facing strings through the project translation system
- avoid ORM lazy-loading query storms triggered by templates

## References
- `references/escaping.md`
- `references/composition.md`
- `references/data-performance.md`
