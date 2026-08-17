
import json,os,subprocess,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class DistributionTest(unittest.TestCase):
    def test_release_attestation_is_pinned(self):
        text=(ROOT/".github/workflows/release.yml").read_text()
        self.assertIn("actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6",text)
        self.assertIn("attestations: write",text)
        self.assertIn("id-token: write",text)

    def test_pages_actions_are_pinned(self):
        text=(ROOT/".github/workflows/pages.yml").read_text()
        for sha in [
            "45bfe0192ca1faeb007ade9deae92b16b8254a0d",
            "fc324d3547104276b827a68afc52ff2a11cc49c9",
            "cd2ce8fcbc39b97be8ca5fce6e763baed58fa128",
        ]:
            self.assertIn(sha,text)

    def test_site_build_uses_manifest(self):
        env=os.environ.copy()
        env["GITHUB_REPOSITORY"]="example/web-engineering-agent-pack"
        r=subprocess.run([sys.executable,str(ROOT/"scripts/build-site.py")],cwd=ROOT,env=env,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr)
        data=(ROOT/"_site/site-data.js").read_text()
        self.assertIn("example/web-engineering-agent-pack",data)
        self.assertIn(json.loads((ROOT/"manifest.json").read_text())["version"],data)
        self.assertTrue((ROOT/"_site/index.html").exists())

if __name__=="__main__":
    unittest.main()
