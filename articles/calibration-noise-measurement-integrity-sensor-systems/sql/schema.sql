CREATE TABLE IF NOT EXISTS sensor_inventory (
    sensor_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    sensor_family TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    unit TEXT NOT NULL,
    valid_min REAL NOT NULL,
    valid_max REAL NOT NULL,
    owner TEXT NOT NULL,
    calibration_version TEXT NOT NULL,
    firmware_version TEXT NOT NULL,
    filter_version TEXT NOT NULL,
    traceability_record_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS calibration_records (
    calibration_version TEXT PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    gain_coefficient REAL NOT NULL,
    offset_coefficient REAL NOT NULL,
    calibration_date TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    reference_device_id TEXT NOT NULL,
    uncertainty_statement TEXT NOT NULL,
    coefficient_checksum TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS measurement_records (
    measurement_id TEXT PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    sensor_family TEXT NOT NULL,
    raw_value REAL NOT NULL,
    calibrated_value REAL NOT NULL,
    expanded_uncertainty REAL NOT NULL,
    snr_db REAL NOT NULL,
    quality_state TEXT NOT NULL,
    allowed_uses TEXT NOT NULL,
    calibration_version TEXT NOT NULL,
    firmware_version TEXT NOT NULL,
    filter_version TEXT NOT NULL,
    acquisition_time TEXT NOT NULL,
    processing_time TEXT NOT NULL,
    lineage_complete BOOLEAN NOT NULL,
    traceability_complete BOOLEAN NOT NULL
);
