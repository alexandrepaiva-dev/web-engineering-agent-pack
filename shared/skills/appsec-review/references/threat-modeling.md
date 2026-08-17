# Threat modeling

Identify:
- valuable assets
- actors
- trust boundaries
- entry points
- privileged operations
- abuse cases

Focus on plausible threats for the actual architecture.

For each sensitive flow ask:
1. what can an attacker control?
2. what trusted decision consumes it?
3. what prevents cross-user/tenant impact?
4. how is replay/automation constrained?
