-- Cyber-physical systems and hardware integration evidence schema

CREATE TABLE IF NOT EXISTS cps_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    subsystem TEXT NOT NULL,
    operating_mode TEXT NOT NULL,
    sensor_age_ms REAL NOT NULL,
    measurement REAL NOT NULL,
    estimate REAL NOT NULL,
    candidate_command REAL NOT NULL,
    filtered_command REAL NOT NULL,
    actuator_saturated BOOLEAN NOT NULL,
    deadline_missed BOOLEAN NOT NULL,
    loop_jitter_ms REAL NOT NULL,
    deadline_slack_ms REAL NOT NULL,
    interface_error BOOLEAN NOT NULL,
    safety_state TEXT NOT NULL,
    total_uncertainty REAL NOT NULL,
    uncertainty_budget REAL NOT NULL,
    recovery_event BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS interface_contracts (
    contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
    signal_name TEXT NOT NULL,
    physical_unit TEXT NOT NULL,
    valid_min REAL,
    valid_max REAL,
    maximum_age_ms REAL,
    failure_behavior TEXT NOT NULL,
    safety_semantics TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS uncertainty_budget_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    sensor_error REAL NOT NULL,
    calibration_error REAL NOT NULL,
    quantization_error REAL NOT NULL,
    estimation_error REAL NOT NULL,
    model_error REAL NOT NULL,
    total_uncertainty REAL NOT NULL,
    uncertainty_budget REAL NOT NULL,
    within_budget BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS requirements_traceability (
    trace_id INTEGER PRIMARY KEY AUTOINCREMENT,
    requirement_id TEXT NOT NULL,
    requirement TEXT NOT NULL,
    implementation_artifact TEXT NOT NULL,
    validation_test TEXT NOT NULL,
    operational_signal TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hil_validation_records (
    hil_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    test_case TEXT NOT NULL,
    target_interface TEXT NOT NULL,
    expected_behavior TEXT NOT NULL,
    observed_behavior TEXT,
    passed BOOLEAN
);
