-- Embedded and Edge Systems Telemetry Schema
-- -----------------------------------------
-- This schema supports device registry, sensors, telemetry, calibration,
-- local inference scores, and edge-generated alerts.

CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT PRIMARY KEY,
    device_type TEXT NOT NULL,
    hardware_platform TEXT NOT NULL,
    firmware_version TEXT NOT NULL,
    deployment_region TEXT NOT NULL,
    installed_at TEXT NOT NULL,
    active INTEGER NOT NULL CHECK (active IN (0, 1))
);

CREATE TABLE IF NOT EXISTS sensors (
    sensor_id TEXT PRIMARY KEY,
    device_id TEXT NOT NULL,
    sensor_type TEXT NOT NULL,
    unit TEXT NOT NULL,
    sampling_interval_seconds INTEGER NOT NULL,
    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE IF NOT EXISTS calibration_records (
    calibration_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id TEXT NOT NULL,
    calibrated_at TEXT NOT NULL,
    calibration_method TEXT NOT NULL,
    offset_value REAL NOT NULL,
    scale_factor REAL NOT NULL,
    technician_or_process TEXT NOT NULL,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

CREATE TABLE IF NOT EXISTS telemetry_readings (
    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    observed_value REAL NOT NULL,
    battery_voltage REAL,
    signal_quality REAL,
    local_inference_score REAL,
    transmitted INTEGER NOT NULL CHECK (transmitted IN (0, 1)),
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);

CREATE TABLE IF NOT EXISTS edge_alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    observed_value REAL NOT NULL,
    threshold_value REAL NOT NULL,
    handled_locally INTEGER NOT NULL CHECK (handled_locally IN (0, 1)),
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id)
);
