# Workflow Overview

This companion workflow models an IoT sensor fleet as a managed evidence system.

## Main computational path

1. Load device inventory, gateway state, telemetry records, identity manifests, topic maps, buffering/replay policies, security-control profile, command-authority policy, OTA rollout plan, and readiness config.
2. Compute freshness from event time and processing time.
3. Evaluate usable telemetry based on freshness, quality state, trust state, and duplicate replay.
4. Detect firmware skew, configuration skew, schema skew, and trust-state gaps.
5. Validate replay records with idempotency keys and replay batches.
6. Evaluate command authority against trust, freshness, local safety, and command scope.
7. Score fleet governability.
8. Summarize fleet health by site, gateway, device class, and sensor family.
9. Generate deployment readiness evidence.
