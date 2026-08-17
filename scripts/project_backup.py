from pathlib import Path
import argparse,json,shutil,sys,importlib.util,re

ROOT=Path(__file__).resolve().parents[1]
BACKUP_RE=re.compile(r"^[0-9]{8}-[0-9]{6}(?:-[0-9]+)?$")
spec=importlib.util.spec_from_file_location("pm",ROOT/"scripts/profile_manager.py")
pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)

def backup_root(project: Path) -> Path:
    return project/".web-engineering-agent-pack-backups"

def list_backups(project: Path):
    root=backup_root(project)
    if not root.exists():
        print("No project backups.")
        return
    for d in sorted((x for x in root.iterdir() if x.is_dir()),reverse=True):
        mf=d/"manifest.json"
        profile="?"
        version="?"
        if mf.exists():
            try:
                data=json.loads(mf.read_text())
                profile=data.get("profile","?")
                version=data.get("packVersion","?")
            except Exception: pass
        print(f"{d.name}\tprofile={profile}\tpack={version}")

def restore(project: Path,name: str):
    root=backup_root(project)
    if name=="latest":
        dirs=sorted((x for x in root.iterdir() if x.is_dir()),reverse=True) if root.exists() else []
        if not dirs: raise SystemExit("No project backups.")
        src=dirs[0]
    else:
        if not BACKUP_RE.fullmatch(name):
            raise SystemExit(f"Invalid backup name: {name}")
        src=root/name
    mf=src/"manifest.json"
    if not mf.exists():
        raise SystemExit(f"Invalid project backup: {src}")
    old=json.loads(mf.read_text())

    current=pm.read_project_manifest(project)
    safety=pm.create_project_backup(project,current)
    if safety:
        print("Current project skills backed up:",safety)

    pm.remove_managed_project_skills(project,current)

    for label,target in [
        ("codex",project/".agents"/"skills"),
        ("claude",project/".claude"/"skills")
    ]:
        source=src/label/"skills"
        if source.exists():
            target.mkdir(parents=True,exist_ok=True)
            for skill in source.iterdir():
                if skill.is_dir():
                    dst=target/skill.name
                    if dst.exists(): shutil.rmtree(dst)
                    shutil.copytree(skill,dst)

    # Recalculate hashes for the restored skill set.
    old["skillHashes"]=pm.current_managed_hashes(
        project,old.get("skills",[]),old.get("target","both")
    )
    (project/".web-engineering-agent-pack.json").write_text(
        json.dumps(old,indent=2)+"\n",encoding="utf-8"
    )
    print("Project backup restored:",src.name)

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("list");p.add_argument("--project-dir",default=".")
    p=sub.add_parser("restore");p.add_argument("backup");p.add_argument("--project-dir",default=".")
    a=ap.parse_args()
    project=Path(a.project_dir).expanduser().resolve()
    if a.cmd=="list": list_backups(project)
    else: restore(project,a.backup)

if __name__=="__main__":
    main()
