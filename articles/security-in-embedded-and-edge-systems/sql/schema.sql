-- Embedded and edge security evidence schema

CREATE TABLE IF NOT EXISTS device_security_profiles (
    device_id TEXT PRIMARY KEY,
    site TEXT NOT NULL,
    device_class TEXT NOT NULL,
    hardware_trust REAL NOT NULL CHECK (hardware_trust BETWEEN 0 AND 1),
    boot_integrity REAL NOT NULL CHECK (boot_integrity BETWEEN 0 AND 1),
    identity_strength REAL NOT NULL CHECK (identity_strength BETWEEN 0 AND 1),
    update_readiness REAL NOT NULL CHECK (update_readiness BETWEEN 0 AND 1),
    runtime_isolation REAL NOT NULL CHECK (runtime_isolation BETWEEN 0 AND 1),
    monitoring_maturity REAL NOT NULL CHECK (monitoring_maturity BETWEEN 0 AND 1),
    exposure REAL NOT NULL CHECK (exposure BETWEEN 0 AND 1),
    lifecycle_drift REAL NOT NULL CHECK (lifecycle_drift BETWEEN 0 AND 1),
    support_state TEXT NOT NULL,
    firmware_version TEXT NOT NULL,
    secure_boot BOOLEAN NOT NULL,
    rollback_ready BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS security_readiness_scores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    security_readiness_score REAL NOT NULL,
    risk_band TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES device_security_profiles(device_id)
);

CREATE TABLE IF NOT EXISTS security_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES device_security_profiles(device_id)
);

CREATE TABLE IF NOT EXISTS credential_inventory (
    credential_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    credential_type TEXT NOT NULL,
    issued_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    rotation_state TEXT NOT NULL,
    FOREIGN KEY (device_id) REFERENCES device_security_profiles(device_id)
);

CREATE TABLE IF NOT EXISTS recovery_records (
    recovery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    recovery_type TEXT NOT NULL,
    previous_state TEXT,
    recovered_state TEXT NOT NULL,
    recovery_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES device_security_profiles(device_id)
);
