# Workflow Overview

This companion workflow turns edge analytics concepts into executable artifacts.

## Main computational path

1. Load signal, preprocessing, window, feature, event, buffer, replay, uplink, SLO, readiness, and security manifests.
2. Generate synthetic local stream events and windowed feature outputs.
3. Validate local preprocessing, missing-sample handling, and unit consistency.
4. Build event-time windows and compute features.
5. Apply rule-based event logic and local inference stubs.
6. Store events locally with retention, priority, and idempotency keys.
7. Route events through selective uplink: immediate, deferred, sampled, summarized, suppressed, or dropped.
8. Validate replay behavior for delayed, duplicate, partial, corrected, and backfilled records.
9. Check analytics SLOs for freshness, latency, backlog, replay lag, feature completeness, lineage completeness, and drop transparency.
10. Export analytics events, replay records, SLO reports, readiness checks, and fleet summaries.
11. Use R to report fleet-level local analytics behavior across sites, gateways, feature versions, and uplink modes.

## Engineering emphasis

The code is designed around practical edge analytics questions:

- What raw signal produced the local output?
- Which preprocessing and feature versions were used?
- What event-time window produced the feature or event?
- Is the output fresh, delayed, replayed, or backfilled?
- Does the local output preserve enough lineage?
- Was the event forwarded immediately, deferred, sampled, suppressed, or dropped?
- Does replay preserve ordering and idempotency?
- Do analytics SLOs reveal degradation before the pipeline becomes misleading?
