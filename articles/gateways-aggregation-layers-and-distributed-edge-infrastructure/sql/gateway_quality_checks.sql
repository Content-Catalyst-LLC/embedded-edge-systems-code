-- Gateway and aggregation quality checks

-- Stale child devices
SELECT timestamp, site_id, gateway_id, device_id, device_freshness_s, child_device_status
FROM gateway_events
WHERE device_freshness_s > 60 OR child_device_status = 'missing';

-- Protocol errors
SELECT timestamp, site_id, gateway_id, device_id, protocol_family
FROM gateway_events
WHERE protocol_error = TRUE;

-- Buffer pressure
SELECT timestamp, site_id, gateway_id, buffer_backlog
FROM gateway_events
WHERE buffer_backlog > 200;

-- Replay lag
SELECT event_id, site_id, gateway_id, replay_lag_s
FROM gateway_events
WHERE replay_lag_s > 120;

-- Incomplete lineage
SELECT event_id, site_id, gateway_id, device_id
FROM gateway_events
WHERE lineage_complete = FALSE;

-- Low site quality
SELECT site_state_id, site_id, gateway_id, site_quality_score, aggregation_confidence
FROM site_state_events
WHERE site_quality_score < 0.80 OR aggregation_confidence < 0.80;

-- Duplicate replay
SELECT event_id, replay_batch_id, idempotency_key
FROM replay_events
WHERE duplicate_detected = TRUE;
