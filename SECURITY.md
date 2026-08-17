# Security Policy

## Reporting vulnerabilities

Please report security issues privately rather than opening a public issue.

For a public GitHub repository, configure a GitHub private vulnerability reporting channel under **Security → Advisories**.

Do not include real credentials, tokens, private repository data, or production configuration in reports.

## Security-sensitive areas

Treat changes to these areas as high risk:
- installers and uninstallers
- backup/restore
- third-party skill installation
- GitHub Actions workflows
- path handling
- shell command construction
- project skill overwrite logic
- state and manifest parsing

## Supply-chain policy

Third-party skills are recorded in `third-party.lock.json`.

Updates should:
1. resolve the upstream commit explicitly
2. review upstream changes
3. update the lock file
4. run CI
5. merge deliberately

Do not silently follow an upstream branch HEAD in production automation.
