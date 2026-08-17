from __future__ import annotations
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]

def executable(name):
    return shutil.which(name)

def version(cmd):
    try:
        return subprocess.run(cmd,text=True,capture_output=True,timeout=5).stdout.strip() or subprocess.run(cmd,text=True,capture_output=True,timeout=5).stderr.strip()
    except Exception:
        return None

def check_path(path: Path, kind="path"):
    return {"name":str(path),"kind":kind,"exists":path.exists(),"writable":os.access(path if path.exists() else path.parent,os.W_OK)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project-dir")
    ap.add_argument("--json",action="store_true")
    a=ap.parse_args()

    home=Path.home()
    codex=Path(os.environ.get("CODEX_HOME",home/".codex"))
    claude=Path(os.environ.get("CLAUDE_CONFIG_DIR",home/".claude"))
    state=Path(os.environ.get("AI_AGENT_PACK_STATE_FILE",home/".ai-agent-pack-state.json"))

    checks=[]
    py3=executable("python3")
    py=executable("python")
    checks.append({
        "category":"binary","name":"python-runtime",
        "ok":bool(py3 or py),"path":py3 or py
    })

    optional_bins=["git","node","npx"]
    for name in optional_bins:
        path=executable(name)
        checks.append({"category":"binary","name":name,"ok":bool(path),"path":path,"optional":True})

    if os.name=="nt":
        path=executable("pwsh") or executable("powershell")
        checks.append({"category":"binary","name":"powershell","ok":bool(path),"path":path})
        bash=executable("bash")
        checks.append({"category":"binary","name":"bash","ok":bool(bash),"path":bash,"optional":True})
    else:
        bash=executable("bash")
        checks.append({"category":"binary","name":"bash","ok":bool(bash),"path":bash})
        pwsh=executable("pwsh")
        checks.append({"category":"binary","name":"pwsh","ok":bool(pwsh),"path":pwsh,"optional":True})


    checks += [
        {"category":"path",**check_path(codex,"codex-home"),"ok":os.access(codex if codex.exists() else codex.parent,os.W_OK)},
        {"category":"path",**check_path(claude,"claude-home"),"ok":os.access(claude if claude.exists() else claude.parent,os.W_OK)},
        {"category":"state","name":str(state),"ok":state.exists(),"optional":True},
    ]

    if state.exists():
        try:
            data=json.loads(state.read_text())
            checks.append({"category":"state","name":"install-state-json","ok":data.get("packVersion") is not None,"value":data})
        except Exception as e:
            checks.append({"category":"state","name":"install-state-json","ok":False,"error":str(e)})

    if a.project_dir:
        p=Path(a.project_dir).expanduser().resolve()
        checks.append({"category":"project","name":str(p),"ok":p.exists()})
        manifest=p/".web-engineering-agent-pack.json"
        lock=p/".web-engineering-agent-pack.lock.json"
        checks.append({"category":"project","name":"project-manifest","ok":manifest.exists(),"optional":True})
        checks.append({"category":"project","name":"project-lock","ok":lock.exists(),"optional":True})
        mcp_state=p/".web-engineering-agent-pack.mcp.json"
        checks.append({"category":"mcp","name":"mcp-project-state","ok":mcp_state.exists(),"optional":True})
        if mcp_state.exists():
            r=subprocess.run([sys.executable,str(ROOT/"mcp_manager.py"),"doctor","--scope","project","--project-dir",str(p)],text=True,capture_output=True,timeout=15)
            checks.append({
                "category":"mcp","name":"mcp-project-doctor",
                "ok":r.returncode==0,"optional":True,
                "value":r.stdout.strip(),"error":r.stderr.strip() if r.returncode else None
            })

        try:
            r=subprocess.run([sys.executable,str(ROOT/"profile_manager.py"),"detect","--project-dir",str(p),"--json"],text=True,capture_output=True,timeout=10)
            if r.returncode==0:
                checks.append({"category":"project","name":"stack-detection","ok":True,"value":json.loads(r.stdout)})
            else:
                checks.append({"category":"project","name":"stack-detection","ok":False,"error":r.stderr.strip()})
        except Exception as e:
            checks.append({"category":"project","name":"stack-detection","ok":False,"error":str(e)})

    required_fail=[c for c in checks if not c.get("ok") and not c.get("optional")]
    result={"ok":not required_fail,"checks":checks}

    if a.json:
        print(json.dumps(result,indent=2))
    else:
        print("WEAP Doctor")
        print("="*72)
        for c in checks:
            status="OK" if c.get("ok") else ("OPTIONAL" if c.get("optional") else "FAIL")
            print(f"[{status:8}] {c['category']}: {c['name']}")
            if c.get("error"): print("          ",c["error"])
        print()
        print("Overall:", "OK" if result["ok"] else "NEEDS ATTENTION")

    return 0 if result["ok"] else 1

if __name__=="__main__":
    raise SystemExit(main())
