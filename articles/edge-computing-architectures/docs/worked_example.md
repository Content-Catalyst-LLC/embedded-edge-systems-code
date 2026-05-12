# Worked Example: Industrial Site Edge Architecture During Cloud Outage

A cloud link becomes unavailable for forty-five minutes while one rotating machine begins showing abnormal vibration.

- Endpoint continues sampling.
- Embedded runtime computes a local health flag.
- Gateway buffers feature windows and event records.
- Local edge node raises a site alarm within its local decision boundary.
- Site dashboard shows degraded connectivity, local event time, buffer backlog, and raw-window retention status.
- Noncritical summaries are throttled.
- Priority telemetry is retained.
- When cloud connectivity returns, the gateway replays delayed records with event time, upload time, ingestion time, idempotency keys, and gap markers.
