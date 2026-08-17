from pathlib import Path
import importlib.util,json,sys

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("pm",ROOT/"scripts/profile_manager.py")
pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)
errors=[];warnings=[]
names={p.stem for p in (ROOT/"profiles").glob("*.json") if p.stem!="catalog"}
for name in sorted(names):
    data=json.loads((ROOT/"profiles"/f"{name}.json").read_text())
    for parent in data.get("extends",[]):
        if parent not in names:errors.append(f"{name}: unknown parent {parent}")
    if len(data.get("skills",[]))!=len(set(data.get("skills",[]))):errors.append(f"{name}: duplicate skills")
    try:resolved=pm.resolve_profile(name)
    except Exception as e:errors.append(f"{name}: {e}");continue
    for removed in data.get("removeSkills",[]):
        if removed in resolved:errors.append(f"{name}: removeSkills did not remove {removed}")
    if name!="core" and not resolved:warnings.append(f"{name}: resolves empty")
print(f"Profile lint: {len(errors)} errors, {len(warnings)} warnings")
for e in errors:print("ERROR:",e)
for x in warnings:print("WARN:",x)
raise SystemExit(1 if errors else 0)
