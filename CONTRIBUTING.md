# Contributing

Contributions are welcome.

## Before opening a PR

Run:

```bash
python scripts/validate-pack.py
python scripts/analyze-context-budget.py
python scripts/validate-schemas.py
python scripts/lint-skills.py
python scripts/lint-profiles.py
python scripts/docs-consistency.py
python -m unittest discover -s tests -p "test_*.py"
bash tests/run-shell-tests.sh
```

On Windows also run:

```powershell
.	ests
un-powershell-tests.ps1
```

## Adding a skill

1. Add `shared/skills/<name>/SKILL.md`.
2. Keep the description precise enough for reliable triggering.
3. Keep detailed guidance in `references/`.
4. Add the skill to a profile only when it is genuinely part of that stack/capability.
5. Update tests and README when behavior changes.
6. Re-run the context-budget analyzer.

## Adding a profile

Add `profiles/<name>.json` that validates against `schemas/profile.schema.json`.

Avoid creating profiles that duplicate an existing profile with only cosmetic differences.

## Installer changes

Installer changes require regression tests for:
- dry run
- install
- failure rollback
- backup/restore
- uninstall
- preservation of unrelated configuration

## Pull requests

Keep changes focused. Explain:
- problem
- proposed behavior
- compatibility impact
- tests performed
- migration implications
