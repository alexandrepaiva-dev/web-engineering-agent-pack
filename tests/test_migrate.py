import importlib.util,json,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("mig",ROOT/"scripts/migrate.py")
mig=importlib.util.module_from_spec(spec);spec.loader.exec_module(mig)

class MigrationTest(unittest.TestCase):
    def test_project_preview_and_apply(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            mf=p/".web-engineering-agent-pack.json"
            mf.write_text(json.dumps({
                "schemaVersion":1,"packVersion":"8.0.0","profile":"nextjs",
                "includeCore":False,"target":"both","skills":["nextjs-engineering"]
            }))
            mig.migrate_project(p,False)
            self.assertEqual(json.loads(mf.read_text())["packVersion"],"8.0.0")
            mig.migrate_project(p,True)
            data=json.loads(mf.read_text())
            self.assertEqual(data["packVersion"],"1.0.0")
            self.assertIn("createdFiles",data)
            self.assertTrue(list(p.glob(".web-engineering-agent-pack.json.pre-v1-*.bak")))

if __name__=="__main__":
    unittest.main()
