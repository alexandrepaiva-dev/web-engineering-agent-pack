# Email architecture

Prefer application event/business decision -> durable queue -> provider send -> provider delivery events.

The HTTP request that triggers a transactional email usually should not wait on actual delivery.

Store enough delivery metadata for diagnostics without retaining unnecessary message content.
