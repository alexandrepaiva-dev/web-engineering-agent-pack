import importlib.util,json,os,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("mcp_manager",ROOT/"scripts/mcp_manager.py")
mcp=importlib.util.module_from_spec(spec);spec.loader.exec_module(mcp)

class McpManagerTest(unittest.TestCase):
    def install_args(self,project,server,target="both",allow=False,force=False):
        return SimpleNamespace(
            project_dir=str(project),scope="project",server=[server],profile=[],
            target=target,allow_high_risk=allow,force=force,dry_run=False
        )

    def test_project_install_preserves_unrelated_config(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            (p/".codex").mkdir()
            (p/".codex/config.toml").write_text('model = "example"\n',encoding="utf-8")
            (p/".mcp.json").write_text(json.dumps({"mcpServers":{"custom":{"command":"custom"}}}),encoding="utf-8")
            mcp.cmd_install(self.install_args(p,"playwright"))
            codex=(p/".codex/config.toml").read_text()
            self.assertIn('model = "example"',codex)
            self.assertIn("[mcp_servers.playwright]",codex)
            claude=json.loads((p/".mcp.json").read_text())
            self.assertIn("custom",claude["mcpServers"])
            self.assertIn("playwright",claude["mcpServers"])
            state=json.loads((p/".web-engineering-agent-pack.mcp.json").read_text())
            self.assertIn("playwright",state["servers"])

    def test_high_risk_requires_explicit_flag(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            with self.assertRaises(SystemExit):
                mcp.cmd_install(self.install_args(p,"filesystem-project",allow=False))

    def test_project_filesystem_is_scoped_per_client(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            mcp.cmd_install(self.install_args(p,"filesystem-project",allow=True))
            codex=(p/".codex/config.toml").read_text()
            # TOML strings escape Windows path separators.
            self.assertIn(json.dumps(str(p))[1:-1],codex)
            claude=json.loads((p/".mcp.json").read_text())
            args=claude["mcpServers"]["filesystem-project"]["args"]
            self.assertIn("${CLAUDE_PROJECT_DIR:-.}",args)

    def test_disable_keeps_codex_definition_but_removes_claude_server(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            mcp.cmd_install(self.install_args(p,"playwright"))
            args=SimpleNamespace(project_dir=str(p),scope="project",name="playwright",force=False)
            mcp.set_enabled(args,False)
            self.assertIn("enabled = false",(p/".codex/config.toml").read_text())
            claude=json.loads((p/".mcp.json").read_text())
            self.assertNotIn("playwright",claude["mcpServers"])

    def test_project_required_server_rejected_at_user_scope(self):
        server=mcp.load_server("filesystem-project")
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(SystemExit):
                mcp.require_allowed(server,"user",Path(td),True)


    def test_reset_preserves_unmanaged_claude_server(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            (p/".mcp.json").write_text(json.dumps({"mcpServers":{"manual":{"command":"manual"}}}),encoding="utf-8")
            mcp.cmd_install(self.install_args(p,"playwright",target="claude"))
            args=SimpleNamespace(project_dir=str(p),scope="project",yes=True,dry_run=False,force=False)
            mcp.cmd_reset(args)
            claude=json.loads((p/".mcp.json").read_text())
            self.assertIn("manual",claude["mcpServers"])
            self.assertNotIn("playwright",claude["mcpServers"])
            self.assertFalse((p/".web-engineering-agent-pack.mcp.json").exists())

    def test_registry_contains_no_literal_secret_fields(self):
        forbidden={"apiKey","password","token","secret","bearerToken"}
        for p in mcp.REGISTRY.glob("*.json"):
            data=json.loads(p.read_text())
            self.assertTrue(forbidden.isdisjoint(data.keys()),p.name)

if __name__=="__main__":
    unittest.main()
