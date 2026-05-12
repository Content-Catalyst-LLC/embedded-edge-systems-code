# Workflow Overview

This companion workflow turns cloud-edge coordination concepts into executable artifacts.

## Main computational path

1. Load responsibility, authority, workload-placement, synchronization, conflict-resolution, degraded-mode, rollout, security, and model-lifecycle manifests.
2. Simulate device, gateway, edge, regional, and cloud layers.
3. Score workload placement across layers.
4. Simulate cloud reachability and offline duration.
5. Apply local authority windows and degraded-mode policy.
6. Generate local edge decisions with policy and model versions.
7. Buffer and selectively uplink telemetry.
8. Compute state age, sync lag, buffer backlog, policy drift, model skew, and rollout convergence.
9. Validate conflict-resolution behavior.
10. Export hybrid event logs and summaries.
11. Use R to report fleet reliability, synchronization, version skew, rollout convergence, and degraded-mode behavior.

## Engineering emphasis

The code is designed around practical hybrid architecture questions:

- Which layer owns which responsibility?
- What can the edge do when the cloud is unavailable?
- How long is offline authority valid?
- Are cloud and edge policies still aligned?
- Are model versions approved, deployed, active, and decision-used?
- Can the cloud distinguish stale state from fresh state?
- Can buffered telemetry be replayed without losing lineage?
- Are reconciliation conflicts handled explicitly?
- Are rollout rings converging safely?
