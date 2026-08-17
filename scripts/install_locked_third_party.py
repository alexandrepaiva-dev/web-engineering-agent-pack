from __future__ import annotations
from pathlib import Path
import argparse, json, os, shutil, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "third-party.lock.json"

def run(*args, cwd=None):
    subprocess.run(list(args), cwd=cwd, check=True)

def atomic_copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    stage = dst.parent / f".{dst.name}.weap-stage"
    old = dst.parent / f".{dst.name}.weap-old"
    shutil.rmtree(stage, ignore_errors=True)
    shutil.rmtree(old, ignore_errors=True)
    shutil.copytree(src, stage)
    if dst.exists():
        dst.rename(old)
    try:
        stage.rename(dst)
    except Exception:
        if dst.exists():
            shutil.rmtree(dst, ignore_errors=True)
        if old.exists():
            old.rename(dst)
        raise
    shutil.rmtree(old, ignore_errors=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["both","codex","claude"], default="both")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = json.loads(LOCK.read_text(encoding="utf-8"))
    home = Path.home()
    codex_root = home / ".agents" / "skills"
    claude_home = Path(os.environ.get("CLAUDE_CONFIG_DIR", home / ".claude"))
    claude_root = claude_home / "skills"

    if args.dry_run:
        for dep in data["dependencies"]:
            print(f"{dep['name']}: {dep['repository']} @ {dep['commit']}")
        print("Targets:", args.target)
        return

    with tempfile.TemporaryDirectory(prefix="weap-third-party-") as td:
        td = Path(td)
        for dep in data["dependencies"]:
            repo = td / dep["name"]
            run("git", "clone", "--filter=blob:none", "--no-checkout", dep["repository"], str(repo))
            run("git", "checkout", "--detach", dep["commit"], cwd=repo)
            actual = subprocess.run(
                ["git","rev-parse","HEAD"], cwd=repo, text=True, capture_output=True, check=True
            ).stdout.strip()
            if actual != dep["commit"]:
                raise SystemExit(f"Commit verification failed for {dep['name']}")

            source = (repo / dep["install"]["sourcePath"]).resolve()
            try:
                source.relative_to(repo.resolve())
            except ValueError:
                raise SystemExit(f"Locked source path escapes repository root for {dep['name']}")
            if not source.exists():
                raise SystemExit(f"Locked source path missing for {dep['name']}: {source}")

            if args.target in {"both","codex"}:
                atomic_copy(source, codex_root / dep["name"])
            if args.target in {"both","claude"}:
                atomic_copy(source, claude_root / dep["name"])
            print(f"Installed {dep['name']} @ {actual[:12]}")

if __name__ == "__main__":
    main()
