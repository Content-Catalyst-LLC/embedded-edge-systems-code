-- Edge infrastructure governance schema

CREATE TABLE IF NOT EXISTS edge_assets (
    device_id TEXT PRIMARY KEY,
    site TEXT NOT NULL,
    vendor TEXT NOT NULL,
    device_class TEXT NOT NULL,
    standard_profile TEXT NOT NULL,
    support_state TEXT NOT NULL,
    firmware_version TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS governance_scores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    protocol_conformance REAL NOT NULL CHECK (protocol_conformance BETWEEN 0 AND 1),
    semantic_alignment REAL NOT NULL CHECK (semantic_alignment BETWEEN 0 AND 1),
    lifecycle_control REAL NOT NULL CHECK (lifecycle_control BETWEEN 0 AND 1),
    security_baseline REAL NOT NULL CHECK (security_baseline BETWEEN 0 AND 1),
    operational_accountability REAL NOT NULL CHECK (operational_accountability BETWEEN 0 AND 1),
    unmanaged_divergence REAL NOT NULL CHECK (unmanaged_divergence BETWEEN 0 AND 1),
    governance_score REAL NOT NULL,
    risk_band TEXT NOT NULL,
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES edge_assets(device_id)
);

CREATE TABLE IF NOT EXISTS telemetry_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    quality_flag TEXT NOT NULL,
    FOREIGN KEY (device_id) REFERENCES edge_assets(device_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_events (
    lifecycle_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT,
    evidence_uri TEXT,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES edge_assets(device_id)
);
