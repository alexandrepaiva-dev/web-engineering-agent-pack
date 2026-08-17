import importlib.util,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

pm=load("pm_lock_test",ROOT/"scripts/profile_manager.py")
pl=load("pl_lock_test",ROOT/"scripts/project_lock.py")

class ProjectLockTest(unittest.TestCase):
    def args(self,p):
        return SimpleNamespace(
            project_dir=str(p),profile="nextjs",include_core=True,
            add_skill=[],remove_skill=[],target="both",init_project=False,
            dry_run=False,force=False
        )

    def test_write_verify_and_hash_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            pm.install_project(self.args(p))
            pl.write_lock(p)
            self.assertEqual(pl.verify(p),0)
            data=json.loads((p/pl.LOCK_NAME).read_text())
            first=data["skills"][0]
            data["sourceSkillHashes"][first]="0"*64
            (p/pl.LOCK_NAME).write_text(json.dumps(data))
            self.assertEqual(pl.verify(p),1)

if __name__=="__main__":
    unittest.main()
