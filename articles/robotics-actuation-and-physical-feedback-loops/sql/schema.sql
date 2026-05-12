-- Robotics, actuation, and feedback-loop evidence schema

CREATE TABLE IF NOT EXISTS robot_profiles (
    robot_id TEXT PRIMARY KEY,
    robot_class TEXT NOT NULL,
    control_mode TEXT NOT NULL,
    target_loop_period_ms REAL NOT NULL,
    max_allowed_jitter_ms REAL NOT NULL,
    watchdog_enabled BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS actuator_profiles (
    actuator_id TEXT PRIMARY KEY,
    joint_id TEXT NOT NULL,
    max_torque_nm REAL NOT NULL,
    max_speed_rad_s REAL NOT NULL,
    max_current_a REAL NOT NULL,
    thermal_limit_c REAL NOT NULL,
    position_resolution_rad REAL NOT NULL,
    backlash_rad REAL NOT NULL,
    command_limit REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS control_loop_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    robot_id TEXT NOT NULL,
    joint_id TEXT NOT NULL,
    task_mode TEXT NOT NULL,
    setpoint REAL NOT NULL,
    measured_position REAL NOT NULL,
    estimated_position REAL NOT NULL,
    tracking_error REAL NOT NULL,
    command REAL NOT NULL,
    actuator_current_a REAL NOT NULL,
    loop_jitter_ms REAL NOT NULL,
    saturated BOOLEAN NOT NULL,
    safety_state TEXT NOT NULL,
    fault_state TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS estimator_residuals (
    residual_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    robot_id TEXT NOT NULL,
    joint_id TEXT NOT NULL,
    predicted_measurement REAL NOT NULL,
    observed_measurement REAL NOT NULL,
    residual REAL NOT NULL,
    residual_band TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS safety_events (
    safety_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    robot_id TEXT NOT NULL,
    joint_id TEXT,
    safety_state TEXT NOT NULL,
    violation_type TEXT NOT NULL,
    measured_value REAL,
    threshold REAL,
    action_taken TEXT NOT NULL
);
