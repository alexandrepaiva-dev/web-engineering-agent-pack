from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
try:
    import jsonschema
except ImportError:
    print("jsonschema is required: python -m pip install jsonschema",file=sys.stderr)
    raise SystemExit(2)

def validate(instance_path,schema_path):
    instance=json.loads(Path(instance_path).read_text(encoding="utf-8"))
    schema=json.loads(Path(schema_path).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(instance)

for p in (ROOT/"profiles").glob("*.json"):
    if p.name!="catalog.json":
        validate(p,ROOT/"schemas/profile.schema.json")

validate(ROOT/"manifest.json",ROOT/"schemas/repository-manifest.schema.json")
validate(ROOT/"third-party.lock.json",ROOT/"schemas/third-party-lock.schema.json")
for p in (ROOT/"mcp/registry").glob("*.json"):
    validate(p,ROOT/"schemas/mcp-server.schema.json")
for p in (ROOT/"mcp/profiles").glob("*.json"):
    validate(p,ROOT/"schemas/mcp-profile.schema.json")
validate(ROOT/"tests/fixtures/mcp-state.json",ROOT/"schemas/mcp-state.schema.json")
validate(ROOT/"tests/fixtures/project-manifest.json",ROOT/"schemas/project-manifest.schema.json")
validate(ROOT/"tests/fixtures/project-lock.json",ROOT/"schemas/project-lock.schema.json")
validate(ROOT/"tests/fixtures/install-state.json",ROOT/"schemas/install-state.schema.json")
validate(ROOT/"tests/fixtures/backup-manifest.json",ROOT/"schemas/backup-manifest.schema.json")
print("Schema validation OK.")
