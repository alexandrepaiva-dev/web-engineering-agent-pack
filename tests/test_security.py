import importlib.util,json,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("pm",ROOT/"scripts/profile_manager.py")
pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)

class SecurityTest(unittest.TestCase):
    def test_profile_path_traversal_rejected(self):
        with self.assertRaises(SystemExit):
            pm.load_profile("../../etc/passwd")

    def test_profile_absolute_path_rejected(self):
        with self.assertRaises(SystemExit):
            pm.load_profile("/tmp/x")

    def test_managed_symlink_is_unlinked_not_followed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            external=p/"external"
            external.mkdir()
            marker=external/"marker"
            marker.write_text("safe")
            link=p/"managed"
            try:
                link.symlink_to(external,target_is_directory=True)
            except OSError as error:
                self.skipTest(f"Symlinks are unavailable in this environment: {error}")
            pm.safe_remove_managed_path(link)
            self.assertFalse(link.exists())
            self.assertEqual(marker.read_text(),"safe")

    def test_invalid_manifest_json_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            (p/".web-engineering-agent-pack.json").write_text("{broken")
            self.assertEqual(pm.read_project_manifest(p),{})

if __name__=="__main__":
    unittest.main()
