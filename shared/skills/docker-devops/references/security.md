# Container security

- run non-root where practical
- minimize runtime tools/packages
- never copy `.env`, SSH keys, cloud credentials or package tokens into image layers
- use build-secret mechanisms for build-time secrets
- avoid privileged containers without a documented need
- maintain base images through normal security updates
