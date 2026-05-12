# Fault Containment and Quality Gating

Weak observations should not contaminate system-level interpretation.

## Typical gates

- `valid_fresh_synchronized`: eligible for normal aggregation, alerts, dashboards, and operational reporting.
- `stale`: historical-only; blocked from real-time alerting and live dashboard state.
- `low_confidence`: diagnostic or qualified trend use only.
- `sync_degraded`: blocked from event-propagation analysis and time-sensitive fusion.
- `coverage_degraded`: blocks unqualified system-level claims.
- `gateway_replay`: historical recovery only; not live status.
- `node_drift_warning`: reduce authority and schedule recalibration.
- `visibility_lost`: no current-state claim is allowed for affected zone.

Fault containment prevents monitoring-system failure from becoming a false claim about the monitored system.
