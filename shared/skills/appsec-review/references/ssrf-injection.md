# SSRF and injection

Treat user-controlled URLs as dangerous when fetched server-side.

Constrain:
- scheme
- host
- redirects
- private/internal networks
- DNS rebinding implications
- response size/time

Use parameterized DB queries.

Avoid shell command construction from untrusted strings.

Validate and constrain templating/path inputs used in sensitive sinks.
