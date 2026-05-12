-- Embedded control systems evidence schema

CREATE TABLE IF NOT EXISTS control_loop_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    loop_id TEXT NOT NULL,
    operating_mode TEXT NOT NULL,
    setpoint REAL NOT NULL,
    measurement REAL NOT NULL,
    estimate REAL NOT NULL,
    control_error REAL NOT NULL,
    candidate_command REAL NOT NULL,
    filtered_command REAL NOT NULL,
    saturated BOOLEAN NOT NULL,
    deadline_missed BOOLEAN NOT NULL,
    loop_jitter_ms REAL NOT NULL,
    deadline_slack_ms REAL NOT NULL,
    safety_state TEXT NOT NULL,
    supervisory_state TEXT NOT NULL,
    safety_filter_reason TEXT NOT NULL,
    current_a REAL,
    temperature_c REAL
);

CREATE TABLE IF NOT EXISTS timing_budget_records (
    timing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loop_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    budget_ms REAL NOT NULL,
    observed_ms REAL,
    within_budget BOOLEAN
);

CREATE TABLE IF NOT EXISTS estimator_residuals (
    residual_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    loop_id TEXT NOT NULL,
    predicted_measurement REAL NOT NULL,
    observed_measurement REAL NOT NULL,
    residual REAL NOT NULL,
    residual_band TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS command_filter_records (
    filter_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    loop_id TEXT NOT NULL,
    candidate_command REAL NOT NULL,
    filtered_command REAL NOT NULL,
    allowed BOOLEAN NOT NULL,
    reason_code TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supervisory_transitions (
    transition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    loop_id TEXT NOT NULL,
    from_state TEXT NOT NULL,
    to_state TEXT NOT NULL,
    reason_code TEXT NOT NULL
);
