# Quick Start — Web Engineering Agent Pack v1.0.0

## Install global CORE

```bash
./weap install --profile core --with-third-party
```

Windows:

```powershell
.\weap.ps1 install --profile core --with-third-party
```

## Initialize a Next.js repository

```bash
./weap project init \
  --profile nextjs \
  --project-dir=. \
  --yes
```

## Initialize a Symfony repository

```bash
./weap project init \
  --profile symfony \
  --project-dir=. \
  --yes
```

## Detect the stack automatically

```bash
./weap project init --detect --project-dir=. --yes
```

## Self-contained team mode

```bash
./weap project init --detect --team --project-dir=. --yes
```

## MCP: preview

```bash
./weap mcp plan \
  --profile development \
  --scope project \
  --project-dir=.
```

## MCP: install

```bash
./weap mcp install \
  --profile development \
  --scope project \
  --project-dir=.
```

High-risk project filesystem access:

```bash
./weap mcp install \
  --server filesystem-project \
  --scope project \
  --project-dir=. \
  --allow-high-risk
```

## Diagnostics

```bash
./weap doctor --project-dir=.
./weap mcp doctor --scope project --project-dir=.
./weap audit
```

## Backups

```bash
./weap backup list
./weap backup restore latest
./weap project backup list --project-dir=.
```

## Uninstall

```bash
./weap uninstall --dry-run
./weap uninstall
```

## Update

```bash
./weap update
./weap update --apply
```

## Validate repository development

```bash
python scripts/validate-pack.py
python scripts/validate-schemas.py
python -m unittest discover -s tests -p "test_*.py"
bash tests/run-shell-tests.sh
```

Read `README.md` for the complete guide.


## Remove WEAP-managed MCP servers

```bash
./weap mcp reset --scope project --project-dir=. --yes
```
