-- Privacy-preserving local edge processing schema

CREATE TABLE IF NOT EXISTS edge_privacy_events (
    event_id TEXT PRIMARY KEY,
    site TEXT NOT NULL,
    device_id TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    raw_collection REAL NOT NULL CHECK (raw_collection BETWEEN 0 AND 1),
    identifiability REAL NOT NULL CHECK (identifiability BETWEEN 0 AND 1),
    retention_hours INTEGER NOT NULL,
    linkability REAL NOT NULL CHECK (linkability BETWEEN 0 AND 1),
    sharing_scope REAL NOT NULL CHECK (sharing_scope BETWEEN 0 AND 1),
    minimisation REAL NOT NULL CHECK (minimisation BETWEEN 0 AND 1),
    local_transformation REAL NOT NULL CHECK (local_transformation BETWEEN 0 AND 1),
    ephemeral_processing REAL NOT NULL CHECK (ephemeral_processing BETWEEN 0 AND 1),
    output_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS disclosure_records (
    disclosure_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    disclosed_output_type TEXT NOT NULL,
    upstream_transfer BOOLEAN NOT NULL,
    purpose TEXT NOT NULL,
    retention_hours INTEGER NOT NULL,
    transform_applied TEXT NOT NULL,
    disclosure_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES edge_privacy_events(event_id)
);

CREATE TABLE IF NOT EXISTS retention_policy (
    data_class TEXT PRIMARY KEY,
    default_retention_hours INTEGER NOT NULL,
    raw_retention_allowed BOOLEAN NOT NULL,
    upstream_transfer_allowed BOOLEAN NOT NULL,
    requires_user_notice BOOLEAN NOT NULL
);
