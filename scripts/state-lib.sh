STATE_FILE="${AI_AGENT_PACK_STATE_FILE:-$HOME/.ai-agent-pack-state.json}"

write_install_state() {
  local profile="$1"
  local target="$2"
  local third_party="${3:-false}"
  shift 3 || true
  local py="python3"
  command -v python3 >/dev/null 2>&1 || py="python"

  "$py" - "$STATE_FILE" "$profile" "$target" "$third_party" "$@" <<'PY'
import json,sys
from pathlib import Path

path=Path(sys.argv[1])
profile=sys.argv[2]
target=sys.argv[3]
third=sys.argv[4].lower()=="true"
skills=sys.argv[5:]

old={}
if path.exists():
    try: old=json.loads(path.read_text())
    except Exception: old={}

old_target=old.get("target")
if old_target and old_target != target and {old_target,target} <= {"codex","claude"}:
    merged_target="both"
elif old_target=="both" or target=="both":
    merged_target="both"
else:
    merged_target=target

old_skills=old.get("firstPartySkills",[])
merged_skills=sorted(set(old_skills)|set(skills))

state={
    "schemaVersion":1,
    "packVersion":"1.0.0",
    "profile":profile,
    "target":merged_target,
    "thirdPartyInstalledByPack":bool(old.get("thirdPartyInstalledByPack")) or third,
    "firstPartySkills":merged_skills,
    "recommendedThirdPartySkills":["ui-ux-pro-max","web-quality-audit"],
}
path.write_text(json.dumps(state,indent=2)+"\n")
PY
}
