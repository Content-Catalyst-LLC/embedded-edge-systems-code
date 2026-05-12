-- Edge analytics and local data processing evidence schema

CREATE TABLE IF NOT EXISTS analytics_events (
    event_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    site_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    signal_id TEXT NOT NULL,
    sensor_id TEXT NOT NULL,
    signal_family TEXT NOT NULL,
    feature_version TEXT NOT NULL,
    rule_version TEXT NOT NULL,
    window_id TEXT NOT NULL,
    window_start TEXT NOT NULL,
    window_end TEXT NOT NULL,
    acquisition_time TEXT NOT NULL,
    processing_time TEXT NOT NULL,
    buffer_entry_time TEXT NOT NULL,
    upload_time TEXT,
    upstream_ingest_time TEXT,
    raw_bytes INTEGER NOT NULL,
    uplink_bytes INTEGER NOT NULL,
    local_latency_ms REAL NOT NULL,
    freshness_s REAL NOT NULL,
    freshness_threshold_s REAL NOT NULL,
    missing_sample_rate REAL NOT NULL,
    feature_complete BOOLEAN NOT NULL,
    event_detected BOOLEAN NOT NULL,
    event_state TEXT NOT NULL,
    uplink_mode TEXT NOT NULL,
    buffer_backlog INTEGER NOT NULL,
    replay_lag_s REAL NOT NULL,
    lineage_complete BOOLEAN NOT NULL,
    drop_reason TEXT NOT NULL,
    quality_flag TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    replay_batch_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS signal_windows (
    window_id TEXT PRIMARY KEY,
    signal_id TEXT NOT NULL,
    sensor_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    window_start TEXT NOT NULL,
    window_end TEXT NOT NULL,
    sample_count INTEGER NOT NULL,
    expected_sample_count INTEGER NOT NULL,
    missing_sample_rate REAL NOT NULL,
    rms REAL,
    peak REAL,
    crest_factor REAL,
    spectral_energy REAL,
    bandpower_low REAL,
    bandpower_high REAL,
    quality_flag TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS replay_records (
    event_id TEXT NOT NULL,
    replay_batch_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    event_time TEXT NOT NULL,
    processing_time TEXT NOT NULL,
    upload_time TEXT,
    upstream_ingest_time TEXT,
    late_arrival BOOLEAN NOT NULL,
    duplicate_detected BOOLEAN NOT NULL,
    gap_detected BOOLEAN NOT NULL,
    correction_record BOOLEAN NOT NULL,
    reconciliation_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS deployment_readiness_results (
    check_id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_name TEXT NOT NULL,
    passed BOOLEAN NOT NULL,
    evidence_path TEXT,
    notes TEXT
);
