## Next.js stack

Expected profile:
- TypeScript
- React
- Tailwind CSS
- Next.js App Router
- Node.js
- Auth.js
- Prisma ORM
- PostgreSQL by default
- Redis/Valkey + BullMQ where used

Rules:
- prefer Server Components
- keep client boundaries small
- keep secrets and privileged operations server-side
- inspect installed versions before using version-sensitive APIs
- enforce authorization independently of hidden UI controls
- Prisma schema changes require migration review
- use the selected database vendor skill for engine-specific behavior
