from pathlib import Path
import re, json, math, itertools, collections

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "shared" / "skills"
PROFILES = ROOT / "profiles"

def approx_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))

def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out={}
    for line in m.group(1).splitlines():
        if ":" in line:
            k,v=line.split(":",1)
            out[k.strip()]=v.strip()
    return out

def words(s: str):
    stop={"use","when","for","or","and","the","a","an","to","of","in","with","is","engineering","implementation","review","explicitly"}
    return {w for w in re.findall(r"[a-z0-9][a-z0-9+-]*",s.lower()) if len(w)>2 and w not in stop}

def jaccard(a,b):
    return len(a&b)/max(1,len(a|b))

def load_profile(name: str):
    return json.loads((PROFILES/f"{name}.json").read_text(encoding="utf-8"))

def resolve_profile(name: str, seen=None):
    seen=set() if seen is None else seen
    if name in seen:
        raise ValueError(f"Profile cycle: {name}")
    seen.add(name)
    d=load_profile(name)
    out=[]
    for parent in d.get("extends",[]):
        for s in resolve_profile(parent,set(seen)):
            if s not in out: out.append(s)
    for s in d.get("skills",[]):
        if s not in out: out.append(s)
    for s in d.get("removeSkills",[]):
        if s in out: out.remove(s)
    return out

rows=[]
paragraph_index=collections.defaultdict(list)
skill_map={}
for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
    sf=d/"SKILL.md"
    text=sf.read_text(encoding="utf-8")
    fm=frontmatter(text)
    desc=fm.get("description","")
    refs=list((d/"references").glob("*.md"))
    ref_text="".join(r.read_text(encoding="utf-8") for r in refs)
    row={
        "skill":d.name,
        "description":desc,
        "description_tokens":approx_tokens(desc),
        "skill_tokens":approx_tokens(text),
        "reference_files":len(refs),
        "reference_tokens":approx_tokens(ref_text) if ref_text else 0,
    }
    rows.append(row); skill_map[d.name]=row
    body=text.split("---",2)[-1] if text.startswith("---") else text
    for para in [re.sub(r"\s+"," ",x.strip()) for x in re.split(r"\n\s*\n",body)]:
        if len(para)>=140: paragraph_index[para].append(d.name)

overlaps=[]
for a,b in itertools.combinations(rows,2):
    score=jaccard(words(a["description"]),words(b["description"]))
    if score>=0.34:
        overlaps.append((score,a["skill"],b["skill"]))
overlaps.sort(reverse=True)

duplicates=[(p,sorted(set(v))) for p,v in paragraph_index.items() if len(set(v))>1]
duplicates.sort(key=lambda x:(-len(x[1]),-len(x[0])))

globals={}
for name,rel in {
    "global_codex":"codex/global/.codex/AGENTS.md",
    "global_claude":"claude/global/.claude/CLAUDE.md",
    "project_agents_base":"project-template/AGENTS.base.md",
}.items():
    q=ROOT/rel
    if q.exists():
        globals[name]={"tokens_est":approx_tokens(q.read_text(encoding="utf-8")),"chars":q.stat().st_size}

profiles={}
core=set(resolve_profile("core"))
for f in sorted(PROFILES.glob("*.json")):
    if f.stem=="catalog": continue
    name=f.stem
    effective=resolve_profile(name)
    delta=effective if name=="core" else [s for s in effective if s not in core]
    profiles[name]={
        "effective_skills":effective,
        "effective_skill_count":len(effective),
        "effective_description_tokens_est":sum(skill_map[s]["description_tokens"] for s in effective),
        "stack_delta_skills":delta,
        "stack_delta_skill_count":len(delta),
        "stack_delta_description_tokens_est":sum(skill_map[s]["description_tokens"] for s in delta),
    }

report={
    "summary":{
        "library_skills":len(rows),
        "all_description_tokens_est":sum(r["description_tokens"] for r in rows),
        "all_skill_body_tokens_est":sum(r["skill_tokens"] for r in rows),
        "all_reference_tokens_est":sum(r["reference_tokens"] for r in rows),
    },
    "globals":globals,
    "profiles":profiles,
    "skills":rows,
    "trigger_overlaps":[{"score":round(s,3),"a":a,"b":b} for s,a,b in overlaps],
    "duplicate_long_paragraphs":[{"skills":v,"preview":p[:220]} for p,v in duplicates[:20]],
}

print("CONTEXT BUDGET REPORT — v1 MULTI-STACK")
print("="*82)
print(f"Library skills: {report['summary']['library_skills']}")
print(f"All descriptions if everything were globally visible: ~{report['summary']['all_description_tokens_est']} tokens")
print(f"All SKILL.md if every skill were loaded: ~{report['summary']['all_skill_body_tokens_est']} tokens")
print(f"All references (on demand): ~{report['summary']['all_reference_tokens_est']} tokens")
print()

print("Persistent instruction estimates")
for k,v in globals.items():
    print(f"- {k:24} ~{v['tokens_est']:5} tokens")
print()

print("Profile metadata budgets")
print(f"{'profile':22} {'effective':>10} {'meta tok':>10} {'project delta':>14} {'delta tok':>10}")
for name,v in profiles.items():
    print(f"{name:22} {v['effective_skill_count']:10} {v['effective_description_tokens_est']:10} {v['stack_delta_skill_count']:14} {v['stack_delta_description_tokens_est']:10}")
print()

print("Recommended architecture")
print(f"- global CORE metadata: ~{profiles['core']['effective_description_tokens_est']} tokens")
print(f"- Next.js project delta: ~{profiles['nextjs']['stack_delta_description_tokens_est']} tokens")
print(f"- Symfony project delta: ~{profiles['symfony']['stack_delta_description_tokens_est']} tokens")
print()

print("Per-skill")
print(f"{'skill':30} {'desc':>6} {'SKILL':>7} {'refs':>7} {'files':>6}")
for r in rows:
    print(f"{r['skill']:30} {r['description_tokens']:6} {r['skill_tokens']:7} {r['reference_tokens']:7} {r['reference_files']:6}")
print()

warnings=[]
for r in rows:
    if r["description_tokens"]>75:
        warnings.append(f"{r['skill']}: description ~{r['description_tokens']} tokens")
    if r["skill_tokens"]>900:
        warnings.append(f"{r['skill']}: SKILL.md ~{r['skill_tokens']} tokens")
for k,v in globals.items():
    if v["tokens_est"]>1800:
        warnings.append(f"{k}: persistent instructions ~{v['tokens_est']} tokens")
for name,v in profiles.items():
    if name not in {"full","core"} and v["stack_delta_description_tokens_est"]>650:
        warnings.append(f"{name}: project delta metadata ~{v['stack_delta_description_tokens_est']} tokens")
if overlaps:
    for score,a,b in overlaps[:10]:
        if score>=0.50:
            warnings.append(f"High description overlap {a}<->{b}: {score:.2f}")

print("Trigger overlaps >= 0.34")
if overlaps:
    for score,a,b in overlaps[:20]:
        print(f"- {a} <-> {b}: {score:.2f}")
else:
    print("- none")
print()

print("Duplicate long paragraphs")
if duplicates:
    for para,skills in duplicates[:10]:
        print(f"- {skills}: {para[:130]}...")
else:
    print("- none")
print()

print("Warnings")
if warnings:
    for w in warnings: print("-",w)
else:
    print("- none")

(ROOT/"context-budget-report.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print()
print("JSON:",ROOT/"context-budget-report.json")
