# Worked Example: Industrial Site Gateway and Aggregation Layer

This example models an industrial site with motor controllers, temperature sensors, vibration sensors, power meters, and legacy field devices.

## System behavior

1. Child devices report local measurements over heterogeneous protocols.
2. A gateway maps protocol-specific fields into normalized telemetry.
3. The gateway buffers events when upstream connectivity is degraded.
4. An aggregation layer computes site-level equipment-health state.
5. Selective uplink forwards summaries, incidents, and priority diagnostics.
6. Local policy may trigger alarms before upstream review.
7. On reconnect, buffered records are replayed with sequence IDs and idempotency keys.
8. Upstream systems receive delayed records with acquisition, gateway receipt, aggregation, upload, and ingestion times.

## Key records

- child device ID
- parent gateway ID
- protocol address
- acquisition time
- gateway receipt time
- aggregation time
- upload time
- upstream ingestion time
- quality flag
- protocol error context
- replay batch ID
- idempotency key
- selective forwarding decision
- aggregation lineage
