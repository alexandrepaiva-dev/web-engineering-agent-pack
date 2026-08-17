# Compatibility Matrix

> Generated documentation for Web Engineering Agent Pack.

| Surface | Linux | macOS | Windows | WSL |
|---|---:|---:|---:|---:|
| Codex global install | ✅ | ✅ | ✅ PowerShell | ✅ |
| Claude Code global install | ✅ | ✅ | ✅ PowerShell | ✅ |
| Project profiles | ✅ | ✅ | ✅ | ✅ |
| Backup / restore | ✅ | ✅ | ✅ | ✅ |
| Uninstall | ✅ | ✅ | ✅ | ✅ |
| `weap` CLI | ✅ | ✅ | ✅ | ✅ |

## Stack profiles

| Profile | Primary stack |
|---|---|
| `core` | Stack-agnostic web engineering |
| `nextjs` | TypeScript, React, Tailwind, Next.js, Node, Auth.js, Prisma, PostgreSQL, BullMQ |
| `nextjs-mysql` | Next.js stack with MySQL |
| `symfony` | PHP, Symfony, Symfony Security, Doctrine, MySQL, Twig |
| `symfony-postgresql` | Symfony stack with PostgreSQL |
| `full` | All first-party stack skills |

## MCP compatibility

| MCP capability | Codex | Claude Code |
|---|---:|---:|
| stdio | ✅ | ✅ |
| Streamable HTTP / HTTP | ✅ | ✅ |
| Project scope | ✅ | ✅ |
| User scope | ✅ | ✅ |
| Environment-backed secrets | ✅ | ✅ |
| Client OAuth flows | ✅ | ✅ |
| WEAP risk policy | ✅ | ✅ |
| Project lock verification | ✅ | ✅ |

## Runtime prerequisites

- Python 3
- Git for locked third-party installation
- Bash on Linux/macOS/WSL
- PowerShell on Windows
- Node.js/npx only for workflows that explicitly require Node tooling
