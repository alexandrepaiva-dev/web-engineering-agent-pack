from __future__ import annotations
from pathlib import Path
import argparse, json, subprocess

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "third-party.lock.json"

def git_head(repo: str, ref: str = "HEAD") -> str:
    proc = subprocess.run(
        ["git", "ls-remote", repo, ref],
        text=True, capture_output=True, check=True
    )
    line = proc.stdout.strip().splitlines()
    if not line:
        raise SystemExit(f"Could not resolve {ref} for {repo}")
    return line[0].split()[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Write resolved commits to lock file.")
    args = ap.parse_args()

    data = json.loads(LOCK.read_text(encoding="utf-8"))
    changed = False
    for dep in data["dependencies"]:
        current = dep["commit"]
        latest = git_head(dep["repository"])
        status = "CURRENT" if current == latest else "UPDATE AVAILABLE"
        print(f"{dep['name']}: {status}")
        print(f"  locked: {current}")
        print(f"  latest: {latest}")
        if args.apply and current != latest:
            dep["commit"] = latest
            changed = True

    if args.apply and changed:
        from datetime import date
        data["reviewedAt"] = date.today().isoformat()
        LOCK.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print("Lock file updated. Review upstream diffs before committing.")

if __name__ == "__main__":
    main()
