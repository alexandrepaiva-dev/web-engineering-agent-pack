# Secrets and dependency risk

Secrets belong in managed environment/secret stores, not source code or images.

Rotate leaked credentials.

Review dependency changes for:
- abandoned packages
- unexpected install scripts
- compromised/transitive risk
- large new attack surface

Prefer framework/platform primitives when they reduce dependency risk.
