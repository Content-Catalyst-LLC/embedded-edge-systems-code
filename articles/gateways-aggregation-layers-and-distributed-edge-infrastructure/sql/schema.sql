-- Gateway, aggregation layer, and distributed edge infrastructure evidence schema

CREATE TABLE IF NOT EXISTS child_devices (
    device_id TEXT PRIMARY KEY,
    gateway_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    protocol_family TEXT NOT NULL,
    protocol_address TEXT NOT NULL,
    expected_heartbeat_s REAL NOT NULL,
    firmware_version TEXT NOT NULL,
    physical_unit TEXT NOT NULL,
    device_role TEXT NOT NULL,
    criticality TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS gateway_events (
    event_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    site_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    protocol_family TEXT NOT NULL,
    local_acquisition_time TEXT NOT NULL,
    gateway_receipt_time TEXT NOT NULL,
    aggregation_time TEXT NOT NULL,
    upload_time TEXT NOT NULL,
    upstream_ingest_time TEXT NOT NULL,
    measurement REAL NOT NULL,
    unit TEXT NOT NULL,
    quality_flag TEXT NOT NULL,
    device_freshness_s REAL NOT NULL,
    child_device_status TEXT NOT NULL,
    protocol_error BOOLEAN NOT NULL,
    buffer_backlog INTEGER NOT NULL,
    replay_lag_s REAL NOT NULL,
    forwarded_upstream BOOLEAN NOT NULL,
    lineage_complete BOOLEAN NOT NULL,
    selective_forwarding_reason TEXT NOT NULL,
    policy_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS site_state_events (
    site_state_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    site_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    aggregation_window_s REAL NOT NULL,
    contributing_devices INTEGER NOT NULL,
    expected_devices INTEGER NOT NULL,
    missing_child_count INTEGER NOT NULL,
    stale_device_count INTEGER NOT NULL,
    protocol_error_count INTEGER NOT NULL,
    lineage_gap_count INTEGER NOT NULL,
    site_quality_score REAL NOT NULL,
    aggregation_confidence REAL NOT NULL,
    forwarded_upstream BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS replay_events (
    event_id TEXT NOT NULL,
    replay_batch_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    local_acquisition_time TEXT NOT NULL,
    upstream_ingest_time TEXT NOT NULL,
    late_arrival BOOLEAN NOT NULL,
    duplicate_detected BOOLEAN NOT NULL,
    gap_detected BOOLEAN NOT NULL,
    reconciliation_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS protocol_errors (
    error_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    site_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    device_id TEXT NOT NULL,
    protocol_family TEXT NOT NULL,
    error_type TEXT NOT NULL,
    error_count INTEGER NOT NULL,
    retry_count INTEGER NOT NULL,
    resolved BOOLEAN NOT NULL
);
