from pathlib import Path
import json,re,unittest

ROOT=Path(__file__).resolve().parents[1]

class DocsConsistency(unittest.TestCase):
    def test_manifest_counts(self):
        m=json.loads((ROOT/"manifest.json").read_text())
        skills=[p for p in (ROOT/"shared/skills").iterdir() if p.is_dir()]
        profiles=[p for p in (ROOT/"profiles").glob("*.json") if p.stem!="catalog"]
        self.assertEqual(set(m["skills"]),{p.name for p in skills})
        self.assertEqual(m.get("skillCount",len(skills)),len(skills))
        self.assertEqual(m.get("profileCount",len(profiles)),len(profiles))

    def test_current_version_consistency(self):
        m=json.loads((ROOT/"manifest.json").read_text())
        self.assertEqual(m["version"],"1.0.0")
        self.assertIn("# 6. MCP support",(ROOT/"README.md").read_text())

    def test_readme_commands_exist(self):
        readme=(ROOT/"README.md").read_text()
        for cmd in [
            "./weap install","./weap project init","./weap project uninstall",
            "./weap backup restore","./weap mcp install","./weap mcp doctor",
            "validate-pack.py"
        ]:
            self.assertIn(cmd,readme)

if __name__=="__main__":
    unittest.main()
