-- Autonomous systems and edge intelligence evidence schema

CREATE TABLE IF NOT EXISTS autonomy_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    mission_type TEXT NOT NULL,
    autonomy_level TEXT NOT NULL,
    observation TEXT NOT NULL,
    belief_state TEXT NOT NULL,
    decision_confidence REAL NOT NULL CHECK (decision_confidence BETWEEN 0 AND 1),
    candidate_action TEXT NOT NULL,
    filtered_action TEXT NOT NULL,
    action_type TEXT NOT NULL,
    latency_ms REAL NOT NULL,
    latency_budget_ms REAL NOT NULL,
    safety_state TEXT NOT NULL,
    human_intervention_required BOOLEAN NOT NULL,
    input_drift_score REAL NOT NULL CHECK (input_drift_score BETWEEN 0 AND 1),
    confidence_drift_score REAL NOT NULL CHECK (confidence_drift_score BETWEEN 0 AND 1),
    mission_outcome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS belief_state_records (
    belief_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    clear_path_probability REAL NOT NULL,
    obstacle_probability REAL NOT NULL,
    hazard_probability REAL NOT NULL,
    belief_state TEXT NOT NULL,
    belief_freshness_ms REAL NOT NULL,
    decision_confidence REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS runtime_assurance_records (
    assurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    candidate_action TEXT NOT NULL,
    filtered_action TEXT NOT NULL,
    allowed BOOLEAN NOT NULL,
    reason_code TEXT NOT NULL,
    autonomy_level TEXT NOT NULL,
    safety_state TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drift_reports (
    drift_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    device_id TEXT NOT NULL,
    input_drift_score REAL NOT NULL,
    confidence_drift_score REAL NOT NULL,
    fallback_rate REAL,
    intervention_rate REAL,
    latency_violation_rate REAL,
    safety_event_rate REAL
);
