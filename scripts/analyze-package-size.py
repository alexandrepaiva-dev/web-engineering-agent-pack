from pathlib import Path
import importlib.util,json

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("pm",ROOT/"scripts/profile_manager.py")
pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)

def size(path: Path):
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())

all_bytes=size(ROOT/"shared"/"skills")
profiles={}
core=set(pm.resolve_profile("core"))
for p in sorted((ROOT/"profiles").glob("*.json")):
    if p.stem=="catalog":continue
    eff=pm.resolve_profile(p.stem)
    delta=eff if p.stem=="core" else [s for s in eff if s not in core]
    profiles[p.stem]={
        "effectiveSkills":len(eff),
        "effectiveBytes":sum(size(ROOT/"shared"/"skills"/s) for s in eff),
        "projectDeltaSkills":len(delta),
        "projectDeltaBytes":sum(size(ROOT/"shared"/"skills"/s) for s in delta),
    }

report={"allSkillBytes":all_bytes,"profiles":profiles}
(ROOT/"package-size-report.json").write_text(json.dumps(report,indent=2)+"\n")
print("WEAP package/profile size")
print("="*72)
print(f"All first-party skills: {all_bytes/1024:.1f} KiB")
for name,v in profiles.items():
    print(f"{name:22} effective={v['effectiveBytes']/1024:7.1f} KiB  project-delta={v['projectDeltaBytes']/1024:7.1f} KiB")
print("JSON:",ROOT/"package-size-report.json")
