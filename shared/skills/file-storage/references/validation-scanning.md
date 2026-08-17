# Validation and scanning

Validate magic/content signatures when the file type matters.

For risky uploads consider:
upload -> quarantine -> scan/validate -> promote/publish.

Scanning failure should fail safely.

Resource-limit parsers and scanners to avoid decompression/image bombs.
