import importlib.util,json,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

pm=load("pm",ROOT/"scripts/profile_manager.py")
pb=load("pb",ROOT/"scripts/project_backup.py")

class ProjectBackupTest(unittest.TestCase):
    def args(self,p,profile,force=False):
        return SimpleNamespace(
            project_dir=str(p),profile=profile,include_core=False,
            add_skill=[],remove_skill=[],target="both",
            init_project=False,dry_run=False,force=force
        )

    def test_restore_previous_profile_skills(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            pm.install_project(self.args(p,"nextjs"))
            pm.install_project(self.args(p,"symfony",force=True))
            self.assertTrue((p/".agents/skills/symfony-engineering").exists())
            pb.restore(p,"latest")
            mf=json.loads((p/".web-engineering-agent-pack.json").read_text())
            self.assertEqual(mf["profile"],"nextjs")
            self.assertTrue((p/".agents/skills/nextjs-engineering").exists())
            self.assertFalse((p/".agents/skills/symfony-engineering").exists())

if __name__=="__main__":
    unittest.main()
