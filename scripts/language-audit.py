from pathlib import Path
import re,sys

ROOT=Path(__file__).resolve().parents[1]
EXT={".md",".py",".sh",".ps1",".json",".toml",".yml",".yaml",".html",".css",".js"}
SKIP={"tests/fixtures/migrations"}
markers=[
    r"\bnão\b",r"\bversão\b",r"\bprojeto\b",r"\busuário\b",r"\barquivo\b",
    r"\bdiretório\b",r"\binstalação\b",r"\bdesinstalação\b",r"\batualização\b",
    r"\bsegurança\b",r"\bconfiguração\b",r"\bsenha\b",r"\batenção\b",
    r"\bsucesso\b",r"\berro\b",r"\bambiente\b",r"\bferramenta\b"
]
pattern=re.compile("|".join(markers),re.I)
hits=[]
for p in ROOT.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in EXT:
        continue
    rel=p.relative_to(ROOT).as_posix()
    if any(rel.startswith(x) for x in SKIP):
        continue
    try:text=p.read_text(encoding="utf-8")
    except Exception:continue
    for lineno,line in enumerate(text.splitlines(),1):
        if pattern.search(line):
            hits.append(f"{rel}:{lineno}: {line.strip()}")
if hits:
    print("English-only language audit FAILED")
    for x in hits[:100]:print("-",x)
    sys.exit(1)
print("English-only language audit OK.")
