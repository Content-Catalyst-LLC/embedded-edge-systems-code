-- Cloud-edge coordination and hybrid architecture evidence schema

CREATE TABLE IF NOT EXISTS hybrid_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    site_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    operating_mode TEXT NOT NULL,
    cloud_reachable BOOLEAN NOT NULL,
    offline_duration_s REAL NOT NULL,
    state_age_s REAL NOT NULL,
    sync_lag_s REAL NOT NULL,
    buffer_backlog INTEGER NOT NULL,
    edge_policy_version TEXT NOT NULL,
    cloud_policy_version TEXT NOT NULL,
    edge_model_version TEXT NOT NULL,
    approved_model_version TEXT NOT NULL,
    target_version TEXT NOT NULL,
    active_version TEXT NOT NULL,
    local_decision_count INTEGER NOT NULL,
    reconciliation_status TEXT NOT NULL,
    degraded_mode BOOLEAN NOT NULL,
    authority_valid BOOLEAN NOT NULL,
    selective_uplink_rate REAL NOT NULL,
    rollout_ring TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS state_lineage_events (
    lineage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    local_acquisition_time TEXT NOT NULL,
    local_decision_time TEXT NOT NULL,
    edge_persist_time TEXT NOT NULL,
    sync_time TEXT NOT NULL,
    cloud_ingest_time TEXT NOT NULL,
    cloud_interpret_time TEXT NOT NULL,
    edge_policy_version TEXT NOT NULL,
    cloud_policy_version TEXT NOT NULL,
    edge_model_version TEXT NOT NULL,
    approved_model_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rollout_nodes (
    node_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    rollout_ring TEXT NOT NULL,
    eligible BOOLEAN NOT NULL,
    target_version TEXT NOT NULL,
    deployed_version TEXT NOT NULL,
    active_version TEXT NOT NULL,
    decision_used_version TEXT NOT NULL,
    health_status TEXT NOT NULL,
    cloud_reachable BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS reconciliation_records (
    reconciliation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    site_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    conflict_type TEXT NOT NULL,
    resolution_action TEXT NOT NULL,
    preserved_local_evidence BOOLEAN NOT NULL,
    cloud_interpretation_added BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS authority_records (
    authority_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    offline_duration_s REAL NOT NULL,
    authority_window_s REAL NOT NULL,
    authority_valid BOOLEAN NOT NULL,
    fallback_action TEXT
);
