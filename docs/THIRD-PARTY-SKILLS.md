# Recommended third-party skills

This pack intentionally does not vendor third-party skill source code.

## ui-ux-pro-max

Use for substantial UI/UX design and design-system work.

```bash
npx skills add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max
```

## web-quality-audit

Use for Lighthouse-style review across Performance, Accessibility, SEO, Best Practices, and Core Web Vitals-oriented quality signals.

```bash
npx skills add https://github.com/addyosmani/web-quality-skills --skill web-quality-audit
```

## Recommended separation

```text
CREATE
├── ui-ux-pro-max
├── web-frontend-engineering
└── nextjs-engineering

VALIDATE
├── testing-playwright
├── web-quality-audit
├── appsec-review
└── code-review

DIAGNOSE
├── bug-investigation
├── performance-profiling
└── observability
```

Update third-party skills using their upstream mechanisms rather than copying their source into this repository.


## v9 supply-chain locking

Version 9 installs these external skills from exact reviewed Git commit SHAs recorded in:

```text
third-party.lock.json
```

Preview:

```bash
./scripts/commands/install-third-party-skills.sh --dry-run
```

Install the locked snapshots:

```bash
./scripts/commands/install-third-party-skills.sh
```

Check whether upstream has changed:

```bash
python scripts/update-third-party-lock.py
```

Update the lock only after reviewing upstream changes:

```bash
python scripts/update-third-party-lock.py --apply
```
