# Pipeline design

Separate concerns:
- install/build
- static checks
- tests
- artifact/image build
- deploy
- post-deploy verification

Fail early on cheap checks.

Avoid rebuilding the same immutable artifact separately for every deployment stage when promotion is possible.
