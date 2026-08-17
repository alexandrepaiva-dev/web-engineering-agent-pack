from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,sys,tempfile,zipfile

ROOT=Path(__file__).resolve().parents[1]
SEMVER=re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?$")

def run(cmd,cwd):
    print("+"," ".join(map(str,cmd)))
    subprocess.run(list(map(str,cmd)),cwd=cwd,check=True)

def set_version(tree: Path, version: str):
    manifest=tree/"manifest.json"
    m=json.loads(manifest.read_text())
    old_version=m["version"]
    old_major=old_version.split(".",1)[0]
    new_major=version.split(".",1)[0]
    m["version"]=version
    manifest.write_text(json.dumps(m,indent=2)+"\n")

    replacements=[
      ("scripts/profile_manager.py",rf'PACK_VERSION = "{re.escape(old_version)}"',f'PACK_VERSION = "{version}"'),
      ("scripts/backup-lib.sh",rf'PACK_VERSION="{re.escape(old_version)}"',f'PACK_VERSION="{version}"'),
      ("scripts/BackupLib.ps1",rf'\$PackVersion = "{re.escape(old_version)}"',f'$PackVersion = "{version}"'),
      ("weap.py",rf'version="weap {re.escape(old_version)}"',f'version="weap {version}"'),
      ("scripts/validate-pack.py",re.escape(old_version),version),
      ("tests/test_docs_consistency.py",re.escape(old_version),version),
      ("README.md",rf'"packVersion": "{re.escape(old_version)}"',f'"packVersion": "{version}"'),
    ]
    for rel,pattern,repl in replacements:
        p=tree/rel
        if p.exists():
            p.write_text(re.sub(pattern,repl,p.read_text()),encoding="utf-8")

    for rel in ["scripts/state-lib.sh","scripts/StateLib.ps1","scripts/migrate.py"]:
        p=tree/rel
        if p.exists():
            text=p.read_text()
            text=text.replace(old_version,version)
            p.write_text(text,encoding="utf-8")

    for rel in [
        "tests/fixtures/project-manifest.json",
        "tests/fixtures/install-state.json",
        "tests/fixtures/backup-manifest.json",
        "tests/fixtures/project-lock.json",
    ]:
        p=tree/rel
        if p.exists():
            data=json.loads(p.read_text())
            if "packVersion" in data:
                data["packVersion"]=version
            p.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")

    analyzer=tree/"scripts/analyze-context-budget.py"
    if analyzer.exists() and old_major != new_major:
        text=analyzer.read_text()
        text=re.sub(r"CONTEXT BUDGET REPORT — v\d+ MULTI-STACK",
                    f"CONTEXT BUDGET REPORT — v{new_major} MULTI-STACK",text)
        analyzer.write_text(text,encoding="utf-8")

def sha256(path: Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return h.hexdigest()

def release_notes(tree: Path,version: str,channel:str):
    changelog=(tree/"CHANGELOG.md").read_text()
    pattern=re.compile(rf"^##\s+{re.escape(version)}(?:[^\n]*)\n(.*?)(?=^##\s+|\Z)",re.M|re.S)
    m=pattern.search(changelog)
    body=m.group(1).strip() if m else "See CHANGELOG.md for release details."
    return f"# Web Engineering Agent Pack {version}\n\nChannel: **{channel}**\n\n{body}\n"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--version",required=True)
    ap.add_argument("--channel",choices=["stable","preview"],default="stable")
    ap.add_argument("--output-dir")
    ap.add_argument("--dry-run",action="store_true")
    a=ap.parse_args()
    if not SEMVER.fullmatch(a.version):
        raise SystemExit("Invalid Semantic Version.")

    out=Path(a.output_dir).expanduser().resolve() if a.output_dir else ROOT/"dist"
    print("Release plan:")
    print("- version:",a.version)
    print("- channel:",a.channel)
    print("- output:",out)
    if a.dry_run:
        return 0

    with tempfile.TemporaryDirectory(prefix="weap-release-") as td:
        tree=Path(td)/"web-engineering-agent-pack"
        shutil.copytree(ROOT,tree,ignore=shutil.ignore_patterns("dist","dist-*","__pycache__",".git","_site","context-budget-report.json","package-size-report.json"))
        set_version(tree,a.version)

        run([sys.executable,"scripts/validate-pack.py"],tree)
        run([sys.executable,"scripts/docs-consistency.py"],tree)
        run([sys.executable,"scripts/lint-skills.py"],tree)
        run([sys.executable,"scripts/lint-profiles.py"],tree)

        out.mkdir(parents=True,exist_ok=True)
        archive=out/f"web-engineering-agent-pack-{a.version}.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
            for p in tree.rglob("*"):
                if p.is_file() and "__pycache__" not in p.parts:
                    z.write(p,arcname=str(Path("web-engineering-agent-pack")/p.relative_to(tree)))

        checksum=sha256(archive)
        sums=out/"SHA256SUMS"
        sums.write_text(f"{checksum}  {archive.name}\n",encoding="utf-8")
        notes=out/f"RELEASE-NOTES-{a.version}.md"
        notes.write_text(release_notes(tree,a.version,a.channel),encoding="utf-8")

        meta={
            "version":a.version,"channel":a.channel,
            "archive":archive.name,"sha256":checksum,
            "releaseNotes":notes.name,
        }
        (out/"release.json").write_text(json.dumps(meta,indent=2)+"\n")
        print("Release artifact:",archive)
        print("SHA-256:",checksum)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
