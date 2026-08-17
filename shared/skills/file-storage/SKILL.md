---
name: file-storage
description: S3/R2-style object storage engineering. Use for uploads, presigned URLs, object access, MIME/size validation, scanning, image processing, CDN delivery, retention, or file security.
---


# File Storage

Treat file uploads as untrusted binary input and object storage as a separate security boundary.

## Workflow

1. Define file purpose, sensitivity and retention.
2. Define allowed size/type/content rules.
3. Choose direct-to-storage vs server-proxied upload.
4. Define object-key strategy and ownership metadata.
5. Define public/private access model.
6. Validate authorization for upload/read/delete.
7. Define post-upload processing/scanning.
8. Define lifecycle, cleanup and orphan handling.
9. Define CDN/cache behavior.
10. Test malicious and failure cases.

## Principles

- Never trust filename extension or browser MIME alone.
- Generate storage keys server-side.
- Do not let user-controlled paths escape intended namespaces.
- Presigned URLs must be scoped, short-lived and operation-specific.
- Private objects require authorization before URL issuance.
- Large uploads need explicit limits.
- File deletion should consider dependent database records and retention policy.
- Image/media processing must not trust malformed input.

## References

- `references/upload-security.md`
- `references/presigned-urls.md`
- `references/object-keys-access.md`
- `references/validation-scanning.md`
- `references/image-processing.md`
- `references/cdn-caching.md`
- `references/lifecycle-retention.md`
- `references/testing.md`
