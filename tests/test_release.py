import importlib.util,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("release",ROOT/"scripts/release.py")
rel=importlib.util.module_from_spec(spec);spec.loader.exec_module(rel)

class ReleaseTest(unittest.TestCase):
    def test_semver(self):
        for v in ["1.0.0","1.1.0","2.0.0-preview.1"]:
            self.assertTrue(rel.SEMVER.fullmatch(v))
        for v in ["v1","1","1.0","1.0.0.1","../1.0.0"]:
            self.assertFalse(rel.SEMVER.fullmatch(v))

if __name__=="__main__":
    unittest.main()
