from pathlib import Path
import argparse,json,shutil

def remove(path: Path, dry: bool):
    if not path.exists(): return
    print("remove:",path)
    if not dry:
        shutil.rmtree(path) if path.is_dir() else path.unlink()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-dir",default=".")
    ap.add_argument("--target",choices=["both","codex","claude"],default="both")
    ap.add_argument("--remove-ai-config",action="store_true")
    ap.add_argument("--dry-run",action="store_true")
    a=ap.parse_args()

    if a.remove_ai_config and a.target!="both":
        raise SystemExit("--remove-ai-config requires --target=both because AGENTS.md is shared across agent configurations.")

    project=Path(a.project_dir).expanduser().resolve()
    mf=project/".web-engineering-agent-pack.json"
    if not mf.exists():
        raise SystemExit(f"No pack project manifest found: {mf}")
    data=json.loads(mf.read_text(encoding="utf-8"))
    skills=data.get("skills",[])

    if a.target in {"both","codex"}:
        for s in skills: remove(project/".agents"/"skills"/s,a.dry_run)
    if a.target in {"both","claude"}:
        for s in skills: remove(project/".claude"/"skills"/s,a.dry_run)

    if a.remove_ai_config:
        allowed={
            "AGENTS.md","CLAUDE.md",".codex/config.toml",".claude/settings.json",
            ".agents/skills/project-domain",".claude/skills/project-domain"
        }
        for rel in data.get("createdFiles",[]):
            if rel in allowed: remove(project/rel,a.dry_run)

    current_target=data.get("target","both")
    if a.target=="both" or current_target==a.target:
        print("remove:",mf)
        if not a.dry_run: mf.unlink(missing_ok=True)
    elif current_target=="both":
        remaining="claude" if a.target=="codex" else "codex"
        print(f"update manifest target -> {remaining}")
        if not a.dry_run:
            data["target"]=remaining
            mf.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    else:
        print(f"manifest target remains {current_target}; requested target {a.target} was not the remaining managed target")

    print("Project uninstall complete. Unmanaged/custom project skills were preserved.")

if __name__=="__main__":
    main()
