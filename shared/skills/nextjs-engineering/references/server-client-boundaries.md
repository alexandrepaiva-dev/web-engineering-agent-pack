# Server/client boundaries

Prefer server execution for secrets, privileged DB access, server-only SDKs, authorization and initial data shaping.

Prefer client execution for browser APIs, local interaction state, event handlers and client-only libraries.

Pass serializable values across the boundary.

Never send server-only credentials or unnecessary sensitive data through props.
