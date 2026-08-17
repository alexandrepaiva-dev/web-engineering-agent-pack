from __future__ import annotations
from pathlib import Path
import argparse, json, os, subprocess, sys

ROOT = Path(__file__).resolve().parent

def run(cmd: list[str]) -> int:
    print("+", " ".join(str(x) for x in cmd))
    return subprocess.call([str(x) for x in cmd])

def py(script: str, *args: str) -> int:
    return run([sys.executable, str(ROOT / script), *args])

def sh(script: str, *args: str) -> int:
    if os.name == "nt":
        raise SystemExit(f"{script} requires Bash. Use the matching PowerShell command on Windows.")
    return run(["bash", str(ROOT / script), *args])

def ps(script: str, *args: str) -> int:
    shell = "pwsh" if subprocess.call(["where" if os.name=="nt" else "which", "pwsh"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 else "powershell"
    return run([shell, "-ExecutionPolicy", "Bypass", "-File", str(ROOT / script), *args])

def platform_script(base: str, args: list[str]) -> int:
    script = f"scripts/commands/{base}"
    if os.name == "nt":
        converted=[]
        i=0
        while i < len(args):
            a=args[i]
            mapping={
                "--profile":"-Profile","--project-dir":"-ProjectDir","--target":"-Target",
                "--include-core":"-IncludeCore","--init-project":"-InitProject",
                "--dry-run":"-DryRun","--force":"-Force","--with-third-party":"-WithThirdParty",
                "--keep-third-party":"-KeepThirdParty","--restore-previous":"-RestorePrevious",
                "--remove-ai-config":"-RemoveAiConfig","--current-paths":"-CurrentPaths",
                "--force-legacy":"-ForceLegacy","--add-skill":"-AddSkill",
                "--remove-skill":"-RemoveSkill",
            }
            if a in mapping:
                converted.append(mapping[a])
                if a in {"--profile","--project-dir","--target","--add-skill","--remove-skill"} and i+1 < len(args):
                    converted.append(args[i+1]); i+=2; continue
            elif a.startswith("--profile="):
                converted += ["-Profile", a.split("=",1)[1]]
            elif a.startswith("--project-dir="):
                converted += ["-ProjectDir", a.split("=",1)[1]]
            elif a.startswith("--add-skill="):
                converted += ["-AddSkill", a.split("=",1)[1]]
            elif a.startswith("--remove-skill="):
                converted += ["-RemoveSkill", a.split("=",1)[1]]
            elif a.startswith("--target="):
                converted += ["-Target", a.split("=",1)[1]]
            else:
                converted.append(a)
            i+=1
        return ps(script + ".ps1", *converted)
    return sh(script + ".sh", *args)

def cmd_install(a):
    args=["--profile",a.profile]
    if a.with_third_party: args.append("--with-third-party")
    if a.dry_run: args.append("--dry-run")
    for x in a.add_skill: args += ["--add-skill",x]
    for x in a.remove_skill: args += ["--remove-skill",x]
    return platform_script("install-all",args)


def cmd_project_init(a):
    project=Path(a.project_dir).expanduser().resolve()
    profile=a.profile
    if a.detect:
        proc=subprocess.run(
            [sys.executable,str(ROOT/"scripts/profile_manager.py"),"detect","--project-dir",str(project),"--json"],
            text=True,capture_output=True
        )
        if proc.returncode:
            print(proc.stderr,file=sys.stderr);return proc.returncode
        detected=json.loads(proc.stdout)
        suggested=detected.get("recommendedProfile")
        print("Detected signals:")
        for s in detected.get("signals",[]): print("-",s)
        print("Suggested profile:",suggested or "unknown")
        if not profile: profile=suggested
    if not profile:
        print("Could not determine a profile. Supply --profile.",file=sys.stderr);return 2

    if not a.yes and sys.stdin.isatty():
        answer=input(f"Initialize {project} with profile '{profile}'{' in team mode' if a.team else ''}? [y/N] ").strip().lower()
        if answer not in {"y","yes"}:
            print("Cancelled.");return 1
    elif not a.yes and not sys.stdin.isatty():
        print("--yes is required for non-interactive project init.",file=sys.stderr);return 2

    args=["--profile",profile,"--project-dir",str(project),"--target","both","--init-project"]
    if a.team: args.append("--include-core")
    rc=platform_script("install-project",args)
    if rc:return rc
    lock_rc=py("scripts/project_lock.py","write","--project-dir",str(project))
    if lock_rc:return lock_rc
    suggested_mcp="development"
    print()
    print("MCP capabilities are opt-in and were not installed.")
    print(f"Suggested MCP profile: {suggested_mcp}")
    print(f"Review: ./weap mcp plan --profile {suggested_mcp} --scope project --project-dir {project}")
    print(f"Install: ./weap mcp install --profile {suggested_mcp} --scope project --project-dir {project}")
    return 0

def cmd_project_install(a):
    args=["--profile",a.profile,"--project-dir",a.project_dir,"--target",a.target]
    if a.include_core: args.append("--include-core")
    if a.init_project: args.append("--init-project")
    if a.dry_run: args.append("--dry-run")
    if a.force: args.append("--force")
    for x in a.add_skill: args += [f"--add-skill={x}"]
    for x in a.remove_skill: args += [f"--remove-skill={x}"]
    return platform_script("install-project",args)

def cmd_project_uninstall(a):
    args=["--project-dir",a.project_dir,"--target",a.target]
    if a.remove_ai_config: args.append("--remove-ai-config")
    if a.dry_run: args.append("--dry-run")
    return platform_script("uninstall-project",args)

def cmd_project_lock(a):
    return py("scripts/project_lock.py","write","--project-dir",a.project_dir)

def cmd_project_verify(a):
    return py("scripts/project_lock.py","verify","--project-dir",a.project_dir)

def cmd_project_apply_lock(a):
    args=["apply","--project-dir",a.project_dir]
    if a.force: args.append("--force")
    return py("scripts/project_lock.py",*args)

def cmd_project_detect(a):
    return py("scripts/profile_manager.py","detect","--project-dir",a.project_dir)

def cmd_doctor(a):
    args=[]
    if a.project_dir: args += ["--project-dir",a.project_dir]
    if a.json: args.append("--json")
    return py("scripts/doctor.py",*args)

def cmd_uninstall(a):
    args=[]
    if a.keep_third_party: args.append("--keep-third-party")
    if a.restore_previous: args.append("--restore-previous")
    if a.dry_run: args.append("--dry-run")
    if a.force_legacy: args.append("--force-legacy")
    return platform_script("uninstall",args)

def cmd_backup_list(a):
    return platform_script("list-backups",[])

def cmd_backup_restore(a):
    args=[a.backup]
    if a.current_paths: args.append("--current-paths")
    return platform_script("restore-backup",args)

def cmd_project_backup_list(a):
    return py("scripts/project_backup.py","list","--project-dir",a.project_dir)

def cmd_project_backup_restore(a):
    return py("scripts/project_backup.py","restore",a.backup,"--project-dir",a.project_dir)

def cmd_audit(a):
    code=0
    for script in [
        "scripts/validate-pack.py",
        "scripts/lint-skills.py",
        "scripts/lint-profiles.py",
        "scripts/docs-consistency.py",
        "scripts/language-audit.py",
        "scripts/analyze-context-budget.py",
        "scripts/analyze-package-size.py",
    ]:
        r=py(script)
        if r: code=r
    try:
        import jsonschema  # noqa
        r=py("scripts/validate-schemas.py")
        if r: code=r
    except ImportError:
        print("WARN: jsonschema not installed; formal schema validation skipped.")
    return code

def cmd_migrate(a):
    args=["--project-dir",a.project_dir]
    if a.apply: args.append("--apply")
    return py("scripts/migrate.py",*args)

def cmd_mcp(a):
    return py("scripts/mcp_manager.py",*a.mcp_args)

def cmd_update(a):
    args=["--channel",a.channel]
    if a.repo: args += ["--repo",a.repo]
    if a.apply: args.append("--apply")
    if a.skip_attestation: args.append("--skip-attestation")
    return py("scripts/update.py",*args)

def cmd_release(a):
    args=["--version",a.version,"--channel",a.channel]
    if a.dry_run: args.append("--dry-run")
    if a.output_dir: args += ["--output-dir",a.output_dir]
    return py("scripts/release.py",*args)

def build():
    p=argparse.ArgumentParser(prog="weap",description="Web Engineering Agent Pack CLI")
    p.add_argument("--version",action="version",version="weap 1.0.0")
    sub=p.add_subparsers(dest="command",required=True)

    s=sub.add_parser("install",help="Install global profile for Codex + Claude Code.")
    s.add_argument("--profile",default="core")
    s.add_argument("--with-third-party",action="store_true")
    s.add_argument("--dry-run",action="store_true")
    s.add_argument("--add-skill",action="append",default=[])
    s.add_argument("--remove-skill",action="append",default=[])
    s.set_defaults(fn=cmd_install)

    project=sub.add_parser("project",help="Manage repository-local profiles.")
    psu=project.add_subparsers(dest="project_cmd",required=True)

    s=psu.add_parser("init")
    s.add_argument("--project-dir",default=".")
    s.add_argument("--profile")
    s.add_argument("--detect",action="store_true")
    s.add_argument("--team",action="store_true",help="Install CORE + stack locally for a self-contained repository.")
    s.add_argument("--yes",action="store_true")
    s.set_defaults(fn=cmd_project_init)

    s=psu.add_parser("install")
    s.add_argument("--profile",required=True)
    s.add_argument("--project-dir",default=".")
    s.add_argument("--target",choices=["both","codex","claude"],default="both")
    s.add_argument("--include-core",action="store_true")
    s.add_argument("--init-project",action="store_true")
    s.add_argument("--dry-run",action="store_true")
    s.add_argument("--force",action="store_true")
    s.add_argument("--add-skill",action="append",default=[])
    s.add_argument("--remove-skill",action="append",default=[])
    s.set_defaults(fn=cmd_project_install)

    s=psu.add_parser("uninstall")
    s.add_argument("--project-dir",default=".")
    s.add_argument("--target",choices=["both","codex","claude"],default="both")
    s.add_argument("--remove-ai-config",action="store_true")
    s.add_argument("--dry-run",action="store_true")
    s.set_defaults(fn=cmd_project_uninstall)

    s=psu.add_parser("detect"); s.add_argument("--project-dir",default="."); s.set_defaults(fn=cmd_project_detect)
    s=psu.add_parser("lock"); s.add_argument("--project-dir",default="."); s.set_defaults(fn=cmd_project_lock)
    s=psu.add_parser("verify"); s.add_argument("--project-dir",default="."); s.set_defaults(fn=cmd_project_verify)
    s=psu.add_parser("apply-lock"); s.add_argument("--project-dir",default="."); s.add_argument("--force",action="store_true"); s.set_defaults(fn=cmd_project_apply_lock)

    b=psu.add_parser("backup")
    bsub=b.add_subparsers(dest="project_backup_cmd",required=True)
    s=bsub.add_parser("list"); s.add_argument("--project-dir",default="."); s.set_defaults(fn=cmd_project_backup_list)
    s=bsub.add_parser("restore"); s.add_argument("backup",nargs="?",default="latest"); s.add_argument("--project-dir",default="."); s.set_defaults(fn=cmd_project_backup_restore)

    s=sub.add_parser("doctor"); s.add_argument("--project-dir"); s.add_argument("--json",action="store_true"); s.set_defaults(fn=cmd_doctor)
    s=sub.add_parser("audit"); s.set_defaults(fn=cmd_audit)

    s=sub.add_parser("uninstall")
    s.add_argument("--keep-third-party",action="store_true")
    s.add_argument("--restore-previous",action="store_true")
    s.add_argument("--dry-run",action="store_true")
    s.add_argument("--force-legacy",action="store_true")
    s.set_defaults(fn=cmd_uninstall)

    b=sub.add_parser("backup")
    bsub=b.add_subparsers(dest="backup_cmd",required=True)
    s=bsub.add_parser("list"); s.set_defaults(fn=cmd_backup_list)
    s=bsub.add_parser("restore"); s.add_argument("backup",nargs="?",default="latest"); s.add_argument("--current-paths",action="store_true"); s.set_defaults(fn=cmd_backup_restore)

    s=sub.add_parser("migrate")
    s.add_argument("--project-dir",default=".")
    s.add_argument("--apply",action="store_true")
    s.set_defaults(fn=cmd_migrate)

    s=sub.add_parser("mcp",help="Manage opt-in MCP servers and profiles.")
    s.add_argument("mcp_args",nargs=argparse.REMAINDER)
    s.set_defaults(fn=cmd_mcp)

    s=sub.add_parser("update",help="Check or apply a verified GitHub release update.")
    s.add_argument("--repo",help="GitHub repository as OWNER/REPO; otherwise inferred from git remote or environment.")
    s.add_argument("--channel",choices=["stable","preview"],default="stable")
    s.add_argument("--apply",action="store_true")
    s.add_argument("--skip-attestation",action="store_true",help="Skip GitHub provenance verification explicitly.")
    s.set_defaults(fn=cmd_update)

    s=sub.add_parser("release")
    s.add_argument("--version",required=True)
    s.add_argument("--output-dir")
    s.add_argument("--channel",choices=["stable","preview"],default="stable")
    s.add_argument("--dry-run",action="store_true")
    s.set_defaults(fn=cmd_release)

    return p

def main():
    p=build()
    a=p.parse_args()
    raise SystemExit(a.fn(a) or 0)

if __name__=="__main__":
    main()
