-- Edge analytics quality checks

-- Stale outputs
SELECT event_id, site_id, gateway_id, signal_id, freshness_s, freshness_threshold_s
FROM analytics_events
WHERE freshness_s > freshness_threshold_s;

-- Feature incompleteness
SELECT event_id, site_id, gateway_id, signal_id, window_id, missing_sample_rate, feature_complete
FROM analytics_events
WHERE feature_complete = FALSE OR missing_sample_rate > 0.05;

-- High local latency
SELECT event_id, site_id, gateway_id, signal_id, local_latency_ms
FROM analytics_events
WHERE local_latency_ms > 100;

-- Buffer pressure
SELECT event_id, site_id, gateway_id, buffer_backlog
FROM analytics_events
WHERE buffer_backlog > 200;

-- Replay lag
SELECT event_id, site_id, gateway_id, replay_lag_s
FROM analytics_events
WHERE replay_lag_s > 300;

-- Incomplete lineage
SELECT event_id, site_id, gateway_id, signal_id, window_id
FROM analytics_events
WHERE lineage_complete = FALSE;

-- Duplicate replay
SELECT event_id, replay_batch_id, idempotency_key
FROM replay_records
WHERE duplicate_detected = TRUE;

-- Partial backfill / gap records
SELECT event_id, replay_batch_id, sequence_number, reconciliation_status
FROM replay_records
WHERE gap_detected = TRUE OR reconciliation_status IN ('gap_recorded', 'correction_appended');
