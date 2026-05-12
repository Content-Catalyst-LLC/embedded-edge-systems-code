-- Device lifecycle and OTA updating evidence schema

CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT PRIMARY KEY,
    site TEXT NOT NULL,
    vendor TEXT NOT NULL,
    device_class TEXT NOT NULL,
    hardware_rev TEXT NOT NULL,
    current_firmware TEXT NOT NULL,
    support_state TEXT NOT NULL,
    rollout_ring TEXT NOT NULL,
    last_checkin_hours INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS update_packages (
    package_id TEXT PRIMARY KEY,
    target_firmware TEXT NOT NULL,
    device_class TEXT NOT NULL,
    hardware_rev_required TEXT NOT NULL,
    package_type TEXT NOT NULL,
    signature_valid BOOLEAN NOT NULL,
    rollback_supported BOOLEAN NOT NULL,
    release_channel TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ota_readiness_scores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    package_id TEXT,
    identity_assurance REAL NOT NULL CHECK (identity_assurance BETWEEN 0 AND 1),
    compatibility_match REAL NOT NULL CHECK (compatibility_match BETWEEN 0 AND 1),
    package_integrity REAL NOT NULL CHECK (package_integrity BETWEEN 0 AND 1),
    validation_status REAL NOT NULL CHECK (validation_status BETWEEN 0 AND 1),
    rollback_readiness REAL NOT NULL CHECK (rollback_readiness BETWEEN 0 AND 1),
    observability REAL NOT NULL CHECK (observability BETWEEN 0 AND 1),
    lifecycle_drift REAL NOT NULL CHECK (lifecycle_drift BETWEEN 0 AND 1),
    ota_readiness_score REAL NOT NULL,
    rollout_decision TEXT NOT NULL,
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(device_id),
    FOREIGN KEY (package_id) REFERENCES update_packages(package_id)
);

CREATE TABLE IF NOT EXISTS deployment_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    package_id TEXT NOT NULL,
    phase TEXT NOT NULL,
    status TEXT NOT NULL,
    error_code TEXT,
    FOREIGN KEY (device_id) REFERENCES devices(device_id),
    FOREIGN KEY (package_id) REFERENCES update_packages(package_id)
);

CREATE TABLE IF NOT EXISTS lifecycle_events (
    lifecycle_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT,
    evidence_uri TEXT,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
