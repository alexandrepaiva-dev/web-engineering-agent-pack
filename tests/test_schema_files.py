from pathlib import Path
import json,unittest

ROOT=Path(__file__).resolve().parents[1]

class SchemaFilesTest(unittest.TestCase):
    def test_schemas_are_json(self):
        files=list((ROOT/"schemas").glob("*.json"))
        self.assertGreaterEqual(len(files),5)
        for f in files:
            data=json.loads(f.read_text())
            self.assertIn("$schema",data)

    def test_third_party_commits_are_pinned(self):
        data=json.loads((ROOT/"third-party.lock.json").read_text())
        for dep in data["dependencies"]:
            self.assertRegex(dep["commit"],r"^[a-f0-9]{40}$")

if __name__=="__main__":
    unittest.main()
