from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, urllib.request, zipfile

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"manifest.json"
SEMVER=re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z.-]+))?$")
GITHUB_API="https://api.github.com"

def parse_version(v:str):
    m=SEMVER.fullmatch(v)
    if not m: raise ValueError(v)
    major,minor,patch=map(int,m.group(1,2,3))
    pre=m.group(4)
    if pre is None:
        prekey=()
        stable=1
    else:
        stable=0
        prekey=tuple((0,int(x)) if x.isdigit() else (1,x) for x in pre.split("."))
    return (major,minor,patch,stable,prekey)

def newer(a:str,b:str)->bool:
    return parse_version(a)>parse_version(b)

def normalize_repo_url(url:str)->str|None:
    url=url.strip()
    m=re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$",url)
    return f"{m.group(1)}/{m.group(2)}" if m else None

def detect_repo(explicit:str|None)->str:
    if explicit: return explicit
    env=os.environ.get("WEAP_UPDATE_REPOSITORY")
    if env: return env
    try:
        m=json.loads(MANIFEST.read_text())
        if m.get("repositorySlug"): return m["repositorySlug"]
    except Exception: pass
    try:
        r=subprocess.run(["git","remote","get-url","origin"],cwd=ROOT,text=True,capture_output=True,timeout=5)
        if r.returncode==0:
            repo=normalize_repo_url(r.stdout)
            if repo:return repo
    except Exception: pass
    raise SystemExit(
        "Cannot determine GitHub repository. Use --repo OWNER/web-engineering-agent-pack "
        "or set WEAP_UPDATE_REPOSITORY."
    )

def request_json(url:str):
    req=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json","User-Agent":"WEAP-Updater"})
    with urllib.request.urlopen(req,timeout=20) as r:
        return json.load(r)

def download(url:str,dst:Path):
    req=urllib.request.Request(url,headers={"Accept":"application/octet-stream","User-Agent":"WEAP-Updater"})
    with urllib.request.urlopen(req,timeout=60) as r, dst.open("wb") as f:
        shutil.copyfileobj(r,f)

def choose_release(releases:list[dict],channel:str,current:str)->dict|None:
    candidates=[]
    for r in releases:
        if r.get("draft"): continue
        tag=str(r.get("tag_name","")).lstrip("v")
        if not SEMVER.fullmatch(tag): continue
        if channel=="stable" and r.get("prerelease"): continue
        if channel=="preview" and not r.get("prerelease"): continue
        if newer(tag,current): candidates.append((parse_version(tag),r))
    return max(candidates,key=lambda x:x[0])[1] if candidates else None

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def expected_checksum(checksums:Path,filename:str)->str:
    for line in checksums.read_text(encoding="utf-8").splitlines():
        parts=line.strip().split()
        if len(parts)>=2 and parts[-1].lstrip("*")==filename:
            if re.fullmatch(r"[a-fA-F0-9]{64}",parts[0]): return parts[0].lower()
    raise SystemExit(f"Checksum for {filename} not found in SHA256SUMS.")

def find_asset(release:dict,name:str)->dict:
    for a in release.get("assets",[]):
        if a.get("name")==name:return a
    raise SystemExit(f"Release asset missing: {name}")

def verify_attestation(archive:Path,repo:str,skip:bool):
    if skip:
        print("WARN: GitHub artifact attestation verification skipped.")
        return
    gh=shutil.which("gh")
    if not gh:
        raise SystemExit(
            "GitHub CLI (gh) is required to verify release provenance. "
            "Install gh or explicitly pass --skip-attestation."
        )
    subprocess.run([gh,"attestation","verify",str(archive),"-R",repo],check=True)

def validate_tree(tree:Path):
    for script in ["scripts/validate-pack.py","scripts/docs-consistency.py","scripts/lint-skills.py","scripts/lint-profiles.py"]:
        subprocess.run([sys.executable,str(tree/script)],cwd=tree,check=True)

def atomic_replace(tree:Path,version:str):
    parent=ROOT.parent
    backup_root=parent/".weap-self-update-backups"
    backup_root.mkdir(exist_ok=True)
    from datetime import datetime
    stamp=datetime.now().strftime("%Y%m%d-%H%M%S")
    backup=backup_root/f"{ROOT.name}-{version}-{stamp}"

    stage=parent/f".{ROOT.name}.update-stage"
    shutil.rmtree(stage,ignore_errors=True)
    shutil.copytree(tree,stage)

    # On POSIX, directory rename is atomic within the same filesystem.
    # On Windows, replacing the directory containing the running interpreter can fail;
    # stage and validated backup are retained and a clear recovery instruction is emitted.
    try:
        ROOT.rename(backup)
        stage.rename(ROOT)
    except Exception:
        if not ROOT.exists() and backup.exists():
            backup.rename(ROOT)
        raise
    print("Previous pack backup:",backup)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo")
    ap.add_argument("--channel",choices=["stable","preview"],default="stable")
    ap.add_argument("--apply",action="store_true")
    ap.add_argument("--skip-attestation",action="store_true")
    a=ap.parse_args()

    current=json.loads(MANIFEST.read_text())["version"]
    repo=detect_repo(a.repo)
    releases=request_json(f"{GITHUB_API}/repos/{repo}/releases?per_page=30")
    release=choose_release(releases,a.channel,current)
    if not release:
        print(f"WEAP {current} is current for channel '{a.channel}'.")
        return 0

    version=release["tag_name"].lstrip("v")
    archive_name=f"web-engineering-agent-pack-{version}.zip"
    print(f"Update available: {current} -> {version}")
    print("Repository:",repo)
    if not a.apply:
        print("Preview only. Re-run with --apply to download, verify, validate, and install.")
        return 0

    with tempfile.TemporaryDirectory(prefix="weap-update-") as td:
        td=Path(td)
        archive=td/archive_name
        sums=td/"SHA256SUMS"
        download(find_asset(release,archive_name)["browser_download_url"],archive)
        download(find_asset(release,"SHA256SUMS")["browser_download_url"],sums)

        expected=expected_checksum(sums,archive_name)
        actual=sha256(archive)
        if actual!=expected:
            raise SystemExit(f"SHA-256 mismatch: expected {expected}, got {actual}")
        print("SHA-256 verified:",actual)

        verify_attestation(archive,repo,a.skip_attestation)

        extract=td/"extract"
        with zipfile.ZipFile(archive) as z: z.extractall(extract)
        tree=extract/"web-engineering-agent-pack"
        if not tree.exists(): raise SystemExit("Release archive root is invalid.")
        incoming=json.loads((tree/"manifest.json").read_text())["version"]
        if incoming!=version: raise SystemExit(f"Archive version mismatch: {incoming} != {version}")
        validate_tree(tree)

        atomic_replace(tree,current)
        print(f"WEAP updated to {version}.")
        print("Run: ./weap doctor")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
