from pathlib import Path
import json,os,shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"_site"
SRC=ROOT/"site"

def main():
    shutil.rmtree(OUT,ignore_errors=True)
    shutil.copytree(SRC,OUT)
    manifest=json.loads((ROOT/"manifest.json").read_text())
    profiles=[]
    for p in sorted((ROOT/"profiles").glob("*.json")):
        if p.stem=="catalog": continue
        d=json.loads(p.read_text())
        profiles.append({
            "name":d["name"],
            "description":d.get("description",""),
            "skills":d.get("skills",[]),
        })
    repo=os.environ.get("GITHUB_REPOSITORY","")
    server=os.environ.get("GITHUB_SERVER_URL","https://github.com")
    repo_url=f"{server}/{repo}" if repo else "https://github.com/"
    mcp_profiles=[]
    for p in sorted((ROOT/"mcp/profiles").glob("*.json")):
        d=json.loads(p.read_text())
        mcp_profiles.append({
            "name":d["name"],
            "description":d.get("description",""),
            "skills":d.get("servers",[]),
        })
    data={
        "version":manifest["version"],
        "skillCount":manifest.get("skillCount",len(manifest.get("skills",[]))),
        "repositoryUrl":repo_url,
        "profiles":profiles,
        "mcpProfiles":mcp_profiles,
    }
    (OUT/"site-data.js").write_text("window.WEAP_SITE="+json.dumps(data,separators=(",",":"))+";\n",encoding="utf-8")
    (OUT/".nojekyll").write_text("",encoding="utf-8")
    print("Built GitHub Pages site:",OUT)

if __name__=="__main__":
    main()
