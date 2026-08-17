from __future__ import annotations
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
PACK=json.loads((ROOT/"manifest.json").read_text(encoding="utf-8"))
spec=importlib.util.spec_from_file_location("pm",ROOT/"scripts/profile_manager.py")
pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)

LOCK_NAME=".web-engineering-agent-pack.lock.json"
MCP_STATE_NAME=".web-engineering-agent-pack.mcp.json"

def mcp_lock_data(project: Path):
    p=project/MCP_STATE_NAME
    if not p.exists():
        return None
    data=json.loads(p.read_text(encoding="utf-8"))
    return {
        "scope":"project",
        "servers":{
            name:{
                "definitionHash":meta.get("definitionHash"),
                "targets":meta.get("targets",[]),
                "enabled":meta.get("enabled",True)
            }
            for name,meta in sorted(data.get("servers",{}).items())
        }
    }


def source_skill_hash(skill: str) -> str:
    return pm.hash_tree(ROOT/"shared"/"skills"/skill)

def write_lock(project: Path):
    mf=project/".web-engineering-agent-pack.json"
    if not mf.exists():
        raise SystemExit("Project is not managed by WEAP; install a profile first.")
    data=json.loads(mf.read_text(encoding="utf-8"))
    skills=data.get("skills",[])
    lock={
        "schemaVersion":1,
        "packVersion":PACK["version"],
        "profile":data["profile"],
        "includeCore":data.get("includeCore",False),
        "target":data.get("target","both"),
        "skills":skills,
        "sourceSkillHashes":{s:source_skill_hash(s) for s in skills},
        "mcp":mcp_lock_data(project),
    }
    (project/LOCK_NAME).write_text(json.dumps(lock,indent=2)+"\n",encoding="utf-8")
    print("Project lock written:",project/LOCK_NAME)

def verify(project: Path) -> int:
    lp=project/LOCK_NAME
    if not lp.exists():
        print("Missing project lock:",lp)
        return 1
    lock=json.loads(lp.read_text(encoding="utf-8"))
    errors=[]
    if lock.get("packVersion")!=PACK["version"]:
        errors.append(f"packVersion locked={lock.get('packVersion')} current={PACK['version']}")
    expected=lock.get("sourceSkillHashes",{})
    for skill,h in expected.items():
        if not (ROOT/"shared"/"skills"/skill).exists():
            errors.append(f"missing source skill: {skill}")
        elif source_skill_hash(skill)!=h:
            errors.append(f"source skill hash mismatch: {skill}")
    resolved=pm.resolve_profile(lock["profile"])
    if not lock.get("includeCore",False):
        core=set(pm.resolve_profile("core"))
        resolved=[s for s in resolved if s not in core]
    if set(resolved)!=set(lock.get("skills",[])):
        errors.append("resolved profile no longer matches locked skill set")
    locked_mcp=lock.get("mcp")
    current_mcp=mcp_lock_data(project)
    if locked_mcp != current_mcp:
        errors.append("project MCP state does not match the lockfile")
    if errors:
        print("Project lock verification FAILED")
        for e in errors: print("-",e)
        return 1
    print("Project lock verification OK.")
    return 0

def apply(project: Path, force: bool):
    if verify(project):
        raise SystemExit("Cannot apply an invalid lock.")
    lock=json.loads((project/LOCK_NAME).read_text(encoding="utf-8"))
    args=SimpleNamespace(
        project_dir=str(project),profile=lock["profile"],include_core=lock.get("includeCore",False),
        add_skill=[],remove_skill=[],target=lock.get("target","both"),init_project=False,
        dry_run=False,force=force
    )
    pm.install_project(args)
    print("Locked skill configuration applied.")
    if lock.get("mcp"):
        print("MCP capabilities are recorded in the lock but are not auto-granted.")
        print("Install the required MCP servers explicitly with `weap mcp install`, then run project verify.")

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)
    for name in ["write","verify"]:
        p=sub.add_parser(name);p.add_argument("--project-dir",default=".")
    p=sub.add_parser("apply");p.add_argument("--project-dir",default=".");p.add_argument("--force",action="store_true")
    a=ap.parse_args()
    project=Path(a.project_dir).expanduser().resolve()
    if a.cmd=="write": write_lock(project)
    elif a.cmd=="verify": raise SystemExit(verify(project))
    else: apply(project,a.force)

if __name__=="__main__":
    main()
