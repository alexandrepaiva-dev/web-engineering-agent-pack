from pathlib import Path
import re,sys,math

ROOT=Path(__file__).resolve().parents[1]
errors=[];warnings=[]

def tok(s):return max(1,math.ceil(len(s)/4))
for d in sorted((ROOT/"shared/skills").iterdir()):
    if not d.is_dir():continue
    sf=d/"SKILL.md"
    if not sf.exists():
        errors.append(f"{d.name}: missing SKILL.md");continue
    text=sf.read_text(encoding="utf-8")
    fm=re.match(r"^---\n(.*?)\n---\n",text,re.S)
    if not fm:
        errors.append(f"{d.name}: invalid frontmatter");continue
    name=re.search(r"^name:\s*(.+)$",fm.group(1),re.M)
    desc=re.search(r"^description:\s*(.+)$",fm.group(1),re.M)
    if not name or name.group(1).strip()!=d.name:errors.append(f"{d.name}: name mismatch")
    if not desc:errors.append(f"{d.name}: missing description");continue
    description=desc.group(1).strip()
    if tok(description)>80:warnings.append(f"{d.name}: description ~{tok(description)} tokens")
    if tok(text)>900:warnings.append(f"{d.name}: SKILL.md ~{tok(text)} tokens")
    if len(description)<35:warnings.append(f"{d.name}: description may be too vague")
    refs=d/"references"
    actual={p.name for p in refs.glob("*.md")} if refs.exists() else set()
    mentioned=set(re.findall(r"`references/([^`]+\.md)`",text))
    missing=mentioned-actual
    orphan=actual-mentioned
    for x in sorted(missing):errors.append(f"{d.name}: missing referenced file {x}")
    for x in sorted(orphan):warnings.append(f"{d.name}: orphan reference {x}")

print(f"Skill lint: {len(errors)} errors, {len(warnings)} warnings")
for e in errors:print("ERROR:",e)
for x in warnings:print("WARN:",x)
raise SystemExit(1 if errors else 0)
