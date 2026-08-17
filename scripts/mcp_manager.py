from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from typing import Iterable

ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"mcp"/"registry"
PROFILES=ROOT/"mcp"/"profiles"
PACK_VERSION="1.0.0"

START="# >>> WEAP MCP MANAGED BLOCK >>>"
END="# <<< WEAP MCP MANAGED BLOCK <<<"
NAME_RE=re.compile(r"^[a-z0-9][a-z0-9-]*$")
RISK_ORDER={"low":0,"medium":1,"high":2,"critical":3}

def canonical_json(data)->bytes:
    return json.dumps(data,sort_keys=True,separators=(",",":")).encode()

def definition_hash(data)->str:
    return hashlib.sha256(canonical_json(data)).hexdigest()

def load_server(name:str)->dict:
    if not NAME_RE.fullmatch(name):
        raise SystemExit(f"Invalid MCP server name: {name}")
    p=REGISTRY/f"{name}.json"
    if not p.exists():
        raise SystemExit(f"Unknown MCP server: {name}")
    return json.loads(p.read_text(encoding="utf-8"))

def load_profile(name:str)->dict:
    if not NAME_RE.fullmatch(name):
        raise SystemExit(f"Invalid MCP profile name: {name}")
    p=PROFILES/f"{name}.json"
    if not p.exists():
        raise SystemExit(f"Unknown MCP profile: {name}")
    return json.loads(p.read_text(encoding="utf-8"))

def state_path(scope:str,project:Path)->Path:
    return project/".web-engineering-agent-pack.mcp.json" if scope=="project" else Path.home()/".weap-mcp-state.json"

def read_state(scope:str,project:Path)->dict:
    p=state_path(scope,project)
    if not p.exists():
        return {"schemaVersion":1,"packVersion":PACK_VERSION,"scope":scope,"servers":{}}
    try:
        data=json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"Invalid MCP state file {p}: {e}")
    data.setdefault("servers",{})
    return data

def write_state(scope:str,project:Path,data:dict):
    p=state_path(scope,project)
    data["schemaVersion"]=1
    data["packVersion"]=PACK_VERSION
    data["scope"]=scope
    p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+".tmp")
    tmp.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    tmp.replace(p)

def resolve_names(server_names:list[str],profile_names:list[str])->list[str]:
    out=[]
    for profile in profile_names:
        for name in load_profile(profile)["servers"]:
            if name not in out: out.append(name)
    for name in server_names:
        load_server(name)
        if name not in out: out.append(name)
    return out

def project_arg(value:str|None)->Path:
    return Path(value or ".").expanduser().resolve()

def require_allowed(server:dict,scope:str,project:Path,allow_high:bool):
    if not server.get("installable",False):
        raise SystemExit(f"MCP server '{server['name']}' is a template and cannot be installed directly.")
    risk=server["risk"]
    if RISK_ORDER[risk]>=RISK_ORDER["high"] and not allow_high:
        raise SystemExit(
            f"MCP server '{server['name']}' is {risk} risk. "
            "Review the definition and re-run with --allow-high-risk."
        )
    if server.get("projectRequired") and scope!="project":
        raise SystemExit(
            f"MCP server '{server['name']}' is project-bound and cannot be installed at user scope."
        )

def toml_string(value:str)->str:
    return json.dumps(value,ensure_ascii=False)

def expand_arg(arg:str,client:str,scope:str,project:Path)->str:
    if arg!="${PROJECT_DIR}":
        return arg
    if scope!="project":
        raise SystemExit("${PROJECT_DIR} requires project scope.")
    if client=="claude":
        return "${CLAUDE_PROJECT_DIR:-.}"
    return str(project)

def render_codex_server(server:dict,scope:str,project:Path,enabled:bool)->str:
    name=server["name"]
    lines=[f"[mcp_servers.{name}]"]
    if server["transport"]=="stdio":
        lines.append(f"command = {toml_string(server['command'])}")
        args=[expand_arg(x,"codex",scope,project) for x in server.get("args",[])]
        if args:
            lines.append("args = ["+", ".join(toml_string(x) for x in args)+"]")
        req=server.get("requiredEnv",[])
        if req:
            lines.append("env_vars = ["+", ".join(toml_string(x) for x in req)+"]")
    else:
        lines.append(f"url = {toml_string(server['url'])}")
        if server.get("bearerTokenEnvVar"):
            lines.append(f"bearer_token_env_var = {toml_string(server['bearerTokenEnvVar'])}")
        headers=server.get("envHttpHeaders",{})
        if headers:
            pairs=", ".join(f"{toml_string(k)} = {toml_string(v)}" for k,v in headers.items())
            lines.append(f"env_http_headers = {{ {pairs} }}")
    lines.append(f"enabled = {'true' if enabled else 'false'}")
    lines.append("required = false")
    lines.append(f"default_tools_approval_mode = {toml_string(server.get('defaultApprovalMode','prompt'))}")
    if server.get("enabledTools"):
        lines.append("enabled_tools = ["+", ".join(toml_string(x) for x in server["enabledTools"])+"]")
    if server.get("disabledTools"):
        lines.append("disabled_tools = ["+", ".join(toml_string(x) for x in server["disabledTools"])+"]")
    return "\n".join(lines)

def remove_managed_block(text:str)->str:
    pattern=re.compile(re.escape(START)+r".*?"+re.escape(END)+r"\n?",re.S)
    return pattern.sub("",text).rstrip()+"\n"

def codex_config_path(scope:str,project:Path)->Path:
    if scope=="project":
        return project/".codex"/"config.toml"
    return Path(os.environ.get("CODEX_HOME",str(Path.home()/".codex")))/"config.toml"

def apply_codex(scope:str,project:Path,state:dict,previous_managed:set[str],force:bool):
    path=codex_config_path(scope,project)
    path.parent.mkdir(parents=True,exist_ok=True)
    original=path.read_text(encoding="utf-8") if path.exists() else ""
    outside=remove_managed_block(original)
    desired=[
        name for name,meta in state["servers"].items()
        if "codex" in meta.get("targets",[])
    ]
    for name in desired:
        if re.search(rf"(?m)^\[mcp_servers\.{re.escape(name)}\]\s*$",outside):
            if name not in previous_managed and not force:
                raise SystemExit(
                    f"Codex config already contains unmanaged MCP server '{name}'. "
                    "Use --force only if WEAP should take ownership."
                )
            if force:
                raise SystemExit(
                    f"Cannot safely replace unmanaged Codex table '{name}' automatically. "
                    "Remove that table manually, then re-run."
                )
    blocks=[]
    for name in sorted(desired):
        server=load_server(name)
        blocks.append(render_codex_server(server,scope,project,state["servers"][name].get("enabled",True)))
    managed=""
    if blocks:
        managed=START+"\n"+"\n\n".join(blocks)+"\n"+END+"\n"
    final=outside.rstrip()
    if final: final+="\n\n"
    final+=managed
    tmp=path.with_name(path.name+".weap.tmp")
    tmp.write_text(final,encoding="utf-8")
    tmp.replace(path)

def claude_config_path(scope:str,project:Path)->Path:
    return project/".mcp.json" if scope=="project" else Path.home()/".claude.json"

def claude_server(server:dict,scope:str,project:Path)->dict:
    if server["transport"]=="stdio":
        data={
            "type":"stdio",
            "command":server["command"],
            "args":[expand_arg(x,"claude",scope,project) for x in server.get("args",[])],
        }
        req=server.get("requiredEnv",[])
        if req:
            data["env"]={name:"${"+name+"}" for name in req}
        return data
    data={"type":"http","url":server["url"]}
    headers={}
    if server.get("bearerTokenEnvVar"):
        env=server["bearerTokenEnvVar"]
        headers["Authorization"]="Bearer ${"+env+"}"
    for header,env in server.get("envHttpHeaders",{}).items():
        headers[header]="${"+env+"}"
    if headers:data["headers"]=headers
    return data

def apply_claude(scope:str,project:Path,state:dict,previous_managed:set[str],force:bool):
    path=claude_config_path(scope,project)
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        try:data=json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:raise SystemExit(f"Invalid Claude MCP config {path}: {e}")
    else:data={}
    mcp=data.setdefault("mcpServers",{})
    desired={
        name for name,meta in state["servers"].items()
        if "claude" in meta.get("targets",[]) and meta.get("enabled",True)
    }
    current_managed=set(previous_managed)
    for name in current_managed:
        mcp.pop(name,None)
    for name in desired:
        if name in mcp and name not in current_managed and not force:
            raise SystemExit(
                f"Claude config already contains unmanaged MCP server '{name}'. "
                "Use --force only after reviewing the existing definition."
            )
        mcp[name]=claude_server(load_server(name),scope,project)
    tmp=path.with_name(path.name+".weap.tmp")
    tmp.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    tmp.replace(path)

def targets(value:str)->list[str]:
    return ["codex","claude"] if value=="both" else [value]

def file_snapshot(path:Path):
    return (path.exists(), path.read_bytes() if path.exists() else b"")

def restore_file(path:Path,snapshot):
    existed,content=snapshot
    if existed:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(content)
    elif path.exists():
        path.unlink()

def apply_configs(scope:str,project:Path,state:dict,previous:dict,force:bool):
    previous_codex={n for n,m in previous.get("servers",{}).items() if "codex" in m.get("targets",[])}
    previous_claude={n for n,m in previous.get("servers",{}).items() if "claude" in m.get("targets",[])}
    current_targets={x for m in state["servers"].values() for x in m.get("targets",[])}
    previous_targets={x for m in previous.get("servers",{}).values() for x in m.get("targets",[])}
    codex_path=codex_config_path(scope,project)
    claude_path=claude_config_path(scope,project)
    snapshots={
        codex_path:file_snapshot(codex_path),
        claude_path:file_snapshot(claude_path),
    }
    try:
        if "codex" in current_targets or "codex" in previous_targets:
            apply_codex(scope,project,state,previous_codex,force)
        if "claude" in current_targets or "claude" in previous_targets:
            apply_claude(scope,project,state,previous_claude,force)
    except (Exception,SystemExit):
        for path,snapshot in snapshots.items():
            restore_file(path,snapshot)
        raise

def lock_refresh_notice(scope:str,project:Path):
    if scope=="project" and (project/".web-engineering-agent-pack.lock.json").exists():
        print("Project lock is now stale. Run: ./weap project lock --project-dir="+str(project))

def cmd_list(a):
    project=project_arg(a.project_dir)
    state=read_state(a.scope,project)
    installed=state["servers"]
    print(f"{'SERVER':22} {'RISK':9} {'TRANSPORT':10} {'INSTALLED':10} {'ENABLED':8} TARGETS")
    for p in sorted(REGISTRY.glob("*.json")):
        s=json.loads(p.read_text())
        meta=installed.get(s["name"])
        print(
            f"{s['name']:22} {s['risk']:9} {s['transport']:10} "
            f"{'yes' if meta else 'no':10} "
            f"{('yes' if meta and meta.get('enabled',True) else 'no') if meta else '-':8} "
            f"{','.join(meta.get('targets',[])) if meta else '-'}"
        )
    return 0

def cmd_profiles(a):
    for p in sorted(PROFILES.glob("*.json")):
        d=json.loads(p.read_text())
        print(f"{d['name']:20} {', '.join(d['servers'])}")
        print(f"  {d['description']}")
    return 0

def cmd_plan(a):
    project=project_arg(a.project_dir)
    names=resolve_names(a.server,a.profile)
    for name in names:
        s=load_server(name)
        print(f"{name}: risk={s['risk']}, transport={s['transport']}, write={str(s['writeCapability']).lower()}")
        if s.get("requiredEnv"):print("  required env:",", ".join(s["requiredEnv"]))
        if s.get("versionPolicy")=="upstream-documentation-example":
            print("  warning: package version follows the upstream documentation example and is not WEAP-pinned")
    print("Scope:",a.scope)
    print("Target:",a.target)
    print("No configuration changed.")
    return 0

def cmd_install(a):
    project=project_arg(a.project_dir)
    names=resolve_names(a.server,a.profile)
    if not names:raise SystemExit("Select at least one --server or --profile.")
    previous=read_state(a.scope,project)
    state=json.loads(json.dumps(previous))
    for name in names:
        server=load_server(name)
        require_allowed(server,a.scope,project,a.allow_high_risk)
        old=state["servers"].get(name,{"targets":[],"enabled":True})
        merged=sorted(set(old.get("targets",[]))|set(targets(a.target)))
        state["servers"][name]={
            "definitionHash":definition_hash(server),
            "targets":merged,
            "enabled":True
        }
    if a.dry_run:
        for n in names:print("would install:",n)
        print("No configuration changed.")
        return 0
    apply_configs(a.scope,project,state,previous,a.force)
    write_state(a.scope,project,state)
    print("Installed MCP servers:",", ".join(names))
    lock_refresh_notice(a.scope,project)
    return 0

def cmd_remove(a):
    project=project_arg(a.project_dir)
    previous=read_state(a.scope,project)
    state=json.loads(json.dumps(previous))
    if a.name not in state["servers"]:
        print(f"MCP server '{a.name}' is not managed in this scope.")
        return 0
    if a.target=="both":
        state["servers"].pop(a.name)
    else:
        meta=state["servers"][a.name]
        meta["targets"]=[x for x in meta.get("targets",[]) if x!=a.target]
        if not meta["targets"]:state["servers"].pop(a.name)
    apply_configs(a.scope,project,state,previous,a.force)
    write_state(a.scope,project,state)
    print("Removed MCP server:",a.name)
    lock_refresh_notice(a.scope,project)
    return 0

def set_enabled(a,value:bool):
    project=project_arg(a.project_dir)
    previous=read_state(a.scope,project)
    state=json.loads(json.dumps(previous))
    if a.name not in state["servers"]:raise SystemExit(f"MCP server '{a.name}' is not managed.")
    state["servers"][a.name]["enabled"]=value
    apply_configs(a.scope,project,state,previous,a.force)
    write_state(a.scope,project,state)
    print(("Enabled" if value else "Disabled")+" MCP server:",a.name)
    lock_refresh_notice(a.scope,project)
    return 0

def cmd_doctor(a):
    project=project_arg(a.project_dir)
    state=read_state(a.scope,project)
    failures=0
    warnings=0
    print("WEAP MCP Doctor")
    print("="*72)
    for name,meta in sorted(state["servers"].items()):
        try:server=load_server(name)
        except SystemExit:
            print(f"[FAIL] {name}: registry definition missing");failures+=1;continue
        actual=definition_hash(server)
        if actual!=meta.get("definitionHash"):
            print(f"[FAIL] {name}: registry definition changed since installation");failures+=1
        else:
            print(f"[ OK ] {name}: definition hash matches")
        if server["transport"]=="stdio":
            command=server["command"]
            if shutil.which(command):
                print(f"[ OK ] {name}: command found: {command}")
            else:
                print(f"[WARN] {name}: command not found in PATH: {command}");warnings+=1
        for env in server.get("requiredEnv",[]):
            if os.environ.get(env):
                print(f"[ OK ] {name}: environment variable is set: {env}")
            else:
                print(f"[WARN] {name}: environment variable is missing: {env}");warnings+=1
        if RISK_ORDER[server["risk"]]>=RISK_ORDER["high"]:
            print(f"[WARN] {name}: {server['risk']} risk capability");warnings+=1
        if server.get("versionPolicy")=="upstream-documentation-example":
            print(f"[WARN] {name}: dependency is not pinned by WEAP");warnings+=1
    print()
    print(f"Result: {failures} failures, {warnings} warnings")
    return 1 if failures else 0

def cmd_reset(a):
    project=project_arg(a.project_dir)
    previous=read_state(a.scope,project)
    if not previous.get("servers"):
        print("No WEAP-managed MCP servers exist in this scope.")
        return 0
    names=sorted(previous["servers"])
    print("WEAP-managed MCP servers to remove:",", ".join(names))
    if a.dry_run:
        print("No configuration changed.")
        return 0
    if not a.yes:
        if not sys.stdin.isatty():
            raise SystemExit("--yes is required for non-interactive MCP reset.")
        answer=input("Remove all WEAP-managed MCP servers in this scope? [y/N] ").strip().lower()
        if answer not in {"y","yes"}:
            print("Cancelled.")
            return 1
    state={"schemaVersion":1,"packVersion":PACK_VERSION,"scope":a.scope,"servers":{}}
    apply_configs(a.scope,project,state,previous,a.force)
    sp=state_path(a.scope,project)
    if sp.exists():
        sp.unlink()
    print("WEAP-managed MCP servers removed from this scope.")
    lock_refresh_notice(a.scope,project)
    return 0

def cmd_export(a):
    project=project_arg(a.project_dir)
    state=read_state(a.scope,project)
    print(json.dumps(state,indent=2))
    return 0

def build_parser():
    p=argparse.ArgumentParser(description="WEAP MCP manager")
    sub=p.add_subparsers(dest="cmd",required=True)
    common=argparse.ArgumentParser(add_help=False)
    common.add_argument("--scope",choices=["project","user"],default="project")
    common.add_argument("--project-dir",default=".")

    s=sub.add_parser("list",parents=[common]);s.set_defaults(fn=cmd_list)
    s=sub.add_parser("profiles");s.set_defaults(fn=cmd_profiles)

    for command in ["plan","install"]:
        s=sub.add_parser(command,parents=[common])
        s.add_argument("--server",action="append",default=[])
        s.add_argument("--profile",action="append",default=[])
        s.add_argument("--target",choices=["both","codex","claude"],default="both")
        if command=="install":
            s.add_argument("--allow-high-risk",action="store_true")
            s.add_argument("--force",action="store_true")
            s.add_argument("--dry-run",action="store_true")
            s.set_defaults(fn=cmd_install)
        else:s.set_defaults(fn=cmd_plan)

    s=sub.add_parser("remove",parents=[common])
    s.add_argument("name");s.add_argument("--target",choices=["both","codex","claude"],default="both")
    s.add_argument("--force",action="store_true");s.set_defaults(fn=cmd_remove)

    for name,value in [("enable",True),("disable",False)]:
        s=sub.add_parser(name,parents=[common]);s.add_argument("name");s.add_argument("--force",action="store_true")
        s.set_defaults(fn=lambda a,v=value:set_enabled(a,v))

    s=sub.add_parser("doctor",parents=[common]);s.set_defaults(fn=cmd_doctor)
    s=sub.add_parser("reset",parents=[common])
    s.add_argument("--yes",action="store_true")
    s.add_argument("--dry-run",action="store_true")
    s.add_argument("--force",action="store_true")
    s.set_defaults(fn=cmd_reset)
    s=sub.add_parser("export",parents=[common]);s.set_defaults(fn=cmd_export)
    return p

def main():
    a=build_parser().parse_args()
    return a.fn(a)

if __name__=="__main__":
    raise SystemExit(main())
