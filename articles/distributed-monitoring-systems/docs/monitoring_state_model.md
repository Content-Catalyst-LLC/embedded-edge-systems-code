# Monitoring State Model

Distributed monitoring dashboards must distinguish monitored-system conditions from monitoring-system conditions.

## States

- `observed_valid`: fresh, synchronized, quality-qualified data are available.
- `observed_low_confidence`: data are present but quality, calibration, uncertainty, or confidence is weakened.
- `observed_stale`: data are present but older than the operational freshness requirement.
- `coverage_degraded`: required zones or node roles are missing or below threshold.
- `gateway_degraded`: gateway is delaying, buffering, dropping, or losing child-node visibility.
- `sync_degraded`: clock drift or timestamp uncertainty exceeds the threshold for the use case.
- `backfill_replay`: delayed records are being uploaded after outage or buffering.
- `visibility_lost`: no valid current-state conclusion can be made for the affected zone.
