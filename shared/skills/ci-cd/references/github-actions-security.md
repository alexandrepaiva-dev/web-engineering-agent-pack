# GitHub Actions security

Use least-privilege `permissions`.

Treat pull requests from forks as untrusted.

Do not expose repository/environment secrets to untrusted code.

Pin third-party actions according to security policy.

Be cautious with `pull_request_target` and workflows that execute attacker-controlled code.
