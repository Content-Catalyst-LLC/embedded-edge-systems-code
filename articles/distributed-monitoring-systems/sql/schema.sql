CREATE TABLE IF NOT EXISTS node_inventory (
    node_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    coverage_zone TEXT NOT NULL,
    node_role TEXT NOT NULL,
    node_class TEXT NOT NULL,
    sensor_family TEXT NOT NULL,
    connectivity_state TEXT NOT NULL,
    health_state TEXT NOT NULL,
    calibration_state TEXT NOT NULL,
    clock_state TEXT NOT NULL,
    firmware_version TEXT NOT NULL,
    configuration_version TEXT NOT NULL,
    owner TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    battery_percent REAL NOT NULL,
    heartbeat_age_seconds REAL NOT NULL,
    expected_reporting_interval_seconds REAL NOT NULL,
    node_authority TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS topology_zones (
    coverage_zone TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    required_nodes INTEGER NOT NULL,
    min_reference_nodes INTEGER NOT NULL,
    criticality TEXT NOT NULL,
    claim_scope TEXT NOT NULL,
    area_required REAL NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS gateway_state (
    gateway_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    coverage_zone TEXT NOT NULL,
    connectivity_state TEXT NOT NULL,
    health_state TEXT NOT NULL,
    child_node_count INTEGER NOT NULL,
    child_nodes_reporting INTEGER NOT NULL,
    buffer_depth INTEGER NOT NULL,
    buffer_capacity INTEGER NOT NULL,
    mean_upload_latency_seconds REAL NOT NULL,
    active_rule_version TEXT NOT NULL,
    approved_rule_version TEXT NOT NULL,
    transformation_lineage_preserved BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS telemetry_records (
    event_id TEXT PRIMARY KEY,
    node_id TEXT NOT NULL,
    site_id TEXT NOT NULL,
    coverage_zone TEXT NOT NULL,
    gateway_id TEXT NOT NULL,
    sensor_family TEXT NOT NULL,
    event_time TEXT NOT NULL,
    upload_time TEXT NOT NULL,
    ingestion_time TEXT NOT NULL,
    processing_time TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    quality_state TEXT NOT NULL,
    calibration_state TEXT NOT NULL,
    clock_skew_ms REAL NOT NULL,
    sequence_number INTEGER NOT NULL,
    replay_batch_id TEXT,
    idempotency_key TEXT NOT NULL,
    duplicate_detected BOOLEAN NOT NULL,
    drop_reason TEXT,
    aggregation_candidate BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS aggregation_records (
    aggregation_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    coverage_zone TEXT NOT NULL,
    aggregation_type TEXT NOT NULL,
    source_event_ids TEXT NOT NULL,
    source_node_count INTEGER NOT NULL,
    required_node_count INTEGER NOT NULL,
    quality_state TEXT NOT NULL,
    confidence REAL NOT NULL,
    aggregation_time TEXT NOT NULL,
    lineage_complete BOOLEAN NOT NULL,
    inference_boundary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS incident_records (
    incident_id TEXT PRIMARY KEY,
    site_id TEXT NOT NULL,
    coverage_zone TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    detected_time TEXT NOT NULL,
    linked_events TEXT NOT NULL,
    monitoring_state TEXT NOT NULL,
    operator_action TEXT NOT NULL
);
