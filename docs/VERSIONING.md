# Versioning and Release Policy

Public versioning starts at 1.0.0. Earlier numbered artifacts were internal development builds, not public SemVer releases.

Web Engineering Agent Pack follows Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

## MAJOR

Use a major version when a change requires migration or materially changes the contract of:

- profile resolution
- manifest/state schemas
- install/uninstall semantics
- backup/restore semantics
- CLI command compatibility
- project lockfile compatibility

## MINOR

Use a minor version for backward-compatible capabilities such as:

- new stack/profile
- new skill
- new CLI command
- new optional integration
- new diagnostic/reporting capability

## PATCH

Use a patch release for backward-compatible:

- bug fixes
- documentation corrections
- test improvements
- trigger refinements that do not change profile contracts
- installer robustness fixes

## Preview releases

Pre-release versions use SemVer prerelease identifiers:

```text
1.1.0-preview.1
1.1.0-rc.1
```

Release channel:

```text
stable
preview
```

Git tags should match the release version:

```text
v1.0.0
v1.1.0-preview.1
```

## Required release gates

Before publication:

```bash
./weap audit
python -m unittest discover -s tests -p "test_*.py"
bash tests/run-shell-tests.sh
```

Windows CI must also pass.

The release command generates SHA-256 checksums and release metadata.
