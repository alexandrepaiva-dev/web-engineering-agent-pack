# GitHub Pages

The repository includes a dependency-free static site in `site/`.

## One-time GitHub setup

After pushing the repository:

1. Open the repository on GitHub.
2. Open **Settings**.
3. Under **Code and automation**, select **Pages**.
4. Set the publishing source to **GitHub Actions**.
5. Push to `main` or manually run the **Pages** workflow.

The deployment workflow is:

```text
.github/workflows/pages.yml
```

It builds `_site/` from:

```text
site/
manifest.json
profiles/*.json
```

## Local build

```bash
python scripts/build-site.py
```

Open `_site/index.html` in a browser or serve `_site/` with any local static HTTP server.

## Default project-site URL

For a repository named:

```text
OWNER/web-engineering-agent-pack
```

the normal GitHub Pages project-site form is:

```text
https://OWNER.github.io/web-engineering-agent-pack/
```

A custom domain can be configured later in GitHub Pages settings.

## Design

The site deliberately uses plain HTML, CSS, and a small amount of JavaScript. It does not add React, Next.js, npm dependencies, or a frontend build tool to the pack itself.
