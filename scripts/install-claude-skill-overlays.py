from pathlib import Path
import re

manual = ['architecture-review', 'ci-cd', 'dependency-upgrades', 'performance-profiling']

def add_manual_flag(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.parent.name not in manual:
        return
    if "disable-model-invocation:" in text:
        return
    text = text.replace("---\n", "---\ndisable-model-invocation: true\n", 1)
    path.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    import sys
    root = Path(sys.argv[1]).expanduser()
    for skill in manual:
        p = root / skill / "SKILL.md"
        if p.exists():
            add_manual_flag(p)
