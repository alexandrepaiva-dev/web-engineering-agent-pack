from pathlib import Path
import json,re,sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]

manifest=json.loads((ROOT/"manifest.json").read_text(encoding="utf-8"))
readme=(ROOT/"README.md").read_text(encoding="utf-8")
quick=(ROOT/"docs/QUICKSTART.md").read_text(encoding="utf-8")
changelog=(ROOT/"CHANGELOG.md").read_text(encoding="utf-8")

version=manifest["version"]
skills=sorted(p.name for p in (ROOT/"shared/skills").iterdir() if p.is_dir())
profiles=sorted(p.stem for p in (ROOT/"profiles").glob("*.json") if p.stem!="catalog")

if set(manifest.get("skills",[])) != set(skills):
    errors.append("manifest skills do not match shared/skills")
if set(manifest.get("profiles",[])) != set(profiles):
    errors.append("manifest profiles do not match profiles/")
if version not in changelog:
    errors.append(f"CHANGELOG does not mention current version {version}")
if "# 6. MCP support" not in readme:
    errors.append("README missing MCP support section")

for command in [
    "./weap install","./weap project init","./weap project uninstall",
    "./weap backup restore","./weap project backup list","./weap project backup restore",
    "./weap mcp install","./weap mcp doctor",
    "scripts/validate-pack.py","scripts/validate-schemas.py"
]:
    if command not in readme:
        errors.append(f"README missing command/reference: {command}")

# Current-state examples must not advertise an older packVersion unless the paragraph
# explicitly discusses a historical migration.
for m in re.finditer(r'"packVersion"\s*:\s*"([^"]+)"',readme):
    found=m.group(1)
    context=readme[max(0,m.start()-300):m.start()].lower()
    if found != version and not any(x in context for x in ["v6","v7","v8","earlier","histor"]):
        errors.append(f"README current-state example uses old packVersion {found}")

if errors:
    print("DOCS CONSISTENCY FAILED")
    for e in errors: print("-",e)
    sys.exit(1)

print(f"Docs consistency OK: version={version}, skills={len(skills)}, profiles={len(profiles)}")
