import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const pkgPath = join(root, "package.json");

if (!existsSync(pkgPath)) process.exit(0);

const pkg = JSON.parse(readFileSync(pkgPath, "utf8"));
const scripts = pkg.scripts || {};

const manager =
  existsSync(join(root, "pnpm-lock.yaml")) ? "pnpm" :
  existsSync(join(root, "yarn.lock")) ? "yarn" :
  existsSync(join(root, "bun.lockb")) || existsSync(join(root, "bun.lock")) ? "bun" :
  "npm";

const script = scripts.typecheck ? "typecheck" : scripts.lint ? "lint" : null;
if (!script) process.exit(0);

const args = manager === "npm" ? ["run", script] : [script];

const result = spawnSync(manager, args, {
  cwd: root,
  stdio: "inherit",
  shell: process.platform === "win32"
});

process.exit(result.status ?? 1);
