import importlib.util,json,tempfile,unittest,os
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("migmatrix",ROOT/"scripts/migrate.py")
mig=importlib.util.module_from_spec(spec);spec.loader.exec_module(mig)
FIX=ROOT/"tests/fixtures/migrations"

class MigrationMatrixTest(unittest.TestCase):
    def test_historical_sources_are_real_archives(self):
        for v in (7,8,9):
            meta=json.loads((FIX/f"v{v}/source-archive.json").read_text())
            self.assertEqual(meta["sourceManifestVersion"],f"{v}.0.0")
            self.assertRegex(meta["sha256"],r"^[a-f0-9]{64}$")
            self.assertIn("sourceManifest",meta)

    def test_project_matrix_v7_v8_v9_to_v1(self):
        for v in (7,8,9):
            with self.subTest(v=v), tempfile.TemporaryDirectory() as td:
                p=Path(td)
                source=json.loads((FIX/f"v{v}/project-manifest.json").read_text())
                mf=p/".web-engineering-agent-pack.json"
                mf.write_text(json.dumps(source))
                mig.migrate_project(p,True)
                data=json.loads(mf.read_text())
                self.assertEqual(data["packVersion"],"1.0.0")
                self.assertIn("createdFiles",data)
                self.assertIn("skillHashes",data)
                self.assertTrue(list(p.glob(".web-engineering-agent-pack.json.pre-v1-*.bak")))

    def test_global_matrix_v7_v8_v9_to_v1(self):
        for v in (7,8,9):
            with self.subTest(v=v), tempfile.TemporaryDirectory() as td:
                sf=Path(td)/"state.json"
                sf.write_text((FIX/f"v{v}/install-state.json").read_text())
                with patch.dict(os.environ,{"AI_AGENT_PACK_STATE_FILE":str(sf)}):
                    mig.migrate_global(True)
                data=json.loads(sf.read_text())
                self.assertEqual(data["packVersion"],"1.0.0")
                self.assertIn("recommendedThirdPartySkills",data)
                self.assertIn("thirdPartyInstalledByPack",data)

if __name__=="__main__":
    unittest.main()
