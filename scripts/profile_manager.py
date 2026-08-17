from __future__ import annotations

from pathlib import Path
import argparse
import json
import re
import shutil
import sys
import hashlib
from datetime import datetime
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "profiles"
SKILLS = ROOT / "shared" / "skills"
PACK_VERSION = "1.0.0"
PROFILE_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

def load_profile(name: str) -> dict:
    if not PROFILE_NAME_RE.fullmatch(name):
        raise SystemExit(f"Invalid profile name: {name}")
    p = PROFILES / f"{name}.json"
    if not p.exists():
        raise SystemExit(f"Unknown profile: {name}")
    return json.loads(p.read_text(encoding="utf-8"))

def resolve_profile(name: str, *, include_extends: bool = True, seen=None) -> list[str]:
    seen = set() if seen is None else seen
    if name in seen:
        raise SystemExit(f"Cyclic profile dependency involving {name}")
    seen.add(name)
    data = load_profile(name)
    skills: list[str] = []
    if include_extends:
        for parent in data.get("extends", []):
            for skill in resolve_profile(parent, include_extends=True, seen=set(seen)):
                if skill not in skills:
                    skills.append(skill)
    for skill in data.get("skills", []):
        if skill not in skills:
            skills.append(skill)
    for skill in data.get("removeSkills", []):
        if skill in skills:
            skills.remove(skill)
    return skills

def resolve_stack_only(name: str) -> list[str]:
    # "Project profile" means the delta beyond CORE. This keeps CORE global.
    all_skills = resolve_profile(name)
    core = set(resolve_profile("core"))
    if name == "core":
        return all_skills
    return [s for s in all_skills if s not in core]

def apply_overrides(skills: list[str], add: Iterable[str], remove: Iterable[str]) -> list[str]:
    out = list(skills)
    for skill in add:
        if not skill:
            continue
        if not (SKILLS / skill / "SKILL.md").exists():
            raise SystemExit(f"Unknown skill requested with --add-skill: {skill}")
        if skill not in out:
            out.append(skill)
    for skill in remove:
        if skill in out:
            out.remove(skill)
    return out

def validate_profile(name: str) -> list[str]:
    skills = resolve_profile(name)
    missing = [s for s in skills if not (SKILLS / s / "SKILL.md").exists()]
    if missing:
        raise SystemExit(f"Profile {name} references missing skills: {', '.join(missing)}")
    return skills

def detect(project: Path) -> dict:
    result = {
        "project": str(project.resolve()),
        "profiles": [],
        "signals": [],
        "recommendedProfile": None,
        "database": None,
        "orm": None,
    }

    package = project / "package.json"
    if package.exists():
        try:
            data = json.loads(package.read_text(encoding="utf-8"))
            deps = {}
            deps.update(data.get("dependencies", {}))
            deps.update(data.get("devDependencies", {}))
            if "next" in deps:
                result["profiles"].append("nextjs")
                result["signals"].append("package.json contains next")
            if "prisma" in deps or "@prisma/client" in deps:
                result["orm"] = "prisma"
                result["signals"].append("package.json contains Prisma")
        except Exception:
            result["signals"].append("package.json exists but could not be parsed")

    composer = project / "composer.json"
    if composer.exists():
        try:
            data = json.loads(composer.read_text(encoding="utf-8"))
            deps = {}
            deps.update(data.get("require", {}))
            deps.update(data.get("require-dev", {}))
            if "symfony/framework-bundle" in deps or any(k.startswith("symfony/") for k in deps):
                result["profiles"].append("symfony")
                result["signals"].append("composer.json contains Symfony packages")
            if "doctrine/orm" in deps or "doctrine/doctrine-bundle" in deps:
                result["orm"] = "doctrine"
                result["signals"].append("composer.json contains Doctrine")
        except Exception:
            result["signals"].append("composer.json exists but could not be parsed")

    prisma_schema = project / "prisma" / "schema.prisma"
    if prisma_schema.exists():
        txt = prisma_schema.read_text(encoding="utf-8", errors="ignore")
        datasource = re_search(r'datasource\s+\w+\s*\{(.*?)\}', txt, flags="s")
        m = re_search(r'provider\s*=\s*"([^"]+)"', datasource.group(1) if datasource else "")
        if m:
            provider = m.group(1).lower()
            if provider in {"mysql", "postgresql"}:
                result["database"] = provider
                result["signals"].append(f"Prisma provider is {provider}")

    doctrine_candidates = [
        project / "config" / "packages" / "doctrine.yaml",
        project / "config" / "packages" / "doctrine.yml",
    ]
    for candidate in doctrine_candidates:
        if candidate.exists():
            txt = candidate.read_text(encoding="utf-8", errors="ignore").lower()
            if "mysql" in txt or "mariadb" in txt:
                result["database"] = "mysql"
                result["signals"].append(f"{candidate.relative_to(project)} references MySQL/MariaDB")
            elif "postgresql" in txt or "postgres" in txt:
                result["database"] = "postgresql"
                result["signals"].append(f"{candidate.relative_to(project)} references PostgreSQL")
            break

    profiles = sorted(set(result["profiles"]))
    result["profiles"] = profiles
    if profiles == ["nextjs"]:
        result["recommendedProfile"] = "nextjs-mysql" if result["database"] == "mysql" else "nextjs"
    elif profiles == ["symfony"]:
        result["recommendedProfile"] = "symfony-postgresql" if result["database"] == "postgresql" else "symfony"
    elif len(profiles) > 1:
        result["recommendedProfile"] = "full"

    return result

def re_search(pattern: str, text: str, flags: str = ""):
    import re
    value = 0
    if "s" in flags:
        value |= re.S
    if "i" in flags:
        value |= re.I
    return re.search(pattern, text, value)

def copy_skill(skill: str, destination_root: Path):
    src = SKILLS / skill
    dst = destination_root / skill
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def hash_tree(path: Path) -> str:
    h=hashlib.sha256()
    if not path.exists():
        return h.hexdigest()
    for p in sorted(x for x in path.rglob("*") if x.is_file()):
        h.update(str(p.relative_to(path)).encode())
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return h.hexdigest()

def current_managed_hashes(project: Path, managed: list[str], target: str) -> dict[str,str]:
    out={}
    roots=[]
    if target in {"both","codex"}:
        roots.append(("codex", project/".agents"/"skills"))
    if target in {"both","claude"}:
        roots.append(("claude", project/".claude"/"skills"))
    for label,base in roots:
        for skill in managed:
            p=base/skill
            if p.exists():
                out[f"{label}:{skill}"]=hash_tree(p)
    return out

def create_project_backup(project: Path, old: dict) -> Path | None:
    managed=old.get("skills",[])
    if not managed:
        return None
    backup_root=project/".web-engineering-agent-pack-backups"
    stamp=datetime.now().strftime("%Y%m%d-%H%M%S")
    dest=backup_root/stamp
    suffix=0
    while dest.exists():
        suffix+=1
        dest=backup_root/f"{stamp}-{suffix}"
    dest.mkdir(parents=True)
    manifest=project/".web-engineering-agent-pack.json"
    if manifest.exists():
        shutil.copy2(manifest,dest/"manifest.json")
    for label,base in [("codex",project/".agents"/"skills"),("claude",project/".claude"/"skills")]:
        for skill in managed:
            src=base/skill
            if src.exists():
                target=dest/label/"skills"/skill
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copytree(src,target)
    return dest

def assert_unmodified_managed_skills(project: Path, old: dict, force: bool):
    recorded=old.get("skillHashes",{})
    if not recorded:
        return
    target=old.get("target","both")
    current=current_managed_hashes(project,old.get("skills",[]),target)
    changed=[]
    for key,expected in recorded.items():
        actual=current.get(key)
        if actual is not None and actual != expected:
            changed.append(key)
    if changed and not force:
        raise SystemExit(
            "Pack-managed project skills were modified locally: "
            + ", ".join(changed)
            + ". Refusing overwrite. Re-run with --force after reviewing or copy changes to a custom skill."
        )

def read_project_manifest(project: Path) -> dict:
    p = project / ".web-engineering-agent-pack.json"
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def safe_remove_managed_path(path: Path):
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()

def remove_managed_project_skills(project: Path, old: dict):
    managed = old.get("skills", [])
    for skill in managed:
        for base in [project / ".agents" / "skills", project / ".claude" / "skills"]:
            target = base / skill
            if target.exists():
                safe_remove_managed_path(target)

def initialize_project_files(project: Path, profile: str) -> list[str]:
    template = ROOT / "project-template"
    created: list[str] = []
    profile_snippet = template / "profiles" / profile / "AGENTS.stack.md"
    if not profile_snippet.exists():
        if profile.startswith("nextjs"):
            profile_snippet = template / "profiles" / "nextjs" / "AGENTS.stack.md"
        elif profile.startswith("symfony"):
            profile_snippet = template / "profiles" / "symfony" / "AGENTS.stack.md"

    agents = project / "AGENTS.md"
    if not agents.exists():
        base = (template / "AGENTS.base.md").read_text(encoding="utf-8")
        snippet = profile_snippet.read_text(encoding="utf-8") if profile_snippet.exists() else ""
        agents.write_text(base.replace("{{PROFILE}}", profile) + "\n\n" + snippet.strip() + "\n", encoding="utf-8")
        created.append("AGENTS.md")

    claude = project / "CLAUDE.md"
    if not claude.exists():
        claude.write_text("@AGENTS.md\n\n# Claude Code\n\nUse project-local skills matching this repository profile.\n", encoding="utf-8")
        created.append("CLAUDE.md")

    codex_config = project / ".codex" / "config.toml"
    if not codex_config.exists():
        codex_config.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template / ".codex" / "config.toml", codex_config)
        created.append(".codex/config.toml")

    claude_settings = project / ".claude" / "settings.json"
    if not claude_settings.exists():
        claude_settings.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(template / ".claude" / "settings.json", claude_settings)
        created.append(".claude/settings.json")

    domain_source_codex = template / ".agents" / "skills" / "project-domain"
    domain_target_codex = project / ".agents" / "skills" / "project-domain"
    if domain_source_codex.exists() and not domain_target_codex.exists():
        domain_target_codex.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(domain_source_codex, domain_target_codex)
        created.append(".agents/skills/project-domain")

    domain_source_claude = template / ".claude" / "skills" / "project-domain"
    domain_target_claude = project / ".claude" / "skills" / "project-domain"
    if domain_source_claude.exists() and not domain_target_claude.exists():
        domain_target_claude.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(domain_source_claude, domain_target_claude)
        created.append(".claude/skills/project-domain")

    return created

def install_project(args):
    project = Path(args.project_dir).expanduser().resolve()
    if not project.exists():
        raise SystemExit(f"Project directory does not exist: {project}")

    skills = resolve_profile(args.profile) if args.include_core else resolve_stack_only(args.profile)
    skills = apply_overrides(skills, args.add_skill, args.remove_skill)
    for skill in skills:
        if not (SKILLS / skill / "SKILL.md").exists():
            raise SystemExit(f"Missing skill source: {skill}")

    old = read_project_manifest(project)
    assert_unmodified_managed_skills(project, old, args.force)
    if args.dry_run:
        old_skills=set(old.get("skills", []))
        new_skills=set(skills)
        added=sorted(new_skills-old_skills)
        removed=sorted(old_skills-new_skills)
        retained=sorted(old_skills&new_skills)
        potentially_updated=retained if old.get("packVersion") not in {None, PACK_VERSION} else []
        print(f"Project: {project}")
        print(f"Profile: {args.profile}")
        print(f"Include CORE: {args.include_core}")
        print(f"Current pack version: {old.get('packVersion','(none)')}")
        print(f"Target pack version: {PACK_VERSION}")
        print("Added:", ", ".join(added) or "(none)")
        print("Removed:", ", ".join(removed) or "(none)")
        print("Retained:", ", ".join(retained) or "(none)")
        print("Potentially updated:", ", ".join(potentially_updated) or "(none)")
        print("Custom/unmanaged project skills are preserved.")
        print("No files are changed in dry-run mode.")
        return

    backup = create_project_backup(project, old)
    if backup:
        print(f"Project skill backup: {backup}")
    remove_managed_project_skills(project, old)
    targets = []
    if args.target in {"both", "codex"}:
        targets.append(project / ".agents" / "skills")
    if args.target in {"both", "claude"}:
        targets.append(project / ".claude" / "skills")

    for target in targets:
        target.mkdir(parents=True, exist_ok=True)
        for skill in skills:
            copy_skill(skill, target)

    if args.target in {"both", "claude"}:
        # Apply manual-only metadata only to Claude copies.
        overlay = ROOT / "scripts" / "install-claude-skill-overlays.py"
        if overlay.exists():
            import subprocess
            subprocess.run([sys.executable, str(overlay), str(project / ".claude" / "skills")], check=True)

    created_files = list(old.get("createdFiles", []))
    if args.init_project:
        for rel in initialize_project_files(project, args.profile):
            if rel not in created_files:
                created_files.append(rel)

    skill_hashes = current_managed_hashes(project, skills, args.target)
    manifest = {
        "schemaVersion": 1,
        "packVersion": PACK_VERSION,
        "profile": args.profile,
        "includeCore": args.include_core,
        "target": args.target,
        "skills": skills,
        "createdFiles": created_files,
        "skillHashes": skill_hashes,
    }
    (project / ".web-engineering-agent-pack.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Installed project profile '{args.profile}' in {project}")
    print(f"Skills: {len(skills)}")

def main():
    parser = argparse.ArgumentParser(description="Web Engineering Agent Pack profile manager")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list")
    p.set_defaults(fn=lambda a: [
        print(f"{f.stem:20} {json.loads(f.read_text(encoding='utf-8')).get('description','')}")
        for f in sorted(PROFILES.glob("*.json")) if f.stem != "catalog"
    ])

    p = sub.add_parser("resolve")
    p.add_argument("--profile", required=True)
    p.add_argument("--stack-only", action="store_true")
    p.add_argument("--add-skill", action="append", default=[])
    p.add_argument("--remove-skill", action="append", default=[])
    def resolve_cmd(a):
        skills = resolve_stack_only(a.profile) if a.stack_only else validate_profile(a.profile)
        skills = apply_overrides(skills, a.add_skill, a.remove_skill)
        print("\n".join(skills))
    p.set_defaults(fn=resolve_cmd)

    p = sub.add_parser("detect")
    p.add_argument("--project-dir", default=".")
    p.add_argument("--json", action="store_true")
    def detect_cmd(a):
        data = detect(Path(a.project_dir).expanduser())
        if a.json:
            print(json.dumps(data, indent=2))
        else:
            print(f"Recommended profile: {data['recommendedProfile'] or 'unknown'}")
            print(f"Detected ORM: {data['orm'] or 'unknown'}")
            print(f"Detected database: {data['database'] or 'unknown'}")
            for s in data["signals"]:
                print("-", s)
    p.set_defaults(fn=detect_cmd)

    p = sub.add_parser("install-project")
    p.add_argument("--profile", required=True)
    p.add_argument("--project-dir", default=".")
    p.add_argument("--target", choices=["both", "codex", "claude"], default="both")
    p.add_argument("--include-core", action="store_true")
    p.add_argument("--add-skill", action="append", default=[])
    p.add_argument("--remove-skill", action="append", default=[])
    p.add_argument("--init-project", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true", help="Overwrite locally modified pack-managed project skills.")
    p.set_defaults(fn=install_project)

    args = parser.parse_args()
    result = args.fn(args)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
