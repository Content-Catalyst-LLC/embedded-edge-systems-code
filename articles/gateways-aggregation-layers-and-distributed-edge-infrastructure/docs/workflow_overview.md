# Workflow Overview

This companion workflow turns gateway and aggregation concepts into executable artifacts.

## Main computational path

1. Load gateway, child-device, protocol, aggregation, buffer, replay, selective-forwarding, local-policy, SLO, and security manifests.
2. Simulate a gateway with heterogeneous child devices.
3. Generate child-device telemetry with acquisition time, protocol identity, quality flags, and local units.
4. Normalize device events through protocol maps.
5. Buffer events when upstream connectivity is degraded.
6. Aggregate device streams into site-level state with freshness, missing-child, and lineage metrics.
7. Select what is forwarded upstream, retained locally, summarized, or dropped under pressure.
8. Validate replay semantics, deduplication, late-arrival behavior, and gap reporting.
9. Evaluate gateway SLOs for freshness, backlog, replay lag, protocol errors, lineage completeness, and site-state quality.
10. Export gateway events, site state, buffer records, replay validation, and SLO reports.
11. Use R to report gateway fleet reliability and aggregation quality.

## Engineering emphasis

The code is designed around practical gateway questions:

- Which devices are parented by which gateways?
- Do protocol translations preserve identity, time, units, and quality?
- Does aggregation disclose stale, missing, and low-confidence inputs?
- Can buffering survive outage without losing lineage?
- Does replay preserve ordering and prevent duplicate counting?
- Does selective uplink preserve enough context for upstream interpretation?
- Are gateway SLOs visible before the system silently degrades?
