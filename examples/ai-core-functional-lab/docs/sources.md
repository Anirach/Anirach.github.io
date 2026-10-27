# Primary source verification — 2026-10-24

- https://docs.typesafe.ai/models — current stable alias points to jev-1.14.0; version pin, dated pricing and other capabilities.
- https://docs.typesafe.ai/introduction/coding-agents — Jev provides typed discriminative decisions, not code or text generation.
- https://docs.typesafe.ai/api/system-one — REST request/response contract and opt-in feature headers.
- https://docs.typesafe.ai/primitives/choice — closed alternatives, distribution and selected label.
- https://docs.typesafe.ai/primitives/noul — probability of yes, no separate confidence field.
- https://docs.typesafe.ai/confidence — distribution-derived statistic, distinct from observed correctness.
- https://docs.typesafe.ai/sdk/javascript/changelog — SDK0.7.0, Node22+, nullable usage and invalid-request rejection.
- https://docs.typesafe.ai/sdk/javascript/api/interfaces/RetryPolicy — maxRetries2 default means initial plus2 retries; SDK has broader retry behavior than this lab's selected transient fixture.
- https://docs.typesafe.ai/model-jaggedness/jev-1.13 — explicitly older model-specific observations; not a measured claim about1.14.

Our runtime baseline Node22.18+ is a chosen stricter minimum, tested with22.23.2.
No SDK installation, API credentials or live calls were used. Optional text-only
REST adapter is untested live and disabled in CLI. All fixtures, latency, token
usage and most price assumptions are authored examples, never real measurements.
