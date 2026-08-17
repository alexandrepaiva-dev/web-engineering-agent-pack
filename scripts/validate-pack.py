from pathlib import Path
import json, re, sys, importlib.util

root = Path(__file__).resolve().parents[1]
skills_root = root / "shared" / "skills"
profiles_root = root / "profiles"
errors=[]

retired = {"frontend-engineering"}
for name in retired:
    if (skills_root/name).exists():
        errors.append(f"Retired skill directory still exists: {name}")

skill_dirs=sorted(p for p in skills_root.iterdir() if p.is_dir())
skill_names={p.name for p in skill_dirs}

for d in skill_dirs:
    sf=d/"SKILL.md"
    if not sf.exists():
        errors.append(f"{d.name}: missing SKILL.md")
        continue
    text=sf.read_text(encoding="utf-8")
    m=re.match(r"^---\n(.*?)\n---\n",text,re.S)
    if not m:
        errors.append(f"{d.name}: invalid frontmatter")
        continue
    fm=m.group(1)
    if f"name: {d.name}" not in fm:
        errors.append(f"{d.name}: frontmatter name mismatch")
    if "description:" not in fm:
        errors.append(f"{d.name}: missing description")
    refs=d/"references"
    if not refs.exists() or not list(refs.glob("*.md")):
        errors.append(f"{d.name}: no references")

# Load profile manager and validate every profile.
spec=importlib.util.spec_from_file_location("profile_manager", root/"scripts/profile_manager.py")
pm=importlib.util.module_from_spec(spec)
spec.loader.exec_module(pm)

profile_names=[]
for f in sorted(profiles_root.glob("*.json")):
    if f.stem=="catalog":
        continue
    profile_names.append(f.stem)
    try:
        resolved=pm.resolve_profile(f.stem)
    except Exception as e:
        errors.append(f"Profile {f.stem} failed to resolve: {e}")
        continue
    unknown=[s for s in resolved if s not in skill_names]
    if unknown:
        errors.append(f"Profile {f.stem} has unknown skills: {unknown}")

required_profiles={"core","nextjs","symfony","full","nextjs-mysql","symfony-postgresql"}
missing_profiles=required_profiles-set(profile_names)
if missing_profiles:
    errors.append(f"Missing profiles: {sorted(missing_profiles)}")

# Ensure intended profile separations.
try:
    core=set(pm.resolve_profile("core"))
    nextjs=set(pm.resolve_stack_only("nextjs"))
    symfony=set(pm.resolve_stack_only("symfony"))
    if "symfony-engineering" in nextjs or "nextjs-engineering" in symfony:
        errors.append("Cross-stack contamination detected in project profile deltas")
    if core & nextjs:
        errors.append("Next.js stack-only profile unexpectedly contains CORE skills")
    if core & symfony:
        errors.append("Symfony stack-only profile unexpectedly contains CORE skills")
except Exception as e:
    errors.append(f"Profile separation check failed: {e}")

required_files=[
    "README.md","docs/QUICKSTART.md","docs/TOKEN-EFFICIENCY.md","docs/BACKUP-RESTORE.md",
    "docs/THIRD-PARTY-SKILLS.md","docs/REPOSITORY.md","manifest.json",
    "scripts/profile_manager.py","scripts/analyze-context-budget.py",
    "scripts/install-claude-skill-overlays.py",
    "scripts/commands/install-all.sh","scripts/commands/install-codex.sh","scripts/commands/install-claude.sh","scripts/commands/install-project.sh",
    "scripts/commands/detect-project-stack.sh","scripts/commands/list-backups.sh","scripts/commands/restore-backup.sh","scripts/commands/cleanup-backups.sh",
    "scripts/commands/install-all.ps1","scripts/commands/install-codex.ps1","scripts/commands/install-claude.ps1","scripts/commands/install-project.ps1",
    "scripts/commands/detect-project-stack.ps1","scripts/commands/list-backups.ps1","scripts/commands/restore-backup.ps1","scripts/commands/cleanup-backups.ps1",
    "project-template/AGENTS.base.md",
    "project-template/profiles/nextjs/AGENTS.stack.md",
    "project-template/profiles/symfony/AGENTS.stack.md",
]
for rel in required_files:
    if not (root/rel).exists():
        errors.append(f"Missing required file: {rel}")

# README operational coverage.
readme=(root/"README.md").read_text(encoding="utf-8")
for phrase in [
    "./weap install","--profile core","--profile nextjs","--profile symfony",
    "--with-third-party","./weap project init","--detect","--team",
    "./weap backup restore","nextjs-mysql","symfony-postgresql",
    "./weap mcp install","./weap mcp doctor"
]:
    if phrase not in readme:
        errors.append(f"README missing operational step: {phrase}")

# Manifest consistency.
try:
    manifest=json.loads((root/"manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version")!="1.0.0":
        errors.append("manifest version is not 1.0.0")
    if set(manifest.get("skills",[]))!=skill_names:
        errors.append("manifest skill list differs from skill library")
except Exception as e:
    errors.append(f"manifest invalid: {e}")


# Uninstall/state lifecycle files.
for rel in [
    "scripts/commands/uninstall.sh","scripts/commands/uninstall.ps1","scripts/commands/uninstall-project.sh","scripts/commands/uninstall-project.ps1",
    "scripts/uninstall_project.py","scripts/state-lib.sh","scripts/StateLib.ps1"
]:
    if not (root/rel).exists():
        errors.append(f"Missing uninstall/state file: {rel}")

readme_text=(root/"README.md").read_text(encoding="utf-8")
for phrase in ["./weap uninstall --dry-run","--keep-third-party","--restore-previous","./weap project uninstall","--remove-ai-config"]:
    if phrase not in readme_text:
        errors.append(f"README missing uninstall workflow: {phrase}")


# Production-hardening files.
for rel in [
    "LICENSE","CONTRIBUTING.md","SECURITY.md","CODE_OF_CONDUCT.md",
    ".editorconfig",".gitignore",".gitattributes",
    ".github/workflows/ci.yml",".github/dependabot.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    "third-party.lock.json",
    "scripts/update-third-party-lock.py","scripts/install_locked_third_party.py",
    "scripts/transaction-lib.sh","scripts/TransactionLib.ps1",
    "scripts/validate-schemas.py",
    "schemas/profile.schema.json","schemas/project-manifest.schema.json",
    "schemas/install-state.schema.json","schemas/backup-manifest.schema.json",
    "schemas/third-party-lock.schema.json","schemas/repository-manifest.schema.json",
    "tests/test_profiles.py","tests/test_project_lifecycle.py",
    "tests/test_docs_consistency.py","tests/test_schema_files.py","tests/test_project_backup.py",
    "tests/run-shell-tests.sh","tests/run-powershell-tests.ps1",
    "scripts/docs-consistency.py","scripts/project_backup.py",
    "scripts/commands/list-project-backups.sh","scripts/commands/restore-project-backup.sh",
    "scripts/commands/list-project-backups.ps1","scripts/commands/restore-project-backup.ps1",
]:
    if not (root/rel).exists():
        errors.append(f"Missing production-hardening file: {rel}")


# Developer-experience files.
for rel in ['weap.py', 'weap', 'weap.ps1', 'scripts/doctor.py', 'scripts/project_lock.py', 'scripts/migrate.py', 'scripts/release.py', 'scripts/lint-skills.py', 'scripts/lint-profiles.py', 'scripts/generate-docs.py', 'scripts/generate-compatibility.py', 'scripts/project_backup.py', 'schemas/project-lock.schema.json', 'docs/PROFILE-CATALOG.md', 'docs/COMPATIBILITY.md', 'tests/test_security.py', 'tests/test_release.py', 'tests/fixtures/project-lock.json']:
    if not (root/rel).exists():
        errors.append(f"Missing developer-experience file: {rel}")


# Distribution-and-trust files.
for rel in [
    "scripts/update.py","scripts/build-site.py",
    "tests/test_update.py","tests/test_migration_matrix.py","tests/test_distribution.py",
    "docs/GITHUB-PAGES.md","docs/RELEASE-VERIFICATION.md",
    "site/index.html","site/styles.css","site/app.js",
    ".github/workflows/pages.yml",
]:
    if not (root/rel).exists():
        errors.append(f"Missing distribution/trust file: {rel}")


# Final v1 MCP and language-policy files.
for rel in [
    "shared/skills/mcp-engineering/SKILL.md",
    "scripts/mcp_manager.py","scripts/language-audit.py",
    "schemas/mcp-server.schema.json","schemas/mcp-profile.schema.json","schemas/mcp-state.schema.json",
    "mcp/registry/context7.json","mcp/registry/playwright.json","mcp/registry/filesystem-project.json",
    "mcp/profiles/docs.json","mcp/profiles/browser.json","mcp/profiles/development.json",
    "docs/MCP.md","docs/MCP-SECURITY.md",
    "tests/test_mcp.py","tests/fixtures/mcp-state.json",
]:
    if not (root/rel).exists():
        errors.append(f"Missing final v1 MCP/language file: {rel}")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print("-",e)
    sys.exit(1)

print(f"OK: {len(skill_names)} first-party skills")
print(f"OK: {len(profile_names)} profiles")
print(f"OK: CORE={len(pm.resolve_profile('core'))} skills")
print(f"OK: Next.js project delta={len(pm.resolve_stack_only('nextjs'))} skills")
print(f"OK: Symfony project delta={len(pm.resolve_stack_only('symfony'))} skills")
print("OK: project/global installers and documentation")
