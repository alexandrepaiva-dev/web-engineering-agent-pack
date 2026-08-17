# Node runtime in containers

Ensure correct Node major, required build output, expected bind address/port and proper signal handling.

Avoid wrappers that swallow SIGTERM.

Gracefully close HTTP servers/workers/connections where needed.

For Next.js standalone output, follow requirements of the installed Next.js version.
