import importlib.util, tempfile, unittest, json
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("pm",ROOT/"scripts/profile_manager.py")
pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)

class ProjectLifecycleTest(unittest.TestCase):
    def args(self, project, profile="nextjs", force=False, init=True):
        return SimpleNamespace(
            project_dir=str(project), profile=profile, include_core=False,
            add_skill=[], remove_skill=[], target="both", init_project=init,
            dry_run=False, force=force
        )

    def test_install_creates_hashes_and_backup_on_update(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            pm.install_project(self.args(p))
            mf=json.loads((p/".web-engineering-agent-pack.json").read_text())
            self.assertTrue(mf["skillHashes"])
            self.assertTrue((p/".agents/skills/nextjs-engineering").exists())

            pm.install_project(self.args(p))
            backups=list((p/".web-engineering-agent-pack-backups").iterdir())
            self.assertTrue(backups)

    def test_local_modification_refuses_without_force(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            pm.install_project(self.args(p))
            skill=p/".agents/skills/nextjs-engineering/SKILL.md"
            skill.write_text(skill.read_text()+"\nLOCAL CHANGE\n")
            with self.assertRaises(SystemExit):
                pm.install_project(self.args(p,force=False))
            pm.install_project(self.args(p,force=True))

    def test_custom_skill_survives_profile_update(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            custom=p/".agents/skills/company-custom"
            custom.mkdir(parents=True)
            (custom/"SKILL.md").write_text("---\nname: company-custom\ndescription: custom\n---\n")
            pm.install_project(self.args(p,"nextjs"))
            pm.install_project(self.args(p,"symfony",force=True,init=False))
            self.assertTrue(custom.exists())
            self.assertTrue((p/".agents/skills/symfony-engineering").exists())
            self.assertFalse((p/".agents/skills/nextjs-engineering").exists())

if __name__=="__main__":
    unittest.main()
