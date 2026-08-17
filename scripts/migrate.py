from __future__ import annotations
from pathlib import Path
import argparse,json,os,shutil
from datetime import datetime

CURRENT="1.0.0"

def major(v):
    try:return int(str(v).split(".",1)[0])
    except:return 0

def backup(path:Path):
    if path.exists():
        stamp=datetime.now().strftime("%Y%m%d-%H%M%S")
        dest=path.with_name(path.name+f".pre-v1-{stamp}.bak")
        shutil.copy2(path,dest)
        print("Backup:",dest)
        return dest

def normalize_project(data:dict)->tuple[dict,list[str]]:
    out=dict(data)
    old=str(out.get("packVersion","0.0.0"))
    changes=[]
    out.setdefault("schemaVersion",1)
    if "createdFiles" not in out:
        out["createdFiles"]=[];changes.append("add createdFiles")
    if "skillHashes" not in out:
        out["skillHashes"]={};changes.append("add skillHashes placeholder")
    out.setdefault("includeCore",False)
    out.setdefault("target","both")
    out.setdefault("skills",[])
    if old!=CURRENT:
        out["packVersion"]=CURRENT;changes.append(f"packVersion {old} -> {CURRENT}")
    return out,changes

def normalize_global(data:dict)->tuple[dict,list[str]]:
    out=dict(data)
    old=str(out.get("packVersion","0.0.0"))
    changes=[]
    out.setdefault("schemaVersion",1)
    if "thirdPartyInstalledByPack" not in out:
        out["thirdPartyInstalledByPack"]=False;changes.append("add thirdPartyInstalledByPack")
    if "recommendedThirdPartySkills" not in out:
        out["recommendedThirdPartySkills"]=["ui-ux-pro-max","web-quality-audit"];changes.append("add recommendedThirdPartySkills")
    out.setdefault("firstPartySkills",[])
    out.setdefault("target","both")
    out.setdefault("profile","core")
    if old!=CURRENT:
        out["packVersion"]=CURRENT;changes.append(f"packVersion {old} -> {CURRENT}")
    return out,changes

def migrate_project(path:Path,apply:bool):
    mf=path/".web-engineering-agent-pack.json"
    if not mf.exists():
        print("No project manifest found:",mf);return 0
    try:data=json.loads(mf.read_text(encoding="utf-8"))
    except Exception as e:raise SystemExit(f"Invalid project manifest: {e}")
    migrated,changes=normalize_project(data)
    if not changes:
        print("Project manifest already current.");return 0
    print("Project migration plan:")
    for c in changes:print("-",c)
    if apply:
        backup(mf);mf.write_text(json.dumps(migrated,indent=2)+"\n",encoding="utf-8");print("Applied.")
    else:print("Preview only. Re-run with --apply.")
    return 0

def migrate_global(apply:bool):
    home=Path.home()
    sf=Path(os.environ.get("AI_AGENT_PACK_STATE_FILE",home/".ai-agent-pack-state.json"))
    if not sf.exists():
        print("No global install state found:",sf);return 0
    try:data=json.loads(sf.read_text(encoding="utf-8"))
    except Exception as e:raise SystemExit(f"Invalid global install state: {e}")
    migrated,changes=normalize_global(data)
    if not changes:
        print("Global state already current.");return 0
    print("Global migration plan:")
    for c in changes:print("-",c)
    if apply:
        backup(sf);sf.write_text(json.dumps(migrated,indent=2)+"\n",encoding="utf-8");print("Applied.")
    else:print("Preview only. Re-run with --apply.")
    return 0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-dir",default=".")
    ap.add_argument("--global-state",action="store_true")
    ap.add_argument("--apply",action="store_true")
    a=ap.parse_args()
    return migrate_global(a.apply) if a.global_state else migrate_project(Path(a.project_dir).expanduser().resolve(),a.apply)

if __name__=="__main__":
    raise SystemExit(main())
