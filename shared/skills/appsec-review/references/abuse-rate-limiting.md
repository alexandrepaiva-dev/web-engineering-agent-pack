# Abuse prevention and rate limiting

Protect expensive or sensitive flows such as login, recovery, signup, uploads, invitations, search abuse and external API triggers.

Rate limits should consider:
- identity
- IP/network
- tenant
- operation cost

Do not let distributed attackers bypass a single simplistic key strategy.

Return safe failure semantics and observe sustained abuse.
