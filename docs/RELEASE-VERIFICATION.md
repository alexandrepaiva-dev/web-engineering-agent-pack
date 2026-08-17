# Release Verification

WEAP releases provide two independent integrity/provenance mechanisms.

## 1. SHA-256

Download:

```text
web-engineering-agent-pack-<version>.zip
SHA256SUMS
```

Verify:

```bash
sha256sum -c SHA256SUMS
```

## 2. GitHub artifact attestation

Release workflows generate signed build provenance for the ZIP.

Verify with GitHub CLI:

```bash
gh attestation verify \
  web-engineering-agent-pack-<version>.zip \
  -R OWNER/web-engineering-agent-pack
```

A successful attestation verification establishes that the artifact digest is associated with a GitHub Actions build from the stated repository.

## Self-update

`weap update --apply` requires both the checksum and GitHub attestation by default.

To bypass attestation only when explicitly necessary:

```bash
./weap update --apply --skip-attestation
```

Checksum verification is never skipped.
