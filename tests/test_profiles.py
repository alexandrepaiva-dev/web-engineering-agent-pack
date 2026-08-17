import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("pm",ROOT/"scripts/profile_manager.py")
pm=importlib.util.module_from_spec(spec);spec.loader.exec_module(pm)

class ProfilesTest(unittest.TestCase):
    def test_required_profiles_resolve(self):
        for name in ["core","nextjs","symfony","nextjs-mysql","symfony-postgresql","full"]:
            skills=pm.resolve_profile(name)
            self.assertTrue(skills)
            for skill in skills:
                self.assertTrue((ROOT/"shared/skills"/skill/"SKILL.md").exists(), skill)

    def test_stack_deltas_do_not_cross(self):
        n=set(pm.resolve_stack_only("nextjs"))
        s=set(pm.resolve_stack_only("symfony"))
        self.assertNotIn("symfony-engineering",n)
        self.assertNotIn("nextjs-engineering",s)
        self.assertTrue(n.isdisjoint(set(pm.resolve_profile("core"))))
        self.assertTrue(s.isdisjoint(set(pm.resolve_profile("core"))))

    def test_database_variants(self):
        n=set(pm.resolve_profile("nextjs-mysql"))
        self.assertIn("mysql-engineering",n)
        self.assertNotIn("postgresql-engineering",n)
        s=set(pm.resolve_profile("symfony-postgresql"))
        self.assertIn("postgresql-engineering",s)
        self.assertNotIn("mysql-engineering",s)

if __name__=="__main__":
    unittest.main()
