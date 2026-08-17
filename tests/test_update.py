import importlib.util,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("upd",ROOT/"scripts/update.py")
upd=importlib.util.module_from_spec(spec);spec.loader.exec_module(upd)

class UpdateTest(unittest.TestCase):
    def test_repo_url_normalization(self):
        self.assertEqual(upd.normalize_repo_url("https://github.com/alex/web-engineering-agent-pack.git"),"alex/web-engineering-agent-pack")
        self.assertEqual(upd.normalize_repo_url("git@github.com:alex/web-engineering-agent-pack.git"),"alex/web-engineering-agent-pack")
        self.assertIsNone(upd.normalize_repo_url("https://gitlab.com/a/b"))

    def test_semver_order(self):
        self.assertTrue(upd.newer("2.0.0","1.9.9"))
        self.assertTrue(upd.newer("2.0.0","2.0.0-preview.1"))
        self.assertFalse(upd.newer("2.0.0-preview.1","2.0.0"))

    def test_release_selection(self):
        releases=[
          {"tag_name":"v2.0.0","draft":False,"prerelease":False},
          {"tag_name":"v2.1.0-preview.1","draft":False,"prerelease":True},
          {"tag_name":"v1.9.0","draft":False,"prerelease":False},
        ]
        self.assertEqual(upd.choose_release(releases,"stable","1.0.0")["tag_name"],"v2.0.0")
        self.assertEqual(upd.choose_release(releases,"preview","1.0.0")["tag_name"],"v2.1.0-preview.1")

if __name__=="__main__":
    unittest.main()
