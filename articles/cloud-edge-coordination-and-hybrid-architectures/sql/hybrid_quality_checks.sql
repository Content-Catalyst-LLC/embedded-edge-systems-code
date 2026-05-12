-- Cloud-edge hybrid quality checks

-- Stale cloud state
SELECT timestamp, site_id, gateway_id, state_age_s
FROM hybrid_events
WHERE state_age_s > 120;

-- Sync lag
SELECT timestamp, site_id, gateway_id, sync_lag_s
FROM hybrid_events
WHERE sync_lag_s > 60;

-- Authority window violations
SELECT timestamp, site_id, gateway_id, offline_duration_s, authority_valid
FROM hybrid_events
WHERE authority_valid = FALSE;

-- Policy drift
SELECT timestamp, site_id, gateway_id, edge_policy_version, cloud_policy_version
FROM hybrid_events
WHERE edge_policy_version != cloud_policy_version;

-- Model version skew
SELECT timestamp, site_id, gateway_id, edge_model_version, approved_model_version, active_version, target_version
FROM hybrid_events
WHERE edge_model_version != approved_model_version OR active_version != target_version;

-- Reconciliation conflicts
SELECT timestamp, site_id, gateway_id, reconciliation_status
FROM hybrid_events
WHERE reconciliation_status IN ('conflict', 'hold_for_review', 'rollback_required');

-- Buffer backlog
SELECT timestamp, site_id, gateway_id, buffer_backlog
FROM hybrid_events
WHERE buffer_backlog > 200;
